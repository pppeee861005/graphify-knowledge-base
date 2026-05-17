# Kling AI 視頻生成 - 設置指南

## 問題診斷

當前認證失敗是因為：
- Kling API 的認證機制可能需要簽名或特定的格式
- 直接的 HTTP 調用容易出錯
- 官方 SDK 會自動處理所有認證細節

## 解決方案

### 方案 A：使用官方 SDK（推薦）

1. **安裝官方 SDK**
```bash
pip install kling-ai-sdk
```

2. **使用提供的腳本**
```bash
python kling_nana_video.py
```

### 方案 B：使用 Web 界面

直接訪問 Kling AI 官方網站，使用 Web 界面上傳提示詞生成視頻：
- 無需編寫代碼
- 無需處理 API 認證
- 可視化界面更容易操作

### 方案 C：使用 cURL 測試

```bash
curl -X POST "https://api.klingai.com/v1/videos/text2video" \
  -H "Authorization: Bearer YOUR_ACCESS_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Your prompt here",
    "duration": 5,
    "mode": "generate"
  }'
```

## 腳本文件

- `kling_nana_video.py` - 完整的視頻生成腳本（SDK 自動處理認證）
- `.env` - API 認證信息存儲位置

## 提示詞

版本 B（極度動感衝擊版）已保存在腳本中：
```
EXPLOSIVE ACTION MOVIE POSTER: Ultra-dynamic confrontation between two beautiful
anime girls in a high-tech cyberpunk arena. The image bursts with kinetic energy.
...
```

## 下一步

1. **安裝 SDK**：`pip install kling-ai-sdk`
2. **確認 .env 配置**：已自動修復為標準格式
3. **運行腳本**：`python kling_nana_video.py`
4. **保存任務 ID**：用於查詢進度

## 常見問題

**Q: 我不想安裝 SDK 怎麼辦？**
A: 可以使用 Kling AI 官方網站的 Web 界面，或等待我們進一步調查認證方式。

**Q: 生成需要多長時間？**
A: 通常 1-5 分鐘，取決於服務器負載。

**Q: 可以生成多長的視頻？**
A: Kling 通常支持 5-60 秒，根據你的計劃而定。

---

**生成日期**：2026-05-17
**提示詞版本**：B（極度動感衝擊版）
**目標時長**：5 秒
