# ⚡ 30 分鐘快速部署：《引力轉移》互動診斷網頁

**目標：在 30 分鐘內部署互動診斷頁面到 Vercel，獲得可分享的公開鏈接**

---

## 第一步：本地開發（10 分鐘）

### 1. 創建 Next.js 項目

```bash
# 打開終端，進入你要放項目的目錄
cd ~/projects  # 或任何地方

# 創建 Next.js 項目
npx create-next-app@latest ai-commander-web \
  --typescript \
  --tailwind \
  --app \
  --no-eslint

# 進入項目
cd ai-commander-web
```

**選項參考（按 Enter 選預設）：**
```
✔ TypeScript? … Yes
✔ Tailwind CSS? … Yes
✔ src/ directory? … No
✔ App Router? … Yes
✔ Customize import alias? … No
```

### 2. 安裝依賴

```bash
npm install framer-motion lucide-react recharts
```

**預期時間：3-5 分鐘（取決於網速）**

### 3. 替換首頁

打開 `app/page.jsx`，**完全替換** 為以下內容：

```jsx
'use client';

import React, { useState } from 'react';
import { ChevronRight, Zap, Share2, Mail } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const CreatorDiagnostic = () => {
  const [phase, setPhase] = useState('landing');
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [userType, setUserType] = useState(null);

  const creatorTypes = {
    storyteller: {
      name: '說故事者',
      emoji: '📖',
      description: '你用敘事和情感連結驅動人心。',
      color: 'from-rose-500 to-pink-500'
    },
    builder: {
      name: '建構者',
      emoji: '🔨',
      description: '你將想法變成產品和工具。',
      color: 'from-blue-500 to-cyan-500'
    },
    connector: {
      name: '連結者',
      emoji: '🌐',
      description: '你連接人、想法和機會。',
      color: 'from-purple-500 to-indigo-500'
    },
    experimenter: {
      name: '實驗者',
      emoji: '⚗️',
      description: '你透過嘗試發現新路徑。',
      color: 'from-amber-500 to-orange-500'
    },
    teacher: {
      name: '教育者',
      emoji: '👨‍🏫',
      description: '你用知識賦能他人。',
      color: 'from-green-500 to-emerald-500'
    }
  };

  const questions = [
    {
      q: '當你完成創作項目後，最開心的感受是？',
      options: [
        { text: '看到人們被你的故事感動', score: { storyteller: 2 } },
        { text: '看到功能正常運作', score: { builder: 2 } },
        { text: '看到社群聚集在你的想法周圍', score: { connector: 2 } },
        { text: '發現新的可能性', score: { experimenter: 2 } },
        { text: '知道有人透過我的教學學到東西', score: { teacher: 2 } }
      ]
    },
    {
      q: '你在哪個時刻感到最有動力？',
      options: [
        { text: '讀者說你改變了他們的想法', score: { storyteller: 2 } },
        { text: '產品上線，有人在用我做的東西', score: { builder: 2 } },
        { text: '引薦了對的人相識', score: { connector: 2 } },
        { text: '發現別人沒試過的領域', score: { experimenter: 2 } },
        { text: '學生問出深度問題', score: { teacher: 2 } }
      ]
    },
    {
      q: '創作過程中，你最投入時間的是？',
      options: [
        { text: '打磨細節，讓故事更感人', score: { storyteller: 2 } },
        { text: '解決技術問題', score: { builder: 2 } },
        { text: '與社群溝通', score: { connector: 2 } },
        { text: '試驗新想法', score: { experimenter: 2 } },
        { text: '設計教學框架', score: { teacher: 2 } }
      ]
    },
    {
      q: '你最害怕什麼？',
      options: [
        { text: '人們不理解我的真實情感', score: { storyteller: 2 } },
        { text: '我建造的東西沒人用', score: { builder: 2 } },
        { text: '被孤立，失去社群', score: { connector: 2 } },
        { text: '被困在舒適區', score: { experimenter: 2 } },
        { text: '我的知識沒有幫到任何人', score: { teacher: 2 } }
      ]
    },
    {
      q: '理想的成功長什麼樣子？',
      options: [
        { text: '我的作品在人們心中留下深刻印記', score: { storyteller: 2 } },
        { text: '建造一個被廣泛使用的系統', score: { builder: 2 } },
        { text: '建立一個充滿信任的社群', score: { connector: 2 } },
        { text: '開創新的領域', score: { experimenter: 2 } },
        { text: '培育出一代有思想的創作者', score: { teacher: 2 } }
      ]
    },
    {
      q: '你傾向如何開始創作？',
      options: [
        { text: '從一個真實的個人經歷開始', score: { storyteller: 2 } },
        { text: '看到一個問題，想辦法解決', score: { builder: 2 } },
        { text: '邀集有趣的人，集思廣益', score: { connector: 2 } },
        { text: '「如果...會怎樣？」好奇心驅動', score: { experimenter: 2 } },
        { text: '發現一個自己想懂的領域', score: { teacher: 2 } }
      ]
    },
    {
      q: '你如何看待失敗？',
      options: [
        { text: '失敗是理解人性的機會', score: { storyteller: 2 } },
        { text: '失敗意味著需要改進', score: { builder: 2 } },
        { text: '失敗是認識新人的入口', score: { connector: 2 } },
        { text: '失敗是最好的老師', score: { experimenter: 2 } },
        { text: '失敗讓我看到教學的盲點', score: { teacher: 2 } }
      ]
    },
    {
      q: '在多巴胺成癮的社會裡，你最抗拒的誘惑是？',
      options: [
        { text: '容易在短視頻迷失', score: { storyteller: 2 } },
        { text: '被無窮功能想像誘惑', score: { builder: 2 } },
        { text: '被無限人脈擴展誘惑', score: { connector: 2 } },
        { text: '被永遠有新東西學誘惑', score: { experimenter: 2 } },
        { text: '被「完美教學」幻想誘惑', score: { teacher: 2 } }
      ]
    }
  ];

  const calculateType = (selectedAnswers) => {
    const scores = {
      storyteller: 0,
      builder: 0,
      connector: 0,
      experimenter: 0,
      teacher: 0
    };

    selectedAnswers.forEach((answerIdx, qIdx) => {
      const selected = questions[qIdx].options[answerIdx];
      Object.keys(selected.score).forEach(type => {
        scores[type] += selected.score[type];
      });
    });

    let maxType = 'storyteller';
    let maxScore = 0;
    Object.keys(scores).forEach(type => {
      if (scores[type] > maxScore) {
        maxScore = scores[type];
        maxType = type;
      }
    });

    return maxType;
  };

  const handleAnswer = (optionIdx) => {
    const newAnswers = [...answers, optionIdx];
    setAnswers(newAnswers);

    if (newAnswers.length === questions.length) {
      const result = calculateType(newAnswers);
      setUserType(result);
      setTimeout(() => setPhase('result'), 300);
    } else {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handleRestart = () => {
    setPhase('landing');
    setCurrentQuestion(0);
    setAnswers([]);
    setUserType(null);
  };

  return (
    <div className="bg-slate-900 min-h-screen font-sans">
      <AnimatePresence mode="wait">
        {phase === 'landing' && (
          <motion.div
            key="landing"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="h-screen flex flex-col items-center justify-center bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 relative overflow-hidden px-6"
          >
            <motion.div className="relative z-10 text-center max-w-2xl">
              <h1 className="text-5xl md:text-7xl font-bold text-white mb-4">
                消費 vs 創造
              </h1>
              <p className="text-xl md:text-2xl text-slate-200 mb-8">
                為什麼創造會比消費更上癮？
              </p>

              <motion.button
                onClick={() => setPhase('opening')}
                whileHover={{ scale: 1.05 }}
                className="bg-gradient-to-r from-amber-500 to-orange-500 text-white px-8 py-4 rounded-full text-lg font-semibold flex items-center gap-2 mx-auto hover:shadow-lg"
              >
                發現你的創作者原型
                <ChevronRight className="w-5 h-5" />
              </motion.button>
            </motion.div>
          </motion.div>
        )}

        {phase === 'opening' && (
          <motion.div
            key="opening"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="min-h-screen bg-slate-50 px-6 py-12"
          >
            <div className="max-w-3xl mx-auto">
              <h2 className="text-4xl font-bold text-slate-900 mb-6">
                你是哪一種創作者？
              </h2>
              <div className="space-y-4 text-slate-600 text-lg mb-8">
                <p>
                  創作不是只有一種形態。有人透過故事感動人心，有人透過工具改變世界...
                </p>
                <p>
                  接下來的 <strong>8 個問題</strong> 會幫你發現自己獨特的創作天賦。
                </p>
              </div>

              <button
                onClick={() => {
                  setPhase('quiz');
                  setCurrentQuestion(0);
                }}
                className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white px-8 py-4 rounded-lg text-lg font-semibold flex items-center gap-2 hover:shadow-lg"
              >
                開始診斷 (2 分鐘)
                <Zap className="w-5 h-5" />
              </button>
            </div>
          </motion.div>
        )}

        {phase === 'quiz' && (
          <motion.div
            key="quiz"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800 px-6 py-12"
          >
            <div className="max-w-2xl mx-auto">
              <div className="mb-8">
                <div className="flex justify-between mb-2">
                  <span className="text-slate-300 text-sm">
                    {currentQuestion + 1} / {questions.length}
                  </span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <motion.div
                    className="h-full bg-gradient-to-r from-amber-500 to-orange-500 rounded-full"
                    initial={{ width: 0 }}
                    animate={{
                      width: `${((currentQuestion + 1) / questions.length) * 100}%`
                    }}
                  />
                </div>
              </div>

              <motion.div
                key={currentQuestion}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-slate-800 rounded-xl p-8 mb-8"
              >
                <h3 className="text-2xl font-bold text-white mb-8">
                  {questions[currentQuestion].q}
                </h3>

                <div className="space-y-3">
                  {questions[currentQuestion].options.map((option, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleAnswer(idx)}
                      className="w-full p-4 bg-slate-700 hover:bg-slate-600 text-white rounded-lg text-left transition-colors"
                    >
                      {option.text}
                    </button>
                  ))}
                </div>
              </motion.div>
            </div>
          </motion.div>
        )}

        {phase === 'result' && (
          <motion.div
            key="result"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800 px-6 py-12"
          >
            <div className="max-w-3xl mx-auto">
              {userType && (
                <motion.div
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  className={`bg-gradient-to-br ${creatorTypes[userType].color} rounded-2xl p-12 text-white mb-8 shadow-2xl`}
                >
                  <div className="text-7xl mb-4">
                    {creatorTypes[userType].emoji}
                  </div>
                  <h2 className="text-4xl font-bold mb-2">
                    {creatorTypes[userType].name}
                  </h2>
                  <p className="text-lg opacity-90">
                    {creatorTypes[userType].description}
                  </p>

                  <div className="mt-8 flex gap-3 flex-wrap">
                    <a
                      href="https://aiagentcommander.substack.com"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg font-semibold"
                    >
                      <Mail className="w-4 h-4" />
                      訂閱 Substack
                    </a>
                    <button
                      onClick={handleRestart}
                      className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg font-semibold"
                    >
                      重新診斷
                    </button>
                  </div>
                </motion.div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default CreatorDiagnostic;
```

