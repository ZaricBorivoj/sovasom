# 08: Close requests, shop and finish a run

Status: ready-for-agent
Blocked by: [06: Submit a request with preserved item details](06-submit-preserved-request.md)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** The runner adjusts or closes the joining window, uses one consolidated shopping list and ends the run through collection or cancellation; administrators can recover abandoned runs.

- [ ] While accepting requests, the runner may set a new closing time 1–180 whole minutes from now or Close requests now. At the deadline, non-empty runs enter Shopping and empty runs cancel. Shopping cannot reopen. Server authority applies even when the worker or client lags.
- [ ] Consolidate submitted quantities by shop, item, coffee choice and identical note, with expandable colleague contributions. Different notes and choices never merge. Both shops remain distinct and drafts stay excluded.
- [ ] Runner uses one Everything collected action in Shopping, with no per-item/shop verification or return confirmation. Collected ends the lifecycle and immediately releases the slot; a new announcement can succeed while the previous runner is physically returning.
- [ ] Runner or office administrator may cancel either active state with confirmation and optional reason, preserving requests/history and releasing the slot. Other members cannot use these actions. Terminal runs cannot reopen or accept stale mutations.
- [ ] All changes refresh visible shared state and present clear conflict feedback. Provide readable terminal detail that later history and deep links can use; complete paginated history is ticket 09.
- [ ] Demo deadline extension/shortening, early and automatic closure, grouped shopping with contributions, collection, administrator cancellation and immediate next announcement through the full stack. Use PostgreSQL races for request-versus-close/cancel/collect and stale deadline/lifecycle actions. Add focused action/grouping tests and component stories for all lifecycle, confirmation, pending and rejection states.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
