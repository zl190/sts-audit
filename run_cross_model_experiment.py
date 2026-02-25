#!/usr/bin/env python3
"""
Cross-Model Architectural Quality Experiment Runner
Pre-registered: commit 05f8902

Runs 3 models × 3 conditions × 3 tasks × N reps, audits each output
with sts_checker.py, and aggregates results.

Usage:
    python run_cross_model_experiment.py                  # full experiment
    python run_cross_model_experiment.py --models claude   # single model
    python run_cross_model_experiment.py --conditions U    # single condition
    python run_cross_model_experiment.py --dry-run         # print plan without calling APIs
"""

import argparse
import json
import os
import random
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "cases" / "cross_model"
RESULTS_FILE_V1 = ROOT / "records" / "cross_model_results.json"
RESULTS_FILE = ROOT / "records" / "cross_model_results_v2.json"
STS_CHECKER = ROOT / "sts_checker.py"

MODELS = {
    # --- Tier A: Pre-registered models (original experiment) ---
    "claude": {
        "id": "claude-sonnet-4-20250514",
        "env_key": "ANTHROPIC_API_KEY",
        "provider": "anthropic",
        "tier": "A",
    },
    "gpt4o": {
        "id": "gpt-4o-2024-11-20",  # pinned snapshot, not alias
        "env_key": "OPENAI_API_KEY",
        "provider": "openai",
        "tier": "A",
    },
    # --- Tier B: Current SOTA flagships ---
    "gemini_pro": {
        "id": "gemini-2.5-pro",  # replaces gemini-2.5-flash (known truncation bug)
        "env_key": "GOOGLE_API_KEY",
        "provider": "google",
        "tier": "B",
    },
    "claude_sonnet45": {
        "id": "claude-sonnet-4-5-20250929",
        "env_key": "ANTHROPIC_API_KEY",
        "provider": "anthropic",
        "tier": "B",
    },
    "gpt5": {
        "id": "gpt-5",
        "env_key": "OPENAI_API_KEY",
        "provider": "openai",
        "tier": "B",
    },
    # --- Tier C: Budget / lightweight ---
    "claude_haiku": {
        "id": "claude-haiku-4-5-20251001",
        "env_key": "ANTHROPIC_API_KEY",
        "provider": "anthropic",
        "tier": "C",
    },
    "gpt5_mini": {
        "id": "gpt-5-mini",
        "env_key": "OPENAI_API_KEY",
        "provider": "openai",
        "tier": "C",
    },
}

# Pre-registration deviation note:
# Pre-registered (commit 05f8902): claude-sonnet-4-20250514, gpt-4o, gemini-2.0-flash
# Changes:
#   gpt-4o -> gpt-4o-2024-11-20: pinned to dated snapshot (same model, prevents alias drift)
#   gemini-2.0-flash -> gemini-2.5-flash: forced sub, original returns 404
#     ("This model is no longer available to new users", Feb 2026)
# Extended experiment (exploratory, not pre-registered):
#   gemini-2.5-flash -> gemini-2.5-pro: Flash had 40% truncation rate (known thinking-token bug)
#   Added: claude-sonnet-4-5, gpt-5, claude-haiku-4-5, gpt-5-mini
#   These 5 models are Tiers B+C (robustness analysis), NOT primary pre-registered results

# Per-provider delays (seconds) to avoid rate limits
PROVIDER_DELAYS = {"anthropic": 2, "openai": 1, "google": 10}

# N per cell; override for specific (model, condition) pairs
DEFAULT_N = 5
N_OVERRIDES = {
    ("claude", "D"): 10,  # disclosure test needs more power
}

# ---------------------------------------------------------------------------
# Task prompts (from pre-registered design)
# ---------------------------------------------------------------------------

