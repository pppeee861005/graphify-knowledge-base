---
name: stage-3-advanced-patterns
description: Claude Code Workflow 學習計劃 - 第 3 階段：進階模式
stage: 3
week: Week 3
estimated_hours: "8-9 小時"
status: pending
date: 2026-05-26
---

# 🔧 第 3 階段：進階模式（Week 3）

## 🎯 階段目標

掌握並行、聚合、對抗驗證等複雜模式，能根據業務需求選擇合適的執行模式

**預期學習時間**：8-9 小時
**難度級別**：高級（複雜的業務邏輯 + 錯誤處理）
**驗收標準**：完成 3 個實踐項目 + 理解 6 種執行模式

---

## 📋 任務清單

### 任務 3.1：實踐「同步聚合模式」（Synchronous Aggregation）
**時間**：2 小時
**難度**：⭐⭐⭐ 有挑戰

#### 模式說明

**核心概念**：多個 Agent 並行執行，最後將結果聚合

```
        ├→ Agent 1 ┐
Input → ├→ Agent 2 →→ Aggregator → Output
        └→ Agent 3 ┘
```

#### 實踐場景：年終績效評估

**業務需求**：
- 同時收集「員工自評」、「同事評價」、「主管評價」
- 根據三方意見，生成最終績效報告

**代碼框架**
```javascript
async function execute(context) {
  const { employeeId } = context.input;

  // ===== Stage 1：並行收集三方評價 =====
  const [selfEval, peerEval, managerEval] = await Promise.all([
    agent.run("SelfEvalAgent", { employeeId }),
    agent.run("PeerEvalAgent", { employeeId }),
    agent.run("ManagerEvalAgent", { employeeId })
  ]);

  // ===== Stage 2：聚合報告 =====
  const finalReport = await agent.run("PerformanceAggregatorAgent", {
    selfEval,
    peerEval,
    managerEval
  });

  return { success: true, output: finalReport };
}
```

#### 驗收標準
- ✅ 三個 Agent 並行執行（不是串行）
- ✅ `/workflows` 顯示三個 Agent 的並行耗時
- ✅ 聚合邏輯正確處理三方意見

---

### 任務 3.2：實踐「對抗驗證模式」（Adversarial Validation）
**時間**：2 小時
**難度**：⭐⭐⭐ 有挑戰

#### 模式說明

**核心概念**：兩個或多個 Agent 給出獨立結論，若衝突則觸發人工升級

```
        ├→ Agent A (Policy) ┐
Input → ├→ Agent B (Legal) ─→ Conflict Detection → Escalate / Proceed
```

#### 實踐場景：晉升名單合規檢查

**業務需求**：
- 「內部政策 Agent」檢查是否符合內部晉升年限規定
- 「法律合規 Agent」檢查是否符合勞動法比例規定
- 如果兩個 Agent 的結論衝突，自動升級給 HRVP 手動決策

**代碼框架**
```javascript
async function execute(context) {
  const { candidateList } = context.input;

  // ===== Stage 1：並行進行兩方檢查 =====
  const [policyCheck, legalCheck] = await Promise.all([
    agent.run("InternalPolicyAgent", { candidateList }),
    agent.run("LegalComplianceAgent", { candidateList })
  ]);

  // ===== Stage 2：衝突檢測與處理 =====
  const conflictExists = policyCheck.approved !== legalCheck.approved;

  if (conflictExists) {
    // 衝突時升級給人工
    return {
      success: false,
      status: "ESCALATED",
      reason: `政策與法律結論衝突：政策=${policyCheck.approved}, 法律=${legalCheck.approved}`,
      details: {
        policy: policyCheck,
        legal: legalCheck
      },
      escalatedTo: "HRVP"
    };
  }

  // 無衝突，繼續流程
  return {
    success: true,
    output: { approved: policyCheck.approved }
  };
}
```

#### 驗收標準
- ✅ 兩個 Agent 給出相同結論時，流程通過
- ✅ 兩個 Agent 結論衝突時，自動升級狀態為 ESCALATED
- ✅ 升級通知包含兩方的完整論據

---

