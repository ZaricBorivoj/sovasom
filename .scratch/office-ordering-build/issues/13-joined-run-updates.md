# 13: Receive updates to runs joined

Status: ready-for-agent
Blocked by: [09: Record unavailable quantities and inspect history](09-unavailable-outcomes-history.md), [10: Leave, remove and restore office membership](10-membership-lifecycle.md), [12: Enable device push and receive new-run notifications](12-enable-push-new-runs.md)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** Request holders receive relevant changes and outcomes, with correct cancellation audiences and current-state navigation even when a message arrives late.

- [ ] For Updates to runs I joined, notify submitted-request holders of deadline changes excluding the changing actor, early closure excluding runner, and collection excluding runner. Manual cancellation includes submitted-request holders plus runner when an administrator cancels, excluding the cancelling actor.
- [ ] Cancellation caused by runner membership departure preserves the same applicable cancellation intent/audience rules while send-time checks exclude departed members. No push for automatic empty-run cancellation, routine request submission/edits or individual unavailable-quantity changes.
- [ ] Completion wording says Items collected without implying arrival. Affected colleagues may see Some items were unavailable without item/price/note details. Record intent with lifecycle mutations and reevaluate current access/session/category and staleness before send.
- [ ] Foreground notices are deduplicated; deep links render latest Collected/Cancelled/access-lost state rather than trusting event-time action availability. No persistent inbox is added.
- [ ] Use full-stack tests with the real worker and recording transport for the event/audience matrix, cancellation actor exclusions, removal, unavailable completion and delayed deep links. Test no-push cases and transactional/restart behavior; add focused notice/navigation interactions and relevant component stories.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
