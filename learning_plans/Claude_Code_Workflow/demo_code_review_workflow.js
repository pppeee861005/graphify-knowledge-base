/**
 * 代碼審查 Workflow - 基本示範版本
 *
 * 執行模式：Pipeline（流水線）
 * 流程：讀取代碼 → 語法檢查 → 安全審查 → 生成報告
 *
 * 📚 學習目標：
 * ✅ 理解 Workflow 三要素
 * ✅ 學習 Pipeline 模式（順序執行）
 * ✅ 掌握 async/await 用法
 * ✅ 實現標準結果格式
 */

// ═══════════════════════════════════════════════════════════════
// 1️⃣ 元數據聲明（必須有！）
// ═══════════════════════════════════════════════════════════════

const metadata = {
  name: "代碼審查 Workflow",
  description: "簡單的代碼審查流程 - 語法檢查 → 安全審查 → 生成報告",
  version: "1.0.0",
  author: "Learning Workflow",
  execution_mode: "Pipeline",  // 順序執行，不是並行
  estimated_time_ms: 3000,

  // 定義所有 Stages（步驟）
  stages: [
    "讀取代碼",
    "語法檢查",
    "安全審查",
    "生成報告"
  ]
};

// ═══════════════════════════════════════════════════════════════
// 2️⃣ 執行邏輯（核心！）
// ═══════════════════════════════════════════════════════════════

