# Credence Good Audit Framework

**Status:** Personal tool / early-stage follow-up project. Not part of the STS finance paper.

## What This Is

STS audits code for hidden architectural quality — converting a credence good into a search good. This framework applies the same principle to **any AI-generated output**: writing, analysis, advice, research.

The insight: when we ran a skeptical audit on our own AI-written research paper, the same failure modes appeared — decorative citations, overclaimed results, tautological models disguised as formal proofs. Explicit quality criteria caught all of them. The credence good problem isn't specific to code. It's a property of AI output in general.

## Origin

During the STS paper audit (2026-02-23), we applied structured quality criteria to an AI-drafted finance paper and found 22 issues (3 critical, 15 substantive, 4 cosmetic). The correction process mirrored the disclosure-as-governance mechanism the paper itself describes: audit criteria improved rigor in writing the same way they improved architecture in code.

## Contents

| File | What it is | How to use it |
|------|-----------|---------------|
| `claude_quality_gates.md` | CLAUDE.md-style instructions | Copy relevant sections into any project's CLAUDE.md |
| `audit_method.md` | Repeatable adversarial audit method | Follow the steps to audit any AI output in any domain |

## Relationship to STS

STS is the **code-specific** instance of this framework:
- Domain: software architecture
- Quality dimensions: CC, LVD, CCR, TL
- Audit tool: `sts_checker.py`
- Signal: binary PASS/FAIL

This framework is the **domain-agnostic generalization**:
- Domain: any AI output (writing, analysis, code, advice)
- Quality dimensions: defined per domain (see `audit_method.md`)
- Audit tool: human + structured checklist (automatable per domain)
- Signal: issue list with severity

## Future Work

This needs experiments before it's publishable:
- Apply the writing audit to N AI-generated papers, measure before/after issue counts
- Test whether CLAUDE.md quality gates reduce issue rates vs. unconstrained generation
- Compare domains: does the same framework work for code, writing, and data analysis?
- Measure the "disclosure as governance" effect: does the AI self-correct when gates are present but not explicitly enforced?

## Not Goals (for now)

- This is not a product
- This is not part of the conference submission (except as a one-liner in the AI workflow appendix)
- This does not replace domain-specific tools (STS for code, style guides for writing, etc.)
