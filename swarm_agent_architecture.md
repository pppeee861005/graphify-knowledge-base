# 完整自建蜂群 Agent 架構設計
## Hermes + CubeSandbox + Vultr VPS 三層模型

**架構理念**：不是永久部署，而是 On-Demand 動態組合 — 任務到達 → Agent 集群喚起 → 運算完成 → 資源立刻釋放

---

## 第一層：指令中樞層（本地機器）

### 角色
- **AI Commander**（豪力風神）的大腦和決策層
- 不負責具體執行，只負責任務分發和結果聚合

### 技術棧
```
Windows WSL2 / MacOS
├─ Claude Code v2.0.76（DISABLE_AUTOUPDATER=1 永遠固定）
├─ Hermes Agent 本地實例（輕量級網關 Gateway）
│  └─ 作用：接收用戶指令 → 決策何時喚起云端 Agent
├─ API Client（Python / Node.js）
│  └─ 管理 CubeSandbox 遠程實例的生命週期
└─ Orchestrator 邏輯（自建）
   └─ 分析任務複雜度 → 決定需要幾個 Specialist Agent
   └─ 監控資源成本 → 自動停止超時任務
```

### 責任
1. **任務解析**：接收自然語言指令
2. **Agent 調度決策**：
   - 簡單任務（<5 min）→ 直接本地執行
   - 中等任務（5-30 min）→ 喚起 1 個 Specialist Agent
   - 複雜任務（>30 min）→ 喚起多個並行 Specialist Agent（最多 25 個）
3. **結果聚合**：等待所有 Specialist 完成 → 統一返回結果

---

## 第二層：持久記憶層（VPS on Vultr）

### 位置選擇
**新加坡 VPS**（最低延遲 to 中國 + 東亞）
- 推薦配置：**dedicated A40 48GB VRAM** or **RTX 4090 24GB**
- 預算方案：8核 32GB RAM（足夠 25 個並發 CubeSandbox 實例）

### 技術棧
```
Vultr Singapore VPS
├─ Hermes Agent 主進程（systemd service）
│  ├─ 工作記憶（Working Memory）
│  │  ├─ Redis（in-memory，AOF persistence）
│  │  └─ 存儲：當前 Session 狀態 + 活動 Agent 上下文
│  │
│  ├─ 長期記憶（Long-term Memory）
│  │  ├─ PostgreSQL / SQLite
│  │  └─ 存儲：過往任務結果 + 提取的 Skill + 學習模式
│  │
│  └─ 事件日誌（Episodic Log）
│     ├─ SQLite（時間戳所有互動）
│     └─ 用途：Agent 自我反思 + 持續學習
│
├─ CubeSandbox 容器運行時（containerd + CubeShim）
│  └─ 零個或多個 MicroVM 實例（按需產生，用完即刪）
│
├─ Gateway API（HTTP 服務）
│  ├─ 監聽 3000 端口（接收本地 Hermes 分發的任務）
│  ├─ 實現 Specialist Agent 生命週期管理
│  └─ 返回 JSON 結果 + 成本統計
│
└─ 監控 + 清理守護進程
   ├─ Task Watchdog：監控每個 Specialist 的執行時間
   ├─ Resource Reaper：超時自動殺掉 Sandbox
   └─ Cost Tracker：累計本次執行的 GPU 成本
```

### 記憶架構（持久化）
```
Redis（在內）→ AOF 日誌（磁盤）
PostgreSQL（磁盤）← 每個 Session 結束時持久化
├─ session_id | agent_id | timestamp | outcome | tokens_used | cost
├─ skill_library（可複用的智能代碼片段）
├─ preference_matrix（模型選擇規則：Claude for reasoning, DeepSeek for chats）
└─ performance_metrics（哪個 Agent 配置最高效）

SQLite Episodic Log（磁盤）
├─ 每次任務的完整過程記錄
└─ Agent 自省的數據源：「我上次怎麼解決類似問題的？」
```

---

## 第三層：執行層（CubeSandbox MicroVM 實例）

### 動態生命週期

#### 0️⃣ 靜止狀態
```
Vultr VPS 空閒
├─ 沒有 CubeSandbox 實例運行
├─ 只有 Hermes 主進程 + Redis + API Server 在監聽
└─ 月成本 = VPS 基礎費 + 極少 GPU 閒置費
```

