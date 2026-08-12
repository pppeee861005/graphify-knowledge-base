"""雙峽之戰預警引擎測試。"""

from __future__ import annotations

import json
import math
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from risk_engine import (  # noqa: E402
    DailyInput,
    InputValidationError,
    calculate_risk,
    classify_warning,
    save_result,
    score_oil,
    score_treasury,
)


class ScoreBoundaryTests(unittest.TestCase):
    def test_oil_boundaries(self) -> None:
        self.assertEqual(score_oil(-1.01), -1)
        self.assertEqual(score_oil(-1.0), 0)
        self.assertEqual(score_oil(1.0), 0)
        self.assertEqual(score_oil(1.01), 1)
        self.assertEqual(score_oil(2.0), 1)
        self.assertEqual(score_oil(2.01), 2)
        self.assertEqual(score_oil(4.0), 2)
        self.assertEqual(score_oil(4.01), 3)

    def test_treasury_boundaries(self) -> None:
        self.assertEqual(score_treasury(-8.01), -1)
        self.assertEqual(score_treasury(-8.0), 0)
        self.assertEqual(score_treasury(3.0), 0)
        self.assertEqual(score_treasury(3.01), 1)
        self.assertEqual(score_treasury(8.0), 1)
        self.assertEqual(score_treasury(8.01), 2)
        self.assertEqual(score_treasury(15.0), 2)
        self.assertEqual(score_treasury(15.01), 3)

    def test_warning_boundaries(self) -> None:
        self.assertEqual(classify_warning(0), "Risk-On")
        self.assertEqual(classify_warning(4), "Low Risk")
        self.assertEqual(classify_warning(7), "Caution")
        self.assertEqual(classify_warning(10), "Risk-Off")
        self.assertEqual(classify_warning(10.01), "Crisis Alert")


class ScenarioTests(unittest.TestCase):
    def _calculate(
        self,
        hormuz: int,
        red_sea: int,
        brent: float,
        us10y: float,
    ):
        return calculate_risk(
            DailyInput(
                date="2026-07-25",
                hormuz_risk=hormuz,
                red_sea_risk=red_sea,
                brent_daily_change_pct=brent,
                us10y_change_bp=us10y,
            )
        )

    def test_all_normal_is_risk_on(self) -> None:
        result = self._calculate(0, 0, 0, 0)
        self.assertEqual(result.total_score, 0)
        self.assertEqual(result.warning_level, "Risk-On")

    def test_hormuz_rhetoric_without_market_confirmation(self) -> None:
        result = self._calculate(1, 0, 0, 0)
        self.assertEqual(result.total_score, 2)
        self.assertEqual(result.warning_level, "Low Risk")

    def test_red_sea_attack_and_small_oil_rise(self) -> None:
        result = self._calculate(0, 2, 1.5, 0)
        self.assertEqual(result.total_score, 4)
        self.assertEqual(result.warning_level, "Low Risk")

    def test_both_straits_escalate(self) -> None:
        result = self._calculate(3, 3, 0, 0)
        self.assertEqual(result.total_score, 10.5)
        self.assertEqual(result.warning_level, "Crisis Alert")

    def test_oil_and_yield_shock(self) -> None:
        result = self._calculate(0, 0, 4.5, 16)
        self.assertEqual(result.total_score, 6)
        self.assertEqual(result.warning_level, "Caution")

    def test_geopolitics_without_market_confirmation(self) -> None:
        result = self._calculate(2, 2, -2, -9)
        self.assertEqual(result.total_score, 5)
        self.assertEqual(result.warning_level, "Caution")

    def test_day_zero_is_risk_off(self) -> None:
        result = self._calculate(3, 2, -3.9, -2)
        self.assertEqual(result.total_score, 8)
        self.assertEqual(result.warning_level, "Risk-Off")
        self.assertEqual(result.oil_score, -1)
        self.assertEqual(result.treasury_score, 0)


class ValidationAndPersistenceTests(unittest.TestCase):
    def test_invalid_risk_is_rejected(self) -> None:
        with self.assertRaisesRegex(InputValidationError, "hormuz_risk"):
            calculate_risk(
                DailyInput(
                    date="2026-07-25",
                    hormuz_risk=5,
                    red_sea_risk=0,
                    brent_daily_change_pct=0,
                    us10y_change_bp=0,
                )
            )

    def test_invalid_date_is_rejected(self) -> None:
        with self.assertRaisesRegex(InputValidationError, "YYYY-MM-DD"):
            calculate_risk(
                DailyInput(
                    date="2026-02-30",
                    hormuz_risk=0,
                    red_sea_risk=0,
                    brent_daily_change_pct=0,
                    us10y_change_bp=0,
                )
            )

    def test_non_finite_value_is_rejected(self) -> None:
        with self.assertRaisesRegex(InputValidationError, "NaN"):
            score_oil(math.nan)

    def test_saving_same_date_replaces_csv_row(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            csv_path = root / "daily.csv"
            json_path = root / "latest.json"
            report_path = root / "report.txt"

            first = calculate_risk(DailyInput("2026-07-25", 1, 1, 0, 0))
            revised = calculate_risk(DailyInput("2026-07-25", 3, 2, -3.9, -2))
            save_result(
                first,
                csv_path=csv_path,
                json_path=json_path,
                report_path=report_path,
            )
            save_result(
                revised,
                csv_path=csv_path,
                json_path=json_path,
                report_path=report_path,
            )

            csv_lines = csv_path.read_text(encoding="utf-8-sig").splitlines()
            self.assertEqual(len(csv_lines), 2)
            self.assertIn("Risk-Off", csv_lines[1])

            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["total_score"], 8)
            self.assertIn("## 資料", report_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