### 任務 3.3：實踐「累積式模式」（Cumulative Pattern）
**時間**：1.5 小時
**難度**：⭐⭐ 中等

#### 模式說明

**核心概念**：隨著流程推進，信息不斷被加入到同一個事件日誌

```
Input → Stage 1 (記錄信息) → Stage 2 (累積信息) → Stage 3 (最終報告)
```

#### 實踐場景：離職交接追蹤

**業務需求**：
- 員工提交離職申請（記錄第一步）
- 進行離職面談（累積面談記錄）
- 進行資產交接（累積交接清單）
- 最後生成完整的離職結案報告

**代碼框架**
```javascript
async function execute(context) {
  const { employeeId } = context.input;

  // 初始化事件日誌
  const eventLog = {
    employeeId,
    events: [],
    timestamp: new Date().toISOString()
  };

  // ===== Stage 1：提交離職申請 =====
  const resignationRecord = await agent.run("ResignationRecorderAgent", {
    employeeId
  });
  eventLog.events.push({
    stage: "Resignation",
    data: resignationRecord,
    timestamp: new Date().toISOString()
  });

  // ===== Stage 2：進行離職面談 =====
  const exitInterview = await agent.run("ExitInterviewAgent", {
    employeeId,
    previousEvents: eventLog.events
  });
  eventLog.events.push({
    stage: "ExitInterview",
    data: exitInterview,
    timestamp: new Date().toISOString()
  });

  // ===== Stage 3：進行資產交接 =====
  const assetHandover = await agent.run("AssetHandoverAgent", {
    employeeId,
    previousEvents: eventLog.events
  });
  eventLog.events.push({
    stage: "AssetHandover",
    data: assetHandover,
    timestamp: new Date().toISOString()
  });

  // ===== Stage 4：生成結案報告 =====
  const finalReport = await agent.run("ExitSummaryAgent", {
    eventLog
  });

  return {
    success: true,
    output: finalReport,
    eventLog
  };
}
```

#### 驗收標準
- ✅ 事件日誌逐步累積每個 Stage 的數據
- ✅ 後續 Stage 能訪問所有之前的事件
- ✅ 最終報告完整反映整個過程

---

### 任務 3.4：實踐「嵌套式工作流」（Nested Workflow）
**時間**：2 小時
**難度**：⭐⭐⭐⭐ 最難

#### 模式說明

**核心概念**：一個 Workflow 的某個 Stage 內部是一個完整的子 Workflow

```
Main Workflow
  ├─ Stage 1
  ├─ Stage 2
  │   ├─ Sub-Workflow-1
  │   ├─ Sub-Workflow-2
  └─ Stage 3
```

#### 實踐場景：差旅審批工作流

**業務需求**：
- Main：差旅審批流程
  - Stage 1：提交差旅申請
  - Stage 2：進行複雜的費用計算（含外幣、稅務）← **包含子流程**
  - Stage 3：審批決策

**代碼框架**
```javascript
// 子 Workflow：外幣匯率轉換 + 稅務申報
async function executeForexAndTaxWorkflow(context) {
  // 子流程的邏輯
}

// 主 Workflow：差旅審批
async function execute(context) {
  const { travelRequest } = context.input;

  // ===== Stage 1：提交申請 =====
  const requestData = await agent.run("TravelRequestParserAgent", {
    travelRequest
  });

  // ===== Stage 2：複雜費用計算（嵌套子 Workflow） =====
  const costAnalysis = await executeForexAndTaxWorkflow({
    input: requestData
  });

  // ===== Stage 3：審批決策 =====
  const approval = await agent.run("ApprovalDecisionAgent", {
    requestData,
    costAnalysis
  });

  return {
    success: true,
    output: approval
  };
}
```

#### 驗收標準
- ✅ 子 Workflow 能正確執行
- ✅ 子 Workflow 的輸出能被主 Workflow 正確使用
- ✅ `/workflows` 能追蹤嵌套的執行軌跡

---

### 任務 3.5：學習「衝突解決機制」與「異常處理」
**時間**：1.5 小時
**難度**：⭐⭐⭐ 有挑戰

