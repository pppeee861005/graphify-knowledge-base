function escapeHtml(value) {
  return value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}

function inlineHtml(value) {
  const parts = value.split('**');
  return parts.map((part, index) => index % 2 ? `<strong>${escapeHtml(part)}</strong>` : escapeHtml(part)).join('');
}

export function parseMarkdown(source, options = {}) {
  const normalized = source.replaceAll('\\n', '\n').replaceAll('\\r', '');
  const firstFence = normalized.indexOf('---');
  const secondFence = normalized.indexOf('---', firstFence + 3);
  const content = secondFence >= 0 ? normalized.slice(secondFence + 3) : normalized;
  const lines = content.split('\n');
  const titleIndex = lines.findIndex((line) => line.trim().startsWith('# '));
  const subtitleIndex = lines.findIndex((line, index) => index > titleIndex && line.trim().startsWith('## '));
  const title = titleIndex >= 0 ? lines[titleIndex].trim().slice(2).trim() : (options.fallbackTitle ?? '').trim();
  if (!title) throw new Error('找不到文章主標題，且未提供檔名作為備用標題。');
  const subtitle = subtitleIndex >= 0 ? lines[subtitleIndex].trim().slice(3).trim() : '';
  const bodyStartIndex = subtitleIndex >= 0 ? subtitleIndex + 1 : titleIndex >= 0 ? titleIndex + 1 : 0;
  let bodyLines = lines.slice(bodyStartIndex);
  const privateNotesIndex = bodyLines.findIndex((line) => /^##\s+草稿討論區（不屬於正文）\s*$/.test(line.trim()));
  if (privateNotesIndex >= 0) bodyLines = bodyLines.slice(0, privateNotesIndex);
  bodyLines = bodyLines.filter((line) => !/^\*\*《.+》#\d+／\d+\*\*$/.test(line.trim()));
  const html = [];
  let index = 0;
  while (index < bodyLines.length) {
    const line = bodyLines[index];
    if (!line.trim()) { index += 1; continue; }
    if (line.startsWith('### ')) { html.push(`<h3>${inlineHtml(line.slice(4))}</h3>`); index += 1; continue; }
    if (line.startsWith('## ')) { html.push(`<h2>${inlineHtml(line.slice(3))}</h2>`); index += 1; continue; }
    if (line.trim() === '---') { html.push('<hr>'); index += 1; continue; }
    if (/^[-*] /.test(line)) {
      const items = [];
      while (index < bodyLines.length && /^[-*] /.test(bodyLines[index])) {
        items.push(`<li>${inlineHtml(bodyLines[index].slice(2))}</li>`);
        index += 1;
      }
      html.push(`<ul>${items.join('')}</ul>`);
      continue;
    }
    if (/^\d+\. /.test(line)) {
      const items = [];
      while (index < bodyLines.length && /^\d+\. /.test(bodyLines[index])) {
        items.push(`<li>${inlineHtml(bodyLines[index].replace(/^\d+\. /, ''))}</li>`);
        index += 1;
      }
      html.push(`<ol>${items.join('')}</ol>`);
      continue;
    }
    if (line.startsWith('>')) {
      const quote = [];
      while (index < bodyLines.length && bodyLines[index].startsWith('>')) {
        quote.push(inlineHtml(bodyLines[index].replace(/^>\s?/, '')));
        index += 1;
      }
      html.push(`<blockquote><p>${quote.join('<br>')}</p></blockquote>`);
      continue;
    }
    html.push(`<p>${inlineHtml(line)}</p>`);
    index += 1;
  }
  const plainText = bodyLines.join('\n').trim();
  const renderedText = plainText.replaceAll('**', '').replace(/^#{2,3}\s+/gm, '').replace(/^>\s?/gm, '').replace(/^[-*]\s+/gm, '').replace(/^\d+\.\s+/gm, '').replace(/^---\s*$/gm, '');
  return {
    title,
    subtitle,
    html: html.join(''),
    plainText,
    renderedText,
    expected: {
      h2: bodyLines.filter((line) => line.startsWith('## ')).length,
      h3: bodyLines.filter((line) => line.startsWith('### ')).length,
      blockquotes: bodyLines.some((line) => line.startsWith('>')) ? 1 : 0,
      horizontalRules: bodyLines.filter((line) => line.trim() === '---').length,
      lists: bodyLines.some((line) => /^[-*] /.test(line)) || bodyLines.some((line) => /^\d+\. /.test(line)) ? 1 : 0
    }
  };
}
