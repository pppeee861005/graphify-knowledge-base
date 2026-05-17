#!/usr/bin/env python3
"""
Kling API - 查詢現有任務
避免重複提交，檢查是否已有正在進行的任務
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
print("🔍 Kling AI - 查詢任務")
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


async def query_tasks() -> dict:
    """
    查詢所有任務
    """

    token = make_kling_token(ACCESS_KEY, SECRET_KEY)

    # 嘗試不同的端點
    endpoints = [
        "https://api.klingai.com/v1/videos/tasks",
        "https://api.klingai.com/v1/tasks",
        "https://api.klingai.com/v1/videos",
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
                    print(json.dumps(result, indent=2, ensure_ascii=False)[:500])
                    return result
                else:
                    print(f"   ❌ {response.text[:100]}")

            except Exception as e:
                print(f"   ❌ 異常: {str(e)[:80]}")

        print()

    return None


async def query_task_by_id(task_id: str) -> dict:
    """
    查詢指定任務的狀態
    """

    token = make_kling_token(ACCESS_KEY, SECRET_KEY)

    endpoints = [
        f"https://api.klingai.com/v1/videos/tasks/{task_id}",
        f"https://api.klingai.com/v1/videos/{task_id}",
        f"https://api.klingai.com/v1/tasks/{task_id}",
    ]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"🔍 查詢任務 ID: {task_id}\n")

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
                    print(f"   ❌ {response.text[:150]}")

            except Exception as e:
                print(f"   ❌ 異常: {str(e)[:80]}")

        print()

    return None


async def main():
    print("選擇操作:")
    print("1. 查詢所有任務")
    print("2. 查詢特定任務 ID 的狀態")
    print()

    choice = input("請輸入選擇 (1 或 2): ").strip()

    if choice == "1":
        print()
        await query_tasks()

    elif choice == "2":
        task_id = input("請輸入任務 ID: ").strip()
        print()
        await query_task_by_id(task_id)

    else:
        print("❌ 無效選擇")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⛔ 已取消")
        exit(0)
