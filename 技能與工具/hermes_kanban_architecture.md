# Hermes Agent Kanban 核心架構完全指南

## 簡介

**Hermes Agent Kanban** 是一個生產級的多代理協作工作流系統，專為 AI 時代設計。與傳統的看板工具不同，Hermes Kanban 將任務管理提升到**多代理自主執行**的層次——每個代理都是一個獨立的 OS 進程，擁有自己的身份、工具集和技能。

**核心理念**：
> 不是人類分配任務給 AI，而是讓 AI 根據任務依賴自主聲稱（Claim）任務，自動協調，完全自動化。

---

## 🏗️ 核心架構

### 架構圖

```
┌─────────────────────────────────────────────────────────────┐
│                    Hermes Gateway                           │
│  (中央協調層，負責調度、監控、通信)                         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
        ┌────────────────────┐
        │  Kanban.db         │
        │  (SQLite 數據庫)   │
        │  ~/.hermes/        │
        │  kanban.db         │
        └────────────────────┘
                 │
     ┌───────────┼───────────┐
     ↓           ↓           ↓
┌─────────┐ ┌─────────┐ ┌─────────┐
│ Agent 1 │ │ Agent 2 │ │ Agent 3 │
│Process1 │ │Process2 │ │Process3 │
│         │ │         │ │         │
│Profile: │ │Profile: │ │Profile: │
│Research │ │Analysis │ │  Write  │
│         │ │         │ │         │
│Tools:   │ │Tools:   │ │Tools:   │
│graphify │ │claude   │ │substack │
│query    │ │api      │ │publish  │
└─────────┘ └─────────┘ └─────────┘

Workspace 隔離：
├─ Agent 1: ~/scratch/task_123
├─ Agent 2: ~/worktree/task_124
└─ Agent 3: ~/task_125_output
```

### 架構的四層含義

#### 第一層：Hermes Gateway（協調層）
- **職責**：監控任務狀態、分派任務、監測心跳、清理僵屍進程
- **特性**：
  - Cron 驅動的定時掃描
  - 原子性任務分派（Atomic Dispatch）
  - 實時狀態同步
  - 自動故障恢復

#### 第二層：Kanban.db（持久化層）
- **儲存位置**：`~/.hermes/kanban.db`
- **技術棧**：SQLite（零配置、高可靠性）
- **核心表結構**：
  ```sql
  -- 任務表
  CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    name TEXT,
    assignee TEXT,  -- 指定代理的 profile 名稱
    status TEXT,    -- pending, ready, in_progress, blocked, done
    workspace_kind TEXT,  -- scratch, worktree, dir:<path>
    parents TEXT,   -- 依賴的上游任務 (JSON list)
    children TEXT,  -- 下游任務 (JSON list)
    created_at TIMESTAMP,
    updated_at TIMESTAMP
  );
  
  -- 心跳表
  CREATE TABLE heartbeats (
    task_id TEXT,
    process_id INTEGER,
    timestamp TIMESTAMP,
    status TEXT
  );
  
  -- 評論表
  CREATE TABLE comments (
    id TEXT PRIMARY KEY,
    task_id TEXT,
    author TEXT,      -- 可以是 Agent Profile 或 Human
    message TEXT,
    created_at TIMESTAMP
  );
  ```

#### 第三層：Agent Profiles（執行層）
- **每個代理** = 一個獨立的 OS 進程
- **生命週期**：
  ```
  1. 啟動 → 讀取 ~/.hermes/profiles/<profile_name>.yaml
  2. 監控 → 每 5 秒查詢 Kanban.db 尋找分配給自己的 Ready 任務
  3. 聲稱 → `kanban_claim <task_id>`（原子操作）
  4. 執行 → 在隔離的 Workspace 中執行任務
  5. 心跳 → 每 10 秒發送一次 `kanban_heartbeat <task_id>`
  6. 完成 → `kanban_complete <task_id>`（或 `kanban_block` 如果被阻塞）
  ```

