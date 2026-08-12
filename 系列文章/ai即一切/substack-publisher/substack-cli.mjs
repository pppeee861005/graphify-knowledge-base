#!/usr/bin/env node
import { readFile } from 'node:fs/promises';
import { basename, extname, resolve } from 'node:path';
import { parseMarkdown } from './markdown.mjs';
import { createDraft, verifyDraft } from './browser-adapter.mjs';
import { appendRecord } from './record.mjs';

function usage() {
  console.error('用法：node substack-cli.mjs draft <article.md> [--dry-run]');
  process.exitCode = 2;
}

const [, , command, inputPath, ...flags] = process.argv;
if (command === 'verify' && inputPath) console.log(JSON.stringify(await verifyDraft(inputPath), null, 2));
else if (command !== 'draft' || !inputPath) usage();
else {
  const absolutePath = resolve(inputPath);
  const source = await readFile(absolutePath, 'utf8');
  const article = parseMarkdown(source, { fallbackTitle: basename(absolutePath, extname(absolutePath)) });
  const result = {
    command: 'draft',
    status: flags.includes('--dry-run') ? 'validated' : 'browser-adapter-pending',
    source: absolutePath,
    title: article.title,
    subtitle: article.subtitle,
    bodyCharacters: article.plainText.length,
    htmlCharacters: article.html.length,
    externalSideEffect: false
  };
  if (flags.includes('--dry-run')) console.log(JSON.stringify(result, null, 2));
  else {
    const result = await createDraft(article);
    const recordPath = resolve('.substack-publisher-records.json');
    await appendRecord(recordPath, { ...result, source: absolutePath, createdAt: new Date().toISOString(), status: 'draft' });
    console.log(JSON.stringify(result, null, 2));
  }
}
