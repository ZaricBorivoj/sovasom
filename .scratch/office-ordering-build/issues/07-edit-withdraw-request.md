# 07: Edit and withdraw requests before closing

Status: ready-for-agent
Blocked by: [06: Submit a request with preserved item details](06-submit-preserved-request.md)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** A colleague can change or withdraw their own submitted request while it is open without losing saved prices or accidentally increasing unavailable selections.

- [ ] Only the request owner may edit/withdraw strictly before closing. Other members and the runner cannot edit another colleague’s request. Shopping requests lock; stale actions get a clear rejection and current state.
- [ ] Quantity/note edits to a saved line retain its original submitted name, choice and displayed price. Added/replaced items use current menu information and pricing. Preserve different notes/coffee choices and recompute the estimated total from the applicable snapshots.
- [ ] Visibly flag saved lines whose items become unavailable. Permit reduction/removal but no increase; unavailable/retired selections cannot be newly added. Never silently delete, substitute or reprice because a menu changed.
- [ ] Withdrawal excludes the saved contribution from the shopping list and future submitted-request audiences. A later valid submission is still at most one request for the member/run. Do not treat a local draft as submitted.
- [ ] Playwright covers edit/withdraw/re-submit, menu changes and unavailable restrictions through reload. PostgreSQL integration proves request edits/withdrawal racing with deadline/transition cannot leak late changes. Add business validation, focused editing interactions and stories for preserved-price, flagged, locked, conflict and error states.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
