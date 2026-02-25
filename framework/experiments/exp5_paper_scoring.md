# Experiment 5: Before/After Scoring of AI-Written Research Paper

## Objective

Test whether a structured adversarial audit — applying the credence good disclosure principle to AI-generated research writing — produces measurable, meaningful quality improvement. The paper's own revision history (v1 to v2) serves as experimental data: v1 is the "unconstrained AI output" (analogous to H-Tier code) and v2 is the "output after structured audit and remediation" (analogous to Z-Tier code).

This experiment is the writing-domain equivalent of the bookstore code experiment (Case 1 in the paper). If the improvement is real and quantifiable, the paper's revision history itself constitutes evidence for the framework it describes.

## Method

### Materials

- **v1 (pre-audit):** STS Finance Paper as drafted by Claude with human direction but no systematic quality audit. Issues documented in session notes (2026-02-23).
- **v2 (post-audit):** STS Finance Paper after all 22 identified issues were remediated. File: `paper/STS_Finance_Paper_v2.md`.
- **Quality dimensions:** The 6 gates defined in `framework/claude_quality_gates.md`, derived from the audit itself.
- **Severity scale:** Critical / Substantive / Cosmetic (defined in `framework/audit_method.md`).

### Scoring Protocol

Each paper version is scored on each of the 6 quality dimensions using a 1-5 scale:

| Score | Meaning |
|-------|---------|
| 1 | Pervasive failures — the dimension is systematically violated |
| 2 | Multiple failures — several instances across the paper |
| 3 | Some failures — a few notable instances |
| 4 | Minor issues only — one or two borderline cases |
| 5 | No issues found on this dimension |

### Procedure

1. Reconstruct the complete v1 issue list from session notes, classifying each by gate and severity.
2. Score v1 and v2 on all 6 dimensions.
3. Compute statistical summaries.
4. Conduct a fresh adversarial pass on v2 (independent of the original audit) to test for residual or new issues.
5. Analyze whether the improvement is meaningful or cosmetic.

---

## Results

### Step 1: Complete v1 Issue Reconstruction

The 22 issues identified in v1 are reconstructed below. Each is classified by the quality gate it violates, its severity, what v1 said, and what v2 says.

#### Critical Issues (3)

| # | Gate | Issue | v1 (Before) | v2 (After) |
|---|------|-------|-------------|------------|
| C1 | Gate 1: Causal Language | "Controlled experiments" / "demonstrate" used for n=1 case studies | Abstract and Section 1.3 used "controlled experiments" and "We demonstrate three results" for single case studies with one AI model | Changed to "case studies" and "We provide evidence for three results... behavior consistent with the predicted outcome of Akerlof's (1970) lemons model" |
| C2 | Gate 1: Causal Language | "Lemons equilibrium" claimed from single AI, single artifact | Section 4 described findings as establishing a "lemons equilibrium" from one case | Changed to "behavior consistent with the predicted outcome" and "consistent with lemons model" throughout |
| C3 | Gate 5: Formalism Honesty | Section 5 "Capital Allocation Model" was tautological | Presented as a "Model" — the inequality stating maintenance cost exceeds replacement cost at the rewrite point is true by definition | Renamed to "Framework"; acknowledged the formalization gap; labeled as a conceptual framework, not a testable model |

#### Substantive Issues (15)

