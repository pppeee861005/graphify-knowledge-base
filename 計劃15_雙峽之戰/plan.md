我們先做一個很小的測試系統，不急著直接控制交易，也暫時不處理複雜的船舶 AIS 資料。

核心想法是把四個面向連起來：

Hormuz／紅海風險 → 原油價格 → 美國公債殖利率 → 美股 Risk-On／Risk-Off

一、第一版測試目標

建立一個 Python 小工具，每天產生一個美股風向預警：

🟢 Risk-On：風險偏低
🟡 Caution：提高警戒
🔴 Risk-Off：美股可能承壓
⚫ Crisis Alert：可能出現快速去風險

第一版只負責：

收集訊號
計算分數
說明原因
儲存每日結果

不自動下單、不預測精確點位。

二、第一版只用四個核心訊號
1. Hormuz Risk

先由你根據 World Monitor 人工輸入分數：

分數	狀態
0	正常
1	言論升高、軍演或零星事件
2	油輪聚集、船舶減速、軍事活動增加
3	船舶改道、港口受阻、實際攻擊
4	海峽嚴重中斷或接近封鎖

第一版採用人工判斷，是因為直接取得可靠的即時 AIS 船舶資料比較困難。

2. Red Sea Risk

同樣由 World Monitor 人工輸入：

分數	狀態
0	正常
1	威脅或警告
2	零星攻擊、保險與運費上升
3	多艘船改道好望角
4	主要航線大規模中斷
3. Oil Shock

觀察 Brent 原油單日漲跌：

Brent 單日變化	分數
下跌超過 1%	-1
-1%～+1%	0
上漲 1%～2%	1
上漲 2%～4%	2
上漲超過 4%	3

油價上漲本身不一定造成美股崩跌，但如果同時出現 Hormuz 或紅海異常，意義就不同。

4. US Treasury Shock

先觀察美國 10 年期公債殖利率的單日變化：

10Y 殖利率變化	分數
下降超過 8 basis points	-1
-8～+3 bp	0
上升 3～8 bp	1
上升 8～15 bp	2
上升超過 15 bp	3

這裡要注意：

油價升、殖利率升：市場擔心通膨，通常對成長股不利。
油價升、殖利率降：可能是避險資金進入美債。
油價跌、殖利率升：可能是利率或財政問題主導。
油價升、殖利率升、海峽風險升：最值得警戒。
三、簡單風險公式

第一版採用容易理解的加權：

總風險分數 =
Hormuz Risk × 2
+ Red Sea Risk × 1.5
+ Oil Shock
+ Treasury Shock

預警分類：

總分	預警
0 以下	🟢 Risk-On
0～4	🟢 Low Risk
4～7	🟡 Caution
7～10	🔴 Risk-Off
10 以上	⚫ Crisis Alert

Hormuz 權重比紅海高，是因為 Hormuz 對全球原油供應的直接影響通常更大。

四、第一個簡單測試案例

假設今天資料如下：

Hormuz Risk：2
Red Sea Risk：2
Brent 單日上漲：3.2%
美國10年期殖利率：上升10 bp

轉換成分數：

Hormuz：2 × 2 = 4
Red Sea：2 × 1.5 = 3
Oil Shock：2
Treasury Shock：2

總分：11

輸出：

預警等級：Crisis Alert

主要原因：
1. Hormuz 與紅海同時出現航運風險。
2. Brent 單日上漲3.2%，顯示能源風險已進入市場價格。
3. 美國10年期殖利率同步上升10 bp，代表市場可能提高通膨與利率預期。
4. 油價與殖利率同時上升，可能壓迫科技股估值及消費類股。

可能承壓：
- Nasdaq
- 高估值科技股
- 航空股
- 運輸股
- 高負債公司

可能相對抗跌：
- 能源股
- 國防股
- 部分商品股
五、系統架構

第一版保持簡單：

World Monitor
    ↓
人工輸入 Hormuz／Red Sea 分數
    ↓
自動或人工輸入 Oil／US Treasury 數據
    ↓
Python Risk Engine
    ↓
產生每日美股風向預警
    ↓
