"""雙峽之戰美股風向預警引擎。

本模組只進行資料驗證、規則評分與報告保存，不包含投資下單功能。
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Final


WARNING_RISK_ON: Final = "Risk-On"
WARNING_LOW_RISK: Final = "Low Risk"
WARNING_CAUTION: Final = "Caution"
WARNING_RISK_OFF: Final = "Risk-Off"
WARNING_CRISIS: Final = "Crisis Alert"

CSV_FIELDS: Final = [
    "date",
    "hormuz_risk",
    "red_sea_risk",
    "brent_daily_change_pct",
    "us10y_change_bp",
    "hormuz_score",
    "red_sea_score",
    "oil_score",
    "treasury_score",
    "total_score",
    "warning_level",
]


class InputValidationError(ValueError):
    """輸入資料不符合模型規則。"""


@dataclass(frozen=True)
class DailyInput:
    """每日模型輸入。"""

    date: str
    hormuz_risk: int
    red_sea_risk: int
    brent_daily_change_pct: float
    us10y_change_bp: float

    def validate(self) -> None:
        """驗證日期、分數範圍與數值有效性。"""

        try:
            date.fromisoformat(self.date)
        except ValueError as exc:
            raise InputValidationError("date 必須是有效的 YYYY-MM-DD 日期。") from exc

        _validate_risk("hormuz_risk", self.hormuz_risk)
        _validate_risk("red_sea_risk", self.red_sea_risk)
        _validate_finite("brent_daily_change_pct", self.brent_daily_change_pct)
        _validate_finite("us10y_change_bp", self.us10y_change_bp)

        if not -100.0 <= self.brent_daily_change_pct <= 100.0:
            raise InputValidationError(
                "brent_daily_change_pct 必須介於 -100 到 100 之間。"
            )
        if not -500.0 <= self.us10y_change_bp <= 500.0:
            raise InputValidationError("us10y_change_bp 必須介於 -500 到 500 之間。")


@dataclass(frozen=True)
class RiskResult:
    """完整評分結果。"""

    date: str
    hormuz_risk: int
    red_sea_risk: int
    brent_daily_change_pct: float
    us10y_change_bp: float
    hormuz_score: float
    red_sea_score: float
    oil_score: int
    treasury_score: int
    total_score: float
    warning_level: str
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        """轉換為可序列化字典。"""

        payload = asdict(self)
        payload["reasons"] = list(self.reasons)
        return payload

    def to_csv_row(self) -> dict[str, object]:
        """輸出CSV所需欄位。"""

        payload = self.to_dict()
        return {field: payload[field] for field in CSV_FIELDS}


def _validate_risk(field_name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise InputValidationError(f"{field_name} 必須是 0 到 4 的整數。")
    if not 0 <= value <= 4:
        raise InputValidationError(f"{field_name} 必須介於 0 到 4。")


def _validate_finite(field_name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InputValidationError(f"{field_name} 必須是數字。")
    if not math.isfinite(float(value)):
        raise InputValidationError(f"{field_name} 不可為 NaN 或無限大。")


def score_oil(change_pct: float) -> int:
    """將Brent單日百分比變化轉換為油價衝擊分數。"""

    _validate_finite("brent_daily_change_pct", change_pct)
    if change_pct < -1.0:
        return -1
    if change_pct <= 1.0:
        return 0
    if change_pct <= 2.0:
        return 1
    if change_pct <= 4.0:
        return 2
    return 3


def score_treasury(change_bp: float) -> int:
    """將美國十年期殖利率單日基點變化轉換為分數。"""

    _validate_finite("us10y_change_bp", change_bp)
    if change_bp < -8.0:
        return -1
    if change_bp <= 3.0:
        return 0
    if change_bp <= 8.0:
        return 1
    if change_bp <= 15.0:
        return 2
    return 3


def classify_warning(total_score: float) -> str:
    """依總分回傳預警等級。"""

    _validate_finite("total_score", total_score)
    if total_score <= 0:
        return WARNING_RISK_ON
    if total_score <= 4:
        return WARNING_LOW_RISK
    if total_score <= 7:
        return WARNING_CAUTION
    if total_score <= 10:
        return WARNING_RISK_OFF
    return WARNING_CRISIS


def calculate_risk(daily_input: DailyInput) -> RiskResult:
    """驗證輸入並計算完整風險結果。"""

    daily_input.validate()

    hormuz_score = daily_input.hormuz_risk * 2.0
    red_sea_score = daily_input.red_sea_risk * 1.5
    oil_score = score_oil(daily_input.brent_daily_change_pct)
    treasury_score = score_treasury(daily_input.us10y_change_bp)
    total_score = round(
        hormuz_score + red_sea_score + oil_score + treasury_score, 2
    )
    warning_level = classify_warning(total_score)

    reasons = _build_reasons(
        daily_input,
        oil_score=oil_score,
        treasury_score=treasury_score,
        warning_level=warning_level,
    )

    return RiskResult(
        date=daily_input.date,
        hormuz_risk=daily_input.hormuz_risk,
        red_sea_risk=daily_input.red_sea_risk,
        brent_daily_change_pct=float(daily_input.brent_daily_change_pct),
        us10y_change_bp=float(daily_input.us10y_change_bp),
        hormuz_score=hormuz_score,
        red_sea_score=red_sea_score,
        oil_score=oil_score,
        treasury_score=treasury_score,
        total_score=total_score,
        warning_level=warning_level,
        reasons=reasons,
    )


def _build_reasons(
    daily_input: DailyInput,
    *,
    oil_score: int,
    treasury_score: int,
    warning_level: str,
) -> tuple[str, ...]:
    reasons: list[str] = []

    if daily_input.hormuz_risk >= 3:
        reasons.append("霍爾木茲已出現實際攻擊、改道或嚴重通行中斷風險。")
    elif daily_input.hormuz_risk >= 1:
        reasons.append("霍爾木茲軍事或航運風險高於正常基準。")

    if daily_input.red_sea_risk >= 3:
        reasons.append("紅海／曼德海峽已出現大規模改道或航線中斷風險。")
    elif daily_input.red_sea_risk >= 1:
        reasons.append("紅海／曼德海峽出現威脅、警告或零星攻擊。")

    if oil_score >= 2:
        reasons.append("Brent明顯上漲，前線風險正在穿透能源價格。")
    elif oil_score == -1:
        reasons.append("Brent單日回落，暫時抵銷部分能源衝擊分數。")

    if treasury_score >= 2:
        reasons.append("美國十年期殖利率明顯上升，債市傳導風險增加。")
    elif treasury_score == -1:
        reasons.append("美國十年期殖利率明顯下降，可能反映避險買盤。")

    if (
        daily_input.hormuz_risk >= 2
        and daily_input.red_sea_risk >= 2
        and oil_score >= 1
        and treasury_score >= 1
    ):
        reasons.append("雙峽、油價與殖利率同步升高，符合完整傳導警戒組合。")
    elif warning_level in {WARNING_RISK_OFF, WARNING_CRISIS}:
        reasons.append("總分已進入去風險區，但仍須確認油價與債市是否同步惡化。")

    if not reasons:
        reasons.append("四項核心訊號均接近正常基準。")

    return tuple(reasons)


def render_report(result: RiskResult) -> str:
    """產生區分資料、推論與風險提醒的繁體中文報告。"""

    reason_lines = "\n".join(f"{index}. {reason}" for index, reason in enumerate(result.reasons, 1))
    transmission = (
        "已出現油價與債市同步傳導。"
        if result.oil_score >= 1 and result.treasury_score >= 1
        else "尚未確認油價與債市同步惡化。"
    )

    return f"""# 雙峽之戰每日美股風向預警