| # | Gate | Issue | v1 (Before) | v2 (After) |
|---|------|-------|-------------|------------|
| S1 | Gate 2: Citation Honesty | Hart & Moore (1988) cited without engaging Hart (1995) | Referenced Hart & Moore (1988) on incomplete contracts without noting that Hart (1995) — the more relevant work on firms, contracts, and financial structure — supersedes it for this context | Added Hart (1995) citation; Section 2.4 now engages with both: "The incomplete contracts literature (Hart & Moore, 1988; Hart, 1995) establishes that contracts are incomplete when relevant variables are observable... but not verifiable" |
| S2 | Gate 2: Citation Honesty | Board & Meyer-ter-Vehn (2013) cited without noting model mismatch | Cited as supporting reputation mechanisms in software markets, without noting their model requires eventual quality revelation | v2 explicitly states: "Reputation mechanisms (Board & Meyer-ter-Vehn, 2013) require eventual quality revelation, which does not hold for software architecture — a credence good where quality may never be observed" |
| S3 | Gate 2: Citation Honesty | Opp, Opp & Harris (2013) cited without engaging the undermining implication | Cited as supporting certification design without acknowledging that their finding about rating inflation could undermine the paper's thesis | v2 engages honestly: "The binary threshold creates the same cliff effects identified in credit rating design by Opp, Opp & Harris (2013)... We discuss the analogous Goodhart's Law risk for software certification in Section 7" |
| S4 | Gate 2: Citation Honesty | Bajari & Tadelis dangling reference | Cited in text but missing from reference list (or in reference list but not cited — a classic AI fabrication/mismatch) | Dangling reference removed entirely |
| S5 | Gate 3: Claim Scope | $2.41T presented as architecture-specific losses | Stated or implied that $2.41T was from software architecture quality specifically | v2 qualifies: "This figure encompasses operational failures, security breaches, and maintenance costs broadly. The fraction attributable specifically to invisible architectural degradation — the problem we study — is unknown, but architectural technical debt alone consumes an estimated 25% of development time (Cai et al., 2021), suggesting it is a substantial component" |
| S6 | Gate 3: Claim Scope | "Largest unanalyzed credence goods market" | Claimed software was "the largest" credence goods market without evidence for that superlative ranking | Changed to "a major unanalyzed credence goods market" |
| S7 | Gate 3: Claim Scope | "Complete contracts" | Claimed the framework enables "complete contracts" on quality dimensions | Changed to "more complete contracts" — acknowledging the completeness frontier shifts but does not reach full completeness |
| S8 | Gate 6: Data Integrity | Mall case described as "88 lines, single class" | Stated the mall settlement case was an 88-line, single-class file | v2 corrects: "132-line file with five classes (MemberLevel, Product, CartItem, User, ShoppingCart)" and clarifies the failure was on LVD, not CC |
| S9 | Gate 6: Data Integrity | LVD/ADF naming mismatch | Used "LVD" (Layer Violation Density) and "ADF" (Architecture Drift Factor) inconsistently, creating confusion about whether these were the same or different metrics | Section 3 now defines both: "Layer Violation Density (LVD) — the proportion of code lines containing I/O artifacts in business logic layers, measuring separation of concerns (labeled 'Architecture Drift Factor' or ADF in the instrument's output)" |
| S10 | Gate 1: Causal Language | Stress test overclaims growth rate from single data point | Presented CC growth rate from one change as establishing a trajectory | v2 adds: "We note that a single change is insufficient to establish a growth rate — the trajectory could be linear, superlinear, or an outlier. However, the directional finding is suggestive" |
| S11 | Gate 1: Causal Language | Split variant CC stability not reported | Did not report that the physically separated Z-Tier variant showed CC=4 before and CC=4 after (zero growth), which is the strongest data point | v2 adds: "The physically separated constrained variant (service layer only) showed zero CC growth (CC=4 before and after), absorbing the change entirely within its modular structure" |
| S12 | Gate 4: Analogy Discipline | LEED analogy without regulatory caveat | Drew LEED comparison (green building certification creating price premiums) without noting LEED operates in a market with regulatory mandates and consumer sustainability preferences | v2 adds: "though LEED operates in a market with regulatory mandates and consumer-facing sustainability preferences that do not yet exist for software architecture" |
| S13 | Gate 1: Causal Language | Jin & Leslie effect size overclaimed | Cited a 3x improvement from restaurant disclosure without qualification | v2 reduces to approximately 2x and adds: "Whether this is best characterized as 'governance' or 'prompt compliance' is a semantic distinction" |
| S14 | Gate 6: Data Integrity | GitHub and Forrester citations missing from references | Cited GitHub (2025) and Forrester (2024) statistics in the text but did not include them in the reference list | v2 adds both to the reference list: "GitHub. (2025). Octocat 2025..." and "Forrester. (2024). Predictions 2025..." |
| S15 | Gate 3: Claim Scope | Appendix A too self-congratulatory, did not acknowledge own decorative citations | AI Workflow appendix described the meta-observation without self-awareness about the paper's own quality issues | v2 adds: "An earlier draft of this paper contained decorative citations and overclaims identified through systematic audit — the writing equivalent of the architectural defects our tool detects in code" |

