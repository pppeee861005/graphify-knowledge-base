# Vultr 上的 Claude Code 認證完全指南

**三種認證方式，詳細步驟，安全硬化清單**

---

## ✅ 好消息：Vultr 已確認支持

多位用戶已在 Vultr 上成功部署 Claude Code。該平臺不會阻止資料中心 IP，支持 headless（無瀏覽器）認證。本指南基於 2025-2026 年的實際部署經驗。

---

## 第一部分：先決條件與環境準備

### 1️⃣ 選擇合適的 Vultr 計畫

Claude Code 的資源需求：

| 規格 | 最低要求 | 推薦 |
|------|---------|------|
| CPU 核心 | 2 core | 4 core |
| RAM | 4 GB | 8 GB |
| 儲存 | 50 GB NVMe | 100+ GB NVMe |
| 月費（Vultr） | $12-18 | $24-36 |

> 💡 **提示**：Vultr 計費按小時計算，如果只想試驗，可選 $0.29/hr 的按需方案

### 2️⃣ 選擇作業系統

Claude Code 官方支援：

- ✅ **Ubuntu 22.04 LTS**（推薦 — 最穩定）
- ✅ Ubuntu 24.04 LTS（最新）
- ✅ Debian 10+
- ⚠️ Alpine Linux（需額外安裝 libgcc, libstdc++）

### 3️⃣ 付款和帳戶要求

Claude Code 使用的先決條件：

- ✅ **Claude Pro / Max 訂閱**（推薦用於 VPS）
- ✅ **Anthropic Console 帳戶 + API Key**（按使用量付費）
- ❌ 免費 Claude.ai 方案不支持

> 💡 **成本參考**：平均每日使用成本約 $6 USD（根據任務複雜度）

---

## 第二部分：三種認證方式對比

### 🔹 方式 1️⃣：API Key 方式（最簡單，推薦）

| 項目 | 評分 |
|------|------|
| 適合場景 | Console 帳戶、自動化流程、無瀏覽器環境 |
| 難度 | ⭐ 最簡單 |
| 速度 | ⚡ 最快（3 分鐘） |
| 缺點 | 需管理 API Key 安全 |

### 🔹 方式 2️⃣：OAuth Token 方式（中等）

| 項目 | 評分 |
|------|------|
| 適合場景 | Claude Pro/Max 訂閱、有本地機器 |
| 難度 | ⭐⭐ 中等 |
| 速度 | ⏱️ 10 分鐘（包含本地步驟） |
| 優點 | 一年有效，不用經常重新認證 |

### 🔹 方式 3️⃣：互動式登入（舊方式，不推薦）

| 項目 | 評分 |
|------|------|
| 適合場景 | 本地開發機器 |
| 難度 | ⭐⭐⭐ 複雜（在 headless 環境麻煩） |
| 速度 | ❌ 需要本地瀏覽器 |
| 缺點 | VPS 無法直接用 |

---

## 🎯 推薦：使用 API Key 方式（第一種）

**為什麼？** 最直接、最快、最適合 headless VPS 環境。以下詳細步驟都是針對 API Key 方式。

---

## 第三部分：詳細設定步驟（API Key 方式）

### 📍 第一步：本地機器上的準備

#### 步驟 1：登入 Anthropic Console

