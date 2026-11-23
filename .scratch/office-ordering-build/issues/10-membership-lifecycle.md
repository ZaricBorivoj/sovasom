# 10: Leave, remove and restore office membership

Status: ready-for-agent
Blocked by: [02: Add colleagues and assign permissions](02-colleagues-and-permissions.md), [07: Edit and withdraw requests before closing](07-edit-withdraw-request.md), [09: Record unavailable quantities and inspect history](09-unavailable-outcomes-history.md)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** A member leaves or an administrator removes/restores membership with immediate, consistent effects on access and any active run or request.

- [ ] Confirmed self-departure and administrator removal immediately revoke office access on all devices. The account survives without office access; preserve earlier attribution/history. Recheck current membership on every operation rather than trust a still-present cookie.
- [ ] If the departing person runs an active run, warn and cancel the run atomically with removal, preserving history and freeing the slot. Another departing participant’s request is withdrawn while accepting requests but preserved in Shopping. Apply authoritative effective state when departure races with closing.
- [ ] Block removal/departure of the last administrator, including concurrent demotion/removal/departure operations. Ordinary members cannot remove or restore colleagues.
- [ ] Administrator restoration reuses the existing account but does not restore old requests or administrator/menu-maintainer grants automatically. Access loss is a delivery eligibility boundary for notification tickets, not permission to keep notifying a former member.
- [ ] Demo leave/removal/restoration in multiple browser contexts and inspect preserved/withdrawn requests/history. PostgreSQL tests prove atomic active-run cancellation, departure-versus-closing behavior and last-administrator races. Add access-loss/confirmation/restoration UI tests and stories.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
