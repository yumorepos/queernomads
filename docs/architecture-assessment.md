# QueerNomads Architecture Assessment

## Current Repository Snapshot
Current implementation is a monolithic Flask app with:
- single `app.py` containing route handlers, DB lifecycle, and startup logic
- SQLite schema with `users` and `stories`
- server-rendered Jinja templates for all pages
- one global stylesheet with shared tokens and component styling

This is a strong baseline for iterative product transformation, but requires structure improvements for a city-intelligence-first roadmap.

## Repo Strengths
- **Simple, understandable stack:** Flask + SQLite + Jinja keeps cognitive load low.
- **Working auth/story foundations:** registration/login/profile/story CRUD path exists.
- **Input validation basics:** several server-side checks are in place.
- **Early design system signals:** CSS variables and reusable visual motifs already exist.
- **Mission-aligned branding:** copy and palette already center queer identity.

## Repo Weaknesses
- **Monolithic backend structure:** route logic, DB concerns, and app bootstrap are tightly coupled in `app.py`.
- **No city domain model:** current schema and routes are stories-centric only.
- **Template duplication:** story card patterns are repeated across home/browse/profile templates.
- **Limited information architecture:** no route structure for discovery/ranking/detail/methodology city flows.
- **Hard-coded configuration:** secret key and database path are inline and non-environmental.

## Maintainability Risks
1. **Scalability risk in `app.py`:** adding city intelligence features into one module will increase coupling and regression risk.
2. **Data consistency risk:** if city scores are introduced ad hoc in templates, logic can become fragmented and untestable.
3. **Styling drift risk:** current global CSS can accumulate page-specific one-offs without component boundaries.
4. **Trust/compliance risk:** safety-related content can appear overly authoritative if confidence and limitations are not codified.

## Styling and Design Inconsistencies
- Strong visual base exists, but there is no componentized style architecture for cards, score blocks, filter controls, and metadata panels.
- Typographic hierarchy is acceptable but not yet editorial-grade for long-form city intelligence pages.
- Navigation labels and homepage copy still frame product mainly as story-sharing, not decision support.

## Data/Modeling Gaps
- No tables or structured models for city-level data dimensions.
- No explicit schema for score categories (e.g., affordability, safety, internet, weather, inclusivity, lifestyle fit).
- No fields for source metadata, confidence labeling, or last updated timestamps.
- No clear contract for ranking logic inputs/outputs.

## Routing/Page Structure Issues
Current routes: home, auth, story posting/browsing, individual story, profile editing.
Missing for target V1:
- city discovery/ranking route
- city detail route(s)
- methodology/trust route
- potential compare/shortlist route (optional post-V1)

## Evolve in Place vs Refactor First
**Recommendation: evolve in place with targeted refactoring.**

Rationale:
- Existing app is small enough to extend rapidly without full rewrite.
- A controlled modularization pass (blueprints/services/models-like separation) can happen incrementally.
- Full rewrite would consume velocity before user-visible product progress.

## Recommended Technical Approach
1. **Stabilize app structure before major feature growth**
   - Introduce lightweight module boundaries (e.g., `routes/`, `services/`, `data/`).
2. **Define city domain contract early**
   - Add typed Python structures (dataclasses or TypedDict) for city records and score dimensions.
3. **Build reusable template primitives**
   - Create shared partials/macros for cards, badges, score bars, and metadata rows.
4. **Separate ranking logic from templates**
   - Keep filter/sort/scoring functions in service utilities to improve testability.
5. **Add trust instrumentation**
   - Include explicit labels and methodology links wherever scores are rendered.
6. **Incremental testing strategy**
   - Start with deterministic unit-level checks for ranking/filter helpers and smoke-route tests.
