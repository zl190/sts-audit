# Formalization Draft: Maintenance Cost Function and Rewrite Threshold Model

**Status:** Working draft for co-author review. Not publication-ready.
**Date:** 2026-02-23
**Gate 5 discipline applied throughout.** Every equation is labeled with its epistemic status.

---

## 1. Literature Review Summary

### 1.1 Banker, Datar, Kemerer & Zweig (1993) — Empirical Cost-Complexity Link

**What they did:** Estimated a production frontier model across 65 COBOL maintenance projects at a large bank. Found that projects maintaining more complex code cost approximately 25% more than otherwise identical projects. Complexity was measured across three dimensions: module size, procedure size, and branching complexity.

**What we can use:** This is the best empirical anchor for the claim that maintenance cost is increasing in structural complexity. The 25% figure is for a dichotomous split (complex vs. not-complex); the underlying regression uses a log-linear functional form, regressing log(maintenance effort) on complexity measures plus controls. This suggests a multiplicative (not additive) relationship between complexity and cost.

**What we cannot use:** Their complexity measures are COBOL-specific (module count, procedure length, branching). Cyclomatic complexity (CC) as measured by `radon` is a related but distinct metric. We cannot directly transfer their coefficients to our setting. The 25% figure is illustrative of effect size, not a parameter we can plug in.

### 1.2 Banker, Datar & Kemerer (1991) — Production Frontier Model

**What they did:** Developed an estimable stochastic frontier production function for software maintenance productivity. The model allows simultaneous estimation of the production frontier and productivity factor effects, with two-sided error terms (inefficiency + noise).

**What we can use:** The functional form precedent. They modeled maintenance output as a production function of inputs (effort, staff) modified by environmental factors (complexity, application type). This is the methodological template for estimating how architectural quality enters the cost function.

**What we cannot use:** Their parameter estimates, which are environment-specific (1980s COBOL banking). The stochastic frontier methodology requires project-level data we do not have.

### 1.3 Banker, Datar & Kemerer (1996) / Chan, Chung & Ho (1996) — Replacement Timing

**Clarification:** The paper cited in our draft as "Banker, Datar & Kemerer (1996)" about replacement timing is actually by Chan, Chung & Ho (1996), "An Economic Model to Estimate Software Rewriting and Replacement Times," IEEE TSE 22(8):580-598. Banker, Datar & Kemerer's 1991 and 1993 papers address maintenance productivity and cost, not replacement timing directly.

**What Chan et al. did:** Proposed a cost model for the rewrite decision that balances ongoing maintenance cost against one-time replacement cost, accounting for factors like user environment volatility, maintenance quality, and team learning.

**What we can use:** The basic decision framework: replace when NPV of remaining maintenance exceeds NPV of replacement + fresh maintenance. This is the structure we need to make non-tautological.

**What we cannot use:** Their specific parameter values, which require organizational survey data.

### 1.4 Ji, Kumar, Mookerjee, Sethi & Yeh (2011) — Optimal Control Model

**What they did:** Formulated the software lifecycle as an optimal control problem: choose initial feature set, dynamic enhancement effort, and system lifetime to maximize net value. Solved for optimal replacement timing using Pontryagin's maximum principle.

**What we can use:** The formal structure of an optimal stopping problem applied to software replacement. Their model shows that the replacement decision can be formalized as: replace when the shadow price of the existing system falls below the option value of a new system. This is the most rigorous treatment of the rewrite decision in the literature.

**What we cannot use:** Their model requires continuous-time dynamics and functional form assumptions (system value as a function of features and quality) that are not directly estimable from our metrics.

### 1.5 Lizzeri (1999) — Certification Intermediary Model

**What he did:** Analyzed a monopolist certification intermediary who observes seller quality (drawn from a distribution) and chooses what to reveal to buyers. Key result: the monopolist certifier optimally reveals only whether quality exceeds a minimum standard (pass/fail), extracting all information surplus. Under competition among certifiers, more information may be revealed.

**What we can use:**
- The pass/fail result directly justifies our binary certification design. Lizzeri shows this is the profit-maximizing strategy for the certifier, not just a simplification.
- The welfare analysis: certification improves on no-certification (prevents trade in the lowest qualities) but a monopolist certifier captures the surplus, leaving welfare below the full-information benchmark.
- The framework for analyzing what happens when we introduce a *free, open-source* certifier (our tool): this removes the monopolist's rent extraction, potentially achieving near-full-information welfare.

