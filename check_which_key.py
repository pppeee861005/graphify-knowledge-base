#!/usr/bin/env python3
"""
用兩個 Key 分別查詢任務，找出哪個 Key 有額度
"""

import os
import asyncio
import json
import time
import jwt
import httpx
from dotenv import load_dotenv

load_dotenv()

KEY_1_ACCESS = os.getenv("KLING_ACCESS_KEY_1") or "Aeeh8L4F4pRD3LQyCNfdFhghbaebMhyD"
KEY_1_SECRET = os.getenv("KLING_SECRET_KEY_1") or "AbHNJDAEnA8nYTPLKeQrGbTFtfbamtYK"

KEY_2_ACCESS = os.getenv("KLING_ACCESS_KEY") or "An98f9gCT9er3hAbfeyByPbaEYdTgyt9"
KEY_2_SECRET = os.getenv("KLING_SECRET_KEY") or "MGL4AYfYgDFKTYGJpyfm4ftnbkFmtADN"

print("=" * 80)
print("🔍 檢查哪個 Key 有額度")
print("=" * 80)
print()


def make_kling_token(access_key: str, secret_key: str) -> str:
    """生成 JWT token"""
    now = int(time.time())
    payload = {
        "iss": access_key,
        "iat": now,
        "nbf": now,
        "exp": now + 1800
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")


async def check_key(key_name, access_key, secret_key):
    """
    檢查某個 Key 的狀態和額度
    """

    token = make_kling_token(access_key, secret_key)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"\n{'=' * 80}")
    print(f"🔑 {key_name}")
    print(f"{'=' * 80}")
    print()
    print(f"Access Key: {access_key[:8]}...{access_key[-8:]}")
    print(f"Secret Key: {secret_key[:8]}...{secret_key[-8:]}")
    print()

    # 1. 先試著查詢任務列表（只需要認證，不需要額度）
    print("1️⃣  查詢任務列表...")
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                "https://api.klingai.com/v1/videos/text2video?pageNum=1&pageSize=10",
                headers=headers
            )

            if response.status_code == 200:
                result = response.json()
                tasks = result.get("data", [])
                print(f"   ✅ 成功！找到 {len(tasks)} 個任務")

                if len(tasks) > 0:
                    latest_task = tasks[0]
                    print(f"      最新任務: {latest_task.get('task_id')}")
                    print(f"      狀態: {latest_task.get('task_status')}")
            else:
                print(f"   ❌ 失敗 HTTP {response.status_code}")

    except Exception as e:
        print(f"   ❌ 異常: {str(e)[:100]}")

    print()

    # 2. 試著提交新任務（需要額度）
    print("2️⃣  嘗試提交新任務...")
    try:
        payload = {
            "prompt": "A beautiful sunset",
            "duration": "5"
        }

        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                "https://api.klingai.com/v1/videos/text2video",
                json=payload,
                headers=headers
            )

            if response.status_code in [200, 201]:
                print(f"   ✅ 成功！任務已提交")
                result = response.json()
                print(f"      任務 ID: {result.get('data', {}).get('task_id')}")

            elif response.status_code == 429:
                print(f"   ❌ 額度不足 (429)")
                result = response.json()
                print(f"      錯誤: {result.get('message')}")

            else:
                print(f"   ⚠️  HTTP {response.status_code}")
                result = response.json()
                print(f"      {result.get('message')}")

    except Exception as e:
        print(f"   ❌ 異常: {str(e)[:100]}")

    print()


async def main():
    print("比較兩個 API Key 的狀態...\n")

    await check_key("Key 1 (原始)", KEY_1_ACCESS, KEY_1_SECRET)
    await check_key("Key 2 (新購買)", KEY_2_ACCESS, KEY_2_SECRET)

    print("=" * 80)
    print("📊 總結")
    print("=" * 80)
    print()
    print("✅ 如果查詢任務成功但提交失敗 (429):")
    print("   → 這個 Key 的額度已用盡")
    print("   → 需要購買新的資源包")
    print()
    print("✅ 如果都成功:")
    print("   → 兩個 Key 都有有效額度")
    print()


if __name__ == "__main__":
    asyncio.run(main())
