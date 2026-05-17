# MEMORY：Agent 的記憶系統

> **記憶決定了一個 Agent 能否真正認識你。**
>
> 沒有記憶，Agent 就是每次都從零開始。有了記憶，Agent 才能說「我理解你」。

---

## 一句話：什麼是 Memory

**Memory 是 Agent 的長期資料庫，記錄用戶的偏好、行為、決策模式，讓 Agent 從第二次交互開始就能認識你。**

---

## Memory 在 Agent OS 中的位置

```
┌─────────────────────────────────────┐
│ 層 4：反饋層 (Feedback & Learning)  │
│         ↓ 學習 & 優化               │
│      (更新到 Memory)                │
├─────────────────────────────────────┤
│ 層 3：執行層 (Execution)            │
│         ↓ 任務執行                  │
│      (使用 Memory 個人化)           │
├─────────────────────────────────────┤
│ 層 2：決策層 (Reasoning)            │
│         ↓ AI 推理                   │
│  (調用 Memory 增強上下文)           │
├─────────────────────────────────────┤
│ 層 1：感知層 (Perception)           │
│         ↓ 環境信號                  │
│   (同步 & 更新到 Memory)            │
└─────────────────────────────────────┘
          ↑ ↑ ↑ ↑ ↑
     MEMORY 貫穿所有層
```

**Memory 在感知層**：新數據進來時，實時同步到 Memory
**Memory 在決策層**：AI 推理時，調用 Memory 增強上下文理解
**Memory 在執行層**：執行任務時，根據 Memory 中的偏好進行個人化
**Memory 在反饋層**：反饋進來時，更新 Memory，改進下次行為

---

## Memory 的三大分類

### 分類 1：短期記憶 (Episodic Memory)

**定義**：最近的對話、最近的交互、當前會話的上下文

**特徵**：
- 時間跨度：數秒到數小時
- 容量：大（完整對話記錄）
- 檢索速度：極快（就在眼前）
- 遺忘速度：快（會話結束或 24 小時後清除）

**應用例**：
- 今天上午的對話記錄（幫 Agent 理解「你之前問過我什麼」）
- 目前正在執行的任務（「我現在正在幫你選衣服」）

**技術實現**：LLM 的 context window（通常 8K-200K token）

---

### 分類 2：長期記憶 (Semantic Memory)

**定義**：用戶的穩定特徵、偏好、身份信息

**特徵**：
- 時間跨度：數週到數年
- 容量：中等（結構化的關鍵信息）
- 檢索速度：中等（需要查詢和過濾）
- 遺忘速度：慢（除非用戶主動修改）

**應用例**：
- 用戶的穿衣風格（「喜歡極簡風」「不喜歡過於暴露」「偏好冷色調」）
- 用戶的工作行程（「每週二下午有重要會議」「週末喜歡戶外活動」）
- 用戶的購物偏好（「價格敏感」「重視質量」「環保意識」）

**技術實現**：結構化數據庫（JSON、向量數據庫）

---

### 分類 3：程序記憶 (Procedural Memory)

**定義**：用戶的行為模式、決策習慣、系統偏好

**特徵**：
- 時間跨度：長期（用戶的生活習慣）
- 容量：小（只記錄模式和規則）
- 檢索速度：快（模式匹配）
- 遺忘速度：慢（除非用戶改變習慣）

**應用例**：
- 用戶的決策模式（「每次選擇都偏好最便宜的選項」）
- 用戶的時間偏好（「早上 8 點最活躍」「周末傾向休息」）
- 用戶的溝通風格（「喜歡簡潔的回答」「不喜歡長篇大論」）

**技術實現**：行為分析、機器學習模型

---

## Memory vs Graphify：不同的存儲哲學

### 對比表

| 維度 | Memory | Graphify |
|------|--------|----------|
| **存儲位置** | Agent 的本地數據庫（跨會話保存） | 外部檔案系統 + 知識圖譜（graph.json） |
| **適合內容** | 小型關鍵事實、偏好、決策模式 | 大段文字、代碼、報告、深度筆記 |
| **查詢方式** | Memory API（add/query/update/delete） | graphify query/explain（語義檢索） |
| **是否需要檔案** | 不需要（直接寫入 Memory） | 必須先有實體檔案 |
| **檢索邏輯** | 向量相似度 + 時間衰減 | 知識圖的社區發現 + 語義關聯 |
| **更新頻率** | 高（每次交互都可能更新） | 低（通常手動或定期更新） |
| **用途** | 讓 Agent 認識「你」 | 讓 Agent 理解「知識領域」 |