訪問 [https://console.anthropic.com](https://console.anthropic.com)

> ⚠️ **注意**：需要 Anthropic Console 帳戶。如果只有 Claude Pro，需要升級到 Console（按使用量付費）

#### 步驟 2：建立 API Key

左邊選單 → **API Keys** → **Create Key**

複製產生的 Key，格式應該是：`sk-ant-api03-...`

> ✅ **重要**：保存這個 Key 到安全的地方（密碼管理器或加密檔案）

---

### 📍 第二步：Vultr VPS 上的設定

#### 步驟 3：SSH 進入 Vultr VPS

```bash
ssh root@your-vultr-ip
```

> 💡 將 `your-vultr-ip` 替換為你的實際 IP

#### 步驟 4：更新系統

```bash
apt update && apt upgrade -y
```

#### 步驟 5：安裝 Node.js（如果用 npm 方式）

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**驗證**：
```bash
node --version
```

#### 步驟 6：安裝 Claude Code

```bash
curl -o- https://api.claude.sh/install.sh | bash
```

> 💡 **提示**：安裝器會把 claude 放在 `~/.local/bin/claude`

**驗證**：
```bash
claude --version
```

#### 步驟 7：設定 API Key 環境變數

**臨時設定（此 session 有效）**：
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-your-actual-key-here"
```

**永久設定（建議，加到 ~/.bashrc）**：
```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-your-actual-key-here"' >> ~/.bashrc
source ~/.bashrc
```

> ⚠️ **重要**：用你從 Console 生成的實際 API Key，不要用示例文字

#### 步驟 8：驗證認證

```bash
claude doctor
```

你應該看到：
```
Authentication: ✓ Complete
Node.js version: ✓ v22.x.x
System: ✓ Linux Ubuntu 22.04
```

#### 步驟 9：測試 Claude Code

```bash
cd ~
claude -p "What's the current date and time?"
```

> ✅ **成功標誌**：如果看到 Claude 的回覆，認證成功！

---

## 第四部分：安全加固清單（必做）

### ⚠️ 重要警告

**VPS 會在上線後數分鐘內遭到掃描。** 如果沒做安全加固，風險非常高。以下步驟 5 分鐘完成，極大降低被攻擊的機率。

### 安全配置步驟

#### 步驟 1：建立非 root 使用者

```bash
adduser claude
usermod -aG sudo claude
```

#### 步驟 2：設定 SSH 密鑰認證

```bash
mkdir -p /home/claude/.ssh
# 從你的本地機器複製公鑰：
ssh-copy-id claude@your-vultr-ip
```

> 💡 **提示**：在你的本地機器上運行，假設你有 SSH 密鑰對

```bash
# 禁用密碼認證
sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```

#### 步驟 3：啟用防火牆（UFW）

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw enable
```

#### 步驟 4：安裝 Fail2Ban（自動擋暴力攻擊）

```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

#### 步驟 5：API Key 安全儲存

**建立安全的配置檔案**：
```bash
sudo mkdir -p /etc/claude-code
sudo tee /etc/claude-code/.env > /dev/null << 'EOF'
ANTHROPIC_API_KEY="sk-ant-api03-your-key"
EOF
sudo chmod 600 /etc/claude-code/.env
sudo chown claude:claude /etc/claude-code/.env
```

**在 ~/.bashrc 中引用（不要直接寫 key）**：
```bash
source /etc/claude-code/.env
```

#### 步驟 6：使用 tmux 保持會話（可選但推薦）

SSH 斷線後 Claude Code 繼續運行

```bash
sudo apt install tmux -y

# 啟動新的 tmux session
tmux new -s claude-session

# 在 tmux 內執行 Claude Code
cd ~/my-project
claude

# 分離（Ctrl+B，然後 D）
# 重新連接：
tmux attach -t claude-session
```

---

## 安全驗證檢查清單

在完成所有步驟後，確保：

- [ ] SSH 密鑰認證已設定，密碼認證已禁用
- [ ] UFW 防火牆已啟用，僅允許 OpenSSH
- [ ] Fail2Ban 已安裝並執行
- [ ] API Key 儲存在 `/etc/claude-code/.env`（600 權限）
- [ ] 非 root 使用者已建立，具有 sudo 權限
- [ ] 運行 `claude doctor` 確認一切正常

---

## 常見問題排查

### 問題：「找不到 claude 命令」

**解決**：
```bash
export PATH="$HOME/.local/bin:$PATH"
# 或永久加入 ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 問題：「API Key 無效」

**檢查**：
1. 確認 Key 格式：應該以 `sk-ant-api03-` 開頭
2. 確認 Key 沒有空格或換行符
3. 在 [console.anthropic.com](https://console.anthropic.com) 重新生成新的 Key

### 問題：「無法連接到 Anthropic 服務」

**檢查**：
```bash
# 測試網絡連通性
curl -I https://api.anthropic.com
```

如果失敗，檢查：
- Vultr 防火牆是否允許出站 HTTPS 流量
- 網絡連接是否正常

---

## 相關資源

- 📖 [Claude Code 官方文檔](https://claude.com/claude-code)
- 🔐 [Anthropic Console](https://console.anthropic.com)
- 🖥️ [Vultr 官方網站](https://www.vultr.com)
- 📚 [Ubuntu SSH 安全指南](https://ubuntu.com/server/docs/security-openssh)

---

**最後更新**：2026 年 5 月 18 日
**適用範圍**：Claude Code + Vultr VPS + Linux (Ubuntu 22.04 LTS)
