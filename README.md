# STS-Project-2026

**Making Software Quality Visible: Converting AI-Generated Code from Credence Good to Inspection Good**

Software architecture is a *credence good* — buyers cannot verify its quality even after delivery. This project builds and validates **STS (Software Tier Standard)**, an automated audit framework that makes architecture quality measurable, contractable, and priceable. We demonstrate it on AI-generated code, where the problem is most acute.

## The Core Thesis

```
Invisible quality  →  Can't price it  →  Won't pay for it  →  Don't invest in it  →  Maintenance explodes
       ↓ STS breaks the cycle here
Visible quality    →  Priced in contract  →  Enforceable  →  Architecture investment justified
```

Three key findings from controlled experiments with Claude:

1. **Zero guidance = H-Tier.** Without architectural constraints, AI defaults to high-coupling code.
2. **Same AI, same requirements, two outcomes.** Architecture quality is bounded by prompt constraint strength, not AI capability.
3. **The audit standard acts as an implicit prompt.** AI self-corrects when it encounters quality specifications — even without being told to follow them.

See [PROPOSAL.md](PROPOSAL.md) for the full research framework, competitive positioning, and the medical data quality extension.

## Environment

- **AI Model:** Claude Opus 4.6 (`claude-opus-4-6`)
- **Client:** Claude Code v2.1.44
- **Audit Tool:** `sts_checker.py` v2.2 SAMA-Arch (radon-based, configurable policy engine)

## Note on Language & Metrics

The original experiments were conducted in a Chinese language environment. To ensure international accessibility, the codebase has been localized to English. While structural metrics (CC, ADF) remain identical, minor variances in Halstead metrics may exist due to token length differences. The original Chinese source prompts are preserved in `prompts/zh-CN/` for audit purposes.

## Experiment Design

### Case 01 — Controlled Comparison (Bookstore System)

Same AI, same prompt → simultaneously produced H-Tier (high-coupling) and Z-Tier (decoupled) variants. Identical requirement changes applied to both; H-Tier degraded (CC 17→23, +35%), Z-Tier remained stable.

### Case 02 — Zero-Guidance Entropy (Mall Settlement)

Constraint-free natural language prompt ("build a simple checkout") → AI defaulted to H-Tier, self-diagnosed as "closer to H-Tier," then demonstrated audit-aware behavior during refactoring (proactively switched `os.path` → `pathlib` after exposure to `sts_checker.py` criteria).

### Case 03 — Real-World Validation (Medical EEG System, 28 files)

v2.2 engine stress-tested against a research-grade Python codebase for Infant Spasm EEG Monitoring. 57.1% pass rate, Max CC=36, Max ADF=0.1391. Provided threshold calibration data (Precision-Recall elbow) and evidence that churn and complexity are co-indicators of architectural stress.

## Audit Results

> ADF values below are from the v2.0 baseline (boolean formula). v2.2 uses density-based ADF — see `CHANGELOG.md` for details.

| Case | Target | Phase | Max CC | ADF | Halstead | Verdict |
|------|--------|-------|--------|-----|----------|---------|
| 01 Bookstore | H_v1_mono | Step1 Initial | 17 | **0.20** | 2272.68 | H-TIER (FAILED) |
| 01 Bookstore | H_v2_mono | Step2 Iteration | **23** | **0.20** | 2980.98 | H-TIER (FAILED) |
| 01 Bookstore | Z_v1_mono | Step1 Initial | 4 | **0.20** | 1786.37 | H-TIER (FAILED) |
| 01 Bookstore | Z_v2_mono | Step2 Iteration | 9 | **0.20** | 3256.38 | H-TIER (FAILED) |
| 01 Bookstore | Z_v2_split/service | Step3 Split | 4 | **0.00** | 1087.82 | Z-TIER (PASSED) |
| 02 Mall | H_mono | Phase1 Zero-guidance | 3 | **0.20** | 1249.62 | H-TIER (FAILED) |
| 02 Mall | Z_split/service | Phase3 Refactored | 3 | **0.00** | 456.13 | Z-TIER (PASSED) |

## Causal Chain: Prompt → Architecture → Verdict

