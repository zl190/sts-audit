# STS Tier Classification Standard v1.0

## Overview

STS (Software Tier Standard) is an architectural quality audit framework for AI-generated code. It combines classical software metrics (CC, MI, Halstead) with 2026 engineering consensus dimensions (ADF, CCR, TL) to produce a binary verdict: **Z-TIER (PASSED)** or **H-TIER (FAILED)**.

## Metric Dimensions

### Core Metrics

| Metric | Full Name | Tool | Red Line |
|--------|-----------|------|----------|
| CC | Cyclomatic Complexity | `radon cc` | Max CC > 20 |
| MI | Maintainability Index | `radon mi` | MI < 20 |
| Halstead | Halstead Effort | `radon hal` | Advisory only, no hard threshold |

### Consensus Metrics

| Metric | Full Name | Detection Method | Red Line |
|--------|-----------|-----------------|----------|
| ADF | Architecture Drift Factor | Density of illegal patterns per line (`print(`, UI lib imports) | ADF > 0.05 (configurable) |
| CCR | Code Churn Rate | Git modification frequency over 14-day window | CCR > 30% |
| TL | Technical Lag | Use of deprecated APIs (`os.path` vs `pathlib`) | Flag; does not single-handedly fail |

### Verdict Logic (Per-File)

$$is\_failed = (CC_{max} > \texttt{cc\_threshold}) \lor (ADF > \texttt{adf\_threshold}) \lor (CCR > \texttt{ccr\_threshold})$$

```
FAILED (H-TIER)  iff any of the above conditions hold
PASSED (Z-TIER)  otherwise
```

Default thresholds: `cc=20, adf=0.05, ccr=0.3`. Configurable via `.sts.toml`.

### ADF Formula (v2.2)

$$ADF = \frac{\text{lines matching illegal patterns}}{\text{total lines}}$$

This density-based metric replaces the v2.0 boolean formula (`pattern_count / 5.0`). It scales with file size — the same number of violations produces a lower ADF in a larger file, reflecting lower drift density.

## Tier Definitions

### H-TIER (High Coupling Tier)

**Characteristics:**
- Single class/method bears multiple responsibilities (compute + render + persist + notify)
- Business logic layer contains `print()` or UI framework calls
- Requirement changes require modification of core business methods
- No abstract interfaces (ABC); strategies hardcoded as if-else chains

**Risks:**
- CC grows exponentially under requirement iteration
- Business logic cannot be unit-tested independently (depends on UI side effects)

### Z-TIER (Zero-Drift Tier)

**Characteristics:**
- Business layer has zero UI dependencies (ADF = 0.00)
- Strategy pattern encapsulates variation points; new variants require no existing code changes (OCP)
- Observer pattern decouples notifications; new channels require only registration
- ABC defines clear module contracts

**Benefits:**
- CC growth is O(1) per iteration, not O(n)
- Business logic is independently unit-testable
- Physical module boundaries are continuously enforced by automated audit tools

## Audit Execution

```bash
python sts_checker.py <target_file.py>
```

**Key principle:** The audit target should be the business layer module (service.py), not the UI assembly layer (views.py). Physical isolation is a prerequisite for ADF=0 — logical decoupling within a single file is insufficient to pass the audit.

## Project-Level Verdict (SAMA-Arch v2.2)

When `sts_checker.py` is invoked on a directory, it scans all `.py` files recursively (skipping configurable directories and `__init__.py`) and produces a project-level verdict.

### Aggregation Rules

| Metric | Aggregation |
|--------|-------------|
| Max CC | Maximum of per-file max CC |
| Mean CC | Arithmetic mean of per-file max CC |
| Max ADF | Maximum of per-file ADF (density) |
| Polluted files | Files with ADF > 0 |
| Mean CCR | Arithmetic mean of per-file CCR |
| Max CCR | Maximum of per-file CCR |
| Global TL | HIGH if any file has `os.path` usage; LOW otherwise |

### Project Verdict Logic

$$Z\text{-TIER} \iff (CC_{max} < \texttt{project\_cc}) \land (ADF_{max} < \texttt{adf\_threshold}) \land (TL_{global} = \text{LOW}) \land (CCR_{max} \leq \texttt{ccr\_threshold})$$

This is stricter than the per-file verdict — a project can contain individually-passing files yet still fail at the project level if any file has elevated CC, high drift density, or high churn.

### Output

- **Terminal:** Per-file table (CC, ADF, TL, verdict) followed by project summary
- **JSON:** opt-in via `--output <path>` flag (never auto-written to target tree)

### CI Integration

Exit code is **1** when the verdict is H-TIER (FAILED), enabling use as a CI gate:

```bash
uv run sts_checker.py src/ || echo "Audit failed"
```

### TL Sensitivity Notes

- **Case 01:** Marked as `TL: HIGH` due to legacy API usage (`os.path`), demonstrating the auditor's sensitivity to technical debt.
- **Case 02:** Achieved `TL: LOW` as the AI proactively aligned with modern standards (`pathlib`) under STS protocol constraints.
