# sts-audit

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-green.svg)](.python-version)
[![STS Engine](https://img.shields.io/badge/STS_Engine-v2.2_SAMA--Arch-orange.svg)](docs/SAMA-Arch_v2.2.md)

## Software Architecture Quality: From Credence Good to Search Good

Software architecture is a **credence good** (Darby & Karni, 1973) — buyers cannot verify its quality even after delivery. This information asymmetry creates adverse selection: buyers can't see quality → won't pay for it → developers stop investing → maintenance costs explode.

This project provides **experimental evidence** and an **audit tool** for research on automated quality certification — converting software architecture from a credence good into a search good via measurable, contractible metrics.

**Target venue:** Human x AI Finance Conference, UCLA Anderson School of Management, April 24, 2026.

## Research Findings

Cross-model experiments across three providers (seven model variants) under three information conditions (375 code generations):

| Finding | Evidence |
|---------|----------|
| **AI defaults to low-quality architecture** | 13.3% pooled certification rate under unconstrained conditions |
| **Specification resolves the asymmetry** | 100% certification under specification — universally, across every model |
| **Disclosure alone is insufficient** | No significant effect (p > 0.28 for all models) |
| **The effect is model-general** | Replicated across 3 providers, 7 model variants, 3 capability tiers |
| **Functional equivalence confirms credence good** | 100% functional correctness + 87% architectural failure (same code) |

## Quick Start

```bash
uv sync

# Audit a single file
uv run sts_checker.py cases/01_bookstore_system/H_v2_mono.py

# Audit a directory (project-level verdict)
uv run sts_checker.py cases/

# JSON report
uv run sts_checker.py cases/ --output audit_report.json
```

## How It Works

The audit engine (`sts_checker.py` v2.2) measures four structural risk indicators:

- **CC** (Cyclomatic Complexity) — branching complexity (McCabe, 1976)
- **ADF** (Architectural Drift Fraction) — I/O artifacts in business logic layers
- **CCR** (Code Churn Rate) — git-based change frequency (Nagappan & Ball, 2005)
- **TL** (Technical Lag) — deprecated API usage

Binary verdict: **Z-TIER (PASSED)** if all metrics within threshold, **H-TIER (FAILED)** otherwise. Thresholds configurable via `.sts.toml`. CI-ready exit code.

## Docker Blind Reviewer

An isolated peer review tool that enforces information boundaries at the container level. The reviewer cannot access prior reviews, version history, or project internals.

```bash
# Run a blind review (builds image automatically)
./docker/blind-reviewer/review.sh paper/your_paper.md

# Use a different model
REVIEWER_MODEL=claude-opus-4-6 ./docker/blind-reviewer/review.sh paper/your_paper.md

# Custom reviewer spec
./docker/blind-reviewer/review.sh paper/your_paper.md path/to/custom_spec.md
```

The container mounts only two files (read-only): the reviewer specification and the paper. Output is written to `output/reviews/` with timestamps for audit trail.

## Project Structure

```
STS-Project-2026/
│
├── sts_checker.py              # Audit engine (v2.2 SAMA-Arch)
├── run_cross_model_experiment.py  # Cross-model experiment runner
├── pyproject.toml              # Python project config (uv)
├── example.sts.toml            # Example audit threshold config
│
├── cases/                      # Case study code — the "lab specimens"
│   ├── 01_bookstore_system/    #   Controlled pair (H-Tier vs Z-Tier)
│   ├── 02_mall_settlement/     #   Zero-guidance entropy experiment
│   └── 03_inventory_system/    #   Third task for cross-model experiments
│
├── docker/                     # Containerized tools
│   └── blind-reviewer/         #   Docker-isolated blind peer reviewer
│       ├── Dockerfile
│       ├── review.py
│       ├── review.sh
│       └── specs/reviewer.md   #   Permanent reviewer criteria
│
├── evidence/                   # Collected research evidence
├── framework/                  # Research framework & methodology
│   ├── agent_specs.md          #   Agent role specifications
│   ├── audit_method.md         #   5-step adversarial audit method
│   └── experiments/            #   Experiment designs
│
└── docs/                       # Standards & specifications
    ├── STS_Standard_v1.0.md
    └── SAMA-Arch_v2.2.md
```

## Cross-Model Experiment

The experiment tests whether architectural quality degradation under AI code generation is model-general:

```bash
# Run the full experiment (requires API keys for Anthropic, OpenAI, Google)
uv run python run_cross_model_experiment.py

# Run specific tiers
uv run python run_cross_model_experiment.py --tier A B C

# Smoke test (1 run per model)
uv run python run_cross_model_experiment.py --smoke-test
```

Pre-registered design (commit `05f8902`). Results in `records/cross_model_results.json`.

## Key References

- Akerlof (1970) — Market for Lemons (information asymmetry)
- Darby & Karni (1973) — Credence goods taxonomy
- Dulleck & Kerschbamer (2006) — Economics of credence goods
- Hart & Moore (1988) — Incomplete contracts
- Lizzeri (1999) — Optimal certification design
- Jin & Leslie (2003) — Disclosure and quality (restaurant hygiene grades)
- Banker et al. (1993) — Software maintenance cost functions

## License

Apache License 2.0 — see [LICENSE](LICENSE).
