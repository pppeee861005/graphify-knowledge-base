# Claude 四層 Agent 架構：從主廚到工廠
## 給工程師的完整技術指南

---

上一篇，我們用「四個廚房」的比喻，
講了領導力的四層進化：

- L1 主廚模式：你決定每一步
- L1.5 監控台：你監督多個廚房
- L2 施工隊：團隊橫向協作
- L3 工廠流程：系統自動運轉

有讀者問：「這個比喻很有啟發，但底層的技術邏輯是什麼？」

今天，我們來看這個模型的技術原型：
**Claude 的 Agent 架構。**

---

## 這不是一篇「功能介紹」

這是一篇幫你回答一個核心問題的指南：

**「我應該用哪一層？」**

當你面對一個 AI 任務時——
是用 Subagent？Agent Teams？還是 Dynamic Workflow？

選錯了，你會浪費 Token、浪費時間、得到不理想的結果。
選對了，你會事半功倍，構建出真正可擴展的 AI 系統。

讓我們開始。

---

## 🔑 官方核心問題

Anthropic 在設計 Claude Agent 架構時，
問了一個根本性的問題：

### **「誰持有計畫？（Who holds the plan?）」**

這一個問題，決定了你應該用哪一層。

| 計畫持有者 | 架構層級 | 適用場景 |
|----------|---------|---------|
| Claude（逐回合決定） | **L1 Subagents** | 靈活任務、邊做邊想 |
| 人類（監控多個 session） | **L1.5 Agent View** | 多任務並行、可視化 |
| Team Lead（共同決策） | **L2 Agent Teams** | 跨領域協作、互相檢查 |
| Script（程式碼本身） | **L3 Dynamic Workflows** | 大規模自動化、完全可重複 |

**重要原則**：這四層不是「選哪一個」，而是「能力逐級升級」。

L1 是基礎，其他層都建立在 L1 的能力上。

---

## 📊 第一層：Subagents（工作層）

### 一句話定義

> **Subagents = Claude 召喚的 worker，每回合決策，任務完成後回報。**

這是最基礎、最常用、最高效的層級。
如果你只學一個，學這個。

---

### 技術規格

| 維度 | 說明 |
|------|------|
| **本質** | Claude 召喚的 worker |
| **誰決定下一步** | Claude，逐回合決定 |
| **誰持有計畫** | Claude（每回合決定） |
| **中間結果** | 放在 Claude 的 context window |
| **可重複性** | Worker 定義可重複，流程不可重複 |
| **規模上限** | 每回合少量任務（10-20 個） |
| **定義方式** | `.claude/agents/*.md` 或程式定義 |

---

### 官方關鍵特性

> "Subagents help you: Preserve context · Enforce constraints · Reuse configurations · Specialize behavior · Control costs by routing tasks to faster, cheaper models like Haiku"

翻譯成人話：
- **保留上下文**：每個 subagent 有自己乾淨的 context
- **強制約束**：可以限定 subagent 只做某件事
- **復用配置**：定義一次，多次使用
- **專業分工**：每個 subagent 專注一個領域
- **控制成本**：可以用 Haiku 模型（便宜 10 倍）

---

### 技術細節（必須知道）

**隔離性**
每個 subagent 有自己乾淨的 context window。
→ 一個 subagent 的錯誤不會污染其他 subagent。

**巢狀限制**
Subagent **不能**再 spawn 自己的 subagent。
→ 這是官方硬限制，防止無限遞歸。

**回傳機制**
只有最終訊息回到 parent，中間 tool call 不回傳。
→ 這是 context window 不爆的關鍵。

**儲存位置**
```
.claude/agents/     ← 專案級（跟著 repo 走）
~/.claude/agents/   ← 個人級（全局可用）
```

**觸發方式**
- Claude 自動根據 description 決定
- 或在 Task tool 中明確指定名稱

---

### 定義示例

