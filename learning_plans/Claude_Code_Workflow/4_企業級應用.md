---
name: stage-4-enterprise-application
description: Claude Code Workflow 學習計劃 - 第 4 階段：企業級應用
stage: 4
week: Week 3-4
estimated_hours: "10-12 小時"
status: pending
date: 2026-05-26
---

# 🏢 第 4 階段：企業級應用（Week 3-4）

## 🎯 階段目標

設計並實現一個完整的企業級 Workflow 系統（基於真實業務），整合多個執行模式

**預期學習時間**：10-12 小時
**難度級別**：企業級（完整的系統設計）
**驗收標準**：完成 2 個企業級項目 + 完整的文檔

---

## 📋 任務清單

### 任務 4.1：分析「新世界 HR 審批系統」案例
**時間**：2 小時
**難度**：⭐⭐ 中等

#### 案例背景

新世界 HR 審批系統是一個完整的員工請假智慧審批流程，整合了以下特性：

- **多 Stage 協作**：4 個主要 Stage
- **對抗驗證**：公司政策 vs 法律合規
- **Human-in-the-Loop**：衝突時升級給人工
- **實時監控**：完整的性能數據

#### 完整流程分析

```
【員工提交請假表單】
         │
         ▼
    ┌─────────────────┐
    │ Stage 1: Data   │ → 提取申請人、天數、理由
    │ Collection      │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────────────┐
    │ Stage 2: Policy Check   │ (並行執行)
    │ ├─ CompanyPolicyAgent   │ → 檢查公司規定
    │ └─ LegalComplianceAgent │ → 檢查勞基法
    └────────┬────────────────┘
             │
      ┌──────┴──────┐
   一致          衝突
    │              │
    │              ▼
    │         Escalate to HR
    │
    ▼
┌──────────────────┐
│ Stage 3: Gen.    │ → 生成審批建議
│ Recommendation   │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│ Stage 4:             │ (並行)
│ ├─ SendEmail        │
│ └─ LogToGoogleSheet │
└──────────────────────┘
```

#### 關鍵設計點

**1️⃣ Pipeline + Parallel 的混合**
- Stage 1-2-3-4 整體是流水線（串行）
- 但 Stage 2 內部是並行（兩個 Agent）
- 也是 Stage 4 內部是並行（郵件 + 日誌）

**2️⃣ 對抗驗證機制**
- 兩個 Agent 給出矛盾結論時，自動升級
- 升級消息包含完整的決策依據

**3️⃣ Human-in-the-Loop**
- 系統不強行決策，而是提供建議 + 標記異常
- HR 主管最終做決定

**4️⃣ 監控透明度**
- 每個 Stage 都可以被觀測
- 性能指標：耗時、Token、成本

#### 理解練習

- [ ] 畫出新世界 HR 的完整流程圖
- [ ] 說出其中的 4 個 Stage 各自的職責
- [ ] 解釋為什麼 Stage 2 內部是並行而不是串行
- [ ] 說明衝突解決機制是如何工作的

---

### 任務 4.2：設計一個企業級 Workflow 藍圖
**時間**：2 小時
**難度**：⭐⭐⭐ 有挑戰

你現在需要根據一個業務需求，設計出完整的 Workflow 藍圖。

#### 設計框架

**Step 1：業務需求分析**
```
業務場景：_____________________
核心問題：_____________________
關鍵約束：_____________________
成功標準：_____________________
```

**Step 2：確定執行模式**

選擇合適的執行模式組合：
- [ ] Pipeline（流水線）
- [ ] Synchronous Aggregation（並行聚合）
- [ ] Adversarial Validation（對抗驗證）
- [ ] Best-of Mode（末尾篩選）
- [ ] Cumulative（累積式）
- [ ] Nested（嵌套式）

**Step 3：設計 Stage 結構**

為每個 Stage 定義：
```
Stage N: 名稱
├─ 輸入：來自哪裡
├─ 處理：由哪個 Agent
├─ 輸出：什麼結構
└─ 錯誤處理：怎麼辦
```

**Step 4：設計衝突解決與異常處理**

- 可能出現哪些衝突？
- 如何解決？（升級、多數表決、降級...）
- 如何處理異常？（重試、降級、人工...）

**Step 5：撰寫設計文檔**

完成一份設計文檔，包括：
- 業務背景和目標
- 完整的流程圖（文字或 ASCII）
- 各 Stage 的詳細說明
- 衝突和異常處理方案
- 預期的監控指標

