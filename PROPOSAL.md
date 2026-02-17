# PROPOSAL: Making Software Quality Visible — From Credence Good to Inspection Good

## Abstract

Software is a **credence good**: buyers cannot verify its architectural quality even after delivery. A client cannot tell whether the code behind a working screen is clean or spaghetti — and because quality is invisible, it cannot be priced, contracted, or insured. This information asymmetry drives a vicious cycle: clients won't pay for architecture they can't see → developers don't invest in architecture → maintenance costs explode → the industry loses $2.41 trillion/year to poor software quality (CISQ/NIST, 2022).

This project proposes **STS (Software Tier Standard)**, a framework that converts software from a credence good into an **inspection good** — one whose quality is deterministically verifiable via automated audit. STS uses static code metrics to classify software into quality tiers (H-Tier / Z-Tier), and maps those tiers directly to commercial contract clauses, transforming "business haggling" into "engineering calculation."

We validate the framework through controlled experiments with AI-generated code, demonstrating that (1) unconstrained LLMs default to architecturally degraded code via a behavior we term **logic diffusion**, (2) the same AI produces high-quality code when architectural constraints are present, and (3) the audit standard itself acts as an **implicit prompt** — AI self-corrects when it encounters quality specifications.

We argue this framework generalizes beyond software to any domain where quality is invisible and contractually unenforceable — including medical data quality for AI training sets, where the EU AI Act (Article 10, compliance deadline August 2027) creates urgent regulatory demand for exactly this kind of tiered quality verification.

---

## 1. The Problem: Why Software Maintenance Costs Spiral Out of Control

The question that started this project came from an undergraduate Software Design Process (SDP) course:

> *"Why can't software be priced like selling cars — with clear prices for each option?"*

The answer reveals a structural market failure. In construction, quality is physically visible: a crooked wall, a leaking roof. The cost of change is visible too — you see the sledgehammer destroying expensive materials. In software, the "material" is invisible. When a client asks to change a logic flow, they don't see a sledgehammer; they see a person typing. They perceive the cost as "just a few hours of your time," even when that change triggers a cascade of structural damage deep inside the system.

This invisibility creates three compounding problems:

1. **The Abstraction Gap.** Adding a "Login with Google" button looks like a 1-inch change on a UI mockup. Behind it: OAuth protocols, security tokens, database migrations, error handling. The client sees a small button and thinks "tiny change."

2. **The Adverse Selection Spiral.** Because clients cannot see architecture quality, they cannot price it. A search feature costs the same whether the code is clean or spaghetti. Developers who invest in architecture are penalized (higher cost, same perceived output). Developers who cut corners are rewarded (lower cost, same perceived output). Quality degrades market-wide.

3. **The Maintenance Trap.** Software delivery day is the day it begins to rot. Environment changes, user growth, and requirement evolution all stress the architecture. Poor architecture absorbs these stresses badly — maintenance costs grow superlinearly. But by the time the client discovers this, the original developer is gone.

**The root cause is not technical. It is economic.** Software architecture quality is a hidden variable in every software transaction. Making it visible — measurable, contractable, priceable — is the prerequisite for fixing the market.

---

## 2. The Circuit Board Delivery Model

We propose decomposing software delivery into four independently priceable layers, analogous to a circuit board system:

### 2.1 Board (Architecture)

The board determines the system's ceiling: concurrency capacity, extensibility, and resilience to requirement changes. It is tiered:

- **H-Level (Hobbyist):** High coupling, single-class designs, business logic entangled with I/O. Development is fast and cheap. But the board does not support "non-destructive modification" — adding features beyond the original scope requires partial or full rewrite.
- **Z-Level (Enterprise):** Decoupled architecture using Strategy pattern, Observer pattern, and ABC interfaces. Development is slower and more expensive. But the board supports modular extension — new features plug in without disturbing existing modules.

**The key commercial innovation:** The board specification becomes a contractual term. When a client signs for an H-Level board and later requests a cross-module UI change, this is not a "modification request" — it is a **breach of the board's physical capacity**, analogous to demanding a load-bearing wall be moved after construction. The contract language shifts from "it's expensive because I'm professional" (which the client doesn't believe) to "the metrics exceeded the board's rated capacity — this triggers the refactoring clause" (which is verifiable).

