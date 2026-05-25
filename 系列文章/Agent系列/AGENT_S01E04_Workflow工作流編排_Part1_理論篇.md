# Workflow：從 Prompt 到代碼，蜂群的編程語言（Part 1 - 理論篇）

**《蜂群 Agent》系列｜第 4 篇（上）**
*新人類聯盟 · Homo Coalitio*

---

## 一個建築師的困境

「我讀完前三篇 Agent 文章了。蜂群的架構很美，大腦、框架、執行三層分離很優雅，可適應性也聽起來無懈可擊。」

在聯盟的線下沙龍中，一位資深系統架構師皺著眉頭，提出了這個讓全場安靜下來的問題：

「但我到底要怎麼寫代碼？我是不是要用 Python 寫個幾萬行的 Agent 框架？要自己用資料庫管理 Session？自己用 API 呼叫管理 Brain？如果每一次都要自己手動建構這些基礎設施，那蜂群的開發成本是不是太高了？」

這是一個極其真實且鋒利的困境。這就像你設計了一座極其宏偉、具有自我修復能力的未來城堡，但當你準備動手建造時，發現手邊連一包水泥、一塊磚頭都沒有，你必須從燒磚、磨水泥開始做起。如果真是這樣，那麼「蜂群」將永遠停留在論文和哲學討論中，無法成為工程師的日常武器。

幸運的是，這個困境已經被解決了。

2026 年，Anthropic 在其開發者工具 **Claude Code (V2.1.47 / V2.1.48)** 中推出了一個低調卻具備革命性的功能——**Workflow（工作流）**。

這不是另一個可有可無的軟體庫，也不是一個花哨的視覺化拖拽界面。**Workflow，就是蜂群的編程語言。**

它允許開發者直接使用 JavaScript 來聲明式地定義多個 Agent 的協作關係、資料流向以及衝突解決機制。你不需要自己去造 Harness 和 Session 的輪子，因為 Anthropic 已經把整個蜂群的物理基礎設施封裝進了這個運行時（Runtime）中。

要啟用它，你只需要在終端機輸入一行簡單的命令：

```bash
export CLAUDE_CODE_WORKFLOWS_ENABLED=1
claude
```

當你啟動 Claude Code 後，你會發現原本單一的對話框，多了一個彩虹漸層的魔法入口：**ultraWork [你的任務]**。

今天，我們就要走進這個魔法入口的底層，看看從 Prompt 到 Workflow，究竟發生了什麼本質的範式轉移，以及為什麼這個轉移將徹底重塑軟體工程的未來。

---

## 第 1 幕：Prompt vs Workflow 的根本衝突

要理解 Workflow 的價值，我們必須先看清它的對立面：**Prompt（提示詞）**。

在過去幾年裡，我們習慣了用 Prompt 來指揮 AI。當你想讓 AI 幫你審查一段代碼時，你會寫下這樣的指令：

```markdown
你是一個資深的資安與代碼質量專家。請審查以下代碼，找出其中的語法錯誤、
邏輯漏洞以及潛在的性能瓶頸，並生成一份詳細的報告。
```

這段 Prompt 傳給 Claude 後，發生了什麼？

這是一個標準的**「黑箱操作」**。Claude 接收到這段指令，在大腦內部進行了複雜的推理，然後自己決定先看語法、再看安全、最後寫報告。

這種基於 Prompt 的做法，在處理簡單任務時很方便，但在企業級生產環境中，它會遇到四個致命的瓶頸：

1. **結果不可預測（Unpredictable）**：模型今天可能先檢查安全，明天可能先檢查性能；今天輸出了 Markdown 格式，明天可能輸出了 JSON。對於需要對接下游系統的程序來說，這簡直是災難。
2. **流程無法控制（Uncontrollable）**：如果代碼有 10,000 行，你無法強制模型「先花 30% 的 Token 做語法掃描，再花 50% 的 Token 做深度安全分析」。它是一口氣吞下去，然後憑直覺吐出結果。
3. **難以複用與優化（Non-reusable）**：當你發現審查報告的「性能分析」部分不夠深入時，你只能去修改那段長長的 Prompt。但修改 Prompt 就像在沙灘上建城堡——你微調了一個字，可能導致原本工作得很好的「安全檢查」部分突然失效。
4. **多 Agent 協作困難（Siloed）**：當你試圖讓多個 Agent 協作時（例如一個負責寫代碼，一個負責測試），如果只靠 Prompt 傳遞，它們就像是在用極其緩慢的文字對講機溝通。沒有統一的進度協調，沒有並行機制，效率極低。

