# network_graph_builder.py
"""
Antigravity 2.0 讀書計畫 – 人脈關係圖產生工具（自動模式）
=====================================================================

根據使用者提供的節點與關係直接產生 `relationship_graph.html`，不再需要
交互式輸入，方便一次性產出固定圖表。

使用方式（Windows PowerShell / CMD）：
    python network_graph_builder.py

產生的 HTML 會放在同目錄下，直接雙擊或 `start` 指令即可在瀏覽器中檢視。
"""

import os
from datetime import datetime

# ------------------------------------------------------------
# 1. 預設資料 – 節點與關係
# ------------------------------------------------------------
# 節點字典：顯示名稱 -> 國家
nodes = {
    "迪斯雷利首相 / 羅斯伯里首相 / 邱吉爾首相": "英國",
    "羅斯柴爾德": "英國",
    "厄蘭路": "法國",
}

# 邊列表 (起點, 終點, 關係文字)
edges = [
    ("羅斯柴爾德", "迪斯雷利首相 / 羅斯伯里首相 / 邱吉爾首相", "扶持"),
    ("厄蘭路", "羅斯柴爾德", "背判的門徒"),
]

# ------------------------------------------------------------
# 2. Mermaid HTML 模板（暗色主題）
# ------------------------------------------------------------

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<title>人脈關係圖</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/normalize.css@8.0.1/normalize.min.css">
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
    mermaid.initialize({{startOnLoad:true, theme:'dark'}});
</script>
<style>
    body {{ background:#121212; color:#e0e0e0; font-family:Arial,Helvetica,sans-serif; padding:2rem; }}
    .container {{ max-width:900px; margin:auto; }}
    h1 {{ text-align:center; margin-bottom:1rem; }}
</style>
</head>
<body>
<div class="container">
    <h1>人脈關係圖</h1>
    <div class="mermaid">
{mermaid_code}
    </div>
    <p style="margin-top:1rem; font-size:0.9rem;">
        產生時間：{timestamp}
    </p>
</div>
</body>
</html>
"""

# ------------------------------------------------------------
# 3. Mermaid 產生函式
# ------------------------------------------------------------
def build_mermaid(nodes_dict, edges_list):
    """根據節點與邊產生 Mermaid 流程圖語法。"""
    lines = ["flowchart LR"]
    # 節點宣告（使用安全的 ID）
    for label, country in nodes_dict.items():
        node_id = label.replace(" ", "_").replace("/", "_")
        lines.append(f'    {node_id}["{label}\\n({country})"]')
    # 連線
    for src, dst, rel in edges_list:
        src_id = src.replace(" ", "_").replace("/", "_")
        dst_id = dst.replace(" ", "_").replace("/", "_")
        lines.append(f'    {src_id} -- {rel} --> {dst_id}')
    return "\n".join(lines)

# ------------------------------------------------------------
# 4. 主程式 – 直接產出圖表
# ------------------------------------------------------------
if __name__ == "__main__":
    print("\n=== Antigravity 2.0 – 人脈關係圖產生器（自動模式） ===\n")
    mermaid_code = build_mermaid(nodes, edges)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content = HTML_TEMPLATE.format(mermaid_code=mermaid_code, timestamp=timestamp)
    out_path = os.path.join(os.path.dirname(__file__), "relationship_graph.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ 圖表已產生於：{out_path}")
    print("可直接雙擊開啟或使用 `start`/`open` 指令在瀏覽器中檢視。")
