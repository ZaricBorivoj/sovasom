# 02: Add colleagues and assign permissions

Status: ready-for-agent
Blocked by: [01: Bootstrap and sign into the private office](01-bootstrap-private-office.md)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** An office administrator adds a colleague, privately hands over a temporary password and assigns office responsibilities; the colleague must choose a personal password before entering the office.

- [ ] Administrator-only account creation requires a display name and unique login email, creates office membership and shows a generated temporary password once for private handoff after identity confirmation outside the app. Existing passwords cannot be retrieved; no SMTP, public registration or invitations are introduced.
- [ ] Temporary passwords expire after 24 hours. Until a personal password is set, authenticated temporary-credential access is restricted to credential setup, not office reads/actions. Successful replacement invalidates the temporary credential and existing sessions; expired credentials show administrator-recovery guidance.
- [ ] Administrators can explicitly grant/revoke equal administrator authority and separate menu-maintainer permission. All current members retain ordinary member capabilities. Initial maintainer rights from bootstrap do not imply every administrator is a menu maintainer.
- [ ] Block demotion of the last administrator atomically, including concurrent demotions. Deny permission-management and account-creation API calls from ordinary members regardless of UI visibility. Keep account emails restricted to holder/administrators.
- [ ] Demo two distinct accounts through the browser from administrator creation to forced password replacement and ordinary-member access. Cover duplicate email, once-only password presentation, exact expiry boundary, direct API authorization and concurrent last-administrator protection with backend/PostgreSQL tests; add focused UI tests and stories for credential handoff, validation and denied/error states.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