這就是**「指令式思維」**的局限。你試圖用自然語言去規定一個複雜系統的執行路徑，這本質上是在對抗熱力學第二定律。

而 **Workflow** 則是完全不同的思維方式。它不再問「你要 AI 做什麼」，而是定義**「多個 Agent 之間的組織結構是什麼」**。

如果用代碼來表達，同一個代碼審查任務在 Workflow 裡會變成這樣：

```javascript
// Workflow：定義結構與流程
Stage 1: Agent.checkSyntax(code)                 // 步驟 1：語法檢查
Stage 2: Parallel(                                // 步驟 2：並行執行安全與性能分析
           Agent.checkSecurity(code),
           Agent.checkPerformance(code)
         )
Stage 3: Agent.generateReport(results)            // 步驟 3：聚合結果生成報告
```

在這個結構中，沒有任何一個 Agent 需要同時負擔「語法、安全、性能、寫報告」這四個截然不同的任務。每一個 Agent 都被解耦成一個單一職責的實體（Single Responsibility Entity），而它們的協作關係被 JavaScript 代碼死死地錨定在系統中。

### 廚房的隱喻：從烹飪配方到餐廳工作流

如果這聽起來太過抽象，讓我們用一個生活中的類比：**烹飪**。

傳統的 Prompt，就像是給廚師一張**烹飪配方**，上面寫著：「做出一道完美的法式紅酒燉牛肉，要注意火候，蔬菜要切得均勻，最後要精美擺盤。」

如果你的廚師是個米其林三星大廚（類似於當下最強的 GPT-4 或 Claude Opus），他確實能憑藉高超的個人能力完成這項任務。但如果今天餐廳要同時接待 200 位客人呢？如果大廚今天生病了，換成了一個剛畢業的學徒呢？這張配方就會失效，廚房會陷入一片混亂，菜品品質會直線下降。

而 Workflow，則是**餐廳的工作流系統**：

* **前台接單員**（Agent A）：負責接收顧客訂單，並將其標準化。
* **配菜員**（Agent B）：負責清洗和切配食材。
* **主廚**（Agent C）：專注於爐火上的烹飪，不關心洗菜和擺盤。
* **擺盤師**（Agent D）：專注於最終的視覺呈現。
* **服務生**（Agent E）：負責將成品送到客人桌上。

在這個工作流中，即使主廚的個人能力有所波動，或者某個環節換了人，只要整個系統的「流水線」依然運轉，餐廳就能以穩定的速度、標準的品質，持續輸出高質量的菜品。

這就是 Prompt 與 Workflow 的本質區別：**Prompt 是對個體智慧的壓榨，而 Workflow 是對組織結構的編排。**

---

## 第 2 幕：Workflow 的三大範式轉變

當我們把蜂群的編排方式從「Prompt」升級為「Workflow」時，我們實際上完成了三個底層的範式轉移。

```
【範式轉移一】 指令式（Imperative）  ──▶  聲明式（Declarative）
【範式轉移二】 黑箱（Black-box）     ──▶  透明盒（Transparent Box）
【範式轉移三】 一次性（Ad-hoc）      ──▶  可複用資產（Reusable Asset）
```

### 1. 從「指令式」到「聲明式」

在傳統的 Agent 開發中，我們是在寫「指令」（告訴 AI 一步步要做什麼）。而在 Workflow 中，我們是在「聲明結構」。

在聲明式架構下，我們不關心 AI 在具體某一步是如何進行邏輯推理的，我們只規定數據流的拓撲結構。例如，我們定義 `Stage 2` 的輸入必須是 `Stage 1` 的輸出，而 `Stage 3` 必須等待 `Stage 2` 的並行任務全部完成後才能觸發。

這種聲明式的設計，讓開發者能夠把精力從「調教 AI 的脾氣（Prompt Tuning）」中解放出來，專注於設計更高效的業務邏輯結構。

### 2. 從「黑箱」到「透明盒」

傳統的 Agent 是一個巨大的黑箱，你輸入一個問題，等待幾十秒，然後得到一個答案。如果答案錯了，你根本不知道是哪個環節出了問題。