### 4. 本地測試

```bash
npm run dev
```

打開 http://localhost:3000，測試功能是否正常

---

## 第二步：部署到 Vercel（10 分鐘）

### 1. 準備 GitHub（如果還沒有）

```bash
# 初始化 git
git init
git add .
git commit -m "Initial commit: Creator diagnostic app"

# 推送到 GitHub（需要先創建 GitHub repository）
git remote add origin https://github.com/你的用戶名/ai-commander-web.git
git branch -M main
git push -u origin main
```

**如果沒有 GitHub：**
- 去 https://github.com，註冊帳號
- 創建新 repository「ai-commander-web」
- 按上面的指令推送

### 2. 連接 Vercel

```bash
# 安裝 Vercel CLI
npm i -g vercel

# 部署
vercel
```

**按提示：**
```
? Set up and deploy "~/projects/ai-commander-web"? (y/N) 
→ y

? Which scope do you want to deploy to?
→ 選你自己的帳號

? Link to existing project?
→ N

? What's your project's name?
→ ai-commander-web

? In which directory is your code located?
→ ./ (按 Enter)

? Want to override the settings? 
→ N
```

**預期結果：**
```
✓ Linked to your-account/ai-commander-web
✓ Production deployment
✓ https://ai-commander-web.vercel.app
```

