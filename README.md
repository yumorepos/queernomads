# 🌍 QueerNomads

QueerNomads is a city-intelligence and community-informed platform for queer digital nomads.

It helps people explore, compare, and better understand cities using transparent demo scoring signals (affordability, safety, internet, weather, inclusivity) alongside lived-experience storytelling.

---

## Product Direction

**Positioning:**
> QueerNomads helps queer digital nomads discover, compare, and understand cities through both data and community-informed context.

This repository intentionally avoids becoming a generic ranking clone. The current product balances:
- **City intelligence** for practical planning
- **Community stories** for lived context
- **Trust-first UX** with explicit methodology and confidence labeling

---

## Current Feature Highlights

### City Intelligence
- City discovery page with search, region filtering, minimum score thresholds, and sortable ranking.
- City detail pages with score breakdowns, tradeoff summaries, strengths/limitations, and related cities.
- Demo-data trust signals (confidence labels, last reviewed dates, methodology links).

### Trust & Methodology
- Dedicated `/methodology` page documenting score meaning, confidence levels, interpretation guidance, and limitations.
- Consistent demo/heuristic wording across city surfaces.

### Community Layer
- Story posting and browsing for queer nomad travel experiences.
- Category/rating context and profile-linked authorship.

### Platform Foundations
- Flask application factory + modular blueprints.
- Service layer separation for DB lifecycle, story logic, and city logic.
- Typed city model for future data-source evolution.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Data | SQLite |
| Templates | Jinja2 |
| Styling | Bootstrap 5 + custom CSS |
| Auth | Flask sessions + Werkzeug password hashing |

---

## Architecture Summary

```text
app/
  __init__.py             # application factory, blueprint registration
  routes/
    main_routes.py        # home/auth/profile
    story_routes.py       # post/browse/story
    city_routes.py        # city discovery/detail/methodology
  services/
    db_service.py         # db connection lifecycle + helpers
    story_service.py      # story queries/business logic
    city_service.py       # city seed data + discovery/methodology helpers
  models/
    city.py               # typed city + score metadata contract
    story.py              # story category constants
```

---

## Trust & Data Limitations (Important)

City intelligence currently uses a **seed/demo heuristic dataset** to support product development and UX validation.

That means:
- scores are **directional planning signals**, not authoritative rankings,
- confidence labels are intentionally conservative,
- users should pair results with fresh local research before travel/relocation decisions.

---

## Local Setup

### Prerequisites
- Python 3.10+
- pip

### Install & run

```bash
git clone https://github.com/yumorepos/queernomads.git
cd queernomads
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The app runs at `http://localhost:5000`.

### Optional environment variables
- `SECRET_KEY` (recommended outside local dev)
- `FLASK_DEBUG` (`1` or `0`, defaults to `1` in local run script)

---

## How to Demo This Project

For a recruiter-friendly walkthrough:

1. Open `/` and explain the positioning (city intelligence + community-informed context).
2. Open `/cities` and demonstrate search/filter/sort controls.
3. Open `/cities/lisbon-portugal` and highlight tradeoffs, score breakdown, strengths/limitations, and trust labels.
4. Open `/methodology` and explain confidence levels + current limitations.
5. Open `/browse` to show the community stories layer that complements city intelligence.

This sequence shows the product concept clearly in under 5 minutes.

---

## Validation Commands

```bash
python -m py_compile app.py helpers.py app/__init__.py app/routes/main_routes.py app/routes/story_routes.py app/routes/city_routes.py app/services/db_service.py app/services/story_service.py app/services/city_service.py app/models/city.py app/models/story.py
```

---

## Roadmap (High-level)

Completed:
- strategy docs + architecture assessment
- modular Flask architecture
- city data contract and read-only routes
- discovery/ranking UX
- detail + methodology trust layer
- homepage/product-shell repositioning

Next:
- final consistency cleanup and selective refactors
- optional tests for service-level discovery/methodology logic
- eventual transition from seed data to validated external sources

---

## License

MIT
