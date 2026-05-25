---
name: workflow-memo-20260525
description: Claude Code Workflow 功能介紹與應用前景
metadata:
  type: memo
  date: 2026-05-25
  status: completed
  keyword: Workflow, Agent編排, 腳本化工程
---

# 📝 Claude Code Workflow 功能介紹與應用前景

**記錄日期**：2026-05-25
**來源**：staging/todo/ClaudeCodeWorkflow.md
**狀態**：✅ 記錄完成

---

## 🎯 核心概念

### 什麼是 Workflow？

Claude Code 在 **V2.1.47 / V2.1.48** 版本新增的功能：

> **用 JavaScript 代碼定義 Agent 編排，而非純自然語言指令**

從「臨場發揮」升級為「結構化腳本」。

### 觸發方式

```bash
# 1. 啟用環境變數
export CLAUDE_CODE_WORKFLOWS_ENABLED=1

# 2. 啟動 Claude Code
claude

# 3. 輸入關鍵詞（彩色漸層效果）
ultraWork [你的任務]
```

---

## 💡 五大核心優勢

| 優勢 | 解釋 | 計劃 1 應用 |
|------|------|----------|
| **精準可控** | JS 代碼定義流程，完全可觀測 | HR 審批流程的每一步都可追蹤 |
| **高度可複用** | 腳本可保存、分享、重複調用 | 一套「員工請假流程」可複用到「報銷」「培訓」 |
| **強大可觀測性** | `/workflows` 查看進度、Token、工具調用 | 監控每個 Agent 的執行時間和資源消耗 |
| **多種執行模式** | 6 種模式應對不同場景 | 流水線模式 → 審批流；對抗驗證 → 合規檢查 |
| **可迭代自定義** | 手動修改腳本優化流程 | 根據實際 HR 需求動態調整 |

---

## 🔄 六種執行模式

### 1. **流水線 (Pipeline)**
- **場景**：線性順序執行
- **計劃 1 用途**：員工請假申請 → AI 整理 → 主管審批 → 通知員工

### 2. **同步聚合 (Synchronous Aggregation)**
- **場景**：多個 Agent 並行，結果聚合
- **計劃 1 用途**：並行檢查多個政策、計算額度、驗證身份 → 整合成審批建議

### 3. **對抗驗證 (Adversarial Validation)**
- **場景**：多個 Agent 互相驗證，發現衝突
- **計劃 1 用途**：合規檢查 Agent vs 人力資源政策 Agent，發現風險

### 4. **末尾制**
- **場景**：篩選或排名最佳結果
- **計劃 1 用途**：當有多個報銷方案時，選出最優方案

### 5. **累積式 (Cumulative)**
- **場景**：逐步累積，最終生成綜合報告
- **計劃 1 用途**：累積月度請假記錄 → 生成年假統計

### 6. **嵌套式 (Nested)**
- **場景**：Workflow 內部調用其他 Workflow
- **計劃 1 用途**：「請假申請 Workflow」內部調用「政策查詢 Workflow」

---

## 🏗️ Workflow 腳本的核心要素

一個有效的 Workflow JS 腳本必須包含：

```javascript
// 1️⃣ 元數據 (Metadata)
const metadata = {
  name: "HR_LeaveApproval",
  description: "員工請假申請自動化流程"
}

// 2️⃣ Agent 方法調用（至少一次）
const result = await agent1.analyze(data)
const validated = await agent2.validate(result)

// 3️⃣ 結果回傳
return {
  approved: validated.status,
  reasoning: validated.reasoning,
  timestamp: new Date()
}
```

---

## 🎬 與計劃 1 的連接點

### 當前 MVP（Google Workspace 基礎）
```
Google Forms → Apps Script → Google Sheets
```
- 優點：低成本、快速上線
- 限制：邏輯固化在 Apps Script 中，難以調整

### Workflow 增強版
```
Ultrawork 腳本 → 多個 Agent 協作 → 結構化流程 → 可觀測 & 可複用
```

### 具體應用場景

#### **Stage 1：資料收集與整理**
```
Agent.Form 提取申請資料
  → Agent.Validation 檢查完整性
  → Agent.DataOrganizer 格式化
```

#### **Stage 2：政策檢查（對抗驗證模式）**
```
Agent.PolicyChecker（檢查公司政策）
  vs
Agent.ComplianceValidator（檢查法規）
  → 發現衝突 → 標記為「需要人工審核」
```

#### **Stage 3：審批建議生成（累積模式）**
```
累積：員工剩餘假期、申請天數、部門人力狀況
  → Agent.Reasoner 生成審批建議
  → 結果傳送主管
```

#### **Stage 4：可觀測性**
```
/workflows 查詢：
- Agent 執行時間：2.3s
- Token 消耗：1,245
- 調用工具：Google Sheets API, Gmail API
- 當前狀態：等待主管審批
```

---

## 📊 Workflow vs 傳統方式

| 維度 | 傳統 Apps Script | Workflow |
|------|-----------------|----------|
| 定義方式 | 硬編碼在代碼中 | JS 腳本動態生成 |
| 可調整性 | 低（需要修改代碼） | 高（修改 JS 即可） |
| 可觀測性 | 只能看日誌 | `/workflows` 完整監控 |
| Agent 協作 | 難以實現 | 原生支持多 Agent |
| 複用性 | 每個專案重新寫 | 腳本可分享複用 |

---

## 🚀 後續行動

### 短期（本週）
- [ ] 在本地環境測試 Workflow 功能激活
- [ ] 理解 `/workflows` 命令的監控界面
- [ ] 手寫一個簡單的 Pipeline 模式腳本

### 中期（6 月）
- [ ] 將計劃 1「員工請假」流程轉換為 Workflow 腳本
- [ ] 驗證多 Agent 協作的效果
- [ ] 對比 Workflow vs Google Apps Script 的效率

### 長期（戰略層面）
- [ ] 考慮使用 Workflow 重構計劃 1 MVP
- [ ] 將「可複用的 HR Workflow 腳本」作為產品化方向
- [ ] 在 GitHub 上發布「企業 HR Workflow 範本庫」

---

## 🔗 參考資源

- **源文檔**：`staging/todo/ClaudeCodeWorkflow.md`
- **計劃 1**：`計劃1_新世界HR系統/README.md`
- **當前 MVP**：`計劃1_新世界HR系統/newworld-hr-system/`

---

## 💭 核心洞見

Workflow 不只是「更好的 Agent 編排工具」，它代表著：

1. **從「指令式」到「聲明式」**：不再說「做什麼」，而是「想要什麼結構」
2. **從「黑箱」到「透明盒」**：每個 Agent 的行為都可被監控和驗證
3. **從「一次性」到「可複用」**：HR 流程不再是孤島，而是可跨部門複用的資產

**對計劃 1 的意義**：Workflow 可能讓我們從「Google Workspace 半自動化」升級為「Agent 驅動的全流程可視化」。

---

**記錄者**：Claude Code Haiku
**記錄時間**：2026-05-25
**下一步跟進**：測試 Workflow 激活
