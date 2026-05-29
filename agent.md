# 🤖 Agent.md - Claude Code Agent 工作框架

**建立日期**：2026-05-20  
**版本**：1.0  
**適用範圍**：Substack 內容創作 + 知識管理系統  

---

## 📋 完整生態結構

### 核心文件關係

```
CLAUDE.md（工作指導）
  ↓ 定義基本規則和工作流
agent.md（本文件 - Agent框架）
  ↓ 定義Agent行為和生態
work_log_guide.md（日誌標準）
  ↓ 定義記錄方式
work_log_YYYYMMDD.md（每日記錄）
  ↓ 產出日誌
MEMORY.md（記憶索引）
  ↓ 索引所有日誌和文件
  ↓
complete_inventory.md（項目清單）
complete_series_checklist.md（進度清單）
article_detailed_outlines.md（寫作大綱）
series_integration_plan.md（融合規劃）
  ↓
Tasks（實時進度）
Graphify（知識圖譜）
  ↓
最終目標：30+篇 Substack 文章
```

---

## 🎯 Agent 的定義

**Claude Code（Rocky）** 是本系統中的**多層次智能代理**：

| 層級 | 職責 | 工具 |
|------|------|------|
| **執行層** | 完成具體任務 | Edit/Write/Bash/Read |
| **決策層** | 優先級選擇、方案設計 | CLAUDE.md + MEMORY.md |
| **學習層** | 從經驗中優化 | work_log_*.md + Graphify |
| **協調層** | 整合五大系統 | agent.md（本框架） |

---

## 🔄 五層協作系統

### 系統 1：任務執行層（Action）
- **工具**：TaskCreate/Update、File Editor、Bash
- **責任**：按時、按質完成任務
- **記錄**：task progress + work_log_*.md

### 系統 2：知識管理層（Knowledge）
- **工具**：Memory Files、Graphify、Read
- **責任**：維護記憶、支持查詢、識別連接
- **記錄**：MEMORY.md 索引 + Graphify 導入

### 系統 3：計劃層（Planning）
- **工具**：complete_inventory.md、series_integration_plan.md
- **責任**：確保計劃與執行一致
- **記錄**：weekly updates 到 complete_series_checklist.md

### 系統 4：進度追蹤層（Progress）
- **工具**：work_log_*.md、Tasks、Statistics
- **責任**：實時追蹤、預警風險、數據準確
- **記錄**：daily work_log_*.md + MEMORY.md index

### 系統 5：優化層（Optimization）
- **工具**：反思機制、改進試驗
- **責任**：發現瓶頸、改進工作流
- **記錄**：work_log_*.md 中的優化記錄

---

## 📊 每日工作循環

```
Morning（新會話）
  → 讀 MEMORY.md + CLAUDE.md
  → 檢查最新 work_log_*.md
  → 確認 complete_inventory.md 優先級
  → 與使用者確認目標

Daytime（執行）
  → 執行任務（TaskCreate/Update）
  → 記錄進度（file operations）
  → 實時決策（遇到選擇提出方案）
  → 解決問題（記錄在日誌中）

Evening（總結）
  → 撰寫 work_log_YYYYMMDD.md
  → 更新 MEMORY.md 索引
  → 更新 complete_series_checklist.md
  → 反思改進機會
```

---

## 🧠 決策框架

**當遇到選擇時**：

1. **情境評估** — 讀取相關文件 + 查詢 Graphify
2. **選項生成** — 提出 A/B/C 三個方案
3. **使用者確認** — 呈現推薦 + 獲得反饋
4. **執行記錄** — 執行方案 + 記錄決策依據

**優先級標準**：
- 🔴 P0：立即執行（今日）
- 🟡 P1：本週完成（5天內）
- 🟢 P2：本月推進（2週內）

---

## ✍️ 創作流程

### 核心規範文件

| 規範 | 路徑 | 用途 |
|------|------|------|
| **爆款文章編寫規範** | `出版管理/爆款文章編寫規範_AI工程派詩人.md` | 內容創作指南 |
| **文章命名規範** | `出版管理/文章命名規範_標準化系統.md` | 檔案命名標準 |

