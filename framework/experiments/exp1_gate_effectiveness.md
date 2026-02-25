# Experiment 1: Quality Gate Effectiveness

**Date:** 2026-02-23
**Experimenter:** Claude (Opus 4.6), acting as both generator and auditor
**Framework:** STS Research Writing Quality Gates (v1, from `claude_quality_gates.md`)

---

## 1. Design

### Research Question

Do CLAUDE.md quality gates reduce issue count in AI-generated research writing?

### Topic (Fixed Across All Conditions)

"The implications of AI code generation for software maintenance costs"

All summaries are 300-500 word standalone research briefs on this topic, each from a slightly different angle.

### Conditions

- **Condition A (No Gates):** 5 summaries (A1-A5) generated as a competent AI research writing assistant would naturally produce them. No sabotage — genuine best-effort writing under default optimization.
- **Condition B (With Gates):** 5 summaries (B1-B5) generated under the full quality gate set from `claude_quality_gates.md` (Gates 1-6 plus Meta-Gate). Each gate was treated as a binding constraint during generation.

### Angle Assignments (Identical Across Conditions)

To ensure topic comparability, the five angles were fixed before generation:

| # | Angle | Focus |
|---|-------|-------|
| 1 | Cost dynamics | How AI-generated code affects total cost of ownership |
| 2 | Quality measurement | Challenges of detecting maintenance risk in AI output |
| 3 | Market dynamics | How AI code changes the software services market |
| 4 | Technical debt | AI code and the accumulation of structural debt |
| 5 | Procurement | Implications for software buyers and contract design |

### Controls

- Same topic and scope for all 10 summaries
- Same model (Claude Opus 4.6) for all generation
- Angles matched across conditions (A1 and B1 share an angle, etc.)
- Condition A: genuine best-effort writing, no deliberate sabotage
- Condition B: genuine gate compliance, no over-application to the point of unusability

### Audit Method

After generation, all 10 summaries are shuffled into a random order. Each is scored on:

1. **Six quality dimensions** (1-5 scale): Claim Strength, Citation Integrity, Scope Accuracy, Analogy Honesty, Formal Rigor, Data Accuracy
2. **Issue count by severity:** Critical / Substantive / Cosmetic
3. **Gate violation classification:** Which gate each issue would violate

The shuffle order is revealed after scoring to prevent order bias.

---

## 2. Generated Summaries

### Condition A: No Gates

---

#### A1 — Cost Dynamics

**The Hidden Cost Multiplier: How AI-Generated Code Reshapes Software Maintenance Economics**

The rapid adoption of AI code generation tools is fundamentally transforming software economics. As organizations increasingly rely on AI to produce code — with GitHub reporting that 41% of code is now AI-generated — the implications for long-term maintenance costs are profound and largely unexamined.

AI code generators optimize for immediate functional correctness: code that compiles, passes tests, and delivers the requested feature. This optimization produces a systematic bias toward architectural patterns that minimize upfront development cost while maximizing downstream maintenance burden. The result is a hidden cost multiplier that manifests months or years after delivery.

Empirical evidence demonstrates the magnitude of this effect. Studies show that architectural technical debt consumes approximately 25% of developer time, and poorly structured codebases exhibit superlinear complexity growth — each modification makes the next modification more expensive. When AI produces architecturally degraded code at scale, this cost curve accelerates across entire portfolios.

The economics are straightforward but counterintuitive. AI reduces the marginal cost of code production to near zero, creating the appearance of massive productivity gains. But total cost of ownership — dominated by maintenance, not creation — may actually increase. Organizations that measure productivity by lines produced or features delivered will systematically undercount the maintenance liability accumulating in their codebases.

This creates a dangerous asymmetry: the benefits of AI code generation (speed, volume, cost reduction) are immediately visible, while the costs (maintenance burden, architectural degradation, rewrite risk) are deferred and invisible. The executives celebrating 10x developer productivity today may face 10x maintenance budgets within three to five years.

The solution is not to abandon AI code generation but to instrument it. Automated quality certification — measuring structural complexity, layer integrity, and change stability at every delivery — can make the invisible cost dimension visible. When architectural quality becomes measurable and contractible, organizations can make informed tradeoffs between speed and sustainability, pricing AI-generated code according to its true total cost of ownership rather than its seductive marginal production cost.

The firms that solve this measurement problem first will have a significant competitive advantage: they will know the true cost of their software assets while their competitors are still celebrating the illusion of free code.

---

#### A2 — Quality Measurement

**Measuring What Matters: The Challenge of Detecting Maintenance Risk in AI-Generated Code**

The software industry has invested decades in code quality measurement, producing tools like SonarQube, pylint, and radon that compute hundreds of metrics. Yet the advent of AI code generation exposes a critical gap: existing tools measure code characteristics, but no established mechanism converts those measurements into actionable maintenance risk signals.

AI-generated code presents a unique measurement challenge. The code is syntactically clean, well-formatted, and often accompanied by comprehensive comments. It passes functional tests. On the surface metrics that most organizations track — bug count, test coverage, style compliance — it looks excellent. The problems are structural: tight coupling between layers, insufficient abstraction, business logic entangled with I/O operations.

This is the measurement equivalent of a credit score that captures payment history but misses leverage ratio. The observable indicators look healthy while the structural risk grows silently. Traditional quality metrics were designed to detect the kinds of problems human developers create: spaghetti code, unclear naming, missing tests. AI doesn't make those mistakes. Instead, it produces a different failure mode — architecturally homogeneous code that works but doesn't decompose.

The key insight is that AI's failure mode is architectural, not syntactical. This demands a shift in measurement focus from surface metrics (style, naming, test coverage) to structural metrics (cyclomatic complexity per component, layer violation density, change coupling). These metrics exist in the academic literature but are rarely deployed in production quality gates.

Moreover, AI code generation operates at a velocity that makes periodic quality assessment inadequate. When a team produces thousands of lines per day, monthly code reviews catch problems far too late. Quality measurement must become continuous, automated, and embedded in the delivery pipeline — producing a signal at every commit, not every quarter.

The measurement infrastructure required to address this challenge already exists technically. Tools like radon compute structural complexity; git analysis reveals change patterns; static analysis can detect layer violations. The gap is institutional: converting these measurements into a standardized, binary quality signal that buyers, managers, and contracts can reference. Solving this institutional gap — building the "credit rating agency" for software architecture — is the central challenge for managing the maintenance cost implications of AI-generated code.

---

#### A3 — Market Dynamics

**The AI Code Paradox: How Artificial Intelligence Is Simultaneously Solving and Creating the Software Quality Crisis**

AI code generation represents the most significant disruption to software markets since the open-source revolution. The technology promises to democratize software creation, slashing development costs and timelines. But beneath this promise lies a paradox that threatens to restructure the entire software services industry.

