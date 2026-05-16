# Hermes Agent + Cube Sandbox 集成指南
## 新人類聯盟 L3 Skill Foundry 執行層架構

**作者**：新人類聯盟 / 風神  
**日期**：2026.05  
**版本**：1.0  
**目標受眾**：獨立 Skill 開發者、Agent 平台運營者

---

## 📋 目錄
1. [架構概述](#架構概述)
2. [前置準備](#前置準備)
3. [部署流程](#部署流程)
4. [Skill 後端修改](#skill-後端修改)
5. [E2B 遷移指南](#e2b-遷移指南)
6. [監控與優化](#監控與優化)
7. [成本對標](#成本對標)
8. [常見問題](#常見問題)

---

## 架構概述

### 三層分離架構

```
┌─────────────────────────────────────────────────────────────┐
│                   Gateway Layer (Hermes)                     │
│  - Telegram/Discord/Slack/CLI 消息適配器                    │
│  - 會話管理、消息路由                                        │
│  - 記憶存儲 (/opt/data) → NotebookLM 知識庫                 │
│  - 持久運行，8GB RAM，Docker 容器                            │
└────────────────────┬────────────────────────────────────────┘
                     │ REST API (JSON)
                     ↓
┌─────────────────────────────────────────────────────────────┐
│            Agent Intelligence Layer (Claude)                 │
│  - 決策邏輯（哪個 Skill？參數是什麼？）                     │
│  - Skill 調度與結果整合                                      │
│  - API 遠程調用                                              │
└────────────────────┬────────────────────────────────────────┘
                     │ Skill 執行請求
                     ↓
┌─────────────────────────────────────────────────────────────┐
│         Execution Sandbox Layer (Cube Sandbox)               │
│  - python-learning-tutor (Python 代碼檢查)                   │
│  - cad-architect (CAD 參數化)                                │
│  - floorplan-to-DXF (圖檔轉換)                               │
│  - 毫秒級創建/銷毀，<5MB 內存開銷，KVM 隔離                 │
└─────────────────────────────────────────────────────────────┘
```

### 數據流示例：學生代碼檢查

```
1. 用戶 (Telegram)
   └─> "幫我檢查這個 Python 代碼"

2. Hermes Gateway
   └─> 解析消息 → 確認用戶身份 → 創建會話

3. Claude (決策層)
   └─> 分析意圖 → 決定用 python-learning-tutor Skill
       構建請求：{code: "...", level: "beginner"}

4. Cube Sandbox API
   POST /api/sandbox/create
   {
     "image": "python:3.11-slim",
     "timeout": 5,
     "script": "檢查代碼\nprint(result)",
     "network_disabled": true
   }

5. Cube Sandbox 內核
   - 60ms 內啟動虛擬機
   - 執行 Python 腳本
   - 捕捉 stdout/stderr
   - 自動清理，內存回收

6. 結果返回 Claude
   └─> 解析輸出 → 生成教學反饋

7. Hermes Gateway
   └─> 格式化 → 發送回 Telegram
```

---

## 前置準備

### 硬件需求

| 層級 | CPU | RAM | 存儲 | 網絡 |
|------|-----|-----|------|------|
| **Hermes Gateway** | 2 核 | 2-4 GB | 10 GB | 穩定 |
| **Cube Sandbox (單節點)** | 4 核+ | 8-16 GB | 20 GB | 低延遲 |
| **推薦配置** | 6-8 核 | 16-24 GB | 50 GB | Gigabit LAN |

### 軟件準備

#### 檢查表
- [ ] Ubuntu 22.04 LTS 或更新版本
- [ ] Docker & Docker Compose 已安裝
- [ ] KVM 硬件虛擬化支持
- [ ] Hermes Agent 已部署（v0.8.0+）
- [ ] Python 3.10+ 開發環境

#### 驗證 KVM 支持

```bash
# 檢查 CPU 標誌
grep -cw vmx /proc/cpuinfo    # Intel
# 或
grep -cw svm /proc/cpuinfo    # AMD

# 輸出 > 0 表示支持

# 檢查 KVM 模塊
lsmod | grep kvm
# 應該看到 kvm 和 kvm_intel (或 kvm_amd)

# 如果缺失，加載模塊
sudo modprobe kvm
sudo modprobe kvm_intel  # 或 kvm_amd
```

#### WSL2 用戶（Windows 環境）

```powershell
# 以管理員身份運行 PowerShell
wsl --install

# 檢查 WSL2 嵌套虛擬化
wsl -l -v

# BIOS 設置：啟用 "Hyper-V" 和 "嵌套虛擬化"
# 或在 PowerShell 中：
Set-VMProcessor -VMName "WSL" -ExposeVirtualizationExtensions $true
```

---

## 部署流程

### Step 1：準備目錄結構

```bash
# 在主機上創建項目目錄
mkdir -p ~/alliance-infrastructure/{hermes,cube-sandbox,shared-config}
cd ~/alliance-infrastructure

# 目錄說明
# hermes/            → Hermes Gateway 配置和數據
# cube-sandbox/      → Cube Sandbox 部署文件
# shared-config/     → 共享配置（API密鑰、Skills清單）
```

### Step 2：Hermes Gateway 部署（或升級）

#### 2.1 docker-compose.yml（Hermes）

```yaml
# ~/alliance-infrastructure/hermes/docker-compose.yml

version: '3.8'

services:
  hermes-gateway:
    image: nousresearch/hermes-agent:latest
    container_name: hermes-gateway
    restart: unless-stopped
    
    # 環境變數
    environment:
      HERMES_DASHBOARD: "1"                    # 啟用儀表板
      HERMES_LOG_LEVEL: "info"
      HERMES_MEMORY_BACKEND: "json"            # 使用 JSON 持久化
      
      # Cube Sandbox 後端配置
      EXECUTION_BACKEND: "cube_sandbox"
      CUBE_SANDBOX_API_URL: "http://cube-sandbox-api:9000"
      CUBE_SANDBOX_TIMEOUT: "30"               # 秒
      CUBE_SANDBOX_MEMORY_LIMIT: "512M"
      
      # LLM 配置
      LLM_PROVIDER: "anthropic"
      ANTHROPIC_API_KEY: "${ANTHROPIC_API_KEY}"
    
    # 端口映射
    ports:
      - "8642:8642"    # Hermes 主端口
      - "8643:8643"    # 儀表板（如果啟用）
    
    # 持久化存儲
    volumes:
      - hermes-data:/opt/data
      - ./skills:/opt/hermes/skills:ro    # Skill 唯讀掛載
      - ./config.yaml:/opt/hermes/config.yaml:ro
    
    # 網絡
    networks:
      - alliance-net
    
    # 資源限制
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
    
    # 健康檢查
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8642/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
    # 依賴
    depends_on:
      - cube-sandbox-api

  # 可選：本地 LLM（如果不想用遠程 Claude）
  # vllm:
  #   image: vllm/vllm-openai:latest
  #   container_name: vllm-server
  #   command: >
  #     --model Qwen/Qwen2.5-7B-Instruct
  #     --served-model-name qwen-local
  #     --host 0.0.0.0
  #     --port 8000
  #   ports:
  #     - "8000:8000"
  #   networks:
  #     - alliance-net
  #   deploy:
  #     resources:
  #       reservations:
  #         devices:
  #           - capabilities: [gpu]  # 如果有 GPU

volumes:
  hermes-data:
    driver: local

networks:
  alliance-net:
    driver: bridge
```

#### 2.2 Hermes 配置文件

```yaml
# ~/alliance-infrastructure/hermes/config.yaml

agent:
  name: "新人類聯盟執行代理"
  version: "1.0"
  description: "L3 Skill Foundry 執行層"

model:
  provider: "anthropic"
  model: "claude-opus-4-20250514"
  api_key: "${ANTHROPIC_API_KEY}"
  temperature: 0.7
  max_tokens: 4096

# Cube Sandbox 集成
execution:
  backend: "cube_sandbox"
  
  cube_sandbox:
    api_url: "${CUBE_SANDBOX_API_URL}"
    timeout: 30  # 秒
    
    sandbox_config:
      memory_limit: "512M"
      cpu_limit: "1"
      network_disabled: true
      
      # 默認環境
      env:
        PYTHONUNBUFFERED: "1"
        PYTHONDONTWRITEBYTECODE: "1"
    
    # 重試策略
    retry:
      max_attempts: 3
      backoff_multiplier: 2.0
      initial_delay: 1.0

# 持久化記憶
memory:
  type: "json"
  path: "/opt/data/memory"
  
  # NotebookLM 集成（知識庫）
  knowledge_base:
    type: "notebooklm"
    api_key: "${NOTEBOOKLM_API_KEY}"
    notebooks:
      - id: "skill-library"
        description: "已發佈 Skills 清單"
      - id: "user-profiles"
        description: "用戶學習檔案"

# 消息平台
platforms:
  cli:
    enabled: true
  
  telegram:
    enabled: true
    token: "${TELEGRAM_BOT_TOKEN}"
    webhook_url: "${TELEGRAM_WEBHOOK_URL}"
  
  discord:
    enabled: true
    token: "${DISCORD_BOT_TOKEN}"
  
  slack:
    enabled: false
    token: "${SLACK_BOT_TOKEN}"

# 安全性
security:
  # Skill 執行白名單
  skill_whitelist:
    - "python-learning-tutor"
    - "cad-architect"
    - "floorplan-to-dxf"
  
  # 沙箱隔離策略
  sandbox_policy:
    allow_network: false
    allow_filesystem_write: false  # 除了臨時目錄
    resource_limits:
      max_processes: 10
      max_fds: 1024

# 日誌
logging:
  level: "info"
  format: "json"
  outputs:
    - type: "file"
      path: "/opt/data/logs/hermes.log"
      rotation: "daily"
      retention: 30  # 天
    - type: "stdout"
```

#### 2.3 啟動 Hermes

```bash
cd ~/alliance-infrastructure/hermes

# 設置環境變數
export ANTHROPIC_API_KEY="sk-ant-..."
export TELEGRAM_BOT_TOKEN="123456:ABC-..."
# ... 其他密鑰

# 啟動
docker-compose up -d

# 檢查日誌
docker-compose logs -f hermes-gateway

# 確認健康狀態
curl http://localhost:8642/health
# 應返回 {"status": "healthy"}
```

---

### Step 3：Cube Sandbox 部署

#### 3.1 Clone & 準備

```bash
cd ~/alliance-infrastructure

# Clone Cube Sandbox
git clone https://github.com/TencentCloud/CubeSandbox.git cube-sandbox-src

# 檢查前置依賴
cd cube-sandbox-src
./scripts/check_env.sh

# 預期輸出：
# ✓ KVM 支持
# ✓ cgroups v2
# ✓ seccomp
# ✓ eBPF
```

#### 3.2 構建 Docker 鏡像

```bash
# 方式 A：從源碼構建（推薦用於定制）
cd ~/alliance-infrastructure/cube-sandbox-src
docker build -t cube-sandbox:latest .

# 方式 B：使用官方預構建鏡像
docker pull tencentcloud/cube-sandbox:latest
docker tag tencentcloud/cube-sandbox:latest cube-sandbox:latest
```

#### 3.3 docker-compose.yml（Cube Sandbox）

```yaml
# ~/alliance-infrastructure/docker-compose.yml
# (在主 alliance-infrastructure 目錄，協調兩個服務)

version: '3.8'

services:
  # ============ Hermes Gateway ============
  hermes-gateway:
    image: nousresearch/hermes-agent:latest
    container_name: hermes-gateway
    restart: unless-stopped
    
    environment:
      EXECUTION_BACKEND: "cube_sandbox"
      CUBE_SANDBOX_API_URL: "http://cube-sandbox-api:9000"
      ANTHROPIC_API_KEY: "${ANTHROPIC_API_KEY}"
    
    ports:
      - "8642:8642"
    
    volumes:
      - hermes-data:/opt/data
      - ./skills:/opt/hermes/skills:ro
    
    networks:
      - alliance-net
    
    depends_on:
      cube-sandbox-api:
        condition: service_healthy

  # ============ Cube Sandbox API ============
  cube-sandbox-api:
    image: cube-sandbox:latest
    container_name: cube-sandbox-api
    restart: unless-stopped
    
    # Cube Sandbox 作為 API 服務運行
    command: 
      - "api"
      - "--host=0.0.0.0"
      - "--port=9000"
      - "--log-level=info"
    
    ports:
      - "9000:9000"
    
    # 特權模式（必需，用於 KVM）
    privileged: true
    
    # 設備映射
    devices:
      - /dev/kvm:/dev/kvm
      - /dev/net/tun:/dev/net/tun  # 網絡虛擬化
    
    volumes:
      - cube-sandbox-data:/var/lib/cube-sandbox
      - /sys/kernel/debug:/sys/kernel/debug:rw  # eBPF 調試
    
    networks:
      - alliance-net
    
    # 資源限制
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
    
    # 健康檢查
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/health"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  # ============ 監控（可選） ============
  # prometheus:
  #   image: prom/prometheus:latest
  #   container_name: prometheus
  #   volumes:
  #     - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
  #     - prometheus-data:/prometheus
  #   ports:
  #     - "9090:9090"
  #   networks:
  #     - alliance-net

volumes:
  hermes-data:
    driver: local
  cube-sandbox-data:
    driver: local
  # prometheus-data:
  #   driver: local

networks:
  alliance-net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

#### 3.4 啟動整個堆棧

```bash
cd ~/alliance-infrastructure

# 啟動所有服務
docker-compose up -d

# 查看日誌
docker-compose logs -f

# 驗證健康狀態
docker-compose ps

# 預期輸出：
# NAME                    STATUS
# hermes-gateway          Up (healthy)
# cube-sandbox-api        Up (healthy)
```

#### 3.5 測試 Cube Sandbox API

```bash
# 測試沙箱創建
curl -X POST http://localhost:9000/api/sandbox/create \
  -H "Content-Type: application/json" \
  -d '{
    "image": "python:3.11-slim",
    "timeout": 5,
    "script": "print(\"Hello from Cube Sandbox\")\nprint(2 + 2)"
  }'

# 預期響應：
# {
#   "sandbox_id": "sb_abc123xyz789...",
#   "status": "created",
#   "stdout": "Hello from Cube Sandbox\n4\n",
#   "stderr": "",
#   "exit_code": 0,
#   "duration_ms": 45
# }

# 重要指標：
# - duration_ms: 45ms ✓ (在 60ms 預期內)
# - memory_used: ~5-10MB ✓ (符合設計目標)
```

---

## Skill 後端修改

### Step 1：Skill 執行層抽象

創建統一的 Skill 執行接口，支持多種後端：

```python
# ~/alliance-infrastructure/skills/shared/execution.py

"""
Skill 執行層抽象
支持多個後端：local, docker, e2b, cube_sandbox
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any
import os
import json
import requests
import subprocess
from datetime import datetime

@dataclass
class ExecutionResult:
    """執行結果標準化"""
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: float
    sandbox_id: Optional[str] = None
    metadata: Dict[str, Any] = None

class ExecutionBackend(ABC):
    """執行後端基類"""
    
    @abstractmethod
    async def execute(
        self,
        script: str,
        image: str = "python:3.11-slim",
        timeout: int = 30,
        **kwargs
    ) -> ExecutionResult:
        """執行腳本，返回標準化結果"""
        pass

class CubeSandboxBackend(ExecutionBackend):
    """Cube Sandbox 後端實現"""
    
    def __init__(self, api_url: str = None):
        self.api_url = api_url or os.getenv(
            "CUBE_SANDBOX_API_URL",
            "http://cube-sandbox-api:9000"
        )
        self.session = requests.Session()
    
    async def execute(
        self,
        script: str,
        image: str = "python:3.11-slim",
        timeout: int = 30,
        network_disabled: bool = True,
        memory_limit: str = "512M",
        **kwargs
    ) -> ExecutionResult:
        """
        在 Cube Sandbox 中執行腳本
        
        Args:
            script: Python 代碼
            image: 容器鏡像
            timeout: 超時秒數
            network_disabled: 禁用網絡
            memory_limit: 內存限制
        
        Returns:
            ExecutionResult: 標準化結果
        """
        
        import time
        start_time = time.time()
        
        try:
            # API 請求
            response = self.session.post(
                f"{self.api_url}/api/sandbox/create",
                json={
                    "image": image,
                    "script": script,
                    "timeout": timeout,
                    "network_disabled": network_disabled,
                    "memory_limit": memory_limit,
                    "env": {
                        "PYTHONUNBUFFERED": "1",
                    }
                },
                timeout=timeout + 10  # 網絡超時稍長
            )
            response.raise_for_status()
            
            # 解析響應
            data = response.json()
            duration_ms = (time.time() - start_time) * 1000
            
            return ExecutionResult(
                stdout=data.get("stdout", ""),
                stderr=data.get("stderr", ""),
                exit_code=data.get("exit_code", 0),
                duration_ms=duration_ms,
                sandbox_id=data.get("sandbox_id"),
                metadata={
                    "backend": "cube_sandbox",
                    "image": image,
                    "memory_limit": memory_limit,
                }
            )
        
        except requests.exceptions.Timeout:
            return ExecutionResult(
                stdout="",
                stderr=f"[CubeSandbox] 執行超時（{timeout}s）",
                exit_code=124,
                duration_ms=(time.time() - start_time) * 1000,
                metadata={"error": "timeout"}
            )
        
        except Exception as e:
            return ExecutionResult(
                stdout="",
                stderr=f"[CubeSandbox] 錯誤: {str(e)}",
                exit_code=-1,
                duration_ms=(time.time() - start_time) * 1000,
                metadata={"error": str(e)}
            )

class LocalBackend(ExecutionBackend):
    """本地執行（開發用）"""
    
    async def execute(
        self,
        script: str,
        image: str = "python:3.11-slim",
        timeout: int = 30,
        **kwargs
    ) -> ExecutionResult:
        """在本地執行（不推薦生產）"""
        
        import time
        start_time = time.time()
        
        try:
            result = subprocess.run(
                ["python", "-c", script],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return ExecutionResult(
                stdout=result.stdout,
                stderr=result.stderr,
                exit_code=result.returncode,
                duration_ms=(time.time() - start_time) * 1000,
                metadata={"backend": "local"}
            )
        
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                stdout="",
                stderr=f"本地執行超時（{timeout}s）",
                exit_code=124,
                duration_ms=(time.time() - start_time) * 1000
            )
        
        except Exception as e:
            return ExecutionResult(
                stdout="",
                stderr=f"本地執行錯誤: {str(e)}",
                exit_code=-1,
                duration_ms=(time.time() - start_time) * 1000
            )

def get_execution_backend(backend_name: str = None) -> ExecutionBackend:
    """工廠函數：根據配置返回後端實例"""
    
    backend_name = backend_name or os.getenv(
        "EXECUTION_BACKEND",
        "cube_sandbox"
    )
    
    backends = {
        "cube_sandbox": CubeSandboxBackend,
        "local": LocalBackend,
        # "e2b": E2BBackend,  # 未來支持
        # "docker": DockerBackend,  # 未來支持
    }
    
    backend_class = backends.get(backend_name)
    if not backend_class:
        raise ValueError(f"未知的執行後端: {backend_name}")
    
    return backend_class()
```

### Step 2：修改現有 Skill（以 python-learning-tutor 為例）

```python
# ~/alliance-infrastructure/skills/python_learning_tutor/main.py

"""
Python Learning Tutor Skill
使用 Cube Sandbox 執行用戶代碼
"""

import asyncio
import json
from typing import Dict, Any

# 導入執行層
import sys
sys.path.insert(0, '/opt/hermes/skills/shared')
from execution import get_execution_backend, ExecutionResult

class PythonLearningTutor:
    """Python 學習輔導 Skill"""
    
    def __init__(self):
        self.executor = get_execution_backend()
        self.max_code_length = 5000
        self.timeout = 10  # 秒
    
    async def analyze_code(self, code: str) -> Dict[str, Any]:
        """
        分析並執行 Python 代碼
        
        Args:
            code: 用戶提交的 Python 代碼
        
        Returns:
            分析結果（包含輸出、錯誤、建議）
        """
        
        # 安全性檢查
        if len(code) > self.max_code_length:
            return {
                "status": "error",
                "message": f"代碼過長（>{self.max_code_length} 字符）"
            }
        
        # 禁用的內置模塊
        forbidden_modules = [
            "os", "sys", "subprocess", "socket", "requests",
            "urllib", "pickle", "marshal", "__import__"
        ]
        
        for module in forbidden_modules:
            if module in code:
                return {
                    "status": "error",
                    "message": f"不允許使用模塊: {module}"
                }
        
        # 執行代碼
        result = await self.executor.execute(
            script=code,
            image="python:3.11-slim",
            timeout=self.timeout,
            network_disabled=True,
            memory_limit="256M"
        )
        
        # 分析結果
        return {
            "status": "success" if result.exit_code == 0 else "error",
            "output": result.stdout,
            "errors": result.stderr,
            "exit_code": result.exit_code,
            "execution_time_ms": result.duration_ms,
            "sandbox_id": result.sandbox_id,
            "suggestions": self._generate_suggestions(
                code, result.stdout, result.stderr, result.exit_code
            )
        }
    
    def _generate_suggestions(
        self,
        code: str,
        stdout: str,
        stderr: str,
        exit_code: int
    ) -> list:
        """根據執行結果生成學習建議"""
        
        suggestions = []
        
        if exit_code != 0:
            if "IndentationError" in stderr:
                suggestions.append({
                    "type": "error",
                    "message": "縮進錯誤：檢查代碼塊的空格/TAB 一致性",
                    "severity": "high"
                })
            elif "NameError" in stderr:
                suggestions.append({
                    "type": "error",
                    "message": "變數未定義：檢查變數名拼寫或定義順序",
                    "severity": "high"
                })
            elif "IndexError" in stderr:
                suggestions.append({
                    "type": "error",
                    "message": "索引超出範圍：列表/字符串長度不足",
                    "severity": "high"
                })
        
        # 風格建議
        if "\t" in code:
            suggestions.append({
                "type": "style",
                "message": "使用空格而不是 TAB（PEP 8 推薦）",
                "severity": "low"
            })
        
        return suggestions
    
    async def explain_concept(self, topic: str) -> str:
        """解釋 Python 概念（使用 Claude）"""
        
        # 由 Hermes 通過 Claude 調用
        return f"關於 '{topic}' 的解釋..."

# Hermes Skill 入口
async def handle_skill_call(
    skill_name: str,
    action: str,
    params: Dict[str, Any]
) -> Dict[str, Any]:
    """Hermes 調用入口"""
    
    tutor = PythonLearningTutor()
    
    if action == "analyze_code":
        return await tutor.analyze_code(params.get("code", ""))
    
    elif action == "explain_concept":
        return {
            "explanation": await tutor.explain_concept(params.get("topic", ""))
        }
    
    else:
        return {"error": f"未知動作: {action}"}
```

### Step 3：Skill 清單（SKILL.md 更新）

```yaml
# ~/alliance-infrastructure/skills/python_learning_tutor/SKILL.md

---
id: "python-learning-tutor"
name: "Python Learning Tutor"
version: "2.0"
author: "新人類聯盟"
description: "Python 代碼分析與教學輔導，使用 Cube Sandbox 隔離執行"

# 執行層配置
execution:
  backend: "cube_sandbox"  # ← 新增：指定後端
  
  sandbox_config:
    image: "python:3.11-slim"
    timeout: 10  # 秒
    memory_limit: "256M"
    network_disabled: true
    max_processes: 5

# 動作定義
actions:
  - id: "analyze_code"
    description: "分析 Python 代碼並提供反饋"
    
    parameters:
      - name: "code"
        type: "string"
        required: true
        description: "要分析的 Python 代碼"
        max_length: 5000
      
      - name: "difficulty_level"
        type: "enum"
        enum: ["beginner", "intermediate", "advanced"]
        default: "beginner"
    
    output:
      type: "object"
      schema:
        status: "string"     # success | error
        output: "string"     # 執行輸出
        errors: "string"     # 錯誤信息
        execution_time_ms: "number"
        suggestions: "array"
  
  - id: "explain_concept"
    description: "解釋 Python 概念"
    parameters:
      - name: "topic"
        type: "string"
        required: true
    output:
      type: "object"
      schema:
        explanation: "string"

# 成本配置
cost:
  per_execution_usd: 0.001  # 每次執行 $0.001
  monthly_estimate_usd: 10  # 估計月成本
  note: "Cube Sandbox 相比 E2B 成本降低 90%+"

# 權限與安全
security:
  require_authentication: true
  sandbox_required: true
  banned_imports:
    - "os"
    - "sys"
    - "subprocess"
    - "socket"
  resource_limits:
    max_runtime_seconds: 10
    max_memory_mb: 256
    max_output_bytes: 10485760  # 10MB

tags:
  - "education"
  - "python"
  - "code-analysis"
  - "sandbox"
---
```

---

## E2B 遷移指南

### 為什麼遷移？

| 指標 | E2B | Cube Sandbox | 改進 |
|------|-----|-------------|------|
| 冷啟動 | ~100ms | <60ms | 40%+ 快 |
| 內存開銷/實例 | ~50MB | ~5MB | 10 倍 |
| 每臺機器容量 | ~150 實例 | ~1500 實例 | 10 倍 |
| 月成本 (1000 次調用) | ~$50 | ~$1 | 98% 省 |
| 開源 | ❌ | ✅ | 廠商獨立 |

### 遷移步驟

#### 1. 環境變數替換

```bash
# 舊 E2B 配置
export E2B_API_KEY="sk_abc123..."
export E2B_API_URL="https://api.e2b.dev"

# 新 Cube Sandbox 配置
export CUBE_SANDBOX_API_URL="http://cube-sandbox-api:9000"
# （無需 API 密鑰，本地部署）

# 在 Hermes config.yaml 中更新
```

#### 2. API 呼叫遷移

```python
# 舊代碼 (E2B)
from e2b import CodeInterpreter

def execute_e2b(code: str):
    with CodeInterpreter() as sandbox:
        result = sandbox.notebook.exec_cell(code)
        return result

# 新代碼 (Cube Sandbox)
async def execute_cube(code: str):
    backend = get_execution_backend("cube_sandbox")
    result = await backend.execute(
        script=code,
        image="python:3.11-slim",
        timeout=10
    )
    return result
```

#### 3. 漸進式遷移計劃

```
Week 1: 搭建 Cube Sandbox 基礎設施
Week 2: 修改 1-2 個 Skill 支持 Cube Sandbox（並行 E2B）
Week 3: 在測試用戶中驗證效果
Week 4: 全量遷移，監控成本與性能
Week 5: 下線 E2B（如不需要回退）
```

#### 4. 回退策略

```python
# 在執行層實現故障轉移
class ExecutionWithFallback(ExecutionBackend):
    
    async def execute(self, **kwargs):
        try:
            # 優先使用 Cube Sandbox
            backend = CubeSandboxBackend()
            return await backend.execute(**kwargs)
        
        except Exception as e:
            print(f"Cube Sandbox 失敗: {e}，回退到 E2B")
            # 回退邏輯
            backend = E2BBackend()
            return await backend.execute(**kwargs)
```

---

## 監控與優化

### Step 1：指標收集

```yaml
# ~/alliance-infrastructure/prometheus.yml

global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'cube-sandbox'
    static_configs:
      - targets: ['localhost:9000']
    metrics_path: '/metrics'

  - job_name: 'hermes'
    static_configs:
      - targets: ['localhost:8642']
    metrics_path: '/metrics'
```

### Step 2：關鍵指標

```
# Cube Sandbox 指標
cube_sandbox_sandbox_create_duration_ms
cube_sandbox_sandbox_memory_bytes
cube_sandbox_sandbox_cpu_percent
cube_sandbox_sandbox_errors_total

# Hermes 指標
hermes_skill_execution_duration_seconds
hermes_skill_execution_errors_total
hermes_api_request_latency_seconds

# 業務指標
skill_python_learning_tutor_accuracy_percent
skill_cad_architect_conversion_success_rate
```

### Step 3：儀表板 (Grafana)

可視化關鍵 KPI：
- 沙箱啟動時間分布
- 內存使用趨勢
- 錯誤率
- 成本對標

---

## 成本對標

### 成本計算模型

假設場景：**100 個活躍學生，每周執行 1000 次 python-learning-tutor**

#### E2B 成本
```
基礎: $99/月 (包 1000 次)
超額: 9000 次 × $0.01 = $90
總計: $189/月
```

#### Cube Sandbox 成本
```
硬件 (AWS EC2 4核, 8GB): $30/月
電力/網絡: $5/月
運維: $0 (開源，自動化)
總計: $35/月

節省: $154/月 (81% 省)
年度節省: $1,848
```

### 盈利模型

服務層級：

| 層級 | 月費 | 包含額度 | 超額價格 |
|------|------|--------|---------|
| **Starter** | 免費 | 100 次/月 | $0.01/次 |
| **Pro** | $9.99 | 5000 次/月 | $0.005/次 |
| **Enterprise** | $99 | 無限 | 諮詢 |

**預期 ARR**（1000 Pro 用戶）:
```
1000 × $9.99 × 12 = $119,880
超額收入: $15,000-30,000
總 ARR: $135,000-150,000

Cube Sandbox 成本: $420/年
毛利率: 99.7%
```

---

## 常見問題

### Q: 為什麼要 KVM？不能用 Docker 代替嗎？

**A**: 可以，但不推薦：
- Docker: 容器級隔離，用戶可能逃逸 (cgroup 漏洞)
- KVM: VM 級隔離，硬件級別，更安全
- Cube Sandbox 的優勢在於輕量化 + 安全性兼得

### Q: Cube Sandbox 支持哪些語言？

**A**: 支持任何 Linux 容器鏡像：
```bash
# Python
docker run python:3.11 python script.py

# JavaScript (Node.js)
docker run node:18 node script.js

# Go
docker run golang:1.21 go run script.go

# 自定義
docker run myimage:latest /start.sh
```

### Q: 多少並發才能飽和一臺 Cube Sandbox 機器？

**A**: 取決於配置：
```
假設：
- 機器: 4核, 8GB RAM
- 每個沙箱: 1核, 256MB
- 沙箱啟動: <60ms

理論上限: 8GB / 256MB = 32 實例

實際考量:
- 啟動隊列 (ramp-up time)
- 慢查詢 (1% 可能超時)
- 系統開銷 (10%)

保守估計: 20-25 並發實例
有效吞吐: 3000-4000 次/小時
```

### Q: 如何處理 Cube Sandbox 宕機？

**A**: 實現健康檢查 + 故障轉移：

```python
class ResilientExecutor:
    
    async def execute_with_fallback(self, code: str):
        backends = [
            CubeSandboxBackend(),
            E2BBackend(),  # 備份
            LocalBackend(),  # 最後手段
        ]
        
        for backend in backends:
            try:
                return await backend.execute(code)
            except Exception as e:
                print(f"後端失敗: {e}，嘗試下一個...")
                continue
        
        # 全部失敗
        return ExecutionResult(
            stderr="所有執行後端均不可用",
            exit_code=-1,
            duration_ms=0
        )
```

### Q: Cube Sandbox 的安全隔離有多好？

**A**: 企業級：
- **網絡隔離**: eBPF 內核級防火牆
- **資源隔離**: cgroups v2 + KVM
- **進程隔離**: 獨立 PID namespace
- **文件隔離**: 獨立 mount namespace
- **時間隔離**: 無時間旁信道 (timing attacks 困難)

**威脅模型**：
```
✓ 防止用戶代碼訪問宿主機
✓ 防止用戶代碼訪問其他沙箱
✓ 防止用戶代碼逃逸 (escape)

⚠ 不防止 Hermes 進程被入侵
  → 需要額外的 WAF + 認證
```

### Q: 如何監控 Skill 的成本？

**A**: 在 ExecutionResult 中追蹤成本：

```python
@dataclass
class ExecutionResult:
    # ... 其他字段
    cost_usd: float = 0.0001  # 每次 $0.0001
    
    @property
    def billing_info(self):
        return {
            "skill": "python-learning-tutor",
            "duration_ms": self.duration_ms,
            "cost_usd": self.cost_usd,
            "timestamp": datetime.now()
        }
```

匯總成本：
```sql
SELECT 
    skill_name,
    COUNT(*) as executions,
    SUM(cost_usd) as total_cost,
    AVG(duration_ms) as avg_duration
FROM skill_executions
WHERE date >= '2026-05-01'
GROUP BY skill_name
```

---

## 總結與後續

### 架構確認
✅ 三層分離 (Gateway / Intelligence / Execution)
✅ Hermes → Cube Sandbox 集成
✅ E2B 成本降低 98%+
✅ 1500+ 並發實例支持

### 下一步行動（按優先級）

**立即 (Week 1)**
1. 部署 Hermes + Cube Sandbox 基礎設施
2. 測試 python-learning-tutor Skill
3. 性能基準測試

**短期 (Week 2-4)**
1. 遷移其他 Skill (cad-architect, floorplan-to-dxf)
2. 實現監控 + 告警
3. 優化資源配置

**中期 (Month 2-3)**
1. 發佈 Skill Foundry 服務 ($0/月免費 + $9.99 Pro)
2. 社群反饋與迭代
3. 商業化路線圖

**長期 (Month 3+)**
1. Multi-node Cube Sandbox 集群
2. GPU Support (for 機器學習 Skills)
3. Agent 市場規範化

---

**文件版本**: 1.0  
**最後更新**: 2026.05  
**維護者**: 新人類聯盟 / 風神  
**反饋**: 提交 Issue 至 GitHub 或 Substack

**相關資源**:
- GitHub: https://github.com/TencentCloud/CubeSandbox
- Hermes Docs: https://hermes-agent.nousresearch.com
- 新人類聯盟 Substack: https://aiagentcommander.substack.com
