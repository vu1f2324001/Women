// Service Worker for PWA functionality
const CACHE_NAME = 'empowerher-v1';
const urlsToCache = [
  '/',
  '/index',
  '/static/css/style.css',
  '/static/js/script.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});

