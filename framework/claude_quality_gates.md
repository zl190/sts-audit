# Quality Gates for AI-Generated Research Writing

Copy the relevant sections below into a project's CLAUDE.md to activate them as constraints during AI-assisted writing. These gates are derived from 22 issues found during adversarial audit of an AI-written finance paper.

---

## How to Use

Add this to your CLAUDE.md (or system prompt):

```
## Writing Quality Gates

Follow these rules when drafting, editing, or revising research writing.
Violations are treated the same as bugs in code — fix before delivery.
```

Then include whichever gate sections apply to your domain.

---

## Gate 1: Causal Language

**Failure mode:** AI defaults to strong causal claims regardless of evidence strength.

```
### Causal Language Policy
- NEVER use "demonstrate," "prove," or "establish" for results with n < 30 or without controlled design
- Case studies "illustrate," "suggest," or "provide evidence consistent with"
- Correlations do not "show" causation — use "is associated with" or "predicts"
- Single examples are "anecdotal" or "illustrative," not "evidence for"
- If a result has one data point, say so explicitly: "a single case study"
```

**Why it matters:** The AI produced "We demonstrate three results" for n=1 case studies. A reviewer catches this instantly. It undermines the entire paper's credibility.

## Gate 2: Citation Honesty

**Failure mode:** AI cites papers it hasn't substantively engaged with, or cites papers whose models don't actually apply.

```
### Citation Policy
- Every citation must serve a specific, stated purpose (support, contrast, method, or data)
- Do NOT cite a paper just to show you know it exists (decorative citation)
- If you cite a theoretical model, state whether its assumptions hold in your context
- If a cited model's assumptions DON'T hold, say so explicitly — don't just name-drop it
- If a paper could be read as undermining your argument, engage with it honestly rather than citing it as if it supports you
- Do NOT leave dangling references (cited in text but missing from reference list, or vice versa)
```

**Why it matters:** The AI cited Board & Meyer-ter-Vehn (2013) on reputation without noting their model requires quality revelation — which doesn't hold for credence goods. It cited Hart & Moore (1988) without engaging with Hart (1995), which is actually the relevant work. Reviewers who know these papers will see through this immediately.

## Gate 3: Claim Scope

**Failure mode:** AI inflates scope of claims beyond what the evidence supports.

```
### Claim Scope Policy
- Every quantitative claim must trace to a specific source with matching scope
- If the source measures X broadly and you're studying a subset, qualify: "of which [subset] is a component"
- Do NOT use superlatives ("largest," "first," "most important") without explicit justification
- Prefer hedged forms: "a major" over "the largest," "more complete" over "complete," "consistent with" over "confirms"
- When citing a dollar figure, state what it covers — not just the number
- If your sample is small, lead with the sample size, not the conclusion
```

**Why it matters:** The AI wrote "$2.41 trillion in annual losses from software architecture quality" when the source covers *all* software quality losses. It called software "the largest unanalyzed credence goods market" without evidence for that ranking. These are the claims reviewers attack first.

## Gate 4: Analogy Discipline

**Failure mode:** AI draws compelling analogies without acknowledging where they break.

```
### Analogy Policy
- Every analogy must include at least one explicit caveat about where it breaks
- Structural similarity does not imply behavioral similarity — state the limits
- If the analogy domain has regulatory mandates and yours doesn't, say so
- Do NOT use an analogy as evidence — it is illustration only
- When reducing a cited effect size for honesty (e.g., "2x" instead of "3x"), explain why
```

**Why it matters:** The AI drew a LEED analogy (green building certification → software certification) without noting that LEED operates in a market with regulatory mandates and consumer sustainability preferences that don't exist for software. The analogy is useful but dishonest without the caveat.

## Gate 5: Formalism Honesty

**Failure mode:** AI produces mathematical notation that looks formal but is logically trivial or tautological.

```
### Formalism Policy
- If you write an equation, it must say something non-trivial — "cost goes up when quality goes down" is not a model
- Tautological inequalities (A > B where A is defined as "the thing that's bigger") must be flagged
- Label speculative frameworks as "Framework" not "Model" unless they produce testable predictions
- If parameters cannot be estimated from available data, say so — don't pretend the model is operational
- Distinguish between: proven theorem, testable hypothesis, conceptual framework, and notation for an intuition
```

**Why it matters:** The AI produced a "Capital Allocation Model" (Section 5) that was a tautological inequality — maintenance cost exceeds replacement cost at the rewrite point, which is true by definition. It had mathematical notation but no content beyond the verbal description. Renaming to "Framework" and acknowledging the limitations was the fix.

## Gate 6: Data Integrity

**Failure mode:** AI fabricates or misremembers specific numbers, file sizes, class counts.

```
### Data Integrity Policy
- Every number must be verifiable against the actual artifact or source
- If you state "88 lines, single class" — verify it's not actually 132 lines with 5 classes
- If metric values appear in a table, they must match the tool's output exactly
- Do NOT round, truncate, or adjust numbers to make a narrative cleaner
- If two naming conventions exist for the same metric (e.g., LVD vs ADF), define both and state the mapping
```

**Why it matters:** The AI described the mall case as "88 lines, single class" when it was actually 132 lines with 5 classes. The case *still* failed the audit, but on LVD, not CC. Getting the facts wrong is worse than having a less dramatic result.

---

## Meta-Gate: Self-Audit

This gate is about the writing process itself.

```
### Self-Audit Requirement
- Before finalizing any draft, re-read every claim as a skeptical reviewer would
- For each citation, ask: "If the cited author read this sentence, would they agree with how I used their work?"
- For each number, ask: "Can I point to the exact source cell/line/output?"
- For each analogy, ask: "Where does this break, and did I say so?"
- If you find an issue, fix it — do not flag it and leave it for the human
```

---

## Domain Adaptation

These gates are written for research writing. To adapt to other domains:

| Domain | Gate 1 (Causal) | Gate 2 (Citation) | Gate 3 (Scope) | Gate 4 (Analogy) | Gate 5 (Formalism) | Gate 6 (Data) |
|--------|----------------|-------------------|----------------|-----------------|-------------------|---------------|
| Research writing | As above | As above | As above | As above | As above | As above |
| Business analysis | "Our data shows" → "Our data suggests" | Source every market stat | Qualify TAM/SAM/SOM | Competitor analogies need caveats | Financial projections need assumptions stated | Verify every metric against source |
| Technical docs | "This ensures" → "This is designed to" | Link to actual API docs, not memory | Version-qualify all claims | Architecture analogies need limits | Pseudocode must match real code | Code samples must compile/run |
| Legal/compliance | "This complies" → "This is intended to comply" | Cite statute + section | Jurisdiction-qualify | Precedent analogies need distinguishing | Regulatory formulas need source | Quote exact regulatory text |