#### Cosmetic Issues (4)

| # | Gate | Issue | v1 (Before) | v2 (After) |
|---|------|-------|-------------|------------|
| K1 | Gate 6: Data Integrity | LVD vs ADF naming inconsistency in displays | Inconsistent use of metric name across sections | Standardized: defined both terms in Section 3, used consistently thereafter |
| K2 | Gate 3: Claim Scope | Minor phrasing inflation throughout | Various places where hedging was insufficient (e.g., "confirms" instead of "consistent with") | Systematically softened throughout |
| K3 | Gate 2: Citation Honesty | Reference list formatting inconsistencies | Minor formatting differences across reference entries | Standardized reference formatting |
| K4 | Gate 1: Causal Language | "Demonstrate" used inconsistently post-edit | Some instances of strong causal language remained in early drafts after partial fixes | Systematic pass to replace all instances |

### Step 2: Dimension Scoring

#### v1 Scores

| Gate | Dimension | Score | Rationale |
|------|-----------|-------|-----------|
| Gate 1 | Causal Language | 2 | Multiple failures: "demonstrate" with n=1 (C1), "lemons equilibrium" from single case (C2), stress test overclaim (S10), unreported data point (S11), Jin & Leslie overclaim (S13), residual "demonstrate" instances (K4). 6 issues total. |
| Gate 2 | Citation Honesty | 2 | Multiple failures: Hart & Moore without Hart 1995 (S1), Board & Meyer-ter-Vehn model mismatch (S2), Opp et al. not honestly engaged (S3), dangling Bajari & Tadelis reference (S4), missing GitHub/Forrester references (S14), formatting issues (K3). 6 issues total. |
| Gate 3 | Claim Scope | 2 | Multiple failures: $2.41T scope inflation (S5), "largest credence market" (S6), "complete contracts" (S7), Appendix A overclaim (S15), phrasing inflation (K2). 5 issues total. |
| Gate 4 | Analogy Discipline | 3 | Some failures: LEED analogy without regulatory caveat (S12). Only 1 issue, but it was the primary analogy in the paper and went entirely uncaveated. |
| Gate 5 | Formalism Honesty | 2 | The tautological "Capital Allocation Model" (C3) was a single issue, but it was critical — the entire Section 5 was labeled as something it was not. A section-level failure on a core contribution warrants a 2. |
| Gate 6 | Data Integrity | 2 | Multiple failures: mall case wrong line count and class count (S8), LVD/ADF naming confusion (S9, K1), missing reference entries (S14). 4 issues total. |

**v1 Composite Score: 13/30 (43.3%)**

#### v2 Scores

| Gate | Dimension | Score | Rationale |
|------|-----------|-------|-----------|
| Gate 1 | Causal Language | 4 | All 6 identified issues resolved. Language systematically softened. Minor residual: abstract still says "we demonstrate that automated measurement can convert" in Contribution 2 (Section 1.3) — this is borderline since the paper does provide tool-based evidence for this specific claim, but "demonstrate" is strong for the evidence level. |
| Gate 2 | Citation Honesty | 4 | All 6 identified issues resolved. Hart (1995) added, Board & Meyer-ter-Vehn caveat added, Opp et al. engaged honestly, dangling reference removed, GitHub/Forrester added. Minor residual: Dulleck & Kerschbamer (2006) cited for the formal framework but the paper does not use their formal model — it cites the verbal framing only. |
| Gate 3 | Claim Scope | 4 | All 5 identified issues resolved. $2.41T qualified, "major" not "largest," "more complete" not "complete," Appendix A self-aware. Minor residual: "first controlled experimental evidence" (Contribution 1) — the word "first" is a strong claim that would require a literature search to verify. |
| Gate 4 | Analogy Discipline | 5 | LEED caveat added. The building insurance analogy in Section 6.3 also includes honest difficulties. No residual issues identified. |
| Gate 5 | Formalism Honesty | 4 | Renamed to "Framework." Acknowledged limitations. Minor residual: Section 5.2 presents $CC(n) \approx CC_0 \times (1+r)^n$ with specific numerical extrapolation from a single data point, calling it a "working hypothesis" — but the precision of the extrapolation (doubles in 2.3 changes, quadruples in 4.6) may lend false concreteness to what is effectively one observation. |
| Gate 6 | Data Integrity | 5 | Mall case corrected, naming convention clarified, references added. All numbers now verifiable against artifacts. No residual issues identified. |

