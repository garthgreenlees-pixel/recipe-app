// Self-destruct service worker.
// Replaces the previous SW that was incorrectly intercepting POST requests
// and causing /api/* routes to hang. This file unregisters itself on install
// and clears all caches, then never intercepts another fetch.

self.addEventListener('install', () => {
  self.skipWaiting();
});

self.addEventListener('activate', async (event) => {
  event.waitUntil((async () => {
    // Clear all caches this SW may have created
    try {
      const keys = await caches.keys();
      await Promise.all(keys.map(k => caches.delete(k)));
    } catch (e) {}

    // Unregister this SW so future page loads don't use it
    try {
      await self.registration.unregister();
    } catch (e) {}

    // Tell every open tab to reload so they pick up a clean state
    try {
      const clients = await self.clients.matchAll({type: 'window'});
      clients.forEach(c => c.navigate(c.url));
    } catch (e) {}
  })());
});

// Critical: do NOT add a 'fetch' event handler.
// Without one, the browser bypasses this SW for all network requests.
