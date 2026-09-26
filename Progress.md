# 📝 Development Log — Event Registration Portal

Tracking progress across sessions for continuity if tools/systems change.

---

## Session 1 — Environment & Foundation

**Date:** Sep 25, 2026

**Completed:**

- Cloned empty repo, set up local dev environment
- Created isolated `venv`, fixed PowerShell execution policy (`RemoteSigned`) to allow venv activation
- Wrote `requirements.txt` (flask, gunicorn, pytest, flake8)
- Configured `.gitignore` (venv/, __pycache__/, .pytest_cache/)
- Built minimal `app.py` skeleton with `/health` endpoint
- Verified `/health` returns `{"status": "ok"}` locally
- Committed and pushed

**Key decision:** Built `/health` first — not a throwaway warm-up, it's the exact endpoint Render polls later to confirm the deployed app is alive.

---

## Session 2 — Core Logic (Phase 1)

**Completed:**

- Defined `EVENTS` data model — in-memory list of dicts (`id`, `name`, `seats_total`, `seats_left`)
- Built `GET /api/events` — returns full event list as JSON
- Built `POST /register/<event_id>` — decrements seats, with proper status-code separation:
  - `200` — successful registration
  - `400` — event exists but full (business rule rejection)
  - `404` — event ID doesn't exist (client addressing error)
- Wrote 4 pytest tests: health check, successful registration, blocked-at-zero, not-found
- Fixed flake8 `W292` warnings (missing newline at EOF) on both files
- All 4 tests passing, flake8 clean
- Committed and pushed

**Key decision:** In-memory data store is deliberate, not a shortcut — assignment scope doesn't require persistence across restarts. A database here would add complexity (connections, migrations, credentials) without a corresponding requirement.

**Logical breakthrough:** Understood why `next(generator, None)` beats a list comprehension for single-item lookup — short-circuits at first match instead of building the full filtered list first.

---

## Session 3 — CI/CD Pipeline (Phase 2)

**Completed:**

- Created `.github/workflows/ci.yml` — runs flake8 + pytest on every push/PR to `main`, on a clean Ubuntu VM
- Verified: pushed to GitHub, watched Actions tab go green
- Created Render account (via GitHub OAuth)
- Connected repo, configured Web Service:
  - Build command: `pip install -r requirements.txt`
  - Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
  - Instance type: Free
- Deployed successfully on first attempt — no debugging needed
- Verified both `/health` and `/api/events` live at:
  `https://event-registration-portal-ygqa.onrender.com`

**System bottleneck identified (not a bug):** Render free-tier spins down after ~15 min idle. First request after that takes 30–50s to cold-start the container (fresh clone → build → gunicorn start) before responding. Documented in README as a known limitation, not something to "fix" in code.

**Key decision:** `--bind 0.0.0.0:$PORT` is required, not optional — Render injects `$PORT` dynamically and expects the app to bind to it; a hardcoded port would deploy "successfully" but the URL would time out.

---

## Session 4 — Documentation Polish

**Completed:**

- Wrote comprehensive `README.md`: overview, architecture, tech stack, full API reference, local setup, testing, CI/CD explanation, design-decision rationale, known limitations, project structure
- Upgraded visual presentation:
  - Added `for-the-badge` style shields.io badges (Python, Flask, Tests, CI, Render)
  - Replaced fragile ASCII architecture diagram with a native GitHub-rendered **Mermaid flowchart**
  - Fixed a broken code-fence (Project Structure tree collapsed into one line — missing triple-backtick wrapper)
  - Corrected Python badge coloring (`306998` background + `FFD43B` logo) to match Python's actual brand palette instead of a flat white-on-dark silhouette
- Committed and pushed

---

## Session 5 — Frontend Build

**Completed:**

- Created `templates/index.html`, added `render_template()` route for `/`
- Built event cards UI: live seat counts, progress bars, open/full badges
- Wired to real backend — `fetch('/api/events')` on load, `fetch('/register/<id>', {method: 'POST'})` on registration
- Added confirmation modal before registering, loading spinner on the button during the request, toast notifications for success/error
- Expanded `EVENTS` from 2 to 6 entries (kept IDs 1 and 2 unchanged — pinned by existing tests)
- Visual polish pass: Inter font, custom color theme, card hover states, animated progress bar transitions
- Added a live stats summary bar (total events, total seats, seats remaining) and an empty-state fallback for zero events
- Fixed a JS bug where `renderStats` was defined but never called (function existed, nothing invoked it — no console error, just a silently empty stats bar)

**Key decision:** Frontend is a thin client only — it holds no state of its own and always re-fetches from `/api/events` after every action, so the UI can never drift from actual server state.

**Logical breakthrough:** Learned to catch "defined but never called" bugs — the most dangerous kind since there's no error, just missing behavior. Fix: check every function invocation against its definition, not just that the code runs without crashing.

## Current State

| Component              | Status                       |
| ---------------------- | ---------------------------- |
| Core API (3 endpoints) | ✅ Done                      |
| Tests (4/4)            | ✅ Passing                   |
| Lint (flake8)          | ✅ Clean                     |
| CI pipeline            | ✅ Live, green on every push |
| Deployment             | ✅ Live on Render            |
| Frontend               | ✅ Done, polished            |
| README                 | ✅ Complete, polished        |

---

## Upcoming / Not Started

None — project scope complete.

---

**Last updated:** Sep 26, 2026
