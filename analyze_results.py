#!/usr/bin/env python3
"""
Statistical Analysis for Cross-Model Architectural Quality Experiment

Pre-registered design: commit 05f8902
See: framework/experiments/exp_cross_model_design.md

Reads cross_model_results.json and produces:
  1. Formatted tables to stdout
  2. JSON report to records/cross_model_analysis.json
  3. Markdown tables to records/cross_model_tables.md

Dependencies: scipy (for Fisher's exact test, Clopper-Pearson CIs, CMH test)
  If not installed: uv add scipy

Usage:
    uv run analyze_results.py
    uv run analyze_results.py --input path/to/results.json
"""

import json
import math
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------

try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("WARNING: scipy is not installed. Install with: uv add scipy")
    print("         Fisher's exact tests, CIs, and CMH test will be skipped.\n")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path(__file__).parent
DEFAULT_INPUT = ROOT / "records" / "cross_model_results.json"
OUTPUT_JSON = ROOT / "records" / "cross_model_analysis.json"
OUTPUT_MD = ROOT / "records" / "cross_model_tables.md"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_git_hash() -> str:
    """Get short git commit hash, or 'unknown' if not in a repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5, cwd=str(ROOT),
        )
        return result.stdout.strip() if result.returncode == 0 else "unknown"
    except Exception:
        return "unknown"


def safe_div(a: float, b: float, default: float = 0.0) -> float:
    return a / b if b != 0 else default


def mean(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0


def stdev(vals: list[float]) -> float:
    if len(vals) < 2:
        return 0.0
    m = mean(vals)
    return math.sqrt(sum((x - m) ** 2 for x in vals) / (len(vals) - 1))


def cohens_h(p1: float, p2: float) -> float:
    """Cohen's h effect size for two proportions.

    h = 2 * arcsin(sqrt(p1)) - 2 * arcsin(sqrt(p2))
    Positive h means p1 > p2.
    """
    p1 = max(0.0, min(1.0, p1))
    p2 = max(0.0, min(1.0, p2))
    return 2.0 * math.asin(math.sqrt(p1)) - 2.0 * math.asin(math.sqrt(p2))


def interpret_h(h: float) -> str:
    """Interpret Cohen's h magnitude."""
    ah = abs(h)
    if ah < 0.2:
        return "negligible"
    elif ah < 0.5:
        return "small"
    elif ah < 0.8:
        return "medium"
    else:
        return "large"


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Clopper-Pearson exact confidence interval for a binomial proportion.

    Returns (lower, upper) bounds.
    """
    if not SCIPY_AVAILABLE:
        return (0.0, 1.0)
    if n == 0:
        return (0.0, 1.0)
    if k == 0:
        lower = 0.0
    else:
        lower = stats.beta.ppf(alpha / 2, k, n - k + 1)
    if k == n:
        upper = 1.0
    else:
        upper = stats.beta.ppf(1 - alpha / 2, k + 1, n - k)
    return (lower, upper)


def fishers_exact(a: int, b: int, c: int, d: int) -> dict:
    """Run Fisher's exact test on a 2x2 table.

    Table layout:
        [[a, b],    a=pass_grp1, b=fail_grp1
         [c, d]]    c=pass_grp2, d=fail_grp2

    Returns dict with odds_ratio and p_value.
    """
    if not SCIPY_AVAILABLE:
        return {"odds_ratio": None, "p_value": None, "note": "scipy not available"}
    table = [[a, b], [c, d]]
    odds_ratio, p_value = stats.fisher_exact(table, alternative="two-sided")
    return {"odds_ratio": odds_ratio, "p_value": p_value}


def cochran_mantel_haenszel(tables: list[tuple[int, int, int, int]]) -> dict:
    """Cochran-Mantel-Haenszel test for stratified 2x2 tables.

    Each table is (a, b, c, d) where:
        a = pass_grp1, b = fail_grp1, c = pass_grp2, d = fail_grp2

    Tests whether the common odds ratio across strata is 1.
    Returns dict with statistic, p_value, and common_odds_ratio.
    """
    if not SCIPY_AVAILABLE:
        return {"statistic": None, "p_value": None, "common_odds_ratio": None,
                "note": "scipy not available"}

    # CMH statistic computation
    # Reference: Agresti, Categorical Data Analysis, Section 6.3
    numerator_sum = 0.0
    denom_sum = 0.0
    or_num = 0.0
    or_den = 0.0

    for a, b, c, d in tables:
        n = a + b + c + d
        if n <= 1:
            continue
        r1 = a + b  # row 1 total
        r2 = c + d  # row 2 total
        c1 = a + c  # col 1 total
        c2 = b + d  # col 2 total

        expected_a = r1 * c1 / n
        var_a = r1 * r2 * c1 * c2 / (n * n * (n - 1)) if n > 1 else 0

        numerator_sum += (a - expected_a)
        denom_sum += var_a

        # Mantel-Haenszel common odds ratio components
        or_num += a * d / n
        or_den += b * c / n

    if denom_sum <= 0:
        return {"statistic": 0.0, "p_value": 1.0, "common_odds_ratio": None,
                "note": "degenerate tables"}

    chi2 = (abs(numerator_sum) - 0.5) ** 2 / denom_sum  # continuity correction
    p_value = 1.0 - stats.chi2.cdf(chi2, df=1)
    common_or = or_num / or_den if or_den > 0 else float("inf")

    return {
        "statistic": round(chi2, 4),
        "p_value": p_value,
        "common_odds_ratio": round(common_or, 4) if common_or != float("inf") else None,
    }


# ---------------------------------------------------------------------------
# Data loading and filtering
# ---------------------------------------------------------------------------

def load_results(filepath: Path) -> list[dict]:
    """Load results JSON and filter out error entries."""
    with open(filepath) as f:
        raw = json.load(f)

    valid = []
    errors = []
    for entry in raw:
        if "error" in entry and "verdict" not in entry:
            # API-level errors (e.g., 529 overloaded) — exclude
            errors.append(entry)
        elif entry.get("verdict") is None:
            # Completed but unauditable (e.g., truncated code) — count as FAIL
            entry["verdict"] = "H-TIER (FAILED: unauditable)"
            valid.append(entry)
        else:
            valid.append(entry)

    print(f"Loaded {len(raw)} entries: {len(valid)} valid, {len(errors)} errors/skipped")
    if errors:
        error_summary = defaultdict(int)
        for e in errors:
            key = f"{e.get('model_name', '?')}/{e.get('condition', '?')}/{e.get('task', '?')}"
            error_summary[key] += 1
        print("  Error entries:")
        for key, count in sorted(error_summary.items()):
            print(f"    {key}: {count}")
    print()

    return valid


def is_pass(entry: dict) -> bool:
    """Check if an entry has a PASSED verdict."""
    return "PASSED" in (entry.get("verdict") or "")


# ---------------------------------------------------------------------------
# Analysis 1: Descriptive Summary Table
# ---------------------------------------------------------------------------

def descriptive_summary(data: list[dict]) -> dict:
    """Build model x condition summary and model x condition x task breakdown."""

    # Group by (model, condition)
    mc_groups = defaultdict(list)
    for r in data:
        mc_groups[(r["model_name"], r["condition"])].append(r)

    # Group by (model, condition, task)
    mct_groups = defaultdict(list)
    for r in data:
        mct_groups[(r["model_name"], r["condition"], r["task"])].append(r)

    summary_table = []
    for (model, cond), entries in sorted(mc_groups.items()):
        n = len(entries)
        passes = sum(1 for e in entries if is_pass(e))
        ccs = [e["max_cc"] for e in entries if e.get("max_cc") is not None]
        adfs = [e["adf"] for e in entries if e.get("adf") is not None]
        func_ok = sum(1 for e in entries if e.get("functional_check"))

        ci_lo, ci_hi = clopper_pearson(passes, n)

        summary_table.append({
            "model": model,
            "condition": cond,
            "n": n,
            "pass_count": passes,
            "pass_rate": safe_div(passes, n),
            "pass_rate_ci_lo": ci_lo,
            "pass_rate_ci_hi": ci_hi,
            "mean_cc": mean(ccs),
            "sd_cc": stdev(ccs),
            "mean_adf": mean(adfs),
            "sd_adf": stdev(adfs),
            "functional_ok": func_ok,
            "functional_rate": safe_div(func_ok, n),
        })

    task_table = []
    for (model, cond, task), entries in sorted(mct_groups.items()):
        n = len(entries)
        passes = sum(1 for e in entries if is_pass(e))
        ccs = [e["max_cc"] for e in entries if e.get("max_cc") is not None]
        adfs = [e["adf"] for e in entries if e.get("adf") is not None]
        func_ok = sum(1 for e in entries if e.get("functional_check"))

        ci_lo, ci_hi = clopper_pearson(passes, n)

        task_table.append({
            "model": model,
            "condition": cond,
            "task": task,
            "n": n,
            "pass_count": passes,
            "pass_rate": safe_div(passes, n),
            "pass_rate_ci_lo": ci_lo,
            "pass_rate_ci_hi": ci_hi,
            "mean_cc": mean(ccs),
            "mean_adf": mean(adfs),
            "functional_ok": func_ok,
            "functional_rate": safe_div(func_ok, n),
        })

    return {"model_condition": summary_table, "model_condition_task": task_table}


# ---------------------------------------------------------------------------
# Analysis 2 & 3: Hypothesis Tests and Effect Sizes
# ---------------------------------------------------------------------------

def within_model_tests(data: list[dict]) -> list[dict]:
    """Within-model pairwise Fisher's exact tests and Cohen's h.

    For each model, compares U vs S, U vs D, and D vs S.
    """
    models = sorted(set(r["model_name"] for r in data))
    conditions = ["U", "D", "S"]
    pairs = [("U", "S"), ("U", "D"), ("D", "S")]

    # Group by (model, condition)
    mc_groups = defaultdict(list)
    for r in data:
        mc_groups[(r["model_name"], r["condition"])].append(r)

    results = []
    for model in models:
        for c1, c2 in pairs:
            g1 = mc_groups.get((model, c1), [])
            g2 = mc_groups.get((model, c2), [])

            n1 = len(g1)
            n2 = len(g2)
            pass1 = sum(1 for e in g1 if is_pass(e))
            pass2 = sum(1 for e in g2 if is_pass(e))
            fail1 = n1 - pass1
            fail2 = n2 - pass2

            p1 = safe_div(pass1, n1, 0.0)
            p2 = safe_div(pass2, n2, 0.0)

            fisher = fishers_exact(pass1, fail1, pass2, fail2)
            h = cohens_h(p1, p2)

            results.append({
                "model": model,
                "comparison": f"{c1} vs {c2}",
                "n_c1": n1,
                "n_c2": n2,
                "pass_c1": pass1,
                "pass_c2": pass2,
                "rate_c1": p1,
                "rate_c2": p2,
                "odds_ratio": fisher["odds_ratio"],
                "p_value": fisher["p_value"],
                "cohens_h": round(h, 4),
                "effect_interpretation": interpret_h(h),
            })

    return results


# ---------------------------------------------------------------------------
# Analysis 4: Confidence Intervals (included in descriptive_summary)
# ---------------------------------------------------------------------------
# Already computed as pass_rate_ci_lo / pass_rate_ci_hi in descriptive_summary.


# ---------------------------------------------------------------------------
# Analysis 5: Cross-Model Pooled Test (CMH)
# ---------------------------------------------------------------------------

def cross_model_pooled_test(data: list[dict]) -> dict:
    """Cochran-Mantel-Haenszel test: U vs S pooled across models.

    Each model is a stratum. Tests whether the U -> S effect is
    consistent across all models.
    """
    models = sorted(set(r["model_name"] for r in data))

    mc_groups = defaultdict(list)
    for r in data:
        mc_groups[(r["model_name"], r["condition"])].append(r)

    tables = []
    strata_detail = []
    for model in models:
        g_u = mc_groups.get((model, "U"), [])
        g_s = mc_groups.get((model, "S"), [])

        if not g_u and not g_s:
            continue

        a = sum(1 for e in g_u if is_pass(e))       # U pass
        b = len(g_u) - a                              # U fail
        c = sum(1 for e in g_s if is_pass(e))         # S pass
        d = len(g_s) - c                              # S fail

        tables.append((a, b, c, d))
        strata_detail.append({
            "model": model,
            "U_pass": a, "U_fail": b, "U_n": a + b,
            "S_pass": c, "S_fail": d, "S_n": c + d,
        })

    cmh = cochran_mantel_haenszel(tables)

    # Also run pooled Fisher's (ignoring strata) for comparison
    total_u_pass = sum(t[0] for t in tables)
    total_u_fail = sum(t[1] for t in tables)
    total_s_pass = sum(t[2] for t in tables)
    total_s_fail = sum(t[3] for t in tables)

    pooled_fisher = fishers_exact(total_u_pass, total_u_fail,
                                   total_s_pass, total_s_fail)

    return {
        "test": "Cochran-Mantel-Haenszel (U vs S, stratified by model)",
        "strata": strata_detail,
        "cmh_statistic": cmh["statistic"],
        "cmh_p_value": cmh["p_value"],
        "common_odds_ratio": cmh["common_odds_ratio"],
        "pooled_fisher_odds_ratio": pooled_fisher["odds_ratio"],
        "pooled_fisher_p_value": pooled_fisher["p_value"],
        "pooled_totals": {
            "U_pass": total_u_pass, "U_fail": total_u_fail,
            "S_pass": total_s_pass, "S_fail": total_s_fail,
            "U_rate": safe_div(total_u_pass, total_u_pass + total_u_fail),
            "S_rate": safe_div(total_s_pass, total_s_pass + total_s_fail),
        },
    }


# ---------------------------------------------------------------------------
# Analysis 6: Metric Distributions
# ---------------------------------------------------------------------------

def metric_distributions(data: list[dict]) -> list[dict]:
    """Per model x condition: mean, sd, min, max for CC, ADF, MI."""
    mc_groups = defaultdict(list)
    for r in data:
        mc_groups[(r["model_name"], r["condition"])].append(r)

    results = []
    for (model, cond), entries in sorted(mc_groups.items()):
        row = {"model": model, "condition": cond, "n": len(entries)}

        for metric_name, field in [("cc", "max_cc"), ("adf", "adf"), ("mi", "mi_score")]:
            vals = [e[field] for e in entries if e.get(field) is not None]
            if vals:
                row[f"{metric_name}_mean"] = round(mean(vals), 4)
                row[f"{metric_name}_sd"] = round(stdev(vals), 4)
                row[f"{metric_name}_min"] = min(vals)
                row[f"{metric_name}_max"] = max(vals)
                row[f"{metric_name}_n"] = len(vals)
            else:
                row[f"{metric_name}_mean"] = None
                row[f"{metric_name}_sd"] = None
                row[f"{metric_name}_min"] = None
                row[f"{metric_name}_max"] = None
                row[f"{metric_name}_n"] = 0

        results.append(row)

    return results


# ---------------------------------------------------------------------------
# Analysis 7: Token Cost Analysis
# ---------------------------------------------------------------------------

def token_cost_analysis(data: list[dict]) -> list[dict]:
    """Mean tokens_out per model x condition."""
    mc_groups = defaultdict(list)
    for r in data:
        mc_groups[(r["model_name"], r["condition"])].append(r)

    results = []
    for (model, cond), entries in sorted(mc_groups.items()):
        tokens_out = [e["tokens_out"] for e in entries if e.get("tokens_out") is not None]
        tokens_in = [e["tokens_in"] for e in entries if e.get("tokens_in") is not None]

        results.append({
            "model": model,
            "condition": cond,
            "n": len(entries),
            "mean_tokens_out": round(mean(tokens_out), 1) if tokens_out else None,
            "sd_tokens_out": round(stdev(tokens_out), 1) if tokens_out else None,
            "min_tokens_out": min(tokens_out) if tokens_out else None,
            "max_tokens_out": max(tokens_out) if tokens_out else None,
            "mean_tokens_in": round(mean(tokens_in), 1) if tokens_in else None,
        })

    return results


# ---------------------------------------------------------------------------
# Output: Terminal
# ---------------------------------------------------------------------------

def print_section(title: str):
    """Print a section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def print_descriptive(summary: dict):
    """Print descriptive summary tables."""
    print_section("1. DESCRIPTIVE SUMMARY: Model x Condition")

    rows = summary["model_condition"]
    header = (f"{'Model':<10} {'Cond':<5} {'N':>3} {'Pass':>5} {'Rate%':>6} "
              f"{'95% CI':>14} {'MeanCC':>7} {'MeanADF':>8} {'Func%':>6}")
    print(f"\n{header}")
    print("-" * len(header))

    for r in rows:
        ci = f"[{r['pass_rate_ci_lo']:.2f},{r['pass_rate_ci_hi']:.2f}]"
        print(f"{r['model']:<10} {r['condition']:<5} {r['n']:>3} "
              f"{r['pass_count']:>5} {r['pass_rate']*100:>5.1f}% "
              f"{ci:>14} {r['mean_cc']:>7.1f} {r['mean_adf']:>8.4f} "
              f"{r['functional_rate']*100:>5.1f}%")

    print_section("1b. DESCRIPTIVE SUMMARY: Model x Condition x Task")

    rows = summary["model_condition_task"]
    header = (f"{'Model':<10} {'Cond':<5} {'Task':<18} {'N':>3} {'Pass':>5} "
              f"{'Rate%':>6} {'MeanCC':>7} {'MeanADF':>8}")
    print(f"\n{header}")
    print("-" * len(header))

    current_model = None
    for r in rows:
        if r['model'] != current_model:
            if current_model is not None:
                print()
            current_model = r['model']
        print(f"{r['model']:<10} {r['condition']:<5} {r['task']:<18} {r['n']:>3} "
              f"{r['pass_count']:>5} {r['pass_rate']*100:>5.1f}% "
              f"{r['mean_cc']:>7.1f} {r['mean_adf']:>8.4f}")


