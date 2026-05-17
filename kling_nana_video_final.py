#!/usr/bin/env python3
"""
Kling AI 視頻生成腳本 - 龍蝦娜娜系列
正確的認證方式：用 AccessKey + SecretKey 生成 JWT token
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

if not ACCESS_KEY or not SECRET_KEY:
    print("❌ 未找到 API 密鑰")
    exit(1)

print("=" * 70)
print("🎬 Kling AI 視頻生成工具 - 龍蝦娜娜系列")
print("=" * 70)
print()

print(f"✓ 認證信息已加載:")
print(f"   AccessKey: {ACCESS_KEY[:8]}...{ACCESS_KEY[-8:]}")
print(f"   SecretKey: {SECRET_KEY[:8]}...{SECRET_KEY[-8:]}")
print()


def make_kling_token(access_key: str, secret_key: str) -> str:
    """
    使用 AccessKey 和 SecretKey 生成 JWT token
    """
    now = int(time.time())
    payload = {
        "iss": access_key,      # issuer = AccessKey
        "iat": now,             # issued at
        "nbf": now,             # not before
        "exp": now + 300        # expires in 5 minutes
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


async def generate_video(prompt: str, duration: int = 5) -> dict:
    """
    調用 Kling API 生成視頻
    """

    # 生成 JWT token
    print("🔐 生成 JWT token...")
    token = make_kling_token(ACCESS_KEY, SECRET_KEY)
    print(f"   ✓ Token: {token[:20]}...{token[-20:]}")
    print()

    # API 端點和請求
    endpoint = "https://api.klingai.com/v1/videos/text2video"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "duration_seconds": duration,
        "aspect_ratio": "16:9"
    }

    print(f"📝 提示詞:")
    print(f"   {prompt[:80]}...")
    print()
    print(f"⏱️  時長: {duration} 秒")
    print(f"🌐 端點: {endpoint}")
    print()

    print("📤 發送請求...")

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.post(endpoint, json=payload, headers=headers)

            print(f"📥 HTTP {response.status_code}")
            print()

            if response.status_code < 300:
                print("✅ 成功！")
                result = response.json()
                print(json.dumps(result, indent=2, ensure_ascii=False))

                # 保存結果
                os.makedirs("generated_videos", exist_ok=True)
                with open("generated_videos/kling_response.json", "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)

                return result

            else:
                print("❌ 失敗")
                error_text = response.text
                print(error_text)

                # 保存錯誤
                os.makedirs("generated_videos", exist_ok=True)
                with open("generated_videos/kling_error.json", "w", encoding="utf-8") as f:
                    json.dump({
                        "status_code": response.status_code,
                        "error": error_text,
                        "timestamp": datetime.now().isoformat()
                    }, f, indent=2, ensure_ascii=False)

                return None

        except Exception as e:
            print(f"❌ 異常: {str(e)}")
            return None


# 龍蝦娜娜系列 - 版本 B 提示詞
NANA_PROMPT = """EXPLOSIVE ACTION MOVIE POSTER: Ultra-dynamic confrontation between two beautiful
anime girls in a high-tech cyberpunk arena. The image bursts with kinetic energy.

LEFT: A lithe, graceful girl with impossibly long flowing red hair (waist-length)
in motion, hair dramatically whipping behind and around her as if caught in a
powerful wind or energy field. She wears red with red glowing effects, body language
shows she's lunging or leaping toward the center with intense focus. Her red-glowing
eyes are fierce and determined. Red light trails follow her movement.

RIGHT: A voluptuous, confident girl with sleek shoulder-length gold hair that
seems perfectly unmoved despite the energy around her. She wears black and gold,
body language shows controlled, calculated power. Her cold golden eyes are
merciless. Gold light trails follow her position.

BETWEEN THEM: An explosion of visual energy where their forces collide.
Massive red and gold light burst, creating an X-shaped shockwave. Digital data
streams flowing in every direction. Holographic shards and particles suspended
in mid-air, both red and gold fragments frozen in the moment of impact.

BACKGROUND: Hyper-futuristic cyberpunk megacity at night. Towering neon
skyscrapers reaching into clouds of digital haze. Data streams like rivers of
light flowing between buildings. Thousands of virtual vehicles on impossible
highways creating layers of motion. Electrical storm clouds above. Massive
holographic billboards displaying fragments of text.

LIGHTING: Extreme cinematic contrast. Left half is dominantly red/warm,
right half is dominantly gold/cool. The center collision point is blindingly bright
white-hot. Lens flares, light streaks, depth of field effect. Volumetric god rays
cutting through the scene.

MOOD: Tension, power, destiny, inevitable conflict, cyberpunk dystopia,
epic sci-fi action. The poster screams "WHO WILL WIN?"

QUALITY: 4K movie poster, professional color grading, HDR effect,
extreme detail, every fiber of hair visible, every clothing texture rendered,
masterpiece cinematic composition."""


async def main():
    """主函數"""

    result = await generate_video(
        prompt=NANA_PROMPT,
        duration=5
    )

    print()
    print("=" * 70)
    print("✨ 任務已提交")
    print("=" * 70)
    print()

    if result:
        task_id = result.get("data", {}).get("task_id") or result.get("task_id")
        print(f"📋 任務 ID: {task_id}")
        print()
        print("📝 下一步:")
        print("   1. 保存任務 ID 用於查詢進度")
        print("   2. 每隔 30 秒查詢一次進度")
        print("   3. 當狀態變為 'succeed' 時下載視頻")
        print()
        print("💾 詳細結果已保存到: generated_videos/kling_response.json")

    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⛔ 已取消")
        exit(0)
