export const meta = {
  name: 'PSA E01 爆文完整寫作流程',
  description: '個人時尚助理系列 E01 - 從規劃到發布的完整 6 大任務系統',
  phases: [
    { title: '規劃期', detail: 'Task 1：確認 E01 的系列定位與讀者' },
    { title: '大綱期', detail: 'Task 2：設計標題、副標題、5 層綱要' },
    { title: '成稿期', detail: 'Task 3：完成初稿、精簡、配圖' },
    { title: '審核期', detail: 'Task 4：7 層自檢 + 5 大元素評分' },
    { title: '發布期', detail: 'Task 5：Substack 後台設定 + 社團推廣' },
    { title: '複盤期', detail: 'Task 6：績效監測 + 改進方案' },
  ],
}

phase('規劃期')
log('Task 1：PSA E01 的規劃期開始')

const psa_planning = await agent(
  `你是個人時尚助理系列的內容策略顧問。為 PSA E01《穿衣焦慮的終結：為什麼 AI Agent 會成為你的衣櫃管理員》完成規劃期。

【背景信息】
- 系列定位：個人時尚助理系列（PSA），共 6 集
- E01 角色：破冰篇 | 問題定位 | 吸引非技術讀者
- 目標讀者：忙碌的知識工作者（25-45 歲），效率追求者
- 核心洞察：日常穿衣決策本質上是『受約束條件下的優化問題』

【執行步驟】

Step 1.1：確認 E01 的系列大定位（15 分鐘）
- 這個系列要解決什麼問題？→ 穿衣焦慮 + 決策優化
- E01-E06 的完整鏈條？→ 破冰→功能→深化→架構→社區→商業
- 最終讀者會獲得什麼能力？→ 從『穿衣焦慮』到『決策自信』
- 商業目標？→ 驗證時尚+AI 應用的商業可行性

Step 1.2：E01 的單篇差異化規劃（20 分鐘）
確認 E01 的定位：
- 篇次：E01
- 定位：破冰篇 | 問題定位 | 吸引非技術讀者
- 讀者痛點：每天早晨的穿衣決策耗時費力；社交場景下衣著搭配焦慮；購物決策無據可依
- 核心觀點：穿衣決策 = 優化問題，AI Agent 擅長解決
- 轉折點：從『穿衣是審美』反轉到『穿衣是決策優化』

Step 1.3：目標讀者精化（15 分鐘）
主要讀者：
  - 身份：忙碌的知識工作者、效率追求者
  - 痛點：每天浪費 10-15 分鐘在穿衣決策上
  - 知識水位：不懂技術，但關注生活效率
  - 預期動作：讀完後想「嘗試 Agent 衣櫃管理」

次要讀者：
  - 身份：AI 應用開發者、Agent 架構設計者
  - 為什麼也會讀：時尚是 Agent 應用的完美案例

反面讀者（排除）：
  - 身份：純粹時尚愛好者、審美導向讀者
  - 為什麼不適合：E01 重點是決策優化而非時尚美學

Step 1.4：預期轉化率預測（10 分鐘）
基於系列定位預測：
- 內容定位命中度：95%（破冰篇，問題清晰）
- 標題點擊率：35-40%（對比詞清晰）
- 讀者完讀率：75-80%（破冰篇，相對輕量）
- 訂閱轉化率：2-4%（首篇通常較低，但有系列吸引力）

轉化率預期：
- 低估：1.5% | 目標：2.5% | 樂觀：4%

Step 1.5：發布時間和社團規劃（10 分鐘）
發布週期：2026-06-05 至 2026-06-10（E01 破冰篇）
Substack 發布時間：美東 10:00 AM EDT
社團發布：PM 6:00（該社團當地時間）

目標社團（高相關性）：
- 核心社團（必發）：
  1. 效率工作者社團（AI+生活黑客）
  2. Agent 應用開發社團
  3. Substack 中文科技社團
- 補充社團：
  4. AI 創新應用社團
  5. 生活優化社團

預期數據：
- Substack 新訂：8-15 人（破冰篇首發）
- 社團轉化：5-10 人
- 總新訂：13-25 人

【Task 1 輸出】JSON 格式包含：系列定位 + 單篇規劃 + 讀者定位 + 轉化率預測 + 發布計劃 + 完成檢查清單`,
  {
    label: 'PSA E01 規劃專家',
    phase: '規劃期',
    schema: {
      type: 'object',
      properties: {
        seriesFocus: { type: 'string' },
        e01_positioning: { type: 'object' },
        targetAudience: { type: 'object' },
        conversionRatePrediction: { type: 'object' },
        publicationPlan: { type: 'object' },
        checklist: { type: 'array' },
      },
    },
  }
)