### 關鍵區別

**Memory 回答的問題**：
- 「我（Agent）對這個用戶的了解有多深？」
- 「這個用戶上次喜歡什麼？」
- 「根據用戶的歷史行為，我應該推薦什麼？」

**Graphify 回答的問題**：
- 「Agent OS 和 Software 3.0 之間有什麼關聯？」
- 「誰寫過關於虛擬穿衣的內容？」
- 「個人時尚助理和 NANA 故事系統的共同點是什麼？」

---

## Memory 的實現架構

### 層 1：數據收集 (Data Collection)

```
用戶交互
  ├─ 顯式反饋（用戶主動告訴我）
  │  ├─ 「我喜歡簡潔的風格」
  │  ├─ 「我下週有5場會議」
  │  └─ 「我不喜歡這個推薦」
  │
  ├─ 隱式反饋（用戶的行為傳達）
  │  ├─ 點擊了什麼（行為信號）
  │  ├─ 停留了多久（注意力信號）
  │  ├─ 選擇了什麼（偏好信號）
  │  └─ 何時交互（時間偏好）
  │
  └─ 環境數據（系統觀察到的）
     ├─ 天氣變化
     ├─ 日程變動
     ├─ 位置變化
     └─ 時間趨勢
```

### 層 2：數據正規化 (Normalization)

```
原始數據 → 結構化 → 向量化 → 儲存到 Memory

例子：
「我下週一下午2點有個重要的客戶演講」

↓

結構化：
{
  "event_type": "meeting",
  "importance": "high",
  "context": "business",
  "time": "2026-05-27 14:00",
  "duration": "unknown",
  "audience": "client",
  "activity": "presentation"
}

↓

向量化：
[0.234, -0.123, 0.456, ...] (384-dim embedding)

↓

存儲：
memory.add({
  "id": "event_2026_05_27",
  "type": "schedule_item",
  "structured_data": {...},
  "embedding": [...],
  "timestamp": "2026-05-23 15:30",
  "relevance_score": 0.95
})
```

### 層 3：向量檢索 (Vector Retrieval)

```
新請求：「推薦明天穿什麼」

↓

1️⃣ 用戶特徵檢索
   向量化「明天」、「穿衣」
   在 Memory 中搜索相關的
   - 時間偏好（明天是周一）
   - 活動計劃（明天有什麼）
   - 穿衣歷史（明天天氣條件下的歷史選擇）

↓

2️⃣ 上下文聚合
   Memory 返回：
   {
     "upcoming_activities": [
       {"type": "meeting", "formality": "high"},
       {"type": "lunch", "formality": "low"}
     ],
     "style_preference": "minimalist, cool_tones",
     "weather": "22°C, 60% humidity",
     "similar_past_days": [
       {"date": "2026-05-15", "outfit": "gray_blazer+white_shirt"},
       {"date": "2026-05-08", "outfit": "navy_sweater+black_pants"}
     ]
   }

↓

3️⃣ AI 推理（在決策層）
   融合 Memory 信息 + 衣柜庫存 + 當前偏好
   生成 5 套推薦
```

### 層 4：持續學習 (Continuous Learning)

```
用戶反饋 → 更新 Memory

例子：
用戶選擇了推薦的穿衣方案 A，而不是 B

↓

分析：
- 方案 A：白色簡潔襯衫 + 深藍褲子
- 方案 B：彩色圖案上衣 + 牛仔褲

↓

Memory 更新：
{
  "style_confidence": 0.92,
  "color_preference": {
    "white": +0.15,
    "navy": +0.12,
    "colorful_patterns": -0.08
  },
  "formality_tolerance": "adjusting upward",
  "pattern_choice_timestamp": "2026-05-23 08:15"
}

↓

下次推薦時，AI 會參考這個更新過的 Memory
自動調整推薦，越來越准確
```

---

## Memory 在四層 Agent OS 中的應用

### 在感知層：實時同步

```
天氣 API → 發現今天溫度下降 5°C
→ Memory.update("weather_trend", {...})

日程 API → 發現新增了下午的重要會議
→ Memory.update("schedule", {...})

衣柜掃描 → 發現新購買的冬衣
→ Memory.update("wardrobe_inventory", {...})

用戶位置 → 發現用戶在公司
→ Memory.update("current_context", {...})
```

