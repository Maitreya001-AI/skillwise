---
name: docker-base-images
description: Choose and maintain Docker base images per the org's approved set. Use when writing a Dockerfile, bumping a base image, or when CI flags an image policy violation.
---

# Base images (org policy)

## Facts

- Approved bases live in `registry.corp/base/*` — currently `base/python:3.12-slim`, `base/node:22-slim`, `base/go:1.23`, `base/distroless-cc`; anything from Docker Hub directly fails the admission controller.
- Org bases rebuild weekly with CVE patches; your image inherits fixes by rebuilding, so schedule a weekly rebuild even when your code is untouched.
- `latest` is not a version: pin the org tag (`base/python:3.12-slim-2026w26`) and let the bump bot PR the weekly update.
- Multi-stage builds: the *final* stage must be an approved base; build stages may use anything internal.

## What correct looks like

`FROM` lines reference only `registry.corp/base/*` with week-pinned tags; the bump bot's PR merges within the week (staleness alarms at 21 days); the admission controller log for your namespace is clean.
