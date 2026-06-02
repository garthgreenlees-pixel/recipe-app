/* kitchen.js — MyKitchen modal wiring (Phase A: URL/Scan/Write; Phase B: PDF) */

// ─── PDF state (global so onclick attrs can reach PDF functions) ────────────
var pdfPages = [];
var pdfSelectedPages = new Set();
var pdfClassification = null;
var pdfExtracted = [];

// ─── Modal management (IIFE — private scope) ───────────────────────────────
(function () {
  var overlay = document.getElementById('kitchen-overlay');
  if (!overlay) return;

  function closeModal() {
    overlay.classList.remove('is-open');
    overlay.setAttribute('aria-hidden', 'true');
    overlay.querySelectorAll('.kmodal').forEach(function (m) { m.hidden = true; });
  }

  // Expose so PDF cancel buttons (in onclick attrs) can call it
  window.closePdfImportModal = function () { closeModal(); resetPdfModal(); };

  // Open
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

  // Close — overlay click, close button, Escape
  overlay.addEventListener('click', function (e) { if (e.target === overlay) closeModal(); });
  overlay.querySelectorAll('[data-close-modal]').forEach(function (btn) {
    btn.addEventListener('click', closeModal);
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeModal(); });

  // ── Scan a page — image → /api/scan → /api/recipes (full pipeline) → redirect ──
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
          btnScan.textContent = 'Building your recipe…';
          status.textContent = 'Scan complete — building recipe…';
          status.hidden = false;
          return fetch('/api/recipes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              title: recipe.title || 'Untitled Recipe',
              preamble: recipe.preamble || '',
              tags: recipe.tags || [],
              time: recipe.time || {},
              servings: recipe.servings || [],
              ingredients: recipe.ingredients || [],
              steps: recipe.steps || [],
              source_book: recipe.source_book || {},
              _images_b64: recipe._images_b64 || [],
              _images_media_types: recipe._images_media_types || []
            })
          })
            .then(function (r2) { return r2.json().then(function (d) { return { ok: r2.ok, data: d }; }); })
            .then(function (res2) {
              if (!res2.ok) throw new Error(res2.data.error || 'Save failed');
              window.location.href = '/recipe/' + res2.data.slug + '/edit';
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

  // ── Import a URL — /api/import-url → /api/recipes (full pipeline) → redirect ──
  var btnUrl = document.getElementById('btn-url');
  if (btnUrl) {
    btnUrl.addEventListener('click', function () {
      var urlInput = document.getElementById('url-input');
      var status = document.getElementById('url-status');
      var url = (urlInput && urlInput.value || '').trim();
      if (!url) {
        status.textContent = 'Paste a URL first.';
        status.classList.add('is-error');
        status.hidden = false;
        return;
      }
      btnUrl.disabled = true;
      btnUrl.textContent = 'Fetching recipe…';
      status.classList.remove('is-error');
      status.hidden = true;
      if (window.ProvenanceProcessing) ProvenanceProcessing.show({ messages: ['Fetching the page…', 'Building your recipe…', 'Running enhancement…'] });

      fetch('/api/import-url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
      })
        .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }); })
        .then(function (res) {
          if (!res.ok) throw new Error(res.data.error || 'Could not fetch that URL');
          var recipe = res.data;
          if ((!recipe.ingredients || recipe.ingredients.length === 0) &&
              (!recipe.steps || recipe.steps.length === 0)) {
            throw new Error("Couldn't read a recipe from that page — try a URL with a structured recipe");
          }
          btnUrl.textContent = 'Building your recipe…';
          status.textContent = 'Page read — running enhancement…';
          status.hidden = false;
          var payload = {
            title: recipe.title || 'Imported Recipe',
            preamble: recipe.preamble || '',
            tags: recipe.tags || [],
            time: recipe.time || {},
            servings: recipe.servings || [],
            ingredients: recipe.ingredients || [],
            steps: recipe.steps || [],
            source: recipe.source || { name: '', address: url }
          };
          if (recipe._hero_b64) payload._hero_custom_b64 = recipe._hero_b64;
          return fetch('/api/recipes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          })
            .then(function (r2) { return r2.json().then(function (d) { return { ok: r2.ok, data: d }; }); })
            .then(function (res2) {
              if (!res2.ok) throw new Error(res2.data.error || 'Save failed');
              if (window.ProvenanceProcessing) ProvenanceProcessing.hide();
              window.location.href = '/recipe/' + res2.data.slug + '/edit';
            });
        })
        .catch(function (err) {
          if (window.ProvenanceProcessing) ProvenanceProcessing.hide();
          status.textContent = err.message;
          status.classList.add('is-error');
          status.hidden = false;
          btnUrl.disabled = false;
          btnUrl.textContent = 'Fetch and import →';
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

  // ── PDF drag-and-drop wiring ────────────────────────────────────────────────
  var pdfArea = document.getElementById('pdfUploadArea');
  if (pdfArea) {
    pdfArea.addEventListener('dragover', function (e) { e.preventDefault(); e.stopPropagation(); pdfArea.classList.add('drag-over'); });
    pdfArea.addEventListener('dragleave', function (e) { e.preventDefault(); e.stopPropagation(); pdfArea.classList.remove('drag-over'); });
    pdfArea.addEventListener('drop', function (e) {
      e.preventDefault(); e.stopPropagation(); pdfArea.classList.remove('drag-over');
      var file = Array.from(e.dataTransfer.files).find(function (f) {
        return f.type === 'application/pdf' || f.name.toLowerCase().endsWith('.pdf');
      });
      if (file) handlePdfFile(file);
    });
  }

  var pdfFileInput = document.getElementById('pdfFileInput');
  if (pdfFileInput) {
    pdfFileInput.addEventListener('change', function (e) {
      var file = e.target.files[0];
      if (!file) return;
      e.target.value = '';
      handlePdfFile(file);
    });
  }
})();

// ─── PDF helpers (global — called from onclick attributes) ─────────────────

function esc(s) {
  if (!s) return '';
  var d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}

function parseIngredientLine(line) {
  line = line.trim();
  if (!line) return null;
  var group = '';
  var groupMatch = line.match(/\[(.+?)\]\s*$/);
  if (groupMatch) { group = groupMatch[1]; line = line.substring(0, groupMatch.index).trim(); }
  var info = '';
  var infoMatch = line.match(/\s-\s(.+)$/);
  if (infoMatch) { info = infoMatch[1]; line = line.substring(0, infoMatch.index).trim(); }
  var parts = line.match(/^(\d+[\d\/\s]*(?:\/\d+)?)\s+(tsp|tbsp|cup|cups|g|kg|ml|L|oz|lb|lbs|teaspoon|tablespoon|bunch|cloves?|pieces?|pinch|handful)\s+(.+)$/i);
  if (parts) return { name: parts[3], unit: parts[2], count: parts[1].trim(), info: info, group: group };
  var numMatch = line.match(/^(\d+[\d\/\s]*(?:\/\d+)?)\s+(.+)$/);
  if (numMatch) return { name: numMatch[2], unit: '', count: numMatch[1].trim(), info: info, group: group };
  return { name: line, unit: '', count: '', info: info, group: group };
}

function setPdfProgress(label, pct) {
  var el = document.getElementById('pdfProgress');
  if (!el) return;
  el.style.display = '';
  var lbl = document.getElementById('pdfProgressLabel');
  if (lbl) lbl.textContent = label;
  var fill = document.getElementById('pdfProgressFill');
  if (fill) fill.style.width = pct + '%';
}

function resetPdfModal() {
  pdfPages = [];
  pdfSelectedPages = new Set();
  pdfClassification = null;
  pdfExtracted = [];
  var ids = ['pdfUploadSection', 'pdfSelectSection', 'pdfClassifySection', 'pdfReviewSection'];
  ids.forEach(function (id) { var el = document.getElementById(id); if (el) el.style.display = id === 'pdfUploadSection' ? '' : 'none'; });
  var progress = document.getElementById('pdfProgress');
  if (progress) progress.style.display = 'none';
  var grid = document.getElementById('pdfPageGrid');
  if (grid) grid.innerHTML = '';
  var ri = document.getElementById('pdfRangeInput');
  if (ri) ri.value = '';
  var rg = document.getElementById('pdfRecipeGroups');
  if (rg) rg.innerHTML = '';
  var rl = document.getElementById('pdfReviewList');
  if (rl) rl.innerHTML = '';
}

function ensurePdfJs() {
  if (window.pdfjsLib) return Promise.resolve();
  return new Promise(function (resolve, reject) {
    var s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js';
    s.onload = function () {
      window.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
      resolve();
    };
    s.onerror = reject;
    document.head.appendChild(s);
  });
}

async function handlePdfFile(file) {
  document.getElementById('pdfUploadSection').style.display = 'none';
  setPdfProgress('Loading PDF.js…', 0);
  try {
    await ensurePdfJs();
  } catch (e) {
    setPdfProgress('Failed to load PDF.js. Check your connection.', 0);
    return;
  }
  setPdfProgress('Opening PDF…', 5);
  var arrayBuffer = await file.arrayBuffer();
  var pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
  var numPages = pdf.numPages;
  setPdfProgress('Rendering pages… 0/' + numPages, 5);
  var grid = document.getElementById('pdfPageGrid');
  grid.innerHTML = '';
  pdfPages = [];

  for (var i = 1; i <= numPages; i++) {
    var page = await pdf.getPage(i);
    var viewport = page.getViewport({ scale: 0.6 });
    var canvas = document.createElement('canvas');
    canvas.width = viewport.width;
    canvas.height = viewport.height;
    await page.render({ canvasContext: canvas.getContext('2d'), viewport: viewport }).promise;
    var dataUrl = canvas.toDataURL('image/jpeg', 0.70);
    var base64 = dataUrl.split(',')[1];
    pdfPages.push({ dataUrl: dataUrl, base64: base64, mediaType: 'image/jpeg' });

    var pageIdx = i - 1;
    var thumb = document.createElement('div');
    thumb.className = 'pdf-page-thumb deselected';
    thumb.innerHTML = '<img src="' + dataUrl + '"><span class="page-num">' + i + '</span><div class="page-check" onclick="togglePdfPage(event,' + pageIdx + ')"></div>';
    thumb.addEventListener('click', function (idx) {
      return function (e) {
        if (e.target.closest('.page-check')) return;
        togglePdfPage(e, idx);
      };
    }(pageIdx));
    grid.appendChild(thumb);

    setPdfProgress('Rendering pages… ' + i + '/' + numPages, 5 + Math.round((i / numPages) * 60));
    await new Promise(function (r) { setTimeout(r, 0); });
  }

  setPdfProgress('Pages rendered — select pages to classify.', 100);
  document.getElementById('pdfSelectSection').style.display = '';
  updatePdfSelectCount();
}

function togglePdfPage(e, pageIdx) {
  if (e) e.stopPropagation();
  if (pdfSelectedPages.has(pageIdx)) { pdfSelectedPages.delete(pageIdx); } else { pdfSelectedPages.add(pageIdx); }
  updatePdfThumbStates();
  updatePdfSelectCount();
  var ri = document.getElementById('pdfRangeInput');
  if (ri) ri.value = buildRangeString();
}

function updatePdfThumbStates() {
  var thumbs = document.getElementById('pdfPageGrid').children;
  for (var i = 0; i < thumbs.length; i++) {
    var thumb = thumbs[i];
    var check = thumb.querySelector('.page-check');
    if (pdfSelectedPages.has(i)) {
      thumb.classList.remove('deselected');
      if (check) { check.classList.add('checked'); check.innerHTML = '&#10003;'; }
    } else {
      thumb.classList.add('deselected');
      if (check) { check.classList.remove('checked'); check.innerHTML = ''; }
    }
  }
}

function updatePdfSelectCount() {
  var countEl = document.getElementById('pdfSelectCount');
  if (countEl) countEl.textContent = pdfSelectedPages.size + ' of ' + pdfPages.length + ' pages selected';
  var btn = document.getElementById('pdfClassifyBtn');
  if (btn) btn.disabled = pdfSelectedPages.size === 0;
}

function pdfSelectAll() {
  for (var i = 0; i < pdfPages.length; i++) pdfSelectedPages.add(i);
  var ri = document.getElementById('pdfRangeInput');
  if (ri) ri.value = '';
  updatePdfThumbStates();
  updatePdfSelectCount();
}

function pdfSelectNone() {
  pdfSelectedPages.clear();
  var ri = document.getElementById('pdfRangeInput');
  if (ri) ri.value = '';
  updatePdfThumbStates();
  updatePdfSelectCount();
}

function applyRangeInput() {
  var input = document.getElementById('pdfRangeInput').value.trim();
  pdfSelectedPages.clear();
  if (!input) {
    for (var i = 0; i < pdfPages.length; i++) pdfSelectedPages.add(i);
  } else {
    input.split(',').forEach(function (part) {
      part = part.trim();
      var rangeMatch = part.match(/^(\d+)\s*-\s*(\d+)$/);
      if (rangeMatch) {
        var start = Math.max(1, parseInt(rangeMatch[1]));
        var end = Math.min(pdfPages.length, parseInt(rangeMatch[2]));
        for (var i = start; i <= end; i++) pdfSelectedPages.add(i - 1);
      } else {
        var num = parseInt(part);
        if (!isNaN(num) && num >= 1 && num <= pdfPages.length) pdfSelectedPages.add(num - 1);
      }
    });
  }
  updatePdfThumbStates();
  updatePdfSelectCount();
}

function buildRangeString() {
  var sorted = Array.from(pdfSelectedPages).sort(function (a, b) { return a - b; });
  if (!sorted.length || sorted.length === pdfPages.length) return '';
  var ranges = [];
  var start = sorted[0], end = sorted[0];
  for (var i = 1; i < sorted.length; i++) {
    if (sorted[i] === end + 1) { end = sorted[i]; } else {
      ranges.push(start === end ? (start + 1) + '' : (start + 1) + '-' + (end + 1));
      start = end = sorted[i];
    }
  }
  ranges.push(start === end ? (start + 1) + '' : (start + 1) + '-' + (end + 1));
  return ranges.join(', ');
}

function startClassification() {
  if (pdfSelectedPages.size === 0) return;
  document.getElementById('pdfSelectSection').style.display = 'none';
  setPdfProgress('Classifying selected pages…', 60);
  classifyPages();
}

async function classifyPages() {
  var selectedIndices = Array.from(pdfSelectedPages).sort(function (a, b) { return a - b; });
  var batchSize = 5;
  var numBatches = Math.ceil(selectedIndices.length / batchSize);
  var allRecipes = [], allSkipped = [];

  for (var b = 0; b < numBatches; b++) {
    if (b > 0) await new Promise(function (r) { setTimeout(r, 5000); });
    var batchIndices = selectedIndices.slice(b * batchSize, (b + 1) * batchSize);
    setPdfProgress('Classifying batch ' + (b + 1) + '/' + numBatches + '…', 60 + Math.round(((b + 1) / numBatches) * 30));
    var images = batchIndices.map(function (idx) { return { data: pdfPages[idx].base64, media_type: pdfPages[idx].mediaType }; });

    var retries = 0;
    while (true) {
      try {
        var res = await fetch('/api/classify-pages', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ images: images })
        });
        var data = await res.json();
        if (!res.ok) {
          if ((res.status === 429 || res.status === 502) && data.error && data.error.includes('rate') && retries < 5) {
            retries++;
            var wait = Math.min(30 + retries * 30, 180);
            setPdfProgress('Rate limited — waiting ' + wait + 's…', 60 + Math.round((b / numBatches) * 30));
            await new Promise(function (r) { setTimeout(r, wait * 1000); });
            continue;
          }
          throw new Error(data.error || 'Classification failed');
        }
        (data.recipes || []).forEach(function (r) {
          allRecipes.push({ title: r.title, pages: r.pages.map(function (p) { return batchIndices[p]; }) });
        });
        (data.skipped_pages || []).forEach(function (p) { allSkipped.push(batchIndices[p]); });
        break;
      } catch (err) {
        setPdfProgress('Error classifying batch ' + (b + 1) + ': ' + err.message, 0);
        return;
      }
    }
  }

  pdfClassification = { recipes: allRecipes, skipped_pages: allSkipped };
  setPdfProgress('Classification complete.', 100);
  showClassificationResults();
}

