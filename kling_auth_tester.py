#!/usr/bin/env python3
"""
Kling API 認證方式測試工具
嘗試多種認證方式找出正確的方法
"""

import os
import asyncio
import json
import base64
import hashlib
import hmac
from datetime import datetime
from dotenv import load_dotenv
import httpx

load_dotenv()

API_KEY = os.getenv("KLING_API_KEY")

if not API_KEY:
    print("❌ 未找到 API 密鑰")
    print("   KLING_API_KEY:", API_KEY[:8] if API_KEY else "未設置")
    exit(1)

print(f"✓ 已加載認證信息")
print(f"   API Key: {API_KEY[:8]}...{API_KEY[-8:]}")
print()

# 簡單測試提示詞（縮短版）
SIMPLE_PROMPT = "A beautiful red and gold energy collision in cyberpunk style"

# API 端點（根據官方 README）
BASE_URL = "https://api.kling.ai/v1"
ENDPOINT = f"{BASE_URL}/videos/text2video"


async def test_auth_method_1():
    """方法 1: Bearer + Access Key (官方 SDK 方式)"""
    print("\n" + "="*60)
    print("測試方法 1: Bearer + Access Key (官方 SDK 推薦方式)")
    print("="*60)

    headers = {
        "Authorization": f"Bearer {ACCESS_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "prompt": SIMPLE_PROMPT,
        "duration": 5
    }

    print(f"Headers: {headers}")
    print(f"Endpoint: {ENDPOINT}")

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.post(ENDPOINT, json=payload, headers=headers)
            print(f"HTTP {resp.status_code}")
            if resp.status_code < 300:
                print("✅ 成功！")
                print(resp.json())
            else:
                print(f"❌ 失敗: {resp.text[:300]}")
        except Exception as e:
            print(f"❌ 異常: {str(e)}")


async def test_auth_method_2():
    """方法 2: Bearer + Secret Key"""
    print("\n" + "="*60)
    print("測試方法 2: Bearer + Secret Key")
    print("="*60)

    headers = {
        "Authorization": f"Bearer {SECRET_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": SIMPLE_PROMPT,
        "duration": 5
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.post(ENDPOINT, json=payload, headers=headers)
            print(f"HTTP {resp.status_code}")
            if resp.status_code < 300:
                print("✅ 成功！")
                print(resp.json())
            else:
                print(f"❌ 失敗: {resp.text[:200]}")
        except Exception as e:
            print(f"❌ 異常: {str(e)}")


async def test_auth_method_3():
    """方法 3: 在 Payload 中包含 access_key 和 secret_key"""
    print("\n" + "="*60)
    print("測試方法 3: Payload 中包含 access_key 和 secret_key")
    print("="*60)

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": SIMPLE_PROMPT,
        "duration": 5,
        "access_key": ACCESS_KEY,
        "secret_key": SECRET_KEY
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.post(ENDPOINT, json=payload, headers=headers)
            print(f"HTTP {resp.status_code}")
            if resp.status_code < 300:
                print("✅ 成功！")
                print(resp.json())
            else:
                print(f"❌ 失敗: {resp.text[:200]}")
        except Exception as e:
            print(f"❌ 異常: {str(e)}")


async def test_auth_method_4():
    """方法 4: AWS Signature V4 風格簽名"""
    print("\n" + "="*60)
    print("測試方法 4: AWS Signature V4 簽名")
    print("="*60)

    # 簡化版的簽名（可能不完全正確，但值得一試）
    timestamp = datetime.utcnow().isoformat() + "Z"
    string_to_sign = f"POST\n{ENDPOINT}\n{timestamp}\n{SIMPLE_PROMPT}"
    signature = base64.b64encode(
        hmac.new(
            SECRET_KEY.encode(),
            string_to_sign.encode(),
            hashlib.sha256
        ).digest()
    ).decode()

    headers = {
        "Authorization": f"Bearer {ACCESS_KEY}:{signature}",
        "X-Timestamp": timestamp,
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": SIMPLE_PROMPT,
        "duration": 5
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.post(ENDPOINT, json=payload, headers=headers)
            print(f"HTTP {resp.status_code}")
            if resp.status_code < 300:
                print("✅ 成功！")
                print(resp.json())
            else:
                print(f"❌ 失敗: {resp.text[:200]}")
        except Exception as e:
            print(f"❌ 異常: {str(e)}")


async def test_auth_method_5():
    """方法 5: Basic Auth"""
    print("\n" + "="*60)
    print("測試方法 5: Basic Auth (Access Key:Secret Key)")
    print("="*60)

    credentials = base64.b64encode(f"{ACCESS_KEY}:{SECRET_KEY}".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": SIMPLE_PROMPT,
        "duration": 5
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.post(ENDPOINT, json=payload, headers=headers)
            print(f"HTTP {resp.status_code}")
            if resp.status_code < 300:
                print("✅ 成功！")
                print(resp.json())
            else:
                print(f"❌ 失敗: {resp.text[:200]}")
        except Exception as e:
            print(f"❌ 異常: {str(e)}")


async def test_auth_method_6():
    """方法 6: 自定義 Header"""
    print("\n" + "="*60)
    print("測試方法 6: 自定義 Header (X-Access-Key / X-Secret-Key)")
    print("="*60)

    headers = {
        "X-Access-Key": ACCESS_KEY,
        "X-Secret-Key": SECRET_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": SIMPLE_PROMPT,
        "duration": 5
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.post(ENDPOINT, json=payload, headers=headers)
            print(f"HTTP {resp.status_code}")
            if resp.status_code < 300:
                print("✅ 成功！")
                print(resp.json())
            else:
                print(f"❌ 失敗: {resp.text[:200]}")
        except Exception as e:
            print(f"❌ 異常: {str(e)}")


async def main():
    print("🔐 Kling API 認證方式測試")
    print("="*60)
    print("將嘗試 6 種不同的認證方式...\n")

    await test_auth_method_1()
    await test_auth_method_2()
    await test_auth_method_3()
    await test_auth_method_4()
    await test_auth_method_5()
    await test_auth_method_6()

    print("\n" + "="*60)
    print("✅ 測試完成")
    print("="*60)
    print("\n請查看上方結果，找到顯示 ✅ 成功的方法")
    print("如果找到成功的方法，告訴我方法編號，我會更新主腳本")


if __name__ == "__main__":
    asyncio.run(main())