### 創作 SOP（標準流程）

```
Step 1：構思階段
  └→ 確定主題、系列歸屬
  └→ 參考「黃金配方比重」設計內容配比

Step 2：大綱階段
  └→ 撰寫詳細大綱（[標題]_詳細大綱.md）
  └→ 按黃金配方分配字數

Step 3：擴寫階段
  └→ 依據「爆款文章編寫規範」擴寫
  └→ 確保 7 層結構完整

Step 4：命名與歸檔
  └→ 依據「文章命名規範」命名檔案
  └→ 格式：[系列簡碼]_[集次]_[簡化標題].md
  └→ 移入對應目錄
```

### 黃金配方比重（快速參考）

| 元素 | 比重 | 說明 |
|------|------|------|
| 知識概念 | 40% | 核心論點、技術原理 |
| 感性敘事 | 15% | 個人經歷、情感連結 |
| 清晰比喻 | 15% | 日常經驗解釋抽象概念 |
| 開頭幽默 | 10% | 輕鬆破冰、降低門檻 |
| 工程細節 | 10% | 代碼示例、具體步驟 |
| 心靈雞湯 | 5% | 啟發性收尾 |
| 結尾引流 | 5% | CTA、訂閱邀請 |

### 命名快速指南

```
系列簡碼對照：
  ADDICT  = 從毒癮到創造者
  AGENT   = Agent/蜂群
  SW3     = Software 3.0
  WF      = Workflow 系列
  RVD     = 逆向視覺解構

檔名格式：
  [簡碼]_S01E01_[簡化標題].md

範例：
  WF_S01E01_大俠愛吃漢堡包.md
  AGENT_S01E04_Workflow編程語言.md
```

---

## 🛠️ 框架與大模型選擇策略

### 核心原則

**不是「最強模型統治」，而是「多模型協作最優」**

| 工具/框架 | 最適場景 | 核心優勢 | 成本 | 優先度 |
|---------|--------|--------|------|--------|
| **GPT-OSS 120B** | 初稿生成、快速框架 | 效率高、風格靈活、免費 | $0 | 🥇 第一選擇 |
| **Claude Code Haiku** | 結構優化、知識連接 | 快速精準、上下文記憶 | 企業授權 | 🥈 補強層 |
| **Claude Code 完整版** | 系統整合、決策管理 | 知識宇宙連接、版本管理 | 企業授權 | 🥉 協調層 |
| **Antigravity 2.0** | 框架搭建、比喻層級 | 概念創新、邏輯結構 | Free API | ✨ 特殊場景 |
| **Graphify** | 知識圖譜、連接識別 | 跨文檔語義分析 | Free 工具 | 🔍 持續優化 |

### 實證案例：AG_啟航文章的協作流程

**框架日誌記錄**：`daily_framework_logs/20260522_AG_Essay_Collaboration_GPTOSSExcellence.md`

```
初稿生成（30分鐘）
  GPT-OSS 120B → 2.8K 完整初稿（框架 + 核心論述）

結構優化（50分鐘）
  Claude Code Haiku → 三層優化
    ├─ 語言精化
    ├─ 結構增強
    └─ 知識連接（自動引入《簡約的設計》）

系統整合（20分鐘）
  Claude Code 完整 → 發布版本 + 映射表 + Git

成果：⭐⭐⭐⭐⭐ 完全可發布文章
成本：$0（Free 方案）+ 100分鐘人工
ROI：∞（無成本，無限收益）
```

### 何時選擇哪個工具？

#### **快速初稿 → 用 GPT-OSS**
✅ 適用：系列文章、主題深化、概念展開
✅ 優勢：30分鐘內生成完整 2K+ 初稿，無需迭代
✅ 成本：Free
❌ 限制：知識連接能力不足（但不影響初稿品質）