#### 設計示例：採購流程審批 Workflow

**業務需求**：
- 員工提交採購申請
- 自動檢查預算、供應商、商品質量
- 必要時升級給主管批准
- 審批通過後通知採購部門

**流程設計**：
```
Stage 1: Request Analysis     (提取申請信息)
         │
         ▼
Stage 2: Parallel Validation  (並行檢查)
         ├─ BudgetAgent
         ├─ VendorAgent
         └─ QualityAgent
         │
         ▼
Stage 3: Conflict Resolution  (衝突檢測)
         (如果有衝突 → 升級)
         │
         ▼
Stage 4: Approval Decision    (批准決策)
         │
         ▼
Stage 5: Notification         (並行通知)
         ├─ SendToApprover
         └─ SendToProcurement
```

#### 完成清單

- [ ] 選擇一個真實的業務場景（可參考：招聘、內容審核、客服工單、產品發布...）
- [ ] 完成業務需求分析
- [ ] 設計完整的 Stage 結構
- [ ] 確定使用的執行模式
- [ ] 撰寫完整的設計文檔

---

### 任務 4.3：實現企業級 Workflow
**時間**：3-4 小時
**難度**：⭐⭐⭐⭐ 最難

根據你在任務 4.2 中的設計，現在實現完整的 Workflow 代碼。

#### 實現檢查清單

代碼實現應包含：

- [ ] **完整的元數據** — name, version, description, author
- [ ] **所有 Stage 的執行邏輯** — 正確的順序、並行、聚合
- [ ] **衝突檢測和解決** — 檢測衝突，升級或決策
- [ ] **異常處理** — 重試、降級、人工升級
- [ ] **清晰的返回結果** — success, output, metrics, error
- [ ] **可觀測性** — 每個 Stage 都有日誌點

#### 代碼質量標準

```javascript
✅ 好的代碼特徵：
- 變數名清晰，易於理解
- Stage 邏輯清晰，易於測試
- 錯誤信息有幫助，便於調試
- 返回值結構一致，易於消費
- 有適當的註釋説明複雜邏輯

❌ 需要避免的：
- Stage 邏輯混亂，難以理解
- 缺乏錯誤處理
- 返回值結構不一致
- 沒有衝突解決機制
- 無法追蹤執行過程
```

#### 實現示例框架

```javascript
const metadata = {
  name: "YourWorkflowName",
  description: "...",
  version: "1.0.0",
  stages: 4,
  executionModes: ["Pipeline", "ParallelValidation", "ConflictDetection"]
};

async function execute(context) {
  try {
    // === Stage 1: 數據提取 ===
    const data = await agent.run("DataExtractorAgent", context.input);

    // === Stage 2: 並行驗證 ===
    const [check1, check2] = await Promise.all([
      agent.run("Validator1Agent", data),
      agent.run("Validator2Agent", data)
    ]);

    // === Stage 3: 衝突檢測 ===
    if (check1.decision !== check2.decision) {
      return {
        status: "ESCALATED",
        escalatedTo: "manager",
        details: { check1, check2 }
      };
    }

    // === Stage 4: 最終決策 ===
    const decision = await agent.run("DecisionAgent", {
      check1,
      check2
    });

    return {
      success: true,
      output: decision,
      metrics: {
        timestamp: new Date().toISOString(),
        tokensUsed: 1245
      }
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

module.exports = { metadata, execute };
```

---

### 任務 4.4：部署 + 監控
**時間**：1.5 小時
**難度**：⭐⭐ 中等

#### 部署步驟

1. **測試執行**
   ```bash
   claude ultraWork < test_input.json
   ```

2. **檢查輸出**
   - 返回值結構是否正確？
   - 所有 Stage 都執行了嗎？
   - 衝突檢測是否工作？

3. **使用 `/workflows` 監控**
   ```bash
   /workflows
   ```

   查看：
   - 每個 Stage 的耗時
   - Token 消耗總數
   - 成本估算
   - 執行狀態（SUCCESS/FAILED/ESCALATED）

#### 監控指標解讀

```json
{
  "workflow_id": "wf_xxx",
  "status": "COMPLETED",
  "metrics": {
    "total_duration_ms": 3450,      // 總耗時 3.45 秒
    "total_tokens_consumed": 2100,   // 總 Token 消耗
    "estimated_cost_usd": 0.0063,    // 估算成本
    "stages": [
      {
        "name": "DataExtraction",
        "duration_ms": 420,
        "tokens": 350,
        "status": "SUCCESS"
      },
      // ... 其他 Stage
    ]
  }
}
```

