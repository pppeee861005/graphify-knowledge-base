# Agent 系列配圖歸屬清單

> 記錄《蜂群 Agent 系列》各篇章的配圖來源、製作工具與設計者

---

## 📊 配圖清單

### Agent 系列 E01：《蜂群 Agent 是什麼》
| 配圖內容 | 檔案名 | 製作工具 | 製作者 | 完成日期 |
|---------|--------|--------|--------|---------|
| — | — | — | — | — |

**狀態**：📝 待補充配圖

---

### Agent 系列 E02：《可適應性蜂群永不被淘汰》
| 配圖內容 | 檔案名 | 製作工具 | 製作者 | 完成日期 |
|---------|--------|--------|--------|---------|
| — | — | — | — | — |

**狀態**：📝 待補充配圖

---

### Agent 系列 E03：《解耦哲學：Anthropic 設計蜂群的靈魂》
| 配圖內容 | 檔案名 | 製作工具 | 製作者 | 完成日期 |
|---------|--------|--------|--------|---------|
| — | — | — | — | — |

**狀態**：📝 待補充配圖

---

### Agent 系列 E04（Part 1）：《Workflow 工作流編排 - 理論篇》
| 配圖內容 | 檔案名 | 製作工具 | 製作者 | 完成日期 |
|---------|--------|--------|--------|---------|
| — | — | — | — | — |

**狀態**：📝 待補充配圖

---

### Agent 系列 E04（Part 2）：《Workflow 工作流編排 - 實踐篇》
| 配圖內容 | 檔案名 | 製作工具 | 製作者 | 完成日期 |
|---------|--------|--------|--------|---------|
| **Pipeline 流水線模式** | pipeline_animation.svg | SVG + CSS3 Animations | Claude Code Haiku 4.5 | 2026-05-25 |
| **Pipeline 高清PNG圖** | pipeline_workflow_diagram.png | Kling AI 圖片生成 | Claude Code Haiku 4.5 | 2026-05-25 |
| **Pipeline GIF動畫** | pipeline_workflow_diagram.gif | Python Selenium + Pillow | Claude Code Haiku 4.5 | 2026-05-25 |

**狀態**：🔄 進行中（Pipeline 完成，待補充其他5種模式配圖）

**待補充配圖：**
- [ ] Synchronous Aggregation（同步聚合模式）
- [ ] Adversarial Validation（對抗驗證模式）
- [ ] Best-of Mode（末尾篩選制）
- [ ] Cumulative Pattern（累積式模式）
- [ ] Nested Workflow（嵌套式工作流）

---

## 🛠️ 製作工具與技術

### Claude Code Haiku 4.5
- **主要工具**：SVG 設計、Kling AI API 調用、Selenium 自動化
- **配圖特徵**：
  - 動態 SVG 動畫（CSS3 keyframes）
  - 4K 高清圖片生成（Kling AI）
  - GIF 循環動畫（自動化捕幀）
- **文檔與代碼**：
  - `svg-to-gif.js`：Node.js SVG 轉 GIF 工具
  - `svg_to_gif.py`：Python SVG 轉 GIF 自動化腳本

---

## 📚 相關資源

### 配圖製作流程
1. **SVG 設計**（Claude Code Haiku）
   - 使用純 SVG + CSS3 動畫
   - 保留動畫效果與編輯性

2. **PNG 導出**（Kling AI）
   - 4K 高清輸出
   - 適合靜態展示與 Substack 發布

3. **GIF 製作**（Python Selenium）
   - 捕捉動畫的全部幀
   - 無限循環播放

### 可重用工具
- `svg_to_gif.py`：通用 SVG 轉 GIF 工具
  - 參數化設置（幀率、解析度、循環次數）
  - 跨平台相容性
  - 可用於其他系列文章配圖

---

## 📝 記錄說明

**更新規則：**
- 每當完成新配圖時，立即更新此清單
- 記錄製作工具、製作者、完成日期
- 注明配圖的檔案位置與技術特徵

**命名規則：**
- SVG 源檔：`[系列名]_[內容簡述].svg`
- PNG 圖片：`[系列名]_[內容簡述].png`
- GIF 動畫：`[系列名]_[內容簡述].gif`

**製作者簽名：**
```
🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

---

**最後更新**：2026-05-25
**維護者**：Claude Code Haiku 4.5