---

## 第三步：連接自定義域名（10 分鐘）

### 1. 在 Vercel 中添加域名

- 打開 https://vercel.com/dashboard
- 選擇「ai-commander-web」項目
- 進入「Settings → Domains」
- 輸入 `aiagentcommander.com`
- 複製 NS 記錄（Nameserver）

### 2. 更新域名 DNS

登陸你的域名註冊商（Namecheap、Google Domains 等）：

- 進入 DNS 設定
- 刪除舊的 NS 記錄
- 添加 Vercel 提供的 NS 記錄

**需要 24-48 小時生效，但通常 1 小時內就可以**

---

## 第四步：測試發布（5 分鐘）

### 1. 驗證上線

訪問：`https://aiagentcommander.com`（或 `ai-commander-web.vercel.app`）

檢查清單：
- [ ] 首頁加載正常
- [ ] 動畫順暢（沒有卡頓）
- [ ] 按鈕可點擊
- [ ] 問卷能完成
- [ ] 結果頁顯示
- [ ] 「訂閱 Substack」鏈接正確
- [ ] 移動端響應式

### 2. 分享鏈接

```
分享文本範本：

「我做了一份《創作者原型診斷》，發現自己是 X 類型創作者。
你呢？一起來診斷你的創作天賦：
https://aiagentcommander.com

這是我的新項目——雙星計畫的一部分：
📖 Substack 是發行星（深度內容 + 變現）
🌐 互動網頁是知識主星（體驗 + 引力）」
```

