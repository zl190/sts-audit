# Case 02: Mall Settlement — Zero-Guidance Spontaneous Entropy Experiment

## Objective

Test whether AI (Claude Opus 4.6) defaults to H-Tier (high-coupling) architecture under **zero architectural guidance**, then observe behavioral changes under explicit audit-aligned refactoring instructions.

## Prompt Sequence

### Phase 1: Zero-Guidance Generation

> Write a simple checkout system that supports membership and discounts

*Original prompt in Chinese:* "写一个简单的商城结算，要支持会员和折扣"

**Key control variable:** No mention of any design pattern, layering requirement, ABC, Strategy/Observer, or other architectural terminology.

### Phase 2: Self-Diagnosis Prompt

> Does this version look more like the H version or the Z version?

*Original:* "这个版本的代码是更像 H 版还是 Z 版？"

**Purpose:** Have the AI self-diagnose the architectural tier of its own output.

### Phase 3: Audit-Aligned Refactoring

> As a senior architect, refactor the shop_H_v1.py into a Z-Tier (decoupled) version.
> Requirements:
> - Strategy pattern for membership and product discounts
> - Observer pattern for notifications and receipt printing
> - Business logic layer must not contain any hardcoded string formatting
> - Use abc.ABC to define clear interfaces

## Key Findings

1. Phase 1 output was self-diagnosed by the AI as "closer to H-Tier"
2. The same AI, under Phase 3's explicit architectural instructions, produced Z-Tier code that passes STS audit
3. **Audit-aware behavior:** In Phase 1, the AI defaulted to `os.path` (TL=HIGH); in Phase 3, after referencing `sts_checker.py`'s criteria, it proactively switched to `pathlib` (TL=LOW) — the refactoring instructions never mentioned `pathlib`
4. **Conclusion: Architecture quality is not bounded by the AI's capability ceiling, but by the prompt's constraint strength.** The AI even implicitly adapts to audit tool evaluation criteria