**What we must be careful about:**
- Lizzeri's model assumes quality is exogenous (seller has a quality draw, cannot change it). Our paper claims disclosure endogenously raises quality. These are complementary but distinct mechanisms — Lizzeri's model does not cover ours.
- Lizzeri's quality is a single scalar drawn from a distribution. Our quality is multi-dimensional (CC, LVD, CCR, TL) collapsed into a binary signal. The information loss from this collapse needs analysis.

### 1.6 Dulleck & Kerschbamer (2006) — Credence Goods Framework

**What they did:** Unified the credence goods literature with a common model. Key result: under a small set of assumptions (Homogeneity, Commitment, Verifiability), the price mechanism alone is sufficient to solve the fraudulent expert problem. Most inefficiency results in the literature can be derived by dropping one assumption.

**Their formal setup:**
- Expert observes consumer's problem type (severity). Consumer does not.
- Expert chooses treatment quality. Consumer cannot verify if treatment was appropriate.
- Key conditions for efficiency:
  - **Liability:** Expert must provide treatment sufficient to solve the problem (rules out undertreatment)
  - **Verifiability:** Consumer can observe what quality was provided (rules out overcharging)
- If both hold, experts set equal-markup prices and provide efficient treatment.
- If verifiability fails (consumer cannot observe quality delivered), overcharging and undertreatment become possible.

**What we can use:** Software architecture quality fails the verifiability condition — the buyer cannot observe $Q_a$ even after delivery. This places the software market in the "no verifiability" regime of their model, which predicts fraud (in our context: delivering low $Q_a$ while charging for high $Q_a$). Our certification instrument restores verifiability.

**What we must be careful about:** Their model assumes the expert privately diagnoses the consumer's *need* (problem severity). In software, the "diagnosis" analog is ambiguous — the developer assesses what architecture the project *needs*, but the buyer specifies functional requirements. The mapping is not one-to-one.

### 1.7 Asseyer & Weksler (2024) — Certification Design with Common Values (Econometrica)