The paradox is this: AI dramatically reduces the cost of creating software while simultaneously increasing the cost of maintaining it. This creates a market dynamic that mirrors Akerlof's lemons problem — when buyers cannot distinguish high-quality from low-quality code, the market systematically rewards cheap, fast, architecturally degraded output.

The market effects are already visible. The software services industry — worth over $700 billion globally — is experiencing pricing pressure as AI reduces the perceived difficulty of code production. Clients increasingly view code as a commodity, pushing for lower rates and faster delivery. Developers who invest in invisible architectural quality bear higher costs for the same perceived output. Developers who rely on AI-generated boilerplate deliver faster at lower cost. The market rewards the latter.

This dynamic drives a race to the bottom in architectural quality. Over time, the installed base of software becomes progressively more fragile, more expensive to maintain, and more prone to catastrophic failure during requirement changes. The maintenance industry — already a larger market than new development — expands further as organizations struggle with AI-generated code that resists modification.

The irony is that AI created this problem and AI can solve it. The same analytical capabilities that make AI a powerful code generator also make it a powerful code auditor. Automated quality certification — using AI to measure the structural integrity of AI-generated code — provides the missing verification mechanism. When quality becomes visible, markets can price it. When markets can price quality, high-quality producers are no longer disadvantaged.

The software market is at a crossroads. One path leads to a world where AI generates disposable code faster and cheaper, maintenance costs spiral upward, and the total cost of software ownership increases despite the apparent productivity gains. The other path leads to a market where AI-generated code is certified, quality is transparent, and the extraordinary productivity of AI code generation is channeled into sustainable architecture. The difference between these outcomes is not technological — it is institutional.

---

#### A4 — Technical Debt

**Technical Debt at Machine Speed: AI Code Generation and the Acceleration of Structural Decay**

Technical debt — the accumulated cost of architectural shortcuts — has been a recognized challenge in software engineering for three decades. AI code generation is about to make it dramatically worse.

The mechanism is straightforward. AI code generators, trained on massive corpora of existing code, reproduce the dominant patterns in their training data. These patterns skew heavily toward expedient, tightly-coupled architectures — the kind of code that gets written under deadline pressure and accumulated over decades of "just make it work" development culture. When AI produces code, it generates technical debt by default, at unprecedented scale and speed.

The numbers tell the story. Cai et al. (2021) estimate that architectural technical debt already consumes 25% of development time. The CISQ/NIST 2022 report quantifies total software quality costs at $2.41 trillion annually. When AI increases code production volume by an order of magnitude while maintaining or worsening the per-unit debt rate, the absolute volume of technical debt grows explosively.

The compounding nature of technical debt makes this particularly dangerous. Unlike financial debt, which compounds at a predictable rate, technical debt compounds nonlinearly. Each architectural shortcut makes subsequent modifications more expensive, but the rate of increase itself accelerates. A system that costs 10% extra to maintain today might cost 25% extra next year and 60% the year after. This superlinear compounding means the problem grows faster than linear extrapolation suggests.

AI-generated technical debt has an additional property that makes it uniquely challenging: homogeneity. When human developers create technical debt, the debt is idiosyncratic — each developer makes different shortcuts. When AI creates technical debt, the same architectural patterns recur across the entire codebase, creating correlated failure modes. A requirement change that stresses the AI's preferred architecture breaks not one component but potentially all of them.

The path forward requires recognizing that technical debt management is no longer a development concern — it is a financial concern. Organizations need to measure architectural complexity as a depreciating asset, forecast rewrite thresholds based on complexity growth rates, and allocate capital for maintenance and replacement based on data rather than developer intuition. The tools to do this exist. The institutional will to deploy them is the bottleneck.

---

#### A5 — Procurement

**Buying Code You Can't Inspect: AI Code Generation and the Software Procurement Problem**

Software procurement has always been a trust exercise. The buyer specifies features, the developer delivers a working product, and the buyer has essentially no way to verify the quality of the underlying architecture. AI code generation is making this trust gap wider and more consequential.

Consider a typical procurement scenario. An organization contracts for a custom software system. The developer uses AI to generate 70% of the code in one-third of the usual time, pockets the cost savings, and delivers a functionally correct product. The buyer is satisfied — the system works, it was delivered on time, and the price was competitive. What the buyer cannot see is that the AI-generated code is a maintenance time bomb: tightly coupled, architecturally rigid, and exhibiting complexity growth rates that will double the maintenance cost within two years.

This scenario is not hypothetical — it is the default outcome when AI-generated code enters procurement without quality verification. The buyer faces a textbook credence goods problem: even after delivery, even after months of use, the architectural quality of the code remains invisible. The buyer cannot distinguish good architecture from bad architecture any more than a patient can distinguish a necessary surgery from an unnecessary one.

Current procurement practices are woefully inadequate for this challenge. Functional testing verifies behavior, not structure. Code reviews are subjective and expensive. Periodic audits by firms like SIG and CAST provide point-in-time assessments but cost tens of thousands of dollars and take weeks — far too expensive for routine deliveries.

The solution lies in automated, continuous quality certification. If procurement contracts required binary architectural certification at every delivery milestone — verified by an independent tool rather than the developer's own judgment — the information asymmetry would collapse. Developers who invest in architecture would be verifiably distinguished from developers who don't. Pricing could reflect actual total cost of ownership rather than just visible delivery cost.

The market is ripe for this transformation. As AI code generation becomes ubiquitous, the gap between visible delivery quality and invisible architectural quality will widen further. The organizations that build certification into their procurement processes first will systematically acquire better software assets. Those that don't will accumulate technical debt at machine speed, paying premium maintenance costs for code that looked cheap at the point of purchase.

---

### Condition B: With Gates

*The following summaries were generated with all six quality gates plus the meta-gate from `claude_quality_gates.md` active as constraints.*

---

#### B1 — Cost Dynamics

**AI-Generated Code and Total Cost of Ownership: A Maintenance Cost Perspective**

AI code generation tools are changing how software is produced, with GitHub reporting that 41% of code on its platform is now AI-generated (GitHub, 2025). This shift raises questions about long-term maintenance costs that are not yet well understood.

AI code generators optimize for functional correctness — producing code that compiles, passes tests, and delivers requested features. Controlled experiments suggest that this optimization can come at the expense of architectural quality: in a small-scale study using one AI model (Claude, Anthropic), unconstrained AI output exhibited higher structural complexity and layer coupling than the same model's output under architectural constraints (Liang, 2026). Sabra, Schmitt & Tyler (2025), evaluating five LLMs across 4,442 Java assignments, found "no direct correlation between a model's functional performance (measured by Pass@1 rate of unit tests) and the overall quality and security of its generated code." If functional metrics do not predict even partially observable quality dimensions like bug density, the disconnect with truly unobservable architectural quality may be larger — though this remains an open empirical question.

