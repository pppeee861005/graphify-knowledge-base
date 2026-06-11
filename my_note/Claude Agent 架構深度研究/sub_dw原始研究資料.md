# 🔍 Claude Agent 架構深度研究
## 官方文件校準版

---

## 🎯 核心發現概覽（5 大重點）

查完官方文件後，有 **5 個重要發現** 需要特別關注：

### ① 官方是「四層」結構，不是三層
- **遺漏的一層**：Agent View（v2.1.139 加入）
- **定位**：你自己在監控多個背景 session
- **層級**：介於 Subagents 和 Agent Teams 之間

### ② Dynamic Workflows 的真正突破點：計畫移入程式碼
**不是「並行」，而是架構根本性轉變**

官方說法：
> With subagents, skills, and agent teams, Claude is the orchestrator: it decides turn by turn what to spawn or assign next, and every result lands in a context window. A workflow script holds the loop, the branching, and the intermediate results itself, so Claude's context holds only the final answer.

**這才是 context window 不爆的根本原因。**

### ③ 對你的 stock-swarm-wf 的關鍵校準
**兩個層次，同名不同物**

| 維度 | 官方 Dynamic Workflows | 你的 stock-swarm-wf |
|------|----------------------|---------------------|
| 形式 | Claude 動態撰寫 JS | TypeScript 寫死 npm 套件 |
| 層級 | 應用層 | Agent SDK 自訂框架層 |
| 優勢 | 自適應 | 更底層、可控、可發布 |

**重要**：你的方案**不是複製**，而是**差異化定位**——更深層、更可控、更有發布價值。

### ④ Agent Teams 的真正特性：橫向 peer 通訊
**不是純 supervisor 樹狀結構**

官方說法：
> Unlike subagents, which run within a single session and can only report back to the main agent, you can also interact with individual teammates directly without going through the lead.

**含義**：
- Teammate 可以直接互相通訊
- 不需透過 lead 轉達
- 這是真正的對等協作（peer-to-peer）

### ⑤ 架構重新設計的指南
根據官方規範重新校準你的架構設計方向

---

## 🔑 官方核心問題

### **「誰持有計畫（Who holds the plan）？」**

**這一個問題決定了你應該用哪一層。**

**重要原則**：四層不是替代關係，是**能力升級關係**。

---

## 📊 四層 Agent 架構完整對比

### **第一層：Subagents（工作層）**

| 維度 | 說明 |
|------|------|
| **本質** | Claude 召喚的 worker |
| **誰決定下一步** | Claude，逐回合決定 |
| **誰持有計畫** | Claude（每回合決定） |
| **中間結果** | 放在 Claude 的 context window |
| **可重複性** | Worker 定義可重複，流程不可重複 |
| **規模** | 每回合少量委派任務 |
| **定義方式** | `.claude/agents/*.md` 或程式定義 |

**官方關鍵特性**：
> "Subagents help you: Preserve context · Enforce constraints · Reuse configurations · Specialize behavior · Control costs by routing tasks to faster, cheaper models like Haiku"

**隔離性**：每個 subagent 有自己乾淨的 context window
**巢狀限制**：Subagent 不能再 spawn 自己的 subagent
**回傳**：只有最終訊息回到 parent，中間 tool call 不回傳
**儲存位置**：`.claude/agents/`（專案）或 `~/.claude/agents/`（個人）
**觸發方式**：Claude 自動根據 description 決定，或明確指定名稱

---

### **第 1.5 層：Agent View（監控層）**

| 維度 | 說明 |
|------|------|
| **本質** | 背景 session 監控 |
| **誰持有計畫** | 你（人類監控多個 session） |
| **中間結果** | 各 session 獨立，你從 UI 監看 |
| **特性** | 可 attach 進入任一 agent 對話 |
| **版本需求** | v2.1.139+ |

**新加入的中間層**：讓你有對多個背景任務的可視化控制

---

### **第二層：Agent Teams（協作層）**

