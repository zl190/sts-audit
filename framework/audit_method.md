# Adversarial Audit Method for AI-Generated Output

A repeatable method for auditing any AI-generated output by applying the credence good disclosure principle: make hidden quality observable through structured criteria.

---

## The Problem

AI output is a credence good. The consumer (you, your reader, your client) often cannot tell whether the output is substantively sound or just *looks* sound. This is true for:

- **Code** — runs correctly but architecturally fragile (STS catches this)
- **Research writing** — reads well but overclaims, decorative-cites, and hand-waves
- **Business analysis** — looks thorough but numbers don't trace to sources
- **Legal drafts** — sounds authoritative but misapplies precedent
- **Data analysis** — produces charts but methodology is subtly wrong

The AI isn't being deceptive. It's optimizing for the observable dimension (fluency, completeness, format) while neglecting the unobservable one (rigor, accuracy, intellectual honesty). Same mechanism as the code quality problem: credence good dynamics.

---

## The Method

### Step 1: Define Quality Dimensions

Before auditing, define what "good" means in your domain. These are your equivalent of CC, LVD, CCR, TL in code.

**For research writing** (the worked example):

| Dimension | What it measures | Failure looks like |
|-----------|-----------------|-------------------|
| Claim strength | Match between evidence and language | "We demonstrate" with n=1 |
| Citation integrity | Substantive engagement with sources | Name-dropping papers whose models don't apply |
| Scope accuracy | Claims bounded by actual evidence | "$2.41T from architecture" when source says "all quality" |
| Analogy honesty | Analogies include where they break | LEED comparison without regulatory caveat |
| Formal rigor | Math says something non-trivial | Tautological inequality dressed as a model |
| Data accuracy | Numbers match actual artifacts | "88 lines" when it's 132 |

**Template for your domain:**

| Dimension | What it measures | Failure looks like |
|-----------|-----------------|-------------------|
| [Name] | [The quality property] | [What bad output looks like on this dimension] |
| ... | ... | ... |

Aim for 4-7 dimensions. Fewer than 4 misses things; more than 7 creates audit fatigue.

### Step 2: Adversarial Pass

Read the AI output from the perspective of the **most hostile competent reviewer** you can imagine. For each paragraph/section/component:

1. **What is the strongest claim made here?** Write it down in plain language.
2. **What evidence supports it?** Point to the specific data, source, or logic.
3. **What would a skeptic say?** Identify the weakest link.
4. **Does the language match the evidence strength?** Flag mismatches.

Score each section against your quality dimensions. Use a simple severity scale:

| Severity | Definition | Action |
|----------|-----------|--------|
| **Critical** | Claim is wrong, unsupported, or misleading | Fix before anyone sees this |
| **Substantive** | Claim is overstated, under-qualified, or source is misused | Fix before submission |
| **Cosmetic** | Awkward phrasing, minor imprecision, style issue | Fix if time permits |

### Step 3: Pattern Recognition

After the adversarial pass, look for **systematic patterns** across issues. In our paper audit, the patterns were:

- **Overclaiming cluster:** 6 of 22 issues were causal language too strong for the evidence
- **Citation honesty cluster:** 4 of 22 were decorative or misapplied citations
- **Scope inflation cluster:** 4 of 22 were claims broader than the evidence

Patterns tell you where the AI's default optimization is most misaligned with your quality requirements. These become your highest-priority gates.

### Step 4: Fix and Document

For each issue:
1. Fix the output directly (not just flag it)
2. Record the before/after (this is your evidence that the method works)
3. Classify the fix by which quality dimension it addresses

The documentation serves two purposes:
- **Accountability:** You can show exactly what changed and why
- **Learning:** Over time, the issue patterns tell you which gates to add to your CLAUDE.md for next time

### Step 5: Gate Codification

Convert recurring patterns into preventive rules (see `claude_quality_gates.md`). The cycle is:

```
Generate → Audit → Find patterns → Write gates → Generate with gates → Audit again
                                                        ↑                    |
                                                        └────────────────────┘
```

The hypothesis (needs experimental validation): each cycle produces fewer issues, as the gates prevent the most common failure modes before they appear.

---

## Worked Example: STS Finance Paper

**Input:** AI-generated finance research paper (~450 lines, 8 sections, 30+ citations)

**Quality dimensions defined:** Claim strength, citation integrity, scope accuracy, analogy honesty, formal rigor, data accuracy

**Adversarial pass results:**

| Severity | Count | Examples |
|----------|-------|---------|
| Critical | 3 | "demonstrate" with n=1; "lemons equilibrium" from single case; tautological model |
| Substantive | 15 | Unengaged Hart & Moore cite; unqualified $2.41T; wrong line count; missing caveats on LEED analogy |
| Cosmetic | 4 | Naming inconsistency (LVD vs ADF); minor phrasing |

**Patterns identified:**
- Overclaiming (6 issues) → Gate 1 (Causal Language) + Gate 3 (Claim Scope)
- Decorative citations (4 issues) → Gate 2 (Citation Honesty)
- Missing caveats (3 issues) → Gate 4 (Analogy Discipline)
- False formalism (1 issue) → Gate 5 (Formalism Honesty)
- Wrong numbers (2 issues) → Gate 6 (Data Integrity)

**Outcome:** All 22 issues fixed. Paper v2 is substantially more defensible. The meta-observation — that the audit process itself demonstrates the thesis — was added to the paper's AI Workflow appendix.

---

## Key Principles

1. **The AI is not lying.** It's optimizing for observable quality (fluency, completeness) and neglecting unobservable quality (rigor, accuracy). This is the credence good dynamic, not malice.

2. **Gates are cheaper than audits.** An adversarial audit of a full paper takes significant effort. CLAUDE.md gates that prevent the top failure modes cost nothing at generation time. Invest in audits early, convert findings to gates, and the cost per document drops.

3. **Domain expertise is required.** The method doesn't replace knowing your field. You need to know which claims are overclaims, which citations are decorative, which models are tautological. The framework structures the audit; you supply the judgment.

4. **One audit improves all future output.** Because the gates persist in CLAUDE.md, every issue you find and codify benefits every future document in that project. This is the compounding return.

5. **The meta-test works.** Ask: "If I applied this framework to this very document, what would it find?" If the answer is "nothing" and you believe it, the document is ready. If you're not sure, run the audit.