function showClassificationResults() {
  var container = document.getElementById('pdfRecipeGroups');
  container.innerHTML = '';
  pdfClassification.recipes.forEach(function (recipe, idx) {
    var group = document.createElement('div');
    group.className = 'pdf-recipe-group';
    var thumbsHtml = recipe.pages.slice(0, 3).map(function (p) {
      return '<img src="' + pdfPages[p].dataUrl + '" title="Page ' + (p + 1) + '">';
    }).join('');
    group.innerHTML = '<div class="group-thumbs">' + thumbsHtml + '</div><div class="group-info"><h4>' + esc(recipe.title) + '</h4><small>Pages: ' + recipe.pages.map(function (p) { return p + 1; }).join(', ') + '</small></div><button class="group-remove" onclick="removePdfRecipe(' + idx + ')" title="Remove">&times;</button>';
    container.appendChild(group);
  });
  document.getElementById('pdfClassifySection').style.display = '';
}

function removePdfRecipe(idx) {
  pdfClassification.recipes.splice(idx, 1);
  showClassificationResults();
}

async function extractAllRecipes() {
  var recipes_to_extract = pdfClassification.recipes;
  if (!recipes_to_extract.length) return;
  document.getElementById('pdfExtractBtn').disabled = true;
  pdfExtracted = new Array(recipes_to_extract.length);
  var total = recipes_to_extract.length;
  var completed = 0;
  var nextIdx = 0;

  async function extractOne(i) {
    var recipe = recipes_to_extract[i];
    var retries = 0;
    while (true) {
      try {
        var fd = new FormData();
        for (var j = 0; j < recipe.pages.length && j < 5; j++) {
          var pageIdx = recipe.pages[j];
          var resp2 = await fetch(pdfPages[pageIdx].dataUrl);
          var blob2 = await resp2.blob();
          fd.append('image_' + j, blob2, 'page_' + pageIdx + '.jpg');
        }
        var res = await fetch('/api/scan', { method: 'POST', body: fd });
        var data = await res.json();
        if (!res.ok) {
          if ((res.status === 429 || res.status === 502) && data.error && data.error.includes('rate') && retries < 5) {
            retries++;
            var wait = Math.min(30 + retries * 30, 180);
            setPdfProgress('Rate limited — waiting ' + wait + 's…', Math.round((completed / total) * 100));
            await new Promise(function (r) { setTimeout(r, wait * 1000); });
            continue;
          }
          throw new Error(data.error || 'Extraction failed');
        }
        pdfExtracted[i] = data;
        completed++;
        setPdfProgress('Extracted ' + completed + ' of ' + total + ' recipes…', Math.round((completed / total) * 100));
        return;
      } catch (err) {
        pdfExtracted[i] = { title: recipe.title + ' (failed)', preamble: '', tags: [], time: {}, servings: [], ingredients: [], steps: [], _error: err.message };
        completed++;
        setPdfProgress('Extracted ' + completed + ' of ' + total + ' recipes…', Math.round((completed / total) * 100));
        return;
      }
    }
  }

  async function worker() {
    while (nextIdx < total) { var i = nextIdx++; await extractOne(i); }
  }

  await Promise.all([worker(), worker(), worker()].slice(0, Math.min(3, total)));
  setPdfProgress('All recipes extracted — review below.', 100);
  showReviewList();
  document.getElementById('pdfExtractBtn').disabled = false;
}