```markdown
<!-- .claude/agents/code-reviewer.md -->
---
name: code-reviewer
description: 專門審查代碼品質和安全性的 agent
model: haiku  # 用便宜模型降低成本
---

你是一個代碼審查專家。

檢查以下維度：
1. 代碼風格一致性
2. 潛在安全漏洞
3. 性能問題
4. 可讀性建議

只輸出問題列表，不要修改代碼。
```

這個 agent 會在你請求代碼審查時自動被調用。
因為用了 Haiku 模型，成本只有 Sonnet 的十分之一。

---

### 什麼時候用 L1

```
✅ 適合：
• 複雜但短期的任務（寫文章、調試 bug、代碼審查）
• 需要頻繁調整方向（邊做邊想）
• Token 效率優先（成本敏感）
• 單人決策場景

❌ 不適合：
• 任務太多（超過 20 個 subagent）
• 需要完全自動化（你要一直盯著）
• 中間產物會爆掉 context（大規模任務）
```

**成本效率**：⭐⭐⭐⭐⭐ 最高

---

## 📡 第 1.5 層：Agent View（監控層）

### 一句話定義

> **Agent View = 人類監控多個背景 session 的可視化介面。**

這不是一個新的「協作模式」，
而是對 L1 Subagents 的「監控增強」。

---

### 技術規格

| 維度 | 說明 |
|------|------|
| **本質** | 背景 session 監控 |
| **誰持有計畫** | 你（人類監控多個 session） |
| **中間結果** | 各 session 獨立存在 |
| **核心能力** | 可 attach 進入任一 agent 對話 |
| **版本需求** | v2.1.139+ |
| **狀態** | 研究預覽 |

---

### 為什麼是「1.5 層」

Agent View 解決的問題是：

當你有多個長時間運行的背景任務時，
怎麼知道它們的進度？怎麼在需要時介入？

想像你開了三家餐廳：
- 廚房 A 在做意大利面
- 廚房 B 在做日本料理
- 廚房 C 在做中餐

Agent View 給你一個「中央監控台」，
讓你看到三個廚房同時進行，
並且可以隨時「跳進」任一廚房直接對話。

---

### 核心操作

**啟動背景任務**
在 Claude Code 中，你可以啟動多個背景 session。

**監控進度**
Agent View 提供儀表板，看到每個 session 的狀態和輸出。

**介入對話**
最重要的功能：你可以 **attach** 進入任一 agent 對話。
就像遠程登錄一台機器——直接跟 agent 對話，調整方向，然後退出讓它繼續。

---

### 什麼時候用 L1.5

```
✅ 適合：
• 多個長期運行的任務（持續發文、監控系統、批量處理）
• 任務間相對獨立（不需要互相協作）
• 你想要可視化控制（看進度，隨時介入）
• Human-in-the-loop 場景

❌ 不適合：
• 需要各任務間協作（用 L2）
• 需要完全自動化（用 L3）
```

---

## 🏗️ 第二層：Agent Teams（協作層）

### 一句話定義

> **Agent Teams = Lead agent + 多個 peer sessions，橫向協作、共享任務清單。**

這是 L1 的根本性升級：
從「boss → worker」變成「peer ↔ peer」。

---

### 技術規格