#### 衝突解決機制

**常見衝突場景**：
- 兩個 Agent 給出矛盾結論（對抗驗證）
- 資源競爭（如果某個資源有限）
- 優先級衝突（多個流程同時進行）

**解決策略**：

**1️⃣ 人工升級（Escalate）**
```javascript
if (conflictDetected) {
  return {
    status: "ESCALATED",
    escalatedTo: "manager",
    reason: "Agent A vs Agent B 結論衝突",
    requiresApproval: true
  };
}
```

**2️⃣ 多數表決**
```javascript
const results = [resultA, resultB, resultC];
const approvals = results.filter(r => r.approved).length;
const decision = approvals >= 2;  // 2/3 贊同
```

**3️⃣ 加權決策**
```javascript
const weightedScore =
  resultA.score * 0.4 +  // 策略權重 40%
  resultB.score * 0.3 +  // 法律權重 30%
  resultC.score * 0.3;   // 業務權重 30%
```

#### 異常處理模式

**模式 1：重試**
```javascript
async function executeWithRetry(agentName, input, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await agent.run(agentName, input);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await delay(1000 * (i + 1));  // 指數退避
    }
  }
}
```

**模式 2：降級（Fallback）**
```javascript
try {
  return await agent.run("PrimaryAgent", input);
} catch (error) {
  // 如果主 Agent 失敗，使用備選方案
  return await agent.run("FallbackAgent", input);
}
```

**模式 3：部分失敗（Partial Failure）**
```javascript
const results = await Promise.allSettled([
  agent.run("Agent1", input),
  agent.run("Agent2", input)
]);

const successResults = results
  .filter(r => r.status === 'fulfilled')
  .map(r => r.value);

if (successResults.length === 0) {
  throw new Error("All agents failed");
}

// 用至少一個成功的結果繼續
```

#### 完整的異常處理示例

```javascript
async function execute(context) {
  try {
    const [result1, result2] = await Promise.all([
      executeWithRetry("Agent1", context.input),
      executeWithRetry("Agent2", context.input)
    ]);

    // 衝突檢測
    if (result1.decision !== result2.decision) {
      // 升級處理
      return {
        status: "ESCALATED",
        details: { result1, result2 }
      };
    }

    return {
      success: true,
      output: result1
    };
  } catch (error) {
    // 降級處理
    return {
      success: false,
      status: "FALLBACK",
      reason: error.message
    };
  }
}
```

---

## 🏆 實踐項目 2 & 3

### 項目 2️⃣：員工年終績效評估（Synchronous Aggregation）

**功能**：
- 同時啟動三個評估 Agent（自評、同事、主管）
- 聚合成最終績效報告

**驗收標準**：
- [ ] 三個 Agent 真正並行（不是串行）
- [ ] `/workflows` 顯示並行耗時優勢
- [ ] 聚合報告包含三方意見

### 項目 3️⃣：晉升名單合規檢查（Adversarial Validation）

**功能**：
- 「政策 Agent」vs「法律 Agent」
- 衝突時升級給 HRVP

**驗收標準**：
- [ ] 一致結論時流程通過
- [ ] 衝突結論時自動升級
- [ ] 升級信息包含完整論據

---

## ✅ 第 3 階段檢查點

- [ ] **並行理解**：理解 Synchronous Aggregation 的優勢
- [ ] **衝突處理**：能設計合理的衝突解決機制
- [ ] **異常處理**：實現重試、降級、部分失敗的完整邏輯
- [ ] **模式掌握**：能為不同場景選擇合適的執行模式
- [ ] **項目完成**：實踐項目 2-3 成功運行

---

## 📚 參考資源

- Agent E04 Part 2：六種執行模式詳解
- 新世界 HR 系統代碼庫：對抗驗證範例
- Promise 官方文檔：錯誤處理和重試模式

---

## 🎓 準備進入第 4 階段？

當完成第 3 階段後，進入 **[第 4 階段：企業級應用](./4_企業級應用.md)**。

---

**階段狀態**：⏳ 待開始
**完成度**：0%
**預計完成日期**：2026-06-02
