#!/usr/bin/env python3
"""
使用兩個 Kling API Key 進行文字轉視頻測試
同時嘗試不同的模型和設置
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

print("=" * 70)
print("🎬 Kling AI - 雙 Key 文字轉視頻測試")
print("=" * 70)
print()


def make_token(access_key: str, secret_key: str) -> str:
    """生成 JWT token"""
    now = int(time.time())
    payload = {
        "iss": access_key,
        "iat": now,
        "nbf": now,
        "exp": now + 300
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")


async def test_video_generation(key_name, access_key, secret_key, prompt, duration=5):
    """
    測試視頻生成
    """
    token = make_token(access_key, secret_key)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 嘗試多個模型
    models = ["kling-v1-5", "kling-v1", "kling-v1-5-free"]

    payload = {
        "prompt": prompt,
        "duration": duration,
        "aspect_ratio": "16:9"
    }

    print(f"\n{'=' * 70}")
    print(f"🔑 測試 {key_name}")
    print(f"{'=' * 70}")
    print(f"Access Key: {access_key[:8]}...{access_key[-8:]}")
    print(f"Secret Key: {secret_key[:8]}...{secret_key[-8:]}")
    print(f"提示詞: {prompt}")
    print(f"時長: {duration} 秒")
    print()

    async with httpx.AsyncClient(timeout=20) as client:
        for model in models:
            payload["model"] = model

            print(f"📤 嘗試模型: {model}")

            try:
                response = await client.post(
                    "https://api.klingai.com/v1/videos/text2video",
                    json=payload,
                    headers=headers
                )

                print(f"   HTTP {response.status_code}")

                result = response.json()

                if response.status_code < 300:
                    print(f"   ✅ 成功！")
                    print(f"   Task ID: {result.get('data', {}).get('task_id')}")
                    print(f"   狀態: {result.get('data', {}).get('status')}")
                    return result

                elif response.status_code == 429:
                    print(f"   ❌ 額度不足 (429)")

                elif response.status_code == 400:
                    error_msg = result.get("message", "未知錯誤")
                    print(f"   ⚠️  參數錯誤 (400): {error_msg}")

                else:
                    error_msg = result.get("message", "未知錯誤")
                    print(f"   ⚠️  錯誤 ({response.status_code}): {error_msg}")

            except Exception as e:
                print(f"   ❌ 異常: {str(e)[:100]}")

            print()

    return None


async def main():
    # 簡短的提示詞
    simple_prompt = "Beautiful sunset over ocean with mountains"

    # 測試第一個 Key
    await test_video_generation(
        "Key 1 (原始)",
        KEY_1_ACCESS,
        KEY_1_SECRET,
        simple_prompt,
        duration=5
    )

    # 測試第二個 Key
    await test_video_generation(
        "Key 2 (新購買)",
        KEY_2_ACCESS,
        KEY_2_SECRET,
        simple_prompt,
        duration=5
    )

    print("\n" + "=" * 70)
    print("📊 測試完成")
    print("=" * 70)
    print()
    print("💡 如果都返回 429 (額度不足):")
    print("   1. 確認新購買的資源包已在官網激活")
    print("   2. 聯繫 Kling 官方客服檢查賬戶狀態")
    print()
    print("如果出現 4xx 錯誤:")
    print("   - 可能是 API 端點或參數不正確")
    print("   - 可以嘗試使用 Kling 官方 SDK 或 CLI 工具")
    print()


if __name__ == "__main__":
    asyncio.run(main())
