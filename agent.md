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

## 📝 記錄責任

| 項目 | 記錄位置 | 頻率 | 誰負責 |
|------|---------|------|--------|
| 工作成果 | work_log_YYYYMMDD.md | 每日 | Agent |
| 決策依據 | work_log_*.md | 決策時 | Agent |
| 進度更新 | complete_series_checklist.md | 週度 | Agent |
| 記憶索引 | MEMORY.md | 每日 | Agent |
| 任務進度 | Tasks | 實時 | Agent |

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

## 📍 生態狀態（2026-05-20）

✅ **已建立**：
- CLAUDE.md（工作指導）
- agent.md（本文件）
- work_log_guide.md（日誌標準）
- complete_inventory.md（項目清單）
- MEMORY.md（記憶索引）
- Tasks 系統（#1-#3 進行中）

🟡 **準備中**：
- 開始撰寫時尚助理 E01
- 建立每日工作日誌習慣
- Graphify 知識圖譜集成

---

**此文件定義了 Agent 在完整生態中的角色和工作方式。**

**最後更新**：2026-05-20 | **版本**：1.0 | **狀態**：Active
