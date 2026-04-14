---
title: PDF Import Hover Preview Z-Index Blocking Checkbox Interaction
category: ui-bugs
date_solved: 2026-03-03
severity: medium
component: PDF Import Modal (index.html)
tags: [css-stacking-context, z-index, hover-preview, accessibility, modal-ui]
symptoms:
  - Hover preview visually covered recipe card thumbnails during PDF page selection
  - Checkboxes rendered invisible beneath hover preview
  - Impossible to click checkboxes while preview was displayed
root_cause: Hover preview element (position fixed, z-index 500) was a DOM sibling of overlay (z-index 300), creating independent stacking context that painted above entire modal. Checkbox z-index 501 was trapped inside overlay stacking context, unable to escape parent z-index 300 limit.
resolution_type: code_fix
related_docs:
  - docs/solutions/performance-issues/pdf-import-timeout-optimization.md
---

# PDF Hover Preview Covering Checkboxes

## Problem

In the PDF import modal, page thumbnails are displayed in a grid with checkboxes for selecting/deselecting pages. When hovering over thumbnails, a large preview image appears to help users see page content. However, the hover preview was covering the checkboxes on adjacent thumbnails, making them impossible to see and click.

## Investigation Steps

1. **Initial observation**: Preview appeared above checkboxes, blocking interaction
2. **Examined CSS structure**: Identified z-index layering across elements:
   - `.pdf-overlay` (modal backdrop): `z-index: 300` with `position: fixed`
   - `.pdf-page-thumb` (thumbnail): `z-index: 1` with `position: relative`
   - `.page-check` (checkbox): `z-index: 2` within the thumb's stacking context
   - `.pdf-hover-preview` (preview): `z-index: 500` with `position: fixed`, **outside the overlay in the DOM**
3. **First fix attempt (failed)**: Increased checkbox z-index to 501 and added mouseenter handler to hide preview on checkbox hover
4. **Discovered why it failed**:
   - z-index values are context-dependent; 501 was still trapped inside the overlay's stacking context (z-index: 300)
   - The mouseenter handler only worked on the SAME thumbnail's checkbox, not adjacent thumbnails covered by the preview

## Root Cause

**Stacking context hierarchy misalignment.** The DOM structure placed the hover preview outside the modal overlay:

```
<body>
  <div class="pdf-overlay" style="z-index: 300">    <!-- stacking context A -->
    <div class="pdf-page-thumb" style="z-index: 1"> <!-- stacking context B (nested in A) -->
      <div class="page-check" style="z-index: 501"> <!-- trapped in B, which is in A -->
    </div>
  </div>
  <div class="pdf-hover-preview" style="z-index: 500"> <!-- stacking context C (root level) -->
  </div>
</body>
```

The preview (z-index: 500 at root level) always paints above the overlay (z-index: 300 at root level). No matter how high the checkbox z-index is, it cannot escape its parent stacking context (300). A child's z-index is only evaluated relative to siblings within the same stacking context.

## Solution

Three coordinated changes were required:

### 1. Move preview element inside the overlay (DOM change)

```html
<!-- Before: preview was a sibling of overlay -->
<div id="pdfOverlay" class="pdf-overlay">
  <div class="pdf-modal">...</div>
</div>
<div id="pdfHoverPreview" class="pdf-hover-preview">...</div>

<!-- After: preview is inside overlay, sharing its stacking context -->
<div id="pdfOverlay" class="pdf-overlay">
  <div class="pdf-modal">...</div>
  <div id="pdfHoverPreview" class="pdf-hover-preview">...</div>
</div>
```

### 2. Remove z-index from .pdf-page-thumb (CSS change)

```css
/* Before: thumb created a nested stacking context */
.pdf-page-thumb { position: relative; z-index: 1; }
.pdf-page-thumb:hover { border-color: var(--accent); z-index: 10; }

/* After: no stacking context, checkbox z-index participates in overlay's context */
.pdf-page-thumb { position: relative; }
.pdf-page-thumb:hover { border-color: var(--accent); }
```

### 3. Checkbox z-index above preview (CSS change)

```css
.page-check {
  position: absolute;
  z-index: 501;         /* above preview's 500, now in overlay's context */
  pointer-events: auto; /* explicit clickability */
}
```

### 4. Defense-in-depth: mouseenter handler (JS, from first fix)

```javascript
const check = thumb.querySelector('.page-check');
check.addEventListener('mouseenter', (e) => {
  e.stopPropagation();
  hidePdfHover();
});
```

## Key Insight

**Z-index problems require examining the entire stacking context tree, not just the conflicting elements.** Simply increasing a z-index number doesn't help if the parent context has a lower z-index in a higher context. The fix often requires DOM restructuring (moving elements into the correct stacking context) rather than z-index escalation.

## Prevention Strategies

1. **DOM hierarchy first, z-index second** -- place positioned elements as children of their intended parent context, don't rely on z-index to fix DOM ordering
2. **Minimize stacking context creation** -- only use z-index on elements that need it; each z-index on a positioned element creates a new stacking context
3. **Test with interactive content** -- when adding hover previews or tooltips, verify they don't block buttons, checkboxes, or inputs on adjacent elements

### Checklist for Fixed/Absolute Positioned Elements

- [ ] Is the element placed as a child of its intended parent container?
- [ ] Does this element actually need a z-index, or can it rely on DOM order?
- [ ] Are there parent elements with z-index that create unwanted stacking contexts?
- [ ] Will this positioned element block interaction with elements below it?
- [ ] Is the z-index relative to other elements in the SAME stacking context?