**What they did:** Extended the Lizzeri model to common values settings (seller's opportunity cost depends on quality). Key result: certifier-optimal design implements partial disclosure; a transparency-maximizing regulator prefers a *less precise* signal that conveys *more* information through higher certification rates and unraveling.

**What we can use:** Their finding that a social planner may prefer a different certification design than the profit-maximizing certifier. Since our tool is open-source (no profit motive), we can design for transparency maximization rather than profit maximization. This provides theoretical backing for our design choices.

### 1.8 Tsoukalas et al. (2020) — Technical Debt Forecasting

**What they did:** Applied ARIMA models to forecast technical debt principal (as measured by SonarQube) across 5 open-source Java projects. Found ARIMA(0,1,1) provides adequate short-term forecasts (up to 8 weeks). Longer horizons degraded.

**What we can use:** Proof of concept that TD-related metrics are forecastable with time-series methods. Their 8-week accuracy horizon is a useful calibration point for what is achievable.

**What we cannot use:** They forecast TD principal (a dollar-denominated composite), not individual metrics like CC. They do not model the replacement decision.

### 1.9 Ajibode et al. (2024) — Systematic Review of TD Forecasting

**What they found:** Surveyed 646 papers, included 14 primary studies. Random Forest and Temporal Convolutional Networks performed best. Only 2 of 15 TD types were studied (code debt 87.5%, architecture debt 12.5%). No study used the replacement decision as a prediction target.

**What this means for us:** The replacement-decision-as-prediction-target is genuinely novel — confirmed by the most comprehensive review. But the forecasting accuracy for the *inputs* to our model (complexity metrics over time) has only been validated in narrow settings.

---

## 2. Maintenance Cost Function

### 2.1 The Problem

The paper states: "The maintenance cost function $C(Q_a, \Delta)$ is convex decreasing in $Q_a$." This is a verbal claim dressed in notation. It says "cost goes down when quality goes up, and the effect accelerates" — which is intuitive but not a model. Gate 5 requires us to either formalize this non-trivially or label it as a conceptual claim.

### 2.2 What Banker et al. (1993) Actually Estimated

Banker et al. used a log-linear specification for their production frontier:

$$\ln(\text{Effort}) = \beta_0 + \beta_1 \ln(\text{Size}) + \beta_2 \cdot \text{Complexity} + \beta_3 \cdot \text{Controls} + \epsilon$$

where Complexity was measured by module-level structural metrics. Their key finding was that the coefficient on the complexity term was positive and significant, with complex systems requiring approximately 25% more effort.

This log-linear form implies a *multiplicative* cost structure: complexity acts as a cost multiplier, not an additive term. In their data, the multiplicative factor for "complex" (vs. "not complex") was approximately 1.25.

### 2.3 Proposed Functional Form

**Epistemic status: Testable hypothesis, not a proven result. The functional form is motivated by empirical precedent (Banker et al.) and theoretical plausibility, but the specific parameters are not estimated from our data.**

We propose the following maintenance cost function for a single change:

$$C(\text{CC}, \Delta) = c_0 \cdot \Delta^{\alpha} \cdot \text{CC}^{\beta}$$

where:
- $c_0 > 0$ is a base cost parameter (organization-specific, captures wage rates, tooling, etc.)
- $\Delta > 0$ measures the scope of the required change (e.g., number of new requirements, story points)
- $\text{CC}$ is the cyclomatic complexity of the module being changed
- $\alpha > 0$ is the elasticity of cost with respect to change scope
- $\beta > 0$ is the elasticity of cost with respect to complexity

**Why this form:**

1. **Multiplicative structure** follows Banker et al. (1993), who found that complexity acts as a cost multiplier, not an additive term. The Cobb-Douglas form is the simplest multiplicative specification.

2. **Log-linear in logs:** Taking logarithms gives $\ln C = \ln c_0 + \alpha \ln \Delta + \beta \ln \text{CC}$, which is estimable via OLS given project-level data on (cost, change scope, complexity).

3. **Convexity in CC when $\beta > 1$:** The second derivative $\partial^2 C / \partial \text{CC}^2 = \beta(\beta - 1) c_0 \Delta^{\alpha} \text{CC}^{\beta - 2}$, which is positive when $\beta > 1$. The claim in our paper that $C$ is "convex decreasing in $Q_a$" requires $\beta > 1$ (superlinear cost growth in complexity). Whether $\beta > 1$ is an *empirical question*, not an assumption we should assert without data.

4. **Decreasing in architectural quality:** Since higher $Q_a$ implies lower CC (by the instrument's definition), $C$ is decreasing in $Q_a$ for any $\beta > 0$. The "convex" qualifier requires $\beta > 1$.

**What this buys us:** A parametric form that is (a) estimable given the right data, (b) nests the linear case ($\beta = 1$) and the convex case ($\beta > 1$), (c) consistent with the empirical literature.

**What it does not buy us:** Actual parameter values. $\beta$ must be estimated from data. The Banker et al. (1993) finding of 25% higher cost for complex systems is consistent with $\beta \approx 0.3-0.5$ (depending on the CC distribution in their sample), but this is a rough calibration, not a measured elasticity for CC specifically.

### 2.4 Incorporating Complexity Growth

If CC grows over successive changes, we need a law of motion. The paper hypothesizes geometric growth:

$$\text{CC}(n) = \text{CC}_0 \cdot (1 + r)^n$$

where $r$ is the per-change complexity growth rate and $n$ is the number of changes applied.

**Epistemic status: Conceptual framework.** We have one data point (CC grew from 17 to 23, i.e., $r \approx 0.35$, after one change for the H-TIER case). A single observation cannot establish whether the growth is geometric, linear, or episodic. The geometric form is a working assumption chosen because:
- It is the standard form for compound growth/depreciation in finance
- It is the worst-case bound for planning purposes (exponential > polynomial)
- It is testable: with a time series of CC values over changes, one can test $H_0: r_{n+1} = r_n$ (constant growth rate)

Under this assumption, the cumulative maintenance cost over $N$ changes is:

$$C_{\text{total}}(N) = \sum_{n=1}^{N} c_0 \cdot \Delta_n^{\alpha} \cdot [\text{CC}_0 (1+r)^n]^{\beta}$$

For homogeneous changes ($\Delta_n = \bar{\Delta}$ for all $n$), this simplifies to:

$$C_{\text{total}}(N) = c_0 \cdot \bar{\Delta}^{\alpha} \cdot \text{CC}_0^{\beta} \sum_{n=1}^{N} (1+r)^{n\beta}$$

The sum is a geometric series: $\sum_{n=1}^{N} q^n = q \cdot \frac{q^N - 1}{q - 1}$ where $q = (1+r)^{\beta}$.

If $\beta > 0$ and $r > 0$, then $q > 1$ and the cumulative cost grows *exponentially* in $N$. This is the formal content of the "depreciating asset" claim: the per-change cost accelerates, causing cumulative cost to explode.

### 2.5 Honest Limitations

1. **$c_0$ is organization-specific and unobservable to us.** We cannot produce dollar estimates without calibrating to organizational cost data.

2. **$\alpha$ and $\beta$ are not estimated.** The functional form is motivated by precedent, not fit to our data. We have n=3 case studies, which is insufficient for parameter estimation.

3. **CC is a proxy for architectural quality, not architectural quality itself.** Jay & Hale (2009) found CC is largely redundant with lines of code. Our instrument uses CC as part of a composite, but the cost function above uses CC alone for tractability. A full model would need the composite metric, which complicates estimation.

4. **The geometric growth assumption for CC is unsupported beyond one data point.** Real CC trajectories may be punctuated (stable, then jump on a major feature), regressive (refactoring reduces CC), or plateau (growth bounded by module size).

---

## 3. Rewrite Threshold Model

### 3.1 The Problem

The current paper states the rewrite threshold as:

$$\sum_{i=1}^{n} C_{\text{maintain}}(\text{CC}(i), \Delta_i) > C_{\text{replace}}$$

This is tautological: the rewrite threshold is defined as the point where maintenance exceeds replacement, and the inequality says... maintenance exceeds replacement at the rewrite threshold. It has no predictive content.

### 3.2 What Makes a Non-Tautological Model

A non-tautological rewrite threshold model must do one of the following:

**(A) Predict when the threshold arrives** — given observable inputs today (current CC, estimated $r$, estimated $\beta$), output a prediction: "the threshold will be reached in approximately $N^*$ changes." This is a forecasting model.

**(B) Determine the optimal replacement timing** — accounting for the time-value of money, the option value of waiting, and the uncertainty in future costs. This is an optimal stopping model.

**(C) Identify the observable leading indicators** — metrics whose current values or trajectories are predictive of how close the system is to the threshold. This is a risk scoring model.

We attempt (A) and sketch (B). We argue that (C) is what the certification instrument already does, but framing it as a model requires (A) or (B) to define what the instrument is predicting.

### 3.3 Forecasting Model (Type A)

**Epistemic status: Testable hypothesis, contingent on parameter estimability.**

Using the cost function from Section 2.3 and assuming geometric CC growth with homogeneous changes:

$$C_{\text{total}}(N) = c_0 \cdot \bar{\Delta}^{\alpha} \cdot \text{CC}_0^{\beta} \cdot (1+r)^{\beta} \cdot \frac{(1+r)^{N\beta} - 1}{(1+r)^{\beta} - 1}$$

The rewrite occurs at $N^*$ where $C_{\text{total}}(N^*) = C_{\text{replace}}$. Solving for $N^*$:

$$N^* = \frac{1}{\beta \ln(1+r)} \cdot \ln\left(1 + \frac{C_{\text{replace}}}{c_0 \bar{\Delta}^{\alpha} \text{CC}_0^{\beta}} \cdot \frac{(1+r)^{\beta} - 1}{(1+r)^{\beta}}\right)$$

**What this says (in words):** The number of changes before the rewrite threshold depends on:
- $C_{\text{replace}} / (c_0 \bar{\Delta}^{\alpha} \text{CC}_0^{\beta})$: the ratio of replacement cost to current per-change cost. Higher ratio means more changes before rewrite.
- $r$: the complexity growth rate. Higher growth rate means fewer changes before rewrite.
- $\beta$: the cost-complexity elasticity. Higher elasticity means fewer changes before rewrite.

**What this predicts (testable implications):**
1. Systems with higher initial CC reach the rewrite threshold sooner ($\partial N^* / \partial \text{CC}_0 < 0$).
2. Systems with faster CC growth reach the rewrite threshold sooner ($\partial N^* / \partial r < 0$).
3. The relationship is logarithmic in the cost ratio — doubling the replacement cost does not double the time-to-rewrite; it adds a fixed number of changes.
4. If $\beta < 1$ (sublinear cost growth in CC), the threshold may never be reached — cumulative cost converges. Only if $\beta > 1$ is the explosion guaranteed.

**Prediction 4 is the key testable claim:** The paper asserts convexity ($\beta > 1$) without evidence. If $\beta \leq 1$, the entire rewrite threshold framework collapses for the geometric-growth case — cumulative maintenance cost grows only linearly or sublinearly, and a finite threshold may not exist for reasonable replacement costs.

### 3.4 Illustrative Calibration (Not an Estimate)

**Epistemic status: Illustration only. These are assumed values to show the model's behavior, not measured parameters.**

Suppose:
- $\text{CC}_0 = 17$ (H-TIER initial complexity from Case 1)
- $r = 0.35$ (observed growth rate from one change in Case 1)
- $\beta = 1.5$ (assumed superlinear; no empirical basis for this specific value)
- $C_{\text{replace}} / (c_0 \bar{\Delta}^{\alpha}) = 50 \cdot 17^{1.5} \approx 3,500$ (assumed: replacement costs 50x a single change on the initial system)

Then:

$$N^* = \frac{1}{1.5 \ln(1.35)} \ln\left(1 + 3500 \cdot \frac{(1.35)^{1.5} - 1}{17^{1.5} \cdot (1.35)^{1.5}}\right)$$

Computing: $(1.35)^{1.5} \approx 1.567$, so the inner ratio is $\approx 3500 \cdot 0.567 / (70.1 \cdot 1.567) \approx 3500 \cdot 0.567 / 109.8 \approx 18.1$.

$$N^* \approx \frac{1}{1.5 \times 0.300} \ln(19.1) \approx \frac{2.95}{0.450} \approx 6.6 \text{ changes}$$

Under these (assumed!) parameters, the H-TIER system hits the rewrite threshold after roughly 7 changes.

For the Z-TIER system ($\text{CC}_0 = 4$, $r = 0$, i.e., no CC growth because the modular architecture absorbs changes):

If $r = 0$, then $\text{CC}(n) = \text{CC}_0$ for all $n$, and $C_{\text{total}}(N) = N \cdot c_0 \bar{\Delta}^{\alpha} \text{CC}_0^{\beta}$. The threshold $N^* = C_{\text{replace}} / (c_0 \bar{\Delta}^{\alpha} \text{CC}_0^{\beta})$.

Using the same replacement cost ratio: $N^* = 50 \cdot 17^{1.5} / 4^{1.5} = 50 \times 70.1 / 8 \approx 438$ changes.

The contrast (7 vs. 438 changes) is dramatic but depends entirely on the assumed parameters, especially $r$ and $\beta$. **This is an illustration of model behavior, not an empirical prediction.**

### 3.5 Optimal Stopping Formulation (Type B) — Sketch Only

**Epistemic status: Conceptual framework. This is the structure a formal model would take; we do not solve it.**

The replacement decision is an optimal stopping problem. At each change $n$, the decision-maker observes the current complexity $\text{CC}(n)$ and chooses: maintain (pay $C(\text{CC}(n), \Delta_{n+1})$ and continue) or replace (pay $C_{\text{replace}}$ and restart with $\text{CC}_0'$).

In the discounted infinite-horizon version, the value function satisfies:

$$V(\text{CC}) = \min\left\{C_{\text{replace}} + V(\text{CC}_0'), \quad C(\text{CC}, \bar{\Delta}) + \delta \cdot \mathbb{E}[V(\text{CC}')] \right\}$$

where:
- $\delta \in (0,1)$ is the discount factor per change cycle
- $\text{CC}' = \text{CC} \cdot (1 + r + \epsilon)$ for some noise $\epsilon$ (stochastic CC growth)
- $\text{CC}_0'$ is the complexity of the replacement system

This is a standard Bellman equation for machine replacement (cf. Rust, 1987, on bus engine replacement). The optimal policy is a threshold rule: replace when $\text{CC} > \text{CC}^*$, where $\text{CC}^*$ is the optimal replacement threshold.

**Why we cannot solve this here:**
1. The transition law $\text{CC}' | \text{CC}$ requires a distributional assumption on the noise, calibrated to actual CC time-series data.
2. The replacement complexity $\text{CC}_0'$ is endogenous if the replacement is AI-generated — our paper's finding is that AI defaults to high $\text{CC}_0'$ without certification, meaning $\text{CC}_0'$ depends on the governance regime.
3. The discount factor $\delta$ requires mapping from calendar time to change cycles, which varies by project.

**What a co-author could contribute:** Solve the Bellman equation for specific distributional assumptions, derive comparative statics on the optimal threshold $\text{CC}^*$, and connect to the Rust (1987) machine replacement literature. This is a well-understood class of problems; the novelty is the application to software with endogenous replacement quality.

### 3.6 Connection to the Certification Instrument

The certification instrument contributes to the rewrite prediction in two ways:

**As a measurement tool (input to prediction):** The instrument records CC, LVD, CCR at each change cycle, producing the time series $\{\text{CC}(n)\}_{n=1}^{N}$ from which $r$ can be estimated. Without standardized per-change measurement, there is no data to predict from.

**As a governance constraint (modifying the model's parameters):** If the instrument is required at each delivery, it prevents $r$ from exceeding the threshold that triggers rejection. This bounds the CC trajectory: $\text{CC}(n) \leq \text{CC}_{\max}$ for all $n$. Under a bounded trajectory, the cumulative cost may never reach the rewrite threshold — the certification instrument prevents the rewrite by preventing the degradation.

This is the "doorkeeper" dual role described in the paper, but formalized: the instrument provides the $r$ estimate that feeds the forecasting model, and the instrument's threshold constrains $r$ such that the forecast may never trigger replacement.

---

## 4. Welfare Analysis Sketch

### 4.1 The Pooling Equilibrium Cost

**Epistemic status: Conceptual framework grounded in Akerlof (1970) and Lizzeri (1999). The structure is standard; the specific application to software is novel but not formally derived.**

In the absence of certification, the software market is in a pooling equilibrium. Buyers pay a price $p^{\text{pool}}$ reflecting expected average quality. Define:

- $\theta \in \{L, H\}$: quality type (Low/High architectural quality)
- $v_{\theta}$: buyer's total cost of ownership given type $\theta$ ($v_L > v_H$ since low quality costs more to maintain)
- $c_{\theta}$: seller's production cost ($c_L < c_H$ since low quality is cheaper to produce)
- $\lambda$: fraction of high-quality producers

**Pooling price:** $p^{\text{pool}} = \lambda v_H + (1-\lambda) v_L$ — buyers pay expected total cost of ownership.

Actually, this is wrong. In the standard Akerlof setup, the price reflects willingness to pay given average quality. Let us be more careful.

**Standard adverse selection structure:**

- Buyer's willingness to pay: $w(\theta)$, with $w(H) > w(L)$
- In pooling: $p^{\text{pool}} = \lambda w(H) + (1-\lambda) w(L)$
- High-quality producer participates if $p^{\text{pool}} \geq c_H$
- If $\lambda w(H) + (1-\lambda) w(L) < c_H$, high-quality producers exit, leading to pure adverse selection

**Deadweight loss from pooling:** The loss has two components:
1. **Allocative inefficiency:** Some buyers who would benefit from high quality at $c_H$ are matched with low quality because high-quality producers have exited or reduced investment.
2. **Maintenance cost externality:** Low-quality software imposes higher maintenance costs on buyers. The excess maintenance cost is $(v_L - v_H)$ per unit of low quality consumed.

**With certification (Lizzeri 1999 applied):** A certifier observing $\theta$ issues a pass/fail signal $s \in \{P, F\}$. If $s = P$ implies $\theta = H$ (no false positives — a property our deterministic tool satisfies), then buyers can condition payment on the signal:
- $p_P = w(H)$ for certified high quality
- $p_F = w(L)$ for uncertified

This is the separating equilibrium. High-quality producers earn $w(H) - c_H > 0$ (by assumption that $w(H) > c_H$). Low-quality producers earn $w(L) - c_L$.

**Welfare gain from certification:**

$$\Delta W = \lambda \cdot [w(H) - c_H - \max(p^{\text{pool}} - c_H, 0)] + (1-\lambda) \cdot [(v_L^{\text{pool}} - v_L^{\text{sep}})]$$

**Honest confession:** This is getting into notation-for-intuition territory. The welfare gain from moving from pooling to separating is a standard result in the adverse selection literature. Writing it down for the software case does not add content beyond: "certification enables a separating equilibrium, which improves welfare by the standard mechanism." The specific welfare gain depends on $\lambda$, $w(\theta)$, and $c_{\theta}$ — none of which we can estimate.

### 4.2 What We Can Say (And What We Cannot)

**What we can say:**
- The software market satisfies the conditions for adverse selection (Section 2.2 of the paper). This is a qualitative claim supported by institutional analysis.
- Certification enables a separating equilibrium (standard result, applicable here given the instrument satisfies Lizzeri's conditions).
- The welfare gain is positive if there exist high-quality producers who are currently priced out or under-investing.
- The welfare gain is bounded above by $\lambda \cdot (w(H) - w(L))$ — the maximum gain from perfect sorting.

**What we cannot say:**
- What $\lambda$ is (what fraction of software producers would produce high-quality architecture if the market rewarded it).
- What $w(H) - w(L)$ is in dollar terms (the maintenance cost differential between high and low quality).
- Whether the CISQ $2.41T figure can be decomposed to isolate the architecture-quality component.

### 4.3 The Lizzeri Insight Applied to Open-Source Certification

Lizzeri (1999) shows that a monopolist certifier captures the information surplus through fee extraction, reducing the welfare gain from certification. Our instrument is open-source and free, which corresponds to the competitive-certifier case in Lizzeri's analysis. Under competitive certification (or free certification), the full information surplus accrues to market participants rather than the certifier.

Asseyer & Weksler (2024) show that a transparency-maximizing regulator prefers a *less precise* signal than the profit-maximizing certifier — because a less precise signal induces higher certification rates and more voluntary disclosure (unraveling). This is directly relevant: our pass/fail binary may be less informationally precise than a graded rating, but the binary design may induce more voluntary adoption, achieving higher overall information transmission. **This is a testable prediction**: we predict higher adoption rates for pass/fail certification than for graded ratings, all else equal.

---

## 5. Self-Audit: Gate 5 Applied to This Document

### Genuine Models (produce testable predictions, contingent on parameter estimation)

1. **The Cobb-Douglas maintenance cost function** (Section 2.3): $C = c_0 \Delta^{\alpha} \text{CC}^{\beta}$. This is a genuine parametric model, estimable via OLS in logs given appropriate data. It produces the testable prediction that log-cost is linear in log-CC and log-change-scope. **Status: Testable hypothesis.** Parameters not estimated.

2. **The forecasting model for $N^*$** (Section 3.3): Given the cost function and geometric CC growth, the time-to-rewrite is a specific function of observables ($\text{CC}_0$, $r$) and parameters ($\beta$, cost ratio). **Status: Testable hypothesis.** Requires: (a) estimated $\beta$, (b) multiple project histories with known rewrite events, (c) validation that CC growth is approximately geometric.

3. **The prediction $\partial N^* / \partial r < 0$** (Section 3.3, prediction 2): Systems with faster CC growth reach rewrite sooner. This is testable even without knowing exact parameters — it's a directional prediction. **Status: Testable hypothesis (directional).**

4. **The prediction about $\beta > 1$** (Section 3.3, prediction 4): Whether cost is convex in CC is an empirical question. If $\beta \leq 1$, the rewrite-explosion result does not hold for all systems. **Status: Open empirical question.** The paper should not assert convexity without evidence.

### Conceptual Frameworks (structure for thinking, not yet models)

5. **The Bellman equation for optimal stopping** (Section 3.5): Standard structure, but unsolved for our specific transition law and cost parameters. Labeling it a "model" is premature. **Status: Conceptual framework.**

6. **The welfare analysis** (Section 4): Standard adverse selection welfare analysis applied to software. No novel formal content beyond the application. Dollar magnitudes are unknown. **Status: Notation for an intuition.** The qualitative argument (certification improves welfare) stands; the equations add rigor of presentation but not rigor of content.

7. **The geometric CC growth assumption** (Section 2.4): A convenient functional form with one data point. **Status: Working assumption in need of validation.**

### Notation-for-Intuition (should be labeled as such in the paper)

8. **The original tautological inequality** $\sum C_{\text{maintain}} > C_{\text{replace}}$: This defines the threshold; it does not predict it. The paper has already labeled this as a "framework" rather than a "model" — correct. But Sections 3.3 and 3.4 show that the inequality, combined with a cost function and growth law, *can* produce non-tautological predictions.

9. **The welfare gain formula** $\Delta W$ in Section 4.1: The formula is correct but vacuous without parameter values. It should appear in the paper (if at all) with explicit caveats that it is a structural framework, not a quantified estimate.

---

## 6. What Still Needs a Co-Author

### Critical Gaps (cannot be addressed without domain expertise + data)

1. **Parameter estimation for $\beta$ (cost-complexity elasticity).** This requires a dataset of software maintenance projects with: (a) measured complexity at each change, (b) measured effort or cost for each change, (c) measured change scope. The closest existing estimates are from Banker et al. (1993, COBOL) and the SonarQube-based TD literature. A co-author with access to organizational project data or large-scale open-source mining infrastructure could estimate $\beta$ for modern Python/JavaScript codebases.

2. **Solving the optimal stopping problem (Section 3.5).** The Bellman equation is standard structure, but solving it for our specific setting — especially with endogenous replacement quality (the AI certification loop) — requires a mathematical economist or operations researcher. Ji et al. (2011) provide the closest template, using optimal control theory. A co-author familiar with the Rust (1987) bus-replacement framework could adapt it to our setting.

3. **Formal welfare analysis.** The Lizzeri (1999) and Asseyer & Weksler (2024) frameworks provide the tools, but properly adapting them to multi-dimensional quality (CC, LVD, CCR, TL collapsed to binary) and endogenous quality (the governance effect) requires formal mechanism design work. This is likely a separate paper, not a section of this one.

4. **Empirical validation of CC growth rates.** The claim that H-TIER systems exhibit superlinear CC growth requires longitudinal data across many projects and many changes. Mining git histories of open-source projects to extract CC trajectories per commit is feasible but labor-intensive. A co-author with software engineering empirical methods experience could run this study.

### Gaps That May Not Need a Co-Author

5. **The illustrative calibration** (Section 3.4) could be extended with more case studies. Running 10-20 controlled experiments (same as Case 1 but with multiple changes) would provide a richer dataset for CC growth rate estimation, achievable with the current experimental infrastructure.

6. **The connection to survival analysis** (Section 5.4 of the paper). Framing the rewrite prediction as a Cox proportional hazards model requires only the standard statistical framework plus a dataset of project lifetimes with covariates. Any statistician could do this; it does not require specialized economic theory.

### What the Paper Should Say About What It Cannot Do

The paper should explicitly state that:
- The maintenance cost function is proposed, not estimated. The functional form is motivated by Banker et al. (1993); the parameters require future empirical work.
- The rewrite threshold model produces testable predictions (higher $r$ means sooner rewrite, higher initial CC means sooner rewrite) but cannot yet produce numerical predictions (because $\beta$ is unknown).
- The welfare analysis establishes that certification improves welfare relative to pooling (a standard result applied to a new domain) but cannot quantify the improvement.
- The $\beta > 1$ (convexity) claim is a hypothesis, not an established fact. If $\beta \leq 1$, the urgency of the rewrite problem is reduced but not eliminated (costs still grow, just linearly).

---

## References Used in This Draft

- Ajibode, A. et al. (2024). Systematic literature review on forecasting and prediction of technical debt evolution. arXiv:2406.12026.
- Akerlof, G.A. (1970). The market for "lemons." QJE, 84(3), 488-500.
- Asseyer, A. & Weksler, R. (2024). Certification design with common values. Econometrica, 92(3), 651-686.
- Banker, R.D., Datar, S.M. & Kemerer, C.F. (1991). A model to evaluate variables impacting the productivity of software maintenance projects. Management Science, 37(1), 1-18.
- Banker, R.D., Datar, S.M., Kemerer, C.F. & Zweig, D. (1993). Software complexity and maintenance costs. CACM, 36(11), 81-94.
- Chan, T., Chung, S.L. & Ho, T.H. (1996). An economic model to estimate software rewriting and replacement times. IEEE TSE, 22(8), 580-598.
- Dulleck, U. & Kerschbamer, R. (2006). On doctors, mechanics, and computer specialists. JEL, 44(1), 5-42.
- Ji, Y., Kumar, S., Mookerjee, V.S., Sethi, S.P. & Yeh, D. (2011). Optimal enhancement and lifetime of software systems. P&OM, 20(6), 889-904.
- Lizzeri, A. (1999). Information revelation and certification intermediaries. RAND JE, 30(2), 214-231.
- Nagappan, N. & Ball, T. (2005). Use of relative code churn measures to predict system defect density. ICSE, 284-292.
- Rust, J. (1987). Optimal replacement of GMC bus engines. Econometrica, 55(5), 999-1033.
- Tsoukalas, D. et al. (2020). Technical debt forecasting. JSS, 170, 110777.
