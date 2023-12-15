self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open('fox-store').then((cache) => cache.addAll([
      '/app/',
      '/app/index.html',
      '/app/index.js',
      '/app/pwa.js',
      '/app/style.css',
      '/app/bootstrap.bundle.min.js.js',
      '/app/plotly-2.27.0.min.js.js',
      '/app/bootstrap.min.css'
    ])),
  );
});

self.addEventListener('fetch', (e) => {
  console.log(e.request.url);
  e.respondWith(
    caches.match(e.request).then((response) => response || fetch(e.request)),
  );
});
