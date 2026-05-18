要執行 kanban 任務，需要三個條件 + 精準指令格式：

⚠️ 當前狀況

  檢查項               狀態
      ───────────────────  ─────────────────────────────────────────────
      Gateway              ❌ 未啟動（tasks 會卡在 ready 不動）
      註冊的 assignees     ✅ 4 個：analyst, researcher, writer, default
      子 profile API keys  ❌ 需要確認（hermes -p researcher setup 等）

    🚀 完整執行流程

    Step 1: 啟動 Gateway（必須）

      ─ bash
      hermes gateway install   # 後台服務
      hermes gateway start     # 啟動
      hermes gateway status    # 確認 ✅

    Step 2: 下達精準指令
    Step 2: 下達精準指令
Orchestrator 分解範例（以暗知識系列 W3 為例）：

# 用 hermes kanban CLI
hermes kanban create "T1: 收集 W3 責任歸屬案例素材" \
  --assignee researcher \
  --body "搜尋 AI 醫療診斷錯誤、自動駕駛事故、DABUS 發明案的責任歸屬案例，整理成結構化報告"
hermes kanban create "T2: 分析法律框架缺口" \
  --assignee analyst \
  --body "基於 T1 的案例，分析現有法律框架在 AI 自主決策時的責任歸屬漏洞"
hermes kanban create "T3: 撰寫 W3 草稿" \
  --assignee writer \
  --body "用豪力風神風格撰寫 3000-4000 字草稿，標題待定，聚焦三個責任問題：知識屬於誰、錯誤誰負責、權利誰定義"

關鍵語法：

• hermes kanban create "標題" — 標題是位置參數，不是 --title
• --assignee 必須是已註冊的 profile（researcher/analyst/writer）
• --body 多行用 heredoc：--body "$(cat <<'EOF'\n...\nEOF\n)"
• 依賴關係：--parent t_xxx1 --parent t_xxx2

Step 3: 監控進度

─ bash
hermes kanban list          # 看所有任務狀態
hermes kanban show t_xxxx   # 看單一任務詳情
hermes kanban tail t_xxxx   # 即時追蹤