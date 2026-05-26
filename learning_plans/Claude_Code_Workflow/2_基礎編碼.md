---
name: stage-2-basic-coding
description: Claude Code Workflow 學習計劃 - 第 2 階段：基礎編碼
stage: 2
week: Week 2
estimated_hours: "6-7 小時"
status: pending
date: 2026-05-26
---

# 💻 第 2 階段：基礎編碼（Week 2）

## 🎯 階段目標

能寫出正確的 Workflow 語法，理解 JavaScript 異步編程在 Workflow 中的應用

**預期學習時間**：6-7 小時
**難度級別**：中級（需要 JavaScript 基礎）
**驗收標準**：完成所有實踐項目 + 通過檢查點

---

## 📋 任務清單

### 任務 2.1：設置 Claude Code Workflow 環境
**時間**：0.5 小時
**難度**：⭐ 簡單

#### 環境要求
- Claude Code CLI 已安裝（版本 2.1.47+）
- 終端機訪問權限
- JavaScript 運行環境

#### 設置步驟

**Step 1：檢查 Claude Code 版本**
```bash
claude --version
# 應顯示 v2.1.47 或更新
```

**Step 2：啟用 Workflow 功能**
```bash
export CLAUDE_CODE_WORKFLOWS_ENABLED=1
claude
```

**Step 3：驗證啟用成功**
- 啟動後，Claude Code 應顯示彩虹漸層的魔法入口
- 輸入 `ultraWork` 應該能觸發 Workflow 入口

#### 檢查項
- [ ] Claude Code 版本 ≥ 2.1.47
- [ ] 成功設置 `CLAUDE_CODE_WORKFLOWS_ENABLED=1`
- [ ] 能看到 Workflow 入口

#### 驗收標準
✅ 環境設置完成，Workflow 功能可用

---

### 任務 2.2：學習「Workflow 三要素」
**時間**：1 小時
**難度**：⭐⭐ 中等

#### 三要素詳解

**1️⃣ 元數據聲明（Metadata）**

元數據定義了 Workflow 的身份和版本信息：

```javascript
const metadata = {
  // 【必填】Workflow 的唯一名稱（使用蛇形命名法）
  name: "CodeReviewWorkflow",

  // 【必填】簡短描述（1-2 句）
  description: "自動化代碼審查與質量評估流程",

  // 【必填】版本號（使用語義版本 major.minor.patch）
  version: "1.0.0",

  // 【可選】作者信息
  author: "Rocky",

  // 【可選】更新日期
  lastUpdated: "2026-05-26"
};
```

**為什麼元數據重要？**
- 便於版本管理（Git 可以追蹤版本變化）
- 便於團隊理解（名稱和描述說明用途）
- 便於監控（系統可以記錄哪個版本在運行）

**2️⃣ 執行邏輯（Execution Logic）**

執行邏輯是一個異步函數，定義 Workflow 的各個 Stage 及其協作方式：

```javascript
// 使用 async 關鍵字，表示函數內可以使用 await
async function execute(context) {
  // context 是一個對象，包含了輸入數據和其他上下文信息

  // 解構輸入
  const { code } = context.input;

  // ===== Stage 1：語法檢查 =====
  // await 等待這個 Agent 完成才能進行下一步
  const syntaxResult = await agent.run("SyntaxCheckAgent", {
    code: code
  });

  // 檢查語法是否通過，如果不通過，立即返回
  if (!syntaxResult.passed) {
    return {
      success: false,
      reason: "語法檢查未通過",
      details: syntaxResult
    };
  }

  // ===== Stage 2：並行執行安全 + 性能分析 =====
  // Promise.all 實現並行執行
  const [securityResult, performanceResult] = await Promise.all([
    agent.run("SecurityAgent", { code }),
    agent.run("PerformanceAgent", { code })
  ]);

  // ===== Stage 3：整合報告 =====
  const finalReport = await agent.run("ReporterAgent", {
    syntax: syntaxResult,
    security: securityResult,
    performance: performanceResult
  });

  // ... 其他邏輯

  // 執行邏輯應該最後返回一個結果對象
  return {
    success: true,
    report: finalReport,
    metrics: { /* ... */ }
  };
}
```

**關鍵概念：`await` 和 `Promise.all()`**

- **`await`**：等待一個 Promise 完成（順序執行）
  ```javascript
  const result1 = await agent.run("Agent1");  // 等待 Agent1 完成
  const result2 = await agent.run("Agent2");  // 再執行 Agent2（順序）
  // 總耗時 = Agent1 + Agent2
  ```

