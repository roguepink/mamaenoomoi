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
# 動画・画像・書体のアドレスに中身の印（?v=…）を付ける。
# 差し替えると印が変わるので、スマホに残った古いものが使われない（動画はしまい直す）
def _ver(m):
    f = root / m.group(1)
    if not f.exists():
        return m.group(0)
    return m.group(1) + "?v=" + hashlib.sha1(f.read_bytes()).hexdigest()[:8]
doc = re.sub(r'(assets/[A-Za-z0-9_./-]+\.(?:jpg|png|woff2|mp4))(?![?\w])', _ver, doc)

# 最初から保存しておくもの＝画面・アイコン・表紙・書体（動画は入れない）
core = ["./", "manifest.webmanifest"] + sorted(set(
    u for u in re.findall(r'(assets/[A-Za-z0-9_./-]+\.(?:jpg|png|woff2)\?v=\w+)', doc)
    if "og.jpg" not in u))

# 版の印：画面と中身が変わると変わる。アプリはこれを見て、開き直したときに自動で新しくする
build = hashlib.sha1(doc.encode()).hexdigest()[:10]
doc = doc.replace("__BUILD__", build)
(root / "index.html").write_text(doc, encoding="utf-8")
(root / "version.txt").write_text(build + "\n", encoding="utf-8")

sw = (root / "src" / "sw.js").read_text(encoding="utf-8")
sw = sw.replace("__VERSION__", build).replace("__CORE__", json.dumps(core, ensure_ascii=False))
(root / "sw.js").write_text(sw, encoding="utf-8")
print("index.html:", len(doc), "bytes / 版:", build, "/ sw.js 保存対象:", len(core), "件")
