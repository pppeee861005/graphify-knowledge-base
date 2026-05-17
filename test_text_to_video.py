#!/usr/bin/env python3
"""
Kling API - 文字轉視頻測試
直接使用 Kling 官方 API
"""

import os
import asyncio
import json
import time
import jwt
import httpx
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# 讀取認證信息
ACCESS_KEY = os.getenv("KLING_ACCESS_KEY") or "Aeeh8L4F4pRD3LQyCNfdFhghbaebMhyD"
SECRET_KEY = os.getenv("KLING_SECRET_KEY") or "AbHNJDAEnA8nYTPLKeQrGbTFtfbamtYK"

print("=" * 70)
print("🎬 Kling AI - 文字轉視頻測試")
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


async def submit_text_to_video(
    prompt: str,
    duration: int = 5,
    model: str = "kling-v1-5"
) -> dict:
    """
    提交文字轉視頻任務
    """

    token = make_kling_token(ACCESS_KEY, SECRET_KEY)

    # Kling API 端點
    endpoint = "https://api.klingai.com/v1/videos/text2video"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "duration": duration,
        "model": model,
        "aspect_ratio": "16:9"
    }

    print(f"📝 提示詞: {prompt}")
    print(f"⏱️  時長: {duration} 秒")
    print(f"🎨 模型: {model}")
    print(f"📏 比例: 16:9")
    print()
    print(f"🚀 提交至: {endpoint}\n")

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(endpoint, json=payload, headers=headers)

            print(f"HTTP {response.status_code}\n")
            result = response.json()

            print("📋 響應內容:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

            return result

    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")
        return None


async def query_task_status(task_id: str) -> dict:
    """
    查詢視頻生成任務的狀態
    """

    token = make_kling_token(ACCESS_KEY, SECRET_KEY)

    endpoint = f"https://api.klingai.com/v1/videos/text2video/{task_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"🔍 查詢任務狀態: {task_id}\n")

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(endpoint, headers=headers)

            print(f"HTTP {response.status_code}\n")
            result = response.json()

            print("📋 任務狀態:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

            return result

    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")
        return None


async def main():
    print("選擇操作:")
    print("1️⃣  提交新的文字轉視頻任務")
    print("2️⃣  查詢任務狀態")
    print()

    choice = input("請輸入選擇 (1 或 2) [預設 1]: ").strip() or "1"

    if choice == "1":
        print()
        prompt = input("輸入提示詞 (預設: 'A beautiful red and gold energy collision in cyberpunk style'): ").strip()
        if not prompt:
            prompt = "A beautiful red and gold energy collision in cyberpunk style"

        duration = input("輸入時長秒數 (5-30，預設 5): ").strip()
        if not duration:
            duration = 5
        else:
            try:
                duration = int(duration)
            except:
                duration = 5

        print()
        await submit_text_to_video(prompt, duration)

    elif choice == "2":
        print()
        task_id = input("輸入任務 ID: ").strip()
        if not task_id:
            print("❌ 任務 ID 不能為空")
            return

        print()
        await query_task_status(task_id)

    else:
        print("❌ 無效選擇")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⛔ 已取消")
        exit(0)