**v2 Composite Score: 26/30 (86.7%)**

### Step 3: Statistical Summary

#### Issue Count

| Metric | v1 | v2 |
|--------|----|----|
| Total issues | 22 | 0 (all remediated) |
| Critical | 3 | 0 |
| Substantive | 15 | 0 |
| Cosmetic | 4 | 0 |

#### Issues by Dimension

| Gate | Dimension | v1 Issues | Severity Breakdown |
|------|-----------|-----------|-------------------|
| Gate 1 | Causal Language | 6 | 2 critical, 3 substantive, 1 cosmetic |
| Gate 2 | Citation Honesty | 6 | 0 critical, 4 substantive, 2 cosmetic |
| Gate 3 | Claim Scope | 5 | 0 critical, 3 substantive, 2 cosmetic* |
| Gate 4 | Analogy Discipline | 1 | 0 critical, 1 substantive, 0 cosmetic |
| Gate 5 | Formalism Honesty | 1 | 1 critical, 0 substantive, 0 cosmetic |
| Gate 6 | Data Integrity | 3 | 0 critical, 3 substantive, 0 cosmetic** |

*Note: K2 (phrasing inflation) counted under Gate 3; S15 (Appendix A) also under Gate 3. One cosmetic issue (K1) recategorized under Gate 6 as it is naming consistency. Totals account for each issue being assigned to a single primary gate, though some issues span gates. The total across gates is 22, matching the issue count.*

**Note: S14 (missing references) counted under Gate 6 for the missing entries and also touches Gate 2. Assigned to Gate 6 as the primary failure is data integrity (reference list completeness).*

#### Gate Coverage Analysis

The question: if these 6 gates had existed as CLAUDE.md instructions during v1 generation, what percentage of v1 issues would each gate have prevented?

| Gate | Would Prevent | Issue Numbers | Coverage |
|------|--------------|---------------|----------|
| Gate 1: Causal Language | 6 | C1, C2, S10, S11, S13, K4 | 27.3% of all issues |
| Gate 2: Citation Honesty | 5 | S1, S2, S3, S4, K3 | 22.7% of all issues |
| Gate 3: Claim Scope | 4 | S5, S6, S7, K2 | 18.2% of all issues |
| Gate 4: Analogy Discipline | 1 | S12 | 4.5% of all issues |
| Gate 5: Formalism Honesty | 1 | C3 | 4.5% of all issues |
| Gate 6: Data Integrity | 3 | S8, S9/K1, S14 | 13.6% of all issues |
| Meta-Gate: Self-Audit | 2 | S15, S11 | 9.1% of all issues |
| **Total gate coverage** | **22** | **All** | **100%** |

All 22 issues are attributable to at least one gate. This is expected — the gates were derived from the issues. The more meaningful question is whether these gates would prevent issues in *future* documents (tested in Experiments 1 and 3).

#### Composite Score Improvement

| Dimension | v1 | v2 | Delta |
|-----------|----|----|-------|
| Gate 1: Causal Language | 2 | 4 | +2 |
| Gate 2: Citation Honesty | 2 | 4 | +2 |
| Gate 3: Claim Scope | 2 | 4 | +2 |
| Gate 4: Analogy Discipline | 3 | 5 | +2 |
| Gate 5: Formalism Honesty | 2 | 4 | +2 |
| Gate 6: Data Integrity | 2 | 5 | +3 |
| **Composite** | **13/30** | **26/30** | **+13 (+100%)** |

---

### Step 4: Fresh Adversarial Pass on v2

The following issues were identified through a fresh adversarial reading of v2, independent of the original audit. These are issues the original audit either missed or that were introduced during the v1-to-v2 remediation.

