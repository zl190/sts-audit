# Experiment Design: Research Program & Strategic Position

## 1. Inventory — What We've Done

### Completed Experiments

| # | Experiment | Question | Result | File |
|---|-----------|----------|--------|------|
| 1 | Gate Effectiveness | Do CLAUDE.md gates reduce issues? | 73% reduction, 100% critical elimination | `exp1_gate_effectiveness.md` |
| 5 | Paper Scoring | Does audit improve paper quality? | v1: 13/30 → v2: 26/30 (100% improvement) | `exp5_paper_scoring.md` |
| 6 | Version Trajectory | Is improvement monotonic across versions? | 3.0 → 3.3 → 3.5, issues 26 → 23 → 18 | `exp6_version_trajectory.md` |

### Completed Reviews

| Version | Score | Verdict | Issues | File |
|---------|:-----:|---------|:------:|------|
| v1 | 3.0 | Major Revision | 26 (4C, 17S, 5K) | `independent_review_v1.md` |
| v2 | 3.3 | R&R | 23 (3C, 16S, 4K) | `independent_review_v2.md` |
| v3 | 3.5 | R&R | 18 (3C, 11S, 4K) | `independent_review_v3.md` |

### Artifacts Produced

| Artifact | Purpose | File |
|----------|---------|------|
| Quality Gates (6) | Preventive — baked into AI context | `claude_quality_gates.md` |
| Audit Method (5-step) | Detective — post-generation review | `audit_method.md` |
| Autonomous Prompt Template | Delegation — background agent work | `autonomous_prompt_template.md` |
| Delegate Skill | Productized delegation framework | `~/claude-skills/delegate/SKILL.md` |
| Formalization Draft | SOTA synthesis + cost function | `formalization_draft.md` |
| Paper v1, v2 (reconstructed), v3 | Version trajectory as data | `paper/` |

---

## 2. Inventory — What We Have

### Data Assets

| Data | Description | Strength | Weakness |
|------|-------------|----------|----------|
| 3-version paper trajectory | v1→v2→v3 with independent blind scores | Monotonic improvement, same reviewer model | N=1 paper, same AI reviewer |
| 22-issue audit log | Full classification by gate, severity, before/after | Comprehensive, traceable | One paper, one auditor |
| Code case studies (3) | H-Tier vs Z-Tier with STS metrics | Controlled comparison, reproducible | 1 AI model, limited scope |
| Gate effectiveness data | 10 summaries, gated vs ungated | Clean A/B design | Same AI generates and audits |
| CC growth trajectory | CC=17→23 (H-Tier), CC=4→4 (Z-Tier service) | Directional evidence | N=1 change each |

### Tool Assets

| Tool | What It Does | Status |
|------|-------------|--------|
| `sts_checker.py` | Automated architecture audit (CC, LVD, CCR, TL) | Production-ready, CI-compatible |
| Quality gates | 6 CLAUDE.md-ready rules | Tested in Exp 1 |
| Audit method | 5-step adversarial review protocol | Applied to paper 3x |
| Delegate skill | Structured autonomous agent prompts | Pushed to GitHub |
| Independent reviewer prompt | Blind review calibrated to finance conference | Used 3x with consistent output |

### Theoretical Assets

| Component | Status | Gap |
|-----------|--------|-----|
| Credence → search conversion | Strong framing, well-cited | No formal equilibrium model |
| Incomplete → more complete contracts | Hart & Moore connection solid | No formal proof of welfare gain |
| Cobb-Douglas cost function | Specified in v3, testable predictions | β unestimated, no empirical validation |
| N* closed-form formula | Derived, illustrative calibration | Parameters assumed, not estimated |
| Bellman equation (optimal stopping) | Conceptual sketch in v3 | Unsolved — needs math econ co-author |
| Disclosure as governance | Jin & Leslie extension, compelling | N=1, "prompt compliance" alternative explanation |

---

## 3. What We Target

### Immediate: UCLA Anderson Conference (March 18 deadline)

**Requirements:**
- PDF of the paper
- Machine-readable version
- AI workflow description

**Current position:** v3 scores 3.5/5 (R&R). The conference reviews by AI agents and selects top 4 papers. We need to be in the top 4 out of however many submissions.