def print_hypothesis_tests(tests: list[dict]):
    """Print within-model hypothesis test results."""
    print_section("2. WITHIN-MODEL HYPOTHESIS TESTS (Fisher's Exact)")

    if not SCIPY_AVAILABLE:
        print("\n  [SKIPPED] scipy not installed\n")
        return

    header = (f"{'Model':<10} {'Compare':<8} {'N1':>3} {'N2':>3} "
              f"{'Pass1':>5} {'Pass2':>5} {'Rate1':>6} {'Rate2':>6} "
              f"{'OR':>7} {'p-val':>8} {'h':>6} {'Effect':>11}")
    print(f"\n{header}")
    print("-" * len(header))

    current_model = None
    for t in tests:
        if t['model'] != current_model:
            if current_model is not None:
                print()
            current_model = t['model']

        or_str = f"{t['odds_ratio']:.2f}" if t['odds_ratio'] is not None and t['odds_ratio'] != float('inf') else "inf"
        p_str = f"{t['p_value']:.4f}" if t['p_value'] is not None else "N/A"
        p = t['p_value']
        if p is not None and p < 0.001:
            sig = " ***"
        elif p is not None and p < 0.01:
            sig = " **"
        elif p is not None and p < 0.05:
            sig = " *"
        else:
            sig = ""

        print(f"{t['model']:<10} {t['comparison']:<8} "
              f"{t['n_c1']:>3} {t['n_c2']:>3} "
              f"{t['pass_c1']:>5} {t['pass_c2']:>5} "
              f"{t['rate_c1']*100:>5.1f}% {t['rate_c2']*100:>5.1f}% "
              f"{or_str:>7} {p_str:>8}{sig} "
              f"{t['cohens_h']:>6.2f} {t['effect_interpretation']:>11}")

    print("\n  Significance: * p<0.05, ** p<0.01, *** p<0.001")
    print("  Cohen's h: |0.2| small, |0.5| medium, |0.8| large")
    print("  Positive h means first condition has higher pass rate")


