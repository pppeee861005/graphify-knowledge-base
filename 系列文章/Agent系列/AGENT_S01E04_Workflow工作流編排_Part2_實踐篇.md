# Workflow：從 Prompt 到代碼，蜂群的編程語言（Part 2 - 實踐篇）

**《蜂群 Agent》系列｜第 4 篇（下）**
*新人類聯盟 · Homo Coalitio*

---

## 第 3 幕：實戰案例：新世界 HR 審批工作流

為了讓大家看到 Workflow 在真實業務中的威力，我們拿聯盟正在推進的**「計劃 1：新世界 HR 系統」**來做一個深度剖析。

在傳統的軟體開發中，我們使用 Google Workspace (Google Forms + Apps Script + Google Sheets) 來搭建一個請假審批系統。

### 舊做法：硬編碼的 Google Apps Script

在傳統的 Apps Script 中，我們需要寫一個龐大的 `Code.gs` 文件。每當員工提交表單時，這個腳本就會被觸發：

```javascript
// 傳統 Apps Script 的偽代碼
function onFormSubmit(e) {
  var formData = extractData(e);

  // 硬編碼的政策檢查
  if (formData.days > 3 && formData.type === "特休") {
    if (getLeaveBalance(formData.employeeId) < formData.days) {
      rejectRequest(formData, "假期餘額不足");
      return;
    }
  }

  // 硬編碼的勞動法規檢查
  if (formData.days > 30) {
    sendToHRDirector(formData);
    return;
  }

  // 寫入 Google Sheet
  logToSheet(formData);
  // 發送 Email
  sendEmailNotification(formData);
}
```

**這個架構有三個致命缺陷：**

1. **邏輯高度耦合（Monolithic）**：政策檢查、法規校驗、郵件發送、數據庫寫入全都混在一個文件裡。一旦公司修改了「特休天數限制」的政策，工程師就必須去修改這段代碼，極易引入 Bug。
2. **缺乏智慧決策**：如果員工請假理由寫的是「因家裡突發緊急狀況，需要回南部老家處理，預計請假 3 天，但目前特休只剩 2 天，希望能用事假抵扣」，傳統的硬編碼規則會直接彈回（Reject），而無法進行智慧型的彈性判斷。
3. **無法並行校驗**：政策校驗和法規校驗必須串行執行，無法同時進行，這在處理大批量審批時會成為性能瓶頸。

### 新做法：基於 Workflow 的蜂群編排

在新人類聯盟的設計中，我們使用 Claude Code Workflow 將其重構為一個 **Human-in-the-Loop（人在回路）** 的 Swarm 工作流。

#### 執行流程視覺化

```
            【員工提交請假表單】
                    │
                    ▼
      ┌───────────────────────────┐
      │  Stage 1: DataCollection  │  ──▶ 提取申請人、天數、理由等結構化數據
      └───────────────────────────┘
                    │
                    ▼
      ┌───────────────────────────┐
      │  Stage 2: PolicyCheck     │
      │  (並行執行，進行對抗驗證)  │
      │  ├── CompanyPolicyAgent   │  ──▶ 檢查公司內部休假條例
      │  └── LegalComplianceAgent │  ──▶ 檢查勞動基準法合規性
      └───────────────────────────┘
                    │
            ┌───────┴───────┐
         一致 (無衝突)     發生衝突
            │               │
            ▼               ▼
      ┌───────────┐   ┌───────────────────────────┐
      │ 繼續流程  │   │  EscalateToHuman (人介入)  │ ──▶ 標記異常，交由 HR 主管裁決
      └─────┬─────┘   └─────────────┬─────────────┘
            │                       │
            └───────┬───────────────┘
                    │
                    ▼
      ┌───────────────────────────┐
      │  Stage 3: Recommendation  │  ──▶ 綜合假期餘額與部門日曆，生成審批建議
      └───────────────────────────┘
                    │
                    ▼
      ┌───────────────────────────┐
      │   Stage 4: Notification   │
      │  (並行執行，通知與歸檔)    │
      │  ├── SendEmailToManager   │  ──▶ 發送含有 AI 建議的審批郵件給主管
      │  └── LogToGoogleSheet     │  ──▶ 將審批狀態同步至總控表
      └───────────────────────────┘
```

