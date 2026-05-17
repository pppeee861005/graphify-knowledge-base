#!/usr/bin/env python3
"""
測試 JWT 是否有效
直接調用 Kling API 驗證認證
"""

import os
import asyncio
import json
import time
import jwt
import httpx
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv("KLING_ACCESS_KEY") or "An98f9gCT9er3hAbfeyByPbaEYdTgyt9"
SECRET_KEY = os.getenv("KLING_SECRET_KEY") or "MGL4AYfYgDFKTYGJpyfm4ftnbkFmtADN"

print("=" * 80)
print("🔐 JWT 有效性測試")
print("=" * 80)
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


async def test_jwt_with_api():
    """用 JWT 調用實際的 Kling API"""

    token = make_kling_token(ACCESS_KEY, SECRET_KEY)

    print("📝 生成的 JWT:")
    print(f"   {token}")
    print()
    print(f"   長度: {len(token)} 字元")
    print()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 嘗試一個簡單的視頻生成請求
    payload = {
        "prompt": "A beautiful sunset over ocean",
        "duration": 5,
        "aspect_ratio": "16:9"
    }

    endpoint = "https://api.klingai.com/v1/videos/text2video"

    print(f"🌐 發送請求到: {endpoint}")
    print()
    print("📋 請求信息:")
    print(f"   Method: POST")
    print(f"   Headers:")
    print(f"      Authorization: Bearer {token[:30]}...{token[-10:]}")
    print(f"      Content-Type: application/json")
    print(f"   Body:")
    print(f"      {json.dumps(payload, indent=8)}")
    print()

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(endpoint, json=payload, headers=headers)

            print("=" * 80)
            print("📊 API 響應")
            print("=" * 80)
            print()
            print(f"HTTP Status Code: {response.status_code}")
            print()

            # 根據狀態碼判斷
            if response.status_code == 200:
                print("✅ JWT 認證成功！")
                print()
                result = response.json()
                print("響應內容：")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return True

            elif response.status_code == 401:
                print("❌ JWT 認證失敗！")
                print("   原因: Unauthorized (401)")
                result = response.json()
                print(f"   錯誤: {result.get('message', '未知錯誤')}")
                return False

            elif response.status_code == 429:
                print("⚠️  JWT 認證成功，但額度不足")
                print("   ✓ JWT 本身是有效的")
                print("   ✗ 但賬戶沒有足夠的額度")
                result = response.json()
                print()
                print("響應內容：")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return True  # JWT 有效，只是額度問題

            elif response.status_code == 400:
                print("⚠️  JWT 認證成功，但請求參數錯誤")
                print("   ✓ JWT 本身是有效的")
                print("   ✗ 但請求參數有問題")
                result = response.json()
                print()
                print("響應內容：")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return True  # JWT 有效，只是參數問題

            else:
                print(f"⚠️  未知狀態碼: {response.status_code}")
                result = response.json()
                print()
                print("響應內容：")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return None

    except Exception as e:
        print(f"❌ 網絡異常: {str(e)}")
        return False


async def test_jwt_structure():
    """驗證 JWT 結構是否正確"""

    print("=" * 80)
    print("🔍 JWT 結構驗證")
    print("=" * 80)
    print()

    token = make_kling_token(ACCESS_KEY, SECRET_KEY)

    # 驗證 JWT 格式
    parts = token.split('.')

    if len(parts) != 3:
        print(f"❌ JWT 格式錯誤！應該有 3 部分，實際有 {len(parts)} 部分")
        return False

    print(f"✅ JWT 有 3 個部分")
    print()

    # 驗證簽名
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(f"✅ JWT 簽名有效")
        print()
        print(f"✅ JWT Payload 解碼成功:")
        print(json.dumps(decoded, indent=2))
        print()

        # 檢查必需的字段
        required_fields = ["iss", "iat", "nbf", "exp"]
        missing_fields = [f for f in required_fields if f not in decoded]

        if missing_fields:
            print(f"❌ JWT 缺少字段: {missing_fields}")
            return False

        print(f"✅ JWT 包含所有必需字段: {required_fields}")
        print()

        # 檢查 Access Key
        if decoded["iss"] == ACCESS_KEY:
            print(f"✅ JWT 的 iss (issuer) 正確: {decoded['iss'][:8]}...{decoded['iss'][-8:]}")
        else:
            print(f"❌ JWT 的 iss 不匹配！")
            return False

        print()
        return True

    except jwt.InvalidSignatureError:
        print(f"❌ JWT 簽名無效！")
        print(f"   可能原因: Secret Key 不正確")
        return False
    except jwt.ExpiredSignatureError:
        print(f"❌ JWT 已過期！")
        return False
    except Exception as e:
        print(f"❌ JWT 解碼失敗: {str(e)}")
        return False


async def main():
    print("🎯 開始 JWT 驗證...\n")

    # 第一步: 驗證 JWT 結構
    print("Step 1: 驗證 JWT 結構")
    print("-" * 80)
    structure_valid = await test_jwt_structure()
    print()

    # 第二步: 用 JWT 調用 API
    print("Step 2: 用 JWT 調用 Kling API")
    print("-" * 80)
    api_valid = await test_jwt_with_api()
    print()

    # 總結
    print("=" * 80)
    print("📊 測試結果總結")
    print("=" * 80)
    print()

    if structure_valid and api_valid is True:
        print("✅✅ JWT 完全有效！可以使用")
        print()
        print("   ✓ JWT 結構正確")
        print("   ✓ JWT 簽名有效")
        print("   ✓ API 認證成功")
        print()
        print("   可能的下一步原因:")
        print("   1. 額度不足 (429)")
        print("   2. 新購買的資源包還未激活")

    elif structure_valid and api_valid is None:
        print("⚠️  JWT 結構有效，但 API 響應異常")
        print()
        print("   ✓ JWT 結構正確")
        print("   ✓ JWT 簽名有效")
        print("   ? API 響應未知")

    elif not structure_valid:
        print("❌ JWT 結構無效")
        print()
        print("   ✗ JWT 格式或簽名有問題")
        print("   檢查事項:")
        print("   1. SECRET_KEY 是否正確")
        print("   2. ACCESS_KEY 是否正確")

    else:
        print("❌ JWT 認證失敗")
        print()
        print("   檢查事項:")
        print("   1. JWT Token 是否被正確傳遞")
        print("   2. Authorization Header 格式是否正確")
        print("   3. API Key 是否仍有效")


if __name__ == "__main__":
    asyncio.run(main())
