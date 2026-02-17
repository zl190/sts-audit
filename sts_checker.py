"""STS Architectural Audit Tool v2.2 (SAMA-Arch)

General-purpose architectural policy engine.
Computes CC, MI, Halstead, CCR, ADF, TL and produces
terminal reports + optional machine-readable JSON.

Usage:
    uv run sts_checker.py <file.py>                        # single-file audit
    uv run sts_checker.py <directory/>                      # project-level scan
    uv run sts_checker.py <directory/> --output report.json # write JSON to file

Configuration:
    Place a .sts.toml in your project root to customize
    thresholds and illegal patterns.  Schema:

        [thresholds]
        max_cc = 20           # per-file CC ceiling
        adf = 0.05            # per-file ADF ceiling (density)
        ccr = 0.3             # per-file / project CCR ceiling
        project_max_cc = 10   # project-level CC ceiling

        [patterns]
        illegal = ["import tkinter", "from bookstore_ui", "print("]

        [skip]
        dirs = ["__pycache__", ".venv", "venv", ".git"]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

from radon.complexity import cc_visit
from radon.metrics import h_visit, mi_visit


# ── Configuration ──────────────────────────────────────────────────
@dataclass(frozen=True, slots=True)
class Config:
    illegal_patterns: tuple[str, ...]
    cc_threshold: int
    adf_threshold: float
    ccr_threshold: float
    project_cc_threshold: int
    skip_dirs: frozenset[str]


DEFAULT_CONFIG = Config(
    illegal_patterns=("import tkinter", "from bookstore_ui", "print("),
    cc_threshold=20,
    adf_threshold=0.05,
    ccr_threshold=0.3,
    project_cc_threshold=10,
    skip_dirs=frozenset({"__pycache__", ".venv", "venv", ".git"}),
)


def _find_config(start: Path) -> Path | None:
    """Walk up from *start* looking for .sts.toml."""
    current = start if start.is_dir() else start.parent
    for directory in (current, *current.parents):
        candidate = directory / ".sts.toml"
        if candidate.is_file():
            return candidate
    return None


def load_config(target: Path) -> Config:
    """Load .sts.toml if found, otherwise return defaults."""
    path = _find_config(target)
    if path is None:
        return DEFAULT_CONFIG

    with path.open("rb") as f:
        raw = tomllib.load(f)

    t = raw.get("thresholds", {})
    p = raw.get("patterns", {})
    s = raw.get("skip", {})

    return Config(
        illegal_patterns=tuple(p.get("illegal", DEFAULT_CONFIG.illegal_patterns)),
        cc_threshold=t.get("max_cc", DEFAULT_CONFIG.cc_threshold),
        adf_threshold=t.get("adf", DEFAULT_CONFIG.adf_threshold),
        ccr_threshold=t.get("ccr", DEFAULT_CONFIG.ccr_threshold),
        project_cc_threshold=t.get("project_max_cc", DEFAULT_CONFIG.project_cc_threshold),
        skip_dirs=frozenset(s.get("dirs", DEFAULT_CONFIG.skip_dirs)),
    )


# ── Data structures ────────────────────────────────────────────────
@dataclass(frozen=True, slots=True)
class FileReport:
    path: Path
    max_cc: int
    mi_score: float
    h_difficulty: float
    h_effort: float
    ccr: float
    adf: float
    tl: str
    tl_instances: tuple[str, ...]
    verdict: str


@dataclass(frozen=True, slots=True)
class ProjectReport:
    total_files: int
    max_cc: int
    mean_cc: float
    max_adf: float
    polluted_files: tuple[Path, ...]
    mean_ccr: float
    max_ccr: float
    global_tl: str
    tl_instances: tuple[str, ...]
    verdict: str


# ── File collection ────────────────────────────────────────────────
def collect_files(directory: Path, config: Config) -> list[Path]:
    """Recursively collect *.py files, skipping configured directories."""
    files: list[Path] = []
    for p in sorted(directory.rglob("*.py")):
        if any(part in config.skip_dirs for part in p.parts):
            continue
        if p.name == "__init__.py":
            continue
        files.append(p)
    return files


# ── Core audit ─────────────────────────────────────────────────────
def audit_file(path: Path, config: Config) -> FileReport:
    """Pure function: read one file and return a frozen FileReport."""
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    total_lines = len(lines)

    # -- Radon metrics --
    cc_results = cc_visit(content)
    max_cc = max((b.complexity for b in cc_results), default=0)
    mi_score = mi_visit(content, multi=True)
    h_metrics = h_visit(content)
    h_difficulty = h_metrics.total.difficulty
    h_effort = h_metrics.total.effort

    # -- CCR (Code Churn Rate) --
    ccr = _compute_ccr(path)

    # -- ADF (Architecture Drift Factor) — density-based --
    if total_lines == 0:
        adf = 0.0
    else:
        drift_lines = sum(
            1 for line in lines
            if any(p in line for p in config.illegal_patterns)
        )
        adf = drift_lines / total_lines

    # -- TL (Technical Lag) with line-level evidence --
    tl_instances = _detect_tl(path, content)
    tl = "HIGH" if tl_instances else "LOW"

    # -- Verdict --
    is_failed = (
        max_cc > config.cc_threshold
        or adf > config.adf_threshold
        or ccr > config.ccr_threshold
    )
    verdict = "H-TIER (FAILED)" if is_failed else "Z-TIER (PASSED)"

    return FileReport(
        path=path,
        max_cc=max_cc,
        mi_score=mi_score,
        h_difficulty=h_difficulty,
        h_effort=h_effort,
        ccr=ccr,
        adf=adf,
        tl=tl,
        tl_instances=tuple(tl_instances),
        verdict=verdict,
    )


def _compute_ccr(path: Path) -> float:
    """Git churn rate over 14-day window (safe subprocess, no shell)."""
    try:
        result = subprocess.run(
            [
                "git", "log",
                "--since=14 days ago",
                "--format=format:",
                "--name-only",
                "--", str(path),
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        churn_count = sum(1 for line in result.stdout.splitlines() if line.strip())
        return min(churn_count / 10.0, 1.0)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return 0.0


def _detect_tl(path: Path, content: str) -> list[str]:
    """Return list of 'file:lineno' strings for each os.path usage."""
    instances: list[str] = []
    for lineno, line in enumerate(content.splitlines(), start=1):
        if "os.path" in line:
            instances.append(f"{path}:{lineno}")
    return instances


# ── Aggregation ────────────────────────────────────────────────────
def aggregate(reports: list[FileReport], config: Config) -> ProjectReport:
    """Combine per-file reports into a project-level summary."""
    all_cc = [r.max_cc for r in reports]
    all_ccr = [r.ccr for r in reports]
    polluted = tuple(r.path for r in reports if r.adf > 0.0)
    all_tl: list[str] = []
    for r in reports:
        all_tl.extend(r.tl_instances)

    max_adf = max((r.adf for r in reports), default=0.0)
    global_tl = "HIGH" if all_tl else "LOW"

    max_cc = max(all_cc, default=0)
    mean_cc = mean(all_cc) if all_cc else 0.0
    mean_ccr = mean(all_ccr) if all_ccr else 0.0
    max_ccr = max(all_ccr, default=0.0)

    # Z-TIER project verdict: strict
    is_z = (
        max_cc < config.project_cc_threshold
        and max_adf < config.adf_threshold
        and global_tl == "LOW"
        and max_ccr <= config.ccr_threshold
    )
    verdict = "Z-TIER (PASSED)" if is_z else "H-TIER (FAILED)"

    return ProjectReport(
        total_files=len(reports),
        max_cc=max_cc,
        mean_cc=mean_cc,
        max_adf=max_adf,
        polluted_files=polluted,
        mean_ccr=mean_ccr,
        max_ccr=max_ccr,
        global_tl=global_tl,
        tl_instances=tuple(all_tl),
        verdict=verdict,
    )


# ── Terminal output ────────────────────────────────────────────────
def print_file_report(r: FileReport, config: Config) -> None:
    """Single-file terminal output."""
    print("=" * 50)
    print("        STS ARCHITECTURAL AUDIT v2.2")
    print("=" * 50)
    print(f"Target: {r.path}")
    print(f"Verdict: [{r.verdict}]")
    print("-" * 50)
    print("[Core Metrics]")
    print(f"  Max Cyclomatic Complexity : {r.max_cc} (Limit: {config.cc_threshold})")
    print(f"  Maintainability Index     : {r.mi_score:.2f} (Limit: 20+)")
    print(f"  Halstead Effort           : {r.h_effort:.2f}")
    print("-" * 50)
    print("[2026 Consensus Audit]")
    print(f"  Code Churn Rate (CCR)     : {r.ccr:.2%} (Limit: {config.ccr_threshold:.0%})")
    print(f"  Architecture Drift (ADF)  : {r.adf:.4f} (Limit: {config.adf_threshold})")
    print(f"  Technical Lag (TL)        : {r.tl}")
    if r.tl_instances:
        for inst in r.tl_instances:
            print(f"    -> {inst}")
    print("-" * 50)
    if "FAILED" in r.verdict:
        print("FINDING : Architectural integrity compromised.")
        print("ACTION  : REJECT DELIVERY / MANDATORY REFACTORING.")
    else:
        print("FINDING : Architecture is healthy and scalable.")
    print("=" * 50)


def print_project_report(
    file_reports: list[FileReport], project: ProjectReport, config: Config
) -> None:
    """Per-file table + project aggregation summary."""
    print("=" * 70)
    print("        STS PROJECT AUDIT v2.2 (SAMA-Arch)")
    print("=" * 70)
    print(f"  Files scanned: {project.total_files}")
    print("-" * 70)

    # Per-file table
    header = f"{'File':<40} {'CC':>4} {'ADF':>7} {'TL':<5} {'Verdict'}"
    print(header)
    print("-" * 70)
    for r in file_reports:
        name = str(r.path)
        if len(name) > 38:
            name = "..." + name[-35:]
        print(f"{name:<40} {r.max_cc:>4} {r.adf:>7.4f} {r.tl:<5} {r.verdict}")
    print("-" * 70)

    # Aggregation
    print("[Project Summary]")
    print(f"  Max CC (across all files) : {project.max_cc}")
    print(f"  Mean CC                   : {project.mean_cc:.1f}")
    print(f"  Max ADF                   : {project.max_adf:.4f}")
    if project.polluted_files:
        print(f"  Polluted files ({len(project.polluted_files)}):")
        for p in project.polluted_files:
            print(f"    -> {p}")
    print(f"  Mean CCR                  : {project.mean_ccr:.2%}")
    print(f"  Max CCR                   : {project.max_ccr:.2%}")
    print(f"  Global TL                 : {project.global_tl}")
    if project.tl_instances:
        for inst in project.tl_instances:
            print(f"    -> {inst}")
    print("-" * 70)
    print(f"  Project Verdict: [{project.verdict}]")
    if "FAILED" in project.verdict:
        print(
            f"  Z-TIER requires: max_cc < {config.project_cc_threshold}, "
            f"max_adf < {config.adf_threshold}, global_tl == LOW, "
            f"max_ccr <= {config.ccr_threshold:.0%}"
        )
    print("=" * 70)


# ── JSON output ────────────────────────────────────────────────────
def build_json(
    target: Path,
    file_reports: list[FileReport],
    project: ProjectReport | None,
) -> dict:
    """Build the audit JSON payload."""
    data: dict = {
        "version": "2.2",
        "target": str(target),
    }
    if project is not None:
        data["project"] = {
            "total_files": project.total_files,
            "max_cc": project.max_cc,
            "mean_cc": round(project.mean_cc, 2),
            "max_adf": round(project.max_adf, 4),
            "polluted_files": [str(p) for p in project.polluted_files],
            "mean_ccr": round(project.mean_ccr, 4),
            "max_ccr": round(project.max_ccr, 4),
            "global_tl": project.global_tl,
            "tl_instances": list(project.tl_instances),
            "verdict": project.verdict,
        }
    data["files"] = [
        {
            "path": str(r.path),
            "max_cc": r.max_cc,
            "mi_score": round(r.mi_score, 2),
            "h_difficulty": round(r.h_difficulty, 2),
            "h_effort": round(r.h_effort, 2),
            "ccr": round(r.ccr, 4),
            "adf": round(r.adf, 4),
            "tl": r.tl,
            "tl_instances": list(r.tl_instances),
            "verdict": r.verdict,
        }
        for r in file_reports
    ]
    return data


def write_json(path: Path, data: dict) -> None:
    """Write audit JSON to the given path."""
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


# ── CLI ────────────────────────────────────────────────────────────
def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="sts_checker",
        description="STS Architectural Audit Tool v2.2 (SAMA-Arch)",
    )
    parser.add_argument(
        "target",
        type=Path,
        help="Python file or directory to audit",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Write JSON report to this path (default: no JSON output)",
    )
    return parser.parse_args(argv[1:])


def main(argv: list[str]) -> None:
    args = parse_args(argv)
    target: Path = args.target
    config = load_config(target)

    failed = False

    if target.is_file():
        # Single-file mode
        report = audit_file(target, config)
        print_file_report(report, config)
        failed = "FAILED" in report.verdict
        if args.output:
            data = build_json(target, [report], None)
            write_json(args.output, data)
            print(f"\nJSON written to {args.output}")

    elif target.is_dir():
        # Project-level scan
        files = collect_files(target, config)
        if not files:
            print(f"No .py files found in {target}")
            sys.exit(1)
        file_reports = [audit_file(f, config) for f in files]
        project = aggregate(file_reports, config)
        print_project_report(file_reports, project, config)
        failed = "FAILED" in project.verdict
        if args.output:
            data = build_json(target, file_reports, project)
            write_json(args.output, data)
            print(f"\nJSON written to {args.output}")

    else:
        print(f"Error: {target} is not a file or directory")
        sys.exit(1)

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
