# voicalculator

Value of Information Calculator for Meta-Analysis Decision Support.

A single-file, offline browser tool (`voi-calculator.html`) that computes the
expected value of perfect information (EVPI) and expected value of sample
information (EVSI) from meta-analysis summary statistics.

## What it does

Given a pooled effect estimate, its standard error, between-study variance
(tau-squared), a decision threshold, net benefit per correct decision, and the
affected population size, the tool computes:

- **EVPI** from a normal posterior: `sigma_total = sqrt(SE^2 + tau^2)`,
  `P(wrong) = min(Phi(z), 1 - Phi(z))` with `z = (threshold - mu) / sigma_total`,
  and `EVPI = N_pop * P(wrong) * net_benefit`.
- **EVSI** across a range of hypothetical trial sizes (10 to 50,000 participants)
  by updating posterior precision with anticipated data precision, and identifies
  the sample size that maximises net benefit (EVSI minus trial cost).

Two worked clinical examples are included (tranexamic acid; intensive glucose
control). The normal CDF uses the Abramowitz & Stegun rational approximation.
The page has no external dependencies and runs offline.

## Tests

`test_voi_calculator.py` runs 20 Selenium tests (headless Chrome) covering the
normal CDF, EVPI/EVSI computation, the EVSI curve, CSV/HTML escaping, tab
navigation, dark mode, and the built-in examples.

```
python -m pytest -q
```
