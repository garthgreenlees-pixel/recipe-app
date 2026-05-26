/* kitchen.js — MyKitchen modal wiring */

(function () {
  const overlay = document.getElementById('kitchen-overlay');
  if (!overlay) return;

  // ── Open modal ──────────────────────────────────────────────────────────────
  document.querySelectorAll('[data-modal]').forEach(function (trigger) {
    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      var id = 'modal-' + trigger.dataset.modal;
      var modal = document.getElementById(id);
      if (!modal) return;
      // hide any previously open modal
      overlay.querySelectorAll('.kmodal').forEach(function (m) { m.hidden = true; });
      modal.hidden = false;
      overlay.classList.add('is-open');
      overlay.setAttribute('aria-hidden', 'false');
      var first = modal.querySelector('input, textarea, button');
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

  // ── Write from scratch ───────────────────────────────────────────────────────
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

  // ── Import a recipe ──────────────────────────────────────────────────────────
  var btnImport = document.getElementById('btn-import');
  if (btnImport) {
    btnImport.addEventListener('click', function () {
      var textarea = document.getElementById('import-text');
      var status = document.getElementById('import-status');
      var text = textarea ? textarea.value.trim() : '';

      if (!text) {
        status.textContent = 'Paste some recipe text first.';
        status.classList.add('is-error');
        status.hidden = false;
        return;
      }

      btnImport.disabled = true;
      btnImport.textContent = 'Reading…';
      status.hidden = true;

      fetch('/api/recipes/extract-from-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.slug) {
            window.location.href = '/recipe/' + data.slug + '/edit';
          } else {
            throw new Error(data.error || 'Unexpected response');
          }
        })
        .catch(function (err) {
          status.textContent = 'Could not read that recipe — ' + err.message;
          status.classList.remove('is-error');
          status.classList.add('is-error');
          status.hidden = false;
          btnImport.disabled = false;
          btnImport.textContent = 'Import →';
        });
    });
  }
})();