| 維度 | 說明 |
|------|------|
| **本質** | Lead + peer sessions |
| **狀態** | 🔬 實驗性功能 |
| **誰決定下一步** | Lead agent（逐回合決定） |
| **中間結果** | 共享任務清單（shared task list） |
| **可重複性** | Team 定義可重複 |
| **規模** | 少數長時間運行的 peers（3-10 個） |
| **啟用方式** | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` |

---

### 官方關鍵特性（重要！）

> "Unlike subagents, which run within a single session and can only report back to the main agent, you can also interact with individual teammates directly without going through the lead."

這是 L2 與 L1 的**根本區別**：

**L1 Subagents**：垂直結構（boss → worker）
- 所有回報都經過 Claude
- Worker 之間不能直接通訊

**L2 Agent Teams**：橫向結構（peer ↔ peer）
- Teammate 可以直接互相通訊
- 不需要透過 lead 轉達
- 你可以 attach 進任一 teammate session

---

### 架構圖解

```
L1 Subagents（垂直）         L2 Agent Teams（橫向）

      Claude                     Lead Agent
        │                       /    │    \
    ┌───┼───┐               ┌──┴─┐ ┌─┴──┐ ┌┴───┐
    ↓   ↓   ↓               │前端│↔│後端│↔│測試│
  Sub1 Sub2 Sub3            └────┘ └────┘ └────┘
    │   │   │                 ↑      ↑      ↑
    ↓   ↓   ↓                 └──────┴──────┘
  回報 回報 回報              直接通訊 + 共享任務清單
```

---

### 最佳應用場景

```
✅ 最適合：
• 前端/後端/測試各自負責的跨層修改
• 需要互相檢查、挑戰彼此的任務
• 各部分相對獨立但需要協調

❌ 不適合：
• 序列任務（A 必須做完 B 才能做）
• 同檔案編輯（衝突太多）
• 高依賴性工作（互相等待）
```

---

### ⚠️ 重要警告

**Token 消耗**
Agent Teams 的 Token 消耗**遠高於**單一 session。
每個 teammate 都有自己的 context，都在消耗 token。

**實驗性功能**
仍有已知的 session 恢復限制。
不建議用於生產環境的關鍵任務。

**啟用方式**
需要設置環境變數：
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

---

## 🏭 第三層：Dynamic Workflows（規模層）

### 一句話定義

> **Dynamic Workflows = Script 持有計畫，Runtime 自動執行，規模可達數百 agents。**

這是架構的最高層級。
計畫不在 Claude 的腦子裡，而在**代碼**裡。

---

### 技術規格

| 維度 | 說明 |
|------|------|
| **本質** | Script holds the plan |
| **狀態** | 🔬 研究預覽 |
| **誰持有計畫** | Script（程式碼本身） |
| **誰決定下一步** | Script（完全自動化） |
| **中間結果** | 存在 script 變數，不佔 context |
| **可重複性** | 編排本身可重複 |
| **規模能力** | 每次執行數十到數百個 agents |

---

### 官方定義

> "A dynamic workflow is a JavaScript script that orchestrates subagents at scale. Claude writes the script for the task you describe, and a runtime executes it in the background while your session stays responsive."

關鍵點：
1. **Claude 寫腳本**：你描述任務，Claude 生成 JS 腳本
2. **Runtime 執行**：腳本在背景運行，你的 session 保持響應
3. **規模化**：可以編排數百個 agents

---

### 這是「計畫移入代碼」的關鍵

**為什麼 L3 能支持大規模？**

L1/L2 的問題：
- Claude 是 orchestrator
- 每回合決定下一步
- 中間結果存在 Claude 的 context window
- **Context 會爆**

L3 的解法：
- Script 是 orchestrator
- 計畫寫在 JavaScript 代碼裡
- 循環、分支、中間結果都在 script 變數中
- **Claude 的 context 只存最終答案**

→ 這就是 context window 不爆的根本原因。

---

### 關鍵指令

**內建指令**
```
/deep-research — 觸發深度研究 workflow
```

**關鍵字觸發**
```
ultracode — 觸發 ultracode workflow
```

**自訂 workflow**
```
可儲存到 .claude/workflows/ 目錄
```

---

### 高級特性

**可儲存**
Script 可存為 `.claude/workflows/` 自訂指令。
→ 你可以複用 workflow，不用每次重新描述。

**可恢復**
同一 session 內可 resume。
→ 但退出 session 後需要重新開始。

**隔離**
`isolation: 'worktree'` 給每個 agent 獨立 repo 副本。
→ 避免多個 agent 同時修改同一檔案的衝突。

**質量保證**
獨立 agent 互相對抗性審查，結果經 cross-check 才輸出。
→ 這是「多角度驗證」的工程實現。

---

### Workflow 概念示例

```javascript
// 這是 Claude 自動生成的 workflow（概念性）
const researchWorkflow = async (topic) => {

  // Stage 1: 並行搜索多個來源
  const sources = await Promise.all([
    agent('researcher-1').search(topic, 'academic'),
    agent('researcher-2').search(topic, 'industry'),
    agent('researcher-3').search(topic, 'news'),
  ]);

  // Stage 2: 獨立分析
  const analyses = await Promise.all(
    sources.map((source, i) =>
      agent(`analyst-${i}`).analyze(source)
    )
  );

  // Stage 3: 對抗性審查
  const reviewed = await Promise.all(
    analyses.map((analysis, i) =>
      agent(`reviewer-${(i+1) % 3}`).review(analysis)
    )
  );

  // Stage 4: 綜合報告
  return agent('synthesizer').combine(reviewed);
};
```

注意結構：
- 並行執行（Promise.all）
- 階段分離（Stage 1→2→3→4）
- 對抗審查（reviewer 檢查 analyst）
- 最終綜合（synthesizer）

這種結構，用 L1 是做不到的。

---

### 🚨 官方硬限制（必須記住！）

| 限制類型 | 數值 | 原因 |
|---------|------|------|
| **並發上限** | 16 個 agents | 資源限制 |
| **總量上限** | 1,000 agents per run | 防止無限迴圈 |
| **巢狀限制** | Subagent 不能再 spawn subagent | 防止遞歸 |
| **版本要求** | v2.1.154+ | 2026/05/28 發布 |
| **訂閱要求** | Pro/Max/Team/Enterprise | 付費功能 |

---

### 什麼時候用 L3

```
✅ 適合：
• 超大規模任務（100+ agents）
• 完全可預測的流程（不需要人工調整）
• 需要質量保證機制（對抗性審查）
• 長期自動化運行（無人監督）
• 內容生成、大規模研究、系統部署