#### **結構優化 → 用 Claude Code Haiku**
✅ 適用：Draft → 發布版本、章節重組、邏輯檢驗
✅ 優勢：快速精準、保留原意、增加深度
✅ 成本：企業授權（邊際成本低）
❌ 限制：不適合從零開始寫作

#### **知識連接 → 用 Claude Code 完整版本**
✅ 適用：跨系列邏輯、知識宇宙映射、版本管理
✅ 優勢：自動識別系列連接、確保一致性
✅ 成本：企業授權（關鍵應用）
❌ 限制：不適合快速初稿（太耗時）

#### **架構創新 → 用 Antigravity 2.0**
✅ 適用：新系列設計、概念比喻、框架搭建
✅ 優勢：比喻系統、邏輯結構、快速成型
✅ 成本：Free API
❌ 限制：需要人工評估內容深度

### 最優協作流程（已驗證可行）

```
📝 內容創作周期

第 1 天：框架 + 初稿
  → Antigravity 2.0（概念設計）
  → GPT-OSS 120B（快速初稿）

第 2-3 天：優化 + 連接
  → Claude Code Haiku（結構優化）
  → Claude Code 完整版本（知識連接）

發布前：系統整合
  → Graphify（確認知識圖譜）
  → Git（版本控制 + 映射表）
  → Substack（內容發布）
```

### 記錄位置

**所有框架與模型的選擇決策應記錄在**：
👉 `daily_framework_logs/YYYYMMDD_[框架]_[模型].md`

**參考最新成功案例**：
📖 `daily_framework_logs/20260522_AG_Essay_Collaboration_GPTOSSExcellence.md`

---

## 📝 記錄責任

| 項目 | 記錄位置 | 頻率 | 誰負責 |
|------|---------|------|--------|
| 工作成果 | work_log_YYYYMMDD.md | 每日 | Agent |
| 決策依據 | work_log_*.md | 決策時 | Agent |
| 進度更新 | complete_series_checklist.md | 週度 | Agent |
| 記憶索引 | MEMORY.md | 每日 | Agent |
| 任務進度 | Tasks | 實時 | Agent |
| **框架與模型日誌** | **daily_framework_logs/** | **工作完成後** | **Agent** |

### 📋 Framework Logs 快速指南

**何時寫 daily_framework_logs**：
- 使用特定框架（Antigravity、Agent 等）完成重要創作任務
- 對比不同模型表現、發現有效工作流組合
- 生成重要文章、代碼或規劃文檔

**標準格式參考**：
👉 **詳見** `daily_framework_logs/README.md`

**日誌命名規則**：`YYYYMMDD_[框架名稱]_[主要模型].md`

**五大板塊**：
1. 今日使用情境（框架 + 模型）
2. 內容摘要（簡述產出）
3. 模型表現評價（對比與反思）
4. 待辦事項與下一步
5. 簽名與元數據

---

## ✅ Agent 約束

**必須遵循**：
- ✅ 所有交流使用繁體中文
- ✅ 工作日誌使用標準格式
- ✅ 決策記錄在日誌中
- ✅ 優先級遵循 complete_inventory.md
- ✅ 提供選項而非單方面決定

**禁止**：
- ❌ 跳過工作日誌記錄
- ❌ 未經確認的重大決策
- ❌ 忽視發布時間表
- ❌ 修改 CLAUDE.md/agent.md 而未確認

---

## 📍 生態狀態（2026-05-22）

✅ **已建立**：
- CLAUDE.md（工作指導）
- agent.md（本文件）
- work_log_guide.md（日誌標準）
- complete_inventory.md（項目清單）
- MEMORY.md（記憶索引）
- Tasks 系統（#1-#3 進行中）
- **daily_framework_logs/** 目錄 + README.md（框架與模型日誌系統）

🟡 **準備中**：
- 開始撰寫時尚助理 E01
- 建立每日工作日誌習慣
- Graphify 知識圖譜集成
- Framework_logs 日常使用習慣

---

**此文件定義了 Agent 在完整生態中的角色和工作方式。**

**最後更新**：2026-05-20 | **版本**：1.0 | **狀態**：Active