| 維度 | 說明 |
|------|------|
| **本質** | Lead + peer sessions |
| **狀態** | 實驗性功能 |
| **誰決定下一步** | Lead agent（逐回合決定） |
| **中間結果** | 共享任務清單（shared task list） |
| **可重複性** | Team 定義可重複 |
| **規模** | 少數長時間運行的 peer sessions |
| **啟用方式** | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` |

**官方關鍵特性**：
> "Unlike subagents, which run within a single session and can only report back to the main agent, you can also interact with individual teammates directly without going through the lead."

**最佳場景**：
- 前端/後端/測試各自擁有的跨層修改
- Teammate 可互相通訊、挑戰彼此

**不適合**：
- 序列任務
- 同檔案編輯
- 高依賴性工作

**注意**：
- Token 消耗遠高於單一 session
- 仍屬實驗性，有已知 session 恢復限制
- 你可以直接 attach 進任一 teammate session

---

### **第三層：Dynamic Workflows（規模層）**

| 維度 | 說明 |
|------|------|
| **本質** | Script holds the plan |
| **狀態** | 研究預覽 |
| **誰持有計畫** | Script（程式碼本身） |
| **誰決定下一步** | Script（完全自動化） |
| **中間結果** | 存在 script 變數，不佔 context |
| **可重複性** | 編排本身可重複 |
| **規模** | 每次執行數十到數百個 agent |

**官方定義**：
> "A dynamic workflow is a JavaScript script that orchestrates subagents at scale. Claude writes the script for the task you describe, and a runtime executes it in the background while your session stays responsive."

**關鍵指令**：
- `/deep-research`（內建）
- `ultracode`（關鍵字觸發）

**高級特性**：
- **可儲存**：Script 可存為 `.claude/workflows/` 自訂指令
- **可恢復**：同一 session 內可 resume（退出後重新開始）
- **隔離**：`isolation: 'worktree'` 給每個 agent 獨立 repo 副本
- **質量保證**：獨立 agent 互相對抗性審查，結果經 cross-check 才輸出

**官方硬限制**：
- **並發上限**：16 個 agents 同時執行
- **總量上限**：1,000 agents per run（防止無限迴圈）
- **巢狀限制**：Subagent 不能再 spawn subagent
- **版本要求**：v2.1.154+（2026/05/28 發布），需 Pro/Max/Team/Enterprise

---

### **第四層：Skills（擴展層）**

| 維度 | 說明 |
|------|------|
| **本質** | Claude 遵循的指令文件 |
| **誰持有計畫** | 指令文件本身 |
| **中間結果** | context window |
| **可重複性** | 指令本身 |

**位置**：是正交維度，與其他三層結合使用

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

---

## 🎓 你之前的理解 vs 官方實際定義

### **修正點 1：Dynamic WF 是 Claude 寫的，不是你寫的**

**官方定義**：Claude 根據你的描述自動撰寫 JavaScript 腳本，runtime 在背景執行。

**與你規劃的區別**：
- 官方 WF：自動生成、動態適應
- 你的方案：TypeScript npm 套件、發布可復用

**真實定位**：你的方案其實更接近「自訂 Agent SDK 框架」，不是「複製官方 WF」。

### **修正點 2：Agent Teams 是橫向 peer，不是垂直 hierarchy**

官方強調 teammate 可以**直接互相通訊**，不需透過 lead 轉達。

- 你之前的理解：純 supervisor 架構
- 官方實際定義：真正的 peer-to-peer 協作
- **關鍵操作**：你可以直接 attach 進任一 teammate session

---

## 🚀 stock-swarm-wf 的重新定位

### **架構層次對比**

```
官方 WF：ultracode 觸發 → Claude 寫 JS → runtime 執行
你的 WF：TypeScript 寫死編排邏輯 → npm 發布 → 任何人可引用
```

### **關鍵認知轉變**

**兩者都叫 Dynamic Workflows，但層次不同**：
- 官方：應用層（高度自適應）
- 你的：框架層（高度可控、可發布）

**你的優勢**：
- ✅ 更底層（Agent SDK 自訂框架）
- ✅ 更可控（TypeScript 類型安全）
- ✅ 更可發布（npm 開源生態）
- ✅ 更可重複（任何人可使用）

**這不是衝突，是**差異化定位**。**

---

## 📌 決策樹：應該用哪一層？

```
開始
  ↓
「誰持有計畫？」

1️⃣ Claude（逐回合決定）
   └─ 使用 Subagents（L1）
       └─ 多個獨立背景任務？
           └─ 是 → Agent View（L1.5）

2️⃣ Team Lead（共同決定）
   └─ 使用 Agent Teams（L2）
       └─ 需要彼此通訊嗎？
           └─ 是 → 充分利用 peer-to-peer 特性

3️⃣ Script（程式碼本身）
   └─ 使用 Dynamic Workflows（L3）
       └─ 規模需求？
           └─ 數十到數百 agents → 適合
           └─ 超過 1000 agents → 超限警告
```

---

## 🔗 關鍵數字速查

| 指標 | 數值 |
|------|------|
| 官方架構層數 | 4 層（含 Agent View） |
| 最小 Agent 並發 | 16 個（同時執行限制） |
| 最大 agents per run | 1,000（防止無限迴圈） |
| 最低版本要求（L3） | v2.1.154+（2026/05/28） |
| Agent View 最低版本 | v2.1.139+ |
| 能否巢狀 spawn subagent | ❌ 不能 |
| Agent Teams 狀態 | 🔬 實驗性 |
| Dynamic Workflows 狀態 | 🔬 研究預覽 |

---

## 💡 核心設計原則

### **「計畫持有權」決定架構選擇**

1. **Subagents（L1）**：Claude 掌握完整計畫，逐回合分派
   💰 Token 效率最高 | 📊 規模有限

2. **Agent View（L1.5）**：人類管理多個獨立背景任務
   👁️ 可視化控制 | 🎯 人在 loop

3. **Agent Teams（L2）**：集體決策，真正的 peer 協作
   🤝 橫向通訊 | ⚠️ Token 消耗大

4. **Dynamic Workflows（L3）**：計畫在程式碼中，自動化最高
   📈 規模最大 | 🚀 完全自動

### **四層是能力升級，不是選擇替代**

- L1 是基礎，其他層都建基於 L1 的能力
- L1.5 擴展了人類的監控能力
- L2 添加了團隊協作維度
- L3 啟用了超大規模編排

---

## 📚 官方參考資源

- 官方文件主頁：code.claude.com/docs/en/workflows
- Dynamic Workflows 深度說明文頁面
- Agent Teams 實驗性功能文檔
- Agent View 背景 session 管理指南
