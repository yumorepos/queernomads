# 🌍 QueerNomads

[![CI](https://github.com/yumorepos/queernomads/actions/workflows/ci.yml/badge.svg)](https://github.com/yumorepos/queernomads/actions/workflows/ci.yml)


QueerNomads is a queer-first analytics product demo for digital nomads choosing where to live, work, and belong.

It combines:
- **structured city scoring** (across six dimensions),
- **preset ranking modes** for different priorities,
- **side-by-side comparison**, and
- **community perspective** from lived-experience stories.

The goal is practical: help users make better relocation and travel decisions with clear tradeoffs, not vague hype.

---

## Why this project exists

Most “best city” lists flatten complex decisions into a single score. For queer travelers, the real decision surface includes safety, social belonging, and local community context alongside affordability and remote-work quality.

QueerNomads is built to show that decision process explicitly:
- transparent dimensions,
- adjustable preset priorities,
- readable strengths/tradeoffs,
- and methodology disclosures.

---

## Product walkthrough

### Core surfaces
- `/` — landing page + featured cities + guided demo flows
- `/cities` — ranked city discovery with filters and presets
- `/cities/<slug>` — city intelligence brief with **radar chart** + evidence bars
- `/compare` — compare 2–4 cities with row-level winners
- `/methodology` — model explanation, caveats, and confidence framing
- `/community` — qualitative stories linked to places

### Guided demo flows (recruiter-friendly)
- ` /compare?city=berlin&city=lisbon `
- ` /cities?preset=best_for_community `
- ` /cities?preset=balanced&cost_level=medium&sort=score_desc `

These routes are intentionally prefilled so reviewers can understand the product in under a minute.

---

## Feature highlights

- **City intelligence model** across six dimensions:
  - affordability
  - safety
  - inclusivity
  - internet quality
  - livability
  - community potential
- **Preset ranking modes**:
  - balanced
  - best_for_remote_work
  - best_for_community
- **Snapshot/read model** for fast ranked list rendering
- **Visual decision support**:
  - radar chart on detail pages
  - score bars + comparison table bars
- **Community context layer** with story linking to city briefs
- **Premium dark UI** tuned for portfolio/demo quality

---

## Screenshots

Add current screenshots here (recommended names):
- `docs/screenshots/homepage.png`
- `docs/screenshots/cities.png`
- `docs/screenshots/city-detail-radar.png`
- `docs/screenshots/compare.png`
- `docs/screenshots/methodology.png`

> The app includes guided scenarios and visual analytics intended to be shown in sequence during demos.

---

## Scoring + preset system

Dimension scores live in seeded data and are weighted by preset definitions.

At runtime:
1. base dimension scores are loaded per city,
2. preset weights are applied,
3. weighted values are normalized to 0–100,
4. strengths/tradeoffs are derived from top/bottom dimension signals,
5. results are materialized into `city_snapshots` for read performance.

This keeps ranking logic deterministic and auditable while preserving fast page loads.

---

## Architecture overview

### App structure
- `app/routes/*` — Flask blueprints and route handlers
- `app/repositories/*` — data access + read shaping
- `app/services/*` — business logic (scoring, presets, filters, comparison, snapshots)
- `app/templates/*` — server-rendered Jinja views
- `app/static/style.css` — premium UI theme

### Data flow (high level)
1. SQL migrations apply schema changes.
2. Seed payloads load city/dimension score data.
3. Snapshot service recalculates preset scores + strengths/tradeoffs.
4. Routes query repositories that read from city + snapshot tables.

---

## Data model overview

Primary tables:
- `cities`
- `score_dimensions`
- `city_scores`
- `city_snapshots` (read model)
- `methodology_notes`
- `stories`
- `users`
- `schema_migrations`

The `city_snapshots` table stores computed preset outputs to keep ranked list and card rendering simple and fast.

---

## Local setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

App runs on `http://127.0.0.1:5000` by default.

---

## Configuration

Environment-driven config is defined in `app/config.py`.

Common vars:
- `SECRET_KEY`
- `DATABASE_PATH`
- `FLASK_ENV`

If `.env` is absent, development-safe defaults are used.

---

## Migrations + seed pipeline

- SQL migrations: `migrations/*.sql`
- Applied migration tracking: `schema_migrations`
- Initialization automatically performs:
  - migration apply,
  - seed upsert,
  - snapshot rebuild.

Manual command:

```bash
flask --app run.py migrate
```

---

## Testing

```bash
pytest
```

Current tests cover:
- core route rendering,
- filtering/preset behavior,
- compare input normalization,
- migration application,
- snapshot population.

---

## Roadmap / future improvements

- user-adjustable custom weighting UI (beyond fixed presets)
- richer confidence and recency metadata per dimension
- locale-aware cost and visa overlays
- saved comparison briefs for signed-in users
- lightweight chart image export for sharing

---

## Portfolio positioning

QueerNomads is designed to demonstrate:
- pragmatic Flask architecture,
- data modeling + migration discipline,
- analytics UX clarity,
- and product storytelling tuned for real reviewer walkthroughs.
