Submodule 是什麼？

  簡單說：Submodule 是「倉庫中的倉庫」。 一個 Git 倉庫可以包含其他 Git 倉庫的引用，而不是直接複製代碼。

  ---
  對比圖解

  ❌ 當前狀況（嵌入式子倉庫）

  graphify-knowledge-base/
  ├── 計劃13_租約哨兵/           ← 這是一個完整的 .git 倉庫
  │   ├── .git/                  ← 有自己的 git 歷史
  │   ├── rules/
  │   ├── workflows/
  │   └── README.md
  │
  └── 其他檔案/

  問題：
  - Clone graphify-knowledge-base 時，計劃13 的代碼不會被自動包含
  - 兩個倉庫的歷史分離，難以追蹤全局變更
  - 容易造成混亂（不知道應該在哪個倉庫提交）

  ---
  ✅ Submodule 方式

  graphify-knowledge-base/                ← 父倉庫
  ├── .gitmodules                         ← 記錄 submodule 配置
  ├── 計劃13_租約哨兵 → [指向]           ← 只是一個連結，指向
  │   https://github.com/pppeee861005/lease-guard-wf.git
  │   (特定 commit)
  │
  └── 其他檔案/

  優點：
  - 在父倉庫中清楚地記錄子倉庫的版本（commit hash）
  - Clone 時加一個參數（--recursive）就能自動拉取子倉庫
  - 子倉庫和父倉庫的版本獨立管理，但可追蹤

  ---
  具體例子

  場景：你和全球貢獻者協作

  使用 Submodule 的好處

  某個貢獻者 fork 你的專案：

  # 一次命令，自動拉取整個倉庫樹
  git clone --recursive https://github.com/pppeee861005/graphify-knowledge-base.git

  # 得到完整目錄：
  # ├── 計劃13_租約哨兵/  ← 自動包含，內容完整
  # ├── 其他知識庫檔案/
  # └── ...

  沒有 Submodule 的話：

  git clone https://github.com/pppeee861005/graphify-knowledge-base.git

  # 得到的是：
  # ├── 計劃13_租約哨兵/  ← 只有目錄，但是空的！
  # ├── 其他知識庫檔案/
  # └── ...

  # 他還要手動執行：
  git submodule update --init --recursive