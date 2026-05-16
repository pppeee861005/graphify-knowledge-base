我們來聊富途https://github.com/FutunnOpen/py-futu-api

5月4日
Claude responded: 風神好，富途的 py-futu-api 我來查一下最新狀態，特別是版本、功能變化、跟我們 Skill Foundry 思路的接點在哪裡。 指揮官，看完了。先講我對這個專案的快速判斷，再聊我們可以怎麼切。
風神好，富途的 py-futu-api 我來查一下最新狀態，特別是版本、功能變化、跟我們 Skill Foundry 思路的接點在哪裡。


Fetched: GitHub - FutunnOpen/py-futu-api: 富途 OpenAPI Python SDK
Fetched: GitHub - FutunnOpen/py-futu-api: 富途 OpenAPI Python SDK
指揮官，看完了。先講我對這個專案的快速判斷，再聊我們可以怎麼切。

專案狀態速寫
富途 OpenAPI Python SDK，1.3k star、260 fork、Apache-2.0、99.9% Python。架構是雙層的——Python SDK 不直接連富途伺服器，而是先連到本地跑的 FutuOpenD 網關客戶端（gateway），SDK 再透過 127.0.0.1:11111 跟 OpenD 對話。OpenD 才是真正連富途後台的那一層。

這個架構設計值得注意：

券商把「協議閘道器」獨立成一個本地 daemon，等於是把「合規/風控/連線管理」鎖在自己的二進位裡，SDK 層完全是開源的薄殼。
對開發者來說，SDK 只是行情/交易接口的 Python 封裝，協議靠 Protobuf。
港股、美股、A股、期貨、加密都走同一個 Context 模式——OpenQuoteContext 看行情、OpenHKTradeContext / OpenUSTradeContext 等做交易。
從 commit 看，這個 repo 維護穩定但不算活躍（537 commits、沒有正式 release tag、issues 101 個未關），典型的「券商出於合規責任會持續維護，但不會做出爆炸性創新」型專案。

三個切入角度（按你關心的順序）
1. 從 Skill Foundry 視角看：這是一個典型的 L3 真空帶候選

這個 SDK 本身不是真空——富途自己會維護。真空在「上層 Skill」：

「自然語言 → 富途下單/查詢」的 SKILL.md（給 Claude/Hermes 用）
「美股期權 theta decay 監控 Agent」（你本來就懂選擇權）
「TSMC + 黃金 + 美元指數三條線聯動觀察 Agent」（接你既有的 macro 監控興趣）
「台灣個人投資者跨市場（台股/港股/美股）統一視圖」——富途剛好都覆蓋
券商 SDK 是「水電」，再過 18-36 個月可能被某個 Agent 平台原生內化（L4），但現在這個窗口，把 py-futu-api 包成一支 SKILL.md，搭配你的選擇權直覺，是有機會的。

2. 從技術架構看：這個 OpenD 閘道模式很有意思

它跟 IBKR 的 TWS/Gateway 架構幾乎一模一樣——Interactive Brokers 也是用 client → local gateway → broker server 的三層。代表這是金融券商面對量化開發者的事實標準。

值得思考的策略含義：未來 Agent 要「自主交易」會卡在哪？ 卡在 OpenD 這層需要本地常駐、需要解鎖密碼、需要人工確認交易。這是券商保留的「最後一道人類確認」護城河——對應你之前那個觀察：「持牌專業的最後護城河是法律責任承擔」，這裡是「交易執行的最後一道授權承擔」。

3. 從合規/可用性看：台灣個人投資者的限制

富途主要服務香港、美國、新加坡、加拿大、澳洲市場。台灣居民開戶有限制——這個你可能要自己確認一下你的帳戶狀態。如果你只是要研究 SDK、做 Skill 原型，paper trading（TrdEnv.SIMULATE）不需要實盤帳戶就能跑，這就夠做開發。

