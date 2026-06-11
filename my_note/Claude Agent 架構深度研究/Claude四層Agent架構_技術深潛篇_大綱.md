# Claude 四層 Agent 架構：從主廚到工廠
## 技術深潛篇 | 面向工程師的完整指南

**寫作定位**：AI 工程派詩人風格（60% 理性 + 40% 感性）
**目標讀者**：軟體工程師、AI 開發者、技術主管、Claude Code 用戶
**前置文章**：《不是權力大，是計畫清：四種領導力的真相》
**核心價值**：讓工程師能立即上手 Claude 四層 Agent 架構
**字數目標**：2,500-3,500 字（技術文章可長一些）

---

## 📖 完整文章大綱（七層結構）

### **第 1 層：標題（決定點擊率）**

#### 黃金標題候選

| 候選 | 對比詞 | 具體化 | 特點 |
|------|--------|--------|------|
| **Claude 四層 Agent 架構：從主廚到工廠** | 主廚→工廠 | 四層 | 延續上篇比喻 |
| **誰持有計畫？Claude Agent 的四層答案** | 誰→答案 | 四層 | 回扣核心問題 |
| **Subagents → Workflows：計畫持有權的四次躍遷** | 躍遷 | 技術名詞 | 工程師向 |
| **從 L1 到 L3：Claude Agent 的能力升級路徑** | L1→L3 | 路徑 | 實操向 |

**推薦選擇**：「**Claude 四層 Agent 架構：從主廚到工廠**」
- 延續上篇比喻（主廚/工廠），老讀者親切
- 包含「Claude」關鍵詞，SEO 友好
- 「四層」預告結構，設定期待

---

### **第 2 層：開場（承接上篇 + 技術預告）— 150-200 字**

#### 段落 1：承接上篇（讀者連結）

```
上一篇，我們用「四個廚房」的比喻，
講了領導力的四層進化：

- L1 主廚模式：你決定每一步
- L1.5 監控台：你監督多個廚房
- L2 施工隊：團隊橫向協作
- L3 工廠流程：系統自動運轉

有讀者問：「這個比喻很有啟發，但底層的技術邏輯是什麼？」

今天，我們來看這個模型的技術原型：
**Claude 的 Agent 架構**。
```

**設計意圖**：
- ✅ 老讀者：「哦，這是上篇的技術版」
- ✅ 新讀者：「我需要先看上篇嗎？」（不用，這篇自足）
- ✅ 建立「技術深潛」的期待

---

#### 段落 2：技術價值預告

```
這不是一篇「介紹 Claude 功能」的文章。

這是一篇幫你回答一個核心問題的指南：
**「我應該用哪一層？」**

當你面對一個 AI 任務時——
是用 Subagent？Agent Teams？還是 Dynamic Workflow？

選錯了，你會浪費 Token、浪費時間、得到不理想的結果。
選對了，你會事半功倍，構建出真正可擴展的 AI 系統。

讓我們開始。
```

**設計意圖**：
- ✅ 明確價值：「幫你選對」
- ✅ 痛點：「選錯會浪費」
- ✅ 承諾：「這篇會給你答案」

---

### **第 3 層：官方核心問題（理論基石）— 200 字**

#### 一個問題，四層答案

```
## 🔑 官方核心問題

Anthropic 在設計 Claude Agent 架構時，
問了一個根本性的問題：

### **「誰持有計畫？（Who holds the plan?）」**

這一個問題，決定了你應該用哪一層。

| 計畫持有者 | 架構層級 | 適用場景 |
|----------|---------|---------|
| Claude（逐回合決定） | L1 Subagents | 靈活任務、邊做邊想 |
| 人類（監控多個 session） | L1.5 Agent View | 多任務並行、可視化 |
| Team Lead（共同決策） | L2 Agent Teams | 跨領域協作、互相檢查 |
| Script（程式碼本身） | L3 Dynamic Workflows | 大規模自動化、完全可重複 |

**重要原則**：這四層不是「選哪一個」，而是「能力逐級升級」。

L1 是基礎，其他層都建立在 L1 的能力上。
```

---

### **第 4 層：四層完整技術解析（核心內容）— 1,200-1,500 字**

---

#### **4.1 第一層：Subagents（工作層）**

##### 一句話定義