❌ 不適合：
• 任務需要頻繁調整（計畫寫死了）
• 規模小於 50 agents（用 L1 更高效）
• 需要即時人工干預
```

---

## 🧩 第四維度：Skills（擴展層）

### 一句話定義

> **Skills = Claude 遵循的指令文件，是正交維度，與其他三層結合使用。**

Skills 不在 L1→L3 的「能力升級」路徑上。
它是一個**正交維度**，可以與任何層級結合：

- L1 + Skills：Subagent 遵循特定 skill 指令
- L2 + Skills：Teammate 有各自的專業 skill
- L3 + Skills：Workflow 中的每個 agent 使用不同 skill

---

### Skills 定義示例

```markdown
<!-- ~/.claude/skills/code-style.md -->
---
name: code-style
description: 公司代碼風格規範
---

遵循以下規範：
1. 使用 TypeScript，嚴格類型
2. 函數名用 camelCase
3. 類名用 PascalCase
4. 每個函數不超過 50 行
5. 必須有 JSDoc 註釋
```

任何層級的 agent 都可以調用這個 skill。

---

## 📋 官方完整對比表

| 維度 | Subagents | Agent Teams | Dynamic Workflows |
|------|-----------|-------------|-------------------|
| **本質** | Claude 召喚的 worker | Lead 監督 peer sessions | Runtime 執行的 script |
| **誰決定下一步** | Claude，逐回合 | Lead agent，逐回合 | Script（程式碼） |
| **中間結果存在** | Claude context window | 共享任務清單 | Script 變數 |
| **可重複的是** | Worker 定義 | Team 定義 | 編排本身 |
| **規模** | 每回合少量任務 | 少數長時間 peers | 每次數十到數百 |
| **中斷後** | 重新開始該回合 | Teammate 繼續運行 | 同 session 可恢復 |
| **Token 效率** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **靈活度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **規模能力** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 📌 決策樹：我應該用哪一層？

### 快速決策流程

```
開始
  │
  ├─「這個任務需要多少 agents？」
  │
  ├─ < 20 個
  │   └─「需要多個長期並行任務嗎？」
  │       ├─ 否 → L1 Subagents ⭐
  │       │        最簡單、最高效、最便宜
  │       │
  │       └─ 是 → L1.5 Agent View 📡
  │                人類監控 + 可介入
  │
  ├─ 20-100 個
  │   └─「需要橫向協作嗎？」
  │       ├─ 否 → L1 Subagents（分批執行）
  │       │
  │       └─ 是 → L2 Agent Teams 🏗️
  │                ⚠️ 實驗性，Token 消耗大
  │
  └─ > 100 個
      └─ L3 Dynamic Workflows 🏭
           需要 v2.1.154+，Pro/Max/Team/Enterprise