### 在決策層：增強推理

```
Claude 推理引擎：
「根據 Memory，我知道：
- 用戶下午有客戶會議（高正式度需求）
- 用戶今年偏好簡潔風格（更新於5月15日）
- 用戶的膚色是暖皮（偏好暖色調）
- 氣溫22°C（中等厚度衣物）

基於這些信息，我應該推薦正式但簡潔的穿衣方案」
```

### 在執行層：個人化輸出

```
Memory 指導下的個人化：

用戶 A（喜歡詳細分析）→ 返回「為什麼選這套」的詳細解釋
用戶 B（喜歡快速決策）→ 只返回推薦，不要廢話
用戶 C（環保意識強）→ 優先推薦可持續衣物
用戶 D（預算敏感）→ 優先推薦高性價比方案

同樣的 AI，但因為 Memory 記錄了偏好，
輸出對每個用戶都是完全個人化的
```

### 在反饋層：不斷優化

```
反饋循環 1:
用戶點讚推薦 A → Memory 提高「這類風格」的得分

反饋循環 2:
用戶拒絕推薦 B → Memory 降低「這類風格」的得分

反饋循環 3:
用戶買了推薦中的衣服 → Memory 大幅提高「購買意圖」信號

多個循環疊加 →
Agent 對用戶的認識越來越准確 →
推薦質量不斷提升 →
用戶滿意度上升
```

---

## Memory 的技術實現

### 存儲引擎選擇

| 技術 | 優點 | 缺點 | 適用場景 |
|------|------|------|---------|
| **向量數據庫** (Pinecone/Weaviate) | 快速語義搜索、支持混合檢索 | 成本高、需維護 | 大規模、多用戶 Agent |
| **本地嵌入** (LLama-Index) | 隱私安全、成本低、離線可用 | 檢索速度較慢 | 個人 Agent、小規模 |
| **PostgreSQL + pgvector** | 開源、可靠、SQL 查詢 | 需自己管理 | 中等規模、開源優先 |
| **Redis** | 極快的內存讀寫、支持過期時間 | 容量有限、成本高 | 短期記憶、高頻訪問 |

**推薦組合**：
- **短期記憶**：Redis（快速訪問）
- **長期記憶**：向量數據庫（語義搜索）
- **程序記憶**：PostgreSQL（結構化查詢）

### API 設計

```python
# Memory 的核心 API

# 1. 添加記憶
memory.add(
  type="user_preference",
  content="喜歡簡潔風格",
  tags=["style", "fashion"],
  metadata={"importance": 0.9, "source": "explicit"},
  ttl=None  # 永久存儲
)

# 2. 檢索記憶
memories = memory.search(
  query="風格偏好",
  top_k=5,
  filter={"type": "user_preference"},
  recency_weight=0.3  # 30% 權重給時間新鮮度
)

# 3. 更新記憶
memory.update(
  id="pref_2026_05_15",
  updates={"confidence": 0.95},
  increment={"style_score": 0.1}
)

# 4. 刪除記憶
memory.delete(
  id="old_pref_2024_01_01"  # 刪除過期記憶
)

# 5. 批量操作
memory.batch_add([
  {"type": "schedule", "content": "..."},
  {"type": "preference", "content": "..."}
])
```

---

## Memory 的個人化案例

### 案例 1：個人時尚助理的 Memory

```json
{
  "user_id": "user_001",
  "memory_version": "2026-05-23T10:30:00Z",
  "style_profile": {
    "aesthetic": "minimalist",
    "color_preference": {
      "whites": 0.95,
      "blacks": 0.88,
      "grays": 0.85,
      "pastels": 0.45,
      "bright_colors": 0.15
    },
    "formality_tolerance": "high_flexibility",
    "body_type": "pear_shape",
    "skin_tone": "warm",
    "budget_sensitivity": 0.7
  },
  "lifestyle_pattern": {
    "monday": {
      "formality": "high",
      "activities": ["meetings", "presentations"],
      "avg_steps": 8000
    },
    "friday": {
      "formality": "low",
      "activities": ["casual_work", "socializing"],
      "avg_steps": 6000
    },
    "weekend": {
      "formality": "very_low",
      "activities": ["outdoor", "relaxation"],
      "avg_steps": 12000
    }
  },
  "shopping_history": {
    "total_purchases": 23,
    "avg_price_point": 45,
    "preferred_brands": ["Uniqlo", "Muji", "COS"],
    "rarely_purchased_from": ["Fast fashion chains"],
    "return_rate": 0.08
  },
  "past_recommendations": {
    "high_satisfaction": [
      {"outfit_id": "rec_2026_05_15", "feedback": "bought", "satisfaction": 0.95},
      {"outfit_id": "rec_2026_05_10", "feedback": "wore_repeatedly", "satisfaction": 0.9}
    ],
    "low_satisfaction": [
      {"outfit_id": "rec_2026_04_20", "feedback": "rejected", "satisfaction": 0.2}
    ]
  },
  "real_time_context": {
    "current_weather": "22°C, clear",
    "upcoming_event": "client_meeting_at_14:00",
    "location": "office",
    "recent_purchases": ["white_blazer", "minimalist_watch"]
  }
}
```