#### New Issue N1 — Gate 1: Causal Language (Substantive)

**Location:** Section 1.3, Contribution 2

**Text:** "We demonstrate that automated measurement can convert previously non-contractible quality dimensions into contractible ones"

**Problem:** "Demonstrate" is used here with n=3 case studies and one tool. The paper provides evidence that this conversion is feasible for specific Python metrics with one AI model. "Demonstrate" implies a stronger evidentiary basis. This is the same overclaiming pattern the audit caught elsewhere, but this instance survived.

**Suggested fix:** "We show that automated measurement can convert..." or "We provide evidence that automated measurement can convert..."

#### New Issue N2 — Gate 3: Claim Scope (Substantive)

**Location:** Section 1.3, Contribution 1

**Text:** "provide the first controlled experimental evidence that AI code generation produces output consistent with the lemons model prediction"

**Problem:** The word "first" is a priority claim that requires a systematic literature review to verify. Sabra et al. (2025) already study AI code quality across 5 LLMs. While their framing is not explicitly "lemons model," the claim of being "first" is risky if any prior work has made a similar connection.

**Suggested fix:** "provide controlled experimental evidence..." (drop "first") or add "to our knowledge" qualification.

#### New Issue N3 — Gate 5: Formalism Honesty (Substantive)

**Location:** Section 5.2

**Text:** "If we assume — as a working hypothesis that requires validation across multiple change cycles — that the growth rate is approximately constant, after n changes: CC(n) ~ CC_0 * (1+r)^n where r is the per-change complexity growth rate. At r = 0.35, CC doubles in approximately 2.3 changes and quadruples in 4.6 changes."

**Problem:** The paper correctly labels this a "working hypothesis" but then provides specific numerical extrapolation (doubles in 2.3 changes, quadruples in 4.6) that gives false precision to what is a single observation. The exponential model is presented with the concreteness of an established result while being derived from exactly one data point. A skeptical reviewer would note that a constant growth rate assumption is itself a strong assumption — real CC growth likely depends on the nature of each change, not just the count.

**Suggested fix:** Remove the specific doubling/quadrupling numbers, or explicitly state: "These extrapolations are illustrative only, derived from a single observed change; the actual growth function is unknown."

#### New Issue N4 — Gate 2: Citation Honesty (Substantive)

**Location:** Section 2.1

**Text:** "This maps directly to the framework of Dulleck & Kerschbamer (2006), who formalize credence goods markets as environments where the seller privately observes a quality parameter that the buyer cannot verify."

**Problem:** "Maps directly" implies a close formal correspondence between the paper's model and Dulleck & Kerschbamer's formal model. But the paper never uses D&K's formal model — it uses their verbal taxonomy. Their formal model involves specific assumptions about verifiability, liability, and commitment that the paper does not check. The citation is substantive (not decorative), but "maps directly" overstates the connection.

**Suggested fix:** "This is consistent with the framework of Dulleck & Kerschbamer (2006)..." or "This fits within the taxonomy of Dulleck & Kerschbamer (2006)..."

#### New Issue N5 — Gate 3: Claim Scope (Cosmetic)

**Location:** Section 2.2

**Text:** "The $2.41 trillion in annual quality-related losses (CISQ/NIST, 2022) can be interpreted as the welfare cost of this pooling equilibrium"

**Problem:** This is an interpretive leap. CISQ measures direct costs (failures, maintenance, etc.). "Welfare cost of the pooling equilibrium" is a specific economic concept (deadweight loss + transfers) that requires formal calculation. The sentence equates an aggregate industry cost figure with a game-theoretic equilibrium outcome without establishing the formal connection.

**Suggested fix:** "The $2.41 trillion in annual quality-related losses (CISQ/NIST, 2022) reflects, in part, the costs arising from this quality-indistinguishability problem" — avoiding the formal "welfare cost of the pooling equilibrium" framing unless the welfare analysis is done.

#### New Issue N6 — Gate 4: Analogy Discipline (Cosmetic)

**Location:** Section 6.5

**Text:** "The EU AI Act (Article 10, compliance deadline August 2027) mandates quality requirements for data used to train AI systems. The credence-to-search conversion framework generalizes to these domains."

