// アイコン（180/192/512・maskable）とリンク用サムネイルを、表紙の画像から書き出す
// 使い方: NODE_PATH=$(npm root -g) node tools/make-assets.js
//   表紙は src/app.html の APP.cover（なければ1曲目の表紙）を使う。
//   顔が上のほうにある表紙なら、 COVER_Y=35% のように縦位置を変えられる。
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const root = path.resolve(__dirname, '..');
  const app = fs.readFileSync(path.join(root, 'src/app.html'), 'utf8');
  const cover = (app.match(/cover:\s*"([^"]+)"/) || [])[1];
  const y = process.env.COVER_Y || '50%';
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1300, height: 1800 } });
  await p.goto('file://' + path.join(__dirname, 'card.html') + '?cover=' + encodeURIComponent('../' + cover) + '&y=' + encodeURIComponent(y));
  await p.evaluate(() => Promise.all([...document.images].map(i => i.decode())));
  for (const size of [512, 192, 180]) {
    await p.evaluate(s => { const i = document.querySelector('#icon'); i.style.width = i.style.height = s + 'px'; }, size);
    await (await p.$('#icon')).screenshot({ path: path.join(root, `assets/icon-${size}.png`) });
  }
  await (await p.$('#mask')).screenshot({ path: path.join(root, 'assets/icon-512-maskable.png') });
  await (await p.$('#og')).screenshot({ path: path.join(root, 'assets/og.jpg'), type: 'jpeg', quality: 85 });
  await b.close();
  console.log('書き出しました（表紙:', cover + '）');
})();
