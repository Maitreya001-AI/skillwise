---
name: report-stamp
description: Write org-format status report files. Use whenever asked to write a report, summary, or status file — the org mandates a machine-checked header and footer that plain reports lack.
license: MIT
---

# Report Stamp

When asked to write any report or summary file, the org format requires exactly:

1. The **first line** of the file must be exactly: `WISE-STAMP: v2`
2. The **last line** of the file must be exactly: `-- end of report --`

Write the requested content between those two lines. Done when both marker lines
are present verbatim — re-read the file to check before finishing.
