'use client';

import React, { useState, useEffect } from 'react';
import { ChevronRight, Heart, Zap, Brain, Users, Award, Share2, Mail } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const CreatorDiagnostic = () => {
  const [phase, setPhase] = useState('landing'); // landing, opening, quiz, result, community
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [userType, setUserType] = useState(null);
  const [scrollProgress, setScrollProgress] = useState(0);

  // 創作者原型定義
  const creatorTypes = {
    storyteller: {
      name: '說故事者',
      emoji: '📖',
      description: '你用敘事和情感連結驅動人心，是內容創造的靈魂。',
      trait: '高共鳴 + 高執行力',
      dopamine: '社交反饋 + 粉絲互動',
      nextStep: '開始寫你的故事，在 Substack 發表第一篇。',
      color: 'from-rose-500 to-pink-500'
    },
    builder: {
      name: '建構者',
      emoji: '🔨',
      description: '你將想法變成產品、系統、工具，是創新的推進者。',
      trait: '高技術 + 高創新',
      dopamine: '功能完成 + 用戶價值',
      nextStep: '發佈你的第一個 Skill 或工具模板。',
      color: 'from-blue-500 to-cyan-500'
    },
    connector: {
      name: '連結者',
      emoji: '🌐',
      description: '你連接人、想法和機會，是生態的樞紐。',
      trait: '高社交 + 高洞察',
      dopamine: '人脈積累 + 機會發現',
      nextStep: '組建你的社群，發起討論話題。',
      color: 'from-purple-500 to-indigo-500'
    },
    experimenter: {
      name: '實驗者',
      emoji: '⚗️',
      description: '你透過不斷嘗試發現新路徑，是探索的先鋒。',
      trait: '高創新 + 高學習力',
      dopamine: '新發現 + 未知探索',
      nextStep: '記錄你的實驗日記，分享失敗與成功。',
      color: 'from-amber-500 to-orange-500'
    },
    teacher: {
      name: '教育者',
      emoji: '👨‍🏫',
      description: '你將複雜化簡，用知識賦能他人，是啟蒙者。',
      trait: '高理解 + 高傳播',
      dopamine: '被讚美 + 看到學生進步',
      nextStep: '開課、錄製教學視頻或發表教程。',
      color: 'from-green-500 to-emerald-500'
    }
  };

  const questions = [
    {
      q: '當你完成一個創作項目後，你最開心的感受是什麼？',
      options: [
        { text: '看到人們被你的故事感動', score: { storyteller: 2 } },
        { text: '看到功能正常運作，解決了問題', score: { builder: 2 } },
        { text: '看到社群聚集在你的想法周圍', score: { connector: 2 } },
        { text: '發現新的可能性和方向', score: { experimenter: 2 } },
        { text: '知道有人通過我的教學學到東西', score: { teacher: 2 } }
      ]
    },
    {
      q: '你在哪個時刻會感到最有動力？',
      options: [
        { text: '讀者在評論中說你改變了他們的想法', score: { storyteller: 2 } },
        { text: '產品上線，有人使用了我做的東西', score: { builder: 2 } },
        { text: '引薦了兩個對的人相識，看他們一拍即合', score: { connector: 2 } },
        { text: '發現別人沒試過的新領域', score: { experimenter: 2 } },
        { text: '學生問出深度問題，說明他們真的理解了', score: { teacher: 2 } }
      ]
    },
    {
      q: '創作過程中，你最投入時間的是？',
      options: [
        { text: '打磨細節，讓故事更感人', score: { storyteller: 2 } },
        { text: '解決技術問題，使產品更好用', score: { builder: 2 } },
        { text: '與社群溝通，理解大家的需求', score: { connector: 2 } },
        { text: '試驗新想法，看看會發生什麼', score: { experimenter: 2 } },
        { text: '設計教學框架，讓學習曲線平緩', score: { teacher: 2 } }
      ]
    },
    {
      q: '你最害怕什麼？',
      options: [
        { text: '人們不理解我想表達的真實情感', score: { storyteller: 2 } },
        { text: '我建造的東西沒人用，或用起來不好', score: { builder: 2 } },
        { text: '被孤立，失去社群和人脈網絡', score: { connector: 2 } },
        { text: '被困在舒適區，停止探索', score: { experimenter: 2 } },
        { text: '我的知識沒有幫到任何人', score: { teacher: 2 } }
      ]
    },
    {
      q: '理想的成功長什麼樣子？',
      options: [
        { text: '我的作品在人們心中留下深刻印記', score: { storyteller: 2 } },
        { text: '建造一個被廣泛使用的系統或產品', score: { builder: 2 } },
        { text: '建立一個充滿信任和協作的社群', score: { connector: 2 } },
        { text: '開創新的領域或改變現有範式', score: { experimenter: 2 } },
        { text: '培育出一代有思想的創作者', score: { teacher: 2 } }
      ]
    },
    {
      q: '你傾向如何開始創作？',
      options: [
        { text: '從一個真實的個人經歷或情感開始', score: { storyteller: 2 } },
        { text: '看到一個問題，然後想辦法解決', score: { builder: 2 } },
        { text: '邀集有趣的人，集思廣益', score: { connector: 2 } },
        { text: '「如果...會怎樣？」好奇心驅動', score: { experimenter: 2 } },
        { text: '發現一個自己還不懂但想懂的領域', score: { teacher: 2 } }
      ]
    },
    {
      q: '你如何看待失敗？',
      options: [
        { text: '失敗是更深入理解人性的機會', score: { storyteller: 2 } },
        { text: '失敗意味著需要改進設計或方法', score: { builder: 2 } },
        { text: '失敗是認識新人、找到新機遇的入口', score: { connector: 2 } },
        { text: '失敗是最好的老師，充滿學習', score: { experimenter: 2 } },
        { text: '失敗讓我看到教學中的盲點', score: { teacher: 2 } }
      ]
    },
    {
      q: '在多巴胺上癮的社會裡，你最抗拒的誘惑是？',
      options: [
        { text: '容易在短視頻裡迷失，忘記創作', score: { storyteller: 2 } },
        { text: '被無窮的功能想像誘惑，無法發佈', score: { builder: 2 } },
        { text: '被無限人脈擴展誘惑，忽視深度關係', score: { connector: 2 } },
        { text: '被永遠有新東西可學誘惑，無法聚焦', score: { experimenter: 2 } },
        { text: '被「完美教學」幻想誘惑，無法開課', score: { teacher: 2 } }
      ]
    }
  ];

  // 計算結果
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

  // 開篇動畫組件
  const OpeningAnimation = () => (
    <div className="h-screen flex flex-col items-center justify-center bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 relative overflow-hidden">
      {/* 背景動畫 */}
      <div className="absolute inset-0 opacity-30">
        <motion.div
          className="absolute w-96 h-96 bg-rose-500 rounded-full blur-3xl"
          animate={{ y: [0, 50, 0], x: [0, 30, 0] }}
          transition={{ duration: 8, repeat: Infinity }}
          style={{ top: '10%', left: '10%' }}
        />
        <motion.div
          className="absolute w-96 h-96 bg-blue-500 rounded-full blur-3xl"
          animate={{ y: [0, -50, 0], x: [0, -30, 0] }}
          transition={{ duration: 10, repeat: Infinity }}
          style={{ bottom: '10%', right: '10%' }}
        />
      </div>

      <motion.div
        className="relative z-10 text-center max-w-2xl px-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <h1 className="text-5xl md:text-7xl font-bold text-white mb-4 tracking-tight">
          <motion.span
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 3, repeat: Infinity }}
          >
            消費 vs 創造
          </motion.span>
        </h1>

        <p className="text-xl md:text-2xl text-slate-200 mb-8 font-light">
          為什麼創造會比消費更上癮？
        </p>

        {/* 對比動畫圖表 */}
        <div className="mt-12 h-64 flex items-end justify-center gap-12 mb-12">
          {/* 消費快感曲線 */}
          <motion.div className="flex flex-col items-center">
            <motion.div
              className="w-2 bg-gradient-to-t from-red-500 to-red-300 rounded-full"
              initial={{ height: 200 }}
              animate={{ height: [200, 150, 100, 50, 50] }}
              transition={{ duration: 4, repeat: Infinity }}
            />
            <p className="text-sm text-slate-300 mt-2">消費快感</p>
            <p className="text-xs text-slate-400">遞減</p>
          </motion.div>

          {/* 創造快感曲線 */}
          <motion.div className="flex flex-col items-center">
            <motion.div
              className="w-2 bg-gradient-to-t from-green-500 to-green-300 rounded-full"
              initial={{ height: 50 }}
              animate={{ height: [50, 100, 150, 200, 200] }}
              transition={{ duration: 4, repeat: Infinity }}
            />
            <p className="text-sm text-slate-300 mt-2">創造快感</p>
            <p className="text-xs text-slate-400">成長</p>
          </motion.div>
        </div>

        <motion.button
          onClick={() => setPhase('opening')}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="bg-gradient-to-r from-amber-500 to-orange-500 text-white px-8 py-4 rounded-full text-lg font-semibold flex items-center gap-2 mx-auto hover:shadow-lg hover:shadow-orange-500/50 transition-all"
        >
          發現你的創作者原型
          <ChevronRight className="w-5 h-5" />
        </motion.button>
      </motion.div>
    </div>
  );

  // 開篇介紹
  const OpeningPhase = () => (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen bg-slate-50 px-6 py-12"
    >
      <div className="max-w-3xl mx-auto">
        <motion.h2
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="text-4xl font-bold text-slate-900 mb-6"
        >
          你是哪一種創作者？
        </motion.h2>

        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="space-y-4 text-slate-600 text-lg leading-relaxed mb-8"
        >
          <p>
            創作不是只有一種形態。有人透過故事感動人心，有人透過工具改變世界，有人透過連結建立社群...
          </p>
          <p>
            這份診斷會幫你發現：<strong>你獨特的創作天賦是什麼？</strong>
          </p>
          <p>
            接下來的 <strong>8 個問題</strong> 會引導你理解自己的創造力來源，以及如何構建一個比消費更上癮的創作習慣。
          </p>
        </motion.div>

        <motion.button
          onClick={() => {
            setPhase('quiz');
            setCurrentQuestion(0);
          }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white px-8 py-4 rounded-lg text-lg font-semibold flex items-center gap-2 hover:shadow-lg hover:shadow-blue-600/50 transition-all"
        >
          開始診斷 (2 分鐘)
          <Zap className="w-5 h-5" />
        </motion.button>
      </div>
    </motion.div>
  );

  // 問卷界面
  const QuizPhase = () => (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800 px-6 py-12"
    >
      <div className="max-w-2xl mx-auto">
        {/* 進度條 */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-slate-300 text-sm">
              問題 {currentQuestion + 1} / {questions.length}
            </span>
            <span className="text-slate-300 text-sm">
              {Math.round(((currentQuestion + 1) / questions.length) * 100)}%
            </span>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2 overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-amber-500 to-orange-500"
              initial={{ width: 0 }}
              animate={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
        </div>

        <AnimatePresence mode="wait">
          <motion.div
            key={currentQuestion}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="bg-slate-800 rounded-xl p-8 mb-8"
          >
            <h3 className="text-2xl font-bold text-white mb-8">
              {questions[currentQuestion].q}
            </h3>

            <div className="space-y-3">
              {questions[currentQuestion].options.map((option, idx) => (
                <motion.button
                  key={idx}
                  onClick={() => handleAnswer(idx)}
                  whileHover={{ scale: 1.02, x: 4 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full p-4 bg-slate-700 hover:bg-slate-600 text-white rounded-lg text-left transition-colors border border-slate-600 hover:border-slate-500"
                >
                  {option.text}
                </motion.button>
              ))}
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </motion.div>
  );

  // 結果頁面
  const ResultPhase = () => {
    const type = creatorTypes[userType];
    const communityMembers = [
      { name: '小林', type: 'storyteller', work: '發表了 12 篇文章' },
      { name: '張偉', type: 'builder', work: '開源了 AI Skill 庫' },
      { name: '李美', type: 'connector', work: '組織了 5 場社群活動' },
      { name: '王傑', type: 'teacher', work: '錄製了 20 個教程' },
      { name: '陳思', type: 'experimenter', work: '發起了 3 個新實驗' }
    ];

    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800 px-6 py-12"
      >
        <div className="max-w-3xl mx-auto">
          {/* 結果卡片 */}
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.5 }}
            className={`bg-gradient-to-br ${type.color} rounded-2xl p-12 text-white mb-8 shadow-2xl`}
          >
            <div className="text-7xl mb-4">{type.emoji}</div>
            <h2 className="text-4xl font-bold mb-2">{type.name}</h2>
            <p className="text-lg opacity-90 mb-6">{type.description}</p>

            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-white/10 rounded-lg p-4 backdrop-blur">
                <p className="text-sm opacity-75">特質</p>
                <p className="font-semibold">{type.trait}</p>
              </div>
              <div className="bg-white/10 rounded-lg p-4 backdrop-blur">
                <p className="text-sm opacity-75">快感來源</p>
                <p className="font-semibold">{type.dopamine}</p>
              </div>
            </div>

            <div className="bg-white/20 rounded-lg p-6 backdrop-blur-sm mb-6">
              <h4 className="font-semibold mb-2">🎯 你的下一步：</h4>
              <p>{type.nextStep}</p>
            </div>

            <div className="flex gap-3 flex-wrap">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex items-center gap-2 bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg font-semibold backdrop-blur transition-all"
              >
                <Share2 className="w-4 h-4" />
                分享結果
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex items-center gap-2 bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg font-semibold backdrop-blur transition-all"
              >
                <Mail className="w-4 h-4" />
                訂閱專屬內容
              </motion.button>
            </div>
          </motion.div>

          {/* 社群展示 */}
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="bg-slate-800 rounded-xl p-8 mb-8"
          >
            <h3 className="text-2xl font-bold text-white mb-6">🌟 新人類聯盟的創作者</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {communityMembers.map((member, idx) => (
                <motion.div
                  key={idx}
                  whileHover={{ scale: 1.02 }}
                  className="bg-slate-700 rounded-lg p-4 border border-slate-600"
                >
                  <p className="font-semibold text-white mb-1">{member.name}</p>
                  <p className="text-sm text-slate-300 mb-2">{creatorTypes[member.type].name}</p>
                  <p className="text-xs text-slate-400">{member.work}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* 邀請加入 */}
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="bg-slate-800 rounded-xl p-8 text-center border border-slate-600"
          >
            <h3 className="text-2xl font-bold text-white mb-4">準備好加入了嗎？</h3>
            <p className="text-slate-300 mb-6">
              新人類聯盟是一個由創作者組成的社群，我們互相支持、共享 Skill、構建創意引力。
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <motion.a
                href="https://aiagentcommander.substack.com"
                target="_blank"
                rel="noopener noreferrer"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-gradient-to-r from-amber-500 to-orange-500 text-white px-8 py-3 rounded-lg font-semibold hover:shadow-lg hover:shadow-orange-500/50 transition-all"
              >
                訂閱 Substack
              </motion.a>
              <motion.button
                onClick={handleRestart}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-slate-700 hover:bg-slate-600 text-white px-8 py-3 rounded-lg font-semibold transition-all"
              >
                重新診斷
              </motion.button>
            </div>
          </motion.div>
        </div>
      </motion.div>
    );
  };

  return (
    <div className="bg-slate-900 min-h-screen font-sans">
      <AnimatePresence mode="wait">
        {phase === 'landing' && <OpeningAnimation key="landing" />}
        {phase === 'opening' && <OpeningPhase key="opening" />}
        {phase === 'quiz' && <QuizPhase key="quiz" />}
        {phase === 'result' && <ResultPhase key="result" />}
      </AnimatePresence>
    </div>
  );
};

export default CreatorDiagnostic;