#### 第四層：Workspace 隔離（資源層）
- **三種隔離模式**：
  ```
  1. scratch:        臨時目錄 ~/scratch/task_<id>
                     適合：數據分析、查詢、無狀態操作
                     
  2. worktree:       Git worktree ~/worktrees/task_<id>
                     適合：代碼修改、PR 創建、版本控制
                     
  3. dir:<path>:     自定義目錄 <指定路徑>
                     適合：長期項目、多任務共享資源
  ```

---

## 🔑 七大關鍵特性

### 特性 1：SQLite 持久化存儲

**What**：所有任務狀態和操作都存儲在本地 SQLite 數據庫中

**Why**：
- 零依賴（無需外部服務）
- 高可靠性（ACID 保證）
- 支持崩潰恢復
- 可離線工作
- 快速查詢（適合實時監控）

**How**：
```bash
# 查詢當前所有任務
sqlite3 ~/.hermes/kanban.db "SELECT id, name, status FROM tasks;"

# 查詢特定代理的任務
sqlite3 ~/.hermes/kanban.db "SELECT * FROM tasks WHERE assignee='writer' AND status='in_progress';"

# 查看任務依賴關係
sqlite3 ~/.hermes/kanban.db "SELECT id, name, parents FROM tasks WHERE status='ready';"
```

### 特性 2：任務 = 行記錄

**What**：每個任務是 Kanban.db 中的一行數據

**Why**：
- 可查詢（SQL）
- 可統計（聚合）
- 可篩選（複雜條件）
- 可追蹤（完整歷史）
- 可遷移（導入導出）

**Example**：
```sql
-- 統計本週完成的任務數
SELECT COUNT(*) FROM tasks 
WHERE status='done' 
AND DATE(updated_at) >= DATE('now', '-7 days');

-- 找出卡住最久的任務（被阻塞超過 1 小時）
SELECT id, name, DATETIME('now') - updated_at AS hours_blocked 
FROM tasks 
WHERE status='blocked' 
AND DATETIME('now') - updated_at > 3600;

-- 找出依賴鏈最長的任務樹
WITH RECURSIVE task_tree AS (
  SELECT id, name, parents, 0 as depth
  FROM tasks WHERE parents IS NULL
  UNION ALL
  SELECT t.id, t.name, t.parents, tt.depth + 1
  FROM tasks t
  JOIN task_tree tt ON t.id IN (tt.children)
)
SELECT * FROM task_tree ORDER BY depth DESC;
```

### 特性 3：代理獨立進程

**What**：每個代理都是一個獨立的、長運行的 OS 進程

**Why**：
- **資源隔離**：一個代理的故障不影響其他代理
- **並行執行**：真正的多進程並行（不是線程）
- **獨立身份**：每個代理有自己的 Profile、工具、權限
- **可觀測性**：可用 `ps`, `top`, `htop` 監控

**Process 結構**：
```
$ ps aux | grep hermes
claude2  12345  0.5  1.2  524288  98765 ?  S  14:23  0:15  hermes run --profile researcher
claude2  12346  0.3  0.9  512000  72000 ?  S  14:23  0:08  hermes run --profile analyst
claude2  12347  0.4  1.5  556000  120000 ?  S  14:23  0:12  hermes run --profile writer

每個進程獨立：
├─ PID 不同
├─ Memory 不同
├─ Workspace 不同
└─ 日誌文件不同
```

**Process 生命週期**：
```
1. hermes kanban dispatch （Gateway 掃描）
   ↓
2. 找到 status='ready' 且 assignee='researcher' 的任務
   ↓
3. 啟動 OS Process: hermes run --profile researcher --task task_123
   ↓
4. Process 進入監控迴圈：每 5 秒查詢 Kanban.db
   ↓
5. 發現新任務後執行（在隔離的 Workspace 中）
   ↓
6. 執行中：每 10 秒發送 heartbeat（更新 updated_at）
   ↓
7. 完成或卡住：kanban_complete 或 kanban_block
   ↓
8. Process 繼續運行，尋找下一個任務
```

