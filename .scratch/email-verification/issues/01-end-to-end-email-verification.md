# End-to-end email verification

Status: needs-info
Blocked by: None

## Purpose

Add end-to-end mailbox ownership verification after an SMTP server is selected. Requested during [Office membership and account lifecycle](../../office-ordering/issues/06-office-access.md). This is future implementation backlog, outside the first-version wayfinding destination.

## Current behavior to preserve

The first version uses administrator-created accounts, temporary passwords with private handoff, and administrator-assisted recovery. Email is a login identifier and is not presented as verified. No public signup or office invitations are authorized by this ticket.

## Information needed

- SMTP server/provider, sender identity, environment configuration and secret provisioning. Do not record live credentials here.
- Decide when verification is required for existing/new accounts and changed email addresses, including how accounts with pending verification can access the office.
- Decide whether emailed password setup or self-service recovery should be separate work; neither is automatically included in email verification.

## Intended outcome

- Send verification mail through the chosen SMTP integration with single-use, expiring links tied to the intended account and email address.
- Verify mailbox ownership only after successful confirmation; prevent stale links from verifying a replacement address.
- Cover resend, expiry, already-used/invalid links, email changes, delivery failures and retry behavior without exposing credentials or verification tokens in application logs.
- Preserve administrator-managed membership; verification alone does not grant office access.

## Verification

Add backend tests for verification state and token/error cases, frontend interaction tests and relevant component stories. Add Playwright coverage exercising the frontend, backend, database and a test SMTP mailbox: capture the actual email, follow its link and confirm the resulting account state. Document a smoke check against the selected SMTP service without depending on that external service for every test run.

## Comments

### 23 November 2026 — requested backlog

User requested this follow-up once they determine which SMTP server to use. `needs-info` records the unresolved provider and activation policy; this ticket does not block the first version.
