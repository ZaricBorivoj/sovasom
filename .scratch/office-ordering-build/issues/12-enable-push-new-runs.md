# 12: Enable device push and receive new-run notifications

Status: ready-for-agent
Blocked by: [03: Manage profiles and recover credentials](03-profile-and-credential-recovery.md), [05: Announce the office’s single active run](05-announce-active-run.md)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** A colleague optionally enables notifications on each device, manages account-wide categories and receives privacy-preserving new-run pushes through durable delivery.

- [ ] Provide explicit Enable notifications and iOS Home Screen guidance, manifest/app identity/icons and a same-origin service worker compatible with the researched original Web Push baseline. Request permission only after the user gesture. Unsupported/denied/revoked states preserve full app use without repeated prompts; no email/SMS fallback.
- [ ] Show three account-wide category controls, initially selected when push is enabled: New runs, Closing reminders, Updates to runs I joined. Distinguish category settings from per-device/session delivery status. Changes affect future delivery without replay; later tickets activate the other event types.
- [ ] Register subscriptions with authenticated account/session ownership; store endpoint/encryption material server-side. Send new-run events to all eligible enabled devices of current members except the runner, subject to current category/access/session checks. Logout, expiry, credential revocation or membership loss stops future delivery; account deletion must erase newly introduced personal data.
- [ ] Write notification intent with the announcement business transaction into PostgreSQL. Implement durable worker claims/recovery, bounded useful retries/TTL, stale-event suppression and invalid/expired endpoint cleanup. Use encrypted standards-based push/VAPID with private keys server-side and a replaceable external transport. Do not promise exactly-once external dispatch or guaranteed receipt.
- [ ] Lock-screen messages include only permitted run/runner/event/time information, never request items, notes or prices. Taps load current run state and recheck access. Original Web Push remains visibly displayed even in foreground; deduplicate supplementary in-app notices.
- [ ] Integrated Playwright exercises preferences, subscription ownership, new-run audience and multi-session revocation with real PostgreSQL/worker and a recording transport only. Test atomic outbox creation, crash/claim recovery, retry expiry, stale/invalid endpoints and category changes; include denied/unsupported/enabled/expired UI states and stories. Real Apple delivery evidence is reserved for ticket 18, not inferred from WebKit.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
