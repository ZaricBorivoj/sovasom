# 05: Announce the office’s single active run

Status: ready-for-agent
Blocked by: [01: Bootstrap and sign into the private office](01-bootstrap-private-office.md)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** Any current member announces a trip to both shops and colleagues see the office’s one authoritative active run, which can be cancelled or expire if unused.

- [ ] Announcement always visits both shops with no shop/title inputs. Generate and persist a funny title once using Europe/Belgrade day and period: morning before 12:00, afternoon 12:00–17:59, evening from 18:00. Show run date, server-derived closing clock time and countdown.
- [ ] Offer exactly 5/10/15/30 minutes, default 15, and custom whole minutes 1–180. Start the window at successful announcement. Enforce a single active-run slot atomically in PostgreSQL; simultaneous announcements yield one success and show the existing run to the other person.
- [ ] Use Accepting requests, Shopping, Collected and Cancelled semantics from the spec. Initially request-free runs cancel automatically at their deadline and release the slot. Runner cancellation of an active run requires confirmation with optional reason, preserves its record and releases the slot. Requests and full shopping actions arrive in later slices.
- [ ] Introduce the worker using the shared backend image with durable PostgreSQL due work/reconciliation. Enforce effective deadlines in server operations even if a screen or worker is stale. Required availability is 08:00–15:00 office time plus outstanding work, without prohibiting authorized out-of-window actions. Restart recovery must preserve due work.
- [ ] Refresh shared state about every five seconds and on focus/reconnection/successful actions. Handle stale/concurrent actions with clear rejection and authoritative refresh. Use prominent active/empty Postcard Club states without prototype debug tools.
- [ ] Prove announcement/cancellation/empty expiry and next announcement through real UI/API/PostgreSQL/worker tests. Use controlled clocks for duration and day-period boundaries, real PostgreSQL for simultaneous announcements and restart recovery, and stories/UI tests for duration validation, countdown, active/empty, pending/conflict/error states.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
