# 🚀 Ultracode 完整使用指南

**作者**：Claude
**日期**：2026-07-09
**難度**：⭐⭐⭐⭐ 進階
**應用場景**：複雜工作流、毫秒級決策、平行審計、多維驗證

---

## 第一部分：Ultracode 是什麼？

### 核心定義

**Ultracode** 於 2026-05-28 隨著 Claude Opus 4.8 推出，是一個**自動化多代理工作流編排系統**。

核心特性：
1. **xhigh 推理釘子**：將推理努力自動鎖定在最高級（xhigh），確保每次訊息都有深度思考
2. **動態工作流編排**：Claude 自動感知任務複雜度 → 自動生成子代理並行工作流 → 自動協調結果

### 簡單類比

| 層級 | 工作模式 | 代理數 | Token消耗 | 決策時間 |
|------|---------|-------|----------|---------|
| **L1 廚房型** | Claude 逐步決策 | 1 | 0.5k-2k | 需要人工干預 |
| **L1.5 監控台型** | 3+ session 獨立並行 | 3-5 | 5k-15k | 人工綜合 |
| **L2 施工隊型** | **主控中心輻射派遣** | 5-10 | **100k-300k** | 5 秒左右 |
| **L3 工廠自動化** | **Ultracode 自動編排** | 10-50+ | **500k-2M** | **毫秒級** |

### 為什麼要用 Ultracode？

```
傳統方式（L1-L1.5）：
妳 → Claude → 分析... → Claude → 決策... → 妳等待 15-60秒

Ultracode 方式（L2-L3）：
妳 → Claude主控 ┐
           ├→ 子代理1 NLP解析     0.03秒 ↓
           ├→ 子代理2 基本面評分  0.08秒 ↓
           ├→ 子代理3 套利計算    0.12秒 ↓
           ├→ 子代理4 風險檢查    0.15秒 ↓
           └→ 子代理5 執行決策    0.35秒

        ↓ 全部並行運行 ↓

妳 ← 主控彙整結果 0.35秒
```

---

## 第二部分：如何開啟 Ultracode？

### 方式 1️⃣：會話級啟用（整個對話使用）

```bash
/effort ultracode
```

執行後，所有後續的任務都會自動使用 xhigh 推理和動態工作流編排。

**適用場景**：
- 整個對話都涉及複雜分析（例如審計、對抗驗證、多維決策）
- 不希望每次任務都手動指定

### 方式 2️⃣：任務級啟用（單個任務）

在你的提示中包含 `ultracode` 關鍵字：

```
"我需要分析這份財報。請用ultracode方式生成五維評分系統。"
```

Claude 會自動為此任務啟動 Ultracode，不影響其他任務。

**適用場景**：
- 只有特定任務需要高深度分析
- 想要節省 Token 預算

### 方式 3️⃣：Workflow 文件級啟用（自動）

在 `.claude/workflows/` 目錄建立 JavaScript 工作流文件：

```javascript
export const meta = {
  name: 'security-audit',
  description: 'Multi-dimension security review',
  phases: [
    { title: 'Review' },
    { title: 'Verify' }
  ]
}

// 工作流體會自動使用 xhigh 推理 + 代理編排
phase('Review')
const findings = await agent('Audit auth checks...')
```

執行此工作流時，Ultracode 自動啟用。

**適用場景**：
- 複雜的持久化工作流（需要保存重複使用）
- 企業級多代理系統

### ⚠️ 重要限制

**只有 Opus 4.8+ 支持 xhigh 推理**。如果你使用：
- Sonnet 4.6 或更舊
- Opus 4.6 或更舊

設置 `/effort ultracode` 會**默默降級到 high 推理**，無法獲得 xhigh 的深度優勢。

---

## 第三部分：六大基本原語實戰教學

Ultracode 中有 6 個核心原語（函數）。掌握它們，你就掌握了整個系統。

### 1️⃣ agent(prompt, opts?)

生成**單一子代理**，返回最終文字或驗證後的 JSON。

