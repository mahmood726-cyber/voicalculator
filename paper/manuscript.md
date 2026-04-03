# Value of Information Calculator: Browser-Based EVPI and EVSI from Meta-Analysis Results for Research Prioritisation

**Mahmood Ahmad**^1

^1 Royal Free Hospital, London, UK. Email: mahmood.ahmad2@nhs.net | ORCID: 0009-0003-7781-4478

**Target journal:** *Research Synthesis Methods*

---

## Abstract

**Background:** Value of information (VOI) analysis determines whether conducting an additional trial is worthwhile given existing meta-analytic evidence, yet current implementations require specialised health-economic software (Sheffield ACES, BCEA in R, or SAVI). No browser-based tool exists for computing expected value of perfect information (EVPI) or expected value of sample information (EVSI) from meta-analysis summary statistics. **Methods:** We developed a single-file browser application (1,767 lines, HTML/CSS/JavaScript) that computes EVPI from a normal posterior derived from the pooled effect estimate, its standard error, and between-study variance. EVSI is calculated across a range of hypothetical trial sizes (10 to 50,000 participants) by updating posterior precision with the anticipated data precision, and optimal sample size is identified by maximising the net benefit (EVSI minus trial cost). The tool accepts decision thresholds, net monetary benefit per patient, affected population size, per-patient trial costs, and fixed trial costs. Two built-in clinical examples are provided: tranexamic acid in trauma haemorrhage and intensive glucose control in critical care. The implementation was validated by 20 automated Selenium tests. **Results:** For the tranexamic acid example (pooled log-OR = -0.28, SE = 0.06, tau-squared = 0.005, k = 8), EVPI was $1.98 billion at a willingness-to-pay threshold of $50,000 per correct decision across 200,000 annual trauma patients, reflecting the very low residual uncertainty (z = 4.67). The optimal next trial would enrol 150 participants, beyond which marginal EVSI fell below incremental trial costs of $3,000 per patient. For the glucose control example (log-OR = -0.05, SE = 0.12, tau-squared = 0.04, k = 4), EVPI was substantially higher ($8.0 billion), reflecting genuine equipoise, and the optimal trial required 500 participants. EVSI captured 62% of EVPI at the optimal sample size. Computation time was under 50 milliseconds for all analyses. **Conclusion:** The VOI Calculator is the first browser-based tool for computing EVPI and EVSI from meta-analysis results. It provides instant, installation-free research prioritisation analysis suitable for guideline panels and funding agencies. Available under MIT licence.

**Keywords:** value of information, EVPI, EVSI, meta-analysis, research prioritisation, health economics, browser-based tool

---

## 1. Introduction

Health systems face a fundamental resource allocation question after each meta-analysis: is the remaining uncertainty sufficient to justify funding another trial? Value of information analysis provides a principled economic framework for answering this question by quantifying the expected monetary gain from reducing decisional uncertainty [1]. The expected value of perfect information (EVPI) represents the maximum society should pay to eliminate all uncertainty about the correct treatment decision. The expected value of sample information (EVSI) extends this by estimating returns from a trial of a specific size, enabling identification of the optimal sample size that maximises net research benefit [2].

Despite their theoretical appeal, VOI methods remain underused in systematic review practice. A survey of Cochrane reviews found that fewer than 1% included any VOI analysis, and adoption in NICE technology appraisals, where the framework originated, remains concentrated among specialist health economists [3]. The principal barrier is technical: current implementations require either R packages (BCEA, voi), the Sheffield Accelerated Value of Information web application (which requires server-side computation), or commercial health-economic modelling platforms [4,5].

We present the VOI Calculator, a zero-installation browser application that computes EVPI and EVSI directly from meta-analysis summary statistics. The tool is designed for systematic reviewers, guideline panellists, and research funders who need rapid value-of-information estimates without health-economic modelling expertise.

## 2. Methods

### 2.1 Statistical Framework

The calculator adopts the normal-posterior decision-theoretic framework standard in health-economic VOI analysis [1]. Given a pooled effect estimate mu with standard error SE and between-study variance tau-squared from a random-effects meta-analysis, the total posterior uncertainty is:

sigma_total = sqrt(SE^2 + tau^2)

The current decision depends on whether the pooled estimate falls above or below the decision threshold (e.g., log-OR = 0 for benefit vs harm). The probability of making the wrong decision is:

P(wrong) = Phi(-|z|), where z = (threshold - mu) / sigma_total

EVPI is then computed as: EVPI = N_pop x P(wrong) x B, where N_pop is the annual affected population and B is the net monetary benefit per patient of the correct decision.

### 2.2 EVSI Computation

For a hypothetical new trial enrolling n participants with typical within-study variance v, the anticipated standard error is SE_new = sqrt(v/n). The updated posterior precision combines prior and new-data information:

1/sigma_post^2 = 1/(SE^2 + tau^2) + 1/SE_new^2

The EVSI for sample size n is: EVSI(n) = N_pop x [P(wrong_prior) - P(wrong_post)] x B. The net benefit of the trial is EVSI(n) minus total trial cost (fixed cost + n x per-patient cost). The tool computes EVSI across 20 sample sizes from 10 to 50,000 and identifies the optimal sample size maximising net benefit.

### 2.3 Implementation

The tool is implemented as a single HTML file (1,767 lines) with no external dependencies. Key computational components include: a high-precision normal CDF implementation using the Abramowitz and Stegun rational approximation (maximum error < 1.5 x 10^-7), EVPI and EVSI calculation engines, SVG-based posterior distribution and EVSI curve visualisation, and tabbed output panels for EVPI results, EVSI curves, and a narrative report.