def print_cmh(cmh: dict):
    """Print cross-model pooled test results."""
    print_section("3. CROSS-MODEL POOLED TEST: U vs S (CMH)")

    if not SCIPY_AVAILABLE:
        print("\n  [SKIPPED] scipy not installed\n")
        return

    print("\n  Strata (per model):")
    for s in cmh["strata"]:
        u_rate = safe_div(s["U_pass"], s["U_n"]) * 100
        s_rate = safe_div(s["S_pass"], s["S_n"]) * 100
        print(f"    {s['model']:<10} U: {s['U_pass']}/{s['U_n']} ({u_rate:.0f}%)  "
              f"S: {s['S_pass']}/{s['S_n']} ({s_rate:.0f}%)")

    totals = cmh["pooled_totals"]
    print(f"\n  Pooled totals:")
    print(f"    U: {totals['U_pass']}/{totals['U_pass'] + totals['U_fail']} "
          f"({totals['U_rate']*100:.1f}%)")
    print(f"    S: {totals['S_pass']}/{totals['S_pass'] + totals['S_fail']} "
          f"({totals['S_rate']*100:.1f}%)")

    print(f"\n  Cochran-Mantel-Haenszel test:")
    print(f"    Chi-squared statistic: {cmh['cmh_statistic']}")
    print(f"    p-value:               {cmh['cmh_p_value']:.6f}" if cmh['cmh_p_value'] is not None else "    p-value: N/A")
    print(f"    Common odds ratio:     {cmh['common_odds_ratio']}" if cmh['common_odds_ratio'] is not None else "    Common odds ratio: N/A")

    print(f"\n  Pooled Fisher's exact (unstratified, for comparison):")
    print(f"    Odds ratio: {cmh['pooled_fisher_odds_ratio']:.4f}" if cmh['pooled_fisher_odds_ratio'] is not None else "    Odds ratio: N/A")
    print(f"    p-value:    {cmh['pooled_fisher_p_value']:.6f}" if cmh['pooled_fisher_p_value'] is not None else "    p-value: N/A")

    if cmh['cmh_p_value'] is not None and cmh['cmh_p_value'] < 0.05:
        print(f"\n  --> The U vs S difference IS significant across models (p < 0.05)")
        print(f"      The specification effect is model-general.")
    elif cmh['cmh_p_value'] is not None:
        print(f"\n  --> The U vs S difference is NOT significant across models (p = {cmh['cmh_p_value']:.4f})")


