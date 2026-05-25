# add_reading_note.py
"""Utility to process a raw reading note and generate a daily summary.

Usage (from command line)::
    python add_reading_note.py "<raw note text>" [--date YYYY-MM-DD]

The script:
1. Determines the note date (default = today).
2. Saves the raw note under `notes/` for reference.
3. Performs a very lightweight importance check (keywords).
4. Renders a summary markdown file using the daily template.
5. If important, adds a placeholder Mermaid block that the user can later edit.
"""
import sys, os, datetime, argparse, re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]  # antigravity2.0讀書計劃
TEMPLATE_PATH = BASE_DIR / "templates" / "daily_summary_template.md"
NOTES_DIR = BASE_DIR / "notes"
SUMMARY_DIR = BASE_DIR / "summary"

def load_template():
    return TEMPLATE_PATH.read_text(encoding="utf-8")

def is_important(text: str) -> bool:
    # Simple heuristic: contains any of the target keywords
    keywords = ["核心概念", "關鍵人物", "關係圖", "重要", "關鍵", "概念"]
    return any(k in text for k in keywords)

def main():
    parser = argparse.ArgumentParser(description="Add a reading note and generate summary")
    parser.add_argument("note", help="Raw note text (can contain newlines if quoted)")
    parser.add_argument("--date", help="Date for the note (YYYY-MM-DD)", default=datetime.date.today().isoformat())
    args = parser.parse_args()

    date_str = args.date
    note_text = args.note.strip()

    # Ensure directories exist
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    # Save raw note
    raw_path = NOTES_DIR / f"{date_str}.md"
    raw_path.write_text(note_text, encoding="utf-8")

    # Generate summary markdown
    tmpl = load_template()
    summary = tmpl.replace("{{date}}", date_str)
    # Insert note content into a placeholder section
    summary = summary.replace("*簡要說明本次閱讀的章節或段落*.", note_text[:200] + ("..." if len(note_text) > 200 else ""))

    # Add Mermaid placeholder if important
    if is_important(note_text):
        mermaid_placeholder = "```mermaid\nflowchart LR\n    A[重要概念] --> B[關鍵人物]\n```"
        summary = summary.replace("```mermaid\n%% Mermaid diagram will be auto‑generated if deemed important\n```", mermaid_placeholder)
    else:
        # Keep empty block
        summary = summary.replace("```mermaid\n%% Mermaid diagram will be auto‑generated if deemed important\n```", "```mermaid\n```")

    summary_path = SUMMARY_DIR / f"{date_str}.md"
    summary_path.write_text(summary, encoding="utf-8")
    print(f"✅ Note saved to {raw_path}\n✅ Summary generated at {summary_path}")

if __name__ == "__main__":
    main()
