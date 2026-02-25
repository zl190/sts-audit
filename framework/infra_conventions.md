# Infrastructure Conventions

Prescriptive rules for any agent adding infrastructure to this repo. Follow these exactly.

## Directory Structure

```
STS-Project-2026/
├── sts_checker.py              # Audit engine — DO NOT MODIFY without updating evidence/
├── run_cross_model_experiment.py
├── pyproject.toml              # Root Python deps (uv)
├── example.sts.toml            # Template audit config
│
├── cases/NN_description/       # Lab specimens (intentionally good or bad code)
├── docker/tool-name/           # Containerized tools (isolation-critical)
├── evidence/                   # Collected metrics, baselines, analysis
├── framework/                  # Methodology, agent specs, experiment designs
│   └── experiments/            # Pre-registered experiment protocols
├── docs/                       # Published standards (STS, SAMA-Arch)
│
├── paper/                      # GITIGNORED — working drafts
├── notes/                      # GITIGNORED — scratch, strategy, logs
├── records/                    # GITIGNORED — version registry, changelogs
└── output/                     # GITIGNORED — review outputs
```

## File Placement Decision Tree

Ask in order:

1. **Is it a reusable tool that needs isolation?** --> `docker/<tool-name>/`
2. **Is it a reusable tool that does NOT need isolation?** --> Root (e.g., `sts_checker.py`) or a script in root
3. **Is it methodology, protocol, or experiment design?** --> `framework/` (experiments go in `framework/experiments/`)
4. **Is it collected results, baselines, or analysis artifacts?** --> `evidence/`
5. **Is it a formal standard or specification document?** --> `docs/`
6. **Is it case study code (H-Tier or Z-Tier)?** --> `cases/NN_description/`
7. **Is it a paper draft, review output, scratch note, or log?** --> Local only. DO NOT commit. See "What NOT to Commit" below.
8. **Is it raw experiment data (generated code files, API responses)?** --> DO NOT commit. Archive as a GitHub Release artifact.

## Case Directories

### Numbering

Sequential two-digit prefix: `01_`, `02_`, `03_`, etc. Use the next available number. Check `ls cases/` before creating.

### Internal Structure

Each case has two variants — both required:

| Variant | Path | Purpose |
|---------|------|---------|
| H-Tier (bad) | `cases/NN_name/H_mono.py` | Monolithic, high-coupling. Single file. |
| Z-Tier (good) | `cases/NN_name/Z_split/` | Decoupled. Contains `service.py` + `views.py`. |

Older cases (01) have versioned names (`H_v1_mono.py`, `Z_v2_split/`). New cases use the simpler convention: `H_mono.py`, `Z_split/`.

### Rules

- **Never refactor case files to "improve" them.** Quality levels are intentional experimental specimens.
- `service.py` is the audit target. `views.py` is the UI layer (not audited).
- Split cases must run from their directory: `cd cases/NN_name/Z_split && python views.py`
- If you edit a case file, verify that CC and ADF still match `evidence/metrics_baseline_v2.0.csv`. If Halstead drifts from string changes, update the CSV. CC and ADF must never change from translation or string-only edits.

## Experiment Files

### Naming

- Design documents: `framework/experiments/exp<N>_<short_name>.md`
  - Examples: `exp1_gate_effectiveness.md`, `exp7_autonomous_convergence.md`
- Runner scripts: root-level Python files (e.g., `run_cross_model_experiment.py`)
- Results data: `records/` (gitignored) or `evidence/` (if curated for the paper)
- Raw generated code: `cases/cross_model/` (gitignored — archive as Release)

### Pre-registration

Experiment designs must be committed BEFORE running. Record the commit hash. The cross-model experiment was pre-registered at commit `05f8902`.

## Docker Tool Pattern

Every containerized tool follows the blind-reviewer template:

```
docker/<tool-name>/
├── Dockerfile          # Build instructions
├── <tool>.py           # Python entry point (ENTRYPOINT in Dockerfile)
├── <tool>.sh           # Host-side shell wrapper (user-facing CLI)
└── specs/              # Specification files mounted into container
    └── <spec>.md
```