#### Workflow JS 腳本實現

以下是這個 HR 審批工作流的真實 JavaScript 配置文件：

```javascript
const hrWorkflow = {
  metadata: {
    name: "NewWorld_HR_LeaveApproval",
    description: "基於蜂群架構的員工請假智慧審批流",
    version: "2.0.0"
  },

  stages: [
    // Stage 1: 資料整理
    {
      name: "DataCollection",
      agent: "FormParserAgent",
      input: (context) => context.rawFormData,
      output: (result) => ({
        employeeId: result.id,
        leaveType: result.type,
        duration: result.days,
        reason: result.reason
      })
    },

    // Stage 2: 合規校驗（對抗驗證模式）
    {
      name: "PolicyValidation",
      mode: "parallel",
      agents: {
        companyCheck: "CompanyPolicyAgent",
        legalCheck: "LegalComplianceAgent"
      },
      input: (context) => context.stages.DataCollection.output,
      // 衝突處理機制：如果公司政策 Agent 與法律合規 Agent 給出了矛盾的結論，觸發人工升級
      conflictHandling: (results) => {
        if (results.companyCheck.approved !== results.legalCheck.approved) {
          return {
            status: "ESCALATED",
            reason: `政策校驗衝突：公司政策回傳 [${results.companyCheck.reason}]，而法律合規回傳 [${results.legalCheck.reason}]。`
          };
        }
        return {
          status: "SUCCESS",
          approved: results.companyCheck.approved,
          reason: results.companyCheck.reason
        };
      }
    },

    // Stage 3: 審批建議生成（累積模式）
    {
      name: "ApprovalReasoning",
      agent: "HRReasonerAgent",
      input: (context) => ({
        request: context.stages.DataCollection.output,
        validation: context.stages.PolicyValidation.output,
        leaveBalance: context.employeeLeaveBalance, // 外部系統傳入的剩餘假期數據
        teamCalendar: context.departmentCalendar     // 同部門其他人的請假狀況
      })
    },

    // Stage 4: 通知與記錄（並行執行）
    {
      name: "Notification",
      mode: "parallel",
      agents: {
        email: "EmailNotificationAgent",
        sheet: "GoogleSheetLoggerAgent"
      },
      input: (context) => ({
        recommendation: context.stages.ApprovalReasoning.output,
        recipient: context.managerEmail
      })
    }
  ]
};
```

### 控制台監控：`/workflows` 的真實輸出

當這個 Workflow 在 Claude Code 中執行時，我們在終端機輸入 `/workflows`，可以看到以下精準的觀測數據：

```json
{
  "workflow_id": "wf_leave_998231",
  "status": "COMPLETED",
  "metrics": {
    "total_duration_ms": 2340,
    "total_tokens_consumed": 1245,
    "estimated_cost_usd": 0.0037
  },
  "stages": [
    {
      "name": "DataCollection",
      "duration_ms": 420,
      "status": "SUCCESS",
      "model_used": "claude-3-5-haiku-20241022"
    },
    {
      "name": "PolicyValidation",
      "duration_ms": 850,
      "status": "SUCCESS",
      "details": {
        "companyCheck": { "approved": true, "reason": "符合特休請假規定" },
        "legalCheck": { "approved": true, "reason": "符合勞基法第 38 條規定" }
      },
      "model_used": "claude-3-5-sonnet-20241022"
    },
    {
      "name": "ApprovalReasoning",
      "duration_ms": 680,
      "status": "SUCCESS",
      "output": {
        "recommendation": "建議批准。該員工特休餘額為 5 天，本次請假 3 天後餘額為 2 天。同部門在該時段無其他人請假，不會影響部門正常運作。"
      },
      "model_used": "claude-3-5-sonnet-20241022"
    },
    {
      "name": "Notification",
      "duration_ms": 390,
      "status": "SUCCESS",
      "model_used": "claude-3-5-haiku-20241022"
    }
  ]
}
```

### 深度對比：傳統 Apps Script vs Workflow Swarm

