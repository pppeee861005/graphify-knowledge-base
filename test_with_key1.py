#!/usr/bin/env python3
"""
用第一個 Key 測試文字轉視頻
"""

import os
import asyncio
import json
import time
import jwt
import httpx
from dotenv import load_dotenv

load_dotenv()

# 使用第一個 Key
ACCESS_KEY = os.getenv("KLING_ACCESS_KEY_1") or "Aeeh8L4F4pRD3LQyCNfdFhghbaebMhyD"
SECRET_KEY = os.getenv("KLING_SECRET_KEY_1") or "AbHNJDAEnA8nYTPLKeQrGbTFtfbamtYK"

print("=" * 80)
print("🎬 用第一個 Key 測試文字轉視頻")
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


async def submit_video():
    """提交文字轉視頻任務"""

    token = make_kling_token(ACCESS_KEY, SECRET_KEY)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": "A stunning golden dragon with intricate scales, flying gracefully over a futuristic neon city with holographic buildings at sunset, cinematic quality, 8k",
        "duration": "5",
        "aspect_ratio": "16:9",
        "model_name": "kling-v2-master"
    }

    print(f"🔑 使用 API Key:")
    print(f"   Access Key: {ACCESS_KEY[:8]}...{ACCESS_KEY[-8:]}")
    print()
    print(f"📝 提示詞: {payload['prompt'][:80]}...")
    print(f"⏱️  時長: {payload['duration']} 秒")
    print(f"📏 比例: {payload['aspect_ratio']}")
    print(f"🎨 模型: {payload['model_name']}")
    print()
    print(f"🚀 提交任務...")
    print()

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                "https://api.klingai.com/v1/videos/text2video",
                json=payload,
                headers=headers
            )

            print(f"HTTP {response.status_code}\n")

            result = response.json()

            if response.status_code == 200 or response.status_code == 201:
                print("✅ 成功提交！")
                print()
                print("📋 任務信息:")

                task_data = result.get("data", {})
                task_id = task_data.get("task_id")
                task_status = task_data.get("task_status")

                print(f"   任務 ID: {task_id}")
                print(f"   狀態: {task_status}")
                print(f"   建立時間: {task_data.get('created_at')}")
                print()
                print("💡 接下來:")
                print(f"   使用此任務 ID 查詢進度: {task_id}")
                print(f"   命令: python query_all_tasks.py")
                print(f"   然後選擇 2，輸入任務 ID")

                return result

            elif response.status_code == 429:
                print("❌ 額度不足 (429)")
                print()
                print("📊 響應:")
                print(json.dumps(result, indent=2, ensure_ascii=False))

            else:
                print(f"⚠️  錯誤 {response.status_code}")
                print()
                print("📊 響應:")
                print(json.dumps(result, indent=2, ensure_ascii=False))

            return result

    except Exception as e:
        print(f"❌ 異常: {str(e)}")
        return None


if __name__ == "__main__":
    asyncio.run(submit_video())
