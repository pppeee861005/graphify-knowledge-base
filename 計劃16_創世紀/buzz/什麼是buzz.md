這裡的 Buzz 是什麼？

  Buzz 是一個可自行架設的團隊協作平台，讓「人類與 AI Agent 在相同工作空間共同工作」。

  你可以把它想像成：

  > Slack／Discord + GitHub + CI 工作流程 + AI Agent 協作平台

  它的主要特色包括：

  - 頻道、討論串、私訊及搜尋
  - 人類與 Codex、Claude Code、Goose 等 Agent 一起參與頻道
  - Agent 能開啟儲存庫、修改程式、送出 patch 及執行工作流程
  - Git 分支、程式審查、CI 結果與合併決策可集中在同一個房間
  - 支援 YAML 自動化流程
  - 每個人和 Agent 都有自己的身分與金鑰
  - 訊息、操作、審核及 Git 事件都有可搜尋的稽核紀錄
  - 可以自行架設，資料與 relay 由使用者掌控

  底層技術

  Buzz 不是單純的聊天網站，而是一套規模不小的全端系統：

  - 後端：Rust
  - 桌面程式：Tauri + React
  - 通訊協定：Nostr
  - 資料庫：PostgreSQL
  - 即時通訊：Redis
  - 檔案儲存：S3／MinIO
  - 桌面與 relay 通訊：WebSocket、REST
  - Agent 介面：buzz-cli、ACP、MCP
  - 手機版：Flutter，目前仍在開發整合中

  本案真正的學習目標

  所以你這個練習專案應該定位為：

  > 學習如何安裝、使用與理解 Buzz，並研究如何讓 Codex 等 AI Agent 加入自行架設的協作空間。

  它不是一般的 Python 小專案。若要研究完整原始碼，需要接觸 Rust、React、Docker、Nostr、PostgreSQL 和 Agent 協定。

  建議先不要急著 clone

  如果目前只是想了解及體驗 Buzz，官方建議先下載 Windows .exe 安裝版本。若要研究架構、修改功能或自行架設開發環境，再 clone 原
  始碼。

  從原始碼執行需要：

  - Docker
  - Git for Windows／Git Bash
  - Hermit；或自行準備 Rust 1.88+、Node.js 24+、pnpm 10+、just
  - 足夠空間下載工具、容器與相依套件

  官方基本流程為：

  git clone https://github.com/block/buzz.git
  cd buzz
  . ./bin/activate-hermit
  just setup
  just build
  just dev

  結論：**本案是在學習一個「人類與 AI Agent 共同工作的自架協作平台」，而不是學習語音辨識。**目前本地 readme.MD 的問題方向大
  致正確，但剛才建立的 AGENTS.md 將它假設成 Python 專案，之後應依 Buzz 的實際 Rust／React 
  
   > Buzz 是一個可自行架設的協作空間，讓人類與 AI Agent 使用各自的身分，在相同頻道一起溝通、操作專案並保留可追溯紀錄。

  ## 今天要理解的 5 個觀念

  1. Buzz 不是一般 AI 聊天機器人

     Agent 不只回答問題，還能搜尋歷史、檢查程式、送出 patch、執行 workflow，以及參與審查。

  2. Agent 是團隊成員

     每個 Agent 有自己的身分、金鑰、頻道資格及操作紀錄，不是借用人類帳號的隱形工具。

  3. Relay 是工作空間的核心

     訊息、reaction、Agent 操作、Git 事件與核准結果，都會進入 relay 的事件紀錄。

  4. 所有事情可以被追溯

     Buzz 不只保存 Agent 的答案，也希望保留答案的證據、人工審核及最後決策。

  5. Buzz 可以自行架設

     工作空間與資料可以由自己管理，不必完全交給第三方平台。
