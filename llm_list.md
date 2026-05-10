以下是 Hermes 經由 OpenRouter 目前支援的代表性 LLM（依模型類型與常見用途簡單分類，僅列出較熱門/實用的部分，完整清單有 300+ 個模型，可自行查閱 OpenRouter 模型頁）：

類別          模型 ID（在 OpenRouter）                                 簡介 / 特色                     適合場景
──────────  ──────────────────────────────────────────────────  ──────────────────────────  ───────────────────────
推理 / 指揮官級   anthropic/claude-sonnet-4                           強推理、長上下文、穩定可靠               任務分解、協調、複雜規劃
            anthropic/claude-opus-4.7                           最強的 Claude 系列，較高成本          需要最高品質輸出的研究或寫作
            openai/gpt-5.5                                      OpenAI 最新旗艦，廣泛知識與多模態潛力      通用高品質任務
            x-ai/grok-4.3                                       xAI 最新模型，推理與實時知識結合          需要即時網路資訊的查詢
平衡型 / 成本效益  google/gemini-3.1-flash-lite                        Google 最新輕量版 Flash，速度快、成本低  大量資料蒐集、快速摘要
            google/gemini-flash-latest                          同上，稍微完整版                    研究員、分析員
            moonshotai/kimi-k2.6                                月之暗面 Kimi 系列，中文表現優秀、成本適中    中文內容生成、學習筆記
            deepseek/deepseek-v4-pro                            DeepSeek 最新版，推理強且開源友好       程式碼、邏輯推理
            qwen/qwen3.6-max-preview                            阿里通義千錢大模型，多語言與多模態           多語言任務、圖文理解
輕量 / 免費層    nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free  NVIDIA 提供的免費推理模型            快速原型、學習實驗
            google/gemma-4-26b-a4b-it:free                      Google Gemma 開源版，免費且效不錯     小型任務、嵌入式場景
            xiaomi/mimo-v2.5                                    小米自研 MiMo，中文理解與生成表現良好       日常對話、筆記整理
            baidu/qianfan-ocr-fast:free                         百度 OCR 快速版（免費）              圖片文字辨識需求
專業工具型       openrouter/owl-alpha                                OpenRouter 內部測試模型，常用於工具鏈測試  除錯、工具鏈驗證
            openai/gpt-5.4-image-2                              具備圖像理解與生成能力的 GPT 變體         多模態（圖文）任務
            x-ai/grok-4.20-multi-agent                          專為多智能體協作設計的 Grok 版本         多Agent 工作流 orchestrator
實驗 / 前沿     inclusionai/ring-2.6-1t:free                        極大參數量的免費實驗模型（適合探索）          研究前沿能力、消融實驗
            tencent/hy3-preview                                 騰訊混沌系列預覽版，推理與創意並重           創意寫作、故事生成