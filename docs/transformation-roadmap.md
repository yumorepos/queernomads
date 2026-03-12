# QueerNomads Transformation Roadmap

## Phased Rollout Plan

## Phase 1 — Strategy and Foundation (current)
- Audit repository architecture and UX baseline.
- Create planning docs for positioning, roadmap, and technical assessment.
- Define phased scope-control boundaries.

## Phase 2 — Brand and Homepage Repositioning
- Update layout shell (header/footer/navigation copy).
- Reframe homepage around city-intelligence use cases.
- Preserve mission tone and queer identity while shifting product emphasis.

## Phase 3 — City Data Foundation
- Introduce typed city domain model in backend (and compatible template data contracts).
- Add structured seed city dataset with transparent provenance notes.
- Separate city intelligence data from user-generated story content.

## Phase 4 — Discovery and Ranking Experience
- Implement city listing/discovery route and template.
- Add search, filter, sort controls with deterministic ranking logic.
- Build clear empty states and no-results guidance.

## Phase 5 — City Detail Experience
- Add city detail route and template architecture.
- Include score breakdown modules, best-for tags, and trade-off summaries.
- Add related-city recommendations based on explicit similarity logic.

## Phase 6 — Methodology and Trust Layer
- Add methodology page/section linked from key city pages.
- Explain scoring formulas, input categories, and confidence/limitations.
- Add “sample/seed data” labeling where applicable.

## Phase 7 — Polish, Cleanup, and DX
- Remove dead code and duplicate template sections.
- Improve naming consistency and utility extraction.
- Refresh README and contributor guidance for new product direction.

## What to Preserve
- Existing Flask + SQLite stack for fast iteration and manageable complexity.
- Current community storytelling DNA as a supporting context layer.
- Existing auth flow and session pattern unless hard blockers appear.
- Existing dark/warm visual base and identity cues.

## What to Refactor
- Route/content information architecture to include city intelligence pages.
- Template component duplication (story cards repeated across pages).
- Data modeling beyond stories (city entities and score dimensions).
- CSS organization to support reusable design tokens/components.

## What to Defer
- Advanced personalization/recommendation engine.
- Real-time social interactions.
- Large third-party integrations that increase reliability risk.
- Multi-source data ingestion pipeline automation.

## Recommended Implementation Order
1. Phase 1 docs and architecture decision framing.
2. Layout + homepage repositioning.
3. Typed city model + seed data.
4. Discovery/ranking flows.
5. City detail and related-city logic.
6. Methodology and trust copy.
7. Final cleanup and consistency pass.

## Scope-Control Strategy
- Ship each phase as a coherent vertical slice.
- Require explicit rationale before adding dependencies.
- Prefer extending existing templates/components over broad rewrites.
- Treat V1 community features as context content, not platform expansion.
- Keep scoring logic simple, explicit, and documented.

## Risk Management Notes
- **Risk: Product drift to generic ranking clone**  
  Mitigation: retain queer-first voice and context modules on all city surfaces.
- **Risk: Credibility loss from opaque scores**  
  Mitigation: add methodology transparency and confidence disclaimers.
- **Risk: Maintainability regressions in template-heavy code**  
  Mitigation: introduce reusable partials/macros and reduce duplicated markup.
- **Risk: Over-scope from simultaneous feature streams**  
  Mitigation: enforce phase gates and keep non-goals explicit.
