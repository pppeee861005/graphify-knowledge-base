#!/usr/bin/env python3
"""
Kling API - 任務查詢工具
查詢特定任務 ID 的詳細信息和進度
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
print("🔍 Kling AI - 任務查詢工具")
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


async def query_task_status(task_id: str) -> dict:
    """
    查詢特定任務的狀態
    """
    token = make_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 嘗試多個可能的端點格式
    endpoints = [
        f"https://api.klingai.com/v1/videos/{task_id}",
        f"https://api.klingai.com/v1/tasks/{task_id}",
        f"https://api.klingai.com/v1/videos/tasks/{task_id}",
        f"https://api.klingai.com/videos/{task_id}",
    ]

    print(f"🔍 查詢任務 ID: {task_id}\n")

    async with httpx.AsyncClient(timeout=15) as client:
        for endpoint in endpoints:
            print(f"📤 嘗試: {endpoint}")

            try:
                response = await client.get(endpoint, headers=headers)

                print(f"   HTTP {response.status_code}", end="")

                if response.status_code < 300:
                    print(" ✅\n")
                    result = response.json()
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                    return result

                elif response.status_code == 404:
                    print(" (404)")
                elif response.status_code == 401:
                    print(" (401)")
                else:
                    print(f" ({response.status_code})")

            except Exception as e:
                print(f"   ❌ {str(e)[:60]}")

            print()

    print("❌ 未找到該任務")
    return None


async def list_recent_tasks() -> dict:
    """
    嘗試列出最近的任務
    """
    token = make_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("📋 嘗試查詢最近的任務...\n")

    endpoints = [
        "https://api.klingai.com/v1/videos",
        "https://api.klingai.com/v1/tasks",
        "https://api.klingai.com/v1/videos/tasks",
    ]

    async with httpx.AsyncClient(timeout=15) as client:
        for endpoint in endpoints:
            print(f"📤 嘗試: {endpoint}")

            try:
                response = await client.get(endpoint, headers=headers)

                print(f"   HTTP {response.status_code}", end="")

                if response.status_code < 300:
                    print(" ✅\n")
                    result = response.json()
                    print(json.dumps(result, indent=2, ensure_ascii=False)[:1000])
                    return result
                else:
                    print(f" ({response.status_code})")

            except Exception as e:
                print(f"   ❌ {str(e)[:60]}")

            print()

    print("❌ 未找到可用的端點")
    return None


async def main():
    print("選擇操作:\n")
    print("1. 查詢特定任務 ID")
    print("2. 列出最近任務")
    print("3. 查看幫助")
    print()

    choice = input("請輸入選擇 (1-3): ").strip()

    if choice == "1":
        print()
        task_id = input("請輸入任務 ID: ").strip()
        if task_id:
            print()
            await query_task_status(task_id)

    elif choice == "2":
        print()
        await list_recent_tasks()

    elif choice == "3":
        print_help()

    else:
        print("❌ 無效選擇")


def print_help():
    """打印幫助信息"""
    print()
    print("=" * 70)
    print("📚 幫助信息")
    print("=" * 70)
    print()
    print("如何查詢任務歷史:")
    print()
    print("1️⃣  方式一：使用任務 ID 查詢")
    print("   - 運行腳本，選擇「1. 查詢特定任務 ID」")
    print("   - 輸入你的任務 ID（通常由 API 在生成時返回）")
    print()
    print("2️⃣  方式二：查看 Web 界面")
    print("   - 訪問 https://www.klingai.com")
    print("   - 登錄你的帳號")
    print("   - 進入「任務管理」或「生成記錄」頁面")
    print("   - 查看所有已生成和進行中的任務")
    print()
    print("3️⃣  方式三：檢查之前的輸出")
    print("   - 運行 kling_nana_video_final.py 時")
    print("   - 響應會保存到 generated_videos/kling_response.json")
    print("   - 其中包含任務 ID 等信息")
    print()
    print("=" * 70)
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⛔ 已取消")
        exit(0)