async function execute(context) {
  console.log("🔍 代碼審查 Workflow 啟動...\n");

  // 從輸入中獲取要審查的代碼
  const codeToReview = context.input?.code || `
    function hello(name) {
      console.log("Hello " + name);
    }
  `;

  try {
    // ─────────────────────────────────────────────────────────
    // Stage 1: 讀取代碼
    // ─────────────────────────────────────────────────────────
    console.log("📖 Stage 1: 讀取代碼");

    const codeLength = codeToReview.length;
    const lineCount = codeToReview.split('\n').length;

    console.log(`   ✓ 代碼長度：${codeLength} 字符`);
    console.log(`   ✓ 行數：${lineCount} 行\n`);

    // ─────────────────────────────────────────────────────────
    // Stage 2: 語法檢查
    // ─────────────────────────────────────────────────────────
    console.log("✅ Stage 2: 語法檢查");

    // 調用 Agent（AI）執行語法檢查
    const syntaxCheckResult = await agent.run("語法檢查器", {
      prompt: `檢查這段 JavaScript 代碼的語法：

               ${codeToReview}

               返回格式：
               {
                 "has_errors": false,
                 "errors": [],
                 "warnings": [],
                 "code_style": "good"
               }`,
      temperature: 0.2  // 低溫 = 準確
    });

    console.log(`   ✓ 語法檢查完成\n`);

    // ─────────────────────────────────────────────────────────
    // Stage 3: 安全審查
    // ─────────────────────────────────────────────────────────
    console.log("🔒 Stage 3: 安全審查");

    // 調用 Agent（AI）執行安全審查
    const securityCheckResult = await agent.run("安全審查器", {
      prompt: `審查這段代碼的安全問題：

               ${codeToReview}

               檢查項目：
               - SQL 注入風險
               - XSS 風險
               - 不安全的函數
               - 權限問題

               返回格式：
               {
                 "risk_level": "low|medium|high",
                 "vulnerabilities": [],
                 "recommendations": []
               }`,
      temperature: 0.2
    });

    console.log(`   ✓ 安全審查完成\n`);

    // ─────────────────────────────────────────────────────────
    // Stage 4: 生成報告
    // ─────────────────────────────────────────────────────────
    console.log("📊 Stage 4: 生成報告");

    // 調用 Agent（AI）生成最終報告
    const reportResult = await agent.run("報告生成器", {
      prompt: `基於這些檢查結果，生成一份代碼審查報告：

               語法檢查結果：${syntaxCheckResult}
               安全審查結果：${securityCheckResult}
               代碼：${codeToReview}

               報告應包括：
               1. 總體評分（1-10）
               2. 主要問題列表
               3. 改進建議
               4. 推薦優先級`,
      temperature: 0.5  // 稍高 = 報告更優美
    });

    console.log(`   ✓ 報告生成完成\n`);

    // ═══════════════════════════════════════════════════════════════
    // 3️⃣ 返回標準結果格式
    // ═══════════════════════════════════════════════════════════════

    return {
      // 成功標誌
      success: true,

      // 主要輸出
      output: {
        code_info: {
          length: codeLength,
          lines: lineCount
        },
        syntax_check: syntaxCheckResult,
        security_check: securityCheckResult,
        final_report: reportResult
      },

      // 性能指標（給 /workflows 命令使用）
      metrics: {
        code_length: codeLength,
        line_count: lineCount,
        timestamp: new Date().toISOString(),
        execution_time_ms: null,  // 由系統自動填充
        stages_completed: 4
      },

      // 狀態信息
      status: {
        stage_1_read_code: "✅ 完成",
        stage_2_syntax_check: "✅ 完成",
        stage_3_security_check: "✅ 完成",
        stage_4_report: "✅ 完成"
      }
    };

  } catch (error) {
    // 錯誤處理
    console.error("❌ Workflow 錯誤:", error.message);

    return {
      success: false,
      error: error.message,
      output: null,
      metrics: {
        timestamp: new Date().toISOString(),
        failed_at_stage: error.stage || "unknown"
      }
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// 💡 使用示例
// ═══════════════════════════════════════════════════════════════

/*
在 Claude Code 中使用：

1. 基礎用法
   ultraWork 代碼審查 Workflow: 審查我的 JavaScript 代碼

2. 帶自定義代碼
   ultraWork 代碼審查 Workflow --code="function test() { return 42; }"

執行完後查看結果：
   /workflows

會看到：
- 每個 Stage 的執行時間
- Token 消耗
- 整個流程的成功/失敗狀態
*/

// ═══════════════════════════════════════════════════════════════
// 🎯 Pipeline 架構說明
// ═══════════════════════════════════════════════════════════════

/*
執行流程（順序執行，一個接一個）：

    輸入代碼
        ↓
    Stage 1: 讀取代碼
        ↓ 等待完成
    Stage 2: 語法檢查
        ↓ 等待完成
    Stage 3: 安全審查
        ↓ 等待完成
    Stage 4: 生成報告
        ↓
    返回結果

時間線：
├─ Stage 1: 100ms
├─ Stage 2: 800ms (agent.run 調用)
├─ Stage 3: 900ms (agent.run 調用)
├─ Stage 4: 1200ms (agent.run 調用)
└─ 總計: ~3000ms

Pipeline 的特點：
✅ 簡單直觀
✅ 一個 Stage 的輸出是下一個的輸入
✅ 如果前面失敗，後面不會執行
✅ 易於調試（知道在哪個 Stage 失敗）
❌ 不夠快（不能並行）
*/

// ═══════════════════════════════════════════════════════════════
// 📚 與 Deep Search Workflow 的對比
// ═══════════════════════════════════════════════════════════════

/*
Deep Search Workflow        代碼審查 Workflow (本文件)
─────────────────────────────────────────────────────
複雜度：高                    複雜度：低
Stages：5 個                  Stages：4 個
執行模式：Sync Aggregation   執行模式：Pipeline
並行度：4 個搜索同時          並行度：0（順序執行）
代碼行數：276 行              代碼行數：179 行
適合：多源聚合                適合：初學者學習

兩者都展示了：
✅ Workflow 三要素
✅ async/await 用法
✅ agent.run() 調用
✅ 標準結果格式
✅ 錯誤處理
*/

// ═══════════════════════════════════════════════════════════════
// 🔧 可以學習和修改的地方
// ═══════════════════════════════════════════════════════════════

/*
修改 1️⃣：添加新的 Stage
─────────────────────────────────────────────
在 Stage 3 和 Stage 4 之間添加「性能審查」

const performanceCheckResult = await agent.run("性能審查器", {
  prompt: `檢查代碼的性能問題...`
});

修改 2️⃣：改成並行模式（Sync Aggregation）
─────────────────────────────────────────────
const [syntaxResult, securityResult, performanceResult] =
  await Promise.all([
    agent.run("語法檢查器", {...}),
    agent.run("安全審查器", {...}),
    agent.run("性能審查器", {...})
  ]);

修改 3️⃣：添加條件邏輯
─────────────────────────────────────────────
if (syntaxCheckResult.has_errors) {
  console.log("⚠️ 語法檢查失敗，跳過安全審查");
  return {
    success: false,
    error: "語法錯誤"
  };
}

修改 4️⃣：改變溫度
─────────────────────────────────────────────
temperature: 0.1   // 極度穩定（檢查）
temperature: 0.5   // 平衡（報告）
temperature: 0.8   // 創意（建議）
*/

// ═══════════════════════════════════════════════════════════════
// 🎓 学习任务
// ═══════════════════════════════════════════════════════════════

/*
Task 1: 理解结构
────────────────────────────────────────────
阅读代码，回答：
1. 元数据中有哪 5 个关键字段？
2. execute 函数为什么是 async？
3. 为什么要用 try/catch？
4. 返回结果中为什么要有 metrics？

Task 2: 理解 Pipeline
────────────────────────────────────────────
运行这个 Workflow，观察：
1. 各个 Stage 的执行时间
2. Stage 执行的先后顺序
3. 如果某个 Stage 失败会发生什么？

Task 3: 修改和扩展
────────────────────────────────────────────
1. 添加第 5 个 Stage（性能检查）
2. 改成 Promise.all() 并行模式
3. 添加更多的检查项目

Task 4: 对比学习
────────────────────────────────────────────
对比这个 Workflow 和 deep_search_workflow.js：
1. 哪些部分相同？
2. 哪些部分不同？
3. 为什么一个用 Pipeline，一个用 Aggregation？
*/

// 导出（必须有！）
module.exports = { metadata, execute };