**Memory 支撑的個人化決策**：
- 根據 Monday 的高正式度需求，優先推薦深色、簡潔的正式風格
- 根據 Pear shape 和暖皮特徵，避免過於蓬鬆或冷色的選擇
- 根據購物歷史，優先推薦價格在 $40-50 範圍內、來自偏好品牌的選擇
- 根據最近購買，建議搭配新購的白色西裝

---

### 案例 2：內容創作 Agent 的 Memory

```json
{
  "creator_id": "creator_substack_001",
  "writing_profile": {
    "preferred_topics": [
      {"topic": "AI_and_humanity", "depth_preference": "deep", "frequency": 0.4},
      {"topic": "personal_growth", "depth_preference": "medium", "frequency": 0.3},
      {"topic": "product_design", "depth_preference": "deep", "frequency": 0.2},
      {"topic": "technology_trends", "depth_preference": "shallow", "frequency": 0.1}
    ],
    "writing_style": "conversational, story-driven, evidence-based",
    "target_audience": "thoughtful professionals aged 25-45",
    "content_length_preference": "2000-3000 words per article"
  },
  "audience_engagement": {
    "subscriber_growth_rate": 0.15,
    "avg_open_rate": 0.38,
    "top_performing_content": [
      {
        "title": "引力轉移：為什麼創造比消費更上癮",
        "open_rate": 0.52,
        "key_themes": ["neuroscience", "motivation", "behavior_change"]
      }
    ],
    "least_engaging": [
      {
        "title": "Technical Deep Dive: X",
        "open_rate": 0.15,
        "key_themes": ["too_technical", "insufficient_storytelling"]
      }
    ]
  },
  "publishing_pattern": {
    "best_days": ["wednesday", "thursday"],
    "best_time": "06:00-08:00 UTC",
    "optimal_frequency": "2 per week",
    "audience_timezone": "AEST dominant (35%), EST (25%), CET (15%)"
  },
  "content_strategy": {
    "series_in_progress": [
      {
        "name": "From Addiction to Creator",
        "episode": 4,
        "expected_completion": "2026-06-15",
        "audience_anticipation": 0.9
      }
    ],
    "planned_next_series": "Personal Stylist AI",
    "cross_promotion_opportunities": ["Agent OS series", "Software 3.0"]
  }
}
```

**Memory 支撑的決策**：
- Agent 知道週三週四上午 6-8 點發布效果最好，自動排期
- Agent 知道「引力轉移」類型的內容開啟率 52%，於是推薦更多這類主題
- Agent 知道「太技術性」的內容效果差，於是在技術內容中加入故事和比喻
- Agent 知道下一個系列計劃，提前 2 週開始建立預期

---

## Memory 的隱私與安全

### 隱私原則

```
原則 1：數據最小化
- 只存儲必要的數據
- 不存儲敏感的個人信息（密碼、銀行卡等）

原則 2：用戶控制
- 用戶可隨時查看 Memory 內容
- 用戶可選擇性刪除某些記憶
- 用戶可導出自己的 Memory

原則 3：透明度
- 告訴用戶「我記得你什麼」
- 解釋「為什麼我基於這個記憶做出推薦」

原則 4：安全存儲
- Memory 加密存儲（AES-256）
- 訪問控制（只有授權的 Agent 可讀）
- 審計日誌（誰訪問了什麼數據）
```

### 實踐例子

