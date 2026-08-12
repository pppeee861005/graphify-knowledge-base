---
name: substack-publisher
description: 建立並驗證 Substack 文章草稿。當使用者要求把 Markdown 文章放入 Substack 草稿、檢查草稿或回報草稿網址時使用；預設只建立草稿，不發布、不排程、不寄送 Email。
---

# Substack Publisher

## MVP 範圍

只執行以下流程：

```text
Markdown → 解析標題／副標題／正文 → 建立 Substack 草稿 → 確認 Saved → 回報網址
```

## 使用規則

1. 讀取指定的 Markdown 檔案，使用 UTF-8。
2. 將第一個 `#` 標題作為文章標題；若不存在，使用 Markdown 檔名作為標題。
3. 將標題後第一個 `##` 標題作為副標題；若不存在，副標題留空。
4. 移除 frontmatter、系列標籤與已移入欄位的標題／副標題，避免正文重複。
5. 保留段落、粗體、標題、引用、清單與水平線。
6. 建立新草稿前檢查相同標題，發現既有草稿時停止並回報，不覆蓋。
7. 建立後確認標題、正文開頭、正文結尾與 `Saved` 狀態。
8. 回報穩定的 `/publish/post/<id>` 草稿網址。
9. 成功建立後，將來源檔、草稿網址、時間與狀態寫入 `.substack-publisher-records.json`。

## 安全邊界

- 不點擊 `Continue`。
- 不發布、不排程、不寄送 Email。
- 不更新既有草稿，除非使用者明確提供草稿 ID 並授權更新。
- 登入、CAPTCHA 或權限問題出現時，停下並請使用者處理。

## 工具入口

```bash
node substack-cli.mjs draft "文章\ai即一切_第02篇.md"
node substack-cli.mjs verify "https://aiagentcommander.substack.com/publish/post/<draft-id>"
```

`--dry-run` 只驗證來源檔與轉換結果；未加 `--dry-run` 時，工具會使用已登入的 Substack 分頁建立實際草稿。

## Codex 執行模式

在 Codex 中，先取得已登入的 Substack 瀏覽器與分頁，再將 `{ browser, tab }` 傳給 `createDraft(article, options)` 或 `verifyDraft(url, options)`。不要依賴一般終端程序自行取得 Codex 的瀏覽器工作階段。