def print_metric_distributions(dists: list[dict]):
    """Print metric distribution table."""
    print_section("4. METRIC DISTRIBUTIONS: Model x Condition")

    header = (f"{'Model':<10} {'Cond':<5} {'N':>3} "
              f"{'CC_mean':>7} {'CC_sd':>6} {'CC_min':>6} {'CC_max':>6} "
              f"{'ADF_mean':>8} {'ADF_sd':>7} "
              f"{'MI_mean':>7} {'MI_sd':>6}")
    print(f"\n{header}")
    print("-" * len(header))

    for r in dists:
        cc_mean = f"{r['cc_mean']:.1f}" if r['cc_mean'] is not None else "  N/A"
        cc_sd = f"{r['cc_sd']:.1f}" if r['cc_sd'] is not None else " N/A"
        cc_min = f"{r['cc_min']}" if r['cc_min'] is not None else " N/A"
        cc_max = f"{r['cc_max']}" if r['cc_max'] is not None else " N/A"
        adf_mean = f"{r['adf_mean']:.4f}" if r['adf_mean'] is not None else "   N/A"
        adf_sd = f"{r['adf_sd']:.4f}" if r['adf_sd'] is not None else "  N/A"
        mi_mean = f"{r['mi_mean']:.1f}" if r['mi_mean'] is not None else "  N/A"
        mi_sd = f"{r['mi_sd']:.1f}" if r['mi_sd'] is not None else " N/A"

        print(f"{r['model']:<10} {r['condition']:<5} {r['n']:>3} "
              f"{cc_mean:>7} {cc_sd:>6} {cc_min:>6} {cc_max:>6} "
              f"{adf_mean:>8} {adf_sd:>7} "
              f"{mi_mean:>7} {mi_sd:>6}")


