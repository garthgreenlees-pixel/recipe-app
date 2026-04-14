---
title: PDF Import Timeout for Large Cookbooks (>5-6 Pages)
date: 2026-03-03
category: performance-issues
tags: [pdf-processing, timeout, gunicorn, batch-processing, image-scaling]
severity: high
component: PDF Import / Batch Processing Pipeline
symptoms:
  - 502 errors when importing PDFs with 5+ pages
  - Import taking 7+ minutes for 20-page PDFs
  - User abandonment due to excessive wait times
  - Gunicorn worker timeout (120s) being exceeded
root_cause: Multiple bottlenecks in PDF processing - undersized gunicorn timeout (120s), small batch size (2 pages), excessive inter-batch delay (30s), full-resolution image rendering producing large base64 payloads, and overly cautious extraction wait (7.5s)
resolution_time: ~30 minutes
---

# PDF Import Timeout for Large Cookbooks

## Problem

PDF import of cookbooks with more than 5-6 pages was timing out or taking extremely long. A 20-page PDF took 7+ minutes or failed with 502 errors. Users would give up waiting.

## Investigation

The PDF import flow has 3 stages:

1. **Client-side rendering** (PDF.js): Renders pages to canvas, converts to JPEG base64. Sequential but fast — not the bottleneck.
2. **Classification** (`/api/classify-pages`): Selected pages sent to Claude vision API to identify which pages contain recipes. Pages batched as base64 images.
3. **Extraction** (`/api/scan`): Each identified recipe sent for full AI extraction.

### Bottlenecks identified

| Bottleneck | Detail | Impact |
|---|---|---|
| Gunicorn timeout 120s | Claude vision API with multiple large images regularly takes 60-90s. Any spike kills the worker. | 502 errors |
| Batch size = 2 pages | 20 pages = 10 API calls needed | 10x more round-trips than necessary |
| 30s inter-batch sleep | Originally to avoid rate limits. 10 batches x 30s = 300s of pure idle time. | 5+ minutes of doing nothing |
| Full resolution rendering | `scale = 1.0` produces ~500KB-1MB base64 per page. Claude doesn't need this for classification. | Slow API calls, large payloads |
| 7.5s extraction sleep | Overly cautious delay between recipe extractions | Compounds with multiple recipes |

## Solution

### 1. Gunicorn timeout: 120s to 300s

File: `Dockerfile`

```dockerfile
# Before
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "120", "--workers", "2", "server:app"]
# After
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "300", "--workers", "2", "server:app"]
```

Accommodates Claude vision API calls that regularly require 60-90s with multiple images.

### 2. Page render scale: 1.0 to 0.6

File: `index.html` (`handlePdfFile` function)

```javascript
// Before
const scale = 1.0;
// After
const scale = 0.6;
```

Reduces base64 payload size by ~64%. Claude's classification doesn't need full resolution.

### 3. Batch size: 2 to 5, wait: 30s to 5s

File: `index.html` (`classifyPages` function)

```javascript
// Before
const batchSize = 2;
if (b > 0) await new Promise(r => setTimeout(r, 30000));

// After
const batchSize = 5;
if (b > 0) await new Promise(r => setTimeout(r, 5000));
```

Fewer API calls needed, dramatically less idle waiting. Rate limit windows are per-minute; 5s between batches is plenty.

### 4. Extraction wait: 7.5s to 3s

File: `index.html` (`extractAllRecipes` function)

```javascript
// Before
if (i > 0) await new Promise(r => setTimeout(r, 7500));
// After
if (i > 0) await new Promise(r => setTimeout(r, 3000));
```

## Impact

| Metric | Before | After |
|---|---|---|
| Gunicorn timeout | 120s (502 risk) | 300s (safe) |
| Page render scale | 1.0 (huge payloads) | 0.6 (~64% smaller) |
| Classification batches (20 pages) | 10 batches of 2 | 4 batches of 5 |
| Batch wait (20 pages) | 300s idle | 15s idle |
| Extraction wait | 7.5s per recipe | 3s per recipe |
| **Total time (20-page PDF)** | **7+ minutes (or 502)** | **1-2 minutes** |

## Prevention & Future Work

### Key lessons

- **Don't use fixed sleep delays for rate limiting.** 30s was chosen arbitrarily and never revisited. Use adaptive backoff: start low, increase only on actual rate limit errors.
- **Right-size payloads for the task.** Classification doesn't need the same image quality as extraction. Consider using different render scales for different pipeline stages.
- **Set server timeouts based on actual API behaviour**, not defaults. Profile your slowest expected API call and add a buffer.

### Monitoring to add

- Track `/api/classify-pages` response times (P50/P95/P99)
- Alert on 502 errors from gunicorn timeout kills
- Log batch sizes, payload sizes, and API durations for tuning

### Future architectural improvements

1. **SSE streaming** for long operations — eliminates timeout pressure entirely
2. **Web Workers** for client-side PDF rendering — unblocks the UI thread
3. **Adaptive batching** — dynamically size batches based on measured API response times
4. **Response caching** — hash page images and cache classification results to avoid re-processing

## Related

- [docs/brainstorms/2026-03-03-beta-readiness-brainstorm.md](../brainstorms/2026-03-03-beta-readiness-brainstorm.md) — broader beta readiness audit that identified this issue