#### 1️⃣ 任務到達 — Agent 喚起
```
本地 Hermes 發送：
{
  "task": "寫一個 React 組件 + 單元測試",
  "model": "claude-opus-4-7",
  "specialist_count": 2,
  "timeout": 600,
  "resources": {
    "cpu": 4,
    "memory": "8GB",
    "gpu": "A40"
  }
}
     ↓
API Server 收到 → 調用 CubeSandbox API
     ↓
產生 2 個 MicroVM 實例（冷啟 <70ms）
├─ Specialist-1（代碼架構師）
│  ├─ 模型：Claude Opus
│  ├─ Sandbox-id：micro-vm-12345
│  ├─ 分配資源：4 核 + 8GB 記憶
│  └─ 啟動時間：~50ms
│
└─ Specialist-2（測試工程師）
   ├─ 模型：Claude Haiku（成本最低）
   ├─ Sandbox-id：micro-vm-12346
   ├─ 分配資源：2 核 + 4GB 記憶
   └─ 啟動時間：~60ms

總啟動時間：<100ms（串行等待最慢的那個）
```

#### 2️⃣ 執行中 — 並行協調

```
┌─────────────────────────────────────────────────────┐
│           Lead Agent（協調者）                      │
│           在 Specialist-1 或本地 Hermes            │
│                                                     │
│  "寫 React 組件" → Specialist-1（已啟動）          │
│  "寫單元測試" → Specialist-2（已啟動）             │
│                                                     │
│  兩個並行執行，各自有隔離的 Sandbox 容器            │
└─────────────────────────────────────────────────────┘
                         ↓
        ┌────────────────┴────────────────┐
        ↓                                 ↓
┌───────────────────┐           ┌───────────────────┐
│ Specialist-1      │           │ Specialist-2      │
│ Sandbox-1         │           │ Sandbox-2         │
│                   │           │                   │
│ 工作內容：        │           │ 工作內容：        │
│ 1. 分析需求      │           │ 1. 分析代碼      │
│ 2. 生成組件代碼   │           │ 2. 編寫 Jest 測試│
│ 3. 自我驗證（測試）│          │ 3. 執行覆蓋率檢查 │
│                   │           │                   │
│ 內存：8GB         │           │ 內存：4GB         │
│ CPU：4 核         │           │ CPU：2 核         │
│ 運行時間：180 sec │           │ 運行時間：90 sec  │
└───────────────────┘           └───────────────────┘
        ↓                                 ↓
  [✓ 完成]                        [✓ 完成]
  結果保存到內存                   結果保存到內存
```

#### 3️⃣ 任務完成 — 資源立刻釋放

```
所有 Specialist 完成 → Lead Agent 收到 2 個結果
     ↓
API Server 調用 CubeSandbox 清理 API
     ↓
同步刪除 2 個 MicroVM 實例
├─ micro-vm-12345：釋放 4 核 + 8GB（70ms 內完成）
└─ micro-vm-12346：釋放 2 核 + 4GB（70ms 內完成）
     ↓
Redis 更新任務完成狀態 → 成本統計保存
     ↓
本地 Hermes 收到最終結果：
{
  "status": "completed",
  "result": { "component": "...", "tests": "..." },
  "execution_time": 180,
  "cost_usd": 0.42,
  "tokens_used": {
    "specialist_1": 4521,
    "specialist_2": 2103
  }
}
     ↓
VPS 回到靜止狀態
（只有 Hermes + Redis 在低功耗運行）
```

---

## 架構圖（完整流程）

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Commander 本地                        │
│  用戶 → 自然語言輸入 → Claude Code / Hermes 本地實例        │
│                          ↓                                   │
│                   Orchestrator Logic                         │
│         分析任務 → 決定喚起幾個 Specialist Agent            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ HTTP API Call (gRPC 可選)
                      │ {task, model, specialist_count, timeout}
                      ↓
┌─────────────────────────────────────────────────────────────┐
│            Vultr Singapore VPS（8核 32GB）                  │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │   Hermes Agent Main Process (systemd service)       │   │
│  │                                                      │   │
│  │  ┌──────────────────┐  ┌──────────────────┐        │   │
│  │  │  API Server      │  │  Task Watchdog   │        │   │
│  │  │  (Port 3000)     │  │  (監控超時)      │        │   │
│  │  └────────┬─────────┘  └──────────────────┘        │   │
│  │           │                                         │   │
│  │  ┌────────v──────────────────────┐                 │   │
│  │  │  Memory Layer                  │                 │   │
│  │  ├─ Redis (Working Memory)        │                 │   │
│  │  ├─ PostgreSQL (Long-term Memory) │                 │   │
│  │  └─ SQLite (Episodic Log)         │                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │   CubeSandbox Runtime (containerd + CubeShim)       │   │
│  │                                                      │   │
│  │   [待命]                                             │   │
│  │   MicroVM 容器池：最多 25 個實例                     │   │
│  │   每個實例 < 5MB 內存開銷 + <70ms 冷啟              │   │
│  │                                                      │   │
│  │   任務來時：                                         │   │
│  │   ┌──────────┐  ┌──────────┐  ┌──────────┐         │   │
│  │   │ Specialist-1 │ │ Specialist-2 │ ... (N 個)  │   │
│  │   │ Agent    │  │ Agent    │  │ Agent    │         │   │
│  │   └──────────┘  └──────────┘  └──────────┘         │   │
│  │   並行執行，各自隔離容器                             │   │
│  │                                                      │   │
│  │   任務完成立刻清理（rm -f 實例）                     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                      ↓
                  [結果返回]
                      ↓
        ┌─────────────────────────────┐
        │ 本地 Hermes 聚合結果        │
        │ 傳給 Claude Code 展示       │
        │ 或發佈到 Substack          │
        └─────────────────────────────┘
