#!/usr/bin/env python3
import time
import io
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 配置
svg_file = r"D:\數位資產\graphify個人知識庫\系列文章\Agent系列\pipeline_animation.svg"
output_gif = r"D:\數位資產\graphify個人知識庫\系列文章\Agent系列\pipeline_workflow_diagram.gif"

# 動畫參數
duration_seconds = 6  # SVG 動畫持續時間
fps = 20  # 每秒幀數
total_frames = duration_seconds * fps

print(f"🎬 開始轉換 SVG → GIF")
print(f"   總幀數: {total_frames}")
print(f"   每秒幀數: {fps}")
print(f"   動畫時長: {duration_seconds}s")

# 啟動 Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1200,400')

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

try:
    # 打開 SVG 文件
    driver.get(f'file:///{svg_file.replace(chr(92), "/")}')

    # 等待 SVG 加載
    time.sleep(1)

    # 捕捉幀
    frames = []
    print(f"\n📸 正在捕捉 {total_frames} 幀...")

    for frame_idx in range(total_frames):
        # 捕捉當前幀
        screenshot = driver.get_screenshot_as_png()
        img = Image.open(io.BytesIO(screenshot))

        # 裁剪到視口大小（移除多餘邊距）
        img = img.crop((0, 0, 1200, 400))
        frames.append(img)

        # 進度條
        if (frame_idx + 1) % 10 == 0:
            print(f"   {frame_idx + 1}/{total_frames} frames captured")

        # 控制幀率
        time.sleep(1.0 / fps)

    # 保存為 GIF
    print(f"\n💾 正在生成 GIF...")
    frames[0].save(
        output_gif,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),  # 毫秒
        loop=0,  # 無限循環
        optimize=False
    )

    # 獲取文件大小
    import os
    file_size = os.path.getsize(output_gif) / (1024 * 1024)  # MB

    print(f"\n✅ GIF 已生成!")
    print(f"   位置: {output_gif}")
    print(f"   大小: {file_size:.2f} MB")
    print(f"   幀數: {len(frames)}")
    print(f"   幀率: {fps} FPS")

finally:
    driver.quit()
    print("\n✨ 完成！")
