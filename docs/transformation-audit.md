# QueerNomads Productization Audit & Transformation Plan

## 1. Executive summary
QueerNomads has a strong brand seed and a clear emotional identity, but today it is still a small monolithic CS50 Flask app centered on story posting rather than city decision-making.

The app is good enough to evolve, not throw away. The right move is a **partial restructure in place**: preserve brand language, visual tone, and community story DNA, while re-architecting around city intelligence + decision support.

## 2. Should we evolve or partially rebuild?
**Recommendation: B) Carefully restructure while preserving identity.**

Why:
- Keep: brand, dark/rainbow design cues, storytelling concept, auth/profile foundation.
- Rebuild: app structure, data model, page architecture, and product framing.

A full rewrite would risk momentum loss and identity drift; pure in-place incremental edits in the current single-file architecture will quickly become fragile.

## 3. Current repo strengths
- Distinct identity already exists (inclusive voice + queer travel framing).
- Simple auth, profile, and content flow are functional and understandable.
- Theme system has a coherent style baseline and recognizable visual character.
- Lightweight stack (Flask + SQLite + server-rendered templates) is fast to iterate for MVP.

## 4. Current repo weaknesses
- **Architecture debt:** almost all application logic is in `app.py`, limiting scale and testability.
- **Data model mismatch:** there are no first-class `cities`, `city_scores`, `methodology`, or comparison entities.
- **Product mismatch:** IA is currently “story feed app,” not “city intelligence platform.”
- **Limited filtering/ranking:** browse page only supports free-text + one category.
- **Hard-coded config/security issues:** static secret key and init-on-import patterns are not production-safe.
- **No service boundaries:** retrieval, scoring, ranking, and content are coupled in route handlers.

## 5. Recommended product direction
Reposition around 3 linked layers:

1. **Community layer:** keep stories, but tie them to cities and topics (safety, belonging, dating, cost, visas, etc.).
2. **City intelligence layer:** introduce city cards, scoring dimensions, ranking/discovery, city detail analytics.
3. **Decision layer:** add filters, persona-based “best for,” compare flow, and transparent methodology.

Tone: mission-led, practical, and evidence-aware. Not a “top 10 cheap cities” clone.

## 6. Recommended information architecture
### Routes / pages
- `/` Home (value proposition + featured cities + recent community insights)
- `/cities` Discovery & rankings (sortable/filterable city intelligence)
- `/cities/<slug>` City detail (scores, tradeoffs, stories, practical guidance)
- `/compare` Multi-city comparison workspace
- `/methodology` Transparency page for scoring and confidence
- `/community` Curated insight feed (stories/guides/tips)
- `/community/<story-slug>` Story detail
- `/profile/<id>` Contributor profile

### Core UI sections
- Hero + decision CTA
- “Best for” quick selectors
- City score cards with dimension breakdown
- Tradeoff panel (“great nightlife, weaker affordability”)
- Insight snippets sourced from community stories
- Methodology confidence tags (high/medium/low confidence)

### Main data entities
- `City` (slug, country, region, baseline metadata)
- `ScoreDimension` (safety, affordability, community, internet, healthcare, legal climate, etc.)
- `CityScore` (city + dimension + value + source + updated_at + confidence)
- `CitySnapshot` (aggregated metrics/materialized read model)
- `Story` (linked to city + theme tags + sentiment facets)
- `MethodologyNote` (dimension definitions, weighting logic)
- `ComparisonSet` (saved user comparison state; optional later)

### MVP boundaries vs later
- **MVP:** discovery, city detail, compare (2–4 cities), methodology, lightweight community tie-ins.
- **Later:** saved plans, personalization, contributor reputation, moderation tooling, richer social graph.

## 7. Recommended technical architecture
### Keep / improve stack
- Keep Flask + Jinja + SQLite for now (portfolio-friendly and shippable).
- Restructure into packages:
  - `app/__init__.py` app factory
  - `app/routes/` blueprints (`auth`, `community`, `cities`, `compare`, `methodology`)
  - `app/services/` scoring + ranking + recommendation logic
  - `app/repositories/` SQL access layer
  - `app/templates/`, `app/static/`
  - `instance/` runtime DB and config

### Data strategy
- `data/seed/` for curated mock city intelligence inputs.
- separate tables for normalized city data + scoring records.
- create a deterministic aggregation step producing `city_snapshots` for fast UI reads.

### Extensibility model for city intelligence
- Dimensions are config-driven (not hard-coded in templates).
- Weight sets can be scenario-based (“best for remote work”, “best for nightlife + safety balance”).
- Every displayed score carries metadata: source_count, last_updated, confidence.

## 8. Phased roadmap
### Phase 1 (highest priority)
- Reframe IA and navigation around city discovery + comparison.
- Add first-class city domain model and seed dataset.
- Ship `/cities`, `/cities/<slug>`, `/compare`, `/methodology`.
- Keep existing stories but attach them to city pages as “community insights.”

### Phase 2
- Improve ranking engine and filter depth.
- Add “best for” presets and weighted scoring controls.
- Add source/confidence UI and richer tradeoff messaging.

### Phase 3
- Contributor workflows (guided submissions, insight quality controls).
- Save comparisons/plans for logged-in users.
- Add quality moderation and lightweight trust signals.

## 9. Phase 1 implementation plan
1. **Refactor foundations**
   - Introduce Flask app factory + blueprints.
   - Move DB access into repository helpers.
2. **Introduce city intelligence schema**
   - Add tables: `cities`, `score_dimensions`, `city_scores`, `city_snapshots`, `story_city_links`, `methodology_notes`.
   - Migrate existing `stories.destination` into linked city references where possible.
3. **Build city discovery page**
   - Filter panel (region, affordability, safety minimum, community strength).
   - Ranked city cards with 4–6 key dimensions.
4. **Build city detail page**
   - Dimension grid, tradeoff summary, practical notes, linked community stories.
5. **Build compare flow**
   - Select 2–4 cities and compare dimensions side-by-side.
6. **Build methodology page**
   - Explain dimensions, weighting defaults, confidence logic, limitations.
7. **Polish UX**
   - Upgrade type scale, spacing system, card hierarchy, and chart primitives.
8. **Validation**
   - Add route tests + service tests for ranking calculations.

## 10. Risks and anti-patterns to avoid
- Turning this into a generic nomad leaderboard with no queer-specific context.
- Overbuilding social mechanics before decision support is solid.
- Hard-coding dimensions and weights in templates.
- Showing single-number city scores without confidence/source transparency.
- Expanding data scope too fast (many cities, poor quality).
- Leaving architecture monolithic; velocity will collapse by Phase 2.