### 特性 4：自動依賴管理

**What**：任務可以聲明 `parents=` 依賴，Kanban 自動管理 Gate

**Why**：
- 無需人工協調
- 自動 Gate（依賴滿足後自動轉 ready）
- 支持複雜的依賴圖（DAG - 有向無環圖）
- 防止死鎖（circular dependency 檢測）

**How**：
```yaml
# 創建任務時指定依賴
$ hermes kanban create "分析報告" \
  --assignee analyst \
  --parents task_123,task_124

# 任務狀態轉遷
task_123 (done) ─┐
                 ├─→ task_125 → status 自動變 ready
task_124 (done) ─┘

# 複雜依賴例子（暗知識系列 E02）
T1 (Update Graph) ──┐
                    ├──→ T3 (Analysis) ──→ T4 (Write)
T2 (Query Graph) ──┘

YAML 表示：
tasks:
  - id: T1
    name: "更新圖譜"
    status: "done"
    
  - id: T2
    name: "查詢圖譜"
    status: "done"
    
  - id: T3
    name: "分析"
    parents: [T1, T2]  # 同時依賴 T1 和 T2
    status: "ready"    # 自動轉為 ready（因為 T1, T2 都 done 了）
    
  - id: T4
    name: "寫作"
    parents: [T3]
    status: "pending"  # 等待 T3 完成
```

### 特性 5：Cron 驅動的自動分派

**What**：Gateway 使用 Cron 定時掃描，自動將 Ready 任務分派給對應的代理

**Why**：
- 無需人類干預
- 無需外部調度工具
- 可預測的延遲（Cron 間隔）
- 原子性分派（無競態條件）

**How**：
```bash
# 啟動 Kanban 分派服務
$ hermes kanban dispatch --interval 60  # 每 60 秒掃描一次

# 分派流程
1. 每 60 秒檢查一次 Kanban.db
2. 查詢：SELECT * FROM tasks WHERE status='ready' AND assignee IS NOT NULL
3. 對於每個 ready 任務：
   a. 檢查 assignee 對應的 profile 是否已有進程運行
   b. 若無，啟動新進程：hermes run --profile <assignee> --task <task_id>
   c. 原子性更新 status 為 'in_progress'
4. 監控運行中的進程（heartbeat）
5. 回到第 1 步

# 分派日誌示例
[14:23:45] Dispatcher scan: Found 3 ready tasks
[14:23:45] Dispatching task_123 to researcher
[14:23:46] Starting process PID=12345 for researcher
[14:23:47] Dispatcher scan: Found 2 ready tasks
[14:23:47] Dispatching task_125 to analyst
[14:23:48] Starting process PID=12346 for analyst
```

### 特性 6：Heartbeat 監控 + 自動清理

**What**：運行中的進程每 10 秒發送心跳，Dispatcher 據此監控和清理

**Why**：
- 檢測僵屍進程（Process 掛了，但數據庫狀態還是 in_progress）
- 自動恢復（重啟故障進程）
- 防止資源洩漏（長期僵屍進程佔用 CPU/Memory）
- 實時監控（知道誰活著、誰死了）

**How**：
```bash
# Process 端：發送心跳
$ hermes kanban heartbeat --task task_123

# 更新 heartbeats 表
INSERT INTO heartbeats (task_id, process_id, timestamp, status)
VALUES ('task_123', 12345, '2026-05-20 14:24:00', 'ok');

# Gateway 端：監控和清理
Gateway 每 30 秒掃描一次：
1. 查詢所有 in_progress 任務
2. 檢查最新的 heartbeat（若 > 30 秒未更新 → 進程死了）
3. 強制殺死 PID（kill -9）
4. 重置任務狀態為 'ready'（重新分派）
5. 記錄日誌（便於追蹤故障）

日誌示例：
[14:24:30] Heartbeat scan
[14:24:30] task_123 (PID 12345): OK (last beat 1s ago)
[14:24:30] task_124 (PID 12346): DEAD (last beat 125s ago)
[14:24:31] Killing zombie process 12346
[14:24:31] Resetting task_124 to ready
[14:24:32] Dispatcher will pick it up in next scan
```

