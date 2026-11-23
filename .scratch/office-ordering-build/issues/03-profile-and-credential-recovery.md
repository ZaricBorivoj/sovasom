# 03: Manage profiles and recover credentials

Status: ready-for-agent
Blocked by: [02: Add colleagues and assign permissions](02-colleagues-and-permissions.md)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** Colleagues maintain their profile and password; administrators correct email or reset credentials, and an operator can explicitly recover a locked-out sole administrator.

- [ ] Account holders can edit required display names and change their own passwords. Administrators can change email without changing identity/history; duplicate addresses are rejected. Email is a login identifier and is never presented as mailbox-verified.
- [ ] Password change/reset ends existing sessions. Administrator email changes also end sessions and require a new once-shown, 24-hour temporary password with forced replacement. Recovery guidance points to an administrator who confirms identity outside the app; do not add self-service email recovery.
- [ ] Provide a separately named explicit operator recovery command for sole-administrator lockout. Bootstrap remains a one-time no-op after initialization and cannot be reused as credential reset or privilege escalation. Document operator use without recording live secrets.
- [ ] Central session validation immediately denies revoked credentials across devices, and makes revoked sessions ineligible for future push once delivery is added. Do not trust cached grants or client state.
- [ ] Use full-stack browser workflows for profile change, password change, administrator reset/email correction and old-session denial in a second context. Cover duplicate email, temporary-password expiry, unauthorized changes, identity preservation and explicit operator recovery through application/command tests. Include focused interactions and relevant Storybook states.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