儲存 CSV、JSON 與文字報告

資料夾建議：

us_market_warning/
├─ app.py
├─ risk_engine.py
├─ data/
│  └─ daily_inputs.csv
├─ output/
│  ├─ latest_signal.json
│  └─ daily_report.txt
├─ tests/
│  └─ test_risk_engine.py
├─ requirements.txt
└─ README.md
六、第一階段測試計畫
階段 A：完全使用假資料

先建立六組情境：

全部正常
Hormuz 言論升高，但油價不動
紅海攻擊，油價小漲
Hormuz 與紅海同時升級
油價暴漲、殖利率暴漲
地緣風險升高，但市場沒有反應

測試目的不是判斷股市，而是確認：

分數計算正確
分類門檻正確
報告原因正確
不會把單一新聞直接判定為危機
階段 B：人工輸入真實資料

每天從 World Monitor 判斷：

Hormuz Risk：0～4
Red Sea Risk：0～4

再輸入：

Brent 單日變化
美國10年期殖利率變化

連續記錄七天。

階段 C：觀察預警是否領先美股

每天記錄預警後，再加入：

S&P 500 隔日漲跌
Nasdaq 隔日漲跌
能源股隔日漲跌
VIX 隔日變化

七天後檢查：

Risk-Off 後，美股是否真的較弱？
預警是領先還是落後？
哪個訊號權重太高？
油價與殖利率是否需要分開解讀？
七、可直接交給 Codex 的第一個任務
請建立一個名為 us_market_warning 的 Python 專案。

目標：
根據 Hormuz、Red Sea、Brent 原油及美國10年期公債殖利率，
產生美股 Risk-On、Low Risk、Caution、Risk-Off 或 Crisis Alert 預警。

第一版不要連接任何外部 API，全部使用人工輸入，方便測試。

輸入欄位：
1. date：日期
2. hormuz_risk：0到4
3. red_sea_risk：0到4
4. brent_daily_change_pct：Brent 單日百分比變化
5. us10y_change_bp：美國10年期殖利率單日 basis points 變化

評分規則：

Hormuz：
hormuz_score = hormuz_risk * 2

Red Sea：
red_sea_score = red_sea_risk * 1.5

Brent：
低於 -1%：-1分
-1%到1%：0分
1%到2%：1分
2%到4%：2分
高於4%：3分

US10Y：
低於 -8 bp：-1分
-8到3 bp：0分
3到8 bp：1分
8到15 bp：2分
高於15 bp：3分

總分：
total_score =
hormuz_score
+ red_sea_score
+ oil_score
+ treasury_score

預警：
total_score <= 0：Risk-On
0 < total_score <= 4：Low Risk
4 < total_score <= 7：Caution
7 < total_score <= 10：Risk-Off
total_score > 10：Crisis Alert

請建立：
- app.py：命令列輸入介面
- risk_engine.py：評分與分類邏輯
- tests/test_risk_engine.py：至少六個測試案例
- data/daily_inputs.csv：儲存每日輸入
- output/latest_signal.json：儲存最新結果
- output/daily_report.txt：產生繁體中文報告
- README.md：繁體中文使用說明
- requirements.txt

程式要求：
- 使用 Python type hints
- 加入輸入驗證
- 分數只能接受合理範圍
- 發生錯誤時顯示清楚訊息
- 不得包含自動交易或下單功能
- 報告必須區分「資料」、「推論」與「風險提醒」
- 執行 pytest 必須全部通過

完成後請先顯示專案目錄，再逐一建立檔案並執行測試。
八、這個模型最重要的判斷

我們不是單純地說：

Hormuz 出事，所以美股會跌。

而是觀察一條完整的傳導鏈：

地緣政治異常
    ↓
船舶、港口或航線受到影響
    ↓
Brent 原油開始反應
    ↓
通膨預期與美債殖利率反應
    ↓
美股估值與風險偏好受到影響

第一版的成功標準不是「預測每一次漲跌」，而是能正確回答：

這次地緣政治新聞，有沒有真正穿透到能源市場與債券市場？

只有穿透到油價與美債，才提高美股風向預警。

