# ママへの思い

ミュージックビデオ「ママへの思い」を見るための、スマホのホーム画面に置けるアプリです。

- 公開先：https://roguepink.github.io/mamaenoomoi/
- 使い方：開く → 大きな「▶ みる」を押す → 画面いっぱいで流れる → 終わると最初の画面に戻る
- 再生中は画面の下に4つのボタン：「巻戻し」「一時停止／再生」「早送り」「もどる（最初の画面へ）」
  - 巻戻し・早送りは、1回押すと10秒ずつ。押し続けるとその間ずっと速く動く
  - スマホの「全画面表示」は使わず、アプリの画面いっぱいで流す（iPhone は下のボタンが隠れ、Android は「全画面表示を終了するには…」のお知らせが出て邪魔なため）
- 検索エンジンには出ません。ただし URL を知っている人は誰でも見られます。

## ホーム画面への追加

- **iPhone**：Safari で開く → 下の共有ボタン（□に↑）→「ホーム画面に追加」→ 右上の「追加」
- **Android**：Chrome で開く → 右上の ︙ →「ホーム画面に追加」または「アプリをインストール」

ブラウザで開いたときだけ、画面の下にこの案内が出ます（「とじる」を押すと二度と出ません）。

## 曲を足す（2曲目・3曲目）

1. 動画を配信用に作り直して `assets/video/` に置く（下の「動画の下ごしらえ」）。例：`assets/video/02.mp4`
2. 表紙の画像を `assets/covers/` に置く。例：`assets/covers/02.jpg`（縦長の写真がおすすめ）
3. `src/app.html` の上のほうにある `SONGS` に1行足す：

   ```js
   const SONGS = [
     { title: "ママへの思い", video: "assets/video/01.mp4", cover: "assets/covers/01.jpg" },
     { title: "新しい曲の名前", video: "assets/video/02.mp4", cover: "assets/covers/02.jpg" },
   ];
   ```

4. `python3 tools/build.py` を実行して、コミットして push する（数分で公開先に反映されます）。

曲が2つ以上になると、最初の画面は自動で「表紙＋大きな曲カードの縦並び」に変わります。

## 表紙を差し替える

1. 新しい画像を `assets/covers/01.jpg` に上書きする（JPEG）。
   表紙は画面の上に幅いっぱいで出て、下の足りない部分は同じ画像をぼかして埋めます。
   顔は画像の上のほう（上から 1/3 くらいまで）にあると、曲名やボタンに隠れません。
2. アイコン用に正方形の画像を `assets/covers/01-icon.jpg` として置く（無ければ表紙の真ん中を切ります）
3. アイコンとリンク用サムネイルを作り直す：
   `COVER_Y=15% NODE_PATH=$(npm root -g) node tools/make-assets.js`
   （`COVER_Y` はリンク用サムネイルの切り抜き位置。顔が上のほうなら小さい数字に）
4. `python3 tools/build.py` → コミット → push

## 動画の下ごしらえ

GitHub は1ファイル 100MB までなので、配信用に作り直します（Git LFS は使わない）。

```
ffmpeg -i 元.mp4 -vf "scale='if(gt(iw,ih),1280,-2)':'if(gt(iw,ih),-2,1280)'" \
  -c:v libx264 -preset slow -crf 23 -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 160k -movflags +faststart assets/video/01.mp4
```

- `-movflags +faststart` は必ず付ける（無いとスマホで再生開始まで長く待たされる）
- 90MB を超えたら `-crf` を 2 ずつ上げて作り直す（目安 30〜60MB）

## ファイルの役目

| ファイル | 役目 |
| --- | --- |
| `src/app.html` | 本体（画面・見た目・動き・曲の一覧）。直すのはここ |
| `tools/build.py` | `src/app.html` から `index.html` と `sw.js` を作る（この2つは直接直さない） |
| `src/sw.js` | 画面と画像を保存しておく係の元。動画には一切さわらない |
| `tools/card.html`, `tools/make-assets.js` | 表紙からアイコン（180/192/512・maskable）と `og.jpg` を書き出す |
| `manifest.webmanifest` | ホーム画面に置いたときの名前・アイコン・全画面表示の設定 |
| `.github/workflows/deploy.yml` | push のたびに GitHub Pages へ自動公開 |