| 維度 | 傳統 Apps Script | Workflow Swarm (蜂群) |
| :--- | :--- | :--- |
| **定義方式** | 將所有邏輯硬編碼在一個單一的代碼文件中。 | 使用 JavaScript 腳本，以**聲明式**定義 Stage 結構。 |
| **邏輯可調整性** | 極低。修改規則需要重新編寫並測試整個 `Code.gs`。 | 極高。只需修改對應 Stage 的 Agent 設定或 Prompts。 |
| **可觀測性** | 只能通過零散的 `console.log()` 在控制台查看日誌。 | 原生支持 `/workflows`，可精確監控每一步的耗時與 Token。 |
| **Agent 協作** | 無法原生支持。必須手動寫 HTTP 請求去對接外部模型。 | 原生支持多 Agent 並行、串行、對抗驗證等多種協作模式。 |
| **複用性** | 每個專案的 Apps Script 都是孤島，極難跨專案複用。 | 腳本可作為**資產**保存、分享，並快速應用於新流程。 |
| **異常處理** | 發生錯誤時，整個腳本崩潰，員工申請丟失。 | 支持 Stage 級別的重試、回退（Fallback）與人工介入。 |

這就是為什麼我們說 **Workflow 讓 AI 應用從「玩具」真正走向了「生產環境」**。它不僅僅是提高了開發效率，更重要的是，它建立了一套**可預測的工程規範**。

---

## 第 4 幕：Workflow 的六種核心模式

在實踐中，不同的業務場景需要不同的 Agent 協作模式。Anthropic 的 Workflow 設計非常精妙，它原生支持了以下六種執行模式，開發者可以根據需要自由組合：

### 1. 流水線模式 (Pipeline)
* **核心概念**：線性順序執行。`A ──▶ B ──▶ C`。後一個 Stage 必須等待前一個 Stage 的輸出作為輸入。
* **HR 應用場景**：**新員工入職流程**。資料審查 ──▶ 帳號創建 ──▶ 發放設備。前一步未完成，後一步絕不觸發。

**動態視覺化：**

