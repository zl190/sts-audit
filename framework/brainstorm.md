# Systematic Brainstorm: Framework + Paper Interaction

## Part 1: The Two Things

### A. Quality Gates (CLAUDE.md approach)
**What it is:** Preventive rules baked into the AI's operating instructions. The AI reads them before generating output and adjusts behavior accordingly.

**Mechanism:** Disclosure-as-governance, applied to the production environment itself. The gates don't enforce anything — they shift the AI's optimization target by making quality dimensions explicit in the context. Same mechanism as Case 2 in the paper (mall system: AI self-corrected when exposed to audit criteria).

**Strengths:**
- Zero marginal cost — once written, applies to all future output
- Compounds over time — new gates from each audit cycle
- Testable — can compare output quality with/without gates
- Immediately usable — no infrastructure needed

**Weaknesses:**
- Context window is finite — can't have 500 gates
- Goodhart risk — AI might satisfy letter but not spirit (same as code metric gaming)
- No enforcement — relies on AI's context-sensitivity, not verification
- Unknown coverage — which failure modes do gates miss?

### B. Audit Method (prompt framework)
**What it is:** Post-generation adversarial review. Human (or AI-as-reviewer) applies structured criteria to completed output and flags issues by severity.

**Mechanism:** Traditional quality inspection, structured by credence good theory. Instead of "does this look good?" it asks "on which specific quality dimensions does this fail?"

**Strengths:**
- Catches what gates miss — gates are preventive, audit is detective
- Produces evidence — before/after documentation is experimental data
- Domain-adaptable — same 5-step method works for code, writing, analysis
- Reveals patterns — systematic issues become new gates

**Weaknesses:**
- Costs time — manual adversarial reading is slow
- Requires expertise — you need to know what "wrong" looks like
- One-shot — only catches issues in the specific output audited
- Subjectivity — different auditors may flag different issues

---

## Part 2: How They Impact Each Other

### Gates → Audit (preventive reduces detective load)
- Good gates reduce the number of issues the audit finds
- The audit becomes faster because fewer problems exist
- Remaining issues are subtler — the "easy" failures are prevented
- Risk: gates create false confidence ("I have gates, no need to audit")

### Audit → Gates (detective improves preventive)
- Every audit finding is a candidate for a new gate
- Patterns across multiple audits reveal the highest-value gates
- Gates that don't reduce audit findings can be dropped (ineffective)
- This is the feedback loop: audit → pattern → gate → audit → fewer issues → new patterns → new gates

### The Compounding Cycle
```
Round 0: No gates. Audit finds 22 issues.
Round 1: 6 gates from Round 0 patterns. Audit finds ??? issues.
Round 2: Updated gates from Round 1. Audit finds ??? issues.
...
Round N: Diminishing returns. Remaining issues are novel or require domain expertise gates can't encode.
```

**The key hypothesis:** Issue count decreases per round, following a decay curve. The asymptote is the floor of issues that require human domain expertise. This is testable.

### Cross-Domain Transfer
- Gates learned from writing audit may prevent code issues (and vice versa)
- Example: Gate 3 (Claim Scope) in writing ≈ over-engineering in code (building for hypothetical requirements)
- Example: Gate 6 (Data Integrity) in writing ≈ hardcoded values / magic numbers in code
- Hypothesis: some quality dimensions are universal across domains, others are domain-specific

---

## Part 3: Experiments We Should Run

### Experiment 1: Gate Effectiveness (immediate, cheap)
**Question:** Do CLAUDE.md quality gates reduce issue count in AI-generated writing?

**Design:**
- Task: Generate 10 short research summaries on the same topic
- Condition A: No gates (baseline). 5 summaries.
- Condition B: Full gate set from `claude_quality_gates.md`. 5 summaries.
- Measure: Blind adversarial audit on all 10. Count issues by severity and dimension.
- Predict: Condition B has fewer issues, especially on dimensions with explicit gates.

**Cost:** Low. One afternoon. Produces quantitative evidence.

### Experiment 2: Audit Method Reliability (important for credibility)
**Question:** Is the adversarial audit method reliable across auditors?

**Design:**
- Take the STS paper v1 (pre-audit) as input
- Have 3 independent auditors (human or AI instances) run the audit method
- Measure: Inter-rater agreement on issue identification and severity
- Predict: High agreement on critical issues, lower on cosmetic

**Cost:** Medium. Need multiple auditors. Key for publishability — if auditors disagree, the method isn't reproducible.

### Experiment 3: Compounding Effect (the core claim)
**Question:** Does the gate → audit → gate cycle reduce issues over multiple rounds?

**Design:**
- Round 0: Generate document with no gates. Audit. Record issue count.
- Round 1: Add gates from Round 0 findings. Generate new document on same topic. Audit. Record.
- Round 2: Update gates. Generate. Audit. Record.
- Repeat for 4-5 rounds.
- Measure: Issue count per round, by severity. Plot the decay curve.
- Predict: Decreasing issue count with diminishing returns.

**Cost:** Medium-high. Multiple generation + audit cycles. But produces the strongest evidence.