```

---

## 資源動態管理邏輯

### 場景 1：快速任務（<5 分鐘）
```
不啟動 CubeSandbox
直接在本地 Hermes 執行
成本最低 = 0（只用本地算力）
```

### 場景 2：中等任務（5-30 分鐘）
```
啟動 1 個 Specialist Agent
使用時間：實際執行 + 10 秒冷啟 + 10 秒清理 = ~20 秒開銷
GPU 時間計費：20 sec + 300-1800 sec（執行）= 320-1820 sec
成本 = (GPU 時間 / 3600) × GPU 時薪

例：A40 時薪 $1.2
180 秒執行 + 20 秒開銷 = 200 秒 = 0.055 小時
成本 = 0.055 × 1.2 = $0.066
```

### 場景 3：複雜任務（>30 分鐘，多 Agent 並行）
```
N 個 Specialist 並行
總 GPU 時間 = max(Specialist 執行時間) + 20 秒開銷

例：2 個 Agent，分別執行 180 秒和 120 秒
總時間 = max(180, 120) + 20 = 200 秒（不是 360 秒！）

成本節省 = 單序列執行成本 - 並行成本
        = (180 + 120 + 40) sec 成本 - (200 sec 成本)
        = (340 - 200) / 3600 × 1.2 = 節省 $0.047
```

### 超時自動清理
```
設置超時閾值（例 30 分鐘）
Task Watchdog 監控每個 Specialist 的實際運行時間

如果任何 Specialist 超時：
1. 立刻發送 SIGTERM（優雅停止）
2. 等待 10 秒
3. 如果仍未停止，發送 SIGKILL（強制終止）
4. 從 CubeSandbox 徹底刪除 MicroVM 實例
5. 記錄失敗日誌（為後續 Agent 改進提供數據）
6. 從 Redis 退款（退還已預配的成本）
```

---

## 内存和狀態管理

### 跨 Session 持久化
```
一個「蜂群執行」= 一個 Session

Session 結構：
{
  "session_id": "sess_abc123xyz",
  "timestamp_start": "2026-05-14T10:30:00Z",
  "task_description": "寫 React 組件 + 測試",
  "orchestrator_config": {
    "specialist_count": 2,
    "model_mapping": {
      "specialist_1": "claude-opus-4-7",
      "specialist_2": "claude-haiku-4-5"
    }
  },
  "agents": [
    {
      "agent_id": "specialist_1",
      "sandbox_id": "micro-vm-12345",
      "status": "completed",
      "execution_time_sec": 180,
      "tokens_used": 4521,
      "result": {...}
    },
    ...
  ],
  "final_result": {...},
  "total_cost_usd": 0.42,
  "timestamp_end": "2026-05-14T10:34:20Z"
}

持久化：
1. 立刻存入 PostgreSQL（計費記錄 + 學習數據源）
2. 實時同步到 SQLite Episodic Log
3. 可選：歸檔到 S3（長期備份）
```

### Agent 自我學習
```
Session 完成後，Lead Agent 自動反思：

1. 讀取 SQLite Episodic Log（過往 N 個 Session）
2. 提取可複用的 Skill：
   - 「React 組件架構模式」
   - 「Jest 單元測試範本」
   - 「錯誤恢復策略 X」
3. 保存到 PostgreSQL skill_library
4. 下次遇到類似任務時，直接調用現成 Skill，跳過 0-1 階段

Skill 復用 = 減少 Token 消耗 = 降低成本
```

---

## 支付和成本追蹤

### 分層計費模型
```
本月賬單 = VPS 基礎費 + GPU 按秒計費

VPS 基礎費（Vultr）
├─ 8 核 32GB RAM：~$80/月
├─ 帶寬：~$10/月（新加坡内网便宜）
└─ 小計：~$90/月