function showReviewList() {
  document.getElementById('pdfClassifySection').style.display = 'none';
  document.getElementById('pdfReviewSection').style.display = '';
  var list = document.getElementById('pdfReviewList');
  list.innerHTML = '';
  pdfExtracted.forEach(function (recipe, idx) {
    var ingLines = (recipe.ingredients || []).map(function (ing) {
      var line = '';
      if (ing.count) line += ing.count + ' ';
      if (ing.unit) line += ing.unit + ' ';
      line += ing.name;
      if (ing.info) line += ' - ' + ing.info;
      return line;
    }).join('\n');
    var item = document.createElement('div');
    item.className = 'pdf-review-item';
    item.innerHTML = '<h4>' + esc(recipe.title) + (recipe._error ? ' <span style="color:#B94040;font-size:0.8rem">(extraction failed)</span>' : '') + '</h4>' +
      '<label>Title</label><input type="text" data-field="title">' +
      '<label>Ingredients (one per line)</label><textarea data-field="ingredients" rows="5"></textarea>' +
      '<label>Steps (one per line)</label><textarea data-field="steps" rows="5"></textarea>';
    item.querySelector('[data-field="title"]').value = recipe.title || '';
    item.querySelector('[data-field="ingredients"]').value = ingLines;
    item.querySelector('[data-field="steps"]').value = (recipe.steps || []).join('\n');
    list.appendChild(item);
  });
}