#### 優化建議

根據監控數據，尋找優化機會：

- **耗時分析**：哪個 Stage 最慢？能否並行？
- **Token 分析**：哪個 Agent 最耗 Token？能否簡化提示？
- **成本分析**：總成本是否可接受？
- **成功率**：是否有反覆失敗的 Stage？

---

### 任務 4.5：撰寫文檔 + 維護指南
**時間**：1 小時
**難度**：⭐⭐ 中等

完整的 Workflow 應包含清晰的文檔。

#### 文檔結構

**1️⃣ README.md — 快速開始**
```markdown
# 採購審批 Workflow

## 功能
簡短說明這個 Workflow 做什麼

## 快速使用
```bash
claude ultraWork < input.json
```

## 主要 Agent
- BudgetValidator
- VendorChecker
- QualityInspector

## 成功案例
- 平均耗時：2.5 秒
- 成本：$0.003 / 次
- 成功率：99.2%
```

**2️⃣ ARCHITECTURE.md — 詳細設計**
```markdown
# 架構設計文檔

## 流程概述
[完整的流程圖 + 文字說明]

## Stage 詳解
- Stage 1: ... (職責、輸入、輸出)
- Stage 2: ... (並行邏輯)
- ...

## 衝突解決
遇到衝突時的處理方式

## 異常處理
重試、降級、升級策略
```

**3️⃣ MAINTENANCE.md — 維護指南**
```markdown
# 維護指南

## 常見問題
Q: Workflow 經常超時？
A: ...

## 版本更新日誌
v1.0.0 (2026-05-26) - 初版發佈
v1.0.1 (2026-06-02) - 修復 Stage 2 超時問題

## 性能優化建議
根據監控數據...
```

#### 完成清單

- [ ] 撰寫 README，能讓新人快速理解用法
- [ ] 撰寫 ARCHITECTURE，詳細説明設計邏輯
- [ ] 撰寫 MAINTENANCE，包含常見問題和優化建議
- [ ] 文檔內容準確、易讀，無語法錯誤

---

## 🏆 實踐項目 4 & 5

### 項目 4️⃣：新世界 HR 系統複製版本

**要求**：
- 複現新世界 HR 系統的 4 個 Stage
- 實現對抗驗證機制（公司政策 vs 法律合規）
- 實現人工升級邏輯
- 完整的監控數據

**驗收標準**：
- [ ] 系統完整，包含所有 4 個 Stage
- [ ] 衝突時正確升級
- [ ] `/workflows` 輸出完整準確
- [ ] 代碼清晰，文檔齊全

### 項目 5️⃣：自選企業案例

**選項**：
- 招聘流程（發佈 → 篩選 → 面試 → 錄取）
- 內容審核（提交 → 編輯 → 法務 → 發佈）
- 客服工單（接收 → 分類 → 分配 → 跟蹤）
- 產品發布（需求 → 開發 → 測試 → 發布）
- 采購流程（申請 → 驗證 → 批准 → 通知）

**驗收標準**：
- [ ] 至少包含 2 種執行模式
- [ ] 設計合理的衝突解決機制
- [ ] 完整的異常處理（重試、降級、升級）
- [ ] 完整的文檔（設計、維護、API）

---

## ✅ 第 4 階段檢查點

- [ ] **案例分析**：深入理解新世界 HR 系統的設計
- [ ] **獨立設計**：能為真實業務場景設計完整 Workflow
- [ ] **代碼實現**：實現企業級的代碼質量
- [ ] **監控優化**：能解讀 `/workflows` 數據，進行優化
- [ ] **文檔完整**：撰寫專業的設計和維護文檔
- [ ] **項目完成**：實踐項目 4-5 成功部署

---

## 📚 參考資源

- 新世界 HR 系統代碼庫
- Agent E04 Part 2：實踐篇詳解
- Claude Code 官方文檔

---

## 🎓 完成第 4 階段？

當你完成第 4 階段，你已成為 **Workflow 應用工程師**。

可選的 **[第 5 階段：認證與深化](./5_認證與深化.md)** 會帶你成為企業架構師級別。

---

**階段狀態**：⏳ 待開始
**完成度**：0%
**預計完成日期**：2026-06-06