- **`Promise.all()`**：同時等待多個 Promise（並行執行）
  ```javascript
  const [result1, result2] = await Promise.all([
    agent.run("Agent1"),
    agent.run("Agent2")
  ]);
  // 總耗時 = max(Agent1, Agent2) 較短
  ```

**3️⃣ 返回結果（Return Value）**

Workflow 的返回值必須是一個標準結構的對象：

```javascript
return {
  // 【必填】布爾值，表示是否成功
  success: true,

  // 【必填】主要輸出，內容根據 Workflow 用途變化
  output: finalReport,  // 或 result, data, recommendation 等

  // 【可選】詳細的執行指標
  metrics: {
    generatedAt: new Date().toISOString(),
    processingTimeMs: 2340,
    tokensUsed: 1245,
    stagesExecuted: 3
  },

  // 【可選】如果失敗，包含錯誤信息
  error: null  // 或 { code: "ERROR_CODE", message: "..." }
};
```

#### 動手練習

完成以下 3 個小練習，理解三要素：

**練習 1：寫出元數據**
```javascript
// 為以下場景寫出完整的元數據：
// 場景：一個用來檢查文章語法和風格的 Workflow
```

**練習 2：寫出簡單執行邏輯**
```javascript
// 寫一個有 2 個 Stage 的 Workflow：
// Stage 1：提取文章的 markdown 結構
// Stage 2：分析語氣和專業度
```

**練習 3：設計返回結果**
```javascript
// 為「文章質量評估」Workflow 設計返回結果結構
// 應該包括哪些字段？為什麼？
```

#### 驗收標準
✅ 能寫出完整的元數據聲明
✅ 理解 async/await 的基本用法
✅ 能設計合理的返回結果結構

---

### 任務 2.3：掌握 `Promise.all()` 用於並行 Agent
**時間**：1.5 小時
**難度**：⭐⭐⭐ 有挑戰

#### 為什麼需要並行執行？

**場景對比**：員工請假審批

❌ **串行方式（慢）**
```javascript
const policyCheck = await agent.run("PolicyAgent");    // 耗時 0.8s
const legalCheck = await agent.run("LegalAgent");      // 耗時 0.9s
// 總耗時：1.7s
```

✅ **並行方式（快）**
```javascript
const [policyCheck, legalCheck] = await Promise.all([
  agent.run("PolicyAgent"),    // 耗時 0.8s
  agent.run("LegalAgent")      // 耗時 0.9s（同時進行）
]);
// 總耗時：0.9s（取決於較慢的那個）
```

**性能提升**：1.7s → 0.9s，提升 **188%**！

#### `Promise.all()` 完全指南

**基本語法**
```javascript
const [result1, result2, result3] = await Promise.all([
  promise1,
  promise2,
  promise3
]);
```

**錯誤處理**
```javascript
try {
  const [result1, result2] = await Promise.all([
    agent.run("Agent1"),
    agent.run("Agent2")
  ]);
} catch (error) {
  // 如果任何一個 Promise 拒絕，整個 Promise.all 會拒絕
  return { success: false, error: error.message };
}
```

**與 Promise.allSettled() 的區別**
```javascript
// Promise.all()：任何一個失敗，全部失敗
const results = await Promise.all([...]);  // 全或無

// Promise.allSettled()：等所有完成，返回每個的狀態
const results = await Promise.allSettled([...]);
// 返回：[{ status: 'fulfilled', value: ... }, { status: 'rejected', reason: ... }]
```

#### 並行模式代碼示例

**模式 1：2 個並行 Agent**
```javascript
async function execute(context) {
  const [securityResult, performanceResult] = await Promise.all([
    agent.run("SecurityAgent", context.input),
    agent.run("PerformanceAgent", context.input)
  ]);

  return {
    success: true,
    output: { security: securityResult, performance: performanceResult }
  };
}
```

**模式 2：3 個並行 Agent + 聚合**
```javascript
async function execute(context) {
  const [selfEval, peerEval, managerEval] = await Promise.all([
    agent.run("SelfEvalAgent", context.input),
    agent.run("PeerEvalAgent", context.input),
    agent.run("ManagerEvalAgent", context.input)
  ]);

  // 聚合三個評價
  const aggregated = await agent.run("AggregatorAgent", {
    self: selfEval,
    peer: peerEval,
    manager: managerEval
  });

  return { success: true, output: aggregated };
}
```

