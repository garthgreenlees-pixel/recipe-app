/* kitchen.js — MyKitchen modal wiring (Phase A: URL / Scan / Write; Phase B adds PDF) */

(function () {
  var overlay = document.getElementById('kitchen-overlay');
  if (!overlay) return;

  // ── Open modal ──────────────────────────────────────────────────────────────
  document.querySelectorAll('[data-modal]').forEach(function (trigger) {
    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      var id = 'modal-' + trigger.dataset.modal;
      var modal = document.getElementById(id);
      if (!modal) return;
      overlay.querySelectorAll('.kmodal').forEach(function (m) { m.hidden = true; });
      modal.hidden = false;
      overlay.classList.add('is-open');
      overlay.setAttribute('aria-hidden', 'false');
      var first = modal.querySelector('input, textarea, button:not(.kmodal__close)');
      if (first) first.focus();
    });
  });

  // ── Close modal ─────────────────────────────────────────────────────────────
  function closeModal() {
    overlay.classList.remove('is-open');
    overlay.setAttribute('aria-hidden', 'true');
    overlay.querySelectorAll('.kmodal').forEach(function (m) { m.hidden = true; });
  }

  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) closeModal();
  });

  overlay.querySelectorAll('[data-close-modal]').forEach(function (btn) {
    btn.addEventListener('click', closeModal);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeModal();
  });

  // ── Import a URL — native form POST to /enhance; no JS handler needed ──────
  // The #modal-url form has method="post" action="/enhance"; browser handles it.

  // ── Scan a page — image upload → /api/scan → save → redirect ──────────────
  var btnScan = document.getElementById('btn-scan');
  if (btnScan) {
    btnScan.addEventListener('click', function () {
      var fileInput = document.getElementById('scan-file');
      var status = document.getElementById('scan-status');

      if (!fileInput || !fileInput.files || !fileInput.files[0]) {
        status.textContent = 'Choose a photo first.';
        status.classList.add('is-error');
        status.hidden = false;
        return;
      }

      btnScan.disabled = true;
      btnScan.textContent = 'Reading image…';
      status.classList.remove('is-error');
      status.hidden = true;

      var fd = new FormData();
      fd.append('image0', fileInput.files[0]);

      fetch('/api/scan', { method: 'POST', body: fd })
        .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }); })
        .then(function (res) {
          if (!res.ok) throw new Error(res.data.error || 'Scan failed');
          var recipe = res.data;
          status.textContent = 'Scan complete — saving…';
          status.hidden = false;
          return fetch('/api/recipes/new', { method: 'POST' })
            .then(function (r2) { return r2.json(); })
            .then(function (draft) {
              if (!draft.uuid) throw new Error('Could not create recipe draft');
              var payload = {
                title: recipe.title || 'Untitled Recipe',
                preamble: recipe.preamble || '',
                tags: recipe.tags || [],
                time: recipe.time || {},
                servings: recipe.servings || [],
                ingredients: recipe.ingredients || [],
                steps: recipe.steps || [],
                source: recipe.source_book || {}
              };
              return fetch('/api/recipes/' + draft.uuid, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
              }).then(function () {
                window.location.href = '/recipe/' + draft.slug + '/edit';
              });
            });
        })
        .catch(function (err) {
          status.textContent = 'Something went wrong — ' + err.message;
          status.classList.add('is-error');
          status.hidden = false;
          btnScan.disabled = false;
          btnScan.textContent = 'Scan and import →';
        });
    });
  }

  // ── Write from scratch — /api/recipes/new → redirect ──────────────────────
  var btnWrite = document.getElementById('btn-write');
  if (btnWrite) {
    btnWrite.addEventListener('click', function () {
      var status = document.getElementById('write-status');
      btnWrite.disabled = true;
      btnWrite.textContent = 'Opening…';
      status.hidden = true;

      fetch('/api/recipes/new', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.slug) {
            window.location.href = '/recipe/' + data.slug + '/edit';
          } else {
            throw new Error(data.error || 'Unexpected response');
          }
        })
        .catch(function (err) {
          status.textContent = 'Something went wrong — ' + err.message;
          status.classList.add('is-error');
          status.hidden = false;
          btnWrite.disabled = false;
          btnWrite.textContent = 'Open blank editor →';
        });
    });
  }

})();
