const BROWSER_CLIENT = 'C:/Users/Administrator/.codex/plugins/cache/openai-bundled/browser/26.803.41515/scripts/browser-client.mjs';
const DEFAULT_PUBLICATION = 'https://aiagentcommander.substack.com';

function escapeRegex(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function normalized(value) {
  return (value ?? '').replace(/\s+/g, ' ').trim();
}

export async function connectToSubstack(options = {}) {
  if (options.browser && options.tab) return { browser: options.browser, tab: options.tab };
  const { setupBrowserRuntime } = await import(BROWSER_CLIENT);
  const agent = globalThis.agent ?? await setupBrowserRuntime();
  const browser = options.browser ?? globalThis.browser ?? globalThis.iab ?? await agent.browsers.getForUrl(DEFAULT_PUBLICATION);
  await browser.nameSession('📝 Substack Publisher');
  if (globalThis.substackTab) return { browser, tab: globalThis.substackTab };
  const tabs = await browser.user.openTabs();
  const tabInfo = tabs.find((tab) => (tab.url ?? '').includes('substack.com'));
  if (!tabInfo) throw new Error('找不到已開啟的 Substack 分頁，請先登入並保持分頁開啟。');
  const tab = await browser.user.claimTab(tabInfo);
  return { browser, tab };
}

export async function createDraft(article, options = {}) {
  const { browser, tab } = await connectToSubstack(options);
  const publication = options.publication ?? DEFAULT_PUBLICATION;
  await tab.goto(`${publication}/publish/posts/drafts`);
  await tab.playwright.waitForTimeout(1200);
  const existing = tab.playwright.getByRole('link', { name: new RegExp(`^${escapeRegex(article.title)}(?:\\s|$)`) });
  if (await existing.count() > 0) {
    await browser.tabs.finalize({ keep: [{ tab, status: 'handoff' }] });
    throw new Error(`偵測到相同標題的既有草稿：「${article.title}」。工具已停止，未建立新草稿。`);
  }
  await tab.goto(`${publication}/publish/post?type=newsletter`);
  await tab.playwright.waitForTimeout(1200);

  const title = tab.playwright.getByRole('textbox', { name: 'title', exact: true });
  const subtitle = tab.playwright.getByPlaceholder('Add a subtitle…', { exact: true });
  const editor = tab.playwright.getByTestId('editor');

  await title.fill(article.title);
  await subtitle.fill(article.subtitle);
  await editor.waitFor({ state: 'visible', timeoutMs: 12000 });
  await editor.click({ timeoutMs: 12000 });
  await tab.clipboard.write([{
    entries: [
      { mimeType: 'text/html', text: article.html },
      { mimeType: 'text/plain', text: article.plainText }
    ]
  }]);
  await editor.press('Control+V');
  await tab.playwright.waitForTimeout(1600);

  const saved = tab.playwright.getByRole('button', { name: 'Saved', exact: true });
  if (await saved.count() !== 1) throw new Error('文章已填入，但未確認 Substack 的 Saved 狀態。');
  const url = await tab.url();
  if (!url?.match(/\/publish\/post\/\d+/)) throw new Error(`未取得穩定草稿網址：${url ?? '未知'}`);

  const verification = await tab.playwright.evaluate(() => {
    const titleElement = document.querySelector('[data-testid="post-title"]');
    const subtitleElement = document.querySelector('textarea[placeholder="Add a subtitle…"]');
    const editorElement = document.querySelector('[data-testid="editor"]');
    const body = editorElement?.innerText ?? '';
    return {
      title: titleElement?.value ?? titleElement?.innerText ?? '',
      subtitle: subtitleElement?.value ?? subtitleElement?.innerText ?? '',
      bodyCharacters: body.length,
      bodyStart: body.slice(0, 100),
      bodyEnd: body.slice(-140),
      h2: editorElement?.querySelectorAll('h2').length ?? 0,
      h3: editorElement?.querySelectorAll('h3').length ?? 0,
      blockquotes: editorElement?.querySelectorAll('blockquote').length ?? 0,
      horizontalRules: editorElement?.querySelectorAll('hr').length ?? 0,
      lists: editorElement?.querySelectorAll('ul, ol').length ?? 0
    };
  });
  const expectedStart = normalized(article.renderedText).slice(0, 60);
  const expectedEnd = normalized(article.renderedText).slice(-80);
  if (normalized(verification.title) !== normalized(article.title)) throw new Error('草稿標題驗證失敗。');
  if (normalized(verification.subtitle) !== normalized(article.subtitle)) throw new Error('草稿副標題驗證失敗。');
  if (!normalized(verification.bodyStart).startsWith(expectedStart.slice(0, 30))) throw new Error('草稿正文開頭驗證失敗。');
  if (!normalized(verification.bodyEnd).endsWith(expectedEnd.slice(-40))) throw new Error('草稿正文結尾驗證失敗。');

  await browser.tabs.finalize({ keep: [{ tab, status: 'deliverable' }] });
  return { url, title: article.title, saved: true, verification };
}

export async function verifyDraft(url, options = {}) {
  const { browser, tab } = await connectToSubstack(options);
  await tab.goto(url);
  await tab.playwright.waitForTimeout(1000);
  const title = tab.playwright.getByRole('textbox', { name: 'title', exact: true });
  const subtitle = tab.playwright.getByPlaceholder('Add a subtitle…', { exact: true });
  const editor = tab.playwright.getByTestId('editor');
  const saved = tab.playwright.getByRole('button', { name: 'Saved', exact: true });
  const result = await tab.playwright.evaluate(() => {
    const titleElement = document.querySelector('[data-testid="post-title"]');
    const subtitleElement = document.querySelector('textarea[placeholder="Add a subtitle…"]');
    const editorElement = document.querySelector('[data-testid="editor"]');
    const body = editorElement?.innerText ?? '';
    return {
      title: titleElement?.value ?? titleElement?.innerText ?? '',
      subtitle: subtitleElement?.value ?? subtitleElement?.innerText ?? '',
      bodyCharacters: body.length,
      bodyStart: body.slice(0, 100),
      bodyEnd: body.slice(-140),
      h2: editorElement?.querySelectorAll('h2').length ?? 0,
      h3: editorElement?.querySelectorAll('h3').length ?? 0,
      blockquotes: editorElement?.querySelectorAll('blockquote').length ?? 0,
      horizontalRules: editorElement?.querySelectorAll('hr').length ?? 0,
      lists: editorElement?.querySelectorAll('ul, ol').length ?? 0
    };
  });
  result.url = await tab.url();
  result.saved = await saved.count() === 1;
  await browser.tabs.finalize({ keep: [{ tab, status: 'deliverable' }] });
  return result;
}
