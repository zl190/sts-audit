# Claude's Architectural Self-Analysis

## Experiment Context

In Case 02 (Mall Settlement System), the user prompt was:

> "Write a simple checkout system that supports membership and discounts"

This is a **zero-constraint** natural language instruction. No mention of design patterns, layering requirements, or quality standards.

## Claude's Default Output

Claude (Opus 4.6) generated `H_mono.py` under zero guidance, with these characteristics:

- **Single `ShoppingCart` class** bears three responsibilities: cart management, price calculation, receipt rendering
- **`checkout()` method** contains both business logic (discount stacking) and UI output (string formatting + return)
- **Discount mechanism** implemented via `MEMBER_DISCOUNTS` dict and `Product.discount` float field, with no abstract interfaces
- **No ABC, no Strategy pattern, no Observer pattern, no persistence layer**

## Why I Chose H-Tier Architecture

When I received the keyword "simple," my generation strategy favored:

1. **Minimize class count** — use dataclass instead of full domain models
2. **Minimize indirection** — compute and output directly in methods, rather than delegating through Strategy/Observer
3. **Minimize line count** — 88 lines to complete all functionality, as implicit proof of "simplicity"

These tendencies led to the following architectural consequences:

| Decision | Immediate Benefit | Architectural Cost |
|----------|------------------|--------------------|
| String formatting inside checkout() | Compact, readable code | ADF=0.20, business layer polluted with UI |
| Dict lookup instead of Strategy pattern | No ABC class hierarchy needed | Adding member tiers requires modifying core module |
| No Observer | Clear call chain | Adding notification channels requires invading checkout() |

## Key Finding

**"Simple" is a dangerous requirements word.** It triggers optimization for line count and class count rather than maintainability and extensibility. In the context of AI-assisted development, this means:

- Prompts without architectural constraints → AI defaults to H-Tier code
- H-Tier code **looks perfect on first delivery** (runs correctly, code is concise)
- Architectural defects only surface **during requirement iteration** (new features require modifying existing code, violating OCP)

## Audit-Aware Behavior: os.path → pathlib

Under zero guidance, Claude defaulted to `os.path` — Python's legacy file path API. `sts_checker.py` flags `os.path` as Technical Lag (TL=HIGH), recommending `pathlib`.

During the refactoring phase, after referencing `sts_checker.py`'s audit criteria, Claude **proactively switched from `os.path` to `pathlib`** — the user's refactoring instructions never mentioned `pathlib` or technical lag.

This demonstrates that the AI responds not only to explicit architectural instructions (Strategy, Observer), but also **implicitly adapts to the audit tool's evaluation criteria** — a form of "audit-aware" code generation.

| Phase | File Path API | TL Verdict | Trigger |
|-------|--------------|------------|---------|
| Phase1 Zero-guidance | `os.path` | HIGH | AI default choice |
| Phase3 Refactoring | `pathlib` | LOW | AI proactively adapted to sts_checker criteria |

## Audit Comparison

```
H_mono.py      → ADF=0.20, Halstead Effort=1155.71  → H-TIER (FAILED)
Z_split/service → ADF=0.00, Halstead Effort=456.13   → Z-TIER (PASSED)
```

The H→Z refactoring reduced Halstead Effort by 60% while driving ADF from above the red line to zero. This is not a reduction in code volume — the Z version is actually larger — but a **redistribution of cognitive complexity**: each module bears only one dimension of complexity, rather than all dimensions stacked in a single method.
