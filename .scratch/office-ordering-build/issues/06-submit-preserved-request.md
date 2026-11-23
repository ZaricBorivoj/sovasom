# 06: Submit a request with preserved item details

Status: ready-for-agent
Blocked by: [04: Maintain and browse both shop menus](04-maintained-shop-menus.md), [05: Announce the office’s single active run](05-announce-active-run.md)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** A member, including the runner, chooses items from both menus and submits one durable request whose selected details remain stable as menus change.

- [ ] Allow one request per colleague/run, quantities as positive whole numbers and optional notes per line. Coffee choices and differing notes remain distinct lines; show displayed prices and estimated total. Include the runner’s own items. Unsubmitted drafts never enter purchased quantities.
- [ ] Submit only for current members strictly before the authoritative deadline. Exactly-at-deadline is too late even if worker transition or screen refresh lags. Validate menu availability, item identity, coffee applicability and current server prices rather than trusting a client-supplied snapshot.
- [ ] Preserve submitted item names, coffee choices and displayed prices as snapshots. Later menu rename/reprice/retirement never deletes, substitutes or silently reprices these lines. Request summary remains readable after reload.
- [ ] Adding requests activates non-empty deadline transition to Shopping while retaining the active slot; request changes are rejected there. Full consolidated shopping/collection is ticket 08. Avoid an intermediate implementation that cancels a populated run as empty.
- [ ] Prove request submission by member and runner, persistence after reload and menu-edit snapshot preservation end-to-end. Test duplicate-request/concurrent submission enforcement and exact deadline races against PostgreSQL, invalid quantities/choices and permissions. Include frontend selection/summary interactions and stories for drafts, notes, choice separation, validation and request-lock/error states.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
