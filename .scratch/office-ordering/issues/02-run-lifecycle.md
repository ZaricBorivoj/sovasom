# Run lifecycle and closing rules

Parent: [Office coffee and bakery ordering](../map.md)
Label: wayfinder:grilling
Type: grilling
Status: resolved
Assignee: Nemanja.Tomic (Codex session)
Blocked by: None

## Question

Given a closing duration in minutes set when a run opens, what are its states and permitted actions? Every run visits both shops. Decide when requests can be edited or withdrawn, whether the runner can change the time or close early, and how cancellation, unavailable items, shopping progress, and returning to the office work. Clarify the consolidated shopping list and enforce at most one active run, including concurrent announcements. Resolve boundary cases such as a request arriving exactly at closing time.

## Comments

### 20 November 2026 — confirmed constraints from frontend review

Apply the [user-confirmed requirements in Explore and choose the frontend direction](03-visual-direction.md#20-november-2026--live-feedback-and-second-exploration) when discussing lifecycle policy. Both shops are always visited; title generation, closing duration and whole-run collection confirmation have been requested. This ticket remains open for the remaining lifecycle decisions.

### 20 November 2026 — single active run confirmed

The user confirmed at most one active run for now; see [Explore and choose the frontend direction](03-visual-direction.md#confirmed-product-requirements). Resolve which states hold that slot and when it is released, including closing, collection, returning and cancellation. The user approved completed-run summaries below the active run; history scope/access remains to be decided here. Quick closing-duration choices are confirmed in the same source. This ticket remains open.

### 20 November 2026 — menu decision handoff

Carry forward [Shop menus and item choices](01-shop-menus.md#answer), now resolved. This ticket owns request editing/withdrawal and handling items unavailable at the shop, subject to the agreed menu-change preservation and availability constraints. Do not reopen the confirmed menu decisions.


### 20 November 2026 — first lifecycle round confirmed

User accepted the first round with one correction: “Collected should also be the end of the lifecycle, no need for an extra action from the runner”.

- Lifecycle: Accepting requests → Shopping → Collected; Cancelled is the other terminal state. The deadline automatically starts Shopping. Collected ends the run and releases the active-run slot; there is no Returned state or return-confirmation action. Accepting requests and Shopping occupy the slot.
- Closing duration: quick choices 5, 10, 15, 30 minutes; default 15; custom whole minutes 1–180. Count from successful announcement and show countdown plus closing clock time.
- Shopping list: group by shop, item, coffee choice and identical note; keep different notes separate. Show quantities and expandable colleague contributions.
- History: all current office members can view completed and cancelled runs and request details. Show latest 10 summaries with Load more; retain history in the first version. Account removal/personal-data handling belongs to Office membership and account lifecycle.
- Use Europe/Belgrade for office times. Generate the funny day/time-of-day title once at announcement; morning before 12:00, afternoon 12:00–17:59, evening from 18:00. Show calendar date in run details.

Remaining policies await the next live discussion; this ticket is not resolved.


### 20 November 2026 — remaining lifecycle rules confirmed

The user answered “yes to all” to the second round: request editing and preservation, deadline changes, cancellation and administrator recovery, unavailable quantities, empty-run cancellation and whole-run completion, and server-authoritative timing/conflict handling. Together with the first-round correction, this confirms the shared understanding below.

## Answer

Resolved through live discussion. Carry forward [Explore and choose the frontend direction](03-visual-direction.md#answer) and [Shop menus and item choices](01-shop-menus.md#answer), including Postcard Club, both shops on every run, Specialty as the coffee default, and preserved submitted request details.

### States and active-run boundary

| State | Meaning | Occupies the single active-run slot? |
| --- | --- | --- |
| Accepting requests | Colleagues can submit, change or withdraw their requests before the deadline. | Yes |
| Shopping | Requests are closed and the runner uses the consolidated shopping list. | Yes |
| Collected | The runner has used the single Everything collected action. The lifecycle has ended. | No |
| Cancelled | The run ended without completion, by cancellation or the empty-run rule. | No |

Normal flow: Accepting requests → Shopping → Collected. The deadline automatically starts Shopping, except that a run with no requested items automatically becomes Cancelled. The runner can close requests early. The runner or an office administrator can cancel either active state. There is no Returned state or Back at the office action. Collected and Cancelled are terminal; a later trip requires a new announcement.

Only Accepting requests and Shopping hold the slot. Collection or cancellation immediately releases it, so another run can be announced even while the previous runner is physically returning. Shopping progress requires no separate shop-completion actions or per-item collection checkboxes.

### Announcement, title and deadline

- Quick duration choices: 5, 10, 15 and 30 minutes; default 15. Custom duration is a whole number from 1–180 minutes.
- Count from successful announcement. Display both countdown and closing clock time.
- Use Europe/Belgrade office time. Generate the funny title once at announcement, identifying the day and time of day, without a title input. Morning is before 12:00; afternoon is 12:00–17:59; evening is from 18:00. Include the calendar date in run details.
- While accepting requests, the runner can set a new closing time 1–180 minutes from now, or use Close requests now. Once Shopping begins, requests cannot reopen.

### Request ownership, editing and menu changes

Each colleague, including the runner, has at most one request per run and can submit, edit or withdraw their own request before closing. Unsubmitted drafts are excluded from the shopping list. Requests lock during Shopping, apart from the runner recording unavailable outcomes described below.

Changing a saved line’s quantity or note preserves its submitted name, coffee choice and displayed price. Added or replaced items use the current menu. A line flagged unavailable can be reduced or removed, but cannot be increased. Existing lines are never silently repriced, deleted or substituted because the menu changes. Other confirmed menu policies remain in [Shop menus and item choices](01-shop-menus.md#answer).

### Shopping list, unavailable items and collection

Group by shop, item, coffee choice and identical note. Keep different notes and coffee choices separate. Show consolidated quantities with expandable colleague contributions.

The runner can record all or part of a requested quantity as unavailable at the shop. Preserve the original request, and show the outcome to the affected colleague. This is a run-specific outcome, separate from maintained menu availability. Do not substitute items.

For a non-empty run, Shopping continues until cancellation or the single Everything collected action. That action ends the run; recorded unavailable quantities remain clearly identified as unfulfilled. It does not falsely declare those quantities collected. No later return confirmation is required.

### Cancellation and recovery

The runner can cancel any active run, including after shopping begins, with confirmation and an optional reason. Office administrators have the same capability to recover abandoned runs. Preserve requests in cancelled history and immediately free the slot. Administrator permission assignment and account-removal consequences belong to [Office membership and account lifecycle](06-office-access.md).

### History

All current office members can view completed and cancelled runs, including request details and outcomes. Show the latest 10 summaries below the active run with Load more. Retain history for the first version; account removal and personal-data handling remain with [Office membership and account lifecycle](06-office-access.md).

### Time boundaries and concurrent actions

The server clock and accepted state are authoritative. Request submission, editing and withdrawal must be accepted strictly before the deadline; exactly at the deadline is too late. Closing applies even if a screen or background transition has not refreshed yet.

Enforce the office’s single active-run slot atomically, including simultaneous announcements: one announcement succeeds and the other person is shown the existing active run. Request changes racing with closing, cancellation or collection either succeed before the transition or receive a clear rejection and refreshed state. The same authoritative state must govern deadline changes and lifecycle actions, avoiding stale actions reopening or modifying a terminal run.

### Downstream handoff and verification

[Notification experience and preferences](05-notifications.md) is now unblocked. It must account for editable deadlines, early closure, cancellation and terminal collection; there is no distinct return-confirmation event. Notification audiences, reminders and preference behavior remain that ticket’s decisions.

No additional decision ticket emerged: notification behavior and membership/history permissions already have existing owners. Only this decision ticket was resolved. No application or prototype behavior changed, so production unit tests, Storybook and integrated Playwright tests were not run.
