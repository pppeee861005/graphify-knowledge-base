# E04｜Workflow：從 Prompt 到代碼，蜂群的編程語言

**《AI 指揮官筆記》蜂群 Agent 系列 · S01E04 實踐篇**

---

## 📋 文章規格

| 項目 | 內容 |
|------|------|
| 字數 | 2,800-3,500 字 |
| 閱讀時間 | 10-12 分鐘 |
| 發布日期 | 待定（建議 6 月初） |
| 狀態 | 📝 大綱階段 |
| 定位 | Agent 系列第 4 篇（實踐篇） |

---

## 🎯 本篇目標

1. **解決的問題**：前三篇講了「蜂群是什麼、為什麼、怎麼設計」，但沒說「怎麼寫代碼」
2. **核心觀點**：Workflow 就是蜂群的編程語言
3. **實踐收穫**：讀者能看懂一個真實的 Workflow 腳本
4. **戰略意義**：從「理論認知」升級到「可執行方案」

---

## 📝 文章大綱

### 一、開場：一個建築師的困境（500 字）

**場景設定**：

> 「我讀完前三篇 Agent 文章了。蜂群的架構很美，三層分離很優雅，可適應性也無敵。
>
> 但有一個問題——我怎麼寫代碼？
>
> 我是不是要用 Python 寫個複雜的 Agent 框架？要自己管理 Session、Harness、Brain 三層嗎？」

**轉折**：
- Anthropic 已經替我們解決了這個問題
- 他們在 Claude Code V2.1.47 推出的 **Workflow** 功能，就是「蜂群的編程語言」
- 不需要自己造輪子，只需要寫 JavaScript 定義流程

**預告**：
- 今天我們要看的，是 Prompt 和 Workflow 的根本區別
- 以及為什麼這個區別很重要

---

### 二、衝突：Prompt vs Workflow（800 字）

#### **舊做法：用 Prompt 指揮 Agent**

```
你：「幫我審查這段代碼」

Claude：
- 自己決定怎麼審查
- 自己決定查哪些方面
- 自己決定輸出什麼格式
```

**問題**：
- 結果不可預測
- 流程無法控制
- 難以複用和優化
- 多 Agent 協作困難（各自為政）

#### **新做法：用 Workflow 定義流程**

```javascript
// 不是「做什麼」，而是「怎麼組織」
Stage 1: Agent.語法檢查()
Stage 2: Agent.邏輯審查() + Agent.性能分析()  // 並行
Stage 3: Agent.生成報告()
```

**優勢**：
- 流程明確、可控
- 每個 Agent 職責清晰
- 結果可預測
- 易於監控和調整

#### **類比：從烹飪配方到餐廳工作流**

> 傳統 Prompt = 對廚師說「做一道好吃的菜」
>
> Workflow = 「明確的餐廳流程」：
> - 前檯接單
> - 廚房切食材
> - 炉火烹飪
> - 配菜員擺盤
> - 服務員上菜
>
> 結果完全不同。

---

### 三、轉折：Workflow 的本質（700 字）

#### **Workflow 是什麼？**

> 用 JavaScript 代碼定義 Agent 的協作方式，而不是靠 Prompt 的「臨場發揮」

#### **三個核心轉變**

**1. 從「指令式」到「聲明式」**

```
// 指令式（Prompt）
「請分析這個數據，給我洞見」

// 聲明式（Workflow）
const workflow = {
  Stage1: cleanData(),
  Stage2: analyze(),
  Stage3: generateInsights()
}
```

前者問「做什麼」，後者定義「結構是什麼」。

**2. 從「黑箱」到「透明盒」**

傳統 Agent：
```
Input → [黑箱] → Output
（你不知道中間發生了什麼）
```

Workflow Agent：
```
Input → Stage1 → Stage2 → Stage3 → Output
（每一步都可見、可測、可優化）
```

**3. 從「一次性」到「可複用」**

- Prompt：用一次就廢
- Workflow：腳本可以保存、分享、複用、迭代

#### **Workflow 的 JS 腳本結構（最少化）**

```javascript
// 1️⃣ 元數據
const metadata = {
  name: "CodeReview",
  description: "Code PR Review Workflow"
}

// 2️⃣ 定義 Stage（至少一個）
async function execute() {
  const syntaxResult = await agent.checkSyntax(code)
  const logicResult = await agent.checkLogic(code)
  const report = await agent.generateReport(syntaxResult, logicResult)

  return report
}

// 3️⃣ 返回結果
return { success: true, data: report }
```

---

### 四、實戰案例：HR 審批流程（900 字）

**場景**：員工請假申請的半自動化審批

#### **傳統做法（Google Apps Script）**

```javascript
// 邏輯全硬編碼在一個 Code.gs 裡
function onFormSubmit(e) {
  // 提取資料
  // 檢查政策
  // 計算假期
  // 生成郵件
  // 全部混在一起，難以調整
}
```

**問題**：
- 難以測試單個邏輯
- 難以並行多個檢查
- 難以替換某個 Agent
- 難以監控性能

#### **Workflow 做法**