```python
# 用戶隱私控制

# 1. 查看我的 Memory
my_memory = memory.view_all()  # 返回所有記憶

# 2. 刪除某個記憶
memory.delete("pref_2026_03_15_color")

# 3. 禁用某些記憶類型
memory.disable_tracking("precise_location")  # 停止追蹤精確位置

# 4. 導出 Memory
memory_export = memory.export_as_json()  # 下載自己的數據

# 5. 設定 Memory 過期
memory.add(
  content="temporary_preference",
  ttl=2592000  # 30天後自動刪除
)
```

---

## Memory 的質量評估

### 關鍵指標

| 指標 | 說明 | 目標值 |
|------|------|--------|
| **Recall** | 相關記憶被檢索出的比例 | > 0.85 |
| **Precision** | 檢索出的記憶中有多少是相關的 | > 0.90 |
| **Freshness** | Memory 中有多少比例的信息是最近更新的 | > 0.70 |
| **Accuracy** | Memory 反映的用戶偏好與實際行為的匹配度 | > 0.80 |
| **Utility** | 使用 Memory 的推薦比不用 Memory 更好多少 | > 25% improvement |

### 自我優化機制

```
每週評估：
1. 檢查推薦准確度
   - 用戶點擊率
   - 用戶滿意度評分
   - 實際購買轉化

2. 識別 Memory 缺陷
   - 推薦偶然性強 → Memory 不夠精准
   - 推薦雷同 → Memory 過度簡化

3. 優化策略
   - 調整權重（重要的記憶更新頻繁）
   - 增加新維度（發現遺漏的用戶特性）
   - 清理噪音（移除對推薦無幫助的舊數據）
```

---

## Memory 與 Agent 的三層進化

### 第一代：無 Memory（2023-2024）

```
用戶：「你推薦的這條褲子，我昨天才說過不喜歡呀」
Agent：「我不知道。這是我第一次聽說」

現象：Agent 無法記住用戶，每次都重新來過
```

### 第二代：短期 Memory（2024-2025）

```
用戶：「根據我之前說的，推薦衣服」
Agent：「好的，我記得你上一次的偏好」

現象：Agent 只記得這個會話，下次會話就忘了
```

### 第三代：持久化 Memory（2025-2026）

```
用戶：「根據我這一年的偏好，推薦衣服」
Agent：「根據我記錄的你 1 年的選擇、購買、反饋，
       我發現你的風格正在從
       極簡風向極簡+質感風演進，
       因此今天的推薦融合了這兩個特點」

現象：Agent 真正認識用戶，推薦越來越准確
```

---

## Memory 的下一步：群體智慧

### 未來想像

```
個人 Memory（你自己的記憶）
    ↓
    ├→ 社區 Memory（你和志同道合的人的共享記憶）
    │    └→ 協作推薦（基於相似用戶的群體智慧）
    │
    └→ 全球 Memory（跨域的集體知識）
         └→ 新趨勢偵測（及時發現新的風格、內容潮流）
```

**應用場景**：
- 「跟我風格相似的 100 人最近開始喜歡什麼？」
- 「我所在城市的溫度下降時，大多數人如何穿衣？」
- 「與我相似的創作者最成功的內容類型是什麼？」

---

## Memory 的核心價值

| 價值 | 對 Agent 的意義 | 對用戶的意義 |
|------|-----------------|------------|
| **個人化** | 能真正認識每個用戶，而不是通用推薦 | 被理解、被看見 |
| **學習** | 每次交互都改進，推薦越來越准確 | 越用越好用 |
| **信任** | 推薦有依據可查（基於你的 Memory） | 信任度提升 |
| **自主** | 用戶可控 Memory，不被黑盒算法支配 | 掌握自己的數據 |
| **適應** | 快速適應用戶的變化（季節、生活階段等） | 推薦始終相關 |

---

## 最後：Memory 的哲學

> **一個沒有記憶的 Agent，每次都在和陌生人說話。**
>
> **一個有記憶的 Agent，才能說「我認識你」。**

Memory 不只是技術，更是 Agent 與人類關係的基礎。

當 Agent 能記住你：
- 你上次買的是什麼顏色
- 你反覆拒絕的是什麼風格
- 你最滿意的推薦是什麼
- 你的品味如何隨時間進化

那時候，Agent 才不是一個冷冰冰的工具，而是一個真正懂你的夥伴。

---

**更新日期**：2026年5月23日
**狀態**：⭐⭐⭐⭐⭐ 系統核心文檔
**維護者**：Claude Code + AI 指揮官