GPU 按秒計費（CubeSandbox MicroVM）
├─ A40 時薪：$1.2/h = $0.000333/sec
├─ RTX 4090 時薪：$0.8/h = $0.000222/sec
├─ 使用時間：只有任務執行時才計費
└─ 待機成本：0（MicroVM 完全刪除，無待命費用）

例：月執行 100 個任務
├─ 平均每個任務 300 秒（5 分鐘）
├─ 總 GPU 秒數：100 × 300 = 30,000 sec = 8.33 小時
├─ 成本：8.33 × 1.2 = $10
├─ 月總費用：$90(VPS) + $10(GPU) = $100
```

### 成本優化機會

**策略 1：智能模型分配**
```
複雜推理任務 → Claude Opus（最精準，但貴）
日常執行任務 → Claude Haiku（最便宜）
節省 60-70% GPU 成本
```

**策略 2：Skill 複用**
```
第一次學習 Skill：Token 多，成本高
後續複用 Skill：直接調用，不重新生成
積累 50 個高頻 Skill → 成本降 40%
```

**策略 3：超時設置**
```
風險任務（可能無限循環）：設短超時（5 分鐘）
確定型任務（一定完成）：寬鬆超時（30 分鐘）
防止資源浪費 + 成本爆炸
```

---

## 與 Managed Agents 的本質區別

| 特性 | Managed Agents（官方） | 你的 Hermes + CubeSandbox |
|------|---------|---------|
| **架構掌控** | Anthropic 黑盒 | 完全透明 + 可改 |
| **Thread 管理** | 內建（25 上限） | 自建（可超過 25） |
| **成本模式** | Token 固定價 | GPU 秒計 + 可優化 |
| **記憶持久化** | Memory Store API | 自建（Redis + PostgreSQL）|
| **Agent 定制** | 受限（Anthropic 生態） | 無限（支持任何模型 + MCP）|
| **部署方式** | 云端托管 | 自己掌控 VPS |
| **學習曲線** | 學習 API 調用 | 學習完整架構 + 運維 |
| **適合人群** | 快速上市創業 | 知識供應商 + 技術傳教 |

---

## 實施路線圖（你的下一步）

### Phase 1（當前 - 2 周）
```
✅ 驗證 CubeSandbox 冷啟 <70ms
✅ Vultr 部署基礎設施
✅ 實現簡化版 Task Watchdog
📋 目標：確保資源能動態產生 + 刪除
```

### Phase 2（2-4 周）
```
📋 實現 Session 狀態機（記錄完整執行歷史）
📋 集成 CubeSandbox 生命週期 API
📋 搭建 API Server（接收本地 Hermes 分發）
📋 測試 2 個並行 Specialist Agent 協調
```

### Phase 3（4-8 周）
```
📋 PostgreSQL + SQLite 持久化層
📋 Skill 提取 + 複用邏輯
📋 成本追蹤 + 可視化儀表板
📋 多模型動態分配策略
```

### Phase 4（8-12 周）
```
📋 完整文檔 + Notion 知識庫
📋 開源到 GitHub（@豪力風神 / swarm-agent-os）
📋 Substack 文章系列發佈
📋 付費課程（L3 Skill：蜂群 Agent 工程化設計）
```

---

## 最關鍵的一句話

> **不是永久部署，而是 On-Demand 動態組合**
>
> 任務來時，Agent 瞬間喚起（<100ms）
>
> 任務完成，資源立刻釋放（<100ms）
>
> 待機成本 = 0，只付使用時長
>
> 這正是 Swarm Agent 相比傳統微服務架構的核心優勢

---

## 術語對標

| 官方術語（Managed Agents） | 你的架構 |
|---------|---------|
| Session | On-Demand 執行會話 |
| Thread | Specialist Agent 實例 |
| Memory Store | Redis + PostgreSQL |
| Sandbox | CubeSandbox MicroVM |
| Tool Router | API Gateway + Task Watchdog |
| Outcome Grading | Session 結果驗證 + Cost Tracking |

---

## 核心優勢總結

✅ **完全掌控** — 不受 Anthropic 生態限制，可支持任何 LLM + MCP Server
✅ **成本可控** — GPU 按秒計費，不用時不付錢
✅ **無限擴展** — 並發 Agent 數不受 25 個上限限制
✅ **知識沉澱** — 完整執行日誌 + Skill 庫成為 IP 資產
✅ **傳教使命** — 開源 + 課程 = 「新人類聯盟」的技術傳播工具
✅ **未來證明** — 基於 CubeSandbox（開源、生產驗證、行業標準）

---

**版本：v1.0-2026.05.14**
**適用者：豪力風神（AI Commander）**
**應用場景：新人類聯盟蜂群 Agent 基礎設施**