```svg
<svg viewBox="0 0 1200 400" xmlns="http://www.w3.org/2000/svg" style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 8px;">
  <defs>
    <style>
      @keyframes slideRight {
        0% { offset-distance: 0%; }
        100% { offset-distance: 100%; }
      }
      @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
      }
      @keyframes flowDot {
        0% { offset-distance: 0%; opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { offset-distance: 100%; opacity: 0; }
      }

      .stage-box { fill: white; stroke: #2c3e50; stroke-width: 3; }
      .stage-box.active { fill: #3498db; stroke: #2980b9; }
      .stage-box.completed { fill: #2ecc71; stroke: #27ae60; }
      .stage-title { font-size: 18px; font-weight: bold; fill: #2c3e50; text-anchor: middle; }
      .stage-title.active { fill: white; }
      .stage-title.completed { fill: white; }
      .stage-subtitle { font-size: 13px; fill: #7f8c8d; text-anchor: middle; }
      .stage-subtitle.active { fill: white; }
      .stage-subtitle.completed { fill: white; }
      .arrow-line { stroke: #34495e; stroke-width: 3; fill: none; }
      .flow-dot { fill: #e74c3c; }
      .pipeline-flow { stroke: #3498db; stroke-width: 2; fill: none; stroke-dasharray: 5,5; }
      .label { font-size: 12px; fill: #7f8c8d; text-anchor: middle; }
      .timeline { font-size: 14px; font-weight: bold; fill: #2c3e50; }
    </style>

    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#34495e"/>
    </marker>
    <marker id="arrowhead-flow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#e74c3c"/>
    </marker>
  </defs>

  <!-- 背景標題 -->
  <text x="600" y="35" font-size="20" font-weight="bold" text-anchor="middle" fill="#2c3e50">
    Pipeline（流水線）：新員工入職流程
  </text>
  <text x="600" y="60" font-size="13" text-anchor="middle" fill="#7f8c8d">
    Stage 順序執行，前一步完成才能觸發下一步 | 無並行處理
  </text>

  <!-- 舞台容器分組 -->
  <g id="stage1-group">
    <!-- Stage 1: 資料審查 -->
    <rect x="80" y="120" width="200" height="120" rx="10" class="stage-box"/>
    <text x="180" y="170" class="stage-title">資料審查</text>
    <text x="180" y="190" class="stage-subtitle">Verify Candidate</text>
    <circle cx="180" cy="145" r="8" fill="#3498db" opacity="0"/>

    <!-- 脈動效果指示燈（Stage 1 啟動時） -->
    <circle cx="180" cy="145" r="12" fill="none" stroke="#e74c3c" stroke-width="2" opacity="0">
      <animate attributeName="r" values="12;20" dur="1s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="1;0" dur="1s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- 箭頭 1 → 2 -->
  <g id="arrow-1-2">
    <line x1="280" y1="180" x2="360" y2="180" class="arrow-line" marker-end="url(#arrowhead)"/>

    <!-- 流動點動畫 -->
    <circle r="6" class="flow-dot" opacity="0">
      <animateMotion dur="2s" repeatCount="indefinite" keyPoints="0;1" keyTimes="0;1">
        <mpath href="#path-1-2"/>
      </animateMotion>
      <animate attributeName="opacity" values="0;1;1;0" dur="2s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- 隱形路徑用於流動點 -->
  <path id="path-1-2" d="M 280 180 L 360 180" fill="none"/>

  <g id="stage2-group">
    <!-- Stage 2: 帳號創建 -->
    <rect x="360" y="120" width="200" height="120" rx="10" class="stage-box"/>
    <text x="460" y="170" class="stage-title">帳號創建</text>
    <text x="460" y="190" class="stage-subtitle">Create Account</text>

    <!-- 脈動效果指示燈（延遲啟動） -->
    <circle cx="460" cy="145" r="12" fill="none" stroke="#e74c3c" stroke-width="2" opacity="0">
      <animate attributeName="r" values="12;20" dur="1s" begin="2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="1;0" dur="1s" begin="2s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- 箭頭 2 → 3 -->
  <g id="arrow-2-3">
    <line x1="560" y1="180" x2="640" y2="180" class="arrow-line" marker-end="url(#arrowhead)"/>

    <!-- 流動點動畫（延遲開始） -->
    <circle r="6" class="flow-dot" opacity="0">
      <animateMotion dur="2s" begin="2s" repeatCount="indefinite" keyPoints="0;1" keyTimes="0;1">
        <mpath href="#path-2-3"/>
      </animateMotion>
      <animate attributeName="opacity" values="0;1;1;0" dur="2s" begin="2s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- 隱形路徑用於流動點 -->
  <path id="path-2-3" d="M 560 180 L 640 180" fill="none"/>

  <g id="stage3-group">
    <!-- Stage 3: 發放設備 -->
    <rect x="640" y="120" width="200" height="120" rx="10" class="stage-box"/>
    <text x="740" y="170" class="stage-title">發放設備</text>
    <text x="740" y="190" class="stage-subtitle">Allocate Equipment</text>

    <!-- 脈動效果指示燈（延遲啟動） -->
    <circle cx="740" cy="145" r="12" fill="none" stroke="#e74c3c" stroke-width="2" opacity="0">
      <animate attributeName="r" values="12;20" dur="1s" begin="4s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="1;0" dur="1s" begin="4s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- 底部時間軸與說明 -->
  <g id="timeline">
    <!-- 時間點 1 -->
    <circle cx="180" cy="280" r="6" fill="#e74c3c"/>
    <line x1="180" y1="286" x2="180" y2="310" stroke="#bdc3c7" stroke-width="2"/>
    <text x="180" y="330" class="timeline">T=0s</text>
    <text x="180" y="350" font-size="12" text-anchor="middle" fill="#7f8c8d">啟動審查</text>

    <!-- 時間點 2 -->
    <circle cx="460" cy="280" r="6" fill="#f39c12"/>
    <line x1="460" y1="286" x2="460" y2="310" stroke="#bdc3c7" stroke-width="2"/>
    <text x="460" y="330" class="timeline">T=2s</text>
    <text x="460" y="350" font-size="12" text-anchor="middle" fill="#7f8c8d">創建帳號</text>

    <!-- 時間點 3 -->
    <circle cx="740" cy="280" r="6" fill="#27ae60"/>
    <line x1="740" y1="286" x2="740" y2="310" stroke="#bdc3c7" stroke-width="2"/>
    <text x="740" y="330" class="timeline">T=4s</text>
    <text x="740" y="350" font-size="12" text-anchor="middle" fill="#7f8c8d">分配設備</text>
  </g>

  <!-- 核心說明文字（右側） -->
  <g id="explanation">
    <rect x="920" y="120" width="260" height="200" rx="8" fill="#ecf0f1" stroke="#95a5a6" stroke-width="2"/>
    <text x="940" y="145" font-size="14" font-weight="bold" fill="#2c3e50">Pipeline 特徵：</text>

    <text x="950" y="170" font-size="12" fill="#34495e">✓ 線性順序執行</text>
    <text x="950" y="190" font-size="12" fill="#34495e">✓ 無並行處理</text>
    <text x="950" y="210" font-size="12" fill="#34495e">✓ 前序依賴</text>
    <text x="950" y="230" font-size="12" fill="#34495e">✓ 簡單透明</text>
    <text x="950" y="250" font-size="12" fill="#e74c3c">⚠ 無法並行優化</text>
    <text x="950" y="270" font-size="12" fill="#e74c3c">⚠ 總耗時 = 三步</text>
    <text x="950" y="290" font-size="11" fill="#7f8c8d">之和</text>
    <text x="950" y="310" font-size="11" fill="#7f8c8d">適用於：強制依賴</text>
  </g>
</svg>
```

