---
name: claude-code-workflow-cheatsheet
description: Claude Code Workflow 核心概念速查手冊
date: 2026-05-26
type: reference
priority: 核心參考
---

# 🔧 Claude Code Workflow 核心速查

## 📌 一句定義

**Workflow** 是 Claude Code（V2.1.47+）推出的功能，讓開發者用 JavaScript 來**聲明式地定義多個 Agent 的協作關係**，而不是靠寫複雜的 Prompt。

---

## ⚡ 啟用方式（新版 v2.1.47+）

```bash
# 設置環境變量
export CLAUDE_CODE_WORKFLOWS=1
export DISABLE_GROWTHBOOK=1
source ~/.zshrc

# 驗證環境變量已設置
echo "$CLAUDE_CODE_WORKFLOWS / $DISABLE_GROWTHBOOK"
# 應輸出：1 / 1

# 啟動新版 Claude Code
claude
```

啟用後，Claude Code 會顯示彩虹漸層的魔法入口：**workflow [你的任務]**

---

## 🎯 Prompt vs Workflow 的核心區別

| 維度 | Prompt（舊） | Workflow（新） |
|-----|----------|----------|
| **編程對象** | 對個體智慧的壓榨 | 對組織結構的編排 |
| **輸出可預測性** | ❌ 不可預測 | ✅ 完全可控 |
| **流程控制** | ❌ 黑箱，無法管制 | ✅ 透明盒，每步可見 |
| **複用性** | ❌ 難以版本控制 | ✅ 標準 JavaScript 代碼 |
| **多 Agent 協作** | ❌ 困難 | ✅ 原生支持 |

---

## 🏗️ 最簡 Workflow 三要素

```javascript
// 1️⃣ 元數據聲明
const metadata = {
  name: "WorkflowName",
  description: "描述功能",
  version: "1.0.0"
};

// 2️⃣ 執行邏輯（異步函數）
async function execute(context) {
  // Stage 1
  const result1 = await agent.run("Agent1", { data });

  // Stage 2：並行執行
  const [result2a, result2b] = await Promise.all([
    agent.run("Agent2", { data }),
    agent.run("Agent3", { data })
  ]);

  // 3️⃣ 返回標準結果
  return {
    success: true,
    output: result,
    metrics: { generatedAt: new Date().toISOString() }
  };
}
```

---

## 📊 六種核心執行模式

1. **Pipeline（流水線）**：A → B → C 線性順序
2. **Synchronous Aggregation（同步聚合）**：並行 → 聚合結果
3. **Adversarial Validation（對抗驗證）**：兩個 Agent 互相審查
4. **Best-of Mode（末尾篩選）**：多版本方案，選最優
5. **Cumulative Pattern（累積式）**：信息逐步累積
6. **Nested Workflow（嵌套式）**：Workflow 內部有小 Workflow

---

## 🔍 實時監控

Workflow 執行完成後，在終端機輸入：

```bash
/workflows
```

會看到每個 Stage 的：
- ⏱️ 耗時（ms）
- 💾 Token 消耗
- 📊 狀態（SUCCESS / FAILED / ESCALATED）
- 🎯 使用的模型版本
- 📈 詳細的輸出與指標

---

## 💡 三大範式轉變

### 1️⃣ 指令式 → 聲明式
- **舊**：告訴 AI「一步步要做什麼」
- **新**：定義「數據流的拓撲結構」

### 2️⃣ 黑箱 → 透明盒
- **舊**：神祕的輸出，無法追蹤
- **新**：每步都可見，完全可觀測

### 3️⃣ 一次性 → 可複用資產
- **舊**：Prompt 難以版本控制
- **新**：代碼形式，支援 Git、測試、複用

---

## 🌟 Software 3.0 的信號

```
【Software 1.0】  Input ──(手寫代碼)──▶ Output
【Software 2.0】  Input ──(機器學習)──▶ Output
【Software 3.0】  Input ──(工作流編排)──▶ Output  ← Workflow 就是這個！
```

在 Software 3.0 時代，我們編程的對象是：**「智慧本身的組織結構」**

---

## 🎯 四個金句

1. **「Prompt 是對個體智慧的壓榨，而 Workflow 是對組織結構的編排。」**
2. **「當 AI 應用不再是神祕莫測的魔法，而是可觀測、可調優的系統，它才真正具備工業價值。」**
3. **「Workflow 工程讓 AI 按照結構做事。這是 AI 應用走向成熟的唯一路徑。」**
4. **「未來企業最核心資產，是沉澱的『AI Workflow 流程庫』——企業的數字大腦運行圖。」**

---

**快速導航**：[完整學習計劃](../README.md)
