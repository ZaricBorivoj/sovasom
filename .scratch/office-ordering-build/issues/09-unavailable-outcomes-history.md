# 09: Record unavailable quantities and inspect history

Status: ready-for-agent
Blocked by: [08: Close requests, shop and finish a run](08-shop-and-finish-run.md)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** The runner records unfulfilled quantities without overwriting original requests, and current office members can review completed and cancelled runs with accurate outcomes.

- [ ] In Shopping the runner may record all or part of a requested quantity as unavailable, bounded to that request line’s original quantity. Preserve original quantities, snapshots and affected-colleague attribution; do not substitute items or alter maintained menu availability.
- [ ] Each affected colleague sees original request and unavailable outcome together. Consolidated shopping and Everything collected preserve unfulfilled quantities explicitly instead of declaring every requested item obtained. These outcomes support private completion wording later.
- [ ] Office runs shows the latest ten collected/cancelled summaries below the active run with Load more. Current members can view retained run dates, requests, cancellation reasons and outcomes; former/non-members cannot. Retain history rather than pruning it in this version.
- [ ] Demo partial/full unavailable outcomes, collection, cancellation, pagination and details after reload through Playwright. Test invalid quantities, actor/state restrictions, grouping and unchanged original snapshots with backend/PostgreSQL coverage; include relevant outcome/history component interactions and stories, empty/loading/error and phone layout states.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
