# VOICalculator — Code Review Findings

**Reviewer:** Claude Opus 4.6 (1M context)
**Date:** 2026-04-03
**File:** voi-calculator.html (1,768 lines)

## P0 — Critical (must fix)

### P0-1: Missing skip-nav link
**Issue:** No skip navigation link for keyboard/screen reader users. Keyboard users must tab through header and all tab buttons before reaching form inputs.
**Fix:** Add `<a href="#panel-input" class="sr-only" style="...">Skip to content</a>` before header.

## P1 — Important

### P1-1: EVPI formula uses simplified P(wrong) = min-tail approach
**Lines:** 798-803
**Issue:** The EVPI calculation first computes direction-aware P(wrong), then overrides with `Math.min(normalCDF(z), 1-normalCDF(z))`. This is actually correct for the decision-theoretic VOI framework (the optimal decision always picks the side with more mass), but the intermediate code (lines 770-796) is dead code that is never used.
**Recommendation:** Remove the dead intermediate `pWrong` calculations for clarity.

### P1-2: `csvSafe` function is well-implemented
**Lines:** 712-720
**Status:** PASS — correctly guards against `=+@\t\r` without blocking leading minus. Good.

### P1-3: `escapeHtml` function is complete
**Lines:** 701-709
**Status:** PASS — escapes `&`, `<`, `>`, `"`, `'`. Correctly used throughout innerHTML generation.

## P2 — Minor

### P2-1: `.sr-only` class defined but skip-nav link missing
**Line:** 518
**Issue:** The utility class exists but no skip-nav element uses it.

### P2-2: Tab arrow key navigation is correctly implemented
**Lines:** 1597-1621
**Status:** PASS — ArrowRight/Left/Home/End all work correctly per ARIA tabs pattern.

### P2-3: Blob URL properly revoked
**Lines:** 1496-1504
**Status:** PASS — `URL.revokeObjectURL(url)` called after download.

### P2-4: `</html>` closing tag present
**Line:** 1768
**Status:** PASS.

## Summary

| Severity | Count |
|----------|-------|
| P0       | 1     |
| P1       | 1     |
| P2       | 4     |

## Statistics Verification

- **Normal CDF (Abramowitz & Stegun):** Lines 742-757. Uses Horner form with correct coefficients. PASS.
- **EVPI = Npop * P(wrong) * NetBenefit:** Standard Claxton (1999) formulation. PASS.
- **EVSI posterior precision = prior precision + new data precision:** Correct Bayesian updating. PASS.
- **Optimal n = argmax(EVSI - cost):** Standard VOI framework. PASS.