**What would push us from 3.5 to 4.0:**
1. Address the 3 critical v3 issues (causal language, "equilibrium" from N=1, "market simulation" framing)
2. Add the N* derivation (reviewer asked for it)
3. Run 30-repeat experiment (same prompt × 30 → distributional evidence)
4. Address the "information vs instruction" conflation (hardest — requires reframing)

**What we probably can't do by March 18:**
- Estimate β (needs maintenance cost dataset)
- Solve the Bellman equation (needs math econ)
- Multi-model experiments (GPT-4, Gemini, etc.)
- Longitudinal validation

### Medium-term: Follow-up Paper / Product

The framework generalizes beyond code and beyond this paper. The generalized thesis:

> Every AI output is a credence good. The user can't verify whether the AI's legal analysis is sound, its medical summary is complete, its code review caught the real issues. Structured disclosure with verifiable quality gates is the only known scalable solution.

This becomes either:
- A second paper: "Credence Good Governance for AI Output: A General Framework"
- A product: Quality gate infrastructure for AI-assisted work
- An open-source project: Domain-adaptable gate + audit toolkit

### Long-term: Research Program

The core research question: **How do you govern AI output in credence good markets?**

Sub-questions:
1. Which quality dimensions are universal vs domain-specific?
2. What is the decay curve of issues per audit round? Where is the asymptote?
3. Can gates transfer across domains?
4. What is the optimal number and specificity of gates?
5. How do you prevent Goodhart's Law from corrupting gate-based governance?
6. Does the framework work for human-AI teams, not just AI alone?

---

## 4. Experiment Designs — Agent Perspective

### Design Principles

When designing experiments that AI agents can run autonomously:

1. **Self-contained inputs:** Every file the agent needs must be specified with absolute paths
2. **Verifiable outputs:** Results go to files with defined structure — no conversational output
3. **Built-in validity checks:** The agent must acknowledge its own limitations (especially self-audit bias)
4. **Reproducible:** Another agent (or human) could re-run the same protocol
5. **File over conversation:** Everything persists even if the session dies

### Experiment 2: Inter-Rater Reliability (Priority: HIGH)

**Question:** Do independent AI reviewer agents agree on issue identification?

**Design:**
- Input: Paper v1 (known to have 22 issues)
- Agents: 3 independent Claude Opus instances + 1 Claude Sonnet + 1 Claude Haiku
- Each runs the same blind review protocol (identical prompt from independent_review template)
- Each writes to a separate output file

**Measures:**
- Issue overlap: How many issues are flagged by all 3+? By 2+? By 1 only?
- Severity agreement: When multiple agents flag the same issue, do they agree on severity?
- Dimension agreement: Do agents score the same dimensions similarly?
- Model variation: Do Sonnet and Haiku find different issues than Opus?

**Agent execution:**
```
/delegate batch \
  "Blind review v1 (Opus instance A)" | \
  "Blind review v1 (Opus instance B)" | \
  "Blind review v1 (Opus instance C)" | \
  "Blind review v1 (Sonnet)" | \
  "Blind review v1 (Haiku)"
```

**Analysis agent:** After all 5 complete, launch a synthesis agent to compute agreement metrics.

**Cost:** 5 parallel agents, ~$5-10 total. High value — addresses the "same reviewer model" validity threat in Exp 6.

