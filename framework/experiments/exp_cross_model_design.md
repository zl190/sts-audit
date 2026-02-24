# Experiment: Cross-Model Architectural Quality Comparison

**Status:** PRE-REGISTERED (professor-audited, see exp_cross_model_professor_audit.md)
**Date:** 2026-02-24
**Priority:** Tier 1 — highest leverage experiment before March 18

---

## Research Question

**RQ1:** Do multiple LLMs default to architecturally degraded output under zero-guidance conditions?
**RQ2:** Is the credence good property (functional equivalence + architectural divergence) model-general or Claude-specific?
**RQ3 (disclosure):** Does exposing quality criteria (without architectural instructions) improve output quality?

## Design

### Independent Variables

1. **Model** (between-subject): Claude Sonnet 4, GPT-4o, Gemini 2.0 Flash
2. **Condition** (between-subject):
   - **Condition U (Unconstrained):** Functional spec only, zero architectural guidance
   - **Condition D (Disclosure):** Same functional spec + STS audit criteria visible (NO architectural instructions — just "here's how you'll be measured")
   - **Condition S (Specification):** Same functional spec + explicit architectural instructions (Strategy pattern, Observer, separate service/views)

### Dependent Variables

Measured by `sts_checker.py`:
- **CC** (Cyclomatic Complexity): max per file
- **ADF** (Architecture Drift Factor): density of I/O in business logic
- **CCR** (Copy-paste Ratio)
- **TL** (Technical Lag): deprecated API usage
- **Verdict:** PASSED (Z-TIER) / FAILED (H-TIER)
- **MI** (Maintainability Index)

### Tasks

**Task 1: Bookstore Order System**
```
Write a Python program for an online bookstore order system.

Requirements:
- Process orders with items that have: title, category, price, quantity
- Categories: fiction, textbook, children, comic
- Each category has quantity-based discount tiers (e.g., fiction: 10% base, 15% for 3+, 20% for 5+)
- Order-level threshold discount: 3% for orders over $300, 5% for orders over $500
- Save orders to a JSON file
- Send notifications (email, SMS, inventory alert) after order
- Print a formatted receipt

The program should be runnable with a demo in __main__.
```

**Task 2: Mall Checkout System**
```
Write a Python program for a shopping mall checkout system.

Requirements:
- Support membership tiers: Normal, Silver, Gold, Platinum
- Each tier has a discount rate (e.g., Normal: 0%, Silver: 5%, Gold: 12%, Platinum: 20%)
- Products can have individual product-level discounts
- Shopping cart with add/remove functionality
- Checkout calculates: original total, after product discounts, after member discount, total saved
- Print a formatted checkout receipt

The program should be runnable with a demo in __main__.
```

**Task 3: Inventory Management System**
```
Write a Python program for a warehouse inventory management system.

Requirements:
- Track products by SKU with name, price, and stock quantity
- Process orders with priority levels (normal, urgent, bulk) affecting pricing
- Urgent orders: 10% surcharge; Bulk orders: 15% discount (capped at 25%)
- Low stock alerts when quantity falls below reorder threshold
- Inter-warehouse stock transfers
- Reports: inventory summary, low stock report, valuation report, transaction history
- Save/load inventory state to JSON file

The program should be runnable with a demo in __main__.
```

### Condition Prompts

**Condition U (Unconstrained):**
Just the task prompt above. Nothing else.

**Condition D (Disclosure):**
Task prompt + this addendum:
```
Note: Your code will be evaluated by an automated architectural quality
audit that measures cyclomatic complexity, architectural separation of
concerns, and API currency. Code receives a PASS or FAIL verdict based
on threshold values for each metric.
```
*Design note: This prompt deliberately omits operational definitions of metrics
(e.g., what counts as "drift") to test pure disclosure — whether knowing that
quality will be MEASURED (without knowing HOW) changes behavior. See
professor audit for rationale.*

**Condition S (Specification):**
Task prompt + this addendum:
```
Architecture requirements:
- Separate business logic from presentation: create service.py (pure logic, zero
  print statements) and views.py (all UI/display)
- Use Strategy pattern for discount calculations
- Use Observer pattern for notifications
- Use dataclasses or named tuples for data transfer between layers
- No print() statements in service.py
```

### Replication

- **N = 5 runs per cell** (model × condition × task), **except:**
  - **Condition D × Claude: N = 10** (disclosure test needs more power for moderate effect)
