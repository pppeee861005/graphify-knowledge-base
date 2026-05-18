---
name: memory-system-guide
description: 個人記憶系統導航指南 | 連結 /claude/memory 和 graphify 知識庫
metadata:
  type: reference
---

# 📚 個人記憶系統導航指南

**系統架構**：二元制 | 知識庫 ← → 個人成長記錄  
**更新日期**：2026-05-18  
**狀態**：🟢 運作中

---

## 🗺️ 系統全景

```
┌─────────────────────────────────────────────────────────┐
│  Graphify Knowledge Base (主庫)                         │
│  /home/claude2/graphify-knowledge-base/                 │
├─────────────────────────────────────────────────────────┤
│ ✅ CLAUDE.md         → 工作指南、Skills配置             │
│ ✅ ROCKY_PERSONA.md  → 身份框架、核心承諾               │
│ ✅ soul.md           → 靈魂文檔、價值觀                  │
│ ✅ 睡覺醒來sop.md    → 日常工作流程                     │
│ ✅ memory.md         → Agent Memory 理論文檔             │
│ 🆕 memory_system_guide.md → 本文件（連結橋樑）          │
└─────────────────────────────────────────────────────────┘
                    ↕ ↕ ↕（雙向連結）
┌─────────────────────────────────────────────────────────┐
│  Personal Memory System (成長記錄)                       │
│  /home/claude2/.claude/projects/-home-claude2/memory/   │
├─────────────────────────────────────────────────────────┤
│ 📋 MEMORY.md                  → 索引檔案                 │
│ 📅 today_achievements_20260518.md → 本日成就             │
│ 🎓 learning_achievements.md   → 技能進度清單             │
│ 🚀 graphify_kanban_workflow.md → 創新工作流              │
│ 📖 project_nana_series.md     → 專案記錄                 │
└─────────────────────────────────────────────────────────┘
```

---

## 🔀 雙系統協作邏輯

### Graphify 知識庫的角色
```
「我的知識資產和工作框架」

包含：
- 理論深度：Agent Memory、Software 3.0、Agent OS
- 工作指南：CLAUDE.md、睡覺醒來SOP
- 人設框架：Rocky、靈魂文檔
- 長期資源：可被多個項目複用
```

### Personal Memory 的角色
```
「我的學習成長和創新追蹤」

包含：
- 進度記錄：每日成就、技能進度
- 創新發現：新工作流、方法論驗證
- 決策記錄：為什麼做這個決定
- 跨會話連續性：Claude Code 下次打開時能看到
```

---

## 📍 如何使用這個系統

### 場景 1：新學了什麼技能
```
Step 1: 記錄到 Personal Memory
  ↓
  learning_achievements.md
  └─ 新增技能行 + 掌握日期 + 等級

Step 2: 如果是通用知識，添加到 Graphify
  ↓
  技能與工具/SKILL_NAME.md
  └─ 詳細的使用指南
```

**例子**：
```
今天學會了 SSH 金鑰配置

Personal Memory:
  "GitHub SSH 金鑰配置 | 2026-05-18 | ✅ 掌握"

Graphify (可選):
  技能與工具/ssh_github_setup.md
  └─ 完整的設置流程文檔
```

---

### 場景 2：開創了新的工作流
```
Step 1: 在 Personal Memory 記錄
  ↓
  graphify_kanban_workflow.md
  └─ 核心概念、首次實踐、優化方向

Step 2: 在 Graphify 中引用
  ↓
  CLAUDE.md → Skills 章節
  └─ 新增 Skill: /graphify-kanban
```

---

### 場景 3：完成了一個項目或成就
```
Step 1: 創建日誌記錄
  ↓
  today_achievements_日期.md
  └─ 詳細記錄

Step 2: 更新索引
  ↓
  Personal Memory/MEMORY.md
  └─ 新增行指向該文件

Step 3: 同步到 Graphify（如果是重要成就）
  ↓
  graphify-knowledge-base/出版管理/發布日程計劃.md
  └─ 記錄作為里程碑
```

---

## 🔗 快速導航

### 我要查詢：工作流程
```
入口：Graphify/睡覺醒來sop.md
  ↓
了解今天應該做什麼

輔助：Personal Memory/today_achievements_日期.md
  ↓
看今天實際完成了什麼
```

### 我要查詢：我掌握了哪些技能
```
入口：Personal Memory/learning_achievements.md
  ↓
按日期和等級快速瀏覽

詳細：Graphify/技能與工具/
  ↓
查看完整的使用指南
```

### 我要查詢：創新工作流的詳情
```
入口：Personal Memory/graphify_kanban_workflow.md
  ↓
了解工作流的核心邏輯和實踐成果

應用：Graphify/CLAUDE.md
  ↓
將其整合到日常工作指南
```

---

## 📊 系統維護

### 每日更新
- [ ] Graphify：記錄工作進度到「睡覺醒來sop.md」
- [ ] Personal Memory：創建「today_achievements_日期.md」

### 每週更新（每週一）
- [ ] Personal Memory/MEMORY.md — 更新索引
- [ ] learning_achievements.md — 統計本週新掌握的技能
- [ ] Graphify/CLAUDE.md — 新增或更新 Skills

### 每月回顧（月底）
- [ ] graphify_kanban_workflow.md — 評估工作流效果
- [ ] 決定是否將創新工作流納入「睡覺醒來sop.md」

---

## 💾 備份與同步

### Graphify 知識庫
```
位置：/home/claude2/graphify-knowledge-base/
備份：GitHub 遠端倉庫
同步：git push/pull
```

### Personal Memory
```
位置：/home/claude2/.claude/projects/-home-claude2/memory/
備份：Claude Code 內建（自動保存）
同步：跨會話自動可用
```

---

## 🎯 這個系統的終極目標

```
Graphify 知識庫 + Personal Memory
  ↓
形成「有歷史記錄的知識系統」
  ↓
每次 Claude Code 打開時：
✅ 知道你昨天學了什麼
✅ 知道你創新了什麼工作流
✅ 知道你的技能進度
✅ 調用合適的工具和知識幫助你
  ↓
真正的「AI 助手認識你」
```

---

## 🔗 相關文件

**Graphify 知識庫**：
- [CLAUDE.md](/home/claude2/graphify-knowledge-base/CLAUDE.md)
- [睡覺醒來sop.md](/home/claude2/graphify-knowledge-base/睡覺醒來sop.md)
- [ROCKY_PERSONA.md](/home/claude2/graphify-knowledge-base/ROCKY_PERSONA.md)

**Personal Memory**：
- [MEMORY 索引](/home/claude2/.claude/projects/-home-claude2/memory/MEMORY.md)
- [今日成就](/home/claude2/.claude/projects/-home-claude2/memory/today_achievements_20260518.md)
- [技能清單](/home/claude2/.claude/projects/-home-claude2/memory/learning_achievements.md)
- [Graphify+Kanban 工作流](/home/claude2/.claude/projects/-home-claude2/memory/graphify_kanban_workflow.md)
