# Claude Managed Agents 完全指南

## 簡介

**Claude Managed Agents** 是 Anthropic 在 2026 年 4 月推出的企業級 API 服務，它將 AI Agent 的開發和運維從「自己搭建」升級到「托管服務」。與自建 Agent 不同，Managed Agents 解耦了 **Brain（推理）** 和 **Hands（執行）**，由 Anthropic 負責基礎設施、故障恢復、安全沙箱等一切運維負擔。

**核心理念**：
> 讓開發者專注於定義 Agent 的「能力和人設」，而不是担心「如何運行和恢復」。

---

## 🏗️ 架構設計

### 核心洞察：解耦 Brain 和 Hands

Managed Agents 的設計核心是**分離推理和執行**：

```
傳統 Agent（自建）：
Claude Model ←→ Tool Executor ←→ File System / APIs
              （同進程、緊耦合）

Claude Managed Agents（托管）：
┌──────────────────────────────────────────┐
│  Anthropic Harness（協調層）            │
│  - 推理循環（無狀態）                  │
│  - 錯誤恢復（自動重試）                │
│  - Context 管理（自動優化）            │
└──────────────────────────────────────────┘
         ↓                      ↓
   Claude Model          Container
   （推理 Brain）        （執行 Hands）
   - 無狀態             - 有狀態
   - 可替換             - 隔離
   - 快速               - 安全
```

### 架構的四層組件

#### 層級 1：Agent 定義（配置層）

一個 Agent 由四個部分組成：
```yaml
Agent Configuration:
  model: "claude-opus-4-6"           # 推理引擎
  system_prompt: "你是一個 AI 研究助手..."  # 人設
  tools:                             # 能力集
    - type: "agent_toolset_20260401" # 內置工具
      name: "bash"                   # bash 執行
    - type: "agent_toolset_20260401"
      name: "file_operations"        # 文件操作
    - type: "agent_toolset_20260401"
      name: "web_search"             # Web 搜索
  mcp_servers:                       # MCP 伺服器
    - name: "brave_search"           # 搜索能力擴展
    - name: "postgres_database"      # 數據庫連接
  skills:                            # Claude Skills
    - "research_paper_analysis"      # 論文分析
```

#### 層級 2：Harness（協調層）

Harness 是無狀態的協調層，負責：
- **推理循環**：馬上識別何時調用工具、何時停止
- **錯誤恢復**：工具失敗時自動重試或備用方案
- **Context 優化**：管理 Claude 的上下文窗口（自動摘要）
- **日誌記錄**：每個步驟都記錄為 Event

```
推理循環：
1. 讀取當前會話的事件日誌
2. 傳送給 Claude Model：「根據這些信息，下一步做什麼？」
3. Claude 決策：調用工具 OR 返回答案 OR 提問
4. 若調用工具：路由到 Container，獲取結果
5. 新增 Event（工具調用 + 結果）
6. 回到第 2 步
```

#### 層級 3：Container（執行層）

每個 Session 有一個專用容器：
- **隔離環境**：運行 bash、文件操作、MCP 命令
- **持久工作區**：在容器中存儲文件、狀態
- **網路存取**：可調用 APIs、訪問數據庫
- **自動清理**：Session 結束後自動銷毀

```
Container 內：
/session/<session_id>/
  ├─ workspace/          # 工作目錄（會話級別）
  │  ├─ documents/
  │  ├─ research/
  │  └─ outputs/
  ├─ logs/              # 日誌（執行詳情）
  └─ credentials/       # 密鑰（Anthropic 管理）
```

#### 層級 4：Session & Event（持久層）

一個 Session 是 Agent + 容器 + 對話歷史的組合：

```
Session Structure:
{
  id: "session_abc123",
  agent_id: "agent_xyz",
  created_at: "2026-05-20T14:30:00Z",
  
  events: [
    {
      type: "user_message",
      content: "寫一篇關於 AI Agent 的論文"
    },
    {
      type: "tool_call",
      tool: "bash",
      command: "curl https://arxiv.org/... | grep -i agent"
    },
    {
      type: "tool_result",
      result: "Found 2341 papers on agents..."
    },
    {
      type: "model_response",
      content: "基於搜索結果，我發現..."
    },
    ...
  ]
}
```