TASKS = {
    "task1_bookstore": """Write a Python program for an online bookstore order system.

Requirements:
- Process orders with items that have: title, category, price, quantity
- Categories: fiction, textbook, children, comic
- Each category has quantity-based discount tiers (e.g., fiction: 10% base, 15% for 3+, 20% for 5+)
- Order-level threshold discount: 3% for orders over $300, 5% for orders over $500
- Save orders to a JSON file
- Send notifications (email, SMS, inventory alert) after order
- Print a formatted receipt

The program should be runnable with a demo in __main__.""",

    "task2_mall": """Write a Python program for a shopping mall checkout system.

Requirements:
- Support membership tiers: Normal, Silver, Gold, Platinum
- Each tier has a discount rate (e.g., Normal: 0%, Silver: 5%, Gold: 12%, Platinum: 20%)
- Products can have individual product-level discounts
- Shopping cart with add/remove functionality
- Checkout calculates: original total, after product discounts, after member discount, total saved
- Print a formatted checkout receipt

The program should be runnable with a demo in __main__.""",

    "task3_inventory": """Write a Python program for a warehouse inventory management system.

Requirements:
- Track products by SKU with name, price, and stock quantity
- Process orders with priority levels (normal, urgent, bulk) affecting pricing
- Urgent orders: 10% surcharge; Bulk orders: 15% discount (capped at 25%)
- Low stock alerts when quantity falls below reorder threshold
- Inter-warehouse stock transfers
- Reports: inventory summary, low stock report, valuation report, transaction history
- Save/load inventory state to JSON file

The program should be runnable with a demo in __main__.""",
}

CONDITION_ADDENDUM = {
    "U": "",  # unconstrained — no addendum
    "D": """

Note: Your code will be evaluated by an automated architectural quality audit that measures cyclomatic complexity, architectural separation of concerns, and API currency. Code receives a PASS or FAIL verdict based on threshold values for each metric.""",
    "S": """

Architecture requirements:
- Separate business logic from presentation: create service.py (pure logic, zero print statements) and views.py (all UI/display)
- Use Strategy pattern for discount calculations
- Use Observer pattern for notifications
- Use dataclasses or named tuples for data transfer between layers
- No print() statements in service.py""",
}

SYSTEM_PROMPT = "You are a Python developer. Write clean, complete, runnable code. Output ONLY the Python code — no explanations, no markdown formatting, just the code. If creating multiple files, separate them with a comment line: # === FILENAME: <name> ==="


# ---------------------------------------------------------------------------
# API callers
# ---------------------------------------------------------------------------

def call_with_retry(caller, model_id: str, prompt: str, provider: str = "", max_retries: int = 5) -> dict:
    """Call an API with exponential backoff on rate limits."""
    # Gemini free tier is 15 RPM — needs longer waits
    base_wait = 10 if provider == "google" else 2
    for attempt in range(max_retries):
        try:
            return caller(model_id, prompt)
        except Exception as e:
            err_str = str(e).lower()
            if any(kw in err_str for kw in ("rate", "429", "quota", "resource_exhausted", "503", "unavailable", "overloaded", "500")):
                wait = base_wait * (2 ** attempt) + random.uniform(0, 1)
                print(f"  Rate limited, retrying in {wait:.1f}s (attempt {attempt+1}/{max_retries})")
                time.sleep(wait)
            else:
                raise
    raise Exception(f"Rate limited after {max_retries} retries")


def call_anthropic(model_id: str, prompt: str) -> dict:
    """Call Anthropic API. Returns {text, model, tokens_in, tokens_out}."""
    import anthropic
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=model_id,
        max_tokens=8192,
        temperature=0,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return {
        "text": resp.content[0].text,
        "model": resp.model,
        "tokens_in": resp.usage.input_tokens,
        "tokens_out": resp.usage.output_tokens,
        "stop_reason": resp.stop_reason,
    }


def call_openai(model_id: str, prompt: str) -> dict:
    """Call OpenAI API. Returns {text, model, tokens_in, tokens_out}."""
    import openai
    client = openai.OpenAI()

    # GPT-5 series uses max_completion_tokens and may reject temperature=0
    params = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    }
    if model_id.startswith("gpt-5"):
        params["max_completion_tokens"] = 8192
        # Reasoning models may not accept temperature=0; omit it
        # Pre-registration deviation: GPT-5 uses default temperature
    else:
        params["max_tokens"] = 8192
        params["temperature"] = 0

    resp = client.chat.completions.create(**params)
    choice = resp.choices[0]
    return {
        "text": choice.message.content,
        "model": resp.model,
        "tokens_in": resp.usage.prompt_tokens,
        "tokens_out": resp.usage.completion_tokens,
        "stop_reason": choice.finish_reason,
    }