### Dockerfile Conventions

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY <tool>.py /app/<tool>.py
WORKDIR /app
RUN uv pip install --system --no-cache <deps>
ENTRYPOINT ["python", "<tool>.py"]
```

Key points:
- Base image: `python:3.12-slim`
- Install uv via multi-stage copy from `ghcr.io/astral-sh/uv:latest`
- Use `uv pip install --system --no-cache` (not pip directly)
- Pin minimum dependency versions (e.g., `anthropic>=0.83.0`)

### Shell Wrapper Conventions

```bash
#!/usr/bin/env bash
set -euo pipefail
```

The wrapper must:
- Validate required env vars (API keys) and input files before calling Docker
- Resolve all paths to absolute before mounting
- Mount input files as `:ro` (read-only)
- Mount output directory as writable
- Build the image (`docker build -q -t <image-name>`) on every invocation (idempotent, uses cache)
- Print what it's doing (paper path, spec path, model, output dir)

### Isolation Principle

The container filesystem IS the isolation boundary. Only mount what the tool should see. For blind review, this means: spec file + paper file only. No prior reviews, no version history, no project files.

## Dependency Management

### Root Project

- Tool: `uv` (not pip, not poetry)
- Lock file: `uv.lock` (committed)
- Add a dep: `uv add <package>`
- Install: `uv sync`
- Run scripts: `uv run python <script>.py` or `uv run sts_checker.py`

### Docker Containers

- Install uv into container via `COPY --from=ghcr.io/astral-sh/uv:latest`
- Install deps with `uv pip install --system --no-cache`
- Do NOT copy `pyproject.toml` or `uv.lock` into containers — containers are self-contained with their own minimal deps

### Python Version

- Minimum: 3.12 (see `.python-version` and `pyproject.toml`)

## What NOT to Commit

These directories are gitignored with reason:

| Path | Reason | Where it goes instead |
|------|--------|-----------------------|
| `paper/` | Working drafts — large, versioned locally | Local only |
| `notes/` | Scratch ideas, strategy docs, reviews | Local only |
| `records/` | Orchestrator logs, version registry, changelogs | Local only |
| `output/` | Docker tool outputs (reviews with scores) | Local only |
| `cases/cross_model/` | Raw experiment data (1,709+ generated files) | GitHub Release artifact |
| `framework/experiments/independent_review_*.md` | Review outputs from blind reviewer experiments | Local only |
| `.sts.toml` | Local audit config (use `example.sts.toml` as template) | Local only |
| `.claude/` | Claude Code session data | Local only |

### Rule of Thumb

If a file is generated output, contains scores/verdicts, or is a working draft -- it stays local. If it's reusable methodology, a tool, or curated evidence for the paper -- it gets committed.

## Audit Config

- Template: `example.sts.toml` (committed)
- Active config: `.sts.toml` (gitignored, local)
- `sts_checker.py` walks up from the target file to find `.sts.toml`. Without one, bookstore defaults apply.
- The config controls thresholds (`max_cc`, `adf`, `ccr`, `project_max_cc`) and illegal patterns.

## Checklist for Adding New Infrastructure

- [ ] Classified the file using the placement decision tree above
- [ ] Used the correct naming convention (case numbering, experiment numbering)
- [ ] If Docker tool: followed the Dockerfile/wrapper/specs pattern from blind-reviewer
- [ ] If Docker tool: shell wrapper validates inputs and mounts files `:ro`
- [ ] If new Python dep: added via `uv add`, not manual `pyproject.toml` edit
- [ ] If new case: both H-Tier and Z-Tier variants exist
- [ ] If new case: ran `uv run sts_checker.py` on service.py and recorded baseline
- [ ] Nothing in `paper/`, `notes/`, `records/`, or `output/` was committed
- [ ] Raw experiment data archived as Release, not committed
