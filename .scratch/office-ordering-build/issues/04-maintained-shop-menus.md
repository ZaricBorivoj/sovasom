# 04: Maintain and browse both shop menus

Status: ready-for-agent
Blocked by: [01: Bootstrap and sign into the private office](01-bootstrap-private-office.md)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** A designated menu maintainer maintains both shop menus and office members browse current choices with clear prices and availability.

- [ ] Maintainers can add, edit, reorder, retire and mark items unavailable across the coffee shop and bakery. Ordinary members can browse but cannot mutate menus through UI or API. Use runtime-maintained content; prototype names/items/prices are examples. Initial content belongs to Nemanja.Tomic operationally without hardcoding account privileges.
- [ ] Coffee offers Blend and Specialty with independent prices that may differ; Specialty is selected before adding. Juice, hot chocolate and non-coffee items have no coffee-choice selector. No structured size/milk/other option groups or automatic note surcharges.
- [ ] Prevent new selection of unavailable/retired items. Preserve stable references needed by future snapshot requests and history instead of destructive menu deletion. Corrections are reported outside the app; no correction-reporting workflow.
- [ ] Phone and desktop browse/maintenance views use the shared design system and show the price appropriate to the visible choice. Quantity/request submission is delivered by ticket 06, not a fake saved request.
- [ ] Prove maintainer edit/reorder/availability/retirement and member-visible persistence through Playwright, including denied member mutation and separate choice pricing. Add backend validation and focused accessible coffee-choice/maintenance interactions plus stories for item kinds, availability, validation, loading and failures.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
