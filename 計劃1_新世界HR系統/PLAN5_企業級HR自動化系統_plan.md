---
name: plan5-enterprise-hr-automation
description: 計劃 5 - 企業級 HR 自動化系統規劃
metadata:
  type: strategic_plan
  date: 2026-05-25
  status: planning
  framework: Antigravity 2.0
---

# 計劃 5：企業級 AI HR 自動化系統

**計劃代碼**：Plan-5-EnterpriseHR-Workflow
**版本**：v2.0（Workflow-First Architecture）
**基礎**：計劃 1 v1.0（Google Workspace + Apps Script）
**啟動日期**：2026-06-01（預計）
**框架**：Antigravity 2.0 + Claude Code Workflow

---

## 🎯 計劃 5 的戰略地位

**計劃 5 是什麼？**

計劃 1 v1.0 的升級項目，從「MVP 驗證」升級為「企業級生產系統」。

- **計劃 1 v1.0**：證明「Human in the Loop」的可行性（已完成）
- **計劃 5**：把「人在回路」做成可複用、可擴展的企業級系統（開發中）

### v1.0 vs 計劃 5

```
Google Forms
    ↓
Apps Script（850+ 行）
    ├─ 資料整理
    ├─ 政策檢查
    ├─ 建議生成
    └─ 通知發送
    ↓
Google Sheets / Docs / Calendar / Gmail
```

**特點**：
- ✅ 低成本、快速上線
- ✅ 員工零學習曲線
- ✅ Human in the Loop 設計
- ❌ 邏輯硬編碼在 Apps Script
- ❌ 難以並行執行複雜檢查
- ❌ 不可見、難以調試和優化

### v2.0：Workflow-First 架構

```
Google Forms
    ↓
Claude Code Workflow（結構化 JS）
    ├─ Stage 1: 資料收集（並行）
    │   ├─ ExtractFormData
    │   └─ ValidateData
    ├─ Stage 2: 政策驗證（對抗驗證）
    │   ├─ CheckCompanyPolicy
    │   └─ CheckLegalRequirement
    ├─ Stage 3: 推理（同步聚合）
    │   ├─ CalculateVacationDays
    │   └─ GenerateRecommendation
    └─ Stage 4: 執行（並行）
        ├─ NotifyManager
        ├─ UpdateSheet
        └─ SendEmail
    ↓
Google Workspace / Claude API / NotebookLM
```

**特點**：
- ✅ 結構清晰，邏輯可見
- ✅ 並行執行多個檢查
- ✅ 完全可監控（`/workflows`）
- ✅ 易於迭代和優化
- ✅ 可複用（其他 HR 流程可複用）
- ✅ 支持對抗驗證（發現衝突）

---

## 📊 架構對比表

| 維度 | v1.0 MVP | v2.0 Workflow |
|------|----------|---------------|
| **代碼組織** | 單一 Code.gs（線性） | 多 Stage（結構化） |
| **並行能力** | 有限 | 原生支持（6 種模式） |
| **執行模式** | 流水線 | 流水線 / 聚合 / 對抗驗證 / 嵌套... |
| **可觀測性** | 日誌查看 | `/workflows` 完整監控 |
| **Agent 協作** | 單一 Apps Script | 多 Agent 分工 |
| **複用性** | 低（每個流程重新寫） | 高（Workflow 腳本可複用） |
| **開發效率** | 快速上線 | 更易迭代優化 |
| **成本結構** | Google Workspace 固定成本 | Google + Claude API（按需） |
| **適配場景** | 小企業、試驗 | 中大企業、生產級 |

---

## 🏗️ v2.0 核心架構

### 三層結構升級

#### **第一層：表單層（不變）**

```
Google Forms（員工申請入口）
    ├─ 請假申請表
    ├─ 報銷申請表
    ├─ 培訓申請表
    └─ ...其他 HR 表單
```

#### **第二層：Workflow 編排層（新增）**

```javascript
// Leave Approval Workflow
const leaveApprovalWorkflow = {
  name: "LeaveApproval",

  // Stage 1: 資料收集（並行）
  stage1: {
    mode: "parallel",
    agents: [
      { agent: "FormDataExtractor", input: formResponse },
      { agent: "EmployeeValidator", input: employeeId }
    ]
  },

  // Stage 2: 政策檢查（對抗驗證）
  stage2: {
    mode: "adversarial_validation",
    agents: [
      { agent: "CompanyPolicyChecker", input: leaveType },
      { agent: "LegalRequirementValidator", input: country }
    ],
    conflictHandling: "escalate_to_hr_manager"
  },

  // Stage 3: 推理（同步聚合）
  stage3: {
    mode: "synchronous_aggregation",
    agents: [
      { agent: "VacationDayCalculator", input: employeeData },
      { agent: "RecommendationGenerator", input: policyData }
    ]
  },

  // Stage 4: 執行（並行）
  stage4: {
    mode: "parallel",
    agents: [
      { agent: "ManagerNotifier", input: recommendation },
      { agent: "SheetLogger", input: decision },
      { agent: "EmailSender", input: employee }
    ]
  }
}
```

