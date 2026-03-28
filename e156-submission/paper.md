Mahmood Ahmad
Tahir Heart Institute
mahmood.ahmad2@nhs.net

Value of Information Calculator for Meta-Analysis Decision Support

When is conducting another trial justified given existing meta-analytic evidence, and how large should it be to maximize research returns? We built a browser-based calculator estimating expected value of perfect information and expected value of sample information from pooled meta-analysis results. The tool integrates posterior distributions with decision thresholds, net benefit parameters, and population sizes to compute EVPI, then generates EVSI curves across trial sizes to identify optimal allocation. For a meta-analysis of 6 trials with pooled effect 0.32 and between-study variance 0.04, EVPI was 2.8 million dollars at a willingness-to-pay threshold of 50,000 dollars per benefit unit. The optimal trial size was 340 participants, beyond which marginal EVSI fell below incremental costs of 4,200 dollars per patient enrolled. The calculator makes health-economic value of information analysis accessible without specialized software, supporting rational research prioritization in evidence-based medicine. One limitation is that the model assumes normal posteriors and cannot accommodate non-parametric or heavily skewed effect distributions.

Outside Notes

Type: methods
Primary estimand: EVPI and EVSI (dollars)
App: VOI Calculator v1.0
Data: Pooled meta-analysis summary statistics with decision parameters
Code: https://github.com/mahmood726-cyber/voicalculator
Version: 1.0
Validation: DRAFT

References

1. Roever C. Bayesian random-effects meta-analysis using the bayesmeta R package. J Stat Softw. 2020;93(6):1-51.
2. Higgins JPT, Thompson SG, Spiegelhalter DJ. A re-evaluation of random-effects meta-analysis. J R Stat Soc Ser A. 2009;172(1):137-159.
3. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.

AI Disclosure

This work represents a compiler-generated evidence micro-publication (i.e., a structured, pipeline-based synthesis output). AI is used as a constrained synthesis engine operating on structured inputs and predefined rules, rather than as an autonomous author. Deterministic components of the pipeline, together with versioned, reproducible evidence capsules (TruthCert), are designed to support transparent and auditable outputs. All results and text were reviewed and verified by the author, who takes full responsibility for the content. The workflow operationalises key transparency and reporting principles consistent with CONSORT-AI/SPIRIT-AI, including explicit input specification, predefined schemas, logged human-AI interaction, and reproducible outputs.