### 2.2 Components (Features)

Each feature is a clearly priced, independently deliverable unit with explicit acceptance criteria. "Supports search" is soft; "returns results within 2 seconds across 1M records via keyword" is hard. Adding a feature after delivery is treated as a new component purchase, not a free adjustment.

### 2.3 UI Layer

Visual presentation based on the board's interfaces. UI changes that stay within the board's rated interface boundaries are priced as design work. UI changes that violate those boundaries escalate to board-level rework — and the contract makes this escalation visible and priced in advance.

### 2.4 Insurance (Testing)

Testing coverage is tiered:

- **Basic:** Main flow passes (suitable for prototypes).
- **Professional:** Unit tests, 99% core path coverage (suitable for commercial use).
- **Industrial:** Stress testing, concurrency testing, automated regression (suitable for regulated industries).

Each tier corresponds to a different warranty/liability allocation. If the client buys "Basic" and later complains about edge-case failures, the contract is clear: that risk was not covered.

---

## 3. The AI Accelerator: Why 2026 Makes This Urgent

### 3.1 Logic Diffusion: The Path of Least Resistance

We observe that unconstrained LLMs tend to complete tasks via what we term **logic diffusion** — optimizing for the shortest path to a passing test case rather than for architectural quality.

- **Human architect's reasoning:** "To add this feature, I should refactor the interface first — slower now, faster later."
- **AI's reasoning:** Optimize for passing the current test case fastest → add `if` blocks, scatter variables, collapse layers.

This is not a capability limitation. Our experiments (Section 6) show that the same AI, given the same functional requirements, produces both H-Tier and Z-Tier code depending on prompt constraints. The architecture quality is bounded by **constraint strength**, not by AI capability.

### 3.2 The Stamina Dividend Masks Logic Debt

AI has unlimited stamina. It can brute-force its way through a 10,000-line monolith without fatigue. This creates a dangerous illusion: the code works, the delivery is fast, the client is happy — until the first requirement change reveals that the architecture cannot absorb stress without cascading breakage.

Industry data confirms the trend: GitClear reports rising code duplication in AI-assisted codebases; Google's DORA report shows a 7.2% delivery stability decrease correlated with 25%+ AI usage; Forrester predicts 75% of firms will face moderate-to-severe technical debt from AI-generated code by 2026.

### 3.3 The Audit Standard as Implicit Prompt

Our most unexpected finding (Case 02, Section 6.2): when an AI encounters quality specifications in its context — even without being explicitly instructed to follow them — it **self-corrects**. In our experiment, Claude proactively switched from `os.path` (legacy API flagged as Technical Lag) to `pathlib` (modern API) after being exposed to `sts_checker.py`'s audit criteria, despite the user's refactoring instructions never mentioning `pathlib`.

This suggests that **the existence of a quality standard in the development environment functions as an implicit architectural constraint on AI behavior** — a form of governance that operates through context rather than command.

---

## 4. The Bottleneck: How to "Weigh" the Board

The Circuit Board model requires an objective, automatable "board capacity declaration." Prior art falls short:

| Approach | What It Does | What It Lacks |
|----------|-------------|---------------|
| **COCOMO II** | Prices by lines of code | Obsolete in modern development; doesn't measure architecture quality |
| **Function Point Analysis** (ISO/IEC 20926) | Prices by "function" | Ignores architecture quality — same search feature costs the same whether code is clean or spaghetti → adverse selection |
| **Clean Architecture** (Martin, 2017) | Defines layering principles | Doesn't talk about money — "expensive faith" that architects can't sell to clients |
| **Evolutionary Fitness Functions** (Ford & Parsons, 2017) | Automated architecture health checks | Doesn't connect to money or AI |
| **Technical Debt Economics** (Kruchten et al.) | Coupling → maintenance cost quantification | Doesn't address AI diffusion behavior or contractualization |
| **AI Code Quality Research** (2024-2026) | Documents LLM code quality issues | Stops at "finding problems," doesn't connect to contracts |

**What is missing:** A system that takes static code metrics, produces a deterministic quality tier, and maps that tier to enforceable contract terms — with the entire chain automated and CI-integrated.

---

## 5. Related Work and Competitive Positioning

We position STS against the closest existing approaches honestly:

| Dimension | SonarQube | CAST / Highlight | SIG (Software Improvement Group) | ISO 5055 | **STS / SAMA-Arch** |
|:---|:---|:---|:---|:---|:---|
| **Core paradigm** | Advisory (graded A–E) | Health scoring (R/O/G) | Star rating (1–5) | Standard definition | **Contractual (pass/fail tier)** |
| **Contract integration** | No | Used in some gov't contracts | Used in PE due diligence | Says "can be written into contracts" | **Defines how: tier → clause → breach** |
| **AI-awareness** | Post-hoc scan | Post-hoc scan | Post-hoc scan | Not AI-specific | **Designed for AI-generated artifacts** |
| **Layer purity (ADF)** | — | — | — | — | **Density-based violation detection** |
| **Stability (CCR)** | — | — | — | — | **Git-integrated churn analysis** |
| **Benchmark data** | Large | Large | **400B+ lines, 30K systems** | N/A | Small (28-file corpus) |
| **Pricing model** | No | No | Maintenance cost correlation | Recommends, doesn't define | **Board tier → contract clause** |

**Our honest position:** SIG has the data moat (400 billion lines benchmarked). CAST has government contract penetration. ISO 5055 has institutional authority. Our advantage is narrow but specific: (1) we are the first to define the complete chain from automated metric → quality tier → contract clause → breach determination, (2) we are purpose-built for AI-generated Python artifacts, and (3) we provide a working, CI-integrated auditor tool.

ISO 5055 says code quality metrics "*can* be written into contracts." STS defines *how*.

---

## 6. The Tool: STS Architectural Stress Meter (sts_checker.py v2.2)

### 6.1 Four Measurement Dimensions

**Cyclomatic Complexity (CC):** Number of independent paths through a module's control flow. Measures branching complexity. Computed via `radon`.

**Architectural Drift Factor (ADF):** Density of layer violations — I/O artifacts (e.g., `print()`, `logging.*`) in business logic layers. Computed as violation density:

$$ADF = \frac{\text{Count(Illegal Patterns)}}{\text{Total Lines of Code}}$$

**Technical Lag (TL):** Heuristic identification of deprecated or non-standard library usage (e.g., `os.path` where `pathlib` is standard).

**Code Churn Rate (CCR):** Git-based analysis of change frequency relative to module lifecycle. High churn correlates with architectural instability.

### 6.2 Verdict Logic

**Per-file verdict:**
- **FAILED (H-TIER)** if: `max_cc > cc_threshold` OR `adf > adf_threshold` OR `ccr > ccr_threshold`
- **PASSED (Z-TIER)** otherwise

**Project-level verdict (SAMA-Arch v2.2):**
$$Verdict_{Z} \iff (Max\_CC < cc\_project) \land (Max\_ADF < adf\_threshold) \land (TL = LOW) \land (Max\_CCR \leq ccr\_threshold)$$

Binary output with CI exit code 1 on FAILED — designed for pipeline integration.

### 6.3 Externalized Configuration

All thresholds are configurable via `.sts.toml`, enabling domain-specific tuning. A medical context might set `cc_threshold=15` for safety-critical code; a prototype context might relax to `cc_threshold=30`.

---

## 7. Experimental Evidence

### 7.1 Case 01 — Controlled Comparison (Bookstore System)

**Setup:** Same AI (Claude), same functional requirements, same prompt → simultaneously produced H-Tier and Z-Tier variants.

| Variant | Max CC | ADF | TL | Verdict |
|---------|--------|-----|-----|---------|
| H_v1_mono.py | 17 | 0.20 | HIGH | **FAILED** |
| Z_v2_split/service.py | 4 | 0.00 | HIGH | **PASSED** |

**Pressure test:** Same requirement change applied to both variants.

| Metric | H-Tier (before → after) | Z-Tier (before → after) |
|--------|------------------------|-----------------------|
| Max CC | 17 → 23 (+35%) | 4 → 9 (stable) |
| Verdict | FAILED → FAILED (degraded) | PASSED → PASSED (stable) |

**Finding:** Architecture quality is not bounded by AI capability, but by **prompt constraint strength**. The H→Z refactoring reduced Halstead Effort by 60% — not by reducing code volume (the Z version is larger), but by redistributing cognitive complexity so each module bears only one dimension.