---

## 常見問題

### Q: 部署後沒有顯示？
**A:** 檢查：
1. Vercel 部署狀態（應該有綠色 checkmark）
2. 瀏覽器緩存（Ctrl+Shift+Delete 清除）
3. DNS 生效（可能需要 24 小時）

### Q: 動畫卡頓？
**A:** 
- 檢查瀏覽器是否是最新版
- 試試 Chrome/Safari（Firefox 有時動畫性能差）
- 關閉其他標籤頁

### Q: 想修改問卷內容？
**A:**
1. 修改本地 `app/page.jsx`
2. `git add . && git commit -m "Update quiz content"`
3. `git push`
4. Vercel 自動重新部署（1-2 分鐘）

---

## 下一步行動

✅ **部署成功後：**

1. **在 Substack 發佈歡迎文**
   ```
   主旨：「我做了一份診斷，幫你發現創作者原型」
   
   內容：
   - 簡介診斷（2-3 句）
   - 截圖或 GIF 演示
   - 鏈接：https://aiagentcommander.com
   - CTA：「做診斷，獲得個性化建議，加入社群」
   ```

2. **邀請 5-10 人內測**
   - 發送鏈接給朋友、社群領袖
   - 收集反饋
   - 截圖他們的結果（徵求許可）

3. **在 LinkedIn/Twitter 分享**
   - 發佈內測體驗帖
   - 邀請早期用戶

---

## 技術支援

遇到問題？檢查：
1. **Vercel 文檔**：https://vercel.com/docs
2. **Next.js 調試**：`npm run dev` 的終端輸出
3. **瀏覽器開發者工具**：F12，檢查 Console 錯誤

---

**恭喜！你現在有了一個可公開分享的互動診斷網頁 🚀**

**下一步：開始收集數據，優化轉化，建立社群。**