所有 events 都存儲在 Anthropic 的服務器上，支持：
- **恢復**：網路中斷後從最後一個 event 繼續
- **回放**：讀取完整歷史，進行審計
- **分析**：統計 Agent 的表現、成本、行為

---

## 🛠️ 內置工具集

### Tool 1: bash（命令執行）

```bash
# Example: 列出目錄
bash ls -la /workspace

# Example: 運行 Python 腳本
bash python3 -c "import json; print(json.dumps({'status': 'ok'}))"

# Example: 調用 curl
bash curl -H "Authorization: Bearer $API_KEY" https://api.example.com/data
```

### Tool 2: file_operations（文件操作）

```bash
# 讀取文件
file_read /workspace/input.txt

# 寫入文件
file_write /workspace/output.txt "內容"

# 編輯文件（指定行號）
file_edit /workspace/config.yaml 10 20 "新內容"

# 搜索文件（glob）
file_glob /workspace/*.md

# 搜索內容（grep）
file_grep /workspace "pattern" --recursive
```

### Tool 3: web_search（Web 搜索）

```bash
# 搜索（返回 JSON 結果）
web_search "Claude Agent 最佳實踐"

# 結果包含：
{
  "results": [
    {
      "title": "...",
      "url": "...",
      "snippet": "..."
    }
  ]
}
```

### Tool 4: web_fetch（獲取網頁）

```bash
# 獲取網頁內容
web_fetch https://example.com/article

# 返回：HTML → Markdown 轉換
# 適合：分析網頁、提取信息
```

### Tool 5: MCP 伺服器（擴展）

MCP（Model Context Protocol）允許集成第三方服務：

```yaml
mcp_servers:
  - name: "database"
    type: "postgres"
    config:
      host: "db.example.com"
      port: 5432
      database: "analytics"
      # Credentials 由 Anthropic 管理
      
  - name: "search"
    type: "brave_search"
    config:
      api_key: "$BRAVE_API_KEY"  # 由 Vault 注入

# Agent 可以直接調用：
# "查詢數據庫：SELECT * FROM users WHERE..."
# "搜索最新新聞：最近的 AI Agent 發展"
```

---

## 🚀 快速開始

### 步驟 1：創建 Agent

```python
from anthropic import Anthropic

client = Anthropic()

# 定義 Agent
agent = client.agents.create(
    model="claude-opus-4-6",
    name="research_assistant",
    description="幫助分析論文和生成報告",
    system_prompt="""
    你是一個 AI 研究助手。
    任務：
    1. 搜索相關文獻
    2. 分析和總結
    3. 生成結構化報告
    
    你可以使用所有可用工具。優先使用 web_search 找最新信息。
    """,
    tools=[
        {
            "type": "agent_toolset_20260401",
            "name": "bash"
        },
        {
            "type": "agent_toolset_20260401",
            "name": "file_operations"
        },
        {
            "type": "agent_toolset_20260401",
            "name": "web_search"
        }
    ]
)

print(f"Agent created: {agent.id}")
```

### 步驟 2：創建 Session

```python
# 為特定用戶/項目創建一個 Session
session = client.agents.sessions.create(
    agent_id=agent.id,
    environment="cloud"  # 也可以是 "self_hosted"
)

print(f"Session created: {session.id}")
```

### 步驟 3：執行任務（流式）

```python
# 發送任務給 Agent
response = client.agents.messages.create(
    session_id=session.id,
    message="請寫一篇關於 AI Agent 未來的報告，包括：1) 當前趨勢 2) 技術挑戰 3) 應用前景"
)

# 流式接收結果
print("Agent is thinking...")
for event in response:
    if event.type == "tool_call":
        print(f"🔧 Calling: {event.tool.name}")
    elif event.type == "tool_result":
        print(f"✅ Result: {event.result[:100]}...")
    elif event.type == "model_response":
        print(f"🤖 Agent: {event.content}")

print("\n✨ Task complete!")
```