### 7.2 Case 02 — Zero-Guidance Entropy (Mall Settlement System)

**Setup:** Constraint-free prompt: "Write a simple checkout system that supports membership and discounts." No mention of design patterns, layering, or quality standards.

**Result:** AI defaulted to H-Tier. Single `ShoppingCart` class with three responsibilities. `checkout()` method contained both business logic and UI output. 88 lines, functionally correct, architecturally doomed.

**AI self-diagnosis:** When shown the STS framework, Claude analyzed its own code: "My generation strategy favored minimizing class count, minimizing indirection, and minimizing line count. These tendencies led to ADF=0.20 and business layer polluted with UI."

**The implicit prompt discovery:** During refactoring, after being exposed to `sts_checker.py`'s criteria, Claude proactively switched from `os.path` → `pathlib` without being instructed to. The user's refactoring instructions never mentioned `pathlib` or Technical Lag. **The audit standard itself functioned as a behavioral constraint on the AI.**

| Phase | File Path API | TL Verdict | Trigger |
|-------|--------------|------------|---------|
| Zero-guidance | `os.path` | HIGH | AI default |
| After exposure to sts_checker | `pathlib` | LOW | AI proactively adapted |

### 7.3 Case 03 — Real-World Validation (Medical EEG System, 28 files)

**Setup:** v2.2 engine stress-tested against a research-grade Python codebase for Infant Spasm EEG Monitoring — a real system being developed for clinical deployment.

| Metric | Value | Verdict |
|--------|-------|---------|
| Global Pass Rate | 57.1% (16/28) | FAILED |
| Project Max CC | 36 (`src/inference.py`) | CRITICAL |
| Project Max ADF | 0.1391 (`scripts/evaluate.py`) | FAILURE |
| Technical Lag | HIGH (`os.path` in `src/data/channels.py`) | FAILURE |
| Mean CCR | 8.57% | PASSED |
| Max CCR | 30.00% (`scripts/aggregate.py`) | AT THRESHOLD |

**Key findings:**

1. **Threshold calibration from real data:** At `adf_threshold=0.05`, 18/28 files have non-zero ADF but only 10/28 exceed the threshold (35.7% flag rate). The threshold correctly filters incidental logging while flagging systemic layer violations. This represents the **Precision-Recall elbow** — tightening further produces false positives on legitimate utility scripts; loosening misses genuine architectural risks.

2. **CCR-complexity correlation:** `scripts/aggregate.py` (CCR=30%) correlates with (CC=24). This provides early evidence that **churn and complexity are co-indicators of architectural stress** — files that change frequently tend to be the ones with the most tangled logic.

3. **Clinical implication:** The engine successfully isolated `src/inference.py` (CC=36) as a major risk factor, recommending mandatory refactoring before clinical deployment. In a medical context, this is not an advisory — it is a safety gate.

---

## 8. From Metrics to Contracts: The Core Mechanism

The central contribution of STS is the **bridge** from engineering measurement to commercial enforcement.

### 8.1 The Economic Transformation

In economics, goods are classified by how quality can be verified:

- **Search goods:** Quality verifiable before purchase (e.g., furniture — you can see and touch it).
- **Experience goods:** Quality verifiable after purchase (e.g., a restaurant meal — you know after eating).
- **Credence goods:** Quality **not verifiable even after purchase** (e.g., car repair — you can't tell if the mechanic actually replaced the part).

Software architecture has been a **credence good**. A working application tells you nothing about the quality of the code behind it. Two systems can behave identically while one is clean and the other is a maintenance time bomb. The buyer has no way to verify which they received.

STS converts software into an **inspection good** — quality is deterministically verifiable by running `sts_checker.py` against the deliverable. The verdict is binary (PASSED/FAILED), reproducible, and automatable. This resolves the information asymmetry that drives adverse selection.

### 8.2 Contract Clause Mapping

| STS Metric | Threshold | Contract Clause |
|------------|-----------|----------------|
| CC > project threshold | Board capacity exceeded | Triggers mandatory refactoring window; cost allocated per tier agreement |
| ADF > threshold | Layer integrity violated | Delivery rejected; rework at developer's cost |
| CCR > threshold | Stability insufficient | Extended warranty / monitoring period required |
| TL = HIGH | Technical lag detected | Modernization clause activated |

The language shifts from subjective negotiation to engineering determination:

- **Old:** "It's expensive because I'm a senior developer." (Client: "I don't believe you.")
- **New:** "You signed for H-Level board, rated for CC < 20. Current CC = 36. Per Section 4.2, this triggers the refactoring clause. This is a breach, not a modification."

### 8.3 The LEED Analogy

This model mirrors how LEED (Leadership in Energy and Environmental Design) transformed the construction industry. Before LEED, "green building" was a subjective marketing claim. After LEED, it became a verifiable certification tier (Certified / Silver / Gold / Platinum) that commanded pricing premiums, was written into government procurement requirements, and created a market for green building practices.

STS aims to be **LEED for code architecture** — a verifiable certification that outsourcing contracts require, insurance underwriters reference, and quality-conscious development teams adopt.

---

## 9. Generalization: Beyond Software

### 9.1 The Common Structure

The "credence good → inspection good" conversion via automated metrics is not software-specific. It applies wherever:

1. Quality is invisible to the buyer
2. Quality can be measured by automated metrics
3. Quality affects downstream costs (maintenance, liability, failure risk)
4. Information asymmetry drives adverse selection

### 9.2 Medical Data Quality: The Natural Second Domain

Medical data for AI training (EHR records, imaging datasets, EEG signals, annotated training sets) suffers from the identical credence good problem. A hospital purchasing an annotated dataset, or a regulator evaluating an AI model's training data, cannot verify data quality from the outside.

**The structural parallel is exact:**

| Dimension | Software (STS) | Medical Data (Proposed) |
|-----------|----------------|-------------------------|
| Quality dimensions | CC, ADF, CCR, TL | Completeness, annotation agreement (Cohen's kappa), signal-to-noise ratio, consistency |
| Automated measurement | `radon`, `sts_checker.py` | OHDSI DQD, Great Expectations, custom checkers |
| Tiered verdict | H-TIER / Z-TIER | Quality tiers with automated scoring |
| Contract enforcement | "CC > 20 = breach" | "Annotation kappa < 0.6 = breach" |
| Regulatory driver | Voluntary | **EU AI Act Article 10 — mandatory by August 2027** |

The components already exist in fragments:

- **METRIC framework** (Schwabe et al., 2024, npj Digital Medicine): 15 data quality dimensions for medical ML training data
- **ISO/IEC 5259 series** (2024-2025): Process standard for AI data quality management; first third-party certification (SGS, November 2025)
- **OHDSI Data Quality Dashboard**: ~4,000 automated checks for EHR data

**What does not exist:** A system that takes these metrics, produces a tiered verdict, and maps that tier to enforceable contract terms with pricing consequences. This is the exact gap STS fills for software — and the same architecture could fill it for medical data.

Case 03 (Medical EEG System) is already the bridge: it is medical software audited by STS. The extension from auditing medical software to auditing medical data is a natural next step.

### 9.3 Honest Difficulties with the Medical Extension

1. **Heterogeneity:** EHR, DICOM imaging, EEG signals, and annotated pathology sets have radically different quality dimensions. A unified scorer is harder than in software.
2. **Ground truth:** In code, CC is objective. In medical data, "accuracy" often requires domain expertise or reference standards that may not exist.
3. **Privacy:** Auditing data quality requires inspecting the data, which creates HIPAA/GDPR compliance burden.
4. **Goodhart's Law:** Once metrics determine price, producers will optimize for the metric rather than actual quality.

---

## 10. Vision: Software Insurance

### 10.1 The Actuarial Infrastructure

Building insurance relies on measurable stress parameters: foundation depth, seismic rating, fire resistance class. These parameters are inspectable, tiered, and directly mapped to premium calculations.

Software has lacked equivalent actuarial infrastructure. STS provides it: architecture tier (H/Z), entropy values (CC, ADF), stability indicators (CCR), and modernization status (TL). These are the missing "seismic ratings" for software.

### 10.2 Honest Difficulties

Three problems must be solved before software insurance becomes viable:

1. **Actuarial gap:** There is no standardized database mapping "architecture quality → system failure probability." Building this database requires large-scale longitudinal data — correlating STS scores at delivery time with actual maintenance costs and failure rates over years. SIG's 400 billion-line benchmark is the closest thing that exists, but it belongs to a competitor.

2. **Moral hazard:** If software is insured against maintenance cost overruns, developers might intentionally write lower-quality code (the insurer absorbs the cost). Traditional insurance handles this via deductibles and co-pays; software insurance would need equivalent mechanisms.

3. **Non-stationarity:** Software environments change fast. An OS update can invalidate architectural assumptions. Unlike buildings (which face stable physics), software faces a moving target. Policies would need re-evaluation triggers tied to environment changes.

---

## 11. Limitations

- **ADF detection is regex-based.** Phase 2 will transition to AST-based analysis for scope-aware detection (distinguishing `print()` in a test method from `print()` in business logic). This is a precision upgrade, not a paradigm shift — the policy model remains identical.
- **Python-only implementation.** Python is the inaugural domain. The policy model (`.sts.toml` thresholds, tier verdicts, CI exit codes) is language-agnostic; implementations for other languages require only new metric extractors.
- **Small calibration corpus.** Thresholds are calibrated against one 28-file medical EEG corpus plus two controlled experiments. Larger-scale calibration across diverse codebases is needed.
- **The metrics-to-pricing mapping function is not yet established.** We demonstrate that metrics can produce contract-relevant verdicts, but the actual dollar-value mapping (e.g., "each CC point above threshold = X% cost increase") requires actuarial data we do not yet have.
- **B-Tier** (Business level) from the original Circuit Board model is not yet implemented in the tool — only H/Z binary classification exists.
- **Legal enforceability is untested.** No court has enforced a software contract based on static analysis metrics. The framework is logically sound but legally unprecedented.

---

## 12. References

*Only verifiable sources are cited. Research directions mentioned without specific titles reflect active areas of investigation, not specific papers.*

### Standards and Reports

- CISQ/NIST. *The Cost of Poor Software Quality in the US: A 2022 Report.* Consortium for Information & Software Quality, 2022. [$2.41 trillion estimated annual cost]
- ISO/IEC 5055:2021. *Information Technology — Software Quality — Software Quality Measures.* [Automated source code quality measures for reliability, security, performance efficiency, and maintainability]
- ISO/IEC 20926:2009. *Software and systems engineering — Software measurement — IFPUG functional size measurement method.* [Function Point Analysis]
- ISO/IEC 5259 series (2024-2025). *Artificial Intelligence — Data Quality for Analytics and Machine Learning.* [Parts 1-5: terminology, measures, management requirements, process framework, governance]

### Books

- Ford, N. & Parsons, R. *Building Evolutionary Architectures: Automated Software Governance.* O'Reilly Media, 2017 (2nd ed. 2023). [Fitness functions for architecture governance]
- Martin, R.C. *Clean Architecture: A Craftsman's Guide to Software Structure and Design.* Prentice Hall, 2017. [Layering principles, dependency rule]
- Boehm, B.W. et al. *Software Cost Estimation with COCOMO II.* Prentice Hall, 2000. [Lines-of-code based estimation model]

### Industry and Research

- Software Improvement Group (SIG). *TUViT Evaluation Criteria for Trusted Product Maintainability.* [1-5 star rating benchmarked against 400B+ lines; used in PE due diligence]
- Schwabe, D. et al. "A systematic assessment of data quality dimensions for machine learning in medicine." *npj Digital Medicine* 7, 2024. [METRIC framework: 15 data quality dimensions]
- SGS. "World's First ISO/IEC 5259-3 Certification for AI Data Quality Management." Press release, November 2025.
- Kruchten, P., Nord, R.L., & Ozkaya, I. *Managing Technical Debt: Reducing Friction in Software Development.* Addison-Wesley, 2019. [Technical debt quantification and economic modeling]

### Tools Referenced

- `radon`: Python library for code metrics (CC, MI, Halstead). [https://radon.readthedocs.io/]
- OHDSI Data Quality Dashboard: ~4,000 automated checks for OMOP Common Data Model. [https://ohdsi.github.io/DataQualityDashboard/]
- Great Expectations: Python framework for data quality assertions. [https://greatexpectations.io/]

---

*This proposal and the associated `sts_checker.py` are part of an ongoing research initiative. The project repository, including all case files, audit tool, and experimental evidence, is available for review.*
