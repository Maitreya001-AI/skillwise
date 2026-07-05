---
name: platform-rest-pagination
description: Design list endpoints to the platform team's pagination conventions. Use when adding a collection endpoint, reviewing API designs, or migrating an endpoint from offset to cursor paging.
---

# Pagination — the platform convention

How our APIs page, so clients behave the same against every service.

## The conventions

- Cursor-based paging for any collection that can grow unboundedly; offset paging only for small, bounded lists.
- Cursors are opaque tokens — clients never parse or construct them.
- The sort underlying a cursor is stable and unique (tiebreak on id), or pages can skip and repeat rows.
- Default page size 50, maximum 200; requests above the max are clamped, not rejected.
- The response carries `next_cursor` (null on the last page); clients stop on null, never on a short page.
- Filters and sort order are baked into the cursor; changing them mid-iteration restarts the walk.

## Exit

Before the API review, walk the endpoint's contract against each convention above and note deviations in the design doc.