```javascript
// 明確的 Stage 分離
const leaveApprovalWorkflow = {
  metadata: {
    name: "Leave Approval",
    description: "員工請假申請自動審批"
  },

  stages: [
    // Stage 1: 資料收集與整理
    {
      name: "DataCollection",
      agents: ["ExtractFormData", "ValidateData"],
      mode: "parallel"
    },

    // Stage 2: 政策檢查（對抗驗證）
    {
      name: "PolicyValidation",
      agents: [
        "CheckCompanyPolicy",      // 檢查公司政策
        "CheckLegalRequirement"    // 檢查法律要求
      ],
      mode: "parallel",
      conflictHandling: "escalate"  // 衝突則升級給人工
    },

    // Stage 3: 生成審批建議
    {
      name: "ApprovalReasoning",
      agents: ["GenerateRecommendation"],
      inputs: ["DataCollection", "PolicyValidation"]
    },

    // Stage 4: 通知
    {
      name: "Notification",
      agents: ["SendToManager", "LogToSheet"],
      mode: "parallel"
    }
  ]
}
```

#### **執行流程可視化**

```
員工提交 Form
    ↓
Stage 1（並行）：提取 + 驗證
    ↓
Stage 2（並行）：政策檢查 + 法規檢查
    ├─ 一致 → 繼續
    └─ 衝突 → 升級給 HR 主任
    ↓
Stage 3：生成建議
    ↓
Stage 4（並行）：通知主管 + 記錄日誌

實時監控（/workflows）：
- 總耗時：2.3 秒
- 各 Stage 耗時分解
- 調用的 API 和模型
- 當前狀態
```

#### **關鍵優勢**

| 優勢 | 體現 |
|------|------|
| **精準** | 每個 Stage 的責任明確 |
| **高效** | Stage 2 的兩個檢查並行執行 |
| **安全** | 衝突自動升級，人類介入 |
| **可測** | 可單獨測試每個 Stage |
| **可監控** | `/workflows` 看完整性能 |

---

### 五、進階：Workflow 的六種模式（600 字）

Workflow 支持六種執行模式，應對不同場景：

| 模式 | 場景 | HR 應用 |
|------|------|--------|
| **流水線** | 線性順序 | 請假：表單 → 檢查 → 建議 → 通知 |
| **同步聚合** | 多 Agent 並行 → 聚合 | 並行檢查多個政策 → 整合結果 |
| **對抗驗證** | 互相驗證，發現衝突 | 政策 vs 法規 的合規檢查 |
| **末尾制** | 篩選最優方案 | 多個報銷方案中選最好的 |
| **累積式** | 逐步累積信息 | 累積月度假期記錄 → 年度統計 |
| **嵌套式** | Workflow 調用 Workflow | 請假 Workflow 內調用「政策查詢」Workflow |

---

### 六、收尾：為什麼 Workflow 是未來（500 字）

#### **回到前三篇的承諾**

- **E01** 說：蜂群是新架構
- **E02** 說：蜂群永不被淘汰
- **E03** 說：蜂群的三層分離很優雅
- **E04 說**：Workflow 讓你能真的用上它

#### **Workflow 代表的轉變**

```
從「AI 助手思維」
    ↓
到「AI 編排思維」
    ↓
Prompt 時代：「請幫我做 X」
Workflow 時代：「按照這個結構，讓多個 Agent 協作」
```

#### **三個未來趨勢**

1. **從「聊天」到「編程」**
   - Prompt 工程 → Workflow 工程
   - AI 應用將變成「寫流程」而不是「寫 Prompt」

2. **從「臨時」到「系統」**
   - 一次性脚本 → 可複用的工作流庫
   - 企業會積累「經過驗證的 Workflow 模板」

3. **從「黑箱」到「透明」**
   - AI 應用變得可監控、可調試、可優化
   - 信任建立在「可見性」之上

#### **對讀者的啟發**

如果你是：
- **開發者**：Workflow 是下一代 Agent 開發框架，值得學
- **產品經理**：Workflow 意味著你可以用代碼定義產品邏輯，不再依賴工程師
- **企業決策者**：Workflow 讓 AI 應用從實驗室走進生產環境

#### **結尾金句**

> Prompt 工程讓 AI 聽懂人話。
>
> Workflow 工程讓 AI 按照結構做事。
>
> 這是 AI 應用成熟的標誌。

---

## 🔑 金句摘錄

1. 「Workflow 就是蜂群的編程語言」

2. 「Prompt 讓 AI 自由發揮，Workflow 讓 AI 按照結構協作」

3. 「從『黑箱』到『透明盒』——Workflow 讓每一步都可見、可測、可優化」

4. 「不是『寫 Prompt』，而是『定義流程』——這是 AI 工程成熟的標誌」

5. 「Workflow 腳本可以保存、分享、複用。企業的 AI 應用將變成『經過驗證的流程庫』」

---

## 📎 參考資源

- **Workflow 筆記**：`計劃1_新世界HR系統/memory/work_log_20260525_workflow_memo.md`
- **計劃 1 案例**：`計劃1_新世界HR系統/newworld-hr-system/`
- **前三篇文章**：Agent 系列 E01-E03

---

## 🔄 與其他篇章的連接

- **E03 的延續**：E03 講「三層分離」的架構理論，E04 用 Workflow 展示如何編碼實現
- **與計劃 1 的橋樑**：用真實的 HR 系統案例説明 Workflow 的強大
- **與 Software 3.0 的對話**：Workflow 是「Software 3.0 時代的編程範式」

---

## ✅ 下一步

- [ ] 完成正文撰寫
- [ ] 製作流程圖（Stage 視覺化）
- [ ] 提供完整的 Workflow JS 腳本範例
- [ ] 發布至 Substack
- [ ] 同步至知識庫

---

**大綱建立日期**：2026-05-25
**狀態**：📝 待撰寫正文
