#!/usr/bin/env python3
"""
查詢所有 Kling 視頻生成任務
檢查請求是否成功
"""

import os
import asyncio
import json
import time
import jwt
import httpx
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

ACCESS_KEY = os.getenv("KLING_ACCESS_KEY") or "An98f9gCT9er3hAbfeyByPbaEYdTgyt9"
SECRET_KEY = os.getenv("KLING_SECRET_KEY") or "MGL4AYfYgDFKTYGJpyfm4ftnbkFmtADN"

print("=" * 80)
print("📋 Kling AI - 查詢所有視頻生成任務")
print("=" * 80)
print()


def make_kling_token(access_key: str, secret_key: str) -> str:
    """生成 JWT token"""
    now = int(time.time())
    payload = {
        "iss": access_key,
        "iat": now,
        "nbf": now,
        "exp": now + 1800  # 30 分鐘有效期（官方標準）
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")


async def query_all_tasks():
    """
    查詢所有視頻生成任務
    """
    token = make_kling_token(ACCESS_KEY, SECRET_KEY)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 多個可能的 API 端點
    endpoints = [
        "https://api.klingai.com/v1/videos/text2video?pageNum=1&pageSize=100",
        "https://api-singapore.klingai.com/v1/videos/text2video?pageNum=1&pageSize=100",
        "https://api-beijing.klingai.com/v1/videos/text2video?pageNum=1&pageSize=100",
    ]

    print(f"🔑 認證信息:")
    print(f"   Access Key: {ACCESS_KEY[:8]}...{ACCESS_KEY[-8:]}")
    print(f"   JWT Token: {token[:30]}...{token[-10:]}")
    print()
    print(f"📊 嘗試查詢任務列表...")
    print()

    async with httpx.AsyncClient(timeout=15) as client:
        for endpoint in endpoints:
            print(f"🌐 端點: {endpoint}")

            try:
                response = await client.get(endpoint, headers=headers)

                print(f"   HTTP {response.status_code}")

                if response.status_code < 300:
                    print("   ✅ 成功！")
                    result = response.json()

                    print()
                    print("=" * 80)
                    print("📋 任務列表")
                    print("=" * 80)
                    print()

                    if "data" in result and isinstance(result["data"], list):
                        tasks = result["data"]
                        if len(tasks) == 0:
                            print("❌ 沒有任務")
                        else:
                            print(f"✅ 找到 {len(tasks)} 個任務\n")

                            for i, task in enumerate(tasks, 1):
                                print(f"任務 #{i}")
                                print(f"   ID: {task.get('task_id', 'N/A')}")
                                print(f"   狀態: {task.get('task_status', 'N/A')}")
                                print(f"   創建時間: {datetime.fromtimestamp(task.get('created_at', 0) / 1000).strftime('%Y-%m-%d %H:%M:%S') if task.get('created_at') else 'N/A'}")
                                print(f"   更新時間: {datetime.fromtimestamp(task.get('updated_at', 0) / 1000).strftime('%Y-%m-%d %H:%M:%S') if task.get('updated_at') else 'N/A'}")

                                # 如果有結果，顯示視頻信息
                                if "task_result" in task and task["task_result"]:
                                    videos = task["task_result"].get("videos", [])
                                    if videos:
                                        print(f"   視頻數量: {len(videos)}")
                                        for j, video in enumerate(videos, 1):
                                            print(f"      視頻 {j}: {video.get('url', 'N/A')[:50]}...")

                                print()

                    else:
                        print("完整響應：")
                        print(json.dumps(result, indent=2, ensure_ascii=False)[:1000])

                    return result

                elif response.status_code == 401:
                    print(f"   ❌ 認證失敗 (401)")

                elif response.status_code == 429:
                    print(f"   ⚠️  速率限制 (429)")

                else:
                    print(f"   ⚠️  錯誤 {response.status_code}")

            except Exception as e:
                print(f"   ❌ 異常: {str(e)[:100]}")

            print()

    return None


async def query_specific_task(task_id: str):
    """
    查詢特定任務的詳細信息
    """
    token = make_kling_token(ACCESS_KEY, SECRET_KEY)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    endpoints = [
        f"https://api.klingai.com/v1/videos/text2video/{task_id}",
        f"https://api-singapore.klingai.com/v1/videos/text2video/{task_id}",
        f"https://api-beijing.klingai.com/v1/videos/text2video/{task_id}",
    ]

    print(f"🔍 查詢任務詳情: {task_id}")
    print()

    async with httpx.AsyncClient(timeout=15) as client:
        for endpoint in endpoints:
            print(f"🌐 端點: {endpoint}")

            try:
                response = await client.get(endpoint, headers=headers)

                print(f"   HTTP {response.status_code}")

                if response.status_code < 300:
                    print("   ✅ 成功！")
                    result = response.json()

                    print()
                    print("=" * 80)
                    print("📋 任務詳情")
                    print("=" * 80)
                    print()
                    print(json.dumps(result, indent=2, ensure_ascii=False))

                    return result

                elif response.status_code == 404:
                    print(f"   ⚠️  任務不存在 (404)")

                else:
                    print(f"   ⚠️  錯誤 {response.status_code}")

            except Exception as e:
                print(f"   ❌ 異常: {str(e)[:100]}")

            print()

    return None


async def main():
    print("選擇操作:")
    print("1️⃣  查詢所有任務")
    print("2️⃣  查詢特定任務")
    print()

    choice = input("請輸入選擇 (1 或 2) [預設 1]: ").strip() or "1"

    if choice == "1":
        print()
        await query_all_tasks()

    elif choice == "2":
        print()
        task_id = input("請輸入任務 ID: ").strip()
        if task_id:
            print()
            await query_specific_task(task_id)
        else:
            print("❌ 任務 ID 不能為空")

    else:
        print("❌ 無效選擇")

    print()
    print("=" * 80)
    print("💡 下一步建議")
    print("=" * 80)
    print()
    print("1. 如果看到 'succeed' 狀態：")
    print("   ✅ 請求成功！視頻已生成")
    print("   📥 可以點擊視頻 URL 下載")
    print()
    print("2. 如果看到 'processing' 狀態：")
    print("   ⏳ 視頻仍在生成中")
    print("   ⏰ 通常需要 30-120 秒")
    print()
    print("3. 如果看到 'failed' 狀態：")
    print("   ❌ 視頻生成失敗")
    print("   💬 查看錯誤信息了解原因")
    print()
    print("4. 如果沒有任何任務：")
    print("   ❌ 可能是額度不足導致請求被拒絕")
    print("   💳 檢查資源包是否已激活")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⛔ 已取消")
        exit(0)
