# Workflow 戰報 #1：初體驗——多智能體編排的魔法時刻

**《Workflow 戰報》系列｜第 1 篇**
*新人類聯盟 · Homo Coalitio*

**日期**：2026-05-26
**進度**：Phase 1 完成 / Day 1
**今日關鍵詞**：#Workflow #多智能體 #HR系統 #開源

---

## 📍 今日戰果

今天，我做了一件以前從未想過可以這麼快完成的事——**讓多個 AI Agent 同時協作，完成一個企業級的請假審批流程**。

不是用 Python 寫幾萬行代碼，不是自己搭建複雜的 Session 管理系統，而是用一個簡單的 JavaScript 文件，定義好 Agent 之間的協作關係，然後看著它們自動運轉。

這感覺就像是，你一直以來都在用手動擋開車，突然有一天換成了自動駕駛。你不再需要關心什麼時候換檔、什麼時候踩離合，你只需要告訴系統：「我要去那裡。」

這就是 **Claude Code Workflow** 給我的第一印象：**非常新奇，好有趣，而且真的能完成長時間的複雜任務**。

---

## 🔧 技術細節

### 啟動 Workflow 的那一刻

要進入這個魔法世界，只需要兩行命令：

```bash
export CLAUDE_CODE_WORKFLOWS_ENABLED=1
claude
```

然後，你會看到一個彩虹漸層的魔法入口：`ultraWork [你的任務]`。

### 請假審批的五個 Stage

我今天實現的請假審批流程，被拆解成了五個清晰的階段：

```javascript
// leave_approval.js 核心結構

Stage 1: 數據收集
  └─ DataCollector Agent 從 Google Form 提取申請信息

Stage 2: 並行檢查（SyncAgg 模式）
  ├─ PolicyChecker Agent 檢查公司政策
  └─ LegalChecker Agent 檢查勞動法規

Stage 3: 衝突分析（Adversarial 模式）
  └─ 如果 Stage 2 有衝突，兩個 Agent 互相對抗驗證

Stage 4: 假期計算
  └─ Calculator Agent 計算剩餘假期、生成建議

Stage 5: 執行批准
  └─ Executor Agent 更新系統、發送通知
```

最讓我驚艷的是 **Stage 2 的並行執行**。在傳統的開發中，你需要自己寫多線程或異步代碼來實現並行。但在 Workflow 中，只需要一行：

```javascript
const [policyResult, legalResult] = await Promise.all([
  agent.run("PolicyChecker", { data }),
  agent.run("LegalChecker", { data })
]);
```

兩個 Agent 同時工作，誰先完成誰先返回，最後系統自動聚合結果。

### 今日產出

| 指標 | 數據 |
|------|------|
| 文件數 | 4 個 |
| 代碼行數 | 2,171 行 |
| Workflow 模式 | 4 種（Pipeline、SyncAgg、Adversarial、Nested） |
| GitHub 倉庫 | [newworld-hr-system](https://github.com/pppeee861005/newworld-hr-system) |

---

## 💥 踩坑記錄

### 坑 1：分支歷史不相關

當我嘗試從遠端拉取代碼時，遇到了這個錯誤：

```
fatal: refusing to merge unrelated histories
```

**原因**：本地的 `master` 分支和遠端的 `main` 分支是兩個完全獨立的歷史。

**解決方案**：

```bash
git merge origin/main --allow-unrelated-histories
```

然後手動解決 README.md 的衝突，選擇正確的倉庫連結。

### 坑 2：Stage 之間的數據傳遞

一開始，我不確定如何在 Stage 之間傳遞數據。後來發現，Workflow 使用標準的 JavaScript 變量作用域，上一個 Stage 的返回值可以直接被下一個 Stage 使用。

```javascript
const stage1Result = await agent.run("DataCollector", { ... });
const stage2Result = await agent.run("PolicyChecker", {
  data: stage1Result  // 直接傳遞
});
```

簡單、直觀、符合直覺。

---

## 🎯 明日預告

明天，我將深入解析 `leave_approval.js` 的每一個 Stage：

1. **DataCollector Agent** 如何從 Google Form 提取和驗證數據
2. **PolicyChecker Agent** 如何讀取公司政策並做出判斷
3. **Adversarial 模式** 如何讓兩個 Agent 互相挑戰

這將是第一次完整展示**一個生產級 Workflow 的內部結構**。

---

## 💡 今日金句

> **「Workflow 不是腳本，是協作模式。你不是在寫程序，你是在設計組織。」**

---

## 📊 系列進度

```
Phase 1: 基礎架構  ████████████ 100% ✅ 今日完成
Phase 2: 功能完善  ░░░░░░░░░░░░   0%   6月1日啟動
Phase 3: 生產部署  ░░░░░░░░░░░░   0%   待規劃
```

---

## 🔗 相關連結

- **GitHub 倉庫**：[newworld-hr-system](https://github.com/pppeee861005/newworld-hr-system)
- **Agent 系列 E04**：[Workflow 工作流編排](link-to-e04)
- **系列規劃**：[Workflow 戰報系列](link-to-series)

---

**系列導航**：系列首篇 | [下一篇 →]

---

*新人類聯盟 · Homo Coalitio*
*《AI 指揮官筆記》Substack · 2026.05.26*
*aiagentcommander.substack.com*