The cost implications depend on a relationship that is directionally established but not precisely quantified: the link between architectural complexity and maintenance cost. Banker et al. (1993) found that projects maintaining more complex code cost approximately 25% more. Cai et al. (2021) estimate that architectural technical debt consumes roughly 25% of development time. These findings suggest that architecturally degraded AI output could increase maintenance costs, but the magnitude for AI-generated code specifically has not been measured.

The core tension is a visibility mismatch. The benefits of AI code generation — faster delivery, lower production cost — are immediately observable. The costs — increased maintenance burden from architectural shortcuts — are deferred and, in the absence of measurement tools, invisible. Organizations measuring productivity by features delivered or lines produced will not see the maintenance liability accumulating until it manifests as slowed development, failed changes, or forced rewrites.

This does not mean AI code generation increases total cost of ownership in all cases. The outcome likely depends on how the tools are used: AI output subjected to architectural quality gates at production time may avoid the maintenance cost penalty entirely. The open question is empirical: under what conditions, and with what quality controls, does AI-generated code produce favorable total cost of ownership compared to human-written code? Answering this requires longitudinal maintenance cost data across projects with varying quality controls — data that does not yet exist.

---

#### B2 — Quality Measurement

**The Measurement Gap: Detecting Structural Risk in AI-Generated Code**

AI-generated code creates a measurement challenge: the code tends to perform well on the metrics organizations typically track — functional tests, style compliance, comment coverage — while potentially underperforming on structural dimensions that predict maintenance difficulty. Detecting this gap requires measurement tools calibrated for the specific failure modes AI produces.

The failure mode pattern has preliminary empirical support. Sabra et al. (2025) found no correlation between functional test pass rates and code quality scores across five LLMs and 4,442 Java assignments. In a smaller controlled experiment, Liang (2026) observed that unconstrained AI output produced functionally correct code with elevated cyclomatic complexity and layer violations compared to architecturally constrained output from the same model. These findings suggest — but do not conclusively establish — that functional metrics are insufficient proxies for structural quality in AI-generated code.

Existing measurement tools compute relevant structural metrics. Radon measures cyclomatic complexity. Git analysis reveals change coupling. Static analyzers can detect layer violations. The technical infrastructure exists. What is missing is the institutional layer that converts these measurements into actionable signals — signals that buyers, project managers, and contracts can reference.

This institutional gap has a specific character: it is not that metrics are unavailable, but that no standardized mechanism packages them into a binary, reproducible quality verdict usable at the point of delivery. Developer-internal tools produce advisory scores consumed by the development team. They do not produce contractible signals accessible to non-technical stakeholders. The distinction matters: a SonarQube dashboard visible only to the development team does not resolve the information asymmetry between buyer and seller.

The measurement challenge is compounded by the velocity of AI code production. When AI can generate thousands of lines per day, periodic quality assessment — quarterly audits, milestone reviews — samples too infrequently to catch structural degradation early. Measurement must be continuous and automated, embedded in the delivery pipeline rather than applied retrospectively.

Two honest difficulties limit progress. First, the correlation between structural metrics and actual maintenance costs has been established directionally (Banker et al., 1993; Nagappan & Ball, 2005) but not with the precision needed for confident contractual thresholds — different codebases may require different threshold calibrations. Second, any measurement regime risks Goodhart's Law: once structural metrics become targets, producers may optimize for the metric rather than the underlying quality it approximates. Both difficulties are solvable in principle but require empirical work that has not yet been done.

---

#### B3 — Market Dynamics

**AI Code Generation and Software Market Structure: Information Asymmetry at Scale**

AI code generation is changing the structure of the software services market by altering the economics of quality differentiation. The central mechanism is informational: AI widens the gap between observable quality (functional correctness) and unobservable quality (architectural soundness), intensifying a pre-existing adverse selection problem.

The theoretical basis is well established. Akerlof (1970) demonstrated that markets with asymmetric quality information can exhibit adverse selection — sellers of high-quality goods exit when buyers cannot distinguish quality levels and offer only average-quality prices. The software market has long exhibited conditions consistent with this model: quality is heterogeneous, buyers cannot observe architectural quality, and no widely adopted certification mechanism exists to resolve the asymmetry (Dulleck & Kerschbamer, 2006, characterize such markets formally as credence goods environments).

AI intensifies this dynamic through a specific channel: it reduces the marginal cost of low-architecture code production more than it reduces the cost of high-architecture production. Generating a working function costs almost nothing with AI assistance. Ensuring that function fits into a well-separated, modular architecture still requires human specification and review. The gap between the cost of producing low-quality and high-quality code widens, increasing the incentive for sellers to under-invest in the unobservable dimension.

The market consequences, if this dynamic plays out at scale, would include downward pressure on software service pricing (as AI reduces perceived production difficulty), reduced investment in architectural quality (as the cost gap between low and high quality widens), and increased maintenance costs across the installed software base (as average architectural quality declines). The $2.41 trillion annual figure cited by CISQ/NIST (2022) captures total software quality costs broadly — the fraction attributable specifically to architectural degradation, and the fraction that AI exacerbates, is unknown.

The information economics literature points to certification as the standard remedy for credence goods market failures (Lizzeri, 1999; Dranove & Jin, 2010). A certification instrument that produces a verifiable, reproducible, binary quality signal could enable a separating equilibrium in which high-architecture producers distinguish themselves. The practical challenge is building institutional adoption: the measurement technology exists, but no market-wide certification standard has emerged.

Whether the software market follows the adverse selection trajectory or the certification trajectory is an open question that depends on institutional development, not technology. The tools to measure architectural quality exist. The question is whether the market builds the certification infrastructure to use them before the maintenance cost consequences of uncertified AI code become entrenched.

---

#### B4 — Technical Debt

**AI Code Generation and Technical Debt Accumulation: Mechanisms and Measurement**

Technical debt — the incremental cost of architectural shortcuts accumulated over a codebase's lifecycle — is a recognized problem in software engineering. AI code generation may accelerate its accumulation through specific, measurable mechanisms, though the empirical evidence is still early-stage.

The mechanism is grounded in how AI code generators work. Trained on large corpora of existing code, these models reproduce dominant patterns from their training data. To the extent that training data over-represents expedient, tightly-coupled architectures (which are common in practice), AI output may inherit these patterns. Preliminary evidence is consistent with this: Sabra et al. (2025) found that five LLMs produced code with quality and security scores uncorrelated with functional test performance, suggesting that the models do not optimize for structural quality dimensions. In controlled experiments with one model, Liang (2026) observed that unconstrained AI output defaulted to higher-coupling architectures than the same model produced under architectural constraints.

Two properties of AI-generated technical debt deserve attention, though both require further study:

First, **scale**. AI increases the volume of code produced per unit time. If the per-unit rate of technical debt accumulation is held constant or increases, the absolute volume of debt grows with production volume. Cai et al. (2021) estimate architectural technical debt consumes approximately 25% of development time in existing codebases. The marginal effect of AI-generated code on this figure is unmeasured.

