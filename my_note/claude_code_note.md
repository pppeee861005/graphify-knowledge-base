找到了！根據官方 Issue，v2.0.62 是最後一個使用 Node.js 的版本，在沒有 AVX 支援的 CPU 上能正常運行。2.1.x 之後改用 Bun 編譯，無法在非 AVX 環境運行。 GitHubGitHub
試試這個：
cmdnpm uninstall -g @anthropic-ai/claude-code
npm install -g @anthropic-ai/claude-code@2.0.62
然後測試：
cmdclaude --version

如果 2.0.62 還是不行，可能根本原因就是你的硬件（或虛擬機配置）沒有暴露 AVX 指令集。在這種情況下，Claude.ai 網頁版是最穩定的替代方案。