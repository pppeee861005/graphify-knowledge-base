讓我給你完整的 ultracode workflows.js 語法規範：
核心語法結構
每個保存的工作流文件在 .claude/workflows/ 包含一個 meta 塊，後跟編排子代理的腳本體： Claude Code Docs
javascriptexport const meta = {
  name: 'audit-routes',
  description: 'Audit every route handler for missing auth checks',
  phases: [{ title: 'Discover' }, { title: 'Audit' }],
}

// 腳本內容...
六大基本原語
1️⃣ agent(prompt, opts?)
生成一個單一子代理，返回最終文字或驗證的 JSON Build This Now
javascriptconst result = await agent(
  'List every .ts file under src/routes/',
  {
    schema: {
      type: 'object',
      properties: {
        files: { type: 'array', items: { type: 'string' } }
      },
      required: ['files']
    },
    label: 'discover-files',
    phase: 'Discover',
    model: 'claude-opus-4.8'  // 可選：覆寫模型
  }
)
Options:

schema - JSON Schema for validated structured output
label - Progress UI 標籤
phase - 進度儀表板分組
model - 覆寫該次呼叫的模型
isolation: 'worktree' - 並行檔案寫入的隔離

2️⃣ parallel(thunks)
並列運行陣列中的任務，是同步屏障——在每個代理返回之前，其後面的代碼都不會運行 GitHub
javascriptconst reviews = await parallel([
  () => agent('Review for auth issues...'),
  () => agent('Review for SQL injection...'),
  () => agent('Review for CSRF vulnerabilities...')
])
// reviews = [result1, result2, result3]
⚠️ 失敗的 thunk 返回 null，所以要 filter：
javascriptconst results = await parallel([...])
const valid = results.filter(Boolean)
3️⃣ pipeline(items, ...stages)
處理陣列的項目通過轉換階段序列，無屏障：item A 可以在 stage 3，而 item 7 仍在 stage 1 GitHub
javascriptconst audited = await pipeline(
  files,  // 要處理的項目
  (file) => agent(`Audit ${file} for auth...`, { schema: FINDINGS }),
  (findings) => parallel(
    findings.issues.map(issue => 
      () => agent(`Verify: ${issue}`, { schema: VERDICT })
    )
  )
)
4️⃣ phase(title)
命名進度監控組
javascriptphase('Discovery')
const files = await agent('List files...')

phase('Audit')
const results = await pipeline(files, ...)
5️⃣ workflow(nameOrRef, args?)
調用保存的工作流作為子步驟（最多一級嵌套） Build This Now
javascriptconst report = await workflow('audit-routes', { dir: 'src/api' })
6️⃣ log()
記錄進度信息
javascriptlog(`Processed ${count} files`)

實戰例：安全審計工作流
javascriptexport const meta = {
  name: 'security-audit',
  description: 'Multi-dimension security review with adversarial verification',
  phases: [
    { title: 'Review' },
    { title: 'Verify' }
  ]
}

const FINDINGS = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          title: { type: 'string' },
          file: { type: 'string' },
          severity: { enum: ['low', 'medium', 'high', 'critical'] }
        },
        required: ['title', 'file']
      }
    }
  },
  required: ['findings']
}

const DIMENSIONS = [
  { key: 'auth', prompt: 'Find authentication bypasses...' },
  { key: 'secrets', prompt: 'Find hardcoded secrets...' },
  { key: 'ssrf', prompt: 'Find SSRF vulnerabilities...' }
]

phase('Review')
const findings = await pipeline(
  DIMENSIONS,
  (d) => agent(`Security review (${d.key}): ${d.prompt}`, {
    label: `review:${d.key}`,
    phase: 'Review',
    schema: FINDINGS
  }),
  (review) => parallel(
    (review?.findings || []).map((f) => 
      () => agent(`Adversarially verify: ${f.title}`, {
        phase: 'Verify',
        schema: { type: 'object', properties: { valid: { type: 'boolean' } } }
      })
    )
  )
)

return {
  confirmed: findings.flat().filter(f => f.valid)
}

關鍵限制
⚠️ 純 JavaScript，無 TypeScript：TypeScript 註解會導致解析錯誤 byteiota
⚠️ 確定性：運行時記錄調用以確保確定性恢復，這意味著非確定性函數在腳本內會拋出 Developers Digest
✅ 並行上限：最多 16 個併發代理，1000 個總代理每次運行
✅ 費用：動態工作流消費明顯更多令牌，大規模 Opus 4.8 運行可能使賬單增加一個數量級 Tech Times

何時用 parallel() vs pipeline()
parallel()pipeline()用途全部結果需要可用後才繼續流式處理，無屏障例子合成跨所有發現、重複數據刪除批量處理、順序轉換吞吐量低（是屏障）高（無屏障）
這就是你的「Agentic Crucible」自鑄熔爐——Claude 用 JS 動態編排蜂群！適合你的 stock-swarm-wf 架構進化嗎？