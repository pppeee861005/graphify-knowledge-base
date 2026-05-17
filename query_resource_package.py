#!/usr/bin/env python3
"""
Kling API - 查詢資源包詳細信息
"""

import os
import asyncio
import json
import time
import jwt
from datetime import datetime
from dotenv import load_dotenv
import httpx

load_dotenv()

# 讀取認證信息
ACCESS_KEY = os.getenv("KLING_ACCESS_KEY") or "Aeeh8L4F4pRD3LQyCNfdFhghbaebMhyD"
SECRET_KEY = os.getenv("KLING_SECRET_KEY") or "AbHNJDAEnA8nYTPLKeQrGbTFtfbamtYK"

print("=" * 70)
print("🔍 Kling AI - 查詢資源包信息")
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


async def query_account_info() -> dict:
    """
    查詢賬戶信息（包括資源包、額度等）
    """

    token = make_kling_token(ACCESS_KEY, SECRET_KEY)

    # 嘗試不同的端點
    endpoints = [
        "https://api.klingai.com/v1/users/me",
        "https://api.klingai.com/v1/account/info",
        "https://api.klingai.com/v1/account",
        "https://api.klingai.com/v1/balance",
        "https://api.klingai.com/v1/resources",
    ]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"✓ JWT Token: {token[:20]}...{token[-20:]}\n")

    for endpoint in endpoints:
        print(f"📤 嘗試端點: {endpoint}")

        async with httpx.AsyncClient(timeout=15) as client:
            try:
                response = await client.get(endpoint, headers=headers)

                print(f"   HTTP {response.status_code}")

                if response.status_code < 300:
                    print("   ✅ 成功！")
                    result = response.json()
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                    return result
                else:
                    print(f"   ❌ {response.text[:200]}")

            except Exception as e:
                print(f"   ❌ 異常: {str(e)[:80]}")

        print()

    return None


async def query_resource_package(package_id: str) -> dict:
    """
    查詢指定資源包的詳細信息
    """

    token = make_kling_token(ACCESS_KEY, SECRET_KEY)

    endpoints = [
        f"https://api.klingai.com/v1/resource-packages/{package_id}",
        f"https://api.klingai.com/v1/resources/{package_id}",
        f"https://api.klingai.com/v1/account/resources/{package_id}",
        f"https://api.klingai.com/v1/users/me/resources/{package_id}",
    ]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"🔍 查詢資源包 ID: {package_id}\n")

    for endpoint in endpoints:
        print(f"📤 端點: {endpoint}")

        async with httpx.AsyncClient(timeout=15) as client:
            try:
                response = await client.get(endpoint, headers=headers)

                print(f"   HTTP {response.status_code}")

                if response.status_code < 300:
                    print("   ✅ 成功！")
                    result = response.json()
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                    return result
                else:
                    print(f"   ❌ {response.text[:200]}")

            except Exception as e:
                print(f"   ❌ 異常: {str(e)[:80]}")

        print()

    return None


async def main():
    print("選擇操作:")
    print("1. 查詢賬戶信息和資源包列表")
    print("2. 查詢特定資源包詳情 (872110445955129360)")
    print()

    choice = input("請輸入選擇 (1 或 2) [預設 2]: ").strip() or "2"

    if choice == "1":
        print()
        await query_account_info()

    elif choice == "2":
        package_id = input("請輸入資源包 ID [預設 872110445955129360]: ").strip() or "872110445955129360"
        print()
        await query_resource_package(package_id)

    else:
        print("❌ 無效選擇")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⛔ 已取消")
        exit(0)