Workflow 則將整個決策過程拆解為多個清晰的 **Stage（階段）**。每一個 Stage 都有其明確的輸入、輸出、狀態、耗時以及 Token 消耗。

當一個 Workflow 執行時，你可以在控制台中使用 `/workflows` 命令進行即時觀測。你會看到：

* `Stage 1 (Data Prep)` 耗時 0.3 秒，消耗 120 Tokens，狀態為 `SUCCESS`。
* `Stage 2 (Parallel Checking)` 正在並行執行，其中 `SecurityAgent` 已完成，而 `LegalAgent` 發生了超時重試。

這時，AI 不再是神祕莫測的魔法，而是一個**可觀測、可測試、可進行性能調優的現代軟體系統**。

### 3. 從「一次性」到「可複用資產」

Prompt 是極難版本控制和複用的。你很難在 GitHub 上對一段 2,000 字的 Prompt 進行優雅的 diff 合併。

但 Workflow 腳本是標準的 JavaScript 代碼。這意味著它可以：

* 納入 Git 進行版本控制。
* 編寫單元測試（Unit Test）來驗證每一個 Stage 的輸出是否符合預期。
* 在不同的專案之間進行 Import 和 Export，建立起企業內部的「工作流資產庫」。

### Workflow 腳本的最簡結構

在 Claude Code 的 Workflow 體系中，一個標準的腳本只需要包含以下三個核心要素：

```javascript
// 1️⃣ 元數據聲明（Metadata）：定義工作流的身份
const metadata = {
  name: "CodeReviewWorkflow",
  description: "自動化代碼審查與質量評估流程",
  version: "1.0.0"
};

// 2️⃣ 執行邏輯（Execution）：使用異步函數編排 Stage
async function execute(context) {
  const { code } = context.input;

  // 呼叫 Stage 1：語法掃描
  const syntaxResult = await agent.run("SyntaxCheckAgent", { code });

  if (!syntaxResult.passed) {
    return { success: false, reason: "語法檢查未通過", details: syntaxResult };
  }

  // 呼叫 Stage 2：並行進行安全與性能分析
  const [securityResult, performanceResult] = await Promise.all([
    agent.run("SecurityAgent", { code }),
    agent.run("PerformanceAgent", { code })
  ]);

  // 呼叫 Stage 3：整合報告
  const finalReport = await agent.run("ReporterAgent", {
    syntaxResult,
    securityResult,
    performanceResult
  });

  // 3️⃣ 返回標準格式的結果
  return {
    success: true,
    report: finalReport,
    metrics: {
      generatedAt: new Date().toISOString()
    }
  };
}
```

這段代碼展示了 Workflow 的精髓：**利用 JavaScript 語言強大的異步處理能力（如 `Promise.all`），原生支持並行 Agent 協作，而不需要任何複雜的多線程框架。**

---

## 🔑 第一部分金句摘錄

1. **「Prompt 是對個體智慧的壓榨，而 Workflow 是對組織結構的編排。」**

2. **「指令式思維無法規定複雜系統，但聲明式思維可以描述完美的組織結構。」**

3. **「從黑箱到透明盒，這才是 AI 走向生產環境的必要條件。」**

---

## 📎 本篇參考資源

* **Workflow 原始筆記**：[work_log_20260525_workflow_memo.md](file:///D:/數位資產/graphify個人知識庫/計劃1_新世界HR系統/memory/work_log_20260525_workflow_memo.md)
* **前三篇回顧**：
  * E01：[蜂群 Agent 是什麼](file:///D:/數位資產/graphify個人知識庫/系列文章/Agent系列/AGENT_S01E01_蜂群Agent是什麼_published.md)
  * E02：[可適應性蜂群永不被淘汰](file:///D:/數位資產/graphify個人知識庫/系列文章/Agent系列/AGENT_S01E02_可適應性蜂群永不被淘汰_published.md)
  * E03：[解耦哲學：Anthropic 設計蜂群的靈魂](file:///D:/數位資產/graphify個人知識庫/系列文章/Agent系列/AGENT_S01E03_解耦哲學Anthropic設計蜂群_published.md)

---

**預告：下一篇（Part 2 - 實踐篇）**
我們將深入「新世界 HR 系統」案例，看 Workflow 如何將理論轉化為企業級生產系統，並詳解六種核心執行模式。

---

*新人類聯盟 · Homo Coalitio*
*《AI 指揮官筆記》Substack · 2026.05*
*aiagentcommander.substack.com*
