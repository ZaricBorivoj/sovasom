# Notification experience and preferences

Parent: [Office coffee and bakery ordering](../map.md)
Label: wayfinder:grilling
Type: grilling
Status: resolved
Assignee: Nemanja.Tomic (Codex session)
Blocked by: 02, 04

Dependencies: [Run lifecycle and closing rules](02-run-lifecycle.md); [Establish iOS web push feasibility](04-ios-web-push.md).

## Question

Given platform constraints and run states, how should notifications for new runs, approaching closing times, and run completion work? Decide audiences, reminder timing, preference controls, installation and permission onboarding, and the experience when push is unavailable or declined. Distinguish best-effort notifications from authoritative run state, and decide how changed closing times affect reminders.


## Comments

### 20 November 2026 — lifecycle decision handoff

[Run lifecycle and closing rules](02-run-lifecycle.md#answer) is resolved, clearing this ticket’s remaining blocker. Collected is terminal and releases the slot; there is no Returned state or return-confirmation action. Reconcile the original returning notification intent with that boundary without promising physical arrival at collection. Decide notification behavior for deadline changes, early closure, cancellation (including an empty run at its deadline), collection and unavailable outcomes here; those notification policies have not been resolved by the lifecycle discussion.


### 20 November 2026 — notification policy confirmed

The user answered “yes to all” in both discussion rounds: event audiences, reminder timing, controls and onboarding, followed by deadline changes, administrator cancellation, devices, message privacy and foreground/delayed delivery. This confirms the shared understanding below.

## Answer

Resolved through live discussion. Carry forward [Explore and choose the frontend direction](03-visual-direction.md#answer), [Shop menus and item choices](01-shop-menus.md#answer), [Run lifecycle and closing rules](02-run-lifecycle.md#answer), and the platform constraints in [Establish iOS web push feasibility](04-ios-web-push.md#answer). Postcard Club, both shops, Specialty-default coffee choices and preserved request details remain approved. Collected is terminal; there is no return-confirmation action or notification promising physical arrival.

### Events, audiences and categories

The following push events are subject to the recipient's category preference, enabled device/session and current office access. Exclude the person performing the action as specified below.

| Event | Audience | Category |
| --- | --- | --- |
| New run | All current office members except the runner | New runs |
| Closing reminder | Eligible colleagues without a submitted request, excluding the runner | Closing reminders |
| Closing deadline changed | Colleagues with a submitted request, excluding the person changing it | Updates to runs I joined |
| Requests closed early | Colleagues with a submitted request, excluding the runner | Updates to runs I joined |
| Run cancelled manually | Colleagues with a submitted request, plus the runner when an administrator cancels; exclude the person cancelling | Updates to runs I joined |
| Everything collected | Colleagues with a submitted request, excluding the runner | Updates to runs I joined |

An empty run automatically cancelled at its deadline needs no push; the outcome remains visible in the app. Routine request submissions and edits do not generate push. Unavailable quantities are visible in the affected colleague's request and reflected in their completion notification, without separate pushes for each change. Use “Items collected” for completion without implying the runner is back at the office.

### Closing reminders and changed deadlines

- Send one reminder two minutes before closing, only to colleagues without a submitted request and excluding the runner. Evaluate eligibility against current state when sending.
- Skip reminders for runs initially allowing two minutes or less.
- Each colleague receives at most one logical closing reminder per run; delivery to their enabled devices is the same reminder, not additional reminders.
- Changing the deadline reschedules an unsent reminder. If shortening leaves two minutes or less, send an eligible unsent reminder immediately while requests remain open.
- Never repeat a reminder already sent, including after a deadline extension. Suppress pending reminders after request submission, closing or cancellation.
- Deadline changes also notify existing request holders through the separate event/category above. The authoritative deadline and lifecycle rules remain unchanged.

### Preferences, devices and optional setup

Offer three independent account-wide category controls: New runs, Closing reminders, and Updates to runs I joined. All are initially selected once the colleague enables push. Changes govern future delivery; enabling a category does not replay past events.

Enabling push requires setup on each device. Deliver eligible notifications to all enabled devices. Signing out stops push to that signed-out session. Account category settings and device/session delivery status must be distinguishable in the experience.

Setup is optional. Provide an explanatory Enable notifications action and iOS Home Screen installation guidance where needed. Ask for operating-system permission only following that user action. If permission is declined or push is unavailable, retain full app usability, clear run status and countdowns, and settings guidance without repeated permission prompts. No email or SMS notification fallback is required.

### Message privacy, opening and foreground behavior

Lock-screen messages may show runner/run identity, the event and relevant closing time. Omit request items, notes and prices. For an affected colleague, completion may say “Some items were unavailable” without listing them.

Tapping a notification opens its run and loads the current authoritative state, including Collected or Cancelled outcomes. A notification is never evidence that an action is still available or that a deadline remains open.

Refresh run details while the app is open and show a brief in-app notice for relevant changes, avoiding duplicate in-app notices for the same event. No persistent notification inbox is required. Run state, request details and outcomes remain available regardless of push preferences or permission.

### Best-effort delivery and downstream handoff

Suppress obsolete pushes before sending, while acknowledging that already-dispatched notifications can arrive late. Explain that push is best effort; current server state governs actions and deadlines.

[Office membership and account lifecycle](06-office-access.md) must account for current-member notification access and removal, preserving the confirmed sign-out behavior. It still owns membership, account removal and historical attribution decisions.

[Delivery architecture and verification approach](07-delivery-and-verification.md) owns scheduling, current-state eligibility checks, logical reminder deduplication, stale-event suppression, delivery/session management, foreground refresh and the verification approach. These are implementation/architecture choices for that existing ticket, not additional product tickets.

No new decision ticket emerged. Only Notification experience and preferences was resolved. No application or prototype behavior changed; production unit tests, Storybook and integrated Playwright tests were not run because this session changed planning documents only.
