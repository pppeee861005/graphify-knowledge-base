# 雙峽之戰美股風向預警 MVP

這是一個規則式危機監測工具，根據霍爾木茲海峽、紅海／曼德海峽、Brent原油與美國十年期公債殖利率，產生每日美股風向預警。

本工具不連接外部API、不預測精確點位，也不包含自動交易或下單功能。

## 評分公式

```text
總分 =
Hormuz Risk × 2
+ Red Sea Risk × 1.5
+ Oil Shock
+ Treasury Shock
```

### 預警門檻

| 總分 | 預警 |
|---:|---|
| ≤ 0 | Risk-On |
| 0–4 | Low Risk |
| 4–7 | Caution |
| 7–10 | Risk-Off |
| > 10 | Crisis Alert |

邊界採「右側包含」規則。例如總分正好為4是Low Risk，正好為7是Caution，正好為10是Risk-Off。

## 執行方式

### 互動輸入

```powershell
python app.py
```

### 命令列參數

```powershell
python app.py `
  --date 2026-07-25 `
  --hormuz-risk 3 `
  --red-sea-risk 2 `
  --brent-change -3.9 `
  --us10y-change -2
```

執行後會更新：

- `data/daily_inputs.csv`：每日歷史資料；相同日期會覆寫，不會重複新增。
- `output/latest_signal.json`：最新結構化結果。
- `output/daily_report.txt`：最新繁體中文報告。

## 人工風險定義

### Hormuz Risk

| 分數 | 狀態 |
|---:|---|
| 0 | 正常 |
| 1 | 言論升高、軍演或零星事件 |
| 2 | 油輪聚集、船舶減速或軍事活動增加 |
| 3 | 船舶改道、港口受阻或實際攻擊 |
| 4 | 嚴重中斷或接近全面封鎖 |

### Red Sea Risk

| 分數 | 狀態 |
|---:|---|
| 0 | 正常 |
| 1 | 威脅或警告 |
| 2 | 零星攻擊、保險或運費上升 |
| 3 | 多艘船改道好望角 |
| 4 | 主要航線大規模中斷 |

World Monitor的0至100分是網站自己的監測分數，不可直接輸入本模型。人工分數必須結合事件核查與實際航運證據。

## 執行測試

不安裝額外套件也可使用Python內建測試：

```powershell
python -m unittest discover -s tests -v
```

安裝requirements後亦可使用pytest：

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
```

測試涵蓋評分邊界、六種情境、Day 0、輸入驗證及檔案覆寫行為。

## Day 0

第一筆正式基準資料：

```text
日期：2026-07-25
Hormuz Risk：3
Red Sea Risk：2
Brent：−3.9%
US10Y：−2 bp
總分：8.0
預警：Risk-Off
```

這代表前線與航運風險已進入去風險區，但最近交易日尚未出現油價與美債殖利率同步上升。