### 步驟 4：查看 Session 歷史

```python
# 獲取完整的事件日誌
history = client.agents.sessions.get_history(
    session_id=session.id
)

for event in history.events:
    print(f"{event.type}: {event.content}")

# 用於：
# - 審計（誰做了什麼）
# - 故障排查（哪一步出錯了）
# - 性能分析（每一步花了多少時間）
```

---

## 📊 工作流示例

### 例子：自動化研究報告生成

```
User Input
  ↓
"寫一篇關於 Swarm Agents 的報告"
  ↓
┌─────────────────────────────────────┐
│ Harness Processing                  │
│ 1. 讀取 Session 歷史                 │
│ 2. 傳給 Claude: "下一步做什麼？"    │
└─────────────────────────────────────┘
  ↓
Claude Decision: "搜索最新信息"
  ↓
┌─────────────────────────────────────┐
│ Tool Call: web_search               │
│ Query: "Swarm Agents 2026"          │
└─────────────────────────────────────┘
  ↓
Container 執行：curl → Google API
  ↓
結果：「Found 1200+ articles...」
  ↓
Event Record: tool_call + tool_result
  ↓
Claude Decision: "分析結果，寫報告"
  ↓
┌─────────────────────────────────────┐
│ Tool Call: file_write               │
│ Content: "# Swarm Agents Report...  │
│          深度分析..."                │
└─────────────────────────────────────┘
  ↓
Output: 完整報告存在容器中
  ↓
User 下載文件
```

---

## 💡 設計模式

### 模式 1：順序執行（Pipeline）

```
Task 1 ──→ Task 2 ──→ Task 3
搜索        分析        寫報告

實現：
- 每個 Task 作為一個 message
- 讀取前一個 Task 的輸出
- 作為下一個 Task 的輸入
```

### 模式 2：並行執行（Fan-out）

```
Main Task
  ├─→ Sub-task A（搜索）
  ├─→ Sub-task B（數據查詢）
  ├─→ Sub-task C（API 調用）
  └─→ Merge Results

實現：
- 創建多個 Session（相同 Agent，不同輸入）
- 監控所有 Session 的完成
- 合並結果
```

### 模式 3：條件分支（If-then-else）

```
Decision Point
  ├─ If condition A → Path 1
  ├─ If condition B → Path 2
  └─ Else → Path 3

實現：
- Claude 根據情況決定下一步
- 自動調用不同的工具
- 動態流程（無需預定義）
```

---

## 🔐 安全性和權限

### 環境隔離

```
Cloud Environment（推薦）:
- Anthropic 管理的容器
- 自動備份、監控
- DDoS 保護、WAF
- 合規認證（SOC 2）

Self-Hosted Environment（企業）:
- 部署在自己的基礎設施
- 完全控制、離線運行
- 需要自己處理故障恢復
```

### 密鑰管理

```
Vault System:
- API keys 存儲在 Anthropic Vault
- Agent 可以引用：$BRAVE_API_KEY
- 運行時注入到容器
- 不暴露在 Agent 代碼或日誌中
```

### 權限控制

```
Session-Level Isolation:
- 每個 Session 只能訪問自己的容器
- 數據隔離：user_A 的 Session 看不到 user_B
- 工具權限：可配置哪些 Agent 能用哪些工具
```

---

## 📈 監控和成本

### 成本追蹤

```
計費基礎：
- Input tokens（文本輸入）
- Output tokens（模型生成）
- Tool usage（調用工具的次數）
- Storage（事件日誌存儲）

示例：
Task: 寫 1000 字報告
├─ Input: 500 tokens（提示詞）
├─ Output: 2000 tokens（報告）
├─ Tools: 5 calls × $0.001 = $0.005
└─ Total: ~$0.015

Monthly Budget:
Pro Tier: $20/月
Max Tier: $100-200/月
```

### 性能指標

```
可監控的指標：
- Time to First Tool Call（TTFC）
- Tool Execution Time
- Error Rate
- Cost per Task
- Tokens per Task
```

---

## 🔄 與其他系統的集成

### 與 Claude Code Agent View 的區別

