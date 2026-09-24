#!/usr/bin/env python3
"""src/app.html（本体）を、そのまま開ける index.html に包む。
   あわせて sw.js（画面と画像の保存係）も作る。
   index.html と sw.js は直接編集しないこと。"""
import hashlib, json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
# 公開先（リンクを送ったときのプレビュー画像の場所）。変わったらここを直す。
SITE = "https://roguepink.github.io/mamaenoomoi"
NAME = "ママへの思い"

body = (root / "src" / "app.html").read_text(encoding="utf-8")
head_part, main_part = body.split("<!-- ここから本文 -->", 1)
doc = (
    "<!doctype html>\n<html lang=\"ja\">\n<head>\n"
    "<meta charset=\"utf-8\">\n"
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
    "<meta name=\"robots\" content=\"noindex, nofollow\">\n"
    f"<meta name=\"description\" content=\"{NAME}\">\n"
    "<meta name=\"theme-color\" content=\"#111014\">\n"
    "<link rel=\"icon\" href=\"assets/icon-192.png\" sizes=\"192x192\">\n"
    "<link rel=\"apple-touch-icon\" href=\"assets/icon-180.png\">\n"
    "<link rel=\"manifest\" href=\"manifest.webmanifest\">\n"
    "<meta name=\"mobile-web-app-capable\" content=\"yes\">\n"
    "<meta name=\"apple-mobile-web-app-capable\" content=\"yes\">\n"
    "<meta name=\"apple-mobile-web-app-status-bar-style\" content=\"black-translucent\">\n"
    f"<meta name=\"apple-mobile-web-app-title\" content=\"{NAME}\">\n"
    f"<meta property=\"og:title\" content=\"{NAME}\">\n"
    "<meta property=\"og:type\" content=\"website\">\n"
    f"<meta property=\"og:url\" content=\"{SITE}/\">\n"
    f"<meta property=\"og:image\" content=\"{SITE}/assets/og.jpg\">\n"
    "<meta name=\"twitter:card\" content=\"summary_large_image\">\n"
    + head_part.strip() + "\n</head>\n<body>\n"
    + main_part.strip() + "\n</body>\n</html>\n"
)
# 動画のアドレスに中身の印（?v=…）を付ける。差し替えるとアプリがしまい直す
def _ver(m):
    f = root / m.group(2)
    if not f.exists():
        return m.group(0)
    return m.group(1) + m.group(2) + "?v=" + hashlib.sha1(f.read_bytes()).hexdigest()[:8] + '"'
doc = re.sub(r'(video:\s*")([^"?]+)"', _ver, doc)
(root / "index.html").write_text(doc, encoding="utf-8")

# sw.js：最初から保存しておくもの＝画面・アイコン・表紙（動画は入れない）
covers = sorted(set(re.findall(r'(?:cover|thumb):\s*"([^"]+)"', body)))
core = ["./", "manifest.webmanifest", "assets/icon-180.png", "assets/icon-192.png", "assets/icon-512.png"] + covers
for c in core[1:]:
    if not (root / c).exists():
        print("※ まだ無いファイル:", c)
h = hashlib.sha1(doc.encode())
for c in core[1:]:
    p = root / c
    if p.exists():
        h.update(p.read_bytes())
sw = (root / "src" / "sw.js").read_text(encoding="utf-8")
sw = sw.replace("__VERSION__", h.hexdigest()[:10]).replace("__CORE__", json.dumps(core, ensure_ascii=False))
(root / "sw.js").write_text(sw, encoding="utf-8")
print("index.html:", len(doc), "bytes / sw.js 保存対象:", len(core), "件")
