"""雙峽之戰美股風向預警命令列介面。"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from risk_engine import DailyInput, InputValidationError, calculate_risk, save_result


PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_CSV = PROJECT_DIR / "data" / "daily_inputs.csv"
DEFAULT_JSON = PROJECT_DIR / "output" / "latest_signal.json"
DEFAULT_REPORT = PROJECT_DIR / "output" / "daily_report.txt"


def _prompt_if_missing(value: object | None, prompt: str, converter: type) -> object:
    if value is not None:
        return value
    return converter(input(prompt).strip())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="根據雙峽、Brent與美國10Y變化產生美股風向預警。",
    )
    parser.add_argument("--date", dest="input_date", help="日期，格式YYYY-MM-DD")
    parser.add_argument("--hormuz-risk", type=int, help="霍爾木茲風險，0至4")
    parser.add_argument("--red-sea-risk", type=int, help="紅海／曼德海峽風險，0至4")
    parser.add_argument("--brent-change", type=float, help="Brent單日百分比變化")
    parser.add_argument("--us10y-change", type=float, help="美國10Y單日基點變化")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        input_date = _prompt_if_missing(
            args.input_date,
            f"日期 [{date.today().isoformat()}]：",
            str,
        )
        if not str(input_date):
            input_date = date.today().isoformat()

        daily_input = DailyInput(
            date=str(input_date),
            hormuz_risk=int(
                _prompt_if_missing(args.hormuz_risk, "Hormuz Risk（0-4）：", int)
            ),
            red_sea_risk=int(
                _prompt_if_missing(args.red_sea_risk, "Red Sea Risk（0-4）：", int)
            ),
            brent_daily_change_pct=float(
                _prompt_if_missing(
                    args.brent_change,
                    "Brent單日變化（%）：",
                    float,
                )
            ),
            us10y_change_bp=float(
                _prompt_if_missing(
                    args.us10y_change,
                    "美國10Y殖利率單日變化（bp）：",
                    float,
                )
            ),
        )
        result = calculate_risk(daily_input)
        save_result(
            result,
            csv_path=DEFAULT_CSV,
            json_path=DEFAULT_JSON,
            report_path=DEFAULT_REPORT,
        )
    except (InputValidationError, ValueError) as exc:
        print(f"輸入錯誤：{exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"檔案寫入失敗：{exc}", file=sys.stderr)
        return 3

    print(f"日期：{result.date}")
    print(f"總分：{result.total_score:.1f}")
    print(f"預警：{result.warning_level}")
    print("主要原因：")
    for index, reason in enumerate(result.reasons, 1):
        print(f"  {index}. {reason}")
    print(f"報告：{DEFAULT_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