```javascript
const result = await agent(
  'List every .ts file under src/routes/',
  {
    schema: {
      type: 'object',
      properties: {
        files: { type: 'array', items: { type: 'string' } }
      },
      required: ['files']
    },
    label: 'discover-files',      // 進度UI標籤
    phase: 'Discover',             // 進度儀表板分組
    model: 'claude-opus-4.8'       // 可選：覆寫模型
  }
)

console.log(result.files)  // ✅ 已驗證的文件列表
```

**Options 詳解**：
- `schema`：JSON Schema 用於驗證輸出（自動格式檢查）
- `label`：顯示在進度面板的子步驟名稱
- `phase`：進度儀表板的分組名稱
- `model`：覆寫該次呼叫的模型（不指定則用默認）
- `isolation: 'worktree'`：並行檔案寫入的隔離層

---

### 2️⃣ parallel(thunks)

**並列運行**陣列中的任務。是**同步屏障**——在每個代理都返回之前，其後面的代碼都不會運行。

```javascript
const reviews = await parallel([
  () => agent('Review for auth issues...', { label: 'auth-check' }),
  () => agent('Review for SQL injection...', { label: 'sql-check' }),
  () => agent('Review for CSRF vulnerabilities...', { label: 'csrf-check' })
])

// reviews = [result1, result2, result3]
// 全部完成後，才會繼續執行下一行代碼
```

**⚠️ 失敗處理**：

```javascript
const results = await parallel([...])
const valid = results.filter(Boolean)  // 失敗的 thunk 返回 null

console.log(`成功: ${valid.length}, 失敗: ${results.length - valid.length}`)
```

**何時使用 parallel()**：
- ✅ 需要所有結果都完成才能做決策（例如 5 維評分全部完成才能綜合）
- ✅ 結果之間有依賴關係（下一步需要所有上一步結果）
- ❌ 不適合流式處理（會產生延遲）

---

### 3️⃣ pipeline(items, ...stages)

**流式處理**陣列中的項目，通過一系列轉換階段。**無屏障** — item A 可以在 stage 3，而 item 7 仍在 stage 1。

```javascript
const audited = await pipeline(
  ['file1.ts', 'file2.ts', 'file3.ts'],  // 項目陣列

  // Stage 1：解析
  (file) => agent(`Parse ${file} for auth...`, {
    schema: {
      type: 'object',
      properties: {
        findings: { type: 'array' }
      }
    }
  }),

  // Stage 2：對每個 finding 做並行驗證
  (findings) => parallel(
    findings.issues.map(issue =>
      () => agent(`Verify: ${issue}`, {
        schema: {
          type: 'object',
          properties: {
            valid: { type: 'boolean' }
          }
        }
      })
    )
  )
)
```

**執行流程視覺化**：

```
Stage 1: file1 ✅ → Stage 2: file1 verify item1 ✅
Stage 1: file2 ✅ → Stage 2: file2 verify item1 ✅
                   → Stage 2: file2 verify item2 ✅
Stage 1: file3 ✅ → Stage 2: file3 verify item1 ✅
                   → Stage 2: file3 verify item2 ✅
                   → Stage 2: file3 verify item3 ✅
```

**何時使用 pipeline()**：
- ✅ 可以邊做邊轉換，不必等所有項目完成第一階段
- ✅ 低延遲需求（例如流式新聞解析）
- ✅ 處理大量項目（不想阻塞整個流程）
- ❌ 結果之間有強依賴（需要先 parallel）

---

### 4️⃣ phase(title)

為進度監控面板**命名分組**。幫助你在複雜工作流中追蹤進度。

```javascript
phase('Discovery')
const files = await agent('List all .ts files...')
log(`Found ${files.length} files`)

phase('Security Audit')
const findings = await pipeline(
  files,
  (file) => agent(`Audit ${file}...`)
)

phase('Verification')
const verified = await parallel(
  findings.map(f => () => agent(`Verify ${f.title}...`))
)
```

執行時的進度面板會顯示：
```
📊 進度
├─ Discovery
│  └─ ✅ Found 42 files
├─ Security Audit
│  └─ ⏳ Processing file 12/42...
└─ Verification
   └─ ⏳ Verifying 23 findings...
```

---

### 5️⃣ workflow(nameOrRef, args?)

呼叫**保存的工作流**作為子步驟（最多一級嵌套）。

