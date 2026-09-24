// 画面と画像だけを保存して、電波が弱くても最初の画面がすぐ出るようにする。
// 動画（.mp4）へのリクエストには一切さわらない。
// （iPhone の Safari は、ここを通した動画の途中読み込みで再生に失敗することがあるため）
const CACHE = 'mama-11b4f0465d';
const CORE = ["./", "manifest.webmanifest", "assets/covers/01.jpg?v=b36d1b22", "assets/covers/02-thumb.jpg?v=78b70d45", "assets/covers/02.jpg?v=327c27d0", "assets/fonts/mplus-rounded-800-latin.woff2?v=61bdd426", "assets/icon-180.png?v=5a5c6df0", "assets/icon-192.png?v=3b61e325"];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k.startsWith('mama-') && k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  const url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin) return;
  if (/\.mp4$/i.test(url.pathname) || req.headers.has('range') || req.destination === 'video') return;
  if (url.pathname.endsWith('/version.txt')) return;   // 版の確認は、いつもネットに聞く
  if (req.mode === 'navigate') {
    // 画面は新しいものを優先（更新がすぐ届くように）。つながらないときは保存分。
    e.respondWith(fetch(req, { cache: 'no-cache' }).then(r => {
      const copy = r.clone(); caches.open(CACHE).then(c => c.put('./', copy)); return r;
    }).catch(() => caches.match('./')));
    return;
  }
  e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => {
    if (r.ok) { const copy = r.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
    return r;
  })));
});
