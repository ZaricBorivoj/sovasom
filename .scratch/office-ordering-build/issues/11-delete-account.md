# 11: Delete an account while preserving shared history

Status: ready-for-agent
Blocked by: [10: Leave, remove and restore office membership](10-membership-lifecycle.md)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** After confirming an account holder’s request, an administrator irreversibly deletes their personal account data without destroying shared run history.

- [ ] Expose a separate administrator-assisted deletion with explicit confirmation after the account holder’s request is confirmed. Apply membership-removal and active-run effects first within a consistent operation; block deletion of the last administrator.
- [ ] Delete credentials, email, display name, preferences and any device registrations. Remove identifying run/request attribution and display Deleted colleague. Retain shared run/item/quantity/outcome history, and clear free-text notes from that person’s requests.
- [ ] Old sessions cannot access office data or qualify for future push. A later account, including one with a reused email, has no link to the deleted identity, requests or former grants. Membership removal alone must continue retaining named history.
- [ ] Prove deletion, active-run handling, anonymized history, note erasure and inaccessible old sessions through full-stack tests; use application/PostgreSQL tests for last-administrator and concurrent access boundaries. Include deletion confirmation, irreversible outcome and denial/failure UI tests/stories. Later notification persistence must preserve these erasure rules.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