### 2. 同步聚合模式 (Synchronous Aggregation)
* **核心概念**：多個 Agent 同時並行執行，最後將所有結果匯總到一個聚合 Agent 中進行統一處理。
* **HR 應用場景**：**員工年終績效評估**。同時啟動「員工自我評價 Agent」、「同事互評 Agent」以及「主管評價 Agent」，三者並行工作，最後由「績效報告生成 Agent」融合成一份最終的績效卡片。

### 3. 對抗驗證模式 (Adversarial Validation)
* **核心概念**：兩個或多個 Agent 針對同一個任務給出結論，並互相審查對方的結論。若發現衝突，自動觸發人工介入或協商機制。
* **HR 應用場景**：**高階主管晉升名單合規檢查**。`內部政策 Agent` 檢查其是否符合內部晉升年限規定，`法律合規 Agent` 檢查其是否符合勞動法相關比例規定。兩者結論若有衝突，自動將案件掛起（Hold），並發送通知給 HRVP。

### 4. 末尾篩選制 (Best-of Mode)
* **核心概念**：同一個任務，由多個不同配置的 Agent（或同一個 Agent 使用不同的 Temperature）生成多個版本的解決方案，最後由一個裁判 Agent 篩選出最優的版本。
* **HR 應用場景**：**招募職缺描述（JD）撰寫**。生成三個不同風格（熱情吸睛型、嚴謹專業型、簡潔條理型）的 JD 草稿，最後由裁判 Agent 選出最符合該職位畫像的版本作為最終發布稿。

### 5. 累積式模式 (Cumulative Pattern)
* **核心概念**：隨著流程的推進，信息不斷被加入到同一個 Session 的事件日誌中，後面的 Agent 擁有前面所有步驟累積的完整上下文。
* **HR 應用場景**：**離職面談與交接追蹤**。從「提交離職申請」開始，陸續累積「部門主管面談記錄」、「HR 離職面談記錄」、「資產交接清單狀態」，最終生成一份無縫累積的「離職結案報告」。

### 6. 嵌套式工作流 (Nested Workflow)
* **核心概念**：一個大 Workflow 的某個 Stage，其內部是一個完整的小 Workflow。
* **HR 應用場景**：**「跨國差旅審批 Workflow」**。在其「費用報銷」這個 Stage 內部，會自動調用「外幣匯率換算與稅務申報 Workflow」。

---

## 尾聲：為什麼 Workflow 代表著 Software 3.0 的到來

在我們回顧整個系列時，你會發現一條非常清晰的演進脈絡：

* **S01E01** 中，我們定義了**「蜂群」**是多 Agent 協作的新架構；
* **S01E02** 中，我們論證了為什麼蜂群具有**「可適應性」**，能夠在模型迭代中永不被淘汰；
* **S01E03** 中，我們剖析了 Anthropic 的**「解耦哲學」**，看清了大腦、框架與執行的三層分離；
* 而今天，在 **S01E04** 中，我們終於拿到了開啟這個新世界的鑰匙——**Workflow**。

