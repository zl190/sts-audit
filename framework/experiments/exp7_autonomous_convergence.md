# Experiment 7: Autonomous Convergence — Can the Wheel Run Without the Human?

## Motivation

The paper (v4, Section 6.6) claims that certification provides convergence infrastructure for agentic AI loops. But the v1→v4 trajectory used human-designed quality gates and human strategic direction at each cycle. The v4 reviewer asked directly:

> "How do you distinguish the effect of the certification instrument from the effect of human judgment about what to audit? Would the iterative process converge without a human directing the audit criteria?"

This experiment answers that question with data.

## Hypothesis

**H1 (strong):** An autonomous agentic loop — equipped with the full accumulated institutional knowledge (quality gates, agent specs, audit method, experiment results) but no human intervention — can continue to improve paper quality beyond the human-directed baseline.

**H0 (null):** The autonomous loop plateaus or degrades. Score stagnates at ~3.5, structural issues persist, and improvements are limited to cosmetic edits.

**H2 (alternative):** The autonomous loop improves on SOME dimensions (those addressable by the agents' tools — running experiments, searching literature, solving equations) but not others (those requiring human strategic judgment — framing decisions, scope changes, co-author recruitment).

## Design

### Baseline

v4: Score 3.5/5, 19 issues (3 critical, 8 substantive, 8 cosmetic). Human-directed, includes scope expansion (Section 6.6) that didn't address prior reviewer feedback.

### Treatment

Six autonomous cycles (v5 through v10), each executing the full convergence wheel:

1. **Auditor** reads the current version + the most recent review. Produces issue list with severity.
2. **Fixer** addresses as many issues as possible. Produces next version.
3. **Reviewer** (blind) scores the new version independently. Produces score + issue list.
4. **Synthesizer** compiles trajectory data. Produces delta report.
5. **Cycle repeats** from step 1 using the new version and new review.

### Agent Capabilities (FULL — not handicapped)

Agents have access to ALL tools. They are NOT limited to text editing. Specifically, they CAN:

- **Run code:** `uv run sts_checker.py` for code experiments, Python for analysis
- **Search the web:** find papers, verify citations, check statistics
- **Run new experiments:** generate code across multiple prompts/tasks, collect metrics
- **Attempt formalization:** solve simplified models, derive equilibrium conditions
- **Collect data:** run the same prompt N times to measure variance

This is critical for scientific honesty. Restricting agents to text editing would rig the experiment to confirm H0. The agents should have every capability a research assistant would have.

### Agent Constraints

Agents have access to the full Memory layer:
- `framework/agent_specs.md` (role constraints)
- `framework/quality_gates.md` (6 quality gates)
- `framework/audit_method.md` (5-step method)
- `records/version_registry.md` (trajectory history)
- `framework/experiments/independent_review_v4.md` (most recent review)
- All prior experiment results

Agents do NOT have:
- Human direction on WHAT to work on (they must decide from the review feedback)
- Human judgment on WHETHER improvements are strategically valuable
- Permission to change the paper's core framing or thesis
- Permission to modify the main version line (they write to `paper/`)

### What "No Human Intervention" Means

- No human reviews agent output between cycles
- No human adjusts quality gates or agent specs during the run
- No human provides strategic direction ("focus on X, ignore Y")
- No human decides which reviewer issues to prioritize
- The agent must make ALL decisions based on the accumulated institutional knowledge + the most recent review

The human's contribution is ONLY at the design stage (this document). After launch, the wheel runs until 6 cycles are complete.

### Versioning

Sequential numbering. The version registry (`records/version_registry.md`) tracks purpose, type, and whether each version was human-directed or autonomous. No special naming — the metadata lives in the registry, not the filename.

```
v1 → v2 → v3 → v4 → v5 → v6 → v7 → v8 → v9 → v10
|--- human-directed ---|--- autonomous (Exp 7) ---|

Files:
  paper/STS_Finance_Paper_v5.md
  paper/STS_Finance_Paper_v6.md
  ...
  framework/experiments/independent_review_v5.md
  framework/experiments/independent_review_v6.md
  ...
```

## Measurement

### Primary Metrics

For each cycle:
1. **Overall reviewer score** (1-5 scale)
2. **Issue count** by severity (critical / substantive / cosmetic)
3. **Dimension-by-dimension scores** (8 dimensions)

### Secondary Metrics

1. **What did the agent change?** Categorize each change as: text edit, new experiment, new citation, formalization attempt, structural reorganization
2. **Did the agent address critical issues?** Track which of the 3 persistent critical issues the agent attempted to resolve, and whether the reviewer acknowledged the improvement
3. **Did the agent introduce new issues?** Track issues created by agent changes (the v4 pattern: fixing some, creating others)
4. **Convergence rate:** Is delta-s decreasing, constant, or increasing across cycles?

### Trajectory Comparison

| Regime | Cycles | Score trajectory | Issue trajectory | Agent type |
|--------|--------|-----------------|-----------------|------------|
| Human-directed (v1→v4) | 4 | 3.0 → 3.3 → 3.5 → 3.5 | 26 → 23 → 18 → 19 | Human + AI |
| Autonomous (v4→v10) | 6 | ? | ? | AI only |

## Predictions (stated before running)

### Score Prediction

- **Cycles 1-2:** Score improves to ~3.6-3.7. The agents will fix the orphaned Howell & Potgieter reference, trim abstract redundancy, address some substantive issues. These are tractable text improvements.
- **Cycles 3-4:** Unclear. If agents attempt new experiments or formalization, score could jump (+0.3-0.5 on theoretical rigor or empirical evidence). If agents only do text edits, score plateaus at ~3.6-3.7.
- **Cycles 5-6:** Unknown. Possible continued improvement if agents have been accumulating new evidence. Possible degradation if agents start over-editing or cycling on cosmetic changes.

### Issue Prediction

Critical issues require NEW WORK, not editing:
1. Empirical evidence → agents CAN run new experiments (generate code with multiple prompts, multiple models via API)
2. Parameter estimation → agents CAN attempt calibration from open-source project data
3. Welfare analysis → agents CAN attempt a simplified formal model

Whether agents WILL attempt these (vs. defaulting to safe text edits) is the key unknown. This is the heart of the experiment.

### What Would Confirm Each Hypothesis

- **H1 confirmed (strong):** Score reaches 4.0+ by cycle 6, with at least one critical issue resolved through new work (not reframing)
- **H0 confirmed (null):** Score stays at 3.5-3.7, all changes are text edits, critical issues persist unchanged
- **H2 confirmed (alternative):** Score reaches 3.7-3.9, some dimensions improve substantially (e.g., literature engagement goes to 4.5) while others stay flat (e.g., empirical evidence stays at 2.5)

## Validity Threats

1. **Same model everywhere.** Generator, Auditor, Fixer, Reviewer are all Claude Opus 4.6. The Reviewer may systematically fail to catch issues that Claude introduces, creating an artificial ceiling. A proper experiment would use diverse reviewer models.

2. **Reviewer calibration drift.** With 10 total reviews (v1-v4 + 6 auto cycles), the scoring scale may drift. Scores are not anchored to an external standard.

3. **Agent specs encode human judgment.** The agents operate under constraints (agent_specs.md) designed by the human. The autonomous loop is not truly "zero human" — it's "human judgment front-loaded into the system design." This is actually the most interesting finding if the loop works: it means the human's value can be encoded in infrastructure.

4. **Quality gates are static.** The 6 gates in quality_gates.md were designed from v1 audit patterns. They may not cover failure modes that emerge in later cycles. A human would update gates; the autonomous loop cannot (by design).

5. **The experiment is not blind to its own hypothesis.** This experiment design document exists. If an agent reads it, it knows what's being tested. Mitigation: the Auditor and Fixer should NOT be pointed to this file. The Reviewer must NOT be pointed to it.

## Execution Protocol

Each cycle is launched as a single orchestrated background task:

```
Cycle N:
  Input: paper/STS_Finance_Paper_v{4+N-1}.md (or v4.md for N=1)
         framework/experiments/independent_review_v{4+N-1}.md (or v4 review for N=1)

  Step 1 (Auditor): Read paper + review. Produce issue list.
  Step 2 (Fixer): Read paper + issue list. Produce v{4+N}.md.
  Step 3 (Reviewer, BLIND): Read ONLY v{4+N}.md. Produce review.
  Step 4 (Synthesizer): Update trajectory table.

  Output: paper/STS_Finance_Paper_v{4+N}.md
          framework/experiments/independent_review_v{4+N}.md
          Updated trajectory in records/version_registry.md
```

## Value to the Paper

If this experiment produces data, it can be added to Appendix A alongside the human-directed trajectory. The comparison directly answers the v4 reviewer's Question 5. Possible framings depending on outcome:

- **If H0:** "The autonomous loop plateaued at [score], with critical issues persisting across [N] cycles. This is consistent with the claim that certification provides a necessary but not sufficient condition for convergence — human strategic direction provides the external signal that determines which quality dimensions improve."

- **If H1:** "The autonomous loop continued to improve beyond the human-directed baseline, reaching [score] by cycle [N]. This suggests that the certification instrument, when combined with well-designed agent specifications and accumulated institutional knowledge, can sustain quality convergence without ongoing human intervention. The human's contribution is front-loaded into system design rather than required at each cycle."

- **If H2:** "The autonomous loop improved on dimensions addressable by the agents' available tools (literature engagement, minor formalization) but plateaued on dimensions requiring judgment beyond the agents' specifications (strategic framing, experimental design beyond the pre-specified protocol). This suggests a boundary: certification infrastructure handles 'how to do X well,' but not 'what X should be.'"

All three outcomes are publishable. There is no losing result.