```
"build a simple checkout"               → H_mono.py      → ADF>0, TL=LOW    FAILED
"use Strategy pattern, Observer..."      → Z_split/service → ADF=0, TL=LOW    PASSED
  ↑ AI referenced sts_checker.py → proactively switched os.path → pathlib
```

**Architecture quality is not bounded by the AI's capability ceiling, but by the prompt's constraint strength. The audit standard itself acts as an implicit prompt.**

## Why This Matters

**For business school researchers:** STS converts software from a *credence good* (quality unverifiable even post-delivery) to an *inspection good* (quality deterministically verifiable). This enables complete contracts where previously only incomplete contracts were possible — a contribution at the intersection of information economics, contract theory, and software engineering.

**For enterprises:** A quantifiable "LEED rating" for AI-generated code quality. Outsourcing contracts can reference STS tiers, shifting dispute resolution from subjective haggling to engineering calculation.

**For developers:** Redefines the architect's role in the AI era — from "the person who writes code" to "the person who defines audit contracts."

**For medical/regulated domains:** The same "credence → inspection good" conversion applies to medical data quality for AI training sets, where the EU AI Act (Article 10, compliance by August 2027) creates regulatory demand.

## Project Structure

```
/STS-Project-2026
├── sts_checker.py             # Core audit engine (v2.2 SAMA-Arch)
├── pyproject.toml             # uv-managed dependencies (radon)
├── example.sts.toml           # Default audit policy template
├── PROPOSAL.md                # Full research proposal & competitive positioning
├── PROPOSAL_REWRITE_PLAN.md   # Narrative chain from original discussions
├── LICENSE                    # Apache License 2.0
├── README.md
│
├── /prompts                   # Reproducibility: all AI prompt transcripts
│   ├── case01_bookstore.md    # Step1 generate H+Z → Step2 apply pressure
│   ├── case02_mall.md         # Phase1 zero-guidance → Phase2 self-diagnosis → Phase3 refactor
│   └── /zh-CN                 # Original Chinese prompts (preserved for audit)
│       ├── case01_bookstore.md
│       └── case02_mall.md
│
├── /cases                     # Case library
│   ├── /01_bookstore_system
│   │   ├── H_v1_mono.py       # Step1: Initial high-coupling (CC=17)
│   │   ├── H_v2_mono.py       # Step2: Post-iteration (CC=23, +35%)
│   │   ├── Z_v1_mono.py       # Step1: Initial decoupled (CC=4)
│   │   ├── Z_v2_mono.py       # Step2: Post-iteration (CC=9, ADF=0.20)
│   │   └── /Z_v2_split        # Step3: Physical isolation
│   │       ├── service.py     #   Business layer (ADF=0.00)
│   │       └── views.py       #   Observers & UI
│   │
│   └── /02_mall_settlement
│       ├── H_mono.py          # Phase1: AI zero-guidance default output
│       └── /Z_split           # Phase3: Audit-aligned refactoring
│           ├── service.py     #   Business layer (ADF=0.00)
│           └── views.py       #   Receipt renderer
│
├── /evidence                  # Audit evidence
│   ├── metrics_baseline_v2.0.csv  # v2.0 baseline audit scoreboard
│   └── claude_confession.md   # Claude's architectural self-analysis
│
└── /docs                      # Contracts & standards
    ├── STS_Standard_v1.0.md   # STS tier classification standard
    └── SAMA-Arch_v2.2.md      # Software Architecture Maintenance Agreement
```

## Quick Reproduction

```bash
uv sync

# Single-file audit
uv run sts_checker.py cases/01_bookstore_system/H_v2_mono.py
uv run sts_checker.py cases/01_bookstore_system/Z_v2_split/service.py

# Directory scan (v2.2 SAMA-Arch — per-file table + project verdict)
uv run sts_checker.py cases/01_bookstore_system/
uv run sts_checker.py cases/

# Write JSON report (opt-in, non-invasive)
uv run sts_checker.py cases/ --output audit_report.json
```

## Disclaimer

This experiment explores quality boundaries in AI-assisted development. STS metrics serve as architectural stress indicators, not as the sole measure of code quality. Results may exhibit minor variance across runs due to the stochastic nature of `claude-opus-4-6` inference.

## License

This project is licensed under the [Apache License 2.0](LICENSE).
