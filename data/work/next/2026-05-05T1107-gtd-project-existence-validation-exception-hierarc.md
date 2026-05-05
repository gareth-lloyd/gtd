---
area: engineering
contexts:
- deep
created: &id001 2026-05-05 11:07:00
defer_until: null
due: null
energy: medium
id: 2026-05-05T1107-gtd-project-existence-validation-exception-hierarc
order: null
project: 2026-04-16T1348-ideas
source_id: null
tags:
- gtd-meta
- backend
time_minutes: 90
title: 'GTD: project-existence validation + exception hierarchy'
updated: *id001
waiting_on: null
waiting_since: null
working_on: false
---

**Problem.** `service.update()` accepts a patch with
`project=<bad-id>` and writes silent garbage — there's no validation
that the referenced project exists. Separately, all validation
errors raise generic `ValueError` and the API blanket-maps every one
to HTTP 400, losing specificity.

**Approach.**
- New module `gtd_core/exceptions.py`:
  ```
  GtdError
    ValidationError
      InvalidContext
      InvalidArea
      InvalidProject
      ImmutableField
    NotFound
      ItemNotFound
      ProjectNotFound
  ```
- Refactor `_validate_patch()` in `gtd_core/service.py` (around
  line 611) to:
  - Check `project` against `repo.list_projects()` if provided
  - Raise specific exceptions instead of `ValueError`
- API `gtd_api/views.py` — map exceptions to HTTP:
  - `InvalidProject` / `InvalidContext` / `InvalidArea` → 422
  - `ProjectNotFound` / `ItemNotFound` → 404
  - Generic `ValidationError` → 400
- Backwards compat: keep `ValueError` raises that aren't validation
  (e.g. immutable id) as-is, or migrate them too — author's call.

**Verification.**
- Backend tests for each new exception type
- API tests for HTTP status mapping
- Run full pytest suite

**Size.** M (~90 min)