| 特性 | Agent View | Managed Agents |
|------|-----------|-----------------|
| **運行環境** | 本地（Claude Code） | 托管（Anthropic 基礎設施）|
| **持久化** | 會話記憶 | API 日誌 + 計費 |
| **規模** | 最多 10 Session | 無限 |
| **計費** | 無（訂閱） | 按使用量 |
| **目標用戶** | 開發者 | 企業 + SaaS |

### 與 Hermes Kanban 的區別

| 特性 | Hermes Kanban | Managed Agents |
|------|--------------|-----------------|
| **運行環境** | 本地（SQLite） | 托管（Anthropic）|
| **依賴管理** | parents= 自動 Gate | 事件驅動 |
| **隔離** | 獨立 OS 進程 | 容器隔離 |
| **目標場景** | 本地自動化 | SaaS/生產 |

---

## 🎓 最佳實踐

### BP1：使用 Vault 管理密鑰

```yaml
# ✅ 好
mcp_servers:
  - name: "database"
    config:
      api_key: "$DB_PASSWORD"  # 運行時注入

# ❌ 不好
mcp_servers:
  - name: "database"
    config:
      api_key: "sk-12345..."   # 硬編碼！
```

### BP2：定義清晰的 System Prompt

```python
# ✅ 好
system_prompt = """
你是一個 Code Review Agent。
任務清晰性：
- 檢查代碼質量、安全性、性能
- 提出具體改進建議
- 用 Markdown 格式輸出

約束：
- 最多 10 分鐘完成（避免無限循環）
- 只使用 file_operations 和 bash
"""

# ❌ 不好
system_prompt = "你是 AI Agent，做有用的事"
```

### BP3：監控工具調用的異常

```python
# ✅ 好：處理工具失敗
try:
    web_search("query")
except ToolError:
    # 備用方案
    use_local_cache()

# ❌ 不好：無限重試
while True:
    try:
        tool_call()
    except:
        pass  # 忽略錯誤
```

### BP4：定期檢查成本

```python
# 定期審計
sessions = client.agents.sessions.list()
for session in sessions:
    cost = session.metadata.get("cost")
    if cost > budget:
        print(f"Warning: Session {session.id} exceeded budget!")
```

---

## ⚠️ 常見坑

### 坑 1：Context Window 溢出

```
症狀：Agent 開始「重複」之前做過的事
原因：Session 太長，Context 滿了
解決：
- 定期創建新 Session
- Claude 會自動摘要舊信息
- 檢查 Event 日誌大小
```

### 坑 2：工具的奇怪行為

```
症狀：bash 命令返回意外結果
原因：容器環境與本地不同
解決：
- 使用 bash --version 檢查環境
- 避免依賴特定的 shell 配置
- 用 python3 -c 而不是複雜的 shell 腳本
```

### 坑 3：成本失控

```
症狀：月度費用突然激增
原因：Agent 進入無限循環
解決：
- 設置 timeout
- 監控 tool_call 數量
- 檢查 Event 日誌
```

---

## 📖 官方資源

- [Claude Managed Agents 官方文檔](https://platform.claude.com/docs/en/managed-agents/overview)
- [快速開始](https://platform.claude.com/docs/en/managed-agents/quickstart)
- [Claude Cookbook](https://github.com/anthropics/cookbook) - 教程和示例
- [Anthropic Blog](https://www.anthropic.com/research) - 最新文章

---

## 🔗 與個人時尚助理的應用

### 第 3 層應用：商業化版本

```
商業模式：
1. 免費版：每天 1 套推薦（Agent View）
2. Pro 版：每天 5 套推薦（Managed Agents）
3. B2B 版：企業白牌化（Managed Agents）

技術實現：
- Frontend：用戶上傳照片 + 日程
  ↓
- Backend：Managed Agents 處理
  ├─ Session per user（隔離）
  ├─ 調用 Kling API 生成虛擬穿衣
  └─ 返回推薦 + 購物鏈接
  ↓
- Billing：按 API 使用量計費
```

---

**文檔狀態**：✅ 完成  
**最後更新**：2026-05-20  
**作者**：Claude Code