Workflow 的出現，標誌著我們正式從 **"Software 2.0"**（以神經網絡模型替代手寫算法）跨入了 **"Software 3.0"** 的大門。

在 Software 3.0 的世界裡，我們的編程對象不再是像素、API 或者是具體的算法規則，而是**「智慧本身的組織結構」**。

```
【Software 1.0】 寫代碼規定每一行邏輯：   Input ──(手寫代碼)──▶ Output
【Software 2.0】 用數據訓練神經網絡：   Input ──(機器學習)──▶ Output
【Software 3.0】 編排多個 Agent 的協作： Input ──(工作流編排)──▶ Output
```

如果你是一位**開發者**，現在是時候放下「如何寫出最完美的 Prompt」這種玄學了。你應該開始學習如何像編排分佈式系統一樣，用 JavaScript/TypeScript 去編排你的 Agent Workflow。這才是未來的核心競爭力。

如果你是一位**企業決策者**，你必須意識到，未來企業最核心的資產，不是你買了多少 SaaS 軟體，也不是你租用了多強大的算力，而是**你企業內部沉澱下來的、經過市場驗證的「AI Workflow 流程庫」**。那是你企業的「數字大腦運行圖」。

Prompt 工程讓 AI 聽懂人話，但它依然把 AI 當作一個隨性的個體助手；

Workflow 工程讓 AI 按照結構做事，這才把 AI 真正變成了工業級的生產力。

新人類聯盟的選擇依然堅定：我們不相信單一 AI 能解決所有問題，我們相信組織的力量。而 Workflow，就是我們用代碼在數字世界中，為蜂群建立的完美秩序。

---

## 🔑 全篇金句摘錄

1. **「Prompt 是對個體智慧的壓榨，而 Workflow 是對組織結構的編排。」**
2. **「當 AI 應用不再是神祕莫測的魔法，而是一個可觀測、可調優的系統時，它才真正具備了工業價值。」**
3. **「在 Software 3.0 時代，代碼會老化，但你為蜂群設計的協作關係與決策流，將成為企業的永恆資產。」**
4. **「Prompt 工程讓 AI 聽懂人話，Workflow 工程讓 AI 按照結構做事。這是 AI 應用走向成熟的唯一路徑。」**

---

## 📎 全系列參考資源

* **Workflow 原始筆記**：[work_log_20260525_workflow_memo.md](file:///D:/數位資產/graphify個人知識庫/計劃1_新世界HR系統/memory/work_log_20260525_workflow_memo.md)
* **新世界 HR 系統 MVP 代碼庫**：[gws-hr-automation](https://github.com/pppeee861005/gws-hr-automation)
* **Agent 系列全部篇章**：
  * E01：[蜂群 Agent 是什麼](file:///D:/數位資產/graphify個人知識庫/系列文章/Agent系列/AGENT_S01E01_蜂群Agent是什麼_published.md)
  * E02：[可適應性蜂群永不被淘汰](file:///D:/數位資產/graphify個人知識庫/系列文章/Agent系列/AGENT_S01E02_可適應性蜂群永不被淘汰_published.md)
  * E03：[解耦哲學：Anthropic 設計蜂群的靈魂](file:///D:/數位資產/graphify個人知識庫/系列文章/Agent系列/AGENT_S01E03_解耦哲學Anthropic設計蜂群_published.md)
  * E04 Part 1：[理論篇](file:///D:/數位資產/graphify個人知識庫/系列文章/Agent系列/AGENT_S01E04_Workflow工作流編排_Part1_理論篇.md)
  * E04 Part 2：[實踐篇](file:///D:/數位資產/graphify個人知識庫/系列文章/Agent系列/AGENT_S01E04_Workflow工作流編排_Part2_實踐篇.md)

---

**Agent 系列完整，共 4 篇 + 3 篇 Human in the Loop 系列正在準備。**

*新人類聯盟 · Homo Coalitio*
*《AI 指揮官筆記》Substack · 2026.05*
*aiagentcommander.substack.com*