```

---

### 特殊情況決策

| 你的需求 | 推薦層級 |
|---------|---------|
| 「我需要 peer review / 互相檢查」 | L2 Agent Teams |
| 「我需要完全自動化，無人監督」 | L3 Dynamic Workflows |
| 「我需要最大靈活度，邊做邊想」 | L1 Subagents |
| 「我需要可視化監控，隨時介入」 | L1.5 Agent View |
| 「我的預算很緊張」 | L1 Subagents + Haiku |

---

## 🔗 關鍵數字速查

| 指標 | 數值 |
|------|------|
| 官方架構層數 | 4 層（含 Agent View） |
| L1 最大並發 | 10-20 個 subagents |
| L3 並發上限 | 16 個 agents 同時執行 |
| L3 總量上限 | 1,000 agents per run |
| Agent View 最低版本 | v2.1.139+ |
| Dynamic Workflows 最低版本 | v2.1.154+ |
| 能否巢狀 spawn subagent | ❌ 不能 |
| Agent Teams 狀態 | 🔬 實驗性 |
| Dynamic Workflows 狀態 | 🔬 研究預覽 |

---

## 💡 回到那個問題

記得上一篇我們問的：
**「誰持有計畫？」**

現在你知道了：

- **L1**：Claude 持有計畫，你逐回合決定
- **L1.5**：你持有計畫，監控多個 agent
- **L2**：Team 持有計畫，peer 協作
- **L3**：Script 持有計畫，完全自動化

這不只是技術選擇。
這是一種**思維方式的進化**。

從「我要控制一切」
到「我要設計系統，讓系統自己運轉」

這正是現代工程師應該學習的領導力。

---

## 🚀 開始實踐

不要只是讀，去試。

**今天就做這三件事：**

**1. 檢查你的 Claude Code 版本**
```bash
claude --version
```
確保 v2.1.154+（如果想用 L3）

**2. 創建你的第一個 Subagent**
在 `.claude/agents/` 創建一個簡單的 agent：
```markdown
---
name: my-first-agent
description: 專門做 X 的 agent
model: haiku
---

你是一個專門做 X 的專家...
```

**3. 試一次 /deep-research**
體驗 Dynamic Workflow 的威力。
觀察它如何並行編排多個 agent。

然後，回來告訴我：
**你的第一個 agent 做了什麼？**

---

## 📚 系列導航

**第一篇**（大眾篇）：
《不是權力大，是計畫清：四種領導力的真相》
→ 用廚房比喻講領導力

**第二篇**（本篇）：
《Claude 四層 Agent 架構：從主廚到工廠》
→ 給工程師的完整技術指南

**下一篇預告**：
《從 L1 到 L3：我的真實遷移故事》
→ 把一個複雜項目從 Subagents 遷移到 Dynamic Workflows 的完整過程

訂閱，確保你不會錯過。

---

> **「計畫在哪裡，決定了系統的能力上限。」**

---

*你打算從哪一層開始？留言告訴我。*