```javascript
// 先前保存的工作流（檔案名：audit-routes.js）
export const meta = {
  name: 'audit-routes',
  description: 'Audit every route handler'
}

// 在另一個工作流中調用
const report = await workflow('audit-routes', {
  dir: 'src/api',
  severity: 'high'
})

console.log(report)  // 返回子工作流的最終結果
```

**適用場景**：
- ✅ 複用已驗證的工作流
- ✅ 大型系統的模組化編排
- ❌ 深層嵌套（超過 2 層會性能下降）

---

### 6️⃣ log(message)

記錄進度信息到日誌。

```javascript
log(`正在分析 ${count} 份財報`)
log(`發現 ${findings.length} 個異常值`)
log(`✅ 彙整完成，準備決策`)
```

輸出到進度面板和最終報告。

---

## 第四部分：parallel() vs pipeline() 決策樹

| 條件 | parallel() | pipeline() |
|------|-----------|-----------|
| **用途** | 全部結果需要可用後才繼續 | 流式處理，無屏障 |
| **例子** | 5維評分 + 6項風險檢查 全部完成 | 逐份財報→逐項目異常→逐項驗證 |
| **吞吐量** | 低（是屏障） | 高（無屏障） |
| **延遲** | 等待最慢的代理 | 低延遲 |
| **適合場景** | 金融決策（需要所有信息） | 實時監控（流式更新） |
| **Token消耗** | ~5k-50k 並行 | ~50k-200k 分批 |
| **並行度** | 最多 16 代理併發 | 最多 16 代理併發（但分階段） |

### 實戰對比代碼

**❌ 錯誤做法**（不用並行）：

```javascript
// 這樣需要 3 倍時間
const auth = await agent('Check auth...')
const sql = await agent('Check SQL...')
const csrf = await agent('Check CSRF...')
// 總耗時 ~= 3 × T
```

**✅ parallel() 做法**（金融決策）：

```javascript
const [auth, sql, csrf] = await parallel([
  () => agent('Check auth...'),
  () => agent('Check SQL...'),
  () => agent('Check CSRF...')
])
// 總耗時 ~= T（最慢的一個）
```

**✅ pipeline() 做法**（流式財報解析）：

```javascript
const reports = await pipeline(
  ['file1.xlsx', 'file2.xlsx', 'file3.xlsx'],
  (file) => agent(`Parse ${file}...`),
  (parsed) => agent(`Extract KPIs from ${parsed}...`)
)
// 流式運行，file1 進入 stage 2 時 file2 可能才在 stage 1
```

---

## 第五部分：完整實戰案例

### 案例 1️⃣：新聞獵手（#4 案例）

**場景**：彭博新聞發布，需在 0.15 秒內決策是否下單。

**架構**：流式五層
```
[11:47:00.00] 新聞發布
      ↓
[11:47:00.03] NLP 層：解析營收、毛利、指引
      ↓
[11:47:00.08] 評分層：六維評分（財報強度、趨勢、股價反應等）
      ↓
[11:47:00.12] 計算層：套利空間 2.36%
      ↓
[11:47:00.15] 決策層：風險檢查
      ↓
[11:47:00.35] 執行層：735 股成交
```

**完整工作流代碼**：