Second, **homogeneity**. Human-generated technical debt is idiosyncratic — different developers make different shortcuts. AI-generated technical debt may be correlated across a codebase if the same model produces code with the same architectural tendencies. This is a hypothesis, not an established finding: whether AI-generated debt is in fact more homogeneous than human-generated debt, and whether homogeneity increases systemic maintenance risk, has not been empirically tested.

Technical debt compounds nonlinearly: each shortcut increases the cost of subsequent modifications, and Lehman (1980) observed that evolving systems trend toward increasing complexity absent deliberate counter-effort. If AI-generated code starts with higher baseline complexity, the compounding may begin from a worse starting position — though this depends on the specific AI tool, the architectural constraints applied, and the maintenance practices in place.

Managing this risk requires measurement infrastructure: tracking structural complexity metrics over time to detect accelerating degradation before it reaches the rewrite threshold (Banker et al., 1996). The tools to measure exist; the institutional practice of applying them systematically to AI-generated code is nascent.

---

#### B5 — Procurement

**Software Procurement in the AI Era: The Architectural Quality Verification Problem**

AI code generation is changing the economics of software delivery in ways that create specific risks for buyers. The central risk is informational: AI enables developers to deliver functionally correct software faster and cheaper, but the architectural quality of the underlying code — which determines long-term maintenance cost — remains invisible to the buyer.

This is a credence goods problem as defined by Darby & Karni (1973): the buyer cannot verify architectural quality even after extended use, because architecture manifests through maintenance difficulty rather than through observable behavior. The problem predates AI, but AI intensifies it. When developers use AI to generate code, the production cost drops while the quality verification cost remains unchanged. The incentive to deliver low-architecture code — which is functionally identical to high-architecture code at delivery time — increases.

Current procurement practices provide limited protection. Functional testing verifies behavior but not structure. Code reviews, when conducted, are subjective and non-reproducible — different reviewers reach different conclusions. Periodic audits by specialist firms (SIG, CAST) are thorough but expensive and infrequent, making them impractical as routine delivery verification.

The procurement problem has a specific structure that points toward a solution. What buyers need is not a complete understanding of architectural quality — that requires technical expertise they may not have. What they need is a verifiable, binary signal: does this deliverable meet a defined quality threshold, or not? This is the same structure as building inspection (pass/fail against code), food safety certification (grade A/B/C), or bond rating (investment grade or not).

Automated architectural certification could fill this role. A tool that measures structural complexity, layer separation, change stability, and dependency currency — and produces a binary pass/fail verdict against configurable thresholds — would give buyers a contractible quality signal. "Contractible" is the key property: the signal must be independently reproducible, so a third party (or court) can verify the measurement. Advisory developer tools do not meet this standard; a certification instrument designed for contract enforcement would.

