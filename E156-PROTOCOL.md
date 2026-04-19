# E156 Protocol — `VOICalculator`

This repository is the source code and dashboard backing an E156 micro-paper on the [E156 Student Board](https://mahmood726-cyber.github.io/e156/students.html).

---

## `[166]` Value of Information Calculator for Meta-Analysis Decision Support

**Type:** methods  |  ESTIMAND: EVPI and EVSI (dollars)  
**Data:** Pooled meta-analysis summary statistics with decision parameters

### 156-word body

When is conducting another trial justified given existing meta-analytic evidence, and how large should it be to maximize research returns? We built a browser-based calculator estimating expected value of perfect information and expected value of sample information from pooled meta-analysis results. The tool integrates posterior distributions with decision thresholds, net benefit parameters, and population sizes to compute EVPI, then generates EVSI curves across allocation. For a meta-analysis of 6 trials with pooled OR 0.32 (95% CI 0.18 to 0.51) and between-study variance 0.04, EVPI was 2.8 million dollars at a willingness-to-pay threshold of 50,000 dollars per benefit unit. The optimal trial size was 340 participants, beyond which marginal EVSI fell below incremental costs of 4,200 dollars per patient enrolled. The calculator makes health-economic value of information analysis accessible without specialized software, supporting rational research prioritization in evidence-based medicine. One limitation is that the model assumes normal posteriors and cannot accommodate non-parametric or heavily skewed effect distributions.

### Submission metadata

```
Corresponding author: Mahmood Ahmad <mahmood.ahmad2@nhs.net>
ORCID: 0000-0001-9107-3704
Affiliation: Tahir Heart Institute, Rabwah, Pakistan

Links:
  Code:      https://github.com/mahmood726-cyber/VOICalculator
  Protocol:  https://github.com/mahmood726-cyber/VOICalculator/blob/main/E156-PROTOCOL.md
  Dashboard: https://mahmood726-cyber.github.io/voicalculator/

References (topic pack: browser-based meta-analysis tooling):
  1. Schwarzer G, Carpenter JR, Rücker G. 2015. Meta-Analysis with R. Springer. doi:10.1007/978-3-319-21416-0
  2. Viechtbauer W. 2010. Conducting meta-analyses in R with the metafor package. J Stat Softw. 36(3):1-48. doi:10.18637/jss.v036.i03

Data availability: No patient-level data used. Analysis derived exclusively
  from publicly available aggregate records. All source identifiers are in
  the protocol document linked above.

Ethics: Not required. Study uses only publicly available aggregate data; no
  human participants; no patient-identifiable information; no individual-
  participant data. No institutional review board approval sought or required
  under standard research-ethics guidelines for secondary methodological
  research on published literature.

Funding: None.

Competing interests: MA serves on the editorial board of Synthēsis (the
  target journal); MA had no role in editorial decisions on this
  manuscript, which was handled by an independent editor of the journal.

Author contributions (CRediT):
  [STUDENT REWRITER, first author] — Writing – original draft, Writing –
    review & editing, Validation.
  [SUPERVISING FACULTY, last/senior author] — Supervision, Validation,
    Writing – review & editing.
  Mahmood Ahmad (middle author, NOT first or last) — Conceptualization,
    Methodology, Software, Data curation, Formal analysis, Resources.

AI disclosure: Computational tooling (including AI-assisted coding via
  Claude Code [Anthropic]) was used to develop analysis scripts and assist
  with data extraction. The final manuscript was human-written, reviewed,
  and approved by the author; the submitted text is not AI-generated. All
  quantitative claims were verified against source data; cross-validation
  was performed where applicable. The author retains full responsibility for
  the final content.

Preprint: Not preprinted.

Reporting checklist: PRISMA 2020 (methods-paper variant — reports on review corpus).

Target journal: ◆ Synthēsis (https://www.synthesis-medicine.org/index.php/journal)
  Section: Methods Note — submit the 156-word E156 body verbatim as the main text.
  The journal caps main text at ≤400 words; E156's 156-word, 7-sentence
  contract sits well inside that ceiling. Do NOT pad to 400 — the
  micro-paper length is the point of the format.

Manuscript license: CC-BY-4.0.
Code license: MIT.

SUBMITTED: [ ]
```


---

_Auto-generated from the workbook by `C:/E156/scripts/create_missing_protocols.py`. If something is wrong, edit `rewrite-workbook.txt` and re-run the script — it will overwrite this file via the GitHub API._