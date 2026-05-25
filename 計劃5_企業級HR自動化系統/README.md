# 計劃 5：企業級 AI HR 自動化系統

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

### Phase 1：Workflow 驗證（06-01 ~ 06-07）
- 激活 Claude Code Workflow 功能
- 測試 `/workflows` 監控
- 編寫首個「請假審批」Workflow 腳本

### Phase 2：核心實現（06-08 ~ 06-21）
- 完整的請假審批流程
- 六個 Workflow Stage 的完整實現
- 與 Google Workspace 整合

### Phase 3：場景擴展（06-22 ~ 07-05）
- 報銷申請 Workflow
- 培訓申請 Workflow
- Workflow 範本庫建立

### Phase 4：生產驗證（07-06 ~ 07-12）
- 小規模試點測試
- 性能監控和優化
- 收集企業用戶反饋

### Phase 5：發布交付（07-13 ~ 07-19）
- v2.0 正式發布
- GitHub release notes
- 遷移指南和文檔

---

## 🔗 相關資源

### 計劃文檔
- [完整規劃](../計劃1_新世界HR系統/PLAN5_企業級HR自動化系統_plan.md)
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
