#!/usr/bin/env python3
"""試試用 Secret Key 代替 Access Key"""

import os
import asyncio
import json
from dotenv import load_dotenv
import httpx

load_dotenv()

# 注意：你提到有 Secret Key，讓我們也試試
SECRET_KEY = "AbHNJDAEnA8nYTPLKeQrGbTFtfbamtYK"  # 從之前的 .env 直接使用

ENDPOINT = "https://api.klingai.com/v1/videos/text2video"
PROMPT = "A beautiful red and gold energy collision in cyberpunk style"

async def test():
    headers = {
        "Authorization": f"Bearer {SECRET_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": PROMPT,
        "duration": 5
    }

    print(f"🔑 嘗試用 Secret Key: {SECRET_KEY[:8]}...{SECRET_KEY[-8:]}")
    print(f"🌐 端點: {ENDPOINT}\n")

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            response = await client.post(ENDPOINT, json=payload, headers=headers)
            print(f"HTTP {response.status_code}")
            print(response.text)
        except Exception as e:
            print(f"異常: {str(e)}")

asyncio.run(test())