def call_google(model_id: str, prompt: str) -> dict:
    """Call Google Gemini API. Returns {text, model, tokens_in, tokens_out}."""
    from google import genai
    from google.genai.types import GenerateContentConfig
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    # Use 16384 for Pro to avoid thinking-token truncation (known Flash bug)
    max_tokens = 16384 if "pro" in model_id else 8192
    resp = client.models.generate_content(
        model=model_id,
        contents=prompt,
        config=GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=max_tokens,
            temperature=0,
        ),
    )
    # Handle safety-blocked responses
    if not resp.candidates or not resp.candidates[0].content.parts:
        usage = getattr(resp, "usage_metadata", None)
        return {
            "text": "",
            "model": model_id,
            "tokens_in": getattr(usage, "prompt_token_count", 0) if usage else 0,
            "tokens_out": 0,
            "stop_reason": f"SAFETY_BLOCKED: {getattr(resp, 'prompt_feedback', 'unknown')}",
        }
    usage = resp.usage_metadata
    try:
        text = resp.text
    except (ValueError, AttributeError):
        text = ""
    return {
        "text": text,
        "model": model_id,
        "tokens_in": getattr(usage, "prompt_token_count", 0),
        "tokens_out": getattr(usage, "candidates_token_count", 0),
        "stop_reason": str(resp.candidates[0].finish_reason) if resp.candidates else "unknown",
    }


CALLERS = {
    "anthropic": call_anthropic,
    "openai": call_openai,
    "google": call_google,
}


# ---------------------------------------------------------------------------
# Code extraction
# ---------------------------------------------------------------------------

def strip_markdown_fences(text: str) -> str:
    """Remove ```python ... ``` fences if present."""
    blocks = re.findall(r'```(?:[Pp]ython|py)?\s*\n(.*?)```', text, re.DOTALL)
    if blocks:
        return "\n\n".join(blocks)
    return text


def extract_files(raw_text: str) -> dict[str, str]:
    """Parse output into {filename: code} dict.

    Handles:
    - Single file output -> {"main.py": code}
    - Multi-file with # === FILENAME: xxx === markers
    - Multi-file with ```python blocks containing filename hints
    """
    text = strip_markdown_fences(raw_text)

    # Check for multi-file separator pattern
    parts = re.split(r'#\s*===\s*FILENAME:\s*(\S+)\s*===', text)
    if len(parts) > 1:
        files = {}
        for i in range(1, len(parts), 2):
            fname = parts[i]
            code = parts[i + 1].strip() if i + 1 < len(parts) else ""
            if code:
                files[fname] = code
        if files:
            return files

    # Check for "# filename.py" or "# --- filename.py ---" separators
    parts2 = re.split(r'\n#\s*[-=]*\s*([\w/.:-]+\.py)\s*[-=]*\s*\n', text)
    if len(parts2) > 2:
        files = {}
        for i in range(1, len(parts2), 2):
            fname = parts2[i]
            code = parts2[i + 1].strip() if i + 1 < len(parts2) else ""
            if code:
                files[fname] = code
        if files:
            return files

    # Single file
    return {"main.py": text.strip()}


# ---------------------------------------------------------------------------
# STS audit
# ---------------------------------------------------------------------------

def run_sts_audit(filepath: Path) -> dict | None:
    """Run sts_checker.py on a file, return parsed JSON or None on error."""
    json_out = filepath.with_suffix(".audit.json")
    try:
        result = subprocess.run(
            ["uv", "run", str(STS_CHECKER), str(filepath), "--output", str(json_out)],
            capture_output=True, text=True, timeout=30, cwd=str(ROOT),
        )
    except Exception as e:
        return {"error": str(e)}

    if json_out.exists():
        try:
            with open(json_out) as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            return {"error": f"Malformed audit JSON: {e}"}

    stderr = result.stderr or ""
    if "SyntaxError" in stderr:
        return {"error": "SyntaxError in generated code"}
    return {"error": stderr[:200] or "no output"}