def print_token_costs(tokens: list[dict]):
    """Print token cost analysis."""
    print_section("5. TOKEN COST ANALYSIS: Model x Condition")

    header = (f"{'Model':<10} {'Cond':<5} {'N':>3} "
              f"{'MeanOut':>8} {'SD':>7} {'Min':>6} {'Max':>6} {'MeanIn':>7}")
    print(f"\n{header}")
    print("-" * len(header))

    for r in tokens:
        m_out = f"{r['mean_tokens_out']:.0f}" if r['mean_tokens_out'] is not None else "N/A"
        s_out = f"{r['sd_tokens_out']:.0f}" if r['sd_tokens_out'] is not None else "N/A"
        mn_out = f"{r['min_tokens_out']}" if r['min_tokens_out'] is not None else "N/A"
        mx_out = f"{r['max_tokens_out']}" if r['max_tokens_out'] is not None else "N/A"
        m_in = f"{r['mean_tokens_in']:.0f}" if r['mean_tokens_in'] is not None else "N/A"

        print(f"{r['model']:<10} {r['condition']:<5} {r['n']:>3} "
              f"{m_out:>8} {s_out:>7} {mn_out:>6} {mx_out:>6} {m_in:>7}")


# ---------------------------------------------------------------------------
# Output: Markdown
# ---------------------------------------------------------------------------