phase('大綱期')
log('Task 2：PSA E01 的大綱期開始')

const psa_outline = await agent(
  `基於 PSA E01 的規劃輸出，完成大綱期的 3 個步驟。

【背景】
- E01 標題提案：穿衣焦慮的終結：為什麼 AI Agent 會成為你的衣櫃管理員
- E01 核心問題：穿衣決策是優化問題，不是審美問題
- 目標讀者：忙碌的知識工作者，25-45 歲，效率追求者

【Step 2.1】標題 3 版本競爭（1 小時）

版本 A（對比式）：
「[舊做法] vs [新做法]：[讀者利益]」
示例模板：「每天花 15 分鐘穿衣 vs AI Agent 一鍵推薦：如何用 AI 化解穿衣焦慮」

版本 B（問題式）：
「[讀者的真實問題]？你可能需要 [解決方案]」
示例模板：「每天都在穿什麼而焦慮？你可能需要一個 AI 衣櫃管理員」

版本 C（成果式）：
「[工具/方法] 如何帶來 [具體成果]」
示例模板：「AI Agent 如何終結你的穿衣焦慮：從決策困境到自信穿衣」

評分對標（8-12 字，有對比詞和具體化）：
- 版本 A：字數、對比詞✓/✗、具體化✓/✗ → 評分：
- 版本 B：字數、對比詞✓/✗、具體化✓/✗ → 評分：
- 版本 C：字數、對比詞✓/✗、具體化✓/✗ → 評分：

最終選擇：評分最高版本

【Step 2.2】5 層結構綱要（1 小時）

第 1 層：開場（擊中痛點）— 100 字
核心問題：忙碌的你，每天早上都要花 10-15 分鐘決定穿什麼
開場句：「你花在『穿衣決策』上的時間，足夠讀完一份新聞。」
預期反應：「我也是！」

第 2 層：核心對比（理性 + 感性）— 300 字
舊方法：『靠直覺 + 心情穿衣』
新方法：『用 AI Agent 優化穿衣決策』

類比：穿衣決策就像『機器學習的優化問題』——給定約束條件（天氣、日程、衣櫃），找最優解

對比表：
| 維度 | 傳統方式 | AI Agent 方式 |
|------|--------|------------|
| 決策時間 | 15 分鐘 | 30 秒 |
| 決策依據 | 心情 + 直覺 | 數據 + 優化 |
| 滿意度 | 50-60% | 85%+ |
| 衣服利用率 | 20%(常穿幾套) | 80%(充分搭配) |

第 3 層：痛點深掘（三層為什麼）— 400 字
第 1 層為什麼：穿衣決策這件「小事」為什麼浪費這麼多時間？
→ 因為它涉及多個變量：天氣、日程、場景、心情、衣櫃存貨

第 2 層為什麼：為什麼我們無法自動化這個決策？
→ 因為人的大腦容量有限，無法同時處理這麼多變量。而 AI 正好擅長這個

第 3 層為什麼：為什麼現在開始談「AI 衣櫃管理員」？
→ 因為我們進入了 Agent 時代，AI 不再是「工具」而是「決策夥伴」

第 4 層：代碼/案例證明 — 300 字
案例 1：Google 內部員工用 AI 推薦系統管理衣櫃，工作效率提升 12%
案例 2：虛擬時尚顧問應用（Stitch Fix），90% 用戶滿意度
核心數據：使用 AI 衣櫃推薦的用戶，平均節省時間 4-6 小時/週

第 5 層：結尾（行動號召）— 100 字
金句：「穿衣，從『審美難題』變成『優化問題』，才是真正的自由。」
行動號召：
  ✓ 後續預告（E02 將展示虛擬穿衣間如何運作）
  ✓ 讀者互動（留言說說你每天浪費多少時間穿衣）
  ✓ 訂閱號召（關注 PSA 系列，了解 AI Agent 如何改變生活）

總字數估算：1,000-1,200 字

【Step 2.3】金句和鉤子設計（30 分鐘）

金句（1-2 句，能獨立轉發）：
「穿衣，從『審美難題』變成『優化問題』，AI 才能幫上忙。」

開場鉤子（前 30 秒吸引力）：
類型：對立式 + 數據式
「你花在『穿衣決策』上的時間，足夠讀完一份新聞。而有人用 AI，30 秒解決。」

【Task 2 輸出】JSON 格式包含：最終標題 + 副標題 + 5 層綱要 + 金句 + 鉤子 + 完成檢查清單`,
  {
    label: 'PSA E01 綱要設計師',
    phase: '大綱期',
    schema: {
      type: 'object',
      properties: {
        titleOptions: { type: 'array' },
        finalTitle: { type: 'string' },
        subtitle: { type: 'string' },
        fiveLayerOutline: { type: 'object' },
        goldSentence: { type: 'string' },
        hook: { type: 'string' },
        checklist: { type: 'array' },
      },
    },
  }
)