```
> **Subagents = Claude 召喚的 worker，每回合決策，任務完成後回報**
```

##### 技術規格表

```
| 維度 | 說明 |
|------|------|
| **本質** | Claude 召喚的 worker |
| **誰決定下一步** | Claude，逐回合決定 |
| **誰持有計畫** | Claude（每回合決定） |
| **中間結果** | 放在 Claude 的 context window |
| **可重複性** | Worker 定義可重複，流程不可重複 |
| **規模上限** | 每回合少量任務（10-20 個） |
| **定義方式** | `.claude/agents/*.md` 或程式定義 |
```

##### 官方關鍵特性

```
> "Subagents help you:
>  Preserve context · Enforce constraints · Reuse configurations ·
>  Specialize behavior · Control costs by routing tasks to faster,
>  cheaper models like Haiku"
```

##### 技術細節（工程師必知）

```
**隔離性**
每個 subagent 有自己乾淨的 context window。
→ 這意味著：一個 subagent 的錯誤不會污染其他 subagent。

**巢狀限制**
Subagent 不能再 spawn 自己的 subagent。
→ 這是官方硬限制，防止無限遞歸。

**回傳機制**
只有最終訊息回到 parent，中間 tool call 不回傳。
→ 這是 context window 不爆的關鍵。

**儲存位置**
- `.claude/agents/`（專案級）
- `~/.claude/agents/`（個人級）

**觸發方式**
- Claude 自動根據 description 決定
- 或在 Task tool 中明確指定名稱
```

##### 定義示例

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

##### 什麼時候用 L1

```
✅ 適合：
- 複雜但短期的任務（寫文章、調試 bug、代碼審查）
- 需要頻繁調整方向（邊做邊想）
- Token 效率優先（成本敏感）
- 單人決策場景

❌ 不適合：
- 任務太多（超過 20 個 subagent）
- 需要完全自動化（你要一直盯著）
- 中間產物會爆掉 context（大規模任務）
```

##### 成本效率

```
⭐⭐⭐⭐⭐ 最高

為什麼？
- 可以用 Haiku 模型（便宜 10 倍）
- 中間結果不重複傳輸
- 沒有額外的 session 開銷
```

---

#### **4.2 第 1.5 層：Agent View（監控層）**

##### 一句話定義

```
> **Agent View = 人類監控多個背景 session 的可視化介面**
```

##### 技術規格表

```
| 維度 | 說明 |
|------|------|
| **本質** | 背景 session 監控 |
| **誰持有計畫** | 你（人類監控多個 session） |
| **中間結果** | 各 session 獨立存在 |
| **核心能力** | 可 attach 進入任一 agent 對話 |
| **版本需求** | v2.1.139+ |
| **狀態** | 研究預覽 |
```

##### 為什麼是「1.5 層」而不是「2 層」

```
Agent View 不是一個新的「協作模式」，
而是對 L1 Subagents 的「監控增強」。

它解決的問題是：
當你有多個長時間運行的背景任務時，
怎麼知道它們的進度？怎麼在需要時介入？

→ Agent View 給你一個「中央監控台」。
```

##### 核心操作

```
**啟動背景任務**
在 Claude Code 中，你可以啟動多個背景 session，
每個 session 獨立運行自己的任務。

**監控進度**
Agent View 提供一個儀表板，
讓你看到每個 session 的狀態和輸出。

**介入對話**
最重要的功能：你可以 attach 進入任一 agent 對話。
就像遠程登錄一台機器一樣，你可以直接跟 agent 對話，
調整方向，然後退出讓它繼續。
```

##### 什麼時候用 L1.5

```
✅ 適合：
- 多個長期運行的任務（持續發文、監控系統、批量處理）
- 任務間相對獨立（不需要互相協作）
- 你想要可視化控制（看進度，隨時介入）
- Human-in-the-loop 場景

❌ 不適合：
- 需要各任務間協作（用 L2）
- 需要完全自動化（用 L3）
```

---

#### **4.3 第二層：Agent Teams（協作層）**

##### 一句話定義

```
> **Agent Teams = Lead agent + 多個 peer sessions，橫向協作、共享任務清單**
```

##### 技術規格表

```
| 維度 | 說明 |
|------|------|
| **本質** | Lead + peer sessions |
| **狀態** | 🔬 實驗性功能 |
| **誰決定下一步** | Lead agent（逐回合決定） |
| **中間結果** | 共享任務清單（shared task list） |
| **可重複性** | Team 定義可重複 |
| **規模** | 少數長時間運行的 peer sessions（3-10 個） |
| **啟用方式** | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` |
```

##### 官方關鍵特性（重要！）

```
> "Unlike subagents, which run within a single session and can only
>  report back to the main agent, you can also interact with individual
>  teammates directly without going through the lead."

這是 L2 與 L1 的根本區別：
- L1 Subagents：垂直結構（boss → worker）
- L2 Agent Teams：橫向結構（peer ↔ peer）

Teammate 可以直接互相通訊，不需要透過 lead 轉達。
這是真正的「施工隊」模式。
```

##### 架構圖解

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

##### 最佳應用場景

```
✅ 最適合：
- 前端/後端/測試各自負責的跨層修改
- 需要互相檢查、挑戰彼此的任務
- 各部分相對獨立但需要協調

❌ 不適合：
- 序列任務（A 必須做完 B 才能做）
- 同檔案編輯（衝突太多）
- 高依賴性工作（互相等待）
```

##### 重要警告

```
⚠️ Token 消耗警告
Agent Teams 的 Token 消耗遠高於單一 session。
每個 teammate 都有自己的 context，都在消耗 token。

⚠️ 實驗性功能
仍有已知的 session 恢復限制。
不建議用於生產環境的關鍵任務。

⚠️ 啟用方式
需要設置環境變數：
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

##### 什麼時候用 L2

```
✅ 適合：
- 多角色協作（前端/後端/測試）
- 需要 peer review（互相檢查）
- Token 預算充足
- 可以接受實驗性功能的不穩定

❌ 不適合：
- 序列依賴的任務
- 同一檔案的修改
- 成本敏感場景
```

---

#### **4.4 第三層：Dynamic Workflows（規模層）**

##### 一句話定義

```
> **Dynamic Workflows = Script 持有計畫，Runtime 自動執行，規模可達數百 agents**
```

##### 技術規格表

```
| 維度 | 說明 |
|------|------|
| **本質** | Script holds the plan |
| **狀態** | 🔬 研究預覽 |
| **誰持有計畫** | Script（程式碼本身） |
| **誰決定下一步** | Script（完全自動化） |
| **中間結果** | 存在 script 變數，不佔 context |
| **可重複性** | 編排本身可重複 |
| **規模能力** | 每次執行數十到數百個 agents |
```

##### 官方定義

```
> "A dynamic workflow is a JavaScript script that orchestrates subagents
>  at scale. Claude writes the script for the task you describe, and a
>  runtime executes it in the background while your session stays responsive."

關鍵點：
1. **Claude 寫腳本**：你描述任務，Claude 生成 JS 腳本
2. **Runtime 執行**：腳本在背景運行，你的 session 保持響應
3. **規模化**：可以編排數百個 agents
```

##### 這是「計畫移入代碼」的關鍵

```
為什麼 L3 能支持大規模？

L1/L2：Claude 是 orchestrator
- 每回合決定下一步
- 中間結果存在 Claude 的 context window
- Context 會爆

L3：Script 是 orchestrator
- 計畫寫在 JavaScript 代碼裡
- 循環、分支、中間結果都在 script 變數中
- Claude 的 context 只存最終答案

→ 這就是 context window 不爆的根本原因。
```

##### 關鍵指令

```
**內建指令**
/deep-research — 觸發深度研究 workflow

**關鍵字觸發**
ultracode — 觸發 ultracode workflow

**自訂 workflow**
可儲存到 .claude/workflows/ 目錄
```

##### 高級特性

```
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
```

##### 官方硬限制（必須記住！）

```
| 限制類型 | 數值 | 原因 |
|---------|------|------|
| **並發上限** | 16 個 agents | 資源限制 |
| **總量上限** | 1,000 agents per run | 防止無限迴圈 |
| **巢狀限制** | Subagent 不能再 spawn subagent | 防止遞歸 |
| **版本要求** | v2.1.154+ | 2026/05/28 發布 |
| **訂閱要求** | Pro/Max/Team/Enterprise | 付費功能 |
```

##### Workflow 示例（概念）

```javascript
// 這是 Claude 自動生成的 workflow 示例（概念性）
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

##### 什麼時候用 L3

```
✅ 適合：
- 超大規模任務（100+ agents）
- 完全可預測的流程（不需要人工調整）
- 需要質量保證機制（對抗性審查）
- 長期自動化運行（無人監督）
- 內容生成、大規模研究、系統部署

❌ 不適合：
- 任務需要頻繁調整（計畫寫死了）
- 規模小於 50 agents（用 L1 更高效）
- 需要即時人工干預
```

---

#### **4.5 第四維度：Skills（擴展層）**

##### 一句話定義

```
> **Skills = Claude 遵循的指令文件，是正交維度，與其他三層結合使用**
```

##### 技術規格表

```
| 維度 | 說明 |
|------|------|
| **本質** | Claude 遵循的指令文件 |
| **誰持有計畫** | 指令文件本身 |
| **中間結果** | context window |
| **可重複性** | 指令本身可重複 |
| **位置** | 正交維度 |
```

##### 為什麼 Skills 是「第四維度」而不是「第四層」

```
Skills 不在 L1→L3 的「能力升級」路徑上。
它是一個正交維度，可以與任何層級結合：

- L1 + Skills：Subagent 遵循特定 skill 指令
- L2 + Skills：Teammate 有各自的專業 skill
- L3 + Skills：Workflow 中的每個 agent 使用不同 skill
```

##### Skills 定義示例

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

---

### **第 5 層：官方對比表（快速參考）— 200 字**

```
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
```

---

### **第 6 層：決策樹（實操指南）— 300 字**

```
## 📌 決策樹：我應該用哪一層？

### 快速決策流程

開始
  │
  ├─「這個任務需要多少 agents？」
  │
  ├─ < 20 個
  │   └─「需要多個長期並行任務嗎？」
  │       ├─ 否 → **L1 Subagents** ⭐
  │       │        最簡單、最高效、最便宜
  │       │
  │       └─ 是 → **L1.5 Agent View** 📡
  │                人類監控 + 可介入
  │
  ├─ 20-100 個
  │   └─「需要橫向協作嗎？」
  │       ├─ 否 → **L1 Subagents**（分批執行）
  │       │
  │       └─ 是 → **L2 Agent Teams** 🏗️
  │                ⚠️ 實驗性，Token 消耗大
  │
  └─ > 100 個
      └─ **L3 Dynamic Workflows** 🏭
           需要 v2.1.154+，Pro/Max/Team/Enterprise

### 特殊情況決策

「我需要 peer review / 互相檢查」
  → L2 Agent Teams

「我需要完全自動化，無人監督」
  → L3 Dynamic Workflows

「我需要最大靈活度，邊做邊想」
  → L1 Subagents

「我需要可視化監控，隨時介入」
  → L1.5 Agent View

「我的預算很緊張」
  → L1 Subagents + Haiku 模型
```

---

### **第 7 層：結尾（行動號召 + 系列預告）— 200 字**

#### 結尾選項 A：工程師行動號召

```
---

## 🚀 開始實踐

不要只是讀，去試。

**今天就做這三件事**：

1. **檢查你的 Claude Code 版本**
   ```bash
   claude --version
   ```
   確保 v2.1.154+（如果想用 L3）

2. **創建你的第一個 Subagent**
   在 `.claude/agents/` 創建一個簡單的 agent
   讓它專門做一件事（代碼審查、文檔生成、測試撰寫）

3. **試一次 /deep-research**
   體驗 Dynamic Workflow 的威力
   觀察它如何並行編排多個 agent

然後，回來告訴我：
你的第一個 agent 做了什麼？

---

**下一篇預告**：
《從 L1 到 L3：我的真實遷移故事》
我會分享把一個複雜項目從 Subagents 遷移到 Dynamic Workflows 的完整過程，
包括踩過的坑、學到的教訓、最終的效果。

訂閱，確保你不會錯過。
```

---

#### 結尾選項 B：回扣領導力主題

```
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
這是一種思維方式的進化。

從「我要控制一切」
到「我要設計系統，讓系統自己運轉」

這正是現代工程師應該學習的領導力。

---

去試吧。
從 L1 開始。
逐步進化。
直到你的 AI 系統可以獨立運轉。

這就是 Software 3.0 時代的工程師。
```

---

## 📊 金句提取

| 金句 | 用途 | 傳播力 |
|------|------|--------|
| **「計畫在哪裡，決定了系統的能力上限」** | 技術核心 | ⭐⭐⭐⭐⭐ |
| **「L1 是基礎，其他層都是能力升級」** | 架構理解 | ⭐⭐⭐⭐ |
| **「Context 不爆的秘密：計畫移入代碼」** | L3 核心 | ⭐⭐⭐⭐ |
| **「從控制一切，到設計系統」** | 思維轉變 | ⭐⭐⭐⭐⭐ |

---

## 🎨 內容配比檢查（技術文章版）

```
✅ 知識概念：1,500 字（60%）
   - 四層完整技術解析
   - 官方規格表
   - 代碼示例

✅ 感性敘事：250 字（10%）
   - 開場承接上篇
   - 結尾回扣領導力主題

✅ 清晰比喻：250 字（10%）
   - 延續「廚房→工廠」的比喻
   - 架構圖解

✅ 工程細節：500 字（20%）
   - 技術規格表
   - 代碼示例
   - 決策樹

✅ 結尾引流：100 字
   - 三件事行動號召
   - 系列預告
```

---

## 📋 發布前檢查清單

```
標題檢查
☐ 包含「Claude」關鍵詞（SEO）
☐ 延續上篇比喻（讀者親切感）
☐ 預告「四層」結構

內容檢查
☐ 承接上篇（讀者連結）
☐ 每層都有：定義 + 規格表 + 適用場景 + 代碼示例
☐ 決策樹清晰可操作
☐ 官方限制說明準確

技術準確性
☐ 版本號正確（v2.1.139+, v2.1.154+）
☐ 環境變數正確
☐ 官方引用準確
☐ 硬限制數字正確（16 並發、1000 總量）

風格檢查
☐ 60% 理性 + 40% 感性
☐ 有代碼示例（但不過多）
☐ 有比喻（延續上篇）
☐ 結尾有行動號召
```

---

## 📝 文章初稿框架

```
[標題]
Claude 四層 Agent 架構：從主廚到工廠

[開場 - 200 字]
上一篇，我們用「四個廚房」的比喻...
今天，我們來看技術原型...

[核心問題 - 200 字]
「誰持有計畫？」
[四層對應表]

[L1 Subagents - 400 字]
[定義 + 規格表 + 適用場景 + 代碼示例]

[L1.5 Agent View - 250 字]
[定義 + 規格表 + 適用場景]

[L2 Agent Teams - 350 字]
[定義 + 規格表 + 架構圖 + 適用場景 + 警告]

[L3 Dynamic Workflows - 400 字]
[定義 + 規格表 + 核心原理 + 硬限制 + 代碼示例]

[Skills - 150 字]
[定義 + 為什麼是「維度」]

[官方對比表 - 200 字]
[完整對比表]

[決策樹 - 300 字]
[流程圖 + 特殊情況]

[結尾 - 200 字]
[行動號召 + 系列預告]
```

---

## 🔗 系列化規劃

```
第一篇（已完成大綱）：
《不是權力大，是計畫清：四種領導力的真相》
→ 大眾篇，用廚房比喻講領導力

第二篇（本篇）：
《Claude 四層 Agent 架構：從主廚到工廠》
→ 技術篇，給工程師的完整指南

第三篇（規劃中）：
《從 L1 到 L3：我的真實遷移故事》
→ 實戰篇，具體項目的遷移過程

第四篇（規劃中）：
《Agent Teams 實戰：三人協作重構一個老項目》
→ L2 深潛，團隊協作的具體案例
```

---

## 📌 特別提醒

**這篇的成功關鍵**：
- ✅ 技術準確（工程師會驗證）
- ✅ 結構清晰（每層都是獨立模塊）
- ✅ 可操作（決策樹 + 代碼示例）
- ✅ 有靈魂（回扣「計畫持有權」的哲學）

**最大風險**：
- ❌ 太乾（純技術堆積，沒有故事）
- ❌ 太長（超過 4000 字會失去讀者）
- ❌ 版本過時（Claude 更新很快，需要核實）

**開始寫吧。**

