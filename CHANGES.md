# Changes

* I've never worked with Svelte before, took some time for reading about it
* The task "improve the styling/ui/ux flow" is a bit vague, i've implmented a few tweaks on my taste

This document summarizes all changes grouped by category.

## Architecture
- Backend project structure cleanup
  - Database engine/session and table initialization extracted to `be/db.py`.
  - Domain models and API schemas extracted to `be/models.py`.
- Configuration via environment variables
  - Backend: `CORS_ORIGINS`, `DATABASE_URL` (see `be/main.py`, `be/db.py`).
  - Frontend: `PUBLIC_API_BASE_URL` (see `fe/src/lib/config.ts`, `.env.example`).
- API versioning introduced under `/v1` to permit non‑breaking evolutions (`be/main.py`).
- Visitor tracking feature
  - New lightweight events endpoint `POST /v1/events` to accept future analytics events; currently handles `object: "question"` and increments the question’s `visits` counter (`be/main.py`).
  - Dedicated stats endpoint `GET /v1/questions/{id}/stats` to read visits (`be/main.py`).
  - Frontend logs a visit to the answer page on mount (`fe/src/routes/questions/[id]/+page.svelte`).

## Semantic Improvements
- Resource naming and routing
  - Plurals for collections (e.g. `questions`) and nested resources for clarity (`/v1/questions/{id}/answers`).
- List response shape standardized
  - Lists return `{ count, results }` to communicate total items and support offset/limit pagination (`/v1/questions`, `/v1/questions/{id}/answers`).
- Separate input/output models
  - Introduced DTOs for create/read to avoid leaking internal fields and to keep payloads minimal (`be/models.py`).
- Frontend route structure mirrors the API
  - Answers and stats are nested under a question: `/questions`, `/questions/[id]`, `/questions/[id]/stats`.
- Navigation IA
  - Removed the redundant “Answers” top‑level entry; answers live under a specific question (`fe/src/routes/Header.svelte`).

## Bug Fixes
- Enable CORS on the backend
  - Without CORS, browser POST/OPTIONS requests failed; added middleware configured via `CORS_ORIGINS` (`be/main.py`).
- Safer answer creation
  - `POST /v1/questions/{id}/answers` now validates that the question exists and automatically binds the `question_id` (`be/main.py`).
- Server‑side filtering
  - Frontend no longer filters answers client‑side; the backend returns only the requested question’s answers (`be/main.py`, `fe/src/routes/questions/[id]/+page.svelte`).

## Misc
- Documentation
  - Rewrote backend README with setup, API examples (`be/README.md`).
  - Rewrote frontend README with setup, config, testing (`fe/README.md`).
- UI/UX touches
  - Display the question text above its answers and on the stats page to provide context (`fe/src/routes/questions/[id]/+page.svelte`, `fe/src/routes/questions/[id]/stats/+page.svelte`).
  - Minor style and content tweaks to improve clarity and flow.
