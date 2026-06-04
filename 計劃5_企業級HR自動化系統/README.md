# 計劃 5：企業級 AI HR 自動化系統
特別意這是v1版本
有v2版本：我們專注於v2版本
**計劃代碼**：Plan-5-EnterpriseHR-Workflow
**版本**：v2.0（Workflow-First Architecture）
**基礎**：計劃 1 v1.0（Google Workspace + Apps Script）
**啟動日期**：2026-06-01
**框架**：Antigravity 2.0 + Claude Code Workflow
**狀態**：🚧 規劃完成，準備啟動 Phase 1

---

## 🎯 計劃 5 的戰略定位

### 為什麼獨立為計劃 5？

| 維度 | 計劃 1 v1.0 | 計劃 5 |
|------|-----------|-------|
| **定位** | MVP / 技術驗證 | 企業級 / 生產系統 |
| **時間** | 1-2 週完成 | 3 個月開發 |
| **目標受眾** | 個人、小企業 | 中大企業、HR 部門 |
| **技術棧** | Google Workspace + Apps Script | Workflow + Claude API + NotebookLM |
| **複用性** | 低（每個流程重寫） | 高（跨部門 Workflow 範本庫） |
| **成果** | 開源參考實現 | 企業級解決方案 |

### 計劃 5 = 計劃 1 的戰略升級

```
計劃 1 v1.0 驗證了「Human in the Loop」的可行性
    ↓
計劃 5 把「Human in the Loop」做成企業級產品
    ↓
完整的 Workflow 架構 + 多個 HR 場景 + 可複用的範本庫
```

---

## 📁 目錄結構

```
計劃5_企業級HR自動化系統/
├── src/                              # 源代碼
│   ├── workflows/                   # Workflow 腳本（計劃開發）
│   ├── agents/                      # Agent 定義（計劃開發）
│   └── utils/                       # 工具函數（計劃開發）
│
├── docs/                             # 文檔
│   ├── PLAN5_架構設計.md
│   ├── 開發路線圖.md
│   ├── API_參考.md
│   └── 最佳實踐.md
│
├── workflows/                        # Workflow 執行日誌
│   ├── leave_approval/             # 請假審批 Workflow
│   ├── expense_report/             # 報銷 Workflow
│   └── training_request/           # 培訓申請 Workflow
│
├── memory/                           # 項目進度追蹤
│   ├── phase_1_log.md
│   ├── phase_2_log.md
│   └── work_log_*.md
│
├── README.md                         # 本文件
└── PLAN5_企業級HR自動化系統_plan.md  # 完整規劃文檔

```

**主要實現代碼**：`計劃1_新世界HR系統/newworld-hr-system-v2/`

---

## 🚀 開發計畫（Phase 1-5）

**📊 詳細進度表**：[開發進度表.md](./docs/開發進度表.md) — 包含完整任務清單、時間表、交付物與成功標準

### 整體進度概覽

| Phase | 時間範圍 | 狀態 | 完成度 | 關鍵交付物 |
|-------|---------|------|--------|-----------|
| **Phase 1** | 06-01 ~ 06-07 | 🟢 準備中 | 0% | Workflow 驗證報告 |
| **Phase 2** | 06-08 ~ 06-21 | ⚪ 未開始 | 0% | 完整請假審批流程 |
| **Phase 3** | 06-22 ~ 07-05 | ⚪ 未開始 | 0% | Workflow 範本庫 |
| **Phase 4** | 07-06 ~ 07-12 | ⚪ 未開始 | 0% | 試點測試報告 |
| **Phase 5** | 07-13 ~ 07-19 | ⚪ 未開始 | 0% | v2.0 正式發布 |

**整體進度**：0% (0/5 Phases)

---

### Phase 1：Workflow 驗證（06-01 ~ 06-07）

**目標**：驗證 Claude Code Workflow 功能，建立首個示範 Workflow

**核心任務**：
- ✅ 激活 Claude Code Workflow 功能
- ✅ 測試 `/workflows` 監控機制
- ✅ 編寫首個「請假審批」Workflow 腳本
- ✅ 設計 Workflow 腳本模板規範
- ✅ 編寫測試案例

**交付物**：
- Workflow 驗證報告 (`memory/phase_1_log.md`)
- 首個 Workflow 腳本 (`workflows/leave_approval/v0.1.yaml`)
- 模板規範文檔 (`docs/Workflow模板規範.md`)

---

### Phase 2：核心實現（06-08 ~ 06-21）

**目標**：完整實現請假審批流程，包含六個 Workflow Stage

**核心任務**：
- ✅ 實現 6 個 Workflow Stage（申請解析 → 主管審批 → HR 審查 → 假期扣除 → 通知發送 → 異常處理）
- ✅ 與 Google Workspace 深度整合
- ✅ 完整的端到端測試
- ✅ 性能優化（目標：< 5 秒）