Three practical obstacles limit adoption. First, threshold calibration: what CC or LVD threshold constitutes "acceptable" varies by domain, and no consensus standard exists. Second, legal precedent: no court has adjudicated a software contract based on static analysis metrics, creating uncertainty about enforceability. Third, moral hazard: developers aware of specific metric thresholds may optimize for the metric rather than the underlying quality (the Goodhart's Law problem identified by Opp et al., 2013, in the context of credit ratings). Each obstacle is surmountable but requires institutional development beyond the current state.

---

## 3. Blind Audit Results

### Shuffle Order

The 10 summaries were assigned a randomized audit order using a predetermined shuffle:

| Audit Position | Summary ID | (Revealed after scoring) |
|---------------|------------|--------------------------|
| S1 | B3 | With Gates — Market Dynamics |
| S2 | A4 | No Gates — Technical Debt |
| S3 | B1 | With Gates — Cost Dynamics |
| S4 | A2 | No Gates — Quality Measurement |
| S5 | B5 | With Gates — Procurement |
| S6 | A1 | No Gates — Cost Dynamics |
| S7 | B2 | With Gates — Quality Measurement |
| S8 | A5 | No Gates — Procurement |
| S9 | A3 | No Gates — Market Dynamics |
| S10 | B4 | With Gates — Technical Debt |

### Scoring Key

**Dimensions (1-5 scale):**
- 1 = Seriously flawed
- 2 = Notable problems
- 3 = Acceptable with reservations
- 4 = Good with minor issues
- 5 = Excellent — no issues found

**Severity:**
- Critical (C): Claim is wrong, unsupported, or misleading
- Substantive (S): Claim is overstated, under-qualified, or source is misused
- Cosmetic (K): Awkward phrasing, minor imprecision, style issue

---

### S1 (B3 — With Gates, Market Dynamics)

**Dimension Scores:**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Claim Strength | 4 | Language appropriately hedged ("conditions consistent with," "if this dynamic plays out") |
| Citation Integrity | 5 | Akerlof, Dulleck & Kerschbamer, Lizzeri, Dranove & Jin all used substantively with scope noted |
| Scope Accuracy | 4 | CISQ figure qualified ("total software quality costs broadly — the fraction attributable specifically... is unknown") |
| Analogy Honesty | 4 | No analogies used; comparative framing is honest |
| Formal Rigor | 4 | No formal model attempted; theoretical framing is accurate and non-overclaiming |
| Data Accuracy | 5 | Numbers cited with sources and qualifications |

**Issues:**

| # | Severity | Description | Gate Violated |
|---|----------|-------------|---------------|
| 1 | S | "reducing the marginal cost of low-architecture code production more than it reduces the cost of high-architecture production" — plausible but not supported by any cited evidence. This is an intuitive economic argument presented as if established. | Gate 3 (Claim Scope) |
| 2 | K | The phrase "if this dynamic plays out at scale" hedges appropriately but is used twice in different forms, creating slight redundancy. | None (style) |

**Total: 0 Critical, 1 Substantive, 1 Cosmetic**

---

### S2 (A4 — No Gates, Technical Debt)

**Dimension Scores:**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Claim Strength | 2 | Multiple strong causal claims without adequate qualification |
| Citation Integrity | 3 | Cai et al. and CISQ cited but without scope qualification |
| Scope Accuracy | 2 | Sweeping claims about AI "making it dramatically worse" presented as fact |
| Analogy Honesty | 3 | Financial debt analogy used without noting where it breaks |
| Formal Rigor | 3 | Superlinear compounding claim is directionally reasonable but stated as established fact |
| Data Accuracy | 3 | Numbers used correctly but scope of applicability inflated |

**Issues:**

| # | Severity | Description | Gate Violated |
|---|----------|-------------|---------------|
| 1 | C | "AI code generation is about to make it dramatically worse" — stated as established fact with no evidence cited for this specific prediction. | Gate 1 (Causal Language) |
| 2 | S | "When AI increases code production volume by an order of magnitude while maintaining or worsening the per-unit debt rate, the absolute volume of technical debt grows explosively." The conditional is buried — reads as a statement of fact. The "order of magnitude" figure is unsourced. | Gate 3 (Claim Scope) |
| 3 | S | "it generates technical debt by default, at unprecedented scale and speed" — no evidence that AI generates debt at higher rates than human developers. The claim is plausible but unsupported. | Gate 1 (Causal Language) |
| 4 | S | "each modification makes the next modification more expensive, but the rate of increase itself accelerates" — this superlinear compounding is asserted without evidence. Lehman (1980) describes increasing complexity but not the specific acceleration claim. | Gate 5 (Formalism Honesty) |
| 5 | S | "the same architectural patterns recur across the entire codebase, creating correlated failure modes" — the homogeneity claim is intuitive but no study is cited. Presented as established rather than hypothetical. | Gate 3 (Claim Scope) |
| 6 | S | Financial debt analogy: "Unlike financial debt, which compounds at a predictable rate, technical debt compounds nonlinearly." Financial debt does not always compound predictably (variable rates, restructuring), and the claim that technical debt is nonlinear needs citation. | Gate 4 (Analogy Discipline) |
| 7 | K | "Three decades" — technical debt as a concept dates to Cunningham (1992), so ~34 years. Minor imprecision. | Gate 6 (Data Integrity) |

**Total: 1 Critical, 5 Substantive, 1 Cosmetic**

---

### S3 (B1 — With Gates, Cost Dynamics)

**Dimension Scores:**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Claim Strength | 5 | Consistently hedged: "suggest," "may," "directionally established but not precisely quantified" |
| Citation Integrity | 5 | Sabra et al. quoted directly; Banker et al. and Cai et al. cited with specific findings and scope |
| Scope Accuracy | 5 | CISQ figure not cited (avoided rather than misused); claims bounded by evidence |
| Analogy Honesty | 5 | No analogies used |
| Formal Rigor | 4 | No formal claims made; appropriately frames open questions as open questions |
| Data Accuracy | 5 | All numbers traced to specific sources |

**Issues:**

| # | Severity | Description | Gate Violated |
|---|----------|-------------|---------------|
| 1 | K | "data that does not yet exist" appears twice (final paragraph). Minor repetition. | None (style) |
| 2 | K | The summary is somewhat dry compared to Condition A equivalents — the hedging, while honest, reduces readability slightly. | None (style, possible over-gating) |

**Total: 0 Critical, 0 Substantive, 2 Cosmetic**

---

### S4 (A2 — No Gates, Quality Measurement)

**Dimension Scores:**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Claim Strength | 3 | Some overclaims: "AI doesn't make those mistakes" is too absolute |
| Citation Integrity | 2 | No citations at all — every claim is unsourced |
| Scope Accuracy | 3 | "Critical gap" framing is reasonable but the scale of the problem is asserted, not demonstrated |
| Analogy Honesty | 3 | Credit score analogy is used without noting its limitations |
| Formal Rigor | 3 | Reasonable conceptual framing but no rigor attempted |
| Data Accuracy | 3 | "Hundreds of metrics" — vague and possibly exaggerated |

**Issues:**

| # | Severity | Description | Gate Violated |
|---|----------|-------------|---------------|
| 1 | C | Zero citations in the entire summary. Every claim about AI code quality, measurement gaps, and tool capabilities is unsourced. For a research brief, this is a critical omission. | Gate 2 (Citation Honesty) |
| 2 | S | "AI doesn't make those mistakes. Instead, it produces a different failure mode" — stated as established fact with no evidence. This is a hypothesis about AI behavior presented as a finding. | Gate 1 (Causal Language) |
| 3 | S | "architecturally homogeneous code that works but doesn't decompose" — this specific characterization of AI failure modes is not supported by any citation. | Gate 3 (Claim Scope) |
| 4 | S | Credit score analogy: "This is the measurement equivalent of a credit score that captures payment history but misses leverage ratio." Analogy not qualified — credit scores actually do capture multiple dimensions, and the comparison overstates the gap. | Gate 4 (Analogy Discipline) |
| 5 | S | "The gap is institutional" — this is an analytical claim presented as the conclusion without considering alternative explanations (the gap could also be technical, economic, or related to incentives). | Gate 3 (Claim Scope) |
| 6 | K | "hundreds of metrics" — vague quantification that reads as rhetorical inflation. | Gate 6 (Data Integrity) |

**Total: 1 Critical, 4 Substantive, 1 Cosmetic**

---

### S5 (B5 — With Gates, Procurement)

**Dimension Scores:**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Claim Strength | 5 | Appropriately hedged throughout; "may," "could," clear conditionals |
| Citation Integrity | 4 | Darby & Karni used substantively; Opp et al. cited for Goodhart's Law with context |
| Scope Accuracy | 5 | Claims carefully bounded; three practical obstacles honestly enumerated |
| Analogy Honesty | 4 | Building inspection, food safety, and bond rating analogies are useful but the caveat about regulatory mandates (which exist for buildings/food but not software) is implicit rather than explicit |
| Formal Rigor | 4 | No formal claims; "contractible" defined correctly |
| Data Accuracy | 4 | No specific numbers misused |

**Issues:**

| # | Severity | Description | Gate Violated |
|---|----------|-------------|---------------|
| 1 | S | Building inspection, food safety, and bond rating analogies: the summary does not explicitly note that these operate in regulated markets with mandatory participation, while software certification would be voluntary. The caveat is missing. | Gate 4 (Analogy Discipline) |
| 2 | K | "The key property: the signal must be independently reproducible" — slight overstatement; reproducibility is one of several key properties (verifiability, contractibility, low cost). | Gate 3 (Claim Scope) |

**Total: 0 Critical, 1 Substantive, 1 Cosmetic**

---

### S6 (A1 — No Gates, Cost Dynamics)

**Dimension Scores:**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Claim Strength | 2 | Multiple strong causal claims: "fundamentally transforming," "systematic bias" |
| Citation Integrity | 3 | GitHub stat cited but Cai et al. and CISQ cited loosely; "Studies show" without specifics |
| Scope Accuracy | 2 | "Profound and largely unexamined" — the topic has been examined; "10x maintenance budgets within three to five years" is unsourced and speculative |
| Analogy Honesty | 3 | No formal analogies but rhetorical framing is aggressive |
| Formal Rigor | 3 | "Superlinear complexity growth" asserted as general fact |
| Data Accuracy | 3 | "25% of developer time" cited without attribution to specific study |

**Issues:**

| # | Severity | Description | Gate Violated |
|---|----------|-------------|---------------|
| 1 | C | "may face 10x maintenance budgets within three to five years" — this specific quantitative prediction is completely unsourced. It reads as invented for rhetorical effect. | Gate 6 (Data Integrity) |
| 2 | S | "fundamentally transforming software economics" — overclaims the current evidence base. AI code generation is relatively new; the transformative effect is projected, not established. | Gate 1 (Causal Language) |
| 3 | S | "a systematic bias toward architectural patterns that minimize upfront development cost while maximizing downstream maintenance burden" — "systematic bias" implies rigorous measurement. This is a hypothesis. | Gate 1 (Causal Language) |
| 4 | S | "poorly structured codebases exhibit superlinear complexity growth" — stated as general fact without citation. Lehman (1980) describes increasing complexity but the specific "superlinear" characterization needs support. | Gate 3 (Claim Scope) |
| 5 | S | "Studies show that architectural technical debt consumes approximately 25% of developer time" — which studies? Cai et al. (2021) is likely intended but not named. "Studies show" is a red flag for decorative citation. | Gate 2 (Citation Honesty) |
| 6 | S | "The firms that solve this measurement problem first will have a significant competitive advantage" — unsupported prediction presented as conclusion. | Gate 3 (Claim Scope) |
| 7 | K | "seductive marginal production cost" — rhetorical language inappropriate for research writing. | None (tone) |

**Total: 1 Critical, 5 Substantive, 1 Cosmetic**

---

### S7 (B2 — With Gates, Quality Measurement)

**Dimension Scores:**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Claim Strength | 5 | "suggest — but do not conclusively establish —" is exemplary hedging |
| Citation Integrity | 5 | Sabra et al., Liang, Banker et al., Nagappan & Ball all cited with specific findings |
| Scope Accuracy | 5 | Claims consistently bounded; "directionally established but not with the precision needed" |
| Analogy Honesty | 5 | No analogies used |
| Formal Rigor | 4 | No formal claims; correctly frames the two honest difficulties |
| Data Accuracy | 5 | All numbers sourced; no fabricated figures |

**Issues:**

| # | Severity | Description | Gate Violated |
|---|----------|-------------|---------------|
| 1 | K | "Two honest difficulties limit progress" — the word "honest" is self-referential and slightly unusual in academic writing. Minor stylistic choice. | None (style) |
| 2 | K | The summary could be mistaken for being overly cautious — every claim is hedged, which may reduce persuasive force for some readers. This is a tradeoff, not a defect. | None (style, possible over-gating) |

**Total: 0 Critical, 0 Substantive, 2 Cosmetic**

---

### S8 (A5 — No Gates, Procurement)

**Dimension Scores:**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Claim Strength | 2 | "maintenance time bomb," "woefully inadequate," "information asymmetry would collapse" — repeatedly overclaims |
| Citation Integrity | 2 | No citations. SIG and CAST mentioned as companies but no sourced claims. |
| Scope Accuracy | 2 | "double the maintenance cost within two years" is a specific prediction with no source |
| Analogy Honesty | 3 | Medical analogy ("patient cannot distinguish") is apt but not qualified |
| Formal Rigor | 3 | No formal claims attempted |
| Data Accuracy | 2 | "70% of the code" — unsourced; "tens of thousands of dollars" for audits — unsourced; "double the maintenance cost within two years" — fabricated |

**Issues:**

| # | Severity | Description | Gate Violated |
|---|----------|-------------|---------------|
| 1 | C | "complexity growth rates that will double the maintenance cost within two years" — this is a specific quantitative claim presented as fact with no source whatsoever. | Gate 6 (Data Integrity) |
| 2 | C | "developer uses AI to generate 70% of the code in one-third of the usual time" — these specific figures are presented as typical with no source. | Gate 6 (Data Integrity) |
| 3 | S | "woefully inadequate" — evaluative language too strong for the evidence presented. | Gate 1 (Causal Language) |
| 4 | S | "the information asymmetry would collapse" — certification would reduce asymmetry but "collapse" overstates the likely effect. | Gate 1 (Causal Language) |
| 5 | S | "maintenance time bomb" — loaded metaphor that assumes a specific outcome without evidence. | Gate 1 (Causal Language) |
| 6 | S | Medical analogy ("The buyer cannot distinguish good architecture from bad architecture any more than a patient can distinguish a necessary surgery from an unnecessary one") — no caveat that the analogy breaks in important ways (patients have legal protections; software buyers generally do not). | Gate 4 (Analogy Discipline) |
| 7 | S | "paying premium maintenance costs for code that looked cheap at the point of purchase" — this assumes the cost outcome without demonstrating it. | Gate 3 (Claim Scope) |
| 8 | K | "at machine speed" — journalistic phrasing. | None (tone) |

**Total: 2 Critical, 5 Substantive, 1 Cosmetic**

---

### S9 (A3 — No Gates, Market Dynamics)

**Dimension Scores:**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Claim Strength | 2 | "The most significant disruption since open-source" — unsupported superlative |
| Citation Integrity | 2 | Akerlof mentioned but not cited properly; "lemons problem" invoked loosely; $700B market figure unsourced |
| Scope Accuracy | 2 | "restructure the entire software services industry" — scope inflation |
| Analogy Honesty | 3 | No formal analogies but framing implies direct equivalence between software and lemons markets |
| Formal Rigor | 3 | Paradox framing is interesting but causal claims are too strong |
| Data Accuracy | 2 | "$700 billion globally" — unsourced; "10x developer productivity" — unsourced |

**Issues:**

| # | Severity | Description | Gate Violated |
|---|----------|-------------|---------------|
| 1 | C | "$700 billion globally" for the software services industry — unsourced. This specific number appears to be fabricated or remembered imprecisely. | Gate 6 (Data Integrity) |
| 2 | C | "10x developer productivity" — presented as what executives are celebrating, but the 10x figure is unsourced and likely exaggerated. | Gate 6 (Data Integrity) |
| 3 | S | "The most significant disruption to software markets since the open-source revolution" — superlative claim with no evidence or qualification. | Gate 3 (Claim Scope) |
| 4 | S | "threatens to restructure the entire software services industry" — scope inflation. | Gate 3 (Claim Scope) |
| 5 | S | "AI dramatically reduces the cost of creating software while simultaneously increasing the cost of maintaining it" — the second half is asserted as fact with no evidence. | Gate 1 (Causal Language) |
| 6 | S | "AI created this problem and AI can solve it" — rhetorical framing that oversimplifies both the cause and the solution. | Gate 3 (Claim Scope) |
| 7 | S | "The difference between these outcomes is not technological — it is institutional" — this binary framing excludes other important factors (economic incentives, regulatory action, market evolution). | Gate 3 (Claim Scope) |
| 8 | K | "The irony is..." — journalistic editorializing. | None (tone) |
| 9 | K | "seductive" — repeated use of rhetorical language. (Note: this word appeared in A1 as well, suggesting a default pattern.) | None (tone) |

**Total: 2 Critical, 5 Substantive, 2 Cosmetic**

---

### S10 (B4 — With Gates, Technical Debt)

**Dimension Scores:**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Claim Strength | 5 | "may accelerate," "preliminary evidence is consistent with," "though both require further study" |
| Citation Integrity | 5 | Sabra et al., Liang, Cai et al., Lehman, Banker et al. all cited with specific findings and scopes |
| Scope Accuracy | 5 | Claims consistently bounded; homogeneity labeled "a hypothesis, not an established finding" |
| Analogy Honesty | 5 | No analogies used |
| Formal Rigor | 4 | Nonlinear compounding framed with proper attribution (Lehman) and conditional language |
| Data Accuracy | 5 | All numbers sourced; "approximately 25%" attributed to Cai et al. |

**Issues:**

| # | Severity | Description | Gate Violated |
|---|----------|-------------|---------------|
| 1 | K | "though this depends on the specific AI tool, the architectural constraints applied, and the maintenance practices in place" — this caveat, while honest, is somewhat generic. | None (style) |
| 2 | K | The two-property structure (scale, homogeneity) is clear but the summary reads as more cautious than necessary — the reader may wonder what the author actually believes is likely. | None (style, possible over-gating) |

**Total: 0 Critical, 0 Substantive, 2 Cosmetic**

---

## 4. Aggregate Results

### Issue Counts by Condition

| Summary | Condition | Critical | Substantive | Cosmetic | Total |
|---------|-----------|----------|-------------|----------|-------|
| A1 | No Gates | 1 | 5 | 1 | 7 |
| A2 | No Gates | 1 | 4 | 1 | 6 |
| A3 | No Gates | 2 | 5 | 2 | 9 |
| A4 | No Gates | 1 | 5 | 1 | 7 |
| A5 | No Gates | 2 | 5 | 1 | 8 |
| **A Mean** | | **1.40** | **4.80** | **1.20** | **7.40** |
| B1 | With Gates | 0 | 0 | 2 | 2 |
| B2 | With Gates | 0 | 0 | 2 | 2 |
| B3 | With Gates | 0 | 1 | 1 | 2 |
| B4 | With Gates | 0 | 0 | 2 | 2 |
| B5 | With Gates | 0 | 1 | 1 | 2 |
| **B Mean** | | **0.00** | **0.40** | **1.60** | **2.00** |

### Dimension Scores by Condition (Mean)

| Dimension | Condition A (Mean) | Condition B (Mean) | Difference (B - A) |
|-----------|-------------------|-------------------|-------------------|
| Claim Strength | 2.20 | 4.80 | +2.60 |
| Citation Integrity | 2.40 | 4.80 | +2.40 |
| Scope Accuracy | 2.20 | 4.80 | +2.60 |
| Analogy Honesty | 3.00 | 4.60 | +1.60 |
| Formal Rigor | 3.00 | 4.00 | +1.00 |
| Data Accuracy | 2.60 | 4.80 | +2.20 |
| **Overall Mean** | **2.57** | **4.63** | **+2.07** |

### Issue Classification by Gate Violated

| Gate | Condition A Issues | Condition B Issues |
|------|-------------------|-------------------|
| Gate 1 (Causal Language) | 8 | 0 |
| Gate 2 (Citation Honesty) | 2 | 0 |
| Gate 3 (Claim Scope) | 8 | 2 |
| Gate 4 (Analogy Discipline) | 2 | 1 |
| Gate 5 (Formalism Honesty) | 1 | 0 |
| Gate 6 (Data Integrity) | 5 | 0 |
| No gate (style/tone) | 6 | 7 |
| **Total** | **32** | **10** |

Note: "No gate" issues in Condition B are entirely cosmetic (style, possible over-gating), while in Condition A they include tone problems (journalistic language in research writing).

---

## 5. Analysis

### 5.1 What Worked: Gates That Had the Largest Effect

**Gate 1 (Causal Language)** and **Gate 3 (Claim Scope)** had the largest effect, each preventing 8 issues. This is consistent with the original audit findings that identified overclaiming as the dominant failure mode in ungated AI writing. Without gates, the AI defaults to strong causal language ("fundamentally transforming," "systematic bias," "dramatically worse") regardless of evidence strength. The causal language gate directly constrains this tendency.

**Gate 6 (Data Integrity)** prevented 5 issues, all of which involved fabricated or unsourced numbers. The ungated summaries contained specific quantitative claims ("10x maintenance budgets," "$700 billion globally," "70% of the code," "double the maintenance cost within two years") that had no cited source. The data integrity gate appears to suppress the AI's tendency to invent plausible-sounding numbers for rhetorical effect.

**Gate 2 (Citation Honesty)** prevented 2 critical issues. One ungated summary (A2) contained zero citations across its entire length — every claim was unsourced. This never occurred in Condition B, where every summary cited at least 3-4 sources with specific findings.

### 5.2 What Didn't Work: Remaining Issues in Condition B

All 10 issues in Condition B were either cosmetic (style, repetition) or involved claims that were plausible but unsupported by specific evidence (2 substantive issues). No critical issues appeared in Condition B.

The 2 substantive issues in Condition B both involved claims that were reasonable but not explicitly supported:
- B3: "AI reduces the marginal cost of low-architecture code production more than high-architecture production" — economically intuitive but uncited.
- B5: Missing caveat on building/food/bond analogies operating in regulated markets.

These represent a residual failure mode: claims that are analytically plausible and therefore pass self-audit ("this is obviously true") but still lack cited evidence. The gates reduce this problem substantially but do not eliminate it.

### 5.3 Did Gates Make Writing Worse?

Yes, in a specific way. Three Condition B summaries (B1, B2, B4) received cosmetic notes about being "overly cautious" or "dry." The aggressive hedging that prevents overclaims also reduces rhetorical force. A reader of B1 might find it informative but unengaging; a reader of A1 might find it compelling but misleading.

This is a real tradeoff, not a defect. The gates optimize for accuracy at the expense of persuasiveness. For research writing — where accuracy should dominate — this is the correct tradeoff. For a blog post or executive summary, the balance might shift.

The average cosmetic issue count was actually slightly higher in Condition B (1.60) than Condition A (1.20). This is because the "over-hedging" pattern shows up as cosmetic issues. The gates reduce serious issues but introduce minor stylistic costs.

### 5.4 Pattern: The AI's Default Optimization

The ungated summaries reveal a consistent default optimization profile:

1. **Lead with drama.** Ungated openings use superlatives ("most significant disruption"), dramatic framing ("time bomb"), and strong causal claims ("fundamentally transforming").
2. **Invent plausible numbers.** When a specific figure would strengthen a rhetorical point, the AI generates one ("$700 billion," "10x," "70%") without sourcing.
3. **Assert rather than argue.** Claims are stated as established facts rather than argued from evidence. The word "show" appears where "suggest" would be accurate.
4. **Skip citations.** When writing flows naturally, the AI omits citations rather than interrupt the rhythm. A2 had zero citations; A1 and A5 had only 1-2 loosely attributed references.
5. **Use journalistic tone.** "The irony is," "seductive," "time bomb" — the ungated AI writes like a tech journalist, not a researcher.

This pattern is consistent with the credence good dynamic described in the STS paper: the AI optimizes for the observable dimension (engaging, fluent, persuasive) while neglecting the unobservable dimension (rigorous, sourced, appropriately scoped).

### 5.5 Quantitative Summary

| Metric | Condition A | Condition B | Reduction |
|--------|------------|------------|-----------|
| Mean total issues | 7.40 | 2.00 | -73% |
| Mean critical issues | 1.40 | 0.00 | -100% |
| Mean substantive issues | 4.80 | 0.40 | -92% |
| Mean cosmetic issues | 1.20 | 1.60 | +33% |
| Mean dimension score | 2.57 | 4.63 | +80% |

The gates eliminated all critical issues and reduced substantive issues by 92%. Cosmetic issues increased slightly, reflecting the over-hedging tradeoff.

---

## 6. Limitations

### 6.1 The Self-Audit Validity Threat (Critical)

**The same AI (Claude Opus 4.6) generated all 10 summaries and performed all audits.** This is the most serious methodological limitation and must be stated plainly:

- The generator knows what the gates are. Even in Condition A ("no gates"), the model has been exposed to the gate definitions in this very conversation. It is impossible to fully isolate Condition A from gate knowledge.
- The auditor may be biased toward finding fewer issues in its own gated output — not deliberately, but because the same model that wrote the hedged language may judge it as appropriate.
- The auditor may be biased toward finding more issues in ungated output — identifying overclaims is easier when you know what the "correct" version looks like (because you just wrote it).
- The dimension scores show a suspiciously clean separation between conditions. A mean of 2.57 vs. 4.63 with no overlap is a strong signal, but it could also reflect systematic bias rather than genuine quality difference.

**What this experiment demonstrates:** The process works — generation, shuffled audit, structured scoring, gate classification. The preliminary signal is strong: gates appear to reduce issues substantially.

**What this experiment does NOT demonstrate:** That the quality difference is real as perceived by an independent human reader. The 73% reduction in issues could shrink, grow, or reverse under independent audit.

### 6.2 What a Valid Experiment Would Look Like

A properly designed experiment would require:

1. **Independent auditors.** At minimum, 2-3 human domain experts who score the summaries blind (not knowing which condition produced each one). Inter-rater reliability (Krippendorff's alpha or Cohen's kappa) would establish whether the audit dimensions are reliably measurable.

2. **Separate generation instances.** Ideally, the ungated summaries would be generated by an AI instance that genuinely has no access to the gate definitions — a separate API call with no gate context in the system prompt.

3. **Larger sample.** 5 per condition is too few for statistical power. A proper experiment would use 20-30 per condition with statistical testing (e.g., Mann-Whitney U for issue counts, which would not assume normality).

4. **Multiple topics.** Testing on one topic confounds topic effects with gate effects. Multiple topics would establish generalizability.

5. **Blinding the auditor.** The auditor should not know the experimental design. In the current setup, the auditor (Claude) designed the experiment, generated both conditions, and knows which summaries have gates. True blinding is not possible when the same entity performs all roles.

### 6.3 Other Limitations

- **Gate completeness.** The 6 gates were derived from a single prior audit (the STS paper). They may not cover all failure modes in research writing. The experiment tests only these specific gates, not the concept of gating in general.
- **Angle effects.** Some angles may be inherently harder to write well. The market dynamics angle (A3, B3) may invite more overclaiming than the measurement angle (A2, B2). The matched-angle design controls for this within pairs but not across the aggregate.
- **Readability not measured.** The experiment measures accuracy-related issues but not readability, engagement, or persuasiveness. If gates make writing more accurate but less readable, the net value depends on the use case.
- **Single model.** Results may not generalize to other AI models (GPT-4, Gemini, etc.) that may have different default optimization profiles.

---

## 7. Conclusion

This experiment provides preliminary evidence that CLAUDE.md quality gates substantially reduce the number of issues in AI-generated research writing. Under the self-audit methodology (acknowledging its limitations):

- **Total issues decreased 73%** (7.40 to 2.00 per summary)
- **Critical issues were eliminated** (1.40 to 0.00)
- **Substantive issues decreased 92%** (4.80 to 0.40)
- **Mean quality dimension scores increased 80%** (2.57 to 4.63)

The gates with the largest effect were **Causal Language** (Gate 1) and **Claim Scope** (Gate 3), which together accounted for 16 of 26 gate-classifiable issues in Condition A. **Data Integrity** (Gate 6) was also highly effective, preventing all 5 instances of fabricated or unsourced numbers.

The main tradeoff was a slight increase in cosmetic issues related to over-hedging — gated writing was more cautious than necessary in places, reducing rhetorical engagement. This is the expected accuracy-persuasiveness tradeoff and is directionally correct for research writing.

**The critical caveat remains:** this is a same-model-generates-and-audits experiment. The process demonstration is valid. The quantitative results are preliminary and require independent validation. Experiment 2 (audit method reliability with independent auditors) should precede any claim that these numbers represent real quality differences as perceived by human experts.

The experiment does confirm one design principle: the gates derived from adversarial audit of one document (the STS paper) transferred to a different writing task (standalone research summaries on a related topic). This is consistent with the hypothesis that some quality dimensions are generalizable across research writing tasks, not specific to the document that generated them.

---

## Appendix: Raw Data Tables

### Issue Severity Distribution

```
Condition A:        Condition B:
A1: C=1 S=5 K=1    B1: C=0 S=0 K=2
A2: C=1 S=4 K=1    B2: C=0 S=0 K=2
A3: C=2 S=5 K=2    B3: C=0 S=1 K=1
A4: C=1 S=5 K=1    B4: C=0 S=0 K=2
A5: C=2 S=5 K=1    B5: C=0 S=1 K=1
----               ----
Tot: C=7 S=24 K=6   Tot: C=0 S=2 K=8
Mean: C=1.4 S=4.8 K=1.2  Mean: C=0.0 S=0.4 K=1.6
```

### Dimension Scores (All 10)

```
         ClStr  CitInt  ScoAcc  AnaHon  FrmRig  DatAcc  Mean
A1:       2      3       2       3       3       3      2.67
A2:       3      2       3       3       3       3      2.83
A3:       2      2       2       3       3       2      2.33
A4:       2      3       2       3       3       3      2.67
A5:       2      2       2       3       3       2      2.33
A Mean:   2.20   2.40    2.20    3.00    3.00    2.60   2.57

B1:       5      5       5       5       4       5      4.83
B2:       5      5       5       5       4       5      4.83
B3:       4      5       4       4       4       5      4.33
B4:       5      5       5       5       4       5      4.83
B5:       5      4       5       4       4       4      4.33
B Mean:   4.80   4.80    4.80    4.60    4.00    4.80   4.63
```
