const CACHE_NAME = 'recipe-site-cache-v1';
const urlsToCache = [
  '/',
  '/assets/css/recipe-styles.css',
  '/assets/css/styles.css',
  '/assets/images/favicon2.png',
  '/assets/images/icon-192x192.png',
  '/assets/images/icon-512x512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => response || fetch(event.request))
  );
});