**模式 3：混合串行和並行**
```javascript
async function execute(context) {
  // Stage 1：串行（必須按順序）
  const data = await agent.run("DataExtractionAgent", context.input);

  // Stage 2：並行（獨立進行）
  const [analysis1, analysis2] = await Promise.all([
    agent.run("AnalysisAgent1", data),
    agent.run("AnalysisAgent2", data)
  ]);

  // Stage 3：聚合
  const result = await agent.run("SynthesisAgent", {
    analysis1,
    analysis2
  });

  return { success: true, output: result };
}
```

#### 動手練習

**練習 1：改寫成並行版本**
```javascript
// 原始代碼（串行）：
const checkPolicy = await agent.run("PolicyAgent", data);
const checkLegal = await agent.run("LegalAgent", data);
const checkCompliance = await agent.run("ComplianceAgent", data);

// 改寫為並行版本：
// 你的代碼？
```

**練習 2：設計一個 4 個並行 Agent 的 Workflow**
```javascript
// 場景：商品上架前的全面檢查
// 需要檢查：
//   - 圖片質量
//   - 文案質量
//   - 價格合理性
//   - 庫存可用性
//
// 用 Promise.all() 實現 4 個並行 Agent
```

**練習 3：混合串行和並行**
```javascript
// 場景：
// Stage 1：提取訂單數據（串行）
// Stage 2：並行進行風險評估和價格驗證（並行）
// Stage 3：聚合決策（串行）
//
// 寫出完整的 execute 函數
```

#### 驗收標準
✅ 理解 `await` 和 `Promise.all()` 的區別
✅ 能寫出正確的並行執行代碼
✅ 知道何時使用並行、何時保持串行

---

### 任務 2.4：理解「Stage」的概念與信息流向
**時間**：1 小時
**難度**：⭐⭐ 中等

#### 什麼是 Stage？

**Stage = Workflow 中的一個獨立工作單元**

每個 Stage：
- 有清晰的輸入（前一個 Stage 的輸出或初始數據）
- 有明確的輸出（被後續 Stage 使用或作為最終結果）
- 由一個或多個 Agent 執行
- 可以被監控和測試

#### Stage 的設計原則

**原則 1：單一職責**
- ❌ 不好：Stage 包含「提取數據、檢查安全、檢查法律、生成報告」
- ✅ 好的：Stage 1 提取數據，Stage 2 檢查安全，Stage 3 檢查法律，Stage 4 生成報告

**原則 2：清晰的信息流**
```
【輸入】              【處理】                【輸出】
employee_data   →  Stage 1: Extract    →  structured_data
structured_data →  Stage 2: Validate   →  validation_result
validation_result → Stage 3: Generate   →  final_report
```

**原則 3：可觀測性**
每個 Stage 的輸出應該是可以被 `/workflows` 監控的：
```json
{
  "stageName": "PolicyValidation",
  "duration_ms": 850,
  "tokens_consumed": 450,
  "status": "SUCCESS",
  "output": { /* ... */ }
}
```

#### 信息流向圖示

**流水線（Pipeline）**
```
Input → Stage 1 → Stage 2 → Stage 3 → Output
```

**並行（Parallel）**
```
        ├→ Stage 2a →┐
Input → ├→ Stage 2b →→ Stage 3 → Output
        └→ Stage 2c →┘
```

**對抗驗證（Adversarial）**
```
        ├→ Agent A (Policy Check) ┐
Input → ├→ Agent B (Legal Check) ─→ Conflict Resolution → Output
```

#### 設計一個 Stage 的 5 個步驟

**Step 1：定義輸入**
```javascript
// 這個 Stage 需要什麼數據？
const { code, config } = context.input;
```

**Step 2：調用 Agent**
```javascript
// 哪個 Agent 執行這個 Stage？
const result = await agent.run("SecurityAnalysisAgent", { code, config });
```

**Step 3：驗證輸出**
```javascript
// 輸出是否符合預期？
if (!result.vulnerabilities || !Array.isArray(result.vulnerabilities)) {
  throw new Error("SecurityAgent returned invalid format");
}
```

**Step 4：信息傳遞**
```javascript
// 這個 Stage 的輸出會被下一個 Stage 使用
return {
  security_issues: result.vulnerabilities,
  risk_level: result.overallRisk,
  timestamp: new Date().toISOString()
};
```

**Step 5：錯誤處理**
```javascript
try {
  // Stage 邏輯
} catch (error) {
  // 是重試還是升級？
  if (error.isRetryable) {
    // 重試邏輯
  } else {
    // 升級給人類
  }
}
```