```javascript
export const meta = {
  name: 'news-hunter',
  description: 'Real-time news parsing and trading decision',
  phases: [
    { title: 'Parse' },
    { title: 'Score' },
    { title: 'Calculate' },
    { title: 'Execute' }
  ]
}

// 接收新聞文本
const newsText = `...彭博新聞內容...`

phase('Parse')
const parsed = await agent(
  `Extract financial data from news: ${newsText}`,
  {
    schema: {
      type: 'object',
      properties: {
        revenue: { type: 'string' },
        eps: { type: 'string' },
        guidance: { type: 'string' },
        sentiment: { enum: ['positive', 'negative', 'neutral'] }
      },
      required: ['revenue', 'eps', 'sentiment']
    },
    label: 'nlp-parse'
  }
)

phase('Score')
const scoring = await parallel([
  () => agent('Score financial strength (1-10)...', {
    label: 'strength-score',
    schema: { type: 'object', properties: { score: { type: 'number' } } }
  }),
  () => agent('Score trend consistency (1-10)...', {
    label: 'trend-score',
    schema: { type: 'object', properties: { score: { type: 'number' } } }
  }),
  () => agent('Score price reaction probability (1-10)...', {
    label: 'reaction-score',
    schema: { type: 'object', properties: { score: { type: 'number' } } }
  }),
  () => agent('Score catalyst strength (1-10)...', {
    label: 'catalyst-score',
    schema: { type: 'object', properties: { score: { type: 'number' } } }
  }),
  () => agent('Score risk assessment (1-10)...', {
    label: 'risk-score',
    schema: { type: 'object', properties: { score: { type: 'number' } } }
  }),
  () => agent('Score follow-up probability (1-10)...', {
    label: 'followup-score',
    schema: { type: 'object', properties: { score: { type: 'number' } } }
  })
])

const avgScore = scoring.reduce((a, b) => a + b.score, 0) / scoring.length
log(`📊 綜合評分: ${avgScore.toFixed(1)}/10`)

if (avgScore < 7) {
  log(`❌ 評分不足，取消交易`)
  return { decision: 'skip', reason: 'Low score' }
}

phase('Calculate')
const priceData = await agent(
  'Current price, technical target, execution cost...',
  {
    schema: {
      type: 'object',
      properties: {
        currentPrice: { type: 'number' },
        targetPrice: { type: 'number' },
        profitTarget: { type: 'number' }  // %
      }
    }
  }
)

const profitAfterCosts = priceData.profitTarget - 0.14  // 佣金 + 融資 + 滑點
log(`💰 淨利潤: ${profitAfterCosts.toFixed(2)}%`)

if (profitAfterCosts < 0.8) {
  log(`❌ 利潤空間不足，取消交易`)
  return { decision: 'skip', reason: 'Insufficient profit' }
}

phase('Execute')
const execution = await parallel([
  () => agent('Calculate optimal position size...', {
    schema: { type: 'object', properties: { shares: { type: 'number' } } }
  }),
  () => agent('Check portfolio concentration...', {
    schema: { type: 'object', properties: { ok: { type: 'boolean' } } }
  }),
  () => agent('Check available cash...', {
    schema: { type: 'object', properties: { available: { type: 'number' } } }
  }),
  () => agent('Check leverage limits...', {
    schema: { type: 'object', properties: { ok: { type: 'boolean' } } }
  })
])

const position = execution[0].shares
log(`✅ 建倉 ${position} 股 @ $${priceData.currentPrice}`)

return {
  decision: 'buy',
  shares: position,
  entryPrice: priceData.currentPrice,
  targetPrice: priceData.targetPrice,
  expectedProfit: profitAfterCosts,
  executedAt: new Date().toISOString()
}
```

**實際執行時間**：0.35 秒（包括 Parse + Scoring + Calculate + Execute）

**對比普通方式**：需要 45-60 秒（人工讀、理解、決策）

---

### 案例 2️⃣：五信號驗證（混合 parallel + pipeline）

**場景**：對抗驗證 #1-#4 篇的交易信號。

**架構**：先並行 5 維驗證，再流式對抗檢驗

```javascript
export const meta = {
  name: 'five-signal-verification',
  description: 'Adversarial verification of trading signals',
  phases: [
    { title: 'Signal Review' },
    { title: 'Adversarial Check' }
  ]
}

const signals = [
  { name: 'Real-time Monitoring', signal: '...' },
  { name: '3D Hunting', signal: '...' },
  { name: 'Auto Rebalance', signal: '...' },
  { name: 'News Hunter', signal: '...' },
  { name: 'Cross-border Snipe', signal: '...' }
]

phase('Signal Review')
const reviews = await pipeline(
  signals,
  (s) => agent(`Deep review "${s.name}": ${s.signal}`, {
    label: `review-${s.name}`,
    schema: {
      type: 'object',
      properties: {
        validity: { type: 'number', minimum: 0, maximum: 10 },
        risks: { type: 'array', items: { type: 'string' } },
        recommendations: { type: 'array', items: { type: 'string' } }
      }
    }
  }),

  // 第二階段：對每個 risk 做並行對抗驗證
  (review) => parallel(
    review.risks.map(risk =>
      () => agent(`Adversarially verify: "${risk}"`, {
        schema: {
          type: 'object',
          properties: {
            confirmed: { type: 'boolean' },
            severity: { enum: ['low', 'medium', 'high'] },
            mitigation: { type: 'string' }
          }
        }
      })
    )
  )
)

log(`✅ 五信號驗證完成，${reviews.length} 層風險已確認`)

return {
  verified: reviews.length,
  timestamp: new Date().toISOString()
}
```

