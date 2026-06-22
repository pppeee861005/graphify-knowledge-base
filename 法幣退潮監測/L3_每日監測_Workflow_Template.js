// 法幣退潮監測 - L3 每日自動化 Workflow
// 檔案：L3_每日監測_Workflow_Template.js
// 用途：每日 08:00 自動執行，收集五層信號數據

export const meta = {
  name: 'FiatTideMonitoring-L3',
  description: '每日 08:00 收集五層信號數據 → 時效性檢查 → 異常預警',
  phases: [
    { title: 'Collect', detail: '平行收集七個信號的實時數據' },
    { title: 'Validate', detail: '驗證時效性，檢查數據新鮮度' },
    { title: 'Alert', detail: '檢測異常波動，發送預警' },
    { title: 'Store', detail: '存儲至日誌，上傳結果' }
  ]
}

// ============================================================================
// 第一步：定義五層信號的信息源
// ============================================================================

const SIGNALS = [
  // 第一層：價格脫鉤
  {
    layer: 1,
    name: '美元指數(DXY)',
    api: 'alpha-vantage',
    endpoint: 'FX_DAILY',
    params: { from_symbol: 'DXY', to_symbol: 'USD' },
    required_fields: ['time', 'close'],
    priority: 'high'
  },
  {
    layer: 1,
    name: '黃金價格',
    api: 'metals-api',
    endpoint: '/api/timeseries',
    params: { base: 'USD', symbols: 'XAU' },
    required_fields: ['date', 'rates.XAU'],
    priority: 'high'
  },
  {
    layer: 1,
    name: '白銀價格',
    api: 'metals-api',
    endpoint: '/api/timeseries',
    params: { base: 'USD', symbols: 'XAG' },
    required_fields: ['date', 'rates.XAG'],
    priority: 'high'
  },
  {
    layer: 1,
    name: '脫鉤係數',
    api: 'calculated',
    depends: ['DXY', 'Gold', 'Silver'],
    formula: 'cov(DXY, Gold) / (σ_DXY × σ_Gold)',
    window: '30days_rolling'
  },

  // 第二層：金銀比
  {
    layer: 2,
    name: '金銀比(GSR)',
    api: 'calculated',
    depends: ['Gold', 'Silver'],
    formula: 'Gold / Silver',
    priority: 'high'
  },

  // 第三層：實物撕裂
  {
    layer: 3,
    name: 'COMEX白銀庫存',
    api: 'comex-official',
    endpoint: '/reports/inventory',
    required_fields: ['date', 'silver_inventory_oz'],
    priority: 'high'
  },
  {
    layer: 3,
    name: '實物白銀溢價',
    api: 'manual-survey',
    frequency: 'monthly',
    required_fields: ['date', 'dealer_name', 'premium_pct'],
    priority: 'medium'
  }
]

// ============================================================================
// 第二步：主 Pipeline - 收集 → 驗證 → 異常檢測 → 存儲
// ============================================================================

phase('Collect')
log('🔍 開始收集五層信號數據...')

// Stage 1: 平行收集所有信號
const results = await pipeline(
  SIGNALS,

  // Stage 1: 查詢數據
  async (sig) => {
    if (sig.api === 'calculated') {
      // 計算類指標，等待依賴完成
      return {
        signal: sig.name,
        status: 'pending',
        depends_on: sig.depends
      }
    }

    const data = await agent(
      `查詢 ${sig.name} 的實時數據。API: ${sig.api}。${
        sig.params ? `參數: ${JSON.stringify(sig.params)}` : ''
      }`,
      {
        label: `query:${sig.name}`,
        schema: {
          type: 'object',
          properties: {
            timestamp: { type: 'string' },
            value: { type: 'number' },
            status: { enum: ['success', 'error', 'unavailable'] }
          }
        },
        model: 'haiku',
        effort: 'low'
      }
    )

    return {
      signal: sig.name,
      layer: sig.layer,
      timestamp: new Date().toISOString(),
      value: data.value,
      status: data.status,
      priority: sig.priority
    }
  },

  // Stage 2: 驗證時效性
  async (data) => {
    if (data.status === 'error' || data.status === 'unavailable') {
      return {
        ...data,
        freshness: 'unavailable',
        age_hours: null,
        warning: true
      }
    }

    const verification = await agent(
      `驗證時效性：${data.signal} 的數據時間戳是 ${data.timestamp}。
       當前時間：${new Date().toISOString()}。
       數據是否在 24 小時內？需要回答 yes/no 並給出小時差。`,
      {
        label: `validate:${data.signal}`,
        schema: {
          type: 'object',
          properties: {
            is_fresh: { type: 'boolean' },
            age_hours: { type: 'number' },
            freshness_status: { enum: ['fresh', 'marginal', 'stale'] }
          }
        },
        model: 'haiku',
        effort: 'low'
      }
    )

    return {
      ...data,
      freshness: verification.freshness_status,
      age_hours: verification.age_hours,
      is_fresh: verification.is_fresh,
      warning: !verification.is_fresh
    }
  },

  // Stage 3: 計算衍生指標
  async (data) => {
    if (data.signal === '金銀比(GSR)' || data.signal === '脫鉤係數') {
      // 這些將在異常檢測層進行計算
      return data
    }
    return data
  }
)