def run_functional_check(filepath: Path) -> dict:
    """Try to run the file with python, return {success, error}."""
    # Strip API keys from subprocess environment
    safe_env = {k: v for k, v in os.environ.items()
                if not any(secret in k.upper() for secret in ("API_KEY", "SECRET", "TOKEN", "PASSWORD"))}
    safe_env.setdefault("PATH", os.environ.get("PATH", ""))
    try:
        result = subprocess.run(
            [sys.executable, str(filepath)],
            capture_output=True, text=True, timeout=15,
            cwd=str(filepath.parent),
            env=safe_env,
        )
        return {
            "success": result.returncode == 0,
            "error": result.stderr[:500] if result.returncode != 0 else None,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "timeout (15s)"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ---------------------------------------------------------------------------
# Main experiment loop
# ---------------------------------------------------------------------------

def _result_key(r: dict) -> tuple:
    return (r["model_name"], r["condition"], r["task"], r["rep"])


def _dedup_append(results: list[dict], entry: dict) -> list[dict]:
    """Remove any prior entry for the same (model, condition, task, rep), then append."""
    key = _result_key(entry)
    return [r for r in results if _result_key(r) != key] + [entry]


def get_n(model_name: str, condition: str) -> int:
    return N_OVERRIDES.get((model_name, condition), DEFAULT_N)


def build_prompt(task_key: str, condition: str) -> str:
    return TASKS[task_key] + CONDITION_ADDENDUM[condition]


def run_experiment(
    models_filter: list[str] | None = None,
    conditions_filter: list[str] | None = None,
    tasks_filter: list[str] | None = None,
    dry_run: bool = False,
    n_override: int | None = None,
):
    """Run the full experiment matrix."""

    models_to_run = models_filter or list(MODELS.keys())
    conditions_to_run = conditions_filter or list(CONDITION_ADDENDUM.keys())
    tasks_to_run = tasks_filter or list(TASKS.keys())

    # Check API keys
    available_models = []
    for m in models_to_run:
        key = MODELS[m]["env_key"]
        if os.environ.get(key):
            available_models.append(m)
            print(f"  [OK] {m}: {key} found ({MODELS[m]['tier']})")
        else:
            print(f"  [SKIP] {m}: {key} not set")

    if not available_models:
        print("\nNo API keys available. Set environment variables and retry.")
        return

    # Build run plan
    plan = []
    for model in available_models:
        for condition in conditions_to_run:
            n = n_override if n_override is not None else get_n(model, condition)
            for task in tasks_to_run:
                for rep in range(1, n + 1):
                    plan.append((model, condition, task, rep))

    total = len(plan)
    print(f"\n{'DRY RUN: ' if dry_run else ''}Experiment plan: {total} runs")
    print(f"  Models: {available_models}")
    print(f"  Conditions: {conditions_to_run}")
    print(f"  Tasks: {tasks_to_run}")

    if dry_run:
        for model, condition, task, rep in plan:
            n = get_n(model, condition)
            print(f"  {model}/{condition}/{task}/run{rep} (N={n})")
        return

    # Load existing results to allow resuming (only count successful runs)
    results = []
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE) as f:
            results = json.load(f)

    completed = {
        (r["model_name"], r["condition"], r["task"], r["rep"])
        for r in results
        if "error" not in r  # failed runs can be retried
    }

    remaining = [p for p in plan if p not in completed]
    if remaining != plan:
        print(f"  Resuming: {len(plan) - len(remaining)} already done, {len(remaining)} remaining")

    start_time = time.time()

    for i, (model_name, condition, task, rep) in enumerate(remaining):
        n = get_n(model_name, condition)
        run_start = time.time()
        print(f"\n[{i+1}/{len(remaining)}] {model_name}/{condition}/{task}/run{rep} (N={n})")

        # Build prompt
        prompt = build_prompt(task, condition)

        # Call API with retry
        model_cfg = MODELS[model_name]
        caller = CALLERS[model_cfg["provider"]]

        try:
            api_result = call_with_retry(caller, model_cfg["id"], prompt, provider=model_cfg["provider"])
        except Exception as e:
            print(f"  ERROR: {e}")
            results = _dedup_append(results, {
                "model_name": model_name,
                "condition": condition,
                "task": task,
                "rep": rep,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            save_results(results)
            continue

        # Check for truncation
        if any(kw in str(api_result["stop_reason"]).lower() for kw in ("max_tokens", "length")):
            print(f"  WARNING: Output truncated ({api_result['tokens_out']} tokens)")

        # Check for safety block
        if "SAFETY_BLOCKED" in str(api_result.get("stop_reason", "")):
            print(f"  WARNING: Response safety-blocked")
            results = _dedup_append(results, {
                "model_name": model_name,
                "condition": condition,
                "task": task,
                "rep": rep,
                "error": api_result["stop_reason"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            save_results(results)
            continue

        print(f"  API: {api_result['tokens_in']}in/{api_result['tokens_out']}out, model={api_result['model']}")

        # Extract and save files
        files = extract_files(api_result["text"])
        out_dir = OUTPUT_DIR / model_name / condition / task / f"run{rep}"
        out_dir.mkdir(parents=True, exist_ok=True)

        # Save raw response
        with open(out_dir / "raw_response.json", "w") as f:
            json.dump({
                "prompt": prompt,
                "response": api_result,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }, f, indent=2)

        # Save extracted code files
        for fname, code in files.items():
            (out_dir / fname).write_text(code)

        print(f"  Files: {list(files.keys())}")

        # Determine audit target (service.py for multi-file, main.py for single)
        if "service.py" in files:
            audit_target = out_dir / "service.py"
        elif "main.py" in files:
            audit_target = out_dir / "main.py"
        else:
            audit_target = out_dir / list(files.keys())[0]

        # Run STS audit
        audit = run_sts_audit(audit_target)

        # Run functional check (on the main entry point)
        if "main.py" in files:
            func_target = out_dir / "main.py"
        elif "views.py" in files:
            func_target = out_dir / "views.py"
        else:
            func_target = audit_target
        func_check = run_functional_check(func_target)

        # Extract metrics from audit
        metrics = {}
        if audit and "files" in audit and audit["files"]:
            f0 = audit["files"][0]
            metrics = {
                "max_cc": f0.get("max_cc"),
                "mi_score": f0.get("mi_score"),
                "adf": f0.get("adf"),
                "ccr": f0.get("ccr"),
                "tl": f0.get("tl"),
                "verdict": f0.get("verdict"),
                "h_effort": f0.get("h_effort"),
            }
        elif audit and "error" in audit:
            metrics = {"audit_error": audit["error"]}

        passed = "PASSED" in metrics.get("verdict", "")

        # ETA calculation
        elapsed_run = time.time() - run_start
        avg_time = (time.time() - start_time) / (i + 1)
        eta = avg_time * (len(remaining) - i - 1)

        print(f"  Audit: CC={metrics.get('max_cc')} ADF={metrics.get('adf')} "
              f"{'PASS' if passed else 'FAIL'} | "
              f"Runs: {'OK' if func_check['success'] else 'FAIL'} | "
              f"{elapsed_run:.1f}s | ETA: {eta/60:.0f}min")

        # Record result
        result_entry = {
            "model_name": model_name,
            "model_id": api_result["model"],
            "condition": condition,
            "task": task,
            "rep": rep,
            "tokens_in": api_result["tokens_in"],
            "tokens_out": api_result["tokens_out"],
            "stop_reason": api_result["stop_reason"],
            "files_generated": list(files.keys()),
            "audit_target": str(audit_target.relative_to(ROOT)),
            "functional_check": func_check["success"],
            "functional_error": func_check.get("error"),
            **metrics,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        results = _dedup_append(results, result_entry)

        # Save after each run (allows resume)
        save_results(results)

        # Per-provider delay to avoid rate limits
        time.sleep(PROVIDER_DELAYS.get(model_cfg["provider"], 1))

    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"Experiment complete: {len(remaining)} new runs in {elapsed:.0f}s")
    print(f"Total results: {len(results)}")
    print(f"Results saved to: {RESULTS_FILE}")

    # Print summary
    print_summary(results)


def save_results(results: list[dict]):
    """Save results to JSON atomically, creating directory if needed."""
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = RESULTS_FILE.with_suffix(".json.tmp")
    with open(tmp, "w") as f:
        json.dump(results, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    tmp.rename(RESULTS_FILE)


def print_summary(results: list[dict]):
    """Print a summary table of results."""
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    # Group by model × condition
    from collections import defaultdict
    groups = defaultdict(list)
    for r in results:
        if "error" in r and "verdict" not in r:
            continue
        groups[(r["model_name"], r["condition"])].append(r)

    print(f"\n{'Model':<10} {'Cond':<6} {'N':>3} {'Pass%':>6} {'MeanCC':>7} {'MeanADF':>8} {'FuncOK%':>8}")
    print("-" * 55)

    for (model, cond) in sorted(groups.keys()):
        runs = groups[(model, cond)]
        n = len(runs)
        passed = sum(1 for r in runs if "PASSED" in (r.get("verdict") or ""))
        func_ok = sum(1 for r in runs if r.get("functional_check"))
        ccs = [r["max_cc"] for r in runs if r.get("max_cc") is not None]
        adfs = [r["adf"] for r in runs if r.get("adf") is not None]

        pass_pct = f"{100*passed/n:.0f}%" if n else "—"
        mean_cc = f"{sum(ccs)/len(ccs):.1f}" if ccs else "—"
        mean_adf = f"{sum(adfs)/len(adfs):.3f}" if adfs else "—"
        func_pct = f"{100*func_ok/n:.0f}%" if n else "—"

        print(f"{model:<10} {cond:<6} {n:>3} {pass_pct:>6} {mean_cc:>7} {mean_adf:>8} {func_pct:>8}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def resolve_models(args) -> list[str] | None:
    """Resolve model list from --models and/or --tier flags."""
    models = []
    if args.models:
        models.extend(args.models)
    if args.tier:
        for tier in args.tier:
            tier_models = [name for name, cfg in MODELS.items() if cfg["tier"] == tier]
            models.extend(tier_models)
    if models:
        # Deduplicate while preserving order
        seen = set()
        return [m for m in models if not (m in seen or seen.add(m))]
    return None  # means "all available"


def main():
    parser = argparse.ArgumentParser(description="Cross-model experiment runner")
    parser.add_argument("--models", nargs="+", choices=list(MODELS.keys()),
                        help="Models to run (default: all available)")
    parser.add_argument("--tier", nargs="+", choices=["A", "B", "C"],
                        help="Run all models in specified tier(s)")
    parser.add_argument("--conditions", nargs="+", choices=["U", "D", "S"],
                        help="Conditions to run (default: all)")
    parser.add_argument("--tasks", nargs="+", choices=list(TASKS.keys()),
                        help="Tasks to run (default: all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print plan without calling APIs")
    parser.add_argument("--smoke-test", action="store_true",
                        help="Run 1 call per model (task1, condition U, rep 1 only)")
    args = parser.parse_args()

    print(f"Cross-Model Experiment Runner")
    print(f"Pre-registration: commit 05f8902")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print(f"Checking API keys...")

    models_filter = resolve_models(args)

    if args.smoke_test:
        # Override to minimal run: 1 task, 1 condition, 1 rep per model
        print("\n=== SMOKE TEST MODE ===")
        run_experiment(
            models_filter=models_filter,
            conditions_filter=["U"],
            tasks_filter=["task1_bookstore"],
            dry_run=args.dry_run,
            n_override=1,
        )
    else:
        run_experiment(
            models_filter=models_filter,
            conditions_filter=args.conditions,
            tasks_filter=args.tasks,
            dry_run=args.dry_run,
        )


if __name__ == "__main__":
    main()
