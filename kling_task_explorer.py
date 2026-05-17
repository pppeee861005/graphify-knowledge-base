#!/usr/bin/env python3
"""
Kling API - 任務探索工具
嘗試多種方式查詢任務和帳戶信息
"""

import os
import asyncio
import json
import time
import jwt
from dotenv import load_dotenv
import httpx

load_dotenv()

ACCESS_KEY = os.getenv("KLING_ACCESS_KEY") or "Aeeh8L4F4pRD3LQyCNfdFhghbaebMhyD"
SECRET_KEY = os.getenv("KLING_SECRET_KEY") or "AbHNJDAEnA8nYTPLKeQrGbTFtfbamtYK"

print("=" * 70)
print("🔍 Kling AI - 任務探索工具")
print("=" * 70)
print()


def make_token():
    """生成 JWT token"""
    now = int(time.time())
    payload = {
        "iss": ACCESS_KEY,
        "iat": now,
        "nbf": now,
        "exp": now + 300
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


async def test_endpoint(method: str, endpoint: str, description: str, payload=None) -> bool:
    """測試單個端點"""
    token = make_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"📤 {description}")
    print(f"   {method} {endpoint}")

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            if method == "GET":
                response = await client.get(endpoint, headers=headers)
            elif method == "POST":
                response = await client.post(endpoint, json=payload or {}, headers=headers)

            print(f"   HTTP {response.status_code}", end="")

            if response.status_code < 300:
                print(" ✅")
                data = response.json()
                print(f"   結果: {json.dumps(data, indent=6, ensure_ascii=False)[:300]}")
                return True
            elif response.status_code == 404:
                print(" ❌ (404 Not Found)")
            elif response.status_code == 401:
                print(" ❌ (401 Unauthorized)")
            else:
                error_msg = response.text[:100]
                print(f" ❌ ({error_msg})")

        except Exception as e:
            print(f" ❌ (異常: {str(e)[:50]})")

    print()
    return False


async def explore_endpoints():
    """探索可能的端點"""

    print("🌐 嘗試不同的端點組合...\n")

    endpoints_to_try = [
        # 任務查詢相關
        ("GET", "https://api.klingai.com/v1/tasks", "查詢所有任務"),
        ("GET", "https://api.klingai.com/v1/videos/tasks", "查詢所有視頻任務"),
        ("GET", "https://api.klingai.com/v1/user/tasks", "查詢用戶任務"),
        ("GET", "https://api.klingai.com/v1/account/tasks", "查詢帳號任務"),

        # 帳戶信息相關
        ("GET", "https://api.klingai.com/v1/user", "獲取用戶信息"),
        ("GET", "https://api.klingai.com/v1/account", "獲取帳號信息"),
        ("GET", "https://api.klingai.com/v1/user/balance", "查詢帳號餘額"),
        ("GET", "https://api.klingai.com/v1/account/balance", "查詢帳號額度"),

        # 視頻相關
        ("GET", "https://api.klingai.com/v1/videos", "查詢所有視頻"),
        ("GET", "https://api.klingai.com/v1/videos/list", "列出視頻列表"),
        ("GET", "https://api.klingai.com/v1/videos/history", "查詢視頻歷史"),

        # 其他可能的端點
        ("GET", "https://api.klingai.com/v1/history", "查詢歷史"),
        ("GET", "https://api.klingai.com/v1/me", "查詢當前用戶"),
        ("GET", "https://api.klingai.com/v1/status", "查詢狀態"),
    ]

    found_count = 0
    for method, endpoint, description in endpoints_to_try:
        if await test_endpoint(method, endpoint, description):
            found_count += 1

    print("\n" + "=" * 70)
    if found_count == 0:
        print("❌ 未找到可用的任務查詢端點")
        print()
        print("💡 建議:")
        print("   1. 檢查 Kling API 官方文檔中的正確端點")
        print("   2. 查看是否有任務管理的 Web 界面")
        print("   3. 如果有已生成的任務 ID，可以用特定 ID 查詢")
    else:
        print(f"✅ 找到 {found_count} 個可用端點")
    print("=" * 70)


async def query_specific_task():
    """查詢特定任務 ID 的狀態"""
    print("\n" + "=" * 70)
    print("🔍 查詢特定任務")
    print("=" * 70)
    print()

    task_id = input("請輸入任務 ID (或按 Enter 跳過): ").strip()

    if not task_id:
        print("⏭️  已跳過")
        return

    endpoints = [
        f"https://api.klingai.com/v1/tasks/{task_id}",
        f"https://api.klingai.com/v1/videos/tasks/{task_id}",
        f"https://api.klingai.com/v1/videos/{task_id}",
        f"https://api.klingai.com/v1/user/tasks/{task_id}",
    ]

    token = make_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"查詢任務 ID: {task_id}\n")

    async with httpx.AsyncClient(timeout=10) as client:
        for endpoint in endpoints:
            try:
                response = await client.get(endpoint, headers=headers)

                print(f"📤 {endpoint}")
                print(f"   HTTP {response.status_code}", end="")

                if response.status_code < 300:
                    print(" ✅")
                    data = response.json()
                    print(json.dumps(data, indent=2, ensure_ascii=False))
                    return
                else:
                    print(f" ❌")

            except Exception as e:
                print(f"❌ {str(e)[:80]}")

    print()
    print("❌ 未找到該任務")


async def main():
    print("選擇操作:\n")
    print("1. 探索所有可能的端點")
    print("2. 查詢特定任務 ID")
    print("3. 退出")
    print()

    choice = input("請輸入選擇 (1-3): ").strip()

    if choice == "1":
        await explore_endpoints()
    elif choice == "2":
        await query_specific_task()
    elif choice == "3":
        print("👋 再見")
        return
    else:
        print("❌ 無效選擇")

    # 詢問是否繼續
    print()
    again = input("是否繼續? (y/n): ").strip().lower()
    if again == "y":
        await main()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⛔ 已取消")
        exit(0)
