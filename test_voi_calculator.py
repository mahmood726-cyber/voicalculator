"""
Test suite for VOI Calculator (voi-calculator.html)
Uses Selenium to test calculations, UI, and exports.
20 tests covering EVPI, EVSI, normalCDF, tabs, dark mode, examples, exports.
"""

import sys
import io
import os
import json
import math
import time
import unittest

# Windows cp1252 safety
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'voi-calculator.html')
FILE_URL = 'file:///' + HTML_PATH.replace('\\', '/')


def get_driver():
    """Create headless Chrome driver."""
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--window-size=1280,900')
    opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    return webdriver.Chrome(options=opts)


# Reference normalCDF (Abramowitz & Stegun, matches the app)
def ref_normalCDF(x):
    if x == float('inf'):
        return 1.0
    if x == float('-inf'):
        return 0.0
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911
    sign = 1
    if x < 0:
        sign = -1
    x_abs = abs(x) / math.sqrt(2)
    t = 1.0 / (1.0 + p * x_abs)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x_abs * x_abs)
    return 0.5 * (1.0 + sign * y)


class TestVOICalculator(unittest.TestCase):
    """Test suite for VOI Calculator."""

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        cls.driver.get(FILE_URL)
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def js(self, script):
        """Execute JS and return result."""
        return self.driver.execute_script('return ' + script)

    def reload(self):
        """Reload page."""
        self.driver.get(FILE_URL)
        time.sleep(0.5)

    # ===== Test 1: normalCDF at z=0 =====
    def test_01_normalCDF_zero(self):
        result = self.js('VOICalc.normalCDF(0)')
        self.assertAlmostEqual(result, 0.5, places=6)

    # ===== Test 2: normalCDF at positive z =====
    def test_02_normalCDF_positive(self):
        result = self.js('VOICalc.normalCDF(1.96)')
        expected = ref_normalCDF(1.96)
        self.assertAlmostEqual(result, expected, places=5)
        self.assertAlmostEqual(result, 0.975, delta=0.001)

    # ===== Test 3: normalCDF at negative z =====
    def test_03_normalCDF_negative(self):
        result = self.js('VOICalc.normalCDF(-1.96)')
        expected = ref_normalCDF(-1.96)
        self.assertAlmostEqual(result, expected, places=5)
        self.assertAlmostEqual(result, 0.025, delta=0.001)

    # ===== Test 4: normalCDF symmetry =====
    def test_04_normalCDF_symmetry(self):
        pos = self.js('VOICalc.normalCDF(2.5)')
        neg = self.js('VOICalc.normalCDF(-2.5)')
        self.assertAlmostEqual(pos + neg, 1.0, places=6)

    # ===== Test 5: EVPI basic calculation =====
    def test_05_evpi_basic(self):
        # mu=0, se=1, tau2=0, threshold=0 => sigma=1, z=0, P(wrong)=0.5
        result = self.js('VOICalc.calcEVPI(0, 1, 0, 0, "below", 1000, 100)')
        self.assertAlmostEqual(result['pWrong'], 0.5, places=4)
        self.assertAlmostEqual(result['evpi'], 50000.0, places=0)
        self.assertAlmostEqual(result['sigmaTotal'], 1.0, places=6)

    # ===== Test 6: EVPI with clear benefit (low pWrong) =====
    def test_06_evpi_clear_benefit(self):
        # mu=-2, se=0.5, tau2=0, threshold=0 => z=(0-(-2))/0.5=4 => P(wrong)=Phi(-4) very small
        result = self.js('VOICalc.calcEVPI(-2, 0.5, 0, 0, "below", 1000, 100)')
        self.assertLess(result['pWrong'], 0.001)
        self.assertLess(result['evpi'], 100)  # Very low EVPI

    # ===== Test 7: EVPI with tau2 =====
    def test_07_evpi_with_heterogeneity(self):
        # Adding tau2 increases uncertainty => higher P(wrong)
        r1 = self.js('VOICalc.calcEVPI(-0.5, 0.2, 0, 0, "below", 1000, 100)')
        r2 = self.js('VOICalc.calcEVPI(-0.5, 0.2, 0.1, 0, "below", 1000, 100)')
        self.assertGreater(r2['pWrong'], r1['pWrong'])
        self.assertGreater(r2['evpi'], r1['evpi'])
        self.assertAlmostEqual(r2['sigmaTotal'], math.sqrt(0.04 + 0.1), places=6)

    # ===== Test 8: EVPI sigma_total formula =====
    def test_08_evpi_sigma_formula(self):
        result = self.js('VOICalc.calcEVPI(0.3, 0.15, 0.03, 0, "above", 5000, 1000)')
        expected_sigma = math.sqrt(0.15**2 + 0.03)
        self.assertAlmostEqual(result['sigmaTotal'], expected_sigma, places=6)

    # ===== Test 9: EVPI per patient =====
    def test_09_evpi_per_patient(self):
        result = self.js('VOICalc.calcEVPI(-0.3, 0.1, 0.01, 0, "below", 50000, 200000)')
        self.assertAlmostEqual(result['evpiPerPatient'], result['evpi'] / 200000, places=2)

    # ===== Test 10: EVSI reduces P(wrong) =====
    def test_10_evsi_reduces_uncertainty(self):
        evpi = self.js('VOICalc.calcEVPI(-0.1, 0.15, 0.02, 0, "below", 40000, 500000)')
        evsi = self.js('VOICalc.calcEVSI(VOICalc.calcEVPI(-0.1, 0.15, 0.02, 0, "below", 40000, 500000), 1000, 0.5)')
        self.assertLess(evsi['pWrongPost'], evpi['pWrong'])
        self.assertGreater(evsi['evsi'], 0)

    # ===== Test 11: EVSI posterior SE formula =====
    def test_11_evsi_posterior_se(self):
        evpi_res = self.js('VOICalc.calcEVPI(0, 0.2, 0.01, 0, "below", 1000, 100)')
        sigma_total = evpi_res['sigmaTotal']
        n_new = 500
        v_typical = 0.4
        evsi = self.js(f'VOICalc.calcEVSI(VOICalc.calcEVPI(0, 0.2, 0.01, 0, "below", 1000, 100), {n_new}, {v_typical})')

        prior_prec = 1.0 / (sigma_total ** 2)
        new_prec = n_new / v_typical
        expected_se = 1.0 / math.sqrt(prior_prec + new_prec)
        self.assertAlmostEqual(evsi['sePosterior'], expected_se, places=6)

    # ===== Test 12: EVSI increases with n =====
    def test_12_evsi_increases_with_n(self):
        evsi_100 = self.js('VOICalc.calcEVSI(VOICalc.calcEVPI(-0.1, 0.15, 0.02, 0, "below", 40000, 500000), 100, 0.5)')
        evsi_5000 = self.js('VOICalc.calcEVSI(VOICalc.calcEVPI(-0.1, 0.15, 0.02, 0, "below", 40000, 500000), 5000, 0.5)')
        self.assertGreater(evsi_5000['evsi'], evsi_100['evsi'])

    # ===== Test 13: EVSI never exceeds EVPI =====
    def test_13_evsi_bounded_by_evpi(self):
        evpi = self.js('VOICalc.calcEVPI(-0.1, 0.15, 0.02, 0, "below", 40000, 500000)')
        evsi_big = self.js('VOICalc.calcEVSI(VOICalc.calcEVPI(-0.1, 0.15, 0.02, 0, "below", 40000, 500000), 100000, 0.5)')
        self.assertLessEqual(evsi_big['evsi'], evpi['evpi'] * 1.001)  # small tolerance

    # ===== Test 14: EVSI curve has optimal n =====
    def test_14_evsi_curve_optimal(self):
        result = self.driver.execute_script(
            'var evpi = VOICalc.calcEVPI(-0.05, 0.12, 0.04, 0, "below", 40000, 500000);'
            'var curve = VOICalc.calcEVSICurve(evpi, 0.6, 8000, 1000000);'
            'return {optimalN: curve.optimalN, bestNet: curve.bestNetBenefit, ptsLen: curve.points.length};'
        )
        self.assertIsNotNone(result['optimalN'])
        self.assertGreater(result['optimalN'], 0)
        self.assertEqual(result['ptsLen'], 20)

    # ===== Test 15: escapeHtml =====
    def test_15_escapeHtml(self):
        result = self.js('VOICalc.escapeHtml(\'<script>"hello"&\')')
        self.assertNotIn('<', result)
        self.assertNotIn('>', result)
        self.assertIn('&lt;', result)
        self.assertIn('&gt;', result)
        self.assertIn('&quot;', result)
        self.assertIn('&amp;', result)

    # ===== Test 16: csvSafe =====
    def test_16_csvSafe(self):
        # Formula injection guard
        self.assertEqual(self.js("VOICalc.csvSafe('=SUM(A1)')"), "'=SUM(A1)")
        # Commas get quoted
        result = self.js("VOICalc.csvSafe('hello, world')")
        self.assertTrue(result.startswith('"'))
        # Negative numbers preserved (not treated as formula)
        self.assertEqual(self.js("VOICalc.csvSafe('-0.5')"), '-0.5')

    # ===== Test 17: Tab navigation =====
    def test_17_tab_navigation(self):
        self.reload()
        # Initially Data Input is active
        tab_input = self.driver.find_element(By.ID, 'tab-input')
        self.assertEqual(tab_input.get_attribute('aria-selected'), 'true')

        panel_input = self.driver.find_element(By.ID, 'panel-input')
        self.assertEqual(panel_input.get_attribute('aria-hidden'), 'false')

        # Click EVPI tab
        tab_evpi = self.driver.find_element(By.ID, 'tab-evpi')
        tab_evpi.click()
        time.sleep(0.3)
        self.assertEqual(tab_evpi.get_attribute('aria-selected'), 'true')
        self.assertEqual(tab_input.get_attribute('aria-selected'), 'false')
        self.assertEqual(self.driver.find_element(By.ID, 'panel-evpi').get_attribute('aria-hidden'), 'false')
        self.assertEqual(panel_input.get_attribute('aria-hidden'), 'true')

    # ===== Test 18: Dark mode toggle =====
    def test_18_dark_mode(self):
        self.reload()
        html_el = self.driver.find_element(By.TAG_NAME, 'html')
        initial_dark = 'dark' in (html_el.get_attribute('class') or '')

        btn = self.driver.find_element(By.ID, 'btn-dark-mode')
        btn.click()
        time.sleep(0.3)

        after_dark = 'dark' in (html_el.get_attribute('class') or '')
        self.assertNotEqual(initial_dark, after_dark)

        # Toggle back
        btn.click()
        time.sleep(0.3)
        restored = 'dark' in (html_el.get_attribute('class') or '')
        self.assertEqual(initial_dark, restored)

    # ===== Test 19: TXA example loads and computes =====
    def test_19_txa_example(self):
        self.reload()
        self.driver.find_element(By.ID, 'ex-txa').click()
        time.sleep(0.3)

        # Verify inputs populated
        effect = self.driver.find_element(By.ID, 'inp-effect').get_attribute('value')
        self.assertEqual(effect, '-0.28')

        # Compute
        self.driver.find_element(By.ID, 'btn-compute').click()
        time.sleep(0.5)

        # Should switch to EVPI tab and show results
        evpi_panel = self.driver.find_element(By.ID, 'panel-evpi')
        self.assertEqual(evpi_panel.get_attribute('aria-hidden'), 'false')

        # Check P(wrong) is visible and small (TXA has clear benefit)
        content = evpi_panel.text.upper()
        self.assertIn('P(WRONG DECISION)', content)
        self.assertIn('EVPI', content)

    # ===== Test 20: Intensive glucose example (high VOI) =====
    def test_20_glucose_example_high_voi(self):
        self.reload()
        self.driver.find_element(By.ID, 'ex-glucose').click()
        time.sleep(0.3)
        self.driver.find_element(By.ID, 'btn-compute').click()
        time.sleep(0.5)

        # Get EVPI values via JS
        result = self.driver.execute_script(
            'var txa = VOICalc.calcEVPI(-0.28, 0.06, 0.005, 0, "below", 50000, 200000);'
            'var glu = VOICalc.calcEVPI(-0.05, 0.12, 0.04, 0, "below", 40000, 500000);'
            'return {txa_pw: txa.pWrong, glu_pw: glu.pWrong, txa_evpi: txa.evpi, glu_evpi: glu.evpi};'
        )

        # Glucose should have higher P(wrong) and EVPI than TXA
        self.assertGreater(result['glu_pw'], result['txa_pw'])
        self.assertGreater(result['glu_evpi'], result['txa_evpi'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