---

## 第六部分：何時該用、何時不該用

### ✅ 適合 Ultracode 的場景

- **平行探索**：多維度同時分析（5 維評分、6 項風險檢查）
- **審計覆蓋**：需要遍歷所有代碼路徑或數據點
- **對抗驗證**：需要多角度質疑同一結論
- **毫秒級決策**：金融、安全監控需要快速響應
- **複雜工作流**：涉及 3+ 層依賴關係，普通方式難以管理

**典型 Token 消耗**：50k - 1M tokens

### ❌ 不適合 Ultracode 的場景

- **單檔編輯**：只改一個文件，用不著多代理
- **快速問答**：「Claude 是誰？」—— 直接問就行
- **機械重構**：單純的查找替換、重命名變數
- **預算緊張**：沒有 10 倍 Token 預算的空間
- **原型探索**：早期想法驗證，不需要企業級精度

**典型 Token 消耗**：0.5k - 5k tokens（用普通方式更經濟）

### 決策樹

```
📊 我需要做什麼？
  │
  ├─ 「快速問個問題」
  │   └─ ❌ 不用 Ultracode，直接問
  │
  ├─ 「分析一份文件」
  │   ├─ 「需要 5+ 維度同時分析」
  │   │   └─ ✅ 用 Ultracode
  │   └─ 「只需要 1-2 維度」
  │       └─ ❌ 用普通 Claude
  │
  ├─ 「做一個決策」
  │   ├─ 「時間要求 < 1 秒」
  │   │   └─ ✅ 用 Ultracode
  │   └─ 「時間要求 > 10 秒，人工綜合沒問題」
  │       └─ ❌ 用 L1.5（多 session）
  │
  └─ 「建立持久化工作流」
      └─ ✅ 用 Ultracode + Workflow 文件
```

---

## 第七部分：Token 成本估算

### 成本層級

| 使用方式 | 單次 Token | 場景 |
|---------|----------|------|
| 普通提問 | 0.5k - 2k | 簡單問題 |
| 普通分析（L1） | 2k - 10k | 單份文檔 |
| L1.5（多 session） | 5k - 50k | 3+ 代理獨立分析 |
| **L2（Ultracode）** | **50k - 300k** | **複雜決策 + 主控彙整** |
| **L3（Ultracode 工廠）** | **500k - 2M** | **持久化工作流 + 對抗審查** |

### 成本控制技巧

**💡 技巧 1：混用模型**

```javascript
// 輕量級查詢用 Haiku（便宜）
const quick = await agent('List files...', {
  model: 'claude-haiku-4-5'  // 便宜 10 倍
})

// 重量級決策用 Opus（貴但精確）
const decision = await agent('Make final decision...', {
  model: 'claude-opus-4.8'   // 貴但 xhigh 推理
})
```

**💡 技巧 2：pipeline 比 parallel 省錢**

```javascript
// ❌ 昂貴（所有項目全部並行）
const results = await parallel(
  items.map(i => () => agent(`Process ${i}...`))
)  // Token ~= N × T（N 是項目數）

// ✅ 便宜（分批流式）
const results = await pipeline(
  items,
  (i) => agent(`Process ${i}...`)
)  // Token ~= T（無論多少項目）
```

**💡 技巧 3：縮小 schema 範圍**

