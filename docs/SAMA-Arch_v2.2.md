# Software Architecture Maintenance Agreement (SAMA-Arch)

## 1. Scope

This agreement applies to all software deliverables developed with AI assistance. All deliverables must pass automated STS audit prior to acceptance.

## 2. Tier Definitions & Service Terms

### Z-TIER Deliverables (Premium Tier)

| Clause | Terms |
|--------|-------|
| Audit Result | ADF < 0.05, Max CC < 10, TL = LOW, PASSED |
| Maintenance SLA | Vendor commits CC delta ≤ 2 per requirement change in core business modules |
| Regression Testing | New features must not require modification of existing unit tests |
| Defect Resolution | 72-hour SLA for defect identification and fix |
| Renewal | Quarterly audit; consecutive PASSED results qualify for automatic renewal |

### H-TIER Deliverables (Risk Tier)

| Clause | Terms |
|--------|-------|
| Audit Result | ADF > 0.05 or Max CC > 20 or CCR > 0.3, FAILED |
| Disposition | Reject delivery / Mandate refactoring |
| Refactoring Window | 14 business days to refactor and resubmit for audit |
| Post-Refactor Acceptance | Must achieve Z-TIER to enter maintenance phase |
| Cost Allocation | Refactoring costs borne by vendor (architectural defects are delivery quality issues) |

## 3. Audit Execution Protocol

- **Tool:** `sts_checker.py` v2.2 (SAMA-Arch)
- **Target:** Business logic layer source files only (excludes UI/View layer)
- **Frequency:** Automated execution before every merge to trunk (CI integration)
- **Dispute Resolution:** Quantitative audit output is authoritative; subjective assessments are not accepted

## 4. Typical Scenarios

### Scenario A: First Delivery of AI-Generated Code

```
1. Vendor generates code using AI tools
2. Run: python sts_checker.py service.py
3. Z-TIER → Proceed to acceptance
4. H-TIER → Return for refactoring, resubmit
```

### Scenario B: Regression Audit After Requirement Iteration

```
1. Client submits new requirement (e.g., add membership tier)
2. Vendor iterates on Z-TIER codebase
3. Post-iteration audit must remain Z-TIER
4. Regression to H-TIER → Classified as maintenance quality incident
```

## 5. Appendix: Verdict Formulas

### Per-File Verdict

$$is\_failed = (CC_{max} > \texttt{cc\_threshold}) \lor (ADF > \texttt{adf\_threshold}) \lor (CCR > \texttt{ccr\_threshold})$$

$$tier = \begin{cases} \text{H-TIER (FAILED)} & \text{if } is\_failed \\ \text{Z-TIER (PASSED)} & \text{otherwise} \end{cases}$$

Default thresholds: `cc=20, adf=0.05, ccr=0.3`. Configurable via `.sts.toml`.

### Project-Level Verdict

$$Z\text{-TIER} \iff (CC_{max} < \texttt{project\_cc}) \land (ADF_{max} < \texttt{adf\_threshold}) \land (TL_{global} = \text{LOW}) \land (CCR_{max} \leq \texttt{ccr\_threshold})$$