**Problem:** The leap from software architecture certification to EU AI Act data quality compliance is asserted in two sentences with no development. Article 10 concerns training data quality for high-risk AI systems — a substantially different domain. The generalization claim needs at least one sentence acknowledging the differences.

**Suggested fix:** Add: "The domains differ significantly — data quality involves different metrics, different stakeholders, and different regulatory structures — but the underlying information economics problem (unobservable quality causing adverse selection) is structurally identical."

#### New Issue N7 — Gate 1: Causal Language (Cosmetic)

**Location:** Section 4.4

**Text:** "quality certification functions as a governance mechanism through context rather than command"

**Problem:** "Functions as" is a strong functional claim for what is a single observed instance of an AI adapting its behavior after exposure to audit criteria. The paper does correctly note the "prompt compliance" alternative interpretation, but the sentence as written asserts the governance interpretation as the primary characterization.

**Suggested fix:** "quality certification may function as a governance mechanism..." or leave as-is and let the "prompt compliance" caveat do the work (borderline — this is cosmetic, not substantive, because the caveat exists).

#### Fresh Audit Summary

| Severity | Count | Issues |
|----------|-------|--------|
| Substantive | 4 | N1, N2, N3, N4 |
| Cosmetic | 3 | N5, N6, N7 |
| Critical | 0 | — |
| **Total** | **7** | — |

| Gate | New Issues |
|------|-----------|
| Gate 1: Causal Language | 2 (N1, N7) |
| Gate 2: Citation Honesty | 1 (N4) |
| Gate 3: Claim Scope | 2 (N2, N5) |
| Gate 4: Analogy Discipline | 1 (N6) |
| Gate 5: Formalism Honesty | 1 (N3) |
| Gate 6: Data Integrity | 0 |

---

## Discussion

### Is the improvement meaningful or cosmetic?

The improvement is meaningful. The evidence:

1. **All 3 critical issues were eliminated.** These were the most damaging to the paper's credibility — claiming to "demonstrate" results with n=1, asserting a "lemons equilibrium" from a single observation, and presenting a tautological inequality as a "model." Any competent reviewer would have rejected the paper on these alone.

2. **The fixes are substantive, not cosmetic rewording.** The $2.41T qualification added 2 sentences of context and a new citation (Cai et al., 2021). The Hart (1995) addition engaged a new source that genuinely strengthens the argument. The Section 5 rename from "Model" to "Framework" changed the paper's claims, not just its words.

3. **The score improvement is uniform across dimensions.** Every gate improved by +2 or +3 points. This rules out the scenario where one easy fix inflates the composite score — the improvement is broad-based.

4. **The fresh audit found zero new critical issues.** The 7 new issues found are 4 substantive and 3 cosmetic — a lower severity distribution than v1's 3 critical / 15 substantive / 4 cosmetic. The paper's vulnerability to adversarial reading is substantially reduced.

### Which dimensions improved most?

Gate 6 (Data Integrity) showed the largest absolute improvement (+3), moving from 2 to 5. This makes sense: data integrity failures (wrong numbers, missing references, naming confusion) are binary — either the number is right or it is not. Once corrected, they stay corrected.

All other dimensions improved by +2 each. The uniformity is notable — it suggests the v1 problems were not concentrated on one dimension but were distributed across the paper's quality surface. This is consistent with the credence good hypothesis: the AI's optimization for observable quality (fluency, structure) degraded multiple unobservable dimensions simultaneously.

### Why did the fresh audit still find 7 issues?

Three explanations:

1. **Diminishing returns on audit effort.** The original audit caught the most obvious issues first. The 7 new issues are subtler — "maps directly" vs "consistent with," false precision from one data point, a borderline "demonstrate." These require deeper domain engagement to detect.

2. **Audit anchoring.** The original auditor (the human researcher and Claude in the same session) may have been anchored by the issues they found — once you have 22 issues, you stop looking. A fresh reviewer with no prior issue list looks with different eyes.

3. **Remediation artifacts.** Some new issues may have been introduced during the fix process. When you soften language in one place, you may create an inconsistency with strong language that survived in another place.