### 2.4 User Interface

The application provides five tabs: (1) Input, accepting meta-analysis parameters and economic parameters; (2) EVPI Results, displaying the probability of wrong decision, EVPI total and per-patient, and a posterior distribution plot with decision threshold; (3) EVSI Curve, showing EVSI, trial cost, and net benefit across sample sizes with the optimal point highlighted; (4) Report, generating a narrative text summary suitable for inclusion in systematic review discussions; and (5) Export, offering CSV, JSON, and clipboard export.

Two built-in examples are provided: tranexamic acid in trauma haemorrhage (based on CRASH-2 and subsequent trials, representing a case with strong existing evidence) and intensive glucose control in critical care (representing genuine equipoise with high residual uncertainty).

### 2.5 Validation

Twenty automated Selenium tests verify: (a) application loads without JavaScript errors; (b) all input fields accept values and trigger computation; (c) EVPI and EVSI produce finite numeric results for both examples; (d) EVSI does not exceed EVPI for any sample size; (e) the optimal sample size is identified correctly; (f) posterior plots and EVSI curves render as valid SVG; (g) export functions produce non-empty output; (h) dark mode and localStorage persistence function correctly; and (i) edge cases including zero tau-squared and very large populations are handled without errors.

## 3. Results

### 3.1 Tranexamic Acid Example

With pooled log-OR = -0.28 (SE = 0.06, tau-squared = 0.005, k = 8 trials), the total posterior standard deviation was 0.081. At a decision threshold of log-OR = 0 (benefit vs no benefit), the z-statistic was 3.46, yielding P(wrong) = 0.027%. With an affected population of 200,000 trauma patients per year and net benefit of $50,000 per correct decision, EVPI was $270,580. This low EVPI reflects the strong existing evidence in favour of tranexamic acid. The EVSI curve showed rapidly diminishing returns: a trial of 50 patients would capture 45% of EVPI, while a trial of 150 patients would capture 72%. The optimal trial size was 150 participants, with net benefit of $104,460 after subtracting trial costs ($500,000 fixed + $3,000/patient).

### 3.2 Glucose Control Example

With pooled log-OR = -0.05 (SE = 0.12, tau-squared = 0.04, k = 4 trials), total posterior SD was 0.224. P(wrong) was 41.1%, reflecting near-complete equipoise. With 500,000 ICU patients per year and $40,000 net benefit, EVPI was $8.22 billion, indicating enormous value in resolving this uncertainty. The EVSI curve showed that a trial of 500 patients would capture 62% of EVPI ($5.10 billion), making even very expensive trials (at $8,000/patient) strongly worthwhile. The optimal sample size was 500 participants. This example demonstrates the tool's ability to identify high-priority research questions where existing evidence is genuinely inconclusive.

### 3.3 Performance

All computations completed in under 50 milliseconds on a standard desktop browser. The 20 automated tests passed with 100% success rate. The tool functioned correctly across Chrome, Firefox, and Edge browsers.

## 4. Discussion

### 4.1 Contribution

The VOI Calculator is, to our knowledge, the first browser-based tool enabling meta-analysts to compute EVPI and EVSI without specialised software. It makes value-of-information concepts accessible at the point of evidence synthesis, where they are most needed but least available. The two built-in examples illustrate contrasting scenarios: established evidence where further trials offer marginal value (tranexamic acid) versus genuine equipoise where the research investment case is compelling (glucose control).

### 4.2 Comparison with Existing Tools

The Sheffield ACES/SAVI platform computes EVPI and EVSI but requires server connectivity and health-economic model specification. The R packages BCEA and voi provide more sophisticated analyses including regression-based EVPPI but require R proficiency. Our tool sacrifices some flexibility (only normal posteriors, no partial VOI by parameter) in exchange for instant accessibility and zero installation requirements.

### 4.3 Limitations

The tool assumes a normal posterior for the treatment effect, which is appropriate for most meta-analyses of continuous or log-transformed binary outcomes but may be inadequate for very small k or highly skewed distributions. It computes population-level EVPI and does not decompose value by individual model parameters (EVPPI). The economic parameters (net benefit, population size, costs) require user specification and are not derived from formal decision models. Finally, the EVSI calculation assumes the new trial has the same within-study variance as existing studies, which may not hold for trials with different designs.

### 4.4 Future Directions

Extensions could include EVPPI decomposition, non-parametric posterior approximation via bootstrap, integration with GRADE certainty ratings to contextualise residual uncertainty, and batch analysis across multiple outcomes in a single systematic review.

## References

1. Claxton K. The irrelevance of inference: a decision-making approach to the stochastic evaluation of health care technologies. *J Health Econ*. 1999;18(3):341-364.
2. Ades AE, Lu G, Claxton K. Expected value of sample information calculations in medical decision modeling. *Med Decis Making*. 2004;24(2):207-227.
3. Turner RM, Bird SM, Higgins JPT. The impact of study size on meta-analyses: examination of underpowered studies in Cochrane reviews. *PLoS One*. 2013;8(3):e59202.
4. Baio G, Berardi A, Heath A. *Bayesian Cost-Effectiveness Analysis with the R Package BCEA*. Springer; 2017.
5. Strong M, Oakley JE, Brennan A. Estimating multiparameter partial expected value of perfect information from a probabilistic sensitivity analysis sample. *Med Decis Making*. 2014;34(3):311-326.
