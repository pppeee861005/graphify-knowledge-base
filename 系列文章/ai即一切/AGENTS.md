# Repository Guidelines

## Project Structure

This repository is a Markdown-first writing project for the eight-part “AI 即一切” Substack series. Drafts, planning notes, and production guidance live at the repository root; `系列文章plan.MD` is the canonical series plan and `草稿.md` is the source-material archive. Keep visual assets in `配圖/`. The `substack-publisher/` directory contains the Node.js publishing helper, its Markdown conversion code, browser adapter, publishing records, and a sample article. There is currently no dedicated test suite.

## Build, Test, and Development Commands

Run publisher commands from `substack-publisher/`:

```powershell
npm install                 # Install the publisher's dependencies
node substack-cli.mjs      # Show the publisher CLI usage
```

Use the project’s configured publishing workflow only after reviewing the target article and account state. For content-only changes, no build step is required; inspect Markdown locally and verify links, headings, images, and series navigation before publishing.

## Content Style and Naming

Write Traditional Chinese unless a quoted or technical term requires another language. Use Markdown headings, short mobile-friendly paragraphs, and descriptive filenames. Series drafts should follow the established pattern, for example `AI即一切_S01E01_主標題.md`; supporting notes may retain the repository’s existing Chinese names. Keep one core question per article, distinguish verified capabilities from future speculation, and mark human review, authorization, and responsibility boundaries for high-risk examples.

## Testing and Review

There is no automated test framework. For publisher changes, run the CLI smoke check and manually verify Markdown conversion against `substack-publisher/test-article.md`. For articles, perform a pre-publication review covering source links, image paths, word count, mobile readability, previous/next navigation, and removal of placeholders or internal notes.

## Commits and Pull Requests

Use concise, action-oriented commit subjects consistent with the repository’s Chinese workflow, such as `新增 第四篇實證稿` or `更新系列發布計劃`. Keep commits focused. Pull requests should summarize the changed articles or tooling, identify evidence and external links added, describe publishing-impacting changes, and include screenshots or rendered examples when layout or images changed.

## Safety and Configuration

Do not commit credentials, session data, or private publishing records. Treat `.substack-publisher-records.json` and browser automation configuration as sensitive. Before any live publishing action, confirm the article, destination, images, and final rendered content.
