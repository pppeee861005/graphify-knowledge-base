#!/usr/bin/env python3
"""
Kling API - 賬戶診斷工具
檢查餘額、資源包狀態、額度信息
"""

import os
import asyncio
import json
import time
import jwt
import httpx
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv("KLING_ACCESS_KEY") or "Aeeh8L4F4pRD3LQyCNfdFhghbaebMhyD"
SECRET_KEY = os.getenv("KLING_SECRET_KEY") or "AbHNJDAEnA8nYTPLKeQrGbTFtfbamtYK"

print("=" * 70)
print("🔍 Kling AI - 賬戶診斷工具")
print("=" * 70)
print()


def make_kling_token(access_key: str, secret_key: str) -> str:
    """生成 JWT token"""
    now = int(time.time())
    payload = {
        "iss": access_key,
        "iat": now,
        "nbf": now,
        "exp": now + 300
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")


async def diagnose():
    """
    診斷賬戶狀態
    """
    token = make_kling_token(ACCESS_KEY, SECRET_KEY)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"🔐 認證信息:")
    print(f"   Access Key: {ACCESS_KEY[:8]}...{ACCESS_KEY[-8:]}")
    print(f"   Secret Key: {SECRET_KEY[:8]}...{SECRET_KEY[-8:]}")
    print(f"   Token: {token[:20]}...{token[-20:]}")
    print()

    # 多個可能的賬戶端點
    account_endpoints = [
        ("用戶信息", "https://api.klingai.com/v1/users/me"),
        ("賬戶餘額", "https://api.klingai.com/v1/account/balance"),
        ("賬戶詳情", "https://api.klingai.com/v1/account"),
        ("資源套餐", "https://api.klingai.com/v1/account/resource-packages"),
        ("使用量", "https://api.klingai.com/v1/account/usage"),
        ("計費信息", "https://api.klingai.com/v1/account/billing"),
    ]

    print("📊 查詢賬戶信息:")
    print()

    async with httpx.AsyncClient(timeout=10) as client:
        for name, endpoint in account_endpoints:
            try:
                response = await client.get(endpoint, headers=headers)
                status = response.status_code

                if status < 300:
                    print(f"✅ {name} ({endpoint})")
                    print(f"   HTTP {status}")
                    result = response.json()
                    print(json.dumps(result, indent=4, ensure_ascii=False)[:500])
                    print()
                else:
                    print(f"⚠️  {name} ({endpoint})")
                    print(f"   HTTP {status}")
                    try:
                        result = response.json()
                        print(f"   {result}")
                    except:
                        print(f"   {response.text[:200]}")
                    print()

            except Exception as e:
                print(f"❌ {name}")
                print(f"   異常: {str(e)}")
                print()

    print()
    print("=" * 70)
    print("📝 診斷建議:")
    print("=" * 70)
    print()
    print("1. 如果看到 ✅ 的結果，檢查 'balance' 或 'quota' 字段")
    print("2. 如果都是 ⚠️ 或 ❌，可能是:")
    print("   - API Key 已過期")
    print("   - 賬戶被鎖定")
    print("   - Kling API 服務不可用")
    print()
    print("3. 新購買的資源包通常需要 5-10 分鐘才能在 API 中生效")
    print()


if __name__ == "__main__":
    asyncio.run(diagnose())