def generate_markdown(summary: dict, tests: list[dict], cmh: dict,
                      dists: list[dict], tokens: list[dict],
                      metadata: dict) -> str:
    """Generate paper-ready markdown tables."""
    lines = []
    lines.append("# Cross-Model Experiment: Statistical Results\n")
    lines.append(f"Generated: {metadata['timestamp']}")
    lines.append(f"Input: `{metadata['input_file']}`")
    lines.append(f"Git commit: `{metadata['git_hash']}`")
    lines.append(f"Valid observations: {metadata['n_valid']}")
    lines.append(f"Errors filtered: {metadata['n_errors']}")
    lines.append("")

    # Table 1: Model x Condition summary
    lines.append("## Table 1: Pass Rates by Model and Condition\n")
    lines.append("| Model | Condition | N | Pass | Rate (%) | 95% CI | Mean CC | Mean ADF | Func (%) |")
    lines.append("|-------|-----------|--:|-----:|---------:|--------|--------:|---------:|---------:|")

    for r in summary["model_condition"]:
        ci = f"[{r['pass_rate_ci_lo']:.2f}, {r['pass_rate_ci_hi']:.2f}]"
        lines.append(
            f"| {r['model']} | {r['condition']} | {r['n']} | {r['pass_count']} "
            f"| {r['pass_rate']*100:.1f} | {ci} "
            f"| {r['mean_cc']:.1f} | {r['mean_adf']:.4f} "
            f"| {r['functional_rate']*100:.1f} |"
        )

    lines.append("")

    # Table 2: Task breakdown
    lines.append("## Table 2: Pass Rates by Model, Condition, and Task\n")
    lines.append("| Model | Cond | Task | N | Pass | Rate (%) | Mean CC | Mean ADF |")
    lines.append("|-------|------|------|--:|-----:|---------:|--------:|---------:|")

    for r in summary["model_condition_task"]:
        lines.append(
            f"| {r['model']} | {r['condition']} | {r['task']} | {r['n']} "
            f"| {r['pass_count']} | {r['pass_rate']*100:.1f} "
            f"| {r['mean_cc']:.1f} | {r['mean_adf']:.4f} |"
        )

    lines.append("")

    # Table 3: Hypothesis tests
    lines.append("## Table 3: Within-Model Pairwise Tests (Fisher's Exact)\n")

    if SCIPY_AVAILABLE:
        lines.append("| Model | Comparison | N1 | N2 | Rate1 (%) | Rate2 (%) | OR | p-value | Cohen's h | Effect |")
        lines.append("|-------|------------|---:|---:|----------:|----------:|---:|--------:|----------:|--------|")

        for t in tests:
            or_str = f"{t['odds_ratio']:.2f}" if t['odds_ratio'] is not None and t['odds_ratio'] != float('inf') else "inf"
            p_str = f"{t['p_value']:.4f}" if t['p_value'] is not None else "N/A"
            sig = ""
            if t['p_value'] is not None:
                if t['p_value'] < 0.001:
                    sig = " ***"
                elif t['p_value'] < 0.01:
                    sig = " **"
                elif t['p_value'] < 0.05:
                    sig = " *"

            lines.append(
                f"| {t['model']} | {t['comparison']} | {t['n_c1']} | {t['n_c2']} "
                f"| {t['rate_c1']*100:.1f} | {t['rate_c2']*100:.1f} "
                f"| {or_str} | {p_str}{sig} "
                f"| {t['cohens_h']:.2f} | {t['effect_interpretation']} |"
            )
    else:
        lines.append("*scipy not installed; tests skipped*")

    lines.append("")

    # Table 4: CMH test
    lines.append("## Table 4: Cross-Model Pooled Test (U vs S)\n")

    if SCIPY_AVAILABLE:
        lines.append("### Strata\n")
        lines.append("| Model | U Pass/N | U Rate (%) | S Pass/N | S Rate (%) |")
        lines.append("|-------|---------|----------:|---------|----------:|")

        for s in cmh["strata"]:
            u_rate = safe_div(s["U_pass"], s["U_n"]) * 100
            s_rate = safe_div(s["S_pass"], s["S_n"]) * 100
            lines.append(
                f"| {s['model']} | {s['U_pass']}/{s['U_n']} | {u_rate:.1f} "
                f"| {s['S_pass']}/{s['S_n']} | {s_rate:.1f} |"
            )

        totals = cmh["pooled_totals"]
        lines.append("")
        lines.append("### CMH Result\n")
        lines.append(f"- **CMH chi-squared:** {cmh['cmh_statistic']}")
        p_str = f"{cmh['cmh_p_value']:.6f}" if cmh['cmh_p_value'] is not None else "N/A"
        lines.append(f"- **p-value:** {p_str}")
        or_str = f"{cmh['common_odds_ratio']}" if cmh['common_odds_ratio'] is not None else "N/A"
        lines.append(f"- **Common odds ratio:** {or_str}")
        lines.append(f"- **Pooled U rate:** {totals['U_rate']*100:.1f}%")
        lines.append(f"- **Pooled S rate:** {totals['S_rate']*100:.1f}%")
    else:
        lines.append("*scipy not installed; test skipped*")

    lines.append("")

    # Table 5: Metric distributions
    lines.append("## Table 5: Metric Distributions\n")
    lines.append("| Model | Cond | N | CC mean | CC sd | CC range | ADF mean | ADF sd | MI mean | MI sd |")
    lines.append("|-------|------|--:|--------:|------:|---------:|---------:|-------:|--------:|------:|")

    for r in dists:
        cc_range = f"{r['cc_min']}-{r['cc_max']}" if r['cc_min'] is not None else "N/A"
        cc_mean = f"{r['cc_mean']:.1f}" if r['cc_mean'] is not None else "N/A"
        cc_sd = f"{r['cc_sd']:.1f}" if r['cc_sd'] is not None else "N/A"
        adf_mean = f"{r['adf_mean']:.4f}" if r['adf_mean'] is not None else "N/A"
        adf_sd = f"{r['adf_sd']:.4f}" if r['adf_sd'] is not None else "N/A"
        mi_mean = f"{r['mi_mean']:.1f}" if r['mi_mean'] is not None else "N/A"
        mi_sd = f"{r['mi_sd']:.1f}" if r['mi_sd'] is not None else "N/A"

        lines.append(
            f"| {r['model']} | {r['condition']} | {r['n']} "
            f"| {cc_mean} | {cc_sd} | {cc_range} "
            f"| {adf_mean} | {adf_sd} "
            f"| {mi_mean} | {mi_sd} |"
        )

    lines.append("")

    # Table 6: Token costs
    lines.append("## Table 6: Token Output by Model and Condition\n")
    lines.append("| Model | Condition | N | Mean tokens out | SD | Min | Max |")
    lines.append("|-------|-----------|--:|----------------:|---:|----:|----:|")

    for r in tokens:
        m_out = f"{r['mean_tokens_out']:.0f}" if r['mean_tokens_out'] is not None else "N/A"
        s_out = f"{r['sd_tokens_out']:.0f}" if r['sd_tokens_out'] is not None else "N/A"
        mn = f"{r['min_tokens_out']}" if r['min_tokens_out'] is not None else "N/A"
        mx = f"{r['max_tokens_out']}" if r['max_tokens_out'] is not None else "N/A"
        lines.append(
            f"| {r['model']} | {r['condition']} | {r['n']} "
            f"| {m_out} | {s_out} | {mn} | {mx} |"
        )

    lines.append("")
    lines.append("---\n")
    lines.append(f"*Significance: \\* p<0.05, \\*\\* p<0.01, \\*\\*\\* p<0.001*")
    lines.append(f"*Cohen's h: |0.2| small, |0.5| medium, |0.8| large*")
    lines.append(f"*CIs: Clopper-Pearson exact 95%*")
    lines.append(f"*CMH test uses continuity correction*")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Output: JSON report