### 特性 7：評論系統（人類 + AI 協作）

**What**：任務可以有評論線程，人類和 AI 都可以讀寫

**Why**：
- **非同步協作**：不用等待實時回應
- **完整記錄**：所有決策和討論都留下痕跡
- **人類干預**：如果 AI 卡住，人類可以評論提示
- **可審計**：便於事後檢查（誰說了什麼）

**How**：
```bash
# AI 端：發送評論（如果卡住）
$ hermes kanban comment task_123 \
  "遇到問題：找不到某節點的參考文獻。是否跳過？"

# 人類端：回覆評論
$ hermes kanban comment task_123 \
  "跳過該節點，改用替代方案 XYZ。繼續執行。"

# 查看評論線程
$ hermes kanban show task_123 --comments

Output:
Task: task_123 (暗知識 E02 - 分析)
───────────────────────────────────
[2026-05-20 14:24:15] analyst (AI):
> 遇到問題：找不到某節點的參考文獻。是否跳過？

[2026-05-20 14:25:00] peter861005 (Human):
> 跳過該節點，改用替代方案 XYZ。繼續執行。

[2026-05-20 14:25:05] analyst (AI):
> 已接受指示，繼續執行...

# 評論可觸發 AI 的行為變化（通過 kanban_comment 事件）
AI Process 定期檢查：
SELECT * FROM comments WHERE task_id='task_123' AND timestamp > last_check
若有新評論 → 更改執行策略 → 繼續執行
```

---

## 🛠️ 工具集詳解（9 個核心工具）

### 1. kanban_show — 查看任務詳情

```bash
$ hermes kanban show task_123

Output:
┌────────────────────────────────────────┐
│ Task: task_123                         │
│ Name: 暗知識 E02 - 分析                │
├────────────────────────────────────────┤
│ Status:      in_progress               │
│ Assignee:    analyst                   │
│ Workspace:   worktree                  │
│ Created:     2026-05-20 14:20:00       │
│ Updated:     2026-05-20 14:24:30       │
│ Parents:     [task_121, task_122]      │
│ Children:    [task_124]                │
├────────────────────────────────────────┤
│ Comments: 2                            │
│ Heartbeat: OK (last 5s ago)            │
└────────────────────────────────────────┘
```

### 2. kanban_list — 列表查詢

```bash
# 列出所有任務
$ hermes kanban list

# 按條件篩選
$ hermes kanban list --status pending
$ hermes kanban list --assignee writer
$ hermes kanban list --status blocked --order created_at

Output:
ID        Name                  Status        Assignee
────────────────────────────────────────────────────────
task_121  更新圖譜              done          researcher
task_122  查詢圖譜              done          researcher
task_123  分析                  in_progress   analyst
task_124  寫作                  pending       writer
task_125  發布                  pending       writer
```

### 3. kanban_create — 創建任務

```bash
$ hermes kanban create "寫暗知識 E02" \
  --assignee writer \
  --workspace worktree \
  --parents task_123 \
  --tenant default

# 返回任務 ID
Created: task_124

# YAML 方式創建（更複雜的配置）
$ hermes kanban create --from config.yaml

# config.yaml
tasks:
  - name: "分析"
    assignee: analyst
    parents: [task_121, task_122]
    workspace_kind: scratch
    
  - name: "寫作"
    assignee: writer
    parents: [task_123]
    workspace_kind: worktree
```

### 4. kanban_link — 創建/修改依賴

```bash
# 添加依賴關係
$ hermes kanban link task_124 --parents task_123

# 移除依賴
$ hermes kanban link task_124 --remove-parent task_123

# 查看依賴圖
$ hermes kanban link --graph
```

### 5. kanban_complete — 標記完成

