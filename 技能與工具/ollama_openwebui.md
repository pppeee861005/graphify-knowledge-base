Ollama 與 Open WebUI 連線設定成功！

## 完成摘要

### 問題
Open WebUI 的 `OLLAMA_BASE_URL` 設為 `/ollama`（錯誤路徑），且 Ollama 只監聽 `127.0.0.1`，導致 Docker 容器無法連線。

### 解決步驟
1. ✅ **修改 Ollama 監聽設定** - 改為監聽 `0.0.0.0:11434`（所有介面）
2. ✅ **開放 UFW 防火牆** - 允許 11434 port
3. ✅ **重新建立 open-webui 容器** - 設定 `OLLAMA_BASE_URL=http://172.17.0.1:11434`
4. ✅ **連線測試成功** - `Ollama is running`

### 目前狀態
- **VPS IP**: `66.42.64.242`
- **Open WebUI**: `http://66.42.64.242:3000`
- **Ollama**: 版本 0.23.2，正常運行
- **連線**: ✅ 已成功

### 下一步建議
1. 在 Open WebUI 中註冊帳號開始使用
2. 如果需要下載模型，在 VPS 上執行 `ollama pull <模型名稱>`（例如 `ollama pull gemma3:1b`）
3. 或直接從 Open WebUI 介面下載模型