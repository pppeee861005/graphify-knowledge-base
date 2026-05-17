#!/usr/bin/env python3
"""
Kling API - 文字生圖測試
"""

import os
import asyncio
import json
import time
import jwt
import httpx
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv("KLING_ACCESS_KEY") or "Aeeh8L4F4pRD3LQyCNfdFhghbaebMhyD"
SECRET_KEY = os.getenv("KLING_SECRET_KEY") or "AbHNJDAEnA8nYTPLKeQrGbTFtfbamtYK"

print("=" * 70)
print("🖼️  Kling AI - 文字生圖測試")
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


async def submit_text_to_image(
    prompt: str,
    model: str = "kling-v3"
) -> dict:
    """
    提交文字生圖任務
    """

    token = make_kling_token(ACCESS_KEY, SECRET_KEY)

    # Kling 官方圖像生成端點
    endpoint = "https://api-beijing.klingai.com/v1/images/generations"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "model": model,
        "num_images": 1,
        "width": 1024,
        "height": 1024,
        "negative_prompt": "low quality, blurry, distorted"
    }

    print(f"📝 提示詞: {prompt}")
    print(f"🎨 模型: {model}")
    print(f"📏 尺寸: 1024x1024")
    print()
    print(f"🚀 提交至: {endpoint}\n")

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(endpoint, json=payload, headers=headers)

            print(f"HTTP {response.status_code}\n")
            result = response.json()

            print("📋 響應內容:")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:1000])

            if response.status_code < 300:
                print("\n✅ 成功！")
                if "images" in result:
                    print(f"   生成了 {len(result['images'])} 張圖片")
                    for i, img in enumerate(result['images']):
                        print(f"   圖片 {i+1}: {img[:100]}...")
            elif response.status_code == 429:
                print("\n❌ 額度不足（429）")
            else:
                print(f"\n⚠️  請求失敗")

            return result

    except Exception as e:
        print(f"❌ 異常: {str(e)}")
        return None


async def main():
    prompt = "A majestic golden dragon flying over a futuristic city with neon lights, detailed scales, cinematic lighting, 8k quality"
    await submit_text_to_image(prompt)


if __name__ == "__main__":
    asyncio.run(main())
