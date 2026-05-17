#!/usr/bin/env python3
"""
Kling JWT Token 生成器
快速生成 JWT 用於 API 調用
"""

import os
import time
import jwt
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# 使用第二個 Key（新購買資源包）
ACCESS_KEY = os.getenv("KLING_ACCESS_KEY") or "An98f9gCT9er3hAbfeyByPbaEYdTgyt9"
SECRET_KEY = os.getenv("KLING_SECRET_KEY") or "MGL4AYfYgDFKTYGJpyfm4ftnbkFmtADN"

print("=" * 80)
print("🔐 Kling JWT Token 生成器")
print("=" * 80)
print()

# 當前時間戳
now = int(time.time())
exp_time = now + 300  # 5 分鐘後過期

# JWT Payload
payload = {
    "iss": ACCESS_KEY,      # Issuer = Access Key
    "iat": now,             # Issued At = 現在
    "nbf": now,             # Not Before = 現在
    "exp": exp_time         # Expiration = 現在 + 300 秒
}

print("📋 Payload 信息:")
print(json.dumps(payload, indent=2))
print()

# 生成 JWT Token
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

print("=" * 80)
print("✅ 生成的 JWT Token:")
print("=" * 80)
print()
print(token)
print()

# 解析 JWT 查看各部分
print("=" * 80)
print("🔍 JWT 結構分析:")
print("=" * 80)
print()

parts = token.split('.')
print(f"Header:    {parts[0]}")
print(f"Payload:   {parts[1]}")
print(f"Signature: {parts[2]}")
print()

# 解碼 Header
import base64
header = base64.urlsafe_b64decode(parts[0] + "==")
print("解碼後的 Header:")
print(json.dumps(json.loads(header), indent=2))
print()

# 解碼 Payload
payload_decoded = base64.urlsafe_b64decode(parts[1] + "==")
print("解碼後的 Payload:")
payload_data = json.loads(payload_decoded)
print(json.dumps(payload_data, indent=2))
print()

# 顯示時間信息
print("=" * 80)
print("⏰ 時間信息:")
print("=" * 80)
print()
print(f"發行時間 (iat): {datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')} (UTC)")
print(f"生效時間 (nbf): {datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')} (UTC)")
print(f"過期時間 (exp): {datetime.fromtimestamp(exp_time).strftime('%Y-%m-%d %H:%M:%S')} (UTC)")
print(f"有效期:        300 秒（5 分鐘）")
print()

# 使用示例
print("=" * 80)
print("📝 如何使用這個 JWT:")
print("=" * 80)
print()
print("1️⃣  複製上面的 Token")
print()
print("2️⃣  在 HTTP 請求中使用:")
print()
print("   curl -X POST https://api.klingai.com/v1/videos/text2video \\")
print("     -H 'Authorization: Bearer " + token[:20] + "...' \\")
print("     -H 'Content-Type: application/json' \\")
print("     -d '{")
print("       \"prompt\": \"A beautiful sunset\",")
print("       \"duration\": 5")
print("     }'")
print()

print("=" * 80)
print("💡 注意事項:")
print("=" * 80)
print()
print("✓ JWT 有效期只有 5 分鐘（300秒）")
print("✓ 超時後需要重新生成")
print("✓ 應該在 API 調用前立即生成，避免時間偏差")
print("✓ 不要在生產環境中洩露 Secret Key")
print()
