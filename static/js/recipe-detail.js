(function () {
  'use strict';

  // ── Servings scaler ──────────────────────────────────────────
  var ctrl = document.getElementById('r6-serves-ctrl');
  var countEl = document.getElementById('r6-servings-count');

  if (ctrl && countEl) {
    var base = parseInt(countEl.dataset.base, 10) || 4;
    var totalCost = parseFloat(ctrl.dataset.totalCost) || 0;

    var perPortionEl = document.getElementById('r6-cost-per-portion');
    var portionLabelEl = document.getElementById('r6-cost-portion-label');

    // G2b — round a scaled quantity to a cook's number, unit-aware.
    function kround(v, unit) {
      unit = (unit || '').toLowerCase().replace(/\.$/, '');
      if (unit === 'g') { var st = v < 100 ? 5 : (v < 1000 ? 10 : 25); return String(Math.round(v / st) * st); }
      if (unit === 'mg') { return String(Math.round(v / 50) * 50); }
      if (unit === 'kg' || unit === 'l') { return String(Math.round(v * 20) / 20); }
      if (unit === 'ml') {
        if (v > 500) return String(Math.round(v / 25) * 25);
        var ladder = [1.25, 2.5, 3.75, 5, 7.5, 10, 15, 20, 30, 45, 60, 80, 125, 175, 250, 375, 500];
        var best = ladder[0];
        ladder.forEach(function (x) { if (Math.abs(x - v) < Math.abs(best - v)) best = x; });
        return String(best);
      }
      // countables (onion, clove, egg, no unit) — whole or common half, never 1.8
      var half = Math.round(v * 2) / 2;
      if (Math.abs(half - Math.round(half)) <= 0.2) return String(Math.round(half));
      return String(half);
    }
    // The ONE scaling engine. Both the inline Serves stepper and the Scale modal
    // call this, so they can never disagree. Scales every .r6-ing__qty from its
    // stored original by (n / base), rounded to cook's numbers.
    window.applyServings = function (n) {
      n = Math.max(1, parseInt(n, 10) || base);
      var factor = n / base;
      document.querySelectorAll('.r6-ing__qty').forEach(function (el) {
        if (el.dataset.orig === undefined) el.dataset.orig = el.textContent;
        var t = el.dataset.orig.trim();
        var mm = t.match(/^(\d+\.?\d*)\s*(.*)$/);
        if (mm) {
          el.textContent = kround(parseFloat(mm[1]) * factor, mm[2]) + (mm[2] ? ' ' + mm[2] : '');
        } else {
          el.textContent = t.replace(/(\d+\.?\d*)/g, function (m, num) {
            var s = parseFloat(num) * factor; return (s % 1 === 0) ? String(s) : s.toFixed(1);
          });
        }
      });
      // G2c — imperial fragments in notes go stale when scaled: drop them off-base,
      // restore at base serves.
      document.querySelectorAll('.r6-ing__note-inline').forEach(function (el) {
        if (el.dataset.orig === undefined) el.dataset.orig = el.textContent;
        if (factor === 1) { el.textContent = el.dataset.orig; }
        else {
          el.textContent = el.dataset.orig
            .replace(/\s*\(?\d+\.?\d*\s*(?:lb|lbs|oz)\)?/gi, '')
            .replace(/\(\s*\)/g, '').replace(/\s{2,}/g, ' ').trim();
        }
      });
      countEl.textContent = n;
      var scNum = document.getElementById('sc-num');
      if (scNum) scNum.textContent = n;
      if (totalCost > 0) {
        var cpp = (totalCost / n).toFixed(2);
        if (perPortionEl) perPortionEl.textContent = '$' + cpp;
        if (portionLabelEl) portionLabelEl.textContent = '(' + n + ' portions)';
      }
      return n;
    };

    ctrl.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-delta]');
      if (!btn) return;
      var delta = parseInt(btn.dataset.delta, 10);
      window.applyServings((parseInt(countEl.textContent, 10) || base) + delta);
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
