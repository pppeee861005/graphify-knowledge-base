#!/usr/bin/env python3
"""
快速重試文字轉視頻
"""

import os
import asyncio
import json
import time
import jwt
import httpx
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv("KLING_ACCESS_KEY")
SECRET_KEY = os.getenv("KLING_SECRET_KEY")

if not ACCESS_KEY or not SECRET_KEY:
    print("❌ 缺少認證信息，請設置 KLING_ACCESS_KEY 和 KLING_SECRET_KEY")
    exit(1)


def make_token(ak, sk):
    now = int(time.time())
    payload = {"iss": ak, "iat": now, "nbf": now, "exp": now + 300}
    return jwt.encode(payload, sk, algorithm="HS256")


async def test_video():
    token = make_token(ACCESS_KEY, SECRET_KEY)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": "A beautiful sunset over mountains with golden light",
        "duration": 5,
        "model": "kling-v1-5",
        "aspect_ratio": "16:9"
    }

    print("🎬 嘗試提交文字轉視頻任務...\n")

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            response = await client.post(
                "https://api.klingai.com/v1/videos/text2video",
                json=payload,
                headers=headers
            )

            print(f"HTTP {response.status_code}\n")
            result = response.json()

            if response.status_code < 300:
                print("✅ 成功！")
                print(f"   Task ID: {result.get('data', {}).get('task_id')}")
                print(f"   狀態: {result.get('data', {}).get('status')}")
            elif response.status_code == 429:
                print("❌ 還是額度不足")
                print("   💡 建議：")
                print("   1. 確認資源包已在官網激活")
                print("   2. 再等 2-3 分鐘讓系統同步")
                print("   3. 如果仍有問題，聯繫 Kling 官方客服")
            else:
                print(f"⚠️  錯誤 {response.status_code}")

            print("\n完整響應：")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        except Exception as e:
            print(f"❌ 異常: {e}")


if __name__ == "__main__":
    asyncio.run(test_video())
