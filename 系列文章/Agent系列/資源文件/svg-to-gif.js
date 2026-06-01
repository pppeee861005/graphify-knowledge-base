const https = require('https');
const fs = require('fs');
const path = require('path');

// 使用 CloudConvert API 或者本地 HTML canvas 方案
// 因為 puppeteer 有依賴問題，我們用 HTML5 Canvas + Node 原生方案

const { execSync } = require('child_process');

// 首先檢查是否有 ImageMagick 或 FFmpeg
function checkTools() {
  try {
    execSync('convert --version', { stdio: 'pipe' });
    return 'imagemagick';
  } catch (e) {
    try {
      execSync('ffmpeg -version', { stdio: 'pipe' });
      return 'ffmpeg';
    } catch (e2) {
      return null;
    }
  }
}

const tool = checkTools();

if (tool === 'imagemagick') {
  console.log('使用 ImageMagick 轉換...');

  // 使用 ImageMagick 將 SVG 轉為 GIF
  // 需要先用 rsvg-convert 或 inkscape 轉為 PNG

  try {
    // 方案：轉換 SVG 為 PNG 序列，然後合成 GIF
    execSync('convert -density 150 "D:\\數位資產\\graphify個人知識庫\\系列文章\\Agent系列\\pipeline_animation.svg" -delay 5 -loop 0 "D:\\數位資產\\graphify個人知識庫\\系列文章\\Agent系列\\pipeline_workflow_diagram.gif"');
    console.log('✅ GIF 已生成: pipeline_workflow_diagram.gif');
  } catch (e) {
    console.error('轉換失敗:', e.message);
  }
} else if (tool === 'ffmpeg') {
  console.log('使用 FFmpeg 轉換...');
  console.log('⚠️ 需要先生成 PNG 序列');
} else {
  console.log('❌ 未找到轉換工具 (ImageMagick 或 FFmpeg)');
  console.log('推薦安裝: choco install imagemagick 或 choco install ffmpeg');
}
