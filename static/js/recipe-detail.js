(function () {
  'use strict';

  // ── Servings scaler ──────────────────────────────────────────
  var ctrl = document.getElementById('r6-serves-ctrl');
  var countEl = document.getElementById('r6-servings-count');

  if (ctrl && countEl) {
    var base = parseInt(countEl.dataset.base, 10) || 4;
    var current = base;
    var totalCost = parseFloat(ctrl.dataset.totalCost) || 0;

    var perPortionEl = document.getElementById('r6-cost-per-portion');
    var portionLabelEl = document.getElementById('r6-cost-portion-label');

    ctrl.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-delta]');
      if (!btn) return;
      var delta = parseInt(btn.dataset.delta, 10);
      current = Math.max(1, current + delta);
      countEl.textContent = current;

      if (totalCost > 0) {
        var cpp = (totalCost / current).toFixed(2);
        if (perPortionEl) perPortionEl.textContent = '$' + cpp;
        if (portionLabelEl) portionLabelEl.textContent = '(' + current + ' portions)';
      }
    });
  }

  // ── Set-target form ──────────────────────────────────────────
  var form = document.getElementById('r6-cost-target-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var slug = form.dataset.slug;
      var menuPrice = parseFloat(form.elements.menu_price.value) || null;
      var targetPct = parseFloat(form.elements.target_food_cost_pct.value) || 30;
      var statusEl = document.getElementById('r6-cost-form-status');

      fetch('/api/costing/recipe/' + slug + '/set-target', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ menu_price: menuPrice, target_food_cost_pct: targetPct })
      })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
        .then(function () {
          if (statusEl) { statusEl.textContent = 'Saved.'; setTimeout(function () { statusEl.textContent = ''; }, 2000); }
          location.reload();
        })
        .catch(function () {
          if (statusEl) statusEl.textContent = 'Save failed — check you are signed in.';
        });
    });
  }
})();
