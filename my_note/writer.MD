📝 VPS 寫文章的 Git 流程

  # 1️⃣  進入文章目錄
  cd graphify-knowledge-base/系列文章/暗知識系列/

  # 2️⃣  拉取最新  git pull
  # 3️⃣  寫文章（新建或編輯）
  nano DK_S01E04_新文章.md
  # 4️⃣  完成後提交
  git add DK_S01E04_新文章.md  git commit -m "完成：暗知識第四篇"
  git push

  ---  ⚡ 快速版本（常用）
  # 拉取
  git pull
  # 寫文章...

  # 提交  git add .
  git commit -m "標題"
  git push

  git push

  ---
  ⚡ 快速版本（常用）

  # 拉取
  git pull

  # 寫文章...

  # 提交
  git add .
  git commit -m "標題"
  git push

  ---
  💡 建議

  每篇文章提交訊息格式：
  完成：[系列名] [標題]

  例如：
  git commit -m "完成：暗知識系列 E04_AI科學家的秘密實驗室"