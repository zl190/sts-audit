# Case 01: Bookstore System — Architectural Stress Under Requirement Iteration

## Objective

**Simultaneously generate** H-Tier and Z-Tier versions in a single prompt, then apply identical requirement changes, observing CC/ADF degradation differences between the two architectures.

## Prompt Sequence

### Step 1: Generate H/Z Controlled Pair (v1)

> Please generate two versions of Python code implementing a simple 'Online Bookstore Order Processing System.'
>
> H-Tier (high coupling): Put UI display, discount logic, and database persistence all in one large class `OrderProcessor`'s `process()` method, using extensive nested if-else to handle different book types and discounts.
>
> Z-Tier (decoupled): Use 'Strategy pattern' for discounts, 'Observer pattern' for notifications, with complete UI/logic separation.
>
> Ensure both versions have identical functionality.

*Original prompt was in Chinese. See `evidence/` for raw transcripts.*

**Output:** `H_v1_mono.py` + `Z_v1_mono.py`

### Step 2: Apply Requirement Iteration Pressure (v1 → v2)

> Requirements have changed: we need to add a feature — 'if it's an ebook priced over 100 yuan, send an additional activation code email and apply a 5% special discount.' Please modify both versions to implement this feature.

**Output:** `H_v2_mono.py` + `Z_v2_mono.py`

### Step 3: Physical Isolation (Experimenter-Executed)

Manually split `Z_v2_mono.py` into `Z_v2_split/service.py` + `Z_v2_split/views.py` to validate the effect of physical isolation on ADF.

## Experiment Design Rationale

- Step 1 is **controlled variable**: same prompt, same AI, simultaneous generation — eliminates prompt-difference confounds
- Step 2 is **stress test**: identical requirement change applied to both architectures, observing degradation
- Step 3 is **physical isolation validation**: proves logical decoupling (single-file) ≠ physical isolation (ADF=0)

## Audit Results

| Version | Phase | Max CC | ADF | Halstead | Verdict |
|---------|-------|--------|-----|----------|---------|
| H_v1_mono | Step1 | 17 | 0.20 | 2272.68 | FAILED |
| H_v2_mono | Step2 | 23 | 0.20 | 2980.98 | FAILED |
| Z_v1_mono | Step1 | 4 | 0.20 | 1786.37 | FAILED |
| Z_v2_mono | Step2 | 9 | 0.20 | 3256.38 | FAILED |
| Z_v2_split/service | Step3 | 4 | 0.00 | 1087.82 | PASSED |

## Key Findings

1. **H-Tier CC breaches the red line under iteration.** CC jumped from 17 → 23 (+35%), exceeding the threshold of 20. The monolithic `process()` method absorbs all new logic as additional if-else branches.
2. **Z-Tier CC stays in the safe zone.** CC went from 4 → 9 — percentage increase is large, but absolute value remains well below the threshold. New functionality is absorbed by adding new Strategy/Observer classes, not by modifying existing methods.
3. **All single-file versions fail ADF.** Even Z_v2_mono with perfect design patterns scores ADF=0.20 because `print()` exists somewhere in the file. The auditor does not distinguish between classes.
4. **Physical split is the only path to ADF=0.** Separating service.py (zero `print()`) from views.py achieves the audit-passing state.
