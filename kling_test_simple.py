#!/usr/bin/env python3
"""
Kling API 簡單測試 - 使用正確的端點和認證方式
"""

import os
import asyncio
import json
from dotenv import load_dotenv
import httpx

load_dotenv()

API_KEY = os.getenv("KLING_API_KEY")

if not API_KEY:
    print("❌ 未找到 KLING_API_KEY")
    exit(1)

print("✓ API Key 已載入")
print(f"  {API_KEY[:8]}...{API_KEY[-8:]}\n")

# 正確的端點（根據用戶提供的信息）
BASE_URL = "https://api.klingai.com"
ENDPOINT = f"{BASE_URL}/v1/videos/text2video"

# 測試提示詞（簡化版，用於快速測試）
SIMPLE_PROMPT = "A beautiful red and gold energy collision in cyberpunk style"

async def test():
    """測試 API"""
    print(f"🌐 端點: {ENDPOINT}")
    print(f"📝 提示詞: {SIMPLE_PROMPT}")
    print(f"⏱️ 時長: 5 秒\n")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "prompt": SIMPLE_PROMPT,
        "duration": 5
    }

    print("📤 發送請求...")

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            response = await client.post(ENDPOINT, json=payload, headers=headers)

            print(f"📥 HTTP {response.status_code}\n")

            if response.status_code < 300:
                print("✅ 成功！")
                result = response.json()
                print(json.dumps(result, indent=2, ensure_ascii=False))

                # 保存結果
                with open("test_result.json", "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print("\n💾 結果已保存到 test_result.json")

            else:
                print("❌ 失敗")
                print(response.text)

                # 保存錯誤
                with open("test_error.json", "w", encoding="utf-8") as f:
                    json.dump({
                        "status_code": response.status_code,
                        "error": response.text
                    }, f, indent=2)

        except Exception as e:
            print(f"❌ 異常: {str(e)}")


if __name__ == "__main__":
    asyncio.run(test())