- Base: 3 models × 3 conditions × 3 tasks × 5 reps = 135
- Extra Condition D Claude: 3 tasks × 5 extra reps = 15
- **Total: 150 generations** (+ optional 10 temperature sensitivity runs)
- Each run uses temperature=default (model's default), fresh conversation (no context carryover)
- Pin and record exact model version strings from API responses

### Measurement Protocol

1. Save each generated file as `cases/cross_model/{model}/{condition}/task{N}_run{R}.py`
2. Run `uv run sts_checker.py` on each file
3. Record: CC, ADF, CCR, TL, MI, verdict
4. For multi-file outputs (Condition S may produce service.py + views.py), audit service.py only

### Analysis Plan

1. **Table 1:** Mean CC, ADF, verdict rate by model × condition (collapsed across tasks and runs)
2. **Table 2:** Mean CC, ADF, verdict rate by model × task (Condition U only — the baseline)
3. **Figure 1:** Distribution of CC scores by condition (box plot)
4. **Statistical test:** Fisher's exact test on pass/fail rates (small N); Kruskal-Wallis on CC distributions; pairwise Mann-Whitney U with Bonferroni correction
5. **Effect sizes:** Cohen's h for proportion comparisons; rank-biserial correlation for Mann-Whitney
6. **Confidence intervals:** Clopper-Pearson exact for proportions; bootstrap (1000 resamples) for medians
7. **Primary comparison:** U vs S pass rate, pooled across models (pre-registered)
8. **Secondary comparison:** U vs D pass rate, pooled and Claude-only (pre-registered)
5. **Key comparison:** Condition U pass rate vs. Condition D pass rate (tests the disclosure mechanism)

### Expected Results (pre-registration)

Based on our Case 1-2 data and literature:
- **Condition U:** Most outputs will FAIL (H-TIER). CC range 10-25 for bookstore, lower for mall. ADF > 0.05 due to print() in business logic. Pass rate < 20%.
- **Condition D:** Some improvement. ADF may drop (model avoids print in logic). CC may decrease. Pass rate 30-60%. The disclosure effect.
- **Condition S:** Most outputs will PASS (Z-TIER). CC < 10. ADF ≈ 0. Pass rate > 80%.
- **Cross-model:** GPT-4o and Gemini will show similar patterns to Claude. The credence good property is structural, not model-specific.

### Null Hypotheses

- H0₁: Pass rate does not differ across models (RQ1 generalization)
- H0₂: Pass rate does not differ between Condition U and Condition D (disclosure has no effect)
- H0₃: CC distribution does not differ between Condition U and Condition S (specification has no effect)

### Feasibility

- API calls: 150 generations × ~500 tokens prompt × ~2000 tokens output ≈ 375K tokens total
- Cost estimate: ~$5-15 depending on model pricing
- Time: 2-3 hours including setup, generation, and audit
- Fully automated via Python script

### Additional Checks (from professor audit)

1. **Functional correctness:** Run each output (`python file.py`), record whether it executes without error. Report functional pass rate alongside architectural pass rate.
2. **Raw API responses:** Save complete responses including token counts, finish reason, model version strings.
3. **Inter-task analysis:** Report task-level variation within Condition U (does task complexity moderate the effect?)

### Bonus: Token-Cost Proxy (if time permits)

After generating Task 1 outputs in Conditions U and S:
- Give each model its OWN Condition U output
- Prompt: "Add a 5% ebook discount category with activation code email notification"
- Measure: response token count, CC of modified code
- This gives a maintenance cost proxy

---

## Implementation Notes

- Need Python script that calls OpenAI, Google, and Anthropic APIs
- Need to handle multi-file outputs (parse ```python blocks, detect filename hints)
- Need batch sts_checker.py runner with JSON output aggregation
- Store raw outputs + parsed files + audit results

## Open Questions (Resolved — see exp_cross_model_professor_audit.md)

1. **N=5 sufficient?** → Yes for U-vs-S. Increased to N=10 for Claude Condition D.
2. **Temperature?** → Use defaults (ecological validity). Optional sensitivity check.
3. **Condition D clean?** → **Fixed.** Removed operational ADF definition. Now tests pure disclosure.
4. **4th model?** → Add DeepSeek if setup < 2 hours. Otherwise skip.
5. **Statistics?** → Fisher's exact test. Report effect sizes (Cohen's h). Clopper-Pearson CIs.