# ---------------------------------------------------------------------------

def build_json_report(metadata: dict, summary: dict, tests: list[dict],
                      cmh: dict, dists: list[dict],
                      tokens: list[dict]) -> dict:
    """Build the complete JSON report."""

    # Round floats for cleaner JSON
    def round_floats(obj, decimals=6):
        if isinstance(obj, float):
            if math.isnan(obj) or math.isinf(obj):
                return str(obj)
            return round(obj, decimals)
        elif isinstance(obj, dict):
            return {k: round_floats(v, decimals) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [round_floats(x, decimals) for x in obj]
        return obj

    report = {
        "metadata": metadata,
        "descriptive_summary": round_floats(summary),
        "within_model_tests": round_floats(tests),
        "cross_model_pooled_test": round_floats(cmh),
        "metric_distributions": round_floats(dists),
        "token_cost_analysis": round_floats(tokens),
    }

    return report


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Statistical analysis for cross-model experiment results"
    )
    parser.add_argument(
        "--input", type=Path, default=DEFAULT_INPUT,
        help=f"Path to results JSON (default: {DEFAULT_INPUT})"
    )
    parser.add_argument(
        "--output-json", type=Path, default=OUTPUT_JSON,
        help=f"Path for JSON report output (default: {OUTPUT_JSON})"
    )
    parser.add_argument(
        "--output-md", type=Path, default=OUTPUT_MD,
        help=f"Path for Markdown tables output (default: {OUTPUT_MD})"
    )
    args = parser.parse_args()

    # Metadata
    timestamp = datetime.now(timezone.utc).isoformat()
    git_hash = get_git_hash()

    print(f"Cross-Model Experiment: Statistical Analysis")
    print(f"Timestamp: {timestamp}")
    print(f"Git commit: {git_hash}")
    print(f"Input: {args.input}")
    print(f"scipy available: {SCIPY_AVAILABLE}")
    print()

    # Load data
    if not args.input.exists():
        print(f"ERROR: Input file not found: {args.input}")
        print(f"Run the experiment first: uv run run_cross_model_experiment.py")
        sys.exit(1)

    data = load_results(args.input)

    if not data:
        print("ERROR: No valid results to analyze.")
        sys.exit(1)

    # Count total and errors for metadata
    with open(args.input) as f:
        raw = json.load(f)
    n_total = len(raw)
    n_valid = len(data)
    n_errors = n_total - n_valid

    metadata = {
        "timestamp": timestamp,
        "git_hash": git_hash,
        "input_file": str(args.input),
        "n_total": n_total,
        "n_valid": n_valid,
        "n_errors": n_errors,
        "scipy_available": SCIPY_AVAILABLE,
        "models_observed": sorted(set(r["model_name"] for r in data)),
        "conditions_observed": sorted(set(r["condition"] for r in data)),
        "tasks_observed": sorted(set(r["task"] for r in data)),
    }

    # Run analyses
    summary = descriptive_summary(data)
    tests = within_model_tests(data)
    cmh = cross_model_pooled_test(data)
    dists = metric_distributions(data)
    tokens = token_cost_analysis(data)

    # Print to stdout
    print_descriptive(summary)
    print_hypothesis_tests(tests)
    print_cmh(cmh)
    print_metric_distributions(dists)
    print_token_costs(tokens)

    # Save JSON report
    report = build_json_report(metadata, summary, tests, cmh, dists, tokens)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_json, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nJSON report saved to: {args.output_json}")

    # Save Markdown tables
    md = generate_markdown(summary, tests, cmh, dists, tokens, metadata)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_md, "w") as f:
        f.write(md)
    print(f"Markdown tables saved to: {args.output_md}")

    # Final verdict summary
    print_section("SUMMARY VERDICT")
    print()

    # Check H0-1: U vs S within each model
    for t in tests:
        if t["comparison"] == "U vs S":
            sig = "REJECT" if t["p_value"] is not None and t["p_value"] < 0.05 else "FAIL TO REJECT"
            p_str = f"p={t['p_value']:.4f}" if t['p_value'] is not None else "N/A"
            print(f"  H0-1 ({t['model']}): U rate = S rate -> {sig} ({p_str}, h={t['cohens_h']:.2f})")

    # Check H0-2: U vs D within each model
    print()
    for t in tests:
        if t["comparison"] == "U vs D":
            sig = "REJECT" if t["p_value"] is not None and t["p_value"] < 0.05 else "FAIL TO REJECT"
            p_str = f"p={t['p_value']:.4f}" if t['p_value'] is not None else "N/A"
            print(f"  H0-2 ({t['model']}): U rate = D rate -> {sig} ({p_str}, h={t['cohens_h']:.2f})")

    # Check H0-3: Model-general U->S effect
    print()
    if cmh['cmh_p_value'] is not None:
        sig = "SUPPORTED" if cmh['cmh_p_value'] < 0.05 else "NOT SUPPORTED"
        print(f"  H0-3: U->S effect is model-general -> {sig} (CMH p={cmh['cmh_p_value']:.6f})")
    else:
        print(f"  H0-3: U->S effect is model-general -> CANNOT TEST (scipy unavailable)")

    print()


if __name__ == "__main__":
    main()