**交付物**：
- 完整請假審批 Workflow v1.0
- Google Workspace 整合模組
- 端到端測試報告與性能分析

---

### Phase 3：場景擴展（06-22 ~ 07-05）

**目標**：複製成功經驗，擴展到報銷與培訓場景

**核心任務**：
- ✅ 實現「報銷申請」Workflow（含 OCR 解析）
- ✅ 實現「培訓申請」Workflow（含課程推薦）
- ✅ 建立 Workflow 範本庫（可複用元件）
- ✅ 撰寫範本庫使用指南

**交付物**：
- 報銷申請 Workflow v1.0
- 培訓申請 Workflow v1.0
- Workflow 範本庫與使用指南

---

### Phase 4：生產驗證（07-06 ~ 07-12）

**目標**：小規模企業試點，收集真實反饋

**核心任務**：
- ✅ 招募 3-5 家企業試點用戶
- ✅ 系統部署與培訓
- ✅ 7 天監控與性能優化
- ✅ 收集用戶反饋（目標：≥ 4.0/5.0 滿意度）

**交付物**：
- 試點測試報告
- 用戶反饋分析
- Bug 修復清單與性能優化報告

---

### Phase 5：發布交付（07-13 ~ 07-19）

**目標**：正式發布 v2.0，推廣至社群

**核心任務**：
- ✅ v2.0 正式發布（GitHub Release）
- ✅ 完善安裝部署文檔與 API 參考
- ✅ 錄製示範影片（3 個場景）
- ✅ 社群推廣（Substack 文章 + 社交媒體）

**交付物**：
- v2.0 GitHub Release
- 完整文檔站點
- 示範影片與遷移指南
- Docker 映像檔

---

## 🔗 相關資源

### 計劃文檔
- [完整規劃](../計劃1_新世界HR系統/PLAN5_企業級HR自動化系統_plan.md)
- [開發進度表](./docs/開發進度表.md) ✅ **新增** — 詳細任務清單、時間表、交付物
- [開發路線圖](./docs/開發路線圖.md)（待撰寫）
- [API 參考](./docs/API_參考.md)（待撰寫）

### 代碼實現
- [Workflow 源代碼](../計劃1_新世界HR系統/newworld-hr-system-v2/src)
- [Workflow 腳本](../計劃1_新世界HR系統/newworld-hr-system-v2/workflows)

### 相關文章
- Agent 系列 E04：「Workflow：從 Prompt 到代碼」
- Human in the Loop 系列：設計哲學和應用

### 進度追蹤
- [工作日誌](./memory/)
- [daily_framework_logs](../daily_framework_logs/)

---

## 🎯 核心目標

**計劃 5 的三個目標**：

1. **技術目標**
   - ✅ 完整的 Workflow-First 架構
   - ✅ 6 種執行模式的實現
   - ✅ 多 Agent 並行協作

2. **應用目標**
   - ✅ 可複用的 HR Workflow 範本庫
   - ✅ 支持多個企業 HR 場景
   - ✅ 企業級文檔和部署指南

3. **生態目標**
   - ✅ 展示「Workflow 工程」的企業應用
   - ✅ 連動文章系列傳播設計理念
   - ✅ 構建社群 Workflow 範本庫

---

## 📊 與文章系列的連動

| 文章 | 發布時間 | 內容 |
|------|---------|------|
| Agent 系列 E04 | 2026-06-01 | Workflow 理論與實踐 |
| Human in the Loop E01 | 2026-05-27 | 設計哲學 |
| GitHub 計劃 5 Release | 2026-07-19 | v2.0 正式發布 |

---

## 🤝 何時加入

**計劃 5 的參與方式**：

- **開發者**：08 月後可參與 Workflow 腳本編寫
- **企業用戶**：Phase 4（試點測試）可申請試用
- **社群貢獻者**：發布 Workflow 範本到社群庫

---

## 📜 快速導航

| 需要 | 查看 |
|------|------|
| 完整規劃文檔 | [PLAN5_企業級HR自動化系統_plan.md](../計劃1_新世界HR系統/PLAN5_企業級HR自動化系統_plan.md) |
| 代碼實現 | [newworld-hr-system-v2/](../計劃1_新世界HR系統/newworld-hr-system-v2/) |
| 工作進度 | [memory/](./memory/) |
| 開發日誌 | [daily_framework_logs](../daily_framework_logs/) |

---

**計劃 5 狀態**：📋 規劃完成，準備啟動
**最後更新**：2026-05-25
**下一里程碑**：Phase 1 啟動（2026-06-01）

🚀 **計劃 5：從 MVP 到企業級產品**