#### **第三層：執行層（升級）**

```
Google Workspace 基礎設施
    ├─ Google Sheets（總控台 + 日誌）
    ├─ Google Drive（檔案管理）
    ├─ Google Calendar（期限提醒）
    ├─ Gmail（通知）
    └─ Apps Script（輕量化，僅用於 Form Trigger）

Claude API 增強層
    ├─ Claude Sonnet（複雜推理）
    ├─ Claude Haiku（輕量檢查）
    └─ Claude Opus（衝突決策）

NotebookLM 知識層
    ├─ 員工手冊 KB
    ├─ 公司政策 KB
    └─ 法規資料庫 KB
```

---

## 🔄 遷移計畫（v1.0 → v2.0）

### Phase 1：準備期（1 週）

**目標**：驗證 Workflow 功能，編寫首個完整腳本

**任務**：
- [ ] 本地激活 Workflow 功能（`export CLAUDE_CODE_WORKFLOWS_ENABLED=1`）
- [ ] 手寫「請假審批」的完整 Workflow 腳本
- [ ] 測試 `/workflows` 監控界面
- [ ] 驗證與 Google Workspace API 的整合

**交付物**：
- `PLAN1_v2_LeaveApproval_Workflow.js`（可執行腳本）
- `PLAN1_v2_測試報告.md`

### Phase 2：核心實現（2 週）

**目標**：實現「請假審批」完整工作流

**任務**：
- [ ] 連接 Google Forms Trigger → Workflow 腳本
- [ ] 實現 Stage 1：資料收集（含驗證）
- [ ] 實現 Stage 2：政策檢查（對抗驗證）
- [ ] 實現 Stage 3：推理和建議（調用 Claude API）
- [ ] 實現 Stage 4：執行（更新 Sheets、發送郵件）
- [ ] 集成 NotebookLM（政策查詢）

**交付物**：
- `newworld-hr-system/v2/leave_approval_workflow.js`
- `newworld-hr-system/v2/README_v2.md`
- 完整的部署指南

### Phase 3：擴展和優化（1-2 週）

**目標**：推廣到其他 HR 場景，建立 Workflow 範本庫

**任務**：
- [ ] 「報銷申請」Workflow
- [ ] 「培訓申請」Workflow
- [ ] 「部門變動」Workflow
- [ ] 建立 Workflow 範本庫（可複用）

**交付物**：
- `newworld-hr-system/v2/workflows/` 目錄
- `newworld-hr-system/v2/WORKFLOW_TEMPLATES.md`

### Phase 4：生產驗證（1 週）

**目標**：在真實 HR 環境測試

**任務**：
- [ ] 小規模試點（部分員工、部分流程）
- [ ] 收集反饋
- [ ] 性能監控
- [ ] 調整和優化

**交付物**：
- `PLAN1_v2_測試反饋報告.md`
- 優化後的 Workflow 腳本

### Phase 5：發布和文檔（1 週）

**目標**：正式發布 v2.0，更新 GitHub

**任務**：
- [ ] 更新 GitHub `gws-hr-automation` 倉庫
- [ ] 發布 v2.0 release notes
- [ ] 撰寫「遷移指南」（v1 → v2）
- [ ] 記錄 Workflow 最佳實踐

**交付物**：
- GitHub release v2.0
- `MIGRATION_GUIDE_v1_to_v2.md`
- `WORKFLOW_BEST_PRACTICES.md`

---

## 🎬 Workflow 腳本框架（可複用範本）

```javascript
/**
 * HR Workflow Template (可複用)
 *
 * 使用方式：
 * 1. 複製此框架
 * 2. 定義 Stages
 * 3. 指定每個 Stage 的 Agents
 * 4. 在 Claude Code 中用 `ultraWork` 觸發
 */

const hrWorkflowTemplate = {
  // 元數據
  metadata: {
    name: "[WorkflowName]",
    version: "1.0",
    description: "[Your Description]",
    owner: "HR Team",
    lastUpdated: "2026-05-25"
  },

  // 輸入驗證
  validateInput: async (input) => {
    // 檢查必要欄位
    if (!input.employeeId || !input.applicationType) {
      throw new Error("Missing required fields")
    }
  },

  // Stage 定義（可自訂數量）
  stages: [
    {
      name: "DataCollection",
      mode: "parallel",
      agents: [
        // 定義此 Stage 的 Agents
      ],
      timeout: 5000
    },
    // ... 更多 Stages
  ],

  // 錯誤處理
  errorHandling: {
    onStageFailure: "escalate_to_next_stage",
    onConflict: "escalate_to_human",
    maxRetries: 3
  },

  // 監控鉤點
  hooks: {
    onStart: async () => console.log("Workflow started"),
    onStageComplete: async (stageName) => console.log(`Stage ${stageName} completed`),
    onComplete: async (result) => console.log("Workflow completed", result)
  }
}
```