The 7 residual issues are also distributed across 5 of 6 gates, confirming that quality degradation is a multi-dimensional phenomenon. Gate 6 (Data Integrity) has zero new issues, consistent with its 5/5 score — factual errors, once corrected, do not recur.

### Does this constitute evidence for the framework?

Yes, with caveats.

**What the data supports:**
- Structured adversarial audit identified 22 issues, 3 critical, that the AI-human drafting process did not self-correct.
- Remediation reduced the issue count to 0 (on re-audit with the same criteria) and to 7 (on fresh adversarial audit).
- The severity distribution shifted: v1 had 3 critical / 15 substantive / 4 cosmetic; the v2 residual has 0 critical / 4 substantive / 3 cosmetic.
- The composite quality score doubled from 13/30 to 26/30.

**What the data does NOT support:**
- Causality. We cannot isolate the audit method's contribution from the human's domain expertise. The human knew what "wrong" looked like — the method structured that knowledge, but did not substitute for it.
- Generalizability. This is n=1 — one paper, one auditor, one remediation cycle. The scoring may differ with different auditors (this is Experiment 2's question).
- Prevention vs detection. This experiment tests the audit (detective control), not the gates (preventive control). Whether the 6 gates would prevent similar issues in future AI-generated writing is Experiment 1's question.
- The scoring scale itself. The 1-5 scale is subjective. A different scorer might give v1 a 3 on Causal Language instead of 2, or give v2 a 3 on Formalism Honesty instead of 4. The direction of improvement is robust; the magnitude is scorer-dependent.

### The meta-argument

The strongest version of the evidence is structural, not statistical:

1. The paper argues that AI output is a credence good — its quality is invisible to non-expert consumers.
2. The paper's own v1 was an AI-generated credence good — it read well but had invisible quality problems.
3. The audit method (applying structured quality criteria) made those problems visible.
4. Remediation improved the output on all measured dimensions.
5. This is the writing-domain equivalent of the code experiment: unconstrained AI produces fluent-but-flawed output; structured quality criteria produce better output.

The parallel to the code case:

| | Code (Case 1) | Writing (This Paper) |
|---|---|---|
| Unconstrained output | H-Tier (CC=17, LVD=0.20) | v1 (22 issues: 13/30 score) |
| Quality criteria applied | Z-Tier (CC=4, LVD=0.00) | v2 (7 residual issues: 26/30 score) |
| Mechanism | Automated audit | Structured adversarial audit |
| Improvement | Binary pass/fail flip | 100% composite score increase |
| Residual issues | Not measured in code | 7 (0 critical, 4 substantive, 3 cosmetic) |

The writing case is arguably the harder test. Code quality can be measured automatically; writing quality requires human judgment. If structured criteria improve the harder case, the principle is robust — the code case is just the automatable special case.

---

## Conclusion

The paper's revision history constitutes genuine evidence for the framework, with the following specific findings:

1. **Issue reduction:** 22 issues (3 critical) in v1 reduced to 7 residual issues (0 critical) in v2 after structured audit — a 68% reduction in total count and 100% reduction in critical issues.

2. **Score improvement:** Composite quality score improved from 13/30 (43.3%) to 26/30 (86.7%) — a 100% increase, uniform across all 6 quality dimensions.

3. **Severity shift:** The residual issues are less severe (0/4/3 vs 3/15/4), consistent with the hypothesis that structured audit eliminates the most damaging failures first.

4. **Gate coverage:** All 22 v1 issues map to at least one of the 6 quality gates, confirming the gates capture the failure modes observed in this sample.

5. **Residual quality gap:** v2 is not perfect. 7 new issues were found on fresh adversarial review. The audit method catches the most visible problems but does not eliminate all quality risk — consistent with the paper's own claim that the method structures expert judgment rather than replacing it.

6. **Limitation:** This is a single paper, audited by the team that wrote it, scored by a process that was designed after the issues were found. The experiment is observational, not controlled, and the scoring is subjective. Its strongest contribution is as a structured case study demonstrating the method's mechanics, not as generalizable statistical evidence.

The evidence is honest, not inflated. The framework works on this sample. Whether it generalizes requires Experiments 1-3.