## 結論

- 日期：{result.date}
- 總分：{result.total_score:.1f}
- 預警：{result.warning_level}

## 資料

| 指標 | 輸入 | 分數貢獻 |
|---|---:|---:|
| Hormuz Risk | {result.hormuz_risk}/4 | {result.hormuz_score:.1f} |
| Red Sea Risk | {result.red_sea_risk}/4 | {result.red_sea_score:.1f} |
| Brent單日變化 | {result.brent_daily_change_pct:+.2f}% | {result.oil_score:+d} |
| 美國10Y殖利率變化 | {result.us10y_change_bp:+.1f} bp | {result.treasury_score:+d} |

## 推論

{reason_lines}

危機傳導判斷：{transmission}

## 風險提醒

- 本結果是規則式監測訊號，不是精確點位預測。
- World Monitor分數不可直接當作本模型的0至4分輸入。
- 未經交叉核實的交戰方聲稱，不應直接提高人工風險分數。
- 本工具不提供投資建議，也不包含自動交易或下單功能。
"""


def save_result(
    result: RiskResult,
    *,
    csv_path: Path,
    json_path: Path,
    report_path: Path,
) -> None:
    """以日期覆寫或新增CSV紀錄，並保存最新JSON及文字報告。"""

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    if csv_path.exists():
        with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames != CSV_FIELDS:
                raise ValueError("既有CSV欄位與目前版本不相容，請先備份後移除。")
            rows = list(reader)

    new_row = {key: str(value) for key, value in result.to_csv_row().items()}
    replaced = False
    for index, row in enumerate(rows):
        if row["date"] == result.date:
            rows[index] = new_row
            replaced = True
            break
    if not replaced:
        rows.append(new_row)
    rows.sort(key=lambda row: row["date"])

    with csv_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    json_path.write_text(
        json.dumps(result.to_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    report_path.write_text(render_report(result), encoding="utf-8")

