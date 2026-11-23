# 14: Receive one timely closing reminder

Status: ready-for-agent
Blocked by: [07: Edit and withdraw requests before closing](07-edit-withdraw-request.md), [08: Close requests, shop and finish a run](08-shop-and-finish-run.md), [12: Enable device push and receive new-run notifications](12-enable-push-new-runs.md)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** A colleague who has not submitted a request receives at most one useful closing reminder per run, including after deadline changes or worker restarts.

- [ ] Schedule one logical reminder per colleague/run two minutes before closing, excluding the runner and submitted-request holders; apply current membership/category/device/session eligibility at dispatch. Initially two-minute-or-shorter runs skip reminders.
- [ ] Reschedule an unsent reminder when the deadline changes. If shortening leaves two minutes or less, send an eligible unsent reminder immediately while requests remain open. Never repeat one already sent, including after extension; delivery to multiple enabled devices is one logical reminder.
- [ ] Suppress pending reminders after submission, closing, cancellation, access/session loss or useful expiry. Restart reconciliation must not replay obsolete reminders. Durable claims, bounded retries and external-dispatch duplicate limits remain consistent with ticket 12.
- [ ] Keep minute-sensitive scheduling in the real application worker, available 08:00–15:00 Europe/Belgrade plus outstanding runs/work, including a 14:59 announcement. Do not prohibit authorized out-of-window actions or implement each reminder as a GitHub scheduled workflow.
- [ ] Integrated tests cover short runs, eligibility, request withdrawal before an unsent reminder, rescheduling/immediate shortening, extension after send, multiple devices, cancellation and restart with controlled time. Prove logical deduplication and claim races in PostgreSQL and visible current-deadline navigation through Playwright; extend reminder/notice stories and focused UI tests as applicable.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