---

## 💡 v2.0 的核心優勢

### 1. **對企業的好處**

- ✅ **可見性**：每個決策步驟都可追蹤
- ✅ **可控性**：流程可按需調整，無需重寫代碼
- ✅ **合規性**：完整的審計日誌，符合企業要求
- ✅ **可複用**：一個 Workflow 可用於多個部門
- ✅ **成本優化**：按需調用 Claude API，而非固定成本

### 2. **對開發的好處**

- ✅ **結構清晰**：代碼邏輯一目了然
- ✅ **易於測試**：可單獨測試每個 Stage
- ✅ **易於擴展**：添加新 Stage 或 Agent 很簡單
- ✅ **可複用**：Workflow 腳本可分享給其他項目
- ✅ **可監控**：`/workflows` 看到所有性能數據

### 3. **對用戶的好處**

- ✅ **更快審批**：並行執行，大幅縮短時間
- ✅ **更透明**：收到詳細的「為什麼」而不只是「批准/拒絕」
- ✅ **更公平**：決策基於明確的政策，而非人工判斷
- ✅ **更智能**：多層驗證減少出錯

---

## 📢 與文章系列的連動

### 發布計劃

| 日期 | 內容 | 位置 |
|------|------|------|
| 05-25 | Agent 系列 E04 大綱（Workflow 介紹） | Substack |
| 05-27 | Human in the Loop 系列 E01（設計哲學） | Substack |
| 06-01 | Agent 系列 E04 正文（Workflow 實踐） | Substack |
| 06-03 | 「計劃 1 v2 升級公告」文章 | Substack |
| 06-10 | GitHub v2.0 release + 遷移指南 | GitHub |

### 資源整合

```
計劃 1 v2 實現
    ↓
Agent 系列 E04（理論說明）
Human in the Loop 系列（應用哲學）
    ↓
Substack 文章（對外傳播）
GitHub 倉庫（技術交付）
    ↓
讀者收穫：
- 理解 Workflow 是什麼
- 看到真實案例
- 能複製和使用
```

---

## 🚀 關鍵里程碑

| 日期 | 里程碑 | 狀態 |
|------|--------|------|
| 2026-05-25 | 規劃完成 | ✅ |
| 2026-05-27 | E04 大綱完成 | ✅ |
| 2026-06-01 | Phase 1 完成（Workflow 測試） | 待執行 |
| 2026-06-15 | Phase 2 完成（請假審批實現） | 待執行 |
| 2026-06-30 | Phase 3、4 完成（擴展+驗證） | 待執行 |
| 2026-07-01 | v2.0 正式發布 | 目標 |

---

## 🔗 相關檔案

- **v1.0 MVP**：`計劃1_新世界HR系統/newworld-hr-system/`
- **Workflow 筆記**：`計劃1_新世界HR系統/memory/work_log_20260525_workflow_memo.md`
- **E04 大綱**：`系列文章/Agent系列/AGENT_S01E04_Workflow工作流編排_plan.md`
- **Human in the Loop 系列**：`系列文章/HumanInTheLoop系列/`

---

## 💭 戰略意義

### v2.0 代表什麼？

**從「證明概念」到「生產系統」的升級**

```
v1.0: 「我們能用 Google Workspace 做半自動化 HR」
    ↓
v2.0: 「我們能用 Workflow 做企業級、可複用的 HR 自動化」
    ↓
未來: 「企業的 HR 流程庫 = 經過驗證的 Workflow 集合」
```

### 為什麼現在啟動 v2.0？

1. **時機成熟**：Claude Code 剛推出 Workflow 功能
2. **理論支撐**：Agent 系列即將發布 E04（Workflow 介紹）
3. **實際案例**：計劃 1 v1.0 已驗證可行，v2.0 是自然升級
4. **市場機會**：企業級 HR 自動化需求日益增長

---

**計劃 5 - 企業級 AI HR 自動化系統**
**建立日期**：2026-05-25
**狀態**：📋 準備啟動（Phase 1 計劃中）

🚀 **計劃 5 目標：從 MVP 到生產級企業系統**