**Why this matters:** If AI reviewers agree, the audit method is reproducible (satisfying Lizzeri's verifiability criterion). If they disagree, we learn which dimensions are subjective vs objective — itself useful data.

### Experiment 3: Compounding Effect (Priority: MEDIUM)

**Question:** Does the gate→audit→gate cycle reduce issues across rounds?

**Design:**
- Topic: "Summarize the economic implications of autonomous vehicles" (neutral, not our paper)
- Round 0: Generate 1000-word summary with NO gates. Audit. Record issues.
- Round 1: Add gates from Round 0 findings. Generate new summary, same topic. Audit. Record.
- Round 2-4: Repeat.
- Each generation and audit is an independent agent (no cross-contamination)

**Agent execution:** Sequential — each round depends on the previous round's audit results.
```
Round 0: /delegate experiment "generate summary, no gates" → audit
         Human extracts new gates from audit findings
Round 1: /delegate experiment "generate summary, with Round 0 gates" → audit
         ...
```

**Measures:**
- Issues per round (expect decreasing)
- Issues by severity per round (expect critical→0 fast, cosmetic→stable)
- Novel issues per round (issues not seen in prior rounds)
- Gate count vs issue count (is there a ratio?)

**Prediction:** Exponential decay to an asymptote. The asymptote represents issues that require domain expertise beyond what gates can encode.

### Experiment 7: Multi-Model Code Quality (Priority: HIGH for paper)

**Question:** Is the credence good dynamic specific to Claude, or does it generalize?

**Design:**
- Same prompt from Case 2 ("Write a simple checkout system with membership discounts")
- Run on: Claude Opus, Claude Sonnet, Claude Haiku, GPT-4o, Gemini Pro
- Each produces code, each is audited by `sts_checker.py`
- Repeat 5x per model for distributional evidence

**Agent execution:**
- Claude variants: Use Task tool with model parameter
- Other models: Requires API access or manual runs

**Measures:**
- STS tier distribution per model
- CC, LVD, CCR distributions per model
- Does the "zero guidance → H-TIER" pattern hold across models?

**Why this matters:** The v1 reviewer's C4 ("N=2 experiments with one AI model insufficient for generalized claims") and the v3 reviewer's Q1 ("How do you distinguish information asymmetry from vague prompting?") both point here. Multi-model evidence would be the single strongest addition to the paper.

### Experiment 8: Prompt Ablation (Priority: HIGH for paper)

**Question:** Is it disclosure (knowing metrics exist) or instruction (being told what to do) that drives the quality improvement?

**Design — 4 conditions:**

| Condition | Prompt | Prediction |
|-----------|--------|------------|
| A: Baseline | "Write a checkout system" | H-TIER (confirmed in Case 2) |
| B: Quality-aware | "Write a checkout system. Note: code will be audited for architectural quality using CC, LVD, and CCR metrics." | If disclosure matters → Z-TIER. If only instruction matters → H-TIER |
| C: Instructed | "Write a checkout system using Strategy pattern with separate service and view layers." | Z-TIER (confirmed in Case 1) |
| D: Both | "Write a checkout system. It will be audited for CC, LVD, CCR. Use appropriate patterns." | Z-TIER |

**The critical comparison is B vs A.** If B produces better architecture than A, then *mere awareness of audit criteria* (disclosure) improves quality, even without explicit instructions. This directly addresses the "prompt compliance vs governance" challenge raised by all three reviewers.

**Agent execution:**
```
/delegate batch \
  "Generate checkout: baseline" | \
  "Generate checkout: quality-aware" | \
  "Generate checkout: instructed" | \
  "Generate checkout: both"
```
Repeat 5x each → 20 code artifacts → audit all with sts_checker.py.

**Why this matters:** This is the experiment the paper needs most. It cleanly separates the disclosure mechanism from the instruction mechanism. If Condition B (disclosure only) produces better code than Condition A (no disclosure), the "governance through context" claim stands. If B ≈ A but C > A, then it's just prompt engineering.

### Experiment 9: 30-Run Distribution (Priority: MEDIUM)

**Question:** Is the CC divergence between H-TIER and Z-TIER robust or an artifact of single runs?

**Design:**
- Same Case 1 prompt, 30 repetitions each condition
- Condition A: No quality spec (expect H-TIER distribution)
- Condition B: With quality spec (expect Z-TIER distribution)
- Audit all 60 artifacts with sts_checker.py

**Measures:**
- CC distribution per condition (mean, SD, range)
- LVD distribution per condition
- Tier assignment frequency
- Statistical test: t-test or Mann-Whitney on CC between conditions

**Why this matters:** Moves from "Case 1 showed CC=17 vs CC=4" to "Mean CC under no spec = X ± Y vs mean CC under spec = A ± B, p < 0.001." This is the statistical backbone the paper lacks.

---

## 5. Priority Matrix — What to Run Before March 18

| Experiment | Impact on Paper Score | Effort | Priority |
|-----------|:--------------------:|:------:|:--------:|
| 8: Prompt Ablation | +++ (addresses core reviewer concern) | Medium | **DO FIRST** |
| 7: Multi-Model | ++ (addresses generalizability) | Medium-High | **DO SECOND** |
| 9: 30-Run Distribution | ++ (statistical backbone) | Medium | **DO THIRD** |
| 2: Inter-Rater Reliability | + (methodology credibility) | Low | Nice-to-have |
| 3: Compounding Effect | + (framework validation) | High | Post-conference |
| 4: Cross-Domain Transfer | + (generalizability) | High | Follow-up paper |

**Realistic target for March 18:** Experiments 8 and 9 (prompt ablation + 30-run distribution). Both are agent-executable, both directly address reviewer concerns, and both produce the kind of quantitative evidence the paper currently lacks.

**If time permits:** Experiment 7 (multi-model) for Claude variants only (Opus, Sonnet, Haiku — no external API needed).

---

## 6. The Bigger Picture — Why This Matters

### The Credence Good Trap in AI Adoption

Every AI output is a credence good. The core dynamic:

```
User can't verify AI output quality
    → Can't distinguish good output from bad
        → Can't pay more for quality
            → No incentive for AI providers to invest in quality
                → Average quality degrades
                    → Trust erodes
                        → Adoption stalls or produces harm
```

This is not speculative — it's happening:

- **AI-generated legal briefs** with fabricated citations (Mata v. Avianca, 2023)
- **AI-generated medical advice** with plausible but wrong recommendations
- **AI-generated code** that passes tests but is architecturally fragile
- **AI-generated research** with decorative citations and overclaims (this paper's v1)

In every case, the output *looked right* to the user. The quality was unverifiable. The failure was a credence good failure.

### Why AI Companies Should Care

The companies deploying AI face a choice they may not realize they're making:

**Without quality governance:** AI output quality is a credence good within their own organization. The engineering team can't verify whether the AI's code suggestions are architecturally sound. The legal team can't verify whether the AI's contract review caught the real risks. The strategy team can't verify whether the AI's market analysis is rigorous or superficial.

Every AI-assisted decision becomes a credence good decision. The organization can't tell whether it's getting good AI output or bad AI output. It optimizes for what it can observe (speed, volume, superficial coherence) while neglecting what it can't (rigor, architectural quality, factual accuracy).

This is the lemons spiral operating *inside the company*.

**With quality governance:** Structured quality gates + adversarial audit creates the internal equivalent of certification. The organization can verify AI output quality on defined dimensions. Bad output is caught before it ships. The AI's optimization target shifts from "looks good" to "is good" on measurable criteria.

### The Skill Set This Builds

Working on this project — whether it gets published or not — builds a skill set that is becoming essential:

1. **Credence good awareness:** Recognizing when you can't verify what you're consuming. This is the meta-skill — once you see the pattern, you see it everywhere.

2. **Gate design:** Writing quality criteria that shift AI behavior. This is prompt engineering, but principled — not "add more detail to the prompt" but "what specific failure modes does this gate prevent?"

3. **Adversarial audit:** Systematically finding failure modes in AI output. Not "does this look right?" but "on which specific dimensions does this fail, and how severely?"

4. **Autonomous delegation:** Structuring work so AI agents can run independently with built-in quality controls. The 5-component framework (context, deliverable, constraints, honesty, anti-patterns) is a reusable skill.

5. **Meta-cognition about AI:** Understanding that the AI's optimization target is set by its context, not its capability. The same AI produces radically different quality under different constraints. The constraint is the lever.

### Where This Goes

Three possible futures, not mutually exclusive:

**Academic track:** This becomes a research program in AI governance. The paper lands at UCLA Anderson, gets refined with a co-author, and becomes a working paper series. The formal model gets solved. The experiments get scaled. The framework gets cited.

**Product track:** The gate + audit framework becomes a tool. Companies deploy it as part of their AI governance stack. "Quality gates for AI output" becomes a product category. The STS checker is the code-domain implementation; equivalents get built for legal, medical, financial AI output.

**Practice track:** None of this gets published or productized, but the person who built it has a skill set that is increasingly rare and increasingly valuable. They can look at any AI output and immediately identify: What are the credence dimensions here? What can the user verify? What can't they verify? What quality gates would shift the optimization target? How would you audit this?

That skill set is worth more than any single paper.

### The Meta-Observation

This entire research project — from code experiments to paper writing to overnight agent runs to this very document — is itself a demonstration of the framework. Every artifact was AI-generated with human direction. The quality depended entirely on the constraints provided.

The overnight agent runs (Experiments 1, 5, 6) produced useful output because they had structured prompts with all 5 components. The paper improved from 3.0 to 3.5 because structured audit criteria were applied. The code cases diverged because one had quality specs and the other didn't.

The constraint, not the capability, determines the quality. This is the thesis. This project is the evidence. And the skill of applying the right constraints to AI output is the practical takeaway.

No matter where this goes — conference, journal, product, or just personal growth — the awareness is the asset.
