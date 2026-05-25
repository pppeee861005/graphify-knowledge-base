#!/usr/bin/env python
"""
Generate relationship graph HTML for given nodes and edges.
"""
from pathlib import Path
from datetime import datetime

# Define nodes: label -> country
nodes = {
    "迪斯雷利首相 / 羅斯伯里首相 / 邱吉爾首相": "英國",
    "羅斯柴爾德": "英國",
    "厄蘭路": "法國",
}

# Define edges as (source, target, relationship)
edges = [
    ("羅斯柴爾德", "迪斯雷利首相 / 羅斯伯里首相 / 邱吉爾首相", "扶持"),
    ("厄蘭路", "羅斯柴爾德", "背判的門徒"),
]

def safe_id(name: str) -> str:
    """Convert a node name to a Mermaid‑compatible identifier."""
    return name.replace(" ", "_").replace("/", "_")

# Build Mermaid script
mermaid_lines = ["flowchart LR"]
for label, country in nodes.items():
    mermaid_lines.append(f'    {safe_id(label)}["{label}\\n({country})"]')
for src, dst, rel in edges:
    mermaid_lines.append(f'    {safe_id(src)} -- {rel} --> {safe_id(dst)}')
mermaid_code = "\n".join(mermaid_lines)

# HTML template (dark theme)
html_content = f"""<!DOCTYPE html>
<html lang=\"zh-TW\">
<head>
<meta charset=\"UTF-8\">
<title>人脈關係圖</title>
<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/normalize.css@8.0.1/normalize.min.css\">
<script src=\"https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js\"></script>
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
    <p style="margin-top:1rem; font-size:0.9rem;">產生時間：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
</div>
</body>
</html>
"""

# Write to HTML file in the same directory
out_path = Path(__file__).with_name("relationship_graph.html")
out_path.write_text(html_content, encoding="utf-8")
print(f"✅ 圖表已寫入: {out_path}")
