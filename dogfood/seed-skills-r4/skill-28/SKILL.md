---
name: docs-screenshot-standards
description: Produce product screenshots for the public docs to this team's standard. Use when capturing, editing, or reviewing images for documentation pages, tutorials, or release notes.
---

# Docs screenshots — the standard

Public docs images follow these rules; the docs team owns the bar.

## Rules

- Crop to the pane the paragraph is about — never a full desktop, never a full browser window with tabs.
- Annotations use the standard red (#D0342C), 2px stroke, rectangles or single arrows only; no freehand circles.
- All data on screen comes from the demo tenant ("Acme Corp", `*.acme.test` emails) — a real customer name, real email, or live token never appears in a published image.
- Light theme, default zoom, English locale — whatever your personal setup is.
- The cursor is invisible unless the step is literally "click here".
- Filenames are `<page-slug>-<ordinal>.png`; an image edited later keeps its name so links hold.

## Exit

Review every image at 100% zoom against each rule above before the docs PR merges — screenshots are checked by eye, image by image, and a violation found later means recapturing, not patching.
