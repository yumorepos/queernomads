# 🌍 QueerNomads

QueerNomads is a **community + city intelligence** platform for queer digital nomads.

It combines lived community insight with a structured city scoring system so users can discover, compare, and evaluate relocation/travel tradeoffs.

## Product surfaces
- `/` — mission-led homepage with featured city intelligence
- `/cities` — city discovery hub with ranking presets and filters
- `/cities/<slug>` — city intelligence brief + linked community insights
- `/compare` — side-by-side city comparison (2–4 cities)
- `/methodology` — scoring model + preset philosophy + limitations
- `/community` — story feed and local insight contributions

## City intelligence model
### Core entities
- `cities`
- `score_dimensions`
- `city_scores`
- `city_snapshots` (read model)
- `methodology_notes`
- `stories` (optionally linked to cities via `city_id`)

### Ranking presets
- `balanced`
- `best_for_remote_work`
- `best_for_community`

Preset logic is deterministic and service-driven (`app/services/ranking_presets.py`, `app/services/city_scoring.py`).

## Tech stack
- Flask + Jinja templates
- SQLite
- Bootstrap + custom dark theme
- Pytest

## Configuration
Configuration is environment-based (`app/config.py`).

Supported environment variables:
- `SECRET_KEY`
- `DATABASE_PATH`
- `FLASK_ENV`

### Local setup
```bash
cp .env.example .env
# edit .env as needed
```

If no `.env` is present, safe development defaults are used.

## Migrations (Phase 1.5)
A lightweight SQL migration system is included.

- Migration scripts live in `migrations/*.sql`
- Applied versions are tracked in `schema_migrations`
- App startup applies migrations, seed data, and rebuilds city snapshots
- You can also run explicitly:

```bash
flask --app run.py migrate
```

## Run locally
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Tests
```bash
pytest
```

## Notes for reviewers
This project intentionally focuses on **decision-support quality** over breadth. Scores are directional guidance for queer nomads, not universal objective truth.
