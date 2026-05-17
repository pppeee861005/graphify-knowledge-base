#!/usr/bin/env python3
"""
Kling API 視頻生成腳本 - 龍蝦娜娜系列
使用版本 B：極度動感衝擊版（高能量版）生成 5 秒動畫
"""

import os
import asyncio
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# 載入 .env 文件
load_dotenv()


def parse_kling_credentials():
    """從環境變數中獲取 Kling API 認證信息"""
    access_key = os.getenv("KLING_ACCESS_KEY")
    secret_key = os.getenv("KLING_SECRET_KEY")

    if not access_key or not secret_key:
        raise ValueError("無法獲取 Kling API 認證信息。請確保 .env 中設置了 KLING_ACCESS_KEY 和 KLING_SECRET_KEY")

    return {
        "access_key": access_key,
        "secret_key": secret_key
    }


# 龍蝦娜娜系列 - 版本 B 提示詞
NANA_PROMPT_V2 = """EXPLOSIVE ACTION MOVIE POSTER: Ultra-dynamic confrontation between two beautiful
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


async def generate_video_with_kling(prompt: str, duration: float = 5.0,
                                    output_dir: str = "generated_videos") -> dict:
    """
    使用 Kling API 生成視頻

    Args:
        prompt: 視頻生成提示詞
        duration: 視頻時長（秒）- Kling 通常支持 5-10 秒
        output_dir: 輸出目錄

    Returns:
        API 響應信息
    """

    # 創建輸出目錄
    os.makedirs(output_dir, exist_ok=True)

    # 獲取認證信息
    try:
        credentials = parse_kling_credentials()
        access_key = credentials["access_key"]
        secret_key = credentials["secret_key"]
    except Exception as e:
        print(f"❌ 認證失敗: {str(e)}")
        return None

    print("=" * 70)
    print("🎬 Kling AI 視頻生成工具 - 龍蝦娜娜系列")
    print("=" * 70)
    print()

    # 驗證認證信息
    print("🔐 認證信息驗證:")
    print(f"   ✓ Access Key: {access_key[:8]}...{access_key[-8:]}")
    print(f"   ✓ Secret Key: {secret_key[:8]}...{secret_key[-8:]}")
    print()

    # 顯示提示詞信息
    print(f"📝 提示詞（版本 B：極度動感衝擊版）:")
    print(f"   {prompt[:100]}...")
    print()
    print(f"⏱️ 視頻時長: {duration} 秒")
    print(f"📂 輸出目錄: {os.path.abspath(output_dir)}")
    print()

    # 嘗試使用官方 SDK
    try:
        from kling.client import KlingClient
        from kling.api.text_to_video import TextToVideoRequest

        print("✓ 已檢測到 Kling SDK，使用官方 SDK...")
        print()

        # 初始化客戶端
        client = KlingClient(
            access_key=access_key,
            secret_key=secret_key
        )

        # 創建視頻生成請求
        request = TextToVideoRequest(
            prompt=prompt,
            duration=duration,
            mode="generate"  # 或 "edit" 取決於 SDK 支持
        )

        print("🎬 正在發送視頻生成請求...")
        response = await client.text_to_video(request)

        print(f"\n✅ 視頻生成任務已提交！")
        print(f"📋 任務 ID: {response.task_id}")
        print(f"📊 狀態: {response.status}")

        # 保存響應信息
        response_file = os.path.join(output_dir, "kling_response.json")
        with open(response_file, "w", encoding="utf-8") as f:
            json.dump(response.dict(), f, indent=2, ensure_ascii=False)
        print(f"💾 響應已保存到: {response_file}")

        return response

    except ImportError:
        print("⚠️  Kling SDK 未安裝，使用 HTTP API...")
        print()
        return await generate_video_via_http(
            prompt=prompt,
            duration=duration,
            access_key=access_key,
            secret_key=secret_key,
            output_dir=output_dir
        )


async def generate_video_via_http(prompt: str, duration: float = 5.0,
                                  access_key: str = None, secret_key: str = None,
                                  output_dir: str = "generated_videos") -> dict:
    """
    使用 HTTP 直接調用 Kling API（SDK 未安裝時使用）
    """
    try:
        import httpx
    except ImportError:
        print("❌ 需要安裝 httpx: pip install httpx")
        print("   或安裝官方 SDK: pip install kling-ai-sdk")
        return None

    # Kling API 端點
    api_base = "https://api.klingai.com"
    endpoint = f"{api_base}/v1/videos/text2video"

    print("🌐 使用 HTTP API 連接 Kling...")
    print(f"   端點: {endpoint}")
    print()

    # 準備請求頭 - Bearer token 格式
    # 嘗試方式：Bearer {access_key} 或 Bearer {access_key}:{secret_key}
    auth_token = f"{access_key}:{secret_key}"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    # 準備請求負載
    payload = {
        "prompt": prompt,
        "duration": int(duration),
        "mode": "generate"
    }

    print("📤 發送請求...")
    print(f"   認證方式: Authorization header (直接使用 Access Key)")

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                endpoint,
                json=payload,
                headers=headers
            )

            print(f"📥 收到響應 (HTTP {response.status_code})")
            print()

            if response.status_code in [200, 201]:
                result = response.json()

                print(f"✅ 視頻生成任務已提交！")
                task_id = result.get("data", {}).get("task_id") or result.get("task_id")
                print(f"📋 任務 ID: {task_id}")
                print(f"📊 狀態: {result.get('data', {}).get('status') or result.get('status')}")
                print()

                # 保存完整響應
                response_file = os.path.join(output_dir, "kling_response.json")
                with open(response_file, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"💾 響應已保存到: {response_file}")

                return result

            else:
                print(f"❌ API 錯誤 (HTTP {response.status_code})")
                print(f"📄 響應:")
                print(response.text)

                # 保存錯誤信息
                error_file = os.path.join(output_dir, "kling_error.json")
                with open(error_file, "w", encoding="utf-8") as f:
                    json.dump({
                        "status_code": response.status_code,
                        "response": response.text
                    }, f, indent=2, ensure_ascii=False)

                return None

        except Exception as e:
            print(f"❌ 請求失敗: {str(e)}")
            return None


def print_next_steps(task_id: str = None):
    """打印後續步驟"""
    print()
    print("=" * 70)
    print("✨ 任務已提交，接下來該怎麼做？")
    print("=" * 70)
    print()

    print("1️⃣  等待視頻生成")
    print("   └─ Kling 通常需要 1-5 分鐘完成視頻生成")
    print()

    print("2️⃣  查詢生成進度")
    if task_id:
        print(f"   └─ 使用任務 ID: {task_id}")
    print("   └─ 發送 GET 請求到: /v1/videos/text2video/{task_id}")
    print()

    print("3️⃣  下載視頻")
    print("   └─ 當狀態變為 'succeed' 時，即可下載視頻")
    print("   └─ 下載地址將在響應中提供")
    print()

    print("4️⃣  後期處理")
    print("   └─ 在 Premiere Pro/DaVinci Resolve 中添加字幕")
    print("   └─ 調整色彩、對比度、音效")
    print("   └─ 導出為 4K 或 1080p")
    print()

    print("=" * 70)


async def main():
    """主函數"""

    # 生成視頻
    result = await generate_video_with_kling(
        prompt=NANA_PROMPT_V2,
        duration=5.0,
        output_dir="generated_videos"
    )

    # 顯示下一步
    if result:
        task_id = result.get("data", {}).get("task_id") or result.get("task_id")
        print_next_steps(task_id)

    print()
    print("💡 提示:")
    print("   • 檢查 generated_videos/ 目錄查看詳細響應")
    print("   • 保存任務 ID 以便後續查詢進度")
    print("   • 建議每隔 30 秒查詢一次進度")


if __name__ == "__main__":
    asyncio.run(main())