```bash
$ hermes kanban complete task_123 \
  --message "分析完成，產出 3370 字結構文檔"

# 效果：
# 1. task_123 status 從 in_progress → done
# 2. 查詢 task_123 的所有 children（task_124 等）
# 3. 對每個 child，檢查其他 parents 是否都 done 了
# 4. 若是，自動轉其狀態為 ready
# 5. 下次 Dispatcher scan 時會立即分派
```

### 6. kanban_block — 標記被阻塞

```bash
$ hermes kanlan block task_124 \
  --reason "等待 task_123 的輸出文件"

# 效果：
# task_124 status 從 in_progress → blocked
# 人類可以在 Kanban 儀表板中看到「被卡住的任務」
# 可以手動 unblock 或調查原因
```

### 7. kanban_unblock — 解除阻塞

```bash
$ hermes kanban unblock task_124

# 或帶原因（用於評論）
$ hermes kanban unblock task_124 \
  --message "已獲得所需文件，恢復執行"
```

### 8. kanban_comment — 評論

```bash
# AI 發評論
$ hermes kanban comment task_123 \
  --message "遇到問題：找不到節點 XYZ 的參考"

# 人類回覆
$ hermes kanban comment task_123 \
  --message "跳過該節點，改用方案 ABC"

# 查看完整評論線程
$ hermes kanban show task_123 --comments
```

### 9. kanban_heartbeat — 心跳信號

```bash
# Process 定期發送（由 Hermes Agent 自動調用）
$ hermes kanban heartbeat --task task_123

# 或手動測試
$ hermes kanban heartbeat --task task_123 --status ok

# 查看最近的心跳
$ hermes kanban show task_123 | grep -A 5 "Heartbeat"
```

---

## 📊 工作流例子：暗知識系列 E02

### 完整時間線

```
14:20:00 | Task 創建
─────────────────────────────────────────────────────────
$ hermes kanban create "更新圖譜" --assignee researcher
→ Created: task_121

$ hermes kanban create "查詢圖譜" --assignee researcher
→ Created: task_122

$ hermes kanban create "分析" --assignee analyst \
  --parents task_121,task_122
→ Created: task_123 (status: pending)

$ hermes kanban create "寫作" --assignee writer \
  --parents task_123
→ Created: task_124 (status: pending)

14:20:10 | Dispatcher 首次掃描
─────────────────────────────────────────────────────────
status='ready' 的任務：task_121, task_122
分派給 researcher（同時啟動兩個子進程）

14:20:15 | Process 開始執行（並行）
─────────────────────────────────────────────────────────
[researcher process 1] $ graphify update . 
[researcher process 2] $ graphify query '黑箱三層次'

14:20:30 | Process 定期發送心跳
─────────────────────────────────────────────────────────
14:20:30 [researcher-1] heartbeat: OK
14:20:30 [researcher-2] heartbeat: OK
14:20:40 [researcher-1] heartbeat: OK
14:20:40 [researcher-2] heartbeat: OK

14:20:57 | task_121 完成
─────────────────────────────────────────────────────────
[researcher-1] $ hermes kanban complete task_121

14:20:58 | task_122 完成
─────────────────────────────────────────────────────────
[researcher-2] $ hermes kanban complete task_122
→ task_123 自動轉為 ready

14:21:00 | Dispatcher 掃描（檢測 task_123 ready）
─────────────────────────────────────────────────────────
status='ready' 的任務：task_123
分派給 analyst

14:21:05 | task_123 開始執行
─────────────────────────────────────────────────────────
[analyst process] $ 讀取 task_121 和 task_122 的產出
[analyst process] $ 綜合分析，生成結構文檔

14:21:15 | task_123 遇到問題，阻塞
─────────────────────────────────────────────────────────
[analyst] $ hermes kanban block task_123 \
  --reason "需要確認某個節點是否納入"

14:21:20 | 人類評論提供指示
─────────────────────────────────────────────────────────
$ hermes kanban comment task_123 \
  --message "納入該節點，使用定義 XYZ"

14:21:25 | AI 檢測到評論，繼續執行
─────────────────────────────────────────────────────────
[analyst] 檢查評論 → 更新執行策略 → 繼續執行

14:28:00 | task_123 完成
─────────────────────────────────────────────────────────
[analyst] $ hermes kanban complete task_123 \
  --message "產出 351 行結構文檔"
→ task_124 自動轉為 ready

14:28:05 | Dispatcher 掃描（檢測 task_124 ready）
─────────────────────────────────────────────────────────
status='ready' 的任務：task_124
分派給 writer

14:28:10 | task_124 開始執行
─────────────────────────────────────────────────────────
[writer process] $ 讀取 task_123 的結構文檔
[writer process] $ 逐段撰寫正文

14:32:20 | task_124 完成
─────────────────────────────────────────────────────────
[writer] $ hermes kanban complete task_124 \
  --message "完成 3370 字初稿"

14:32:30 | 所有任務完成
─────────────────────────────────────────────────────────
$ hermes kanban list --status done
task_121  ✓
task_122  ✓
task_123  ✓
task_124  ✓

Total Time: 12 分 30 秒（包括 1 分鐘人工干預）
```

