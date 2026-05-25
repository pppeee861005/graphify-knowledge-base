# Antigravity 2.0 讀書計劃

此目錄用於 **邊聊天邊記錄** 《貨幣戰爭2 · 金權天下》以及其他書籍的筆記與心得。

## 目錄結構
```
antigravity2.0讀書計劃/
├─ notes/                # 原始每日筆記（raw）
├─ summary/              # 匯總心得（YYYY-MM-DD.md）
├─ templates/            # 模板檔案
│   └─ daily_summary_template.md
├─ scripts/              # 協作腳本
│   ├─ add_reading_note.py
│   └─ build.py
└─ data/                 # 來源書籍 PDF/Markdown（可自行放入）
```

- **即時摘要**：每當你在聊天中提供段落，我會判斷其重要性，若關鍵則自動生成 **Mermaid** 關係圖建議，寫入 `summary/` 中。
- **自動化建置**：`build.py` 會監聽 `notes/` 與 `summary/` 的變更，於變更時重新產生靜態 HTML（使用 Mermaid 暗色主題、柔和漸層、微動畫）。
- **視覺風格**：Mermaid 圖表將套用 `theme: dark` 並加上自訂 CSS，以符合本計畫的高階視覺需求。
