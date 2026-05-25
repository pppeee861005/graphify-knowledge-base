# build.py
"""Static site generator for Antigravity 2.0 reading plan.

- Reads markdown in `summary/`.
- Converts to HTML with `markdown2`.
- Processes Mermaid code blocks into `<div class="mermaid">`.
- Generates `web/index.html` with TOC and content sections.
- Uses dark theme and Mermaid CDN.
"""

import re
from pathlib import Path
import markdown2

# Base directories
BASE_DIR = Path(__file__).resolve().parents[1]
SUMMARY_DIR = BASE_DIR / "summary"
WEB_DIR = BASE_DIR / "web"
KNOWLEDGE_DIR = WEB_DIR / "knowledge"
TEMPLATE_INDEX = WEB_DIR / "index_template.html"
INDEX_HTML = WEB_DIR / "index.html"

def ensure_dirs():
    """Create output directories if they do not exist."""
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    WEB_DIR.mkdir(parents=True, exist_ok=True)

def load_template():
    """Load a custom HTML template or fall back to a minimal one."""
    if TEMPLATE_INDEX.exists():
        return TEMPLATE_INDEX.read_text(encoding="utf-8")
    return """
<!DOCTYPE html>
<html lang=\"zh-TW\">
<head>
<meta charset=\"UTF-8\">
<title>Antigravity 2.0 讀書計劃</title>
<link rel=\"stylesheet\" href=\"styles.css\">
<script src=\"https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js\"></script>
<script>mermaid.initialize({startOnLoad:true, theme:'dark', securityLevel:'loose'});</script>
</head>
<body>
<h1>Antigravity 2.0 讀書計劃 – 心得匯總</h1>
<nav id=\"toc\"></nav>
<main id=\"content\"></main>
</body>
</html>
"""

def _process_mermaid(html_content: str) -> str:
    """Convert Mermaid fenced code blocks into <div class='mermaid'> blocks.
    Handles both explicit language‑mermaid fences and generic fences that start
    with a Mermaid keyword (flowchart, sequenceDiagram, graph, etc.).
    """
    def replace_match(m):
        inner = m.group(1)
        if re.search(r"\b(flowchart|sequenceDiagram|graph|stateDiagram|classDiagram)\b", inner, flags=re.IGNORECASE):
            return f"<div class=\"mermaid\">{inner}</div>"
        return m.group(0)
    return re.sub(r"<pre><code>(.*?)</code></pre>", replace_match, html_content, flags=re.DOTALL)

def generate_content():
    """Create TOC items and HTML body sections from markdown summaries."""
    entries = sorted(SUMMARY_DIR.glob("*.md"), reverse=True)
    toc_items = []
    body_html = []
    for md_path in entries:
        date_str = md_path.stem
        title = f"{date_str} 心得"
        toc_items.append(f'<li><a href="#{{date_str}}">{title}</a></li>')
        md_text = md_path.read_text(encoding="utf-8")
        html = markdown2.markdown(md_text, extras=["fenced-code-blocks", "code-friendly", "tables"])
        html = _process_mermaid(html)
        body_html.append(f'<section id="{date_str}"><h2>{title}</h2>{html}</section>')
    return "\n".join(toc_items), "\n".join(body_html)

def build_site():
    """Generate the static site HTML file."""
    ensure_dirs()
    toc, body = generate_content()
    template = load_template()
    # Insert TOC
    if "<nav id=\"toc\"></nav>" in template:
        template = template.replace("<nav id=\"toc\"></nav>", f'<nav id=\"toc\"><ul>{toc}</ul></nav>')
    else:
        template = template.replace("</head>", f"<style>/* placeholder */</style></head>")
    # Insert content
    if "<main id=\"content\"></main>" in template:
        template = template.replace("<main id=\"content\"></main>", f'<main id=\"content\">{body}</main>')
    else:
        template += body
    INDEX_HTML.write_text(template, encoding="utf-8")
    print(f"✅ Site generated: {INDEX_HTML}")

if __name__ == "__main__":
    build_site()