### Experiment 4: Cross-Domain Transfer (ambitious)
**Question:** Do quality gates learned in one domain (writing) transfer to another (code)?

**Design:**
- Learn gates from writing audit (already done)
- Translate gates to code domain (e.g., "causal language" → "comments that overclaim what the code does")
- Apply translated gates to AI code generation
- Measure: STS audit results with/without transferred gates
- Predict: Some transfer (universal dimensions), some not (domain-specific)

**Cost:** High. Needs careful gate translation. But proves generalizability.

### Experiment 5: The Live Paper Experiment (already happening)
**Question:** Does the paper's own revision history demonstrate the framework?

**Design:**
- v1 of the paper = "unconstrained AI output" (the H-Tier equivalent)
- Adversarial audit = "certification instrument"
- v2 of the paper = "output after disclosure/governance"
- The changelog (22 issues, severities, categories, fixes) = experimental data

**Evidence already collected:**
- 3 critical, 15 substantive, 4 cosmetic issues found
- All fixed in v2
- Patterns mapped to 6 quality gate categories
- Gates codified in `claude_quality_gates.md`

**What's missing:** A formal before/after comparison. We could:
- Run both v1 and v2 past an independent AI reviewer (or multiple)
- Score on the 6 quality dimensions
- Show the quantitative improvement

**Cost:** Low. We already have v1 and v2. Just need the scoring pass.

### Priority Order
1. **Experiment 5** — essentially free, already have the data, strongest meta-narrative
2. **Experiment 1** — cheap, fast, produces clean quantitative result
3. **Experiment 2** — necessary for methodological credibility
4. **Experiment 3** — the core claim, do after 1 and 2 validate components
5. **Experiment 4** — ambitious, save for follow-up paper

---

## Part 4: The Paper as Live Experiment

### Why this matters
The paper's revision history is not just documentation — it's DATA. The v1→v2 transition is a controlled experiment:

- **Treatment:** Structured adversarial audit with explicit quality dimensions
- **Subject:** AI-generated research paper
- **Control:** v1 (no audit criteria applied)
- **Outcome:** v2 (all identified issues resolved)

This is the writing equivalent of the bookstore experiment:
| | Code (Case 1) | Writing (Paper itself) |
|---|---|---|
| Unconstrained output | H-Tier (CC=17, LVD=0.20) | v1 (22 issues: overclaims, decorative cites, tautologies) |
| Quality criteria applied | Z-Tier (CC=4, LVD=0.00) | v2 (issues resolved, honest caveats added) |
| Mechanism | STS audit → binary certification | Adversarial audit → structured fix list |
| Generalization | Tool-automatable for code | Human-driven but structurable for writing |

### The stronger-than-code argument
Code quality is EASIER to certify — you can automate the check. Writing quality is HARDER — it requires judgment. If structured criteria improve the harder case, the principle is robust. The code case is just the automatable special case of a general principle.

### What this means for the paper
The paper can make a stronger meta-claim: "This paper's own revision history demonstrates the framework operating on a domain (research writing) that is strictly harder to certify than code." This belongs in Appendix A (AI Workflow), which already has the meta-observation. It could be strengthened with the specific numbers (22 issues, category breakdown, before/after).

---

## Part 5: Filling the Formal Gaps (Can Claude Do It?)

### What's missing
1. **Maintenance cost function $C(Q_a, \Delta)$** — stated to be "convex decreasing in $Q_a$" but never formalized
2. **Rewrite threshold prediction** — the inequality $\sum C_{maintain} > C_{replace}$ is tautological
3. **Welfare analysis** — no formal deadweight loss calculation for the pooling equilibrium

### Approach: Read SOTA, then formalize
Papers to study:
- **Banker, Datar & Kemerer (1996)** — already cited, has the economic model for software replacement timing
- **Cai et al. (2021)** — architectural technical debt and developer productivity (25% cost estimate)
- **Tsoukalas et al. (2020)** — technical debt forecasting with time-series models
- **Ajibode et al. (2024)** — systematic review of TD forecasting (646 papers)
- **Lizzeri (1999)** — certification intermediary model (for welfare analysis)
- **Dulleck & Kerschbamer (2006)** — credence goods formal model (for proper application)

### What Claude can realistically do
- Read and synthesize these papers' formal models
- Attempt to specialize them to the software architecture domain
- Apply Gate 5 (Formalism Honesty) to self-audit: is the model non-trivial? Are parameters estimable?
- Produce a draft formalization that's honest about its limitations

### What still might need a co-author
- Proving the model has a unique equilibrium (or characterizing multiple equilibria)
- Connecting to established results in mechanism design
- The "is this novel?" judgment — Claude can check against literature, but can't attend seminars and know what the field considers interesting
- Institutional credibility — a formal model reviewed by an information economist carries more weight

### Proposed process
1. Claude reads the key papers above (web fetch or user provides)
2. Claude attempts formalization with full quality gates active
3. Adversarial self-audit against Gate 5
4. User reviews
5. If gaps remain → co-author fills them. If sufficient → co-author validates.
6. Either way, the attempt is more evidence for the framework (meta-experiment continues)
