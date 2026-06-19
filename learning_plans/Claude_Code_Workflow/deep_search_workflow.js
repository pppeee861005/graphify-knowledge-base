/**
 * Deep Search Workflow
 * 多層次智能搜索流程
 *
 * 執行模式：Sync Aggregation（同步聚合）
 * 流程：理解查詢 → 並行多源搜索 → 聚合排序 → 生成報告
 */

// ═══════════════════════════════════════════════════════════════
// 1️⃣ 元數據聲明
// ═══════════════════════════════════════════════════════════════

const metadata = {
  name: "Deep Search Workflow",
  description: "多層次智能搜索流程 - 理解查詢 → 並行搜索 → 聚合結果 → 生成報告",
  version: "1.0.0",
  author: "Claude Code Workflow",
  tags: ["search", "aggregation", "multi-source"],
  execution_mode: "Sync Aggregation",
  estimated_time_ms: 5000,
  stages: [
    "查詢分析",
    "並行多源搜索",
    "結果聚合",
    "質量排序",
    "最終報告"
  ]
};

// ═══════════════════════════════════════════════════════════════
// 2️⃣ 執行邏輯（核心工作流）
// ═══════════════════════════════════════════════════════════════

async function execute(context) {
  console.log("🔍 Deep Search Workflow 啟動...");

  const userQuery = context.input?.query || "如何學習 Claude Code Workflow";
  const searchDepth = context.input?.depth || "standard"; // light, standard, deep

  try {
    // ─────────────────────────────────────────────────────────
    // Stage 1: 查詢理解與優化
    // ─────────────────────────────────────────────────────────
    console.log(`\n📋 Stage 1: 查詢分析`);

    const queryAnalysis = await agent.run("查詢分析器", {
      prompt: `分析這個搜索查詢，提取關鍵詞和搜索意圖：
               查詢：${userQuery}
               返回格式：{ keywords: [], intent: "", entities: [] }`,
      temperature: 0.3
    });

    const { keywords, intent, entities } = JSON.parse(queryAnalysis);
    console.log(`   ✓ 關鍵詞：${keywords.join(", ")}`);
    console.log(`   ✓ 搜索意圖：${intent}`);

    // ─────────────────────────────────────────────────────────
    // Stage 2: 並行多源搜索（核心：Sync Aggregation）
    // ─────────────────────────────────────────────────────────
    console.log(`\n🔎 Stage 2: 並行多源搜索`);

    const [documentSearch, codeSearch, conceptSearch, exampleSearch] = await Promise.all([
      // 搜索來源 1: 文檔和理論
      agent.run("文檔搜索器", {
        prompt: `在技術文檔中搜索：${userQuery}
                 返回：[ { title, relevance_score, excerpt } ]`,
        temperature: 0.2
      }),

      // 搜索來源 2: 代碼示例
      agent.run("代碼搜索器", {
        prompt: `尋找相關的代碼實現：${userQuery}
                 返回：[ { filename, language, snippet, relevance_score } ]`,
        temperature: 0.2
      }),

      // 搜索來源 3: 概念關係
      agent.run("概念搜索器", {
        prompt: `映射相關概念和知識圖譜：${userQuery}
                 返回：[ { concept, related_to, relationship_type } ]`,
        temperature: 0.3
      }),

      // 搜索來源 4: 實踐範例
      agent.run("範例搜索器", {
        prompt: `找到實踐案例和應用場景：${userQuery}
                 返回：[ { title, domain, use_case, relevance_score } ]`,
        temperature: 0.3
      })
    ]);

    console.log(`   ✓ 文檔搜索完成`);
    console.log(`   ✓ 代碼搜索完成`);
    console.log(`   ✓ 概念搜索完成`);
    console.log(`   ✓ 範例搜索完成`);

    // ─────────────────────────────────────────────────────────
    // Stage 3: 結果聚合與去重
    // ─────────────────────────────────────────────────────────
    console.log(`\n🔗 Stage 3: 結果聚合與去重`);

    const aggregationResult = await agent.run("結果聚合器", {
      prompt: `聚合並去重這些搜索結果：
               文檔：${documentSearch}
               代碼：${codeSearch}
               概念：${conceptSearch}
               範例：${exampleSearch}

               返回：{ total_results, unique_items, clusters }`,
      temperature: 0.2
    });

    console.log(`   ✓ 聚合完成`);

    // ─────────────────────────────────────────────────────────
    // Stage 4: 質量排序與重排
    // ─────────────────────────────────────────────────────────
    console.log(`\n⭐ Stage 4: 質量排序`);

    const rankedResults = await agent.run("排序引擎", {
      prompt: `基於相關性、新鮮度、實用性對結果排序：
               查詢：${userQuery}
               結果：${aggregationResult}
               深度：${searchDepth}

               返回有序的排名列表`,
      temperature: 0.2
    });

    console.log(`   ✓ 排序完成（${searchDepth} 深度）`);

    // ─────────────────────────────────────────────────────────
    // Stage 5: 生成最終報告
    // ─────────────────────────────────────────────────────────
    console.log(`\n📊 Stage 5: 生成報告`);

    const finalReport = await agent.run("報告生成器", {
      prompt: `基於排序結果，生成一份專業搜索報告：
               原始查詢：${userQuery}
               關鍵詞：${keywords.join(", ")}
               排序結果：${rankedResults}

               報告應包括：
               1. 執行摘要
               2. 頂部 5 個結果
               3. 相關概念圖
               4. 推薦後續查詢`,
      temperature: 0.5
    });

    console.log(`   ✓ 報告生成完成`);

    // ═══════════════════════════════════════════════════════════════
    // 3️⃣ 返回標準結果格式
    // ═══════════════════════════════════════════════════════════════

    return {
      success: true,

      output: {
        query: userQuery,
        depth: searchDepth,

        // 各階段輸出
        analysis: {
          keywords,
          intent,
          entities
        },

        search_results: {
          documents: documentSearch,
          code: codeSearch,
          concepts: conceptSearch,
          examples: exampleSearch
        },

        aggregated: aggregationResult,
        ranked: rankedResults,
        final_report: finalReport
      },

      // 性能指標
      metrics: {
        query_length: userQuery.length,
        search_depth,
        timestamp: new Date().toISOString(),
        execution_time_ms: null, // 由 Workflow 系統自動填充
        stages_completed: 5,
        sources_queried: 4,
        total_results_aggregated: 0 // 由実際搜索結果決定
      },

      // 狀態信息
      status: {
        stage_1_query_analysis: "✅ 完成",
        stage_2_parallel_search: "✅ 完成",
        stage_3_aggregation: "✅ 完成",
        stage_4_ranking: "✅ 完成",
        stage_5_reporting: "✅ 完成"
      }
    };

  } catch (error) {
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
// 💡 使用範例與測試用例
// ═══════════════════════════════════════════════════════════════

/*
使用方式：

1. 標準搜索
   ultraWork Deep Search Workflow: 如何學習 Claude Code Workflow

2. 深度搜索
   ultraWork Deep Search Workflow: 如何設計企業級系統 --depth=deep

3. 快速搜索
   ultraWork Deep Search Workflow: Workflow 執行模式 --depth=light

執行完後，在終端運行：
   /workflows

查看每個 Stage 的：
- ⏱️ 耗時
- 💾 Token 消耗
- 📊 狀態
*/

// ═══════════════════════════════════════════════════════════════
// 🎯 Workflow 架構說明
// ═══════════════════════════════════════════════════════════════

/*
執行模式：Sync Aggregation（同步聚合）

    Stage 1: 查詢分析
        ↓
    Stage 2: 並行搜索 ─┬─ 文檔搜索
                      ├─ 代碼搜索
                      ├─ 概念搜索
                      └─ 範例搜索
        ↓ (Promise.all)
    Stage 3: 聚合結果
        ↓
    Stage 4: 排序優化
        ↓
    Stage 5: 生成報告
        ↓
    返回標準結果

優勢：
✅ 並行搜索提高效率（Stage 2）
✅ 多源聚合提高質量
✅ 每個 Stage 完全可觀測
✅ 易於監控和優化
✅ 支援 Git 版本控制
*/

// 導出元數據和執行函數
module.exports = { metadata, execute };