#### 動手練習：畫流程圖

為以下三個場景畫出 Stage 的流程圖（文本形式）：

**場景 1：新員工入職（Pipeline）**
- 資料審查 → 帳號創建 → 設備發放 → 歡迎信發送

**場景 2：年終績效評估（Parallel）**
- 並行：員工自評、同事評價、主管評價 → 聚合報告

**場景 3：高階晉升檢查（Adversarial）**
- 並行：公司政策檢查、法律合規檢查 → 衝突檢測 → 升級決策

#### 驗收標準
✅ 理解 Stage 的設計原則
✅ 能為 3 個不同的場景設計合理的 Stage 結構
✅ 知道如何使用流程圖表示 Stage 關係

---

### 任務 2.5：實踐項目 1 - 簡單代碼審查流
**時間**：1.5 小時
**難度**：⭐⭐⭐ 有挑戰

這是你的第一個完整 Workflow 代碼項目！

#### 項目場景

**功能**：User 提交代碼 → 自動審查 → 生成審查報告

**三個 Stage**：
1. **Stage 1：語法檢查** - 檢查代碼是否有語法錯誤
2. **Stage 2：安全掃描** - 檢查是否有安全漏洞
3. **Stage 3：生成報告** - 整合結果，生成最終報告

#### 實踐代碼框架

```javascript
// workflow.js

const metadata = {
  name: "CodeReviewWorkflow",
  description: "簡單的代碼審查流程",
  version: "1.0.0"
};

async function execute(context) {
  const { code } = context.input;

  // === Stage 1: 語法檢查 ===
  // 調用 SyntaxCheckAgent 檢查代碼語法
  // 如果失敗，立即返回結果

  // === Stage 2: 安全掃描 ===
  // 調用 SecurityAgent 檢查安全漏洞

  // === Stage 3: 生成報告 ===
  // 調用 ReporterAgent，整合 Stage 1 和 2 的結果

  // === 返回結果 ===
  return {
    success: true,
    output: finalReport
  };
}

module.exports = { metadata, execute };
```

#### 完成清單

完成以下任務以通過這個項目：

- [ ] 寫出完整的元數據聲明
- [ ] 實現 3 個 Stage 的執行邏輯
- [ ] Stage 1 失敗時，能正確返回錯誤信息
- [ ] 在終端運行 Workflow，確認代碼可以執行
- [ ] 使用 `/workflows` 命令，查看每個 Stage 的監控數據
- [ ] 驗證報告包含所有檢查結果

#### 驗收標準

✅ 代碼無語法錯誤，能在 Claude Code 中運行
✅ 三個 Stage 按順序執行
✅ `/workflows` 輸出顯示三個 Stage 的耗時、Token 消耗、狀態
✅ 最終報告格式合理，包含所有必要信息

#### 提交成果物

當完成時，你應該有：
1. `code_review_workflow.js` — 完整的 Workflow 代碼
2. `test_input.json` — 測試輸入（代碼片段）
3. `execution_log.txt` — `/workflows` 的輸出日誌

---

## ✅ 第 2 階段檢查點

完成以下檢查，才算完成第 2 階段：

- [ ] **環境就緒**：Claude Code Workflow 環境已設置
- [ ] **語法掌握**：理解元數據、執行邏輯、返回值三要素
- [ ] **異步理解**：能正確使用 `await` 和 `Promise.all()`
- [ ] **Stage 設計**：能為業務場景設計合理的 Stage 結構
- [ ] **項目完成**：實踐項目 1 成功運行

---

## 📚 參考資源

- **完整實踐篇**：AGENT_S01E04_Workflow工作流編排_Part2_實踐篇.md
- **代碼示例**：新世界 HR 系統 MVP 代碼庫
- **JavaScript 教程**：Promise/async 官方文檔
- **監控工具**：Claude Code 控制台 `/workflows` 命令

---

## 🎓 準備進入第 3 階段？

當你完成以上所有任務和檢查點後，你已準備好進入 **[第 3 階段：進階模式](./3_進階模式.md)**。

在第 3 階段中，你將：
- 實踐同步聚合模式（3 個並行 Agent）
- 實踐對抗驗證模式（衝突檢測 + 升級）
- 實踐累積式模式（事件日誌）
- 完成實踐項目 2-3

---

**階段狀態**：⏳ 待開始
**完成度**：0%
**預計完成日期**：2026-05-29