### 關鍵亮點

1. **完全並行**：task_121 + task_122 同時執行（0.5 分）
2. **自動門控**：task_123 在依賴完成後自動轉 ready
3. **人類協作**：AI 卡住時，評論提示立即改變行為
4. **審計日誌**：每個決策都永久記錄在 Kanban.db 中
5. **快速分派**：下一個任務在依賴完成後 5 秒內開始（Dispatcher 掃描間隔）

---

## 🔄 與 Claude Agents（Agent View）的對比

| 維度 | Hermes Kanban | Claude Agents |
|-----|---------------|--------------|
| **持久化** | ✅ SQLite 永久存儲 | ❌ 會話記憶（重啟消失） |
| **自動依賴** | ✅ parents= 自動 gate | ❌ 無自動依賴管理 |
| **進程隔離** | ✅ 獨立 OS 進程 | ❌ 同一個 Claude 進程 |
| **並行度** | N 個 worker | 最多 10 個 Session |
| **反饋速度** | ⏳ 60 秒（Cron 掃描） | ⚡ 實時（按 Space Peek） |
| **學習成本** | ❌ 高（概念多） | ✅ 低（直觀易用） |
| **人類協作** | ✅ 評論系統 + block/unblock | ✅ 可打斷、改指令 |
| **網路斷線** | ✅ 自動恢復 | ❌ 中斷就掉線 |
| **適用場景** | 複雜、長流程、需要自動化 | 簡單、快速迭代、實驗 |

---

## 🎯 何時使用 Hermes Kanban？

### 最適合的場景

✅ **複雜多步流程**（3+ 個任務，有依賴鏈）
- 例：暗知識系列寫作（T1 → T2 → T3 → T4）
- 例：個人時尚助理 Skill 開發（需求 → API 集成 → 測試 → 發布）

✅ **週期性重複工作**
- 例：每週自動發布 Substack 文章
- 例：月度數據分析流程

✅ **需要完整審計日誌**
- 例：生產環境任務（需要追蹤每個決策）
- 例：團隊協作（誰做了什麼、為什麼做）

✅ **網路不穩定**
- 例：VPS 上運行長時間任務
- 例：需要自動故障恢復

✅ **多代理大規模協作**
- 例：20+ 個並行任務
- 例：需要優先級調度（不同代理優先級不同）

### 不太合適的場景

❌ **簡單單步操作**（直接用 Claude Agents）
❌ **需要實時交互**（用 Claude Code 交互模式）
❌ **快速原型、頻繁改指令**（用 Agent View 更靈活）

---

## 📚 快速開始

### 1. 安裝和初始化