async function bulkSaveRecipes() {
  var btn = document.getElementById('pdfSaveAllBtn');
  var status = document.getElementById('pdfSaveStatus');
  btn.disabled = true;
  status.hidden = true;
  var items = document.querySelectorAll('.pdf-review-item');
  var saved = 0;

  for (var i = 0; i < items.length; i++) {
    var item = items[i];
    var title = item.querySelector('[data-field="title"]').value.trim();
    if (!title) continue;
    setPdfProgress('Saving recipe ' + (i + 1) + ' of ' + items.length + '…', Math.round((i / items.length) * 100));
    var ingText = item.querySelector('[data-field="ingredients"]').value;
    var stepsText = item.querySelector('[data-field="steps"]').value;
    var payload = {
      title: title,
      preamble: (pdfExtracted[i] && pdfExtracted[i].preamble) || '',
      tags: (pdfExtracted[i] && pdfExtracted[i].tags) || [],
      time: (pdfExtracted[i] && pdfExtracted[i].time) || {},
      servings: (pdfExtracted[i] && pdfExtracted[i].servings) || [],
      ingredients: ingText.split('\n').map(parseIngredientLine).filter(Boolean),
      steps: stepsText.split('\n').map(function (s) { return s.trim(); }).filter(Boolean),
      source: (pdfExtracted[i] && pdfExtracted[i].source_book) || {}
    };
    try {
      var res = await fetch('/api/recipes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
      if (res.ok) saved++;
    } catch (err) {
      // continue saving others
    }
  }

  setPdfProgress('Saved ' + saved + ' recipe' + (saved !== 1 ? 's' : '') + '.', 100);
  setTimeout(function () { window.location.href = '/kitchen'; }, 1200);
}