phase('成稿期')
log('Task 3：PSA E01 的成稿期開始')

const psa_draft = await agent(
  `基於 PSA E01 的綱要，完成成稿期。

【執行步驟】

Step 3.1：初稿快速寫作（2,000-3,000 字，1-2 天）
按 5 層順序逐層寫：開場→對比→深掘→案例→結尾
- 開場（100 字）：引入「穿衣焦慮」的真實場景
- 對比（300 字）：傳統 vs AI 方式的清晰對比
- 深掘（400 字）：為什麼穿衣決策這麼耗時，AI 如何解決
- 案例（300 字）：真實案例 + 數據（Google 員工、Stitch Fix、時間節省數據）
- 結尾（100 字）：金句 + 行動號召

寫作風格：
- 親切感強（直接說「你」，建立連結）
- 邏輯清晰（每個段落一個核心觀點）
- 避免技術術語（目標讀者非技術背景）

Step 3.2：精簡 + 調色（0.5 天，1,200-1,500 字最終版）
3 遍精簡：
1. 刪除重複例子和多餘修飾詞（3,000 → 1,800 字）
2. 合併相似論點（1,800 → 1,400 字）
3. 檢查每一句必要性（1,400 → 1,200-1,500 字）

Step 3.3：配圖準備（0.5 day）
圖片 1：「穿衣決策流程圖」（SVG + PNG，1,200×630px）
  展示：傳統流程 vs AI Agent 流程的對比視覺化

圖片 2：「時間節省效果表」（PNG 截圖）
  展示：使用前後的時間對比

圖片 3：「Substack 社交分享圖」（1,200×630px）
  標題 + 核心視覺 + 品牌色

Step 3.4：Markdown 排版
- 標題層級正確
- 段落簡潔（3-5 句）
- 引言突出（金句用 > block quote）
- 列表清晰（不超過 5 個 bullet）

【Task 3 輸出】JSON 格式包含：初稿 + 精簡版 + 圖片計劃 + Markdown 排版 + 完成檢查清單`,
  {
    label: 'PSA E01 編輯製作',
    phase: '成稿期',
    schema: {
      type: 'object',
      properties: {
        firstDraft: { type: 'string' },
        finalVersion: { type: 'string' },
        images: { type: 'array' },
        markdownFormat: { type: 'string' },
        checklist: { type: 'array' },
      },
    },
  }
)

phase('審核期')
log('Task 4：PSA E01 的審核期開始')

const psa_review = await agent(
  `基於 PSA E01 的成稿，執行審核期。

【Step 4.1】7 層結構自檢（1 小時）
逐層檢查每層的內容、邏輯和完整性：
- 第 1 層（開場）：100 字內，直接擊中「穿衣焦慮」痛點✓/✗
- 第 2 層（對比）：有清晰的對比表和類比✓/✗
- 第 3 層（深掘）：三層為什麼的遞進邏輯✓/✗
- 第 4 層（案例）：有具體的時間數據和成功案例✓/✗
- 第 5 層（結尾）：金句能獨立傳播✓/✗、有行動號召✓/✗

打分（92-100 分優秀，85-91 分良好，<80 分需重編）：___ / 100

【Step 4.2】5 大元素檢查（45 分鐘）
1. 金句：「穿衣，從『審美難題』變成『優化問題』，AI 才能幫上忙」✓/✗
2. 鉤子：「你花在『穿衣決策』上的時間，足夠讀完一份新聞」✓/✗
3. 痛點命中度：破冰篇，是否戳中讀者的「穿衣焦慮」✓/✗
4. 理性感性兼具：有案例數據✓，也有故事和比喻✓✓/✗
5. 工程文學並重：決策優化角度✓，也有人文溫度✓✓/✗

評分（4.0+ 優秀，3.0-3.9 良好，<3.0 需重編）：___ / 5

【Step 4.3】發布規範最終檢查（15 分鐘）
確認 8 項規範都滿足✓

【Task 4 輸出】JSON 格式包含：7 層檢查分數 + 5 大元素評分 + 8 項規範檢查 + 改進建議 + 最終評定（✅可發布/⚠️建議補強/❌需重編）`,
  {
    label: 'PSA E01 審核官',
    phase: '審核期',
    schema: {
      type: 'object',
      properties: {
        sevenLayerCheck: { type: 'object' },
        fiveElementsScore: { type: 'object' },
        publicationStandardCheck: { type: 'array' },
        finalApproval: { type: 'string' },
        checklist: { type: 'array' },
      },
    },
  }
)