```bash
# 安裝 Hermes（假設已裝）
hermes version

# 初始化 Kanban（創建 ~/.hermes/kanban.db）
hermes kanban init

# 創建 Agent Profile
cat > ~/.hermes/profiles/researcher.yaml << EOF
name: researcher
tools:
  - graphify
  - bash
personality: |
  You are a research expert. Extract knowledge from documents.
EOF

cat > ~/.hermes/profiles/analyst.yaml << EOF
name: analyst
tools:
  - claude_api
  - bash
personality: |
  You are an analyst. Synthesize information into insights.
EOF

cat > ~/.hermes/profiles/writer.yaml << EOF
name: writer
tools:
  - substack_api
  - bash
personality: |
  You are a writer. Create engaging content.
EOF
```

### 2. 創建任務

```bash
hermes kanban create "Task 1" --assignee researcher
hermes kanban create "Task 2" --assignee analyst --parents <task_1_id>
hermes kanban create "Task 3" --assignee writer --parents <task_2_id>
```

### 3. 啟動 Dispatcher

```bash
# 後臺啟動（推薦）
hermes kanban dispatch --interval 60 &

# 或前臺（便於調試）
hermes kanban dispatch --interval 60 --verbose
```

### 4. 監控

```bash
# 查看所有任務
hermes kanban list

# 監控特定任務
hermes kanban show <task_id> --watch

# 查看實時日誌
tail -f ~/.hermes/kanban.log
```

---

## ⚠️ 常見問題

### Q1: 任務卡住了怎麼辦？

```bash
# 1. 查看任務狀態
hermes kanban show <task_id>

# 2. 查看評論（有沒有 AI 的錯誤信息）
hermes kanban show <task_id> --comments

# 3. 人類干預：添加評論
hermes kanban comment <task_id> --message "嘗試方案 XYZ"

# 4. 若無法恢復，標記為 blocked
hermes kanban block <task_id> --reason "人工介入所需"

# 5. 修復後解除阻塞
hermes kanban unblock <task_id>
```

### Q2: 如何修改已創建的任務？

```bash
# Kanban 不支持直接修改（只讀設計），需要：
# 1. 完成原任務
hermes kanban complete <old_task_id>

# 2. 創建新任務（改進的版本）
hermes kanban create "改進版本" --assignee <profile>
```

### Q3: 如何處理循環依賴？

```bash
# Hermes 會檢測並拒絕（Circular Dependency Detection）
$ hermes kanban link task_A --parents task_B
$ hermes kanban link task_B --parents task_A
→ Error: Circular dependency detected: task_A → task_B → task_A

# 需要重新設計依賴結構，確保是 DAG（有向無環圖）
```

### Q4: 進程崩潰了怎麼辦？

```bash
# Heartbeat 監控會自動檢測（30 秒內無心跳 = 進程死亡）
# Gateway 會：
# 1. 殺死僵屍進程
# 2. 重置任務狀態為 ready
# 3. 下次掃描時重新分派

# 人類可以查看崩潰日誌：
tail -f ~/.hermes/kanban.log | grep "DEAD\|crash\|ERROR"
```

---

## 📖 相關資源

- [Hermes Agent 官方文檔](https://hermes-agent.nousresearch.com/docs/)
- [Kanban 教程](https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-tutorial)
- [SQLite 查詢參考](https://www.sqlite.org/lang.html)
- [DAG 設計最佳實踐](https://en.wikipedia.org/wiki/Directed_acyclic_graph)

---

## 📝 版本歷史

| 版本 | 日期 | 更新內容 |
|-----|------|---------|
| 1.0 | 2026-05-20 | 完成初稿，包含架構、特性、工具集、工作流、對比、FAQ |

**文檔作者**：Claude Code  
**最後更新**：2026-05-20  
**狀態**：✅ 完成

---

## 🔗 與內部知識的連接

- [[kanban-agents-knowledge-block]] — Kanban & Agents 統一知識板塊（Memory）
- [[skill-development-plan]] — Skill 開發計劃（使用 Hermes Kanban）
- [[focus-2026-q2]] — Q2 聚焦項目（包含 Kanban 實踐）
- `iinput/kanban_flow.MD` — 實際工作流案例
- `iinput/cc_agentview_vs_kanban_revised.html` — Kanban vs Agent View 對比