```javascript
// ❌ 大 schema（強制詳細輸出）
const result = await agent('...', {
  schema: {
    type: 'object',
    properties: {
      analysis: { type: 'string' },  // 可能生成 1000 字
      detail: { type: 'string' },    // 可能生成 2000 字
      ...10 more fields
    }
  }
})  // Token ~= 15k-30k

// ✅ 小 schema（只要關鍵數據）
const result = await agent('...', {
  schema: {
    type: 'object',
    properties: {
      decision: { enum: ['buy', 'sell', 'hold'] },
      confidence: { type: 'number' }
    }
  }
})  // Token ~= 2k-5k
```

---

## 第八部分：實際操作步驟

### 步驟 1️⃣：開啟 Ultracode

選擇以下任一方式：

**會話級**（推薦用於整個工作流項目）：
```
/effort ultracode
```

**任務級**（推薦用於單個高複雜度任務）：
```
"請用ultracode方式分析這份財報，生成五維評分。"
```

### 步驟 2️⃣：給出詳細任務

包括：
- ✅ 目標明確（不要「分析一下」，要「分析營收、利潤、指引三個維度」）
- ✅ 輸出格式（schema 或範本）
- ✅ 時間限制（如果有）
- ✅ 決策標準（什麼情況下買/賣/持）

**例子**：
```
我需要在 1 秒內決策是否買入 NVIDIA。

請用 ultracode 並行做以下：
1. 解析最新新聞（營收、利潤、指引）
2. 計算 6 維評分（財報強度、趨勢、反應度、催化劑、風險、後續概率）
3. 計算套利空間（成本 0.14%，目標收益 2.36% 以上為可執行）
4. 風險檢查（集中度、融資、時機）
5. 下單決策（成交價、數量）

給我最終決策：買/不買。
```

### 步驟 3️⃣：監看進度面板

執行中會看到：

```
📊 進度
├─ Parse
│  └─ ⏳ Parsing news... 0.03秒
├─ Score
│  ├─ ✅ Strength score: 9/10
│  ├─ ✅ Trend score: 9/10
│  ├─ ⏳ Reaction score...
│  ├─ ⏳ Catalyst score...
│  └─ ⏳ Risk score...
├─ Calculate
│  └─ ⏳ Computing profit after costs...
└─ Execute
   └─ ⏳ Risk checks...
```

### 步驟 4️⃣：收到結果

Ultracode 會返回：
- ✅ 最終決策（買/賣/持）
- ✅ 執行細節（數量、進價、目標）
- ✅ 風險評估
- ✅ 信心度
- ✅ 執行時間戳

```json
{
  "decision": "buy",
  "shares": 735,
  "entryPrice": 245.37,
  "targetPrice": 251.50,
  "expectedProfit": "2.36%",
  "riskLevel": "low",
  "confidence": 0.92,
  "executedAt": "2026-07-09T11:47:00.35Z"
}
```

---

## 第九部分：保存 Workflow 到 Claude Code

### 步驟 1️⃣：建立 .js 文件

在 `.claude/workflows/` 目錄建立檔案，例如：

```bash
.claude/workflows/swarm-04-news-hunter.js
```

### 步驟 2️⃣：定義 meta 塊

```javascript
export const meta = {
  name: 'news-hunter',
  description: 'Real-time news parsing and trading decision in <0.5 seconds',
  phases: [
    { title: 'Parse' },
    { title: 'Score' },
    { title: 'Calculate' },
    { title: 'Execute' }
  ]
}
```

### 步驟 3️⃣：撰寫工作流體

```javascript
// 接在 meta 塊後
const newsText = newsInput  // 從外部傳入

phase('Parse')
const parsed = await agent(
  `Extract financial data from news: ${newsText}`,
  { schema: {...} }
)

phase('Score')
const scores = await parallel([
  () => agent('Score strength...'),
  () => agent('Score trend...'),
  ...
])

// ... 繼續工作流
```

### 步驟 4️⃣：觸發工作流

在 Claude Code 會話中：

```javascript
const result = await workflow('news-hunter', {
  newsText: '彭博新聞：NVIDIA 營收超預期...'
})
```

或命令行：

```bash
claude code --workflow news-hunter
```

---

## 第十部分：調試技巧

### 問題 1️⃣：Ultracode 沒啟動

**症狀**：執行 `/effort ultracode` 後，代理仍然逐步執行，沒有並行。

