---
name: sql-review-bar
description: Judge committed SQL against this team's review bar. Use when writing or reviewing analytics queries, dbt models, or any SQL headed for the shared repository.
---

# SQL review bar

What the data team holds committed SQL to at review time.

## The bar

- Keywords uppercase, identifiers lowercase; one clause per line for anything beyond a one-liner.
- No `SELECT *` in committed queries — name the columns; a model's contract is its column list.
- Aliases are words, not letters: `orders o` fails review, `orders ord` passes.
- Beyond two levels of nesting, restructure as CTEs; each CTE named for what it holds, not `t1`/`t2`.
- Every JOIN carries its condition explicitly; implicit cross joins and USING-clause shortcuts fail review.
- Magic constants get a comment or a reference table; a bare `WHERE status = 3` fails review.

## Exit

At PR review, read the query against each line of the bar; request changes with the violated line quoted.