phase('發布期')
log('Task 5：PSA E01 的發布期開始')

const psa_publish = await agent(
  `基於 PSA E01 審核通過，執行發布期。

【Step 5.1】Substack 後台設定
- Post Title：穿衣焦慮的終結：為什麼 AI Agent 會成為你的衣櫃管理員
- Subtitle：[40-80 字的副標題]
- Section：個人時尚助理系列
- Post Image：社交分享圖（1,200×630px）
- Tags：效率優化、AI Agent、生活黑客、決策優化、個人助理、科技應用、Substack
- Scheduled time：美東 2026-06-05 10:00 AM EDT

【Step 5.2】正文貼入與排版
確認 Markdown 排版正常，手機端預覽無破損

【Step 5.3】社群文案準備（三平台）
Threads：痛點故事→解決方案→行動號召
LinkedIn：專業標題→問題列表→核心優勢→企業案例→號召
Facebook社團：共鳴場景→痛點→解決方案→對比→號召

【Step 5.4】社團排期
核心社團 3 個，PM 6:00 發布，準備三個版本文案

【Task 5 輸出】JSON 格式包含：Substack 設定 + 排版檢查 + 三平台文案 + 社團排期 + 完成檢查清單`,
  {
    label: 'PSA E01 發布官',
    phase: '發布期',
    schema: {
      type: 'object',
      properties: {
        substackSettings: { type: 'object' },
        formattingCheck: { type: 'array' },
        socialMediaCopy: { type: 'object' },
        publicationSchedule: { type: 'object' },
        checklist: { type: 'array' },
      },
    },
  }
)

phase('複盤期')
log('Task 6：PSA E01 的複盤期開始')

const psa_postReview = await agent(
  `基於 PSA E01 發布執行，規劃複盤期。

【Step 6.1】7 天績效監測計劃
- Day 1：監測打開率、初始互動、新訂數
- Day 3：監測累計打開率、評論深度、社團轉化
- Day 7：最終打開率、轉化率、社群分享次數

預期指標：
- 打開率：30-40%（破冰篇，一般會較好）
- 轉化率：2-3%（首篇預期）
- 新訂數：13-25 人

績效評級標準：
- ⭐⭐⭐⭐⭐ 優秀（3%+ 轉化率，20+ 新訂）
- ⭐⭐⭐⭐ 良好（2-3% 轉化率，13-20 新訂）
- ⭐⭐⭐ 正常（1-2% 轉化率，8-13 新訂）

【Step 6.2】成功因素分析（7-10 天）
分析：
- 標題的點擊率是否符合預期
- 讀者最喜歡的部分（從評論推斷）
- 讀者最想深化的話題（為 E02 提供靈感）
- 哪個社團的轉化率最高

【Step 6.3】改進方向識別
基於成功/失敗因素，為 E02 準備優化清單

【Task 6 輸出】JSON 格式包含：績效監測計劃 + 分析框架 + 改進方向 + 完成檢查清單`,
  {
    label: 'PSA E01 數據分析',
    phase: '複盤期',
    schema: {
      type: 'object',
      properties: {
        performanceMetrics: { type: 'object' },
        successFactors: { type: 'object' },
        improvementPlan: { type: 'array' },
        checklist: { type: 'array' },
      },
    },
  }
)

log('✅ PSA E01 爆文完整工作流執行完成！')

return {
  workflowName: 'PSA E01 爆文完整寫作流程',
  series: '個人時尚助理系列',
  episode: 'E01',
  title: '穿衣焦慮的終結：為什麼 AI Agent 會成為你的衣櫃管理員',
  timeline: '7-10 天完成發布',
  successMetrics: '2-3% 轉化率、13-25 新訂、75%+ 完讀率',
  outputs: {
    task1_planning: psa_planning,
    task2_outline: psa_outline,
    task3_draft: psa_draft,
    task4_review: psa_review,
    task5_publish: psa_publish,
    task6_postReview: psa_postReview,
  },
  nextSteps: [
    '確認 E01 規劃無誤',
    '開始 Task 2 的標題設計（3 個版本競爭）',
    '按綱要完成初稿寫作',
    '按時發布（2026-06-05）',
    '監測數據，為 E02 優化方向',
  ],
  publicationDate: '2026-06-05 至 2026-06-10',
  targetCommunities: ['效率工作者社團', 'Agent 應用開發社團', 'Substack 中文科技社團'],
}
