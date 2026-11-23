# Postcard Club — selected frontend prototype

The user approved the refined Postcard Club prototype, including the active-run and past-run layout. See [Explore and choose the frontend direction](../issues/03-visual-direction.md#answer) for the canonical decision, confirmed requirements, compatible design-system approach and unresolved details.

From the repository root:

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory .scratch/office-ordering/prototype
```

- Selected preview: http://127.0.0.1:4173/frontend-prototype.html?variant=C
- Empty-state / announcement example: http://127.0.0.1:4173/frontend-prototype.html?variant=C&demo=empty
- Archived comparison: http://127.0.0.1:4173/frontend-comparison-prototype.html?variant=C

The selected preview defaults to Postcard Club, with one active run, quieter completed summaries below, coffee-specific Blend / Specialty controls, juices/hot chocolate without those controls, duration chips and whole-run collection. The design switcher is removed from the selected preview. The footer scenario links reset in-memory sample data; they are prototype controls, not application navigation.

Coffee quantities are held separately for each item and choice. Adding both blend and specialty preserves both, and shopping consolidation groups only matching choices. Blend preselection and equal example prices are illustrative. All quantities and announcements reset on reload. The sample 15-minute countdown is fixed, not a live clock.

## Verification — 20 November 2026

Ad hoc Playwright checks passed at 390px and 1440px:

- Exactly one active postcard with two completed summaries.
- Active-run announcement guard, including after creating a run from the empty scenario.
- No active run in the empty scenario; announce a generated-title run with a five-minute duration.
- Exact chips: 5, 10, 15, 30 minutes.
- Three coffees each have native Blend / Specialty radio controls; Orange juice and Hot chocolate have none.
- Add both choices of flat white, juice and hot chocolate; submit; verify distinct flat-white choices and consolidated quantities in the runner list.
- One-click collection with no individual item checkboxes.
- All five screens fit without horizontal overflow. The mobile menu was also checked before collection.
- No JavaScript page errors during workflow checks.

Visually inspected home at phone and desktop sizes and menu controls at phone size.

This is a standalone throwaway HTML prototype with sample data. There are no real accounts, notifications, backend or persistence. Production Storybook, frontend/backend unit suites and integrated frontend/backend/database E2E infrastructure do not exist yet and could not be run. No production code was implemented or promoted. Earlier alternatives remain in the local comparison archive because the repository lacks an initial commit and remote for branch publication.