**原因**：
- ❌ 使用了舊模型（Sonnet 4.6, Opus 4.6）
- ❌ 任務太簡單，Claude 判斷用不著 Ultracode
- ❌ 沒有明確告訴 Claude 需要並行（例如沒有 `parallel()` 呼叫）

**解決方案**：

```javascript
// ✅ 明確要求並行
const [a, b, c, d, e, f] = await parallel([
  () => agent('Task 1...'),
  () => agent('Task 2...'),
  ...
])
```

或在提示中強調：

```
"用ultracode並行做以下6項任務..."
```

### 問題 2️⃣：Token 超支

**症狀**：一次工作流消耗了 500k tokens，賬單爆炸。

**原因**：
- ❌ 用 `parallel()` 並行了太多代理（超過 16 個）
- ❌ 用了太大的 schema（生成大量文字）
- ❌ 對同一對象做了多層對抗驗證

**解決方案**：

```javascript
// ❌ 並行 30 個代理
await parallel(items.map(i => () => agent(`Process ${i}...`)))

// ✅ 分批並行（16 個為限）
const batch1 = await parallel(items.slice(0, 16).map(...))
const batch2 = await parallel(items.slice(16, 32).map(...))

// ✅ 或改用 pipeline（流式，省 Token）
await pipeline(items, (i) => agent(`Process ${i}...`))
```

### 問題 3️⃣：結果不一致

**症狀**：同一個工作流執行两次，結果不同。

**原因**：
- ❌ Workflows.js 中有非確定性函數（例如 `Math.random()`）
- ❌ 代理之間有相互依賴，但沒用屏障

**解決方案**：

```javascript
// ❌ 不確定
const random = Math.random()

// ✅ 確定
const seed = 42
const pseudo = seed * 1103515245 + 12345  // 偽隨機但確定

// ✅ 確保依賴關係用屏障
const [first, second] = await parallel([
  () => agent('Do A...'),
  () => agent('Do B...', { depends: 'result of A' })  // ❌ 錯誤

// ✅ 改成序列
const first = await agent('Do A...')
const second = await agent(`Do B... (given A = ${first})...`)
```

---

## 快速速查表

| 需求 | 命令 |
|------|------|
| 啟用 Ultracode | `/effort ultracode` |
| 並列 5 個任務 | `await parallel([...])` |
| 流式處理 100 份文件 | `await pipeline(files, ...)` |
| 標記進度分組 | `phase('Step Name')` |
| 保存工作流 | `.claude/workflows/name.js` |
| 呼叫子工作流 | `await workflow('name', args)` |
| 記錄進度 | `log('message')` |

---

## 與《新聞獵手》的對應

#4 正文的**五層架構**就是 Ultracode 會自動生成的結構：

```
新聞發布 [0.00s]
    ↓ (主控派遣 5 層班組並行)
    ├─ Layer 1: 新聞接收器 [0.01s]        ← agent() 接收輸入
    ├─ Layer 2: NLP 解析 [0.03s]          ← agent(parsing schema)
    ├─ Layer 3: 6 維評分 [0.08s]          ← parallel(6 dimensions)
    ├─ Layer 4: 套利計算 [0.12s]          ← agent(arbitrage schema)
    └─ Layer 5: 決策+執行 [0.35s]         ← parallel(validation) + execute
        ↓
妳才讀完新聞第二段，蜂群已建倉
```

**代碼對應**：見本文第五部分「案例 1️⃣：新聞獵手」

---

## 延伸資源

**官方文檔**：
- Ultracode 核心定義：`技術架構/ultracode核心定義.md`
- Workflows.js 語法規範：`技術架構/workflows_js_語法規範.md`

**系列對應**：
- 《新聞獵手》正文：`SWARM_S01E04_新聞獵手_正文.md`
- 《自動校準》實戰案例：`SWARM_S01E03_自動校準_正文.md`

**實戰項目**：
- GitHub 武器庫：[ai-swarm-investing](https://github.com/)
- 核心工作流代碼：`workflows/swarm-04-news-hunter.js`

---

**作者**：克勞德
**最後更新**：2026-07-09
**版本**：v1.0.0

*準備好用 Ultracode 狩獵了嗎？*
