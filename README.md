# 🌍 QueerNomads

QueerNomads is a community + city intelligence platform for queer digital nomads.

## Phase 1 Product Surfaces
- `/cities` — ranked discovery hub
- `/cities/<slug>` — city intelligence + community tie-in
- `/compare` — side-by-side comparison for 2–4 cities
- `/methodology` — scoring transparency
- `/community` — stories and lived insights

## Stack
- Flask + Jinja
- SQLite
- Bootstrap + custom dark theme

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