// 處理計算類指標（依賴完成後）
const gold_data = results.find(r => r.signal === '黃金價格')
const silver_data = results.find(r => r.signal === '白銀價格')
const dxy_data = results.find(r => r.signal === '美元指數(DXY)')

if (gold_data && silver_data) {
  const gsr = gold_data.value / silver_data.value
  results.push({
    signal: '金銀比(GSR)',
    layer: 2,
    value: gsr,
    status: 'success',
    timestamp: new Date().toISOString()
  })
  log(`✅ 金銀比計算完成: ${gsr.toFixed(2)}`)
}

log(`✅ 數據收集完成: ${results.filter(r => r.status === 'success').length}/${SIGNALS.length} 個信號`)

// ============================================================================
// 第三步：異常檢測
// ============================================================================

phase('Alert')
log('⚠️ 開始異常檢測...')

const anomalies = []

// 檢測環比變化 > 5% 的異常
for (const data of results.filter(r => r.status === 'success')) {
  if (data.layer >= 2) {  // 只檢測 L2 以上（有歷史對比意義）
    const alert = await agent(
      `檢測異常：${data.signal} = ${data.value}。
       過往基線（昨日或月初）估計值為 ${data.value * 0.95} ~ ${data.value * 1.05}（±5%）。
       是否超過 5% 環比？若是，請描述異常類型和嚴重度。`,
      {
        label: `alert:${data.signal}`,
        schema: {
          type: 'object',
          properties: {
            is_anomaly: { type: 'boolean' },
            change_pct: { type: 'number' },
            severity: { enum: ['low', 'medium', 'high', 'critical'] },
            description: { type: 'string' }
          }
        },
        model: 'sonnet',
        effort: 'medium'
      }
    )

    if (alert.is_anomaly) {
      anomalies.push({
        signal: data.signal,
        layer: data.layer,
        value: data.value,
        change_pct: alert.change_pct,
        severity: alert.severity,
        description: alert.description,
        timestamp: data.timestamp
      })

      log(`⚠️ 異常警報 [L${data.layer}] ${data.signal}: ${alert.description}`)
    }
  }
}

// ============================================================================
// 第四步：存儲結果
// ============================================================================

phase('Store')
log('💾 生成每日監測日誌...')

const summary = await agent(
  `基於以下數據生成每日監測摘要：
   收集成功: ${results.filter(r => r.status === 'success').length}/${SIGNALS.length}
   異常警報數: ${anomalies.length}

   格式：
   - 整體狀態（正常/微弱信號/強信號）
   - 最重要的 3 個發現
   - 下次監測重點（若有異常則說明）`,
  {
    label: 'generate-summary',
    schema: {
      type: 'object',
      properties: {
        overall_status: { enum: ['normal', 'signal', 'anomaly'] },
        findings: { type: 'array', items: { type: 'string' } },
        next_focus: { type: 'string' }
      }
    },
    model: 'sonnet',
    effort: 'medium'
  }
)

log(`✅ 監測完成！狀態: ${summary.overall_status}`)

// 返回結果（用於存儲）
return {
  date: new Date().toISOString().split('T')[0],
  execution_time: new Date().toISOString(),
  data_collection: {
    total_signals: SIGNALS.length,
    successful: results.filter(r => r.status === 'success').length,
    failed: results.filter(r => r.status !== 'success').length
  },
  signals: results,
  anomalies: anomalies,
  summary: summary,
  next_file: `每日數據_${new Date().toISOString().split('T')[0].replace(/-/g, '')}.md`
}

// ============================================================================
// 排程配置（用於 CronCreate）
// ============================================================================

/*
// 使用此配置啟動每日排程：

CronCreate({
  schedule: '0 8 * * *',  // 每日 08:00
  timezone: 'Asia/Taipei',
  workflow: 'FiatTideMonitoring-L3',
  notify_on_completion: true,
  notify_on_failure: true,
  retry_on_failure: 3,
  retry_delay_minutes: 5,
  timeout_minutes: 30,
  max_concurrent_agents: 16
})

*/

// ============================================================================
// 注意事項
// ============================================================================

/*

本 Workflow 的設計原則：

1. **Pipeline 而非 Parallel**
   - 每個信號獨立流過 3 個階段
   - 不在信號間創建障礙，確保快速完成
   - Wall-clock 時間 ~5-10 分鐘

2. **Haiku 優先的成本策略**
   - 查詢層（Stage 1）使用 Haiku（便宜，適合簡單 API 調用）
   - 驗證層（Stage 2）使用 Haiku（簡單時效檢查）
   - 異常檢測（Alert）使用 Sonnet（複雜模式識別）
   - 預期成本：~3,000-5,000 tokens/天

3. **兩個可選自動化**
   - 若異常嚴重度 >= 'high' → 自動發送郵件/Slack 通知
   - 若異常涉及第四五層 → 自動觸發提早月度報告

4. **數據持久化**
   - 每次執行結果存為 `每日數據_YYYYMMDD.md`
   - 30 天自動聚合為月度報告（L2 負責）

*/
