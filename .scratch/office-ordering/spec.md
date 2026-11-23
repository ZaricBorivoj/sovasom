# Office coffee and bakery ordering — first usable release

Status: ready-for-agent
Blocked by: None
Parent: [Completed wayfinder map](map.md)
Testing seams: confirmed by the user on 23 November 2026 in the to-spec handoff.

## Problem Statement

Office colleagues need a private, reliable way to coordinate coffee and bakery trips. They need to know who is going, how long they have to request items, what they requested, and which items could not be obtained. The runner needs one accurate shopping list rather than scattered messages. Administrators need to manage access without public registration, and the operator needs a deployable application with recoverable data and credentials.

## Solution

Build a responsive private-office web application using the approved Postcard Club design. Any office member can announce a run visiting both shops. Colleagues submit requests from maintained shop menus until a server-enforced closing deadline. The runner shops from consolidated quantities, records unavailable quantities, and ends the run with Everything collected. Collection or cancellation immediately frees the office's single active-run slot.

Provide administrator-created email/password accounts, separate office memberships and permissions, optional per-device Web Push with account-wide categories, and retained run history. Deploy React 19/Vite, FastAPI, a durable worker and PostgreSQL through Compose on the user's Intel Mac mini running macOS/Docker Desktop. GitHub Actions orchestrates delivery, Terraform-managed AWS infrastructure, and encrypted off-host backups.

## User Stories

1. As an office colleague, I want a private application usable on phone and desktop, so that I can coordinate a run wherever I am.
2. As an office member, I want one prominent active run above quieter history, so that I can immediately see the current trip.
3. As an office member, I want an empty state offering to announce a run, so that I know how to start the next trip.
4. As an office member, I want every run to include both shops, so that I can choose coffee and bakery items together.
5. As an office member, I want to announce a run myself, so that organizing a trip does not require an administrator.
6. As a runner, I want a funny title generated once with the office day and time of day, so that I do not have to name my run.
7. As a runner, I want quick closing durations of 5, 10, 15 and 30 minutes with 15 selected initially, so that announcing a run is quick.
8. As a runner, I want a custom whole-minute duration from 1 to 180, so that I can allow an appropriate joining window.
9. As an office member, I want concurrent announcements to lead to one active run, so that colleagues do not split across competing trips.
10. As an office member, I want the countdown, closing clock time and calendar date in office time, so that I understand the deadline.
11. As a runner, I want to move the closing time while requests are open, so that I can respond to changed plans.
12. As a runner, I want to close requests early, so that I can start shopping immediately.
13. As an office member, I want requests to close even if my screen is stale, so that the shopping list has a reliable cutoff.
14. As a colleague, I want maintained menus grouped by shop, so that I can select available items without typing product names.
15. As a coffee requester, I want Specialty selected initially and Blend available before adding, so that my coffee choice is explicit.
16. As a colleague, I want juice and hot chocolate without coffee-choice controls, so that irrelevant options do not confuse me.
17. As a colleague, I want positive whole-number quantities and optional notes per request line, so that I can describe what to collect.
18. As a colleague, I want different coffee choices and notes represented separately, so that my preferences survive consolidation.
19. As a colleague, I want item prices and an estimated request total, so that I can judge my expected spend.
20. As a colleague, I want one submitted request per run, so that my contribution has a clear identity.
21. As a runner, I want to submit my own request, so that my items are included in the same shopping list.
22. As a colleague, I want to edit or withdraw my request before closing, so that I can change my mind.
23. As a colleague, I want drafts excluded from the shopping list, so that unsubmitted selections are not purchased.
24. As a colleague, I want submitted names, coffee choices and displayed prices preserved after menu changes, so that my saved request does not silently change.
25. As a colleague, I want unavailable menu items blocked for new selection and visibly flagged in existing requests, so that I can make an informed correction.
26. As a colleague, I want to reduce or remove an unavailable saved line, so that I can adjust without increasing an unavailable selection.
27. As a menu maintainer, I want to add, edit, reorder and retire items in both shop menus, so that colleagues have a useful selection.
28. As a menu maintainer, I want separate Blend and Specialty prices, so that the menu can reflect real price differences.
29. As a menu maintainer, I want to mark an item unavailable without deleting saved requests, so that availability and history remain accurate.
30. As a runner, I want a shopping list grouped by shop, item, coffee choice and identical note, so that I can purchase accurate quantities.
31. As a runner, I want to expand colleague contributions, so that I can understand each consolidated quantity.
32. As a runner, I want to record all or part of a requested quantity as unavailable, so that outcomes reflect what I could obtain.
33. As an affected colleague, I want my original request and unavailable outcome visible together, so that I can see what was unfulfilled.
34. As a runner, I want one Everything collected action, so that I can finish without per-item or per-shop collection checks.
35. As an office member, I want collection to free the run slot immediately, so that another trip can start without a return confirmation.
36. As a runner, I want to cancel an active run with confirmation and an optional reason, so that I can communicate abandoned plans.
37. As an office administrator, I want to cancel abandoned active runs, so that the office is not blocked indefinitely.
38. As an office member, I want an empty run automatically cancelled at its deadline, so that an unused run does not hold the slot.
39. As an office member, I want the latest ten collected or cancelled summaries with Load more and request details, so that I can inspect retained history.
40. As a colleague, I want clear rejection and refreshed state after a conflicting action, so that I understand what the server accepted.
41. As a colleague, I want shared state refreshed while viewing the app and after returning online, so that I can follow a run without push.
42. As a colleague, I want optional notification setup on each device, so that declining push does not prevent office participation.
43. As an iPhone colleague, I want Home Screen installation and permission guidance, so that I can enable supported Web Push.
44. As a colleague, I want independent New runs, Closing reminders and Updates to runs I joined controls, so that I choose which future pushes I receive.
45. As a colleague, I want account preferences distinguished from device/session status, so that I understand where delivery is enabled.
46. As a colleague without a submitted request, I want at most one closing reminder two minutes before closing, so that I can join without repeated reminders.
47. As a colleague with a request, I want relevant deadline-change, early-close, cancellation and collection updates, so that I can follow changes affecting me.
48. As a runner, I want notification when an administrator cancels my run, so that I know it has ended.
49. As a colleague, I want notification text to omit my items, notes and prices, so that lock-screen messages preserve request privacy.
50. As a colleague, I want a notification to open the current run state, so that delayed delivery does not mislead me about available actions.
51. As a colleague, I want clear denied or unsupported notification states without repeated permission prompts, so that I can use the app comfortably.
52. As a colleague, I want sign-out, credential changes and lost office access to stop future push delivery, so that revoked sessions cannot keep receiving office updates.
53. As an office administrator, I want to create accounts manually, so that office access remains controlled without invitations or public signup.
54. As a newly added colleague, I want a temporary password privately handed to me and a required personal-password change, so that I can establish my own credentials before office access.
55. As an office administrator, I want temporary passwords shown once and expired after 24 hours, so that credential handoff is bounded.
56. As a colleague who forgot a password, I want administrator-assisted recovery guidance, so that I can regain access without an email service.
57. As an operator, I want runtime bootstrap and separate sole-administrator recovery, so that the installation can start and recover without hardcoded credentials.
58. As an office administrator, I want equal administrator peers and separate menu-maintainer grants, so that responsibilities can be shared explicitly.
59. As an office member, I want the last administrator protected from demotion, departure, removal and deletion, so that office management remains possible.
60. As a colleague, I want to change my display name and password, so that I can maintain my account.
61. As an office administrator, I want to change an account email without changing identity or history, so that login details can be corrected safely.
62. As a colleague, I want my email visible only to me and administrators, so that it is not exposed as a public profile.
63. As an office administrator, I want membership removal to revoke office access immediately on all devices, so that former members cannot continue office operations.
64. As a departing runner, I want a warning that leaving cancels my active run, so that I understand the effect before confirming.
65. As a departing participant, I want my open request withdrawn and my Shopping request preserved, so that departure respects the runner's current work.
66. As a colleague, I want to leave the office while retaining my account, so that office access and account identity remain separate.
67. As an office administrator, I want to restore membership to the same account without restoring old requests or elevated permissions, so that return is deliberate.
68. As an account holder requesting deletion, I want administrator-assisted erasure of my personal data with shared history retained as Deleted colleague, so that deletion does not destroy colleagues' run records.
69. As an operator, I want reproducible CI, image builds and serialized deployments, so that releases are traceable and gated by checks.
70. As an operator, I want public HTTPS and a private persistent database, so that colleagues can use accounts and push reliably.
71. As an operator, I want retained infrastructure storage separated from application teardown, so that removing the application does not delete backups or Terraform state.
72. As an operator, I want encrypted weekly and pre-migration backups with restore verification, so that I can recover from host loss or a failed change.
73. As an operator, I want secret custody, rotation and recovery independent of the mini, so that host loss does not also destroy recovery access.
74. As an operator, I want verified recovery after manual cold-boot unlock/login, so that the accepted macOS recovery procedure is usable.

## Implementation Decisions

### Authority, current repository and decision dependencies

- This is a greenfield implementation: inspection on 23 November 2026 found planning documents and standalone HTML prototypes only, with no production application, package manifests, test suites, design-system implementation, commits or remote. Use the shared [glossary](../../GLOSSARY.md). No ADRs currently exist; there is no ADR to override. Do not treat absent implementation as an existing reusable seam.
- The authoritative chain is visual direction → menu policy → lifecycle → notification policy, with iOS feasibility constraining notifications; account lifecycle then supplies access and deletion rules; delivery consolidates these and the hosting research. Decision sources and supersessions are indexed in Further Notes. Earlier comments marked pending and research recommendations do not override resolved answers.

### Application and persistence boundaries

- Build one modular FastAPI application with accounts/access, menus, runs/requests and notifications responsibilities. Run a separate worker from the same backend package/image. Use React 19 with Vite for the SPA and PostgreSQL in Docker for saved state, permissions, sessions and durable work. Do not split domain modules into separately deployed services.
- Persist accounts independently of email/password and separately from office membership; model administrator and menu-maintainer grants explicitly. Persist shops/menu items with ordering, coffee applicability, prices, availability and retirement; runs with runner, generated title, authoritative timestamps, state and optional cancellation reason; unique colleague/run requests and snapshot request lines; per-line unavailable outcomes; account notification categories; session-bound subscriptions; durable event/due-work and logical-reminder identities. Preserve historical references while permitting the deletion anonymization below. These are required data relationships, not a mandate for a particular ORM or table layout.
- Use authenticated same-origin JSON HTTP endpoints under the API proxy. Cover authentication/credential setup/sign-out/profile, administrator access management, menus, active run and history/details, announcement/deadline/lifecycle actions, own-request operations, runner shopping outcomes, and notification preferences/device registration. Recheck current account, membership and action permission on every operation; frontend visibility is not authorization.
- Enforce one active run per office and one request per colleague/run with PostgreSQL constraints and transactions. Serialize conflicting lifecycle, request and access operations with appropriate locking. Simultaneous announcements yield one success; the loser sees the existing active run. Deadline/lifecycle races either accept the action before transition or clearly reject it and refresh authoritative state. Stale actions cannot reopen or modify terminal runs.
- Refresh visible shared state roughly every five seconds and on focus, reconnection and successful actions. Deduplicate brief relevant in-app notices. Server instants govern deadlines, regardless of client clock, stale screen, polling or worker delay. Notification navigation loads current state and checks access anew.

### Postcard Club experience and design system

- Follow the approved selected preview's layout: Office runs, one prominent active-run postcard, quieter collected/cancelled summaries below, and an announcement empty state. Support phone and desktop without overflow. History begins with ten summaries and Load more; all current members can inspect retained request details and outcomes.
- Create a project-owned React design system using shared tokens and accessible primitives. Visual references: background `#f4f0fc`, peach `#f9ce98`, lavender `#dad1f6`, green `#e5eec7`, plum `#4c2864`, ink `#41294e`, 2px borders, approximately 24px corners and 5px offset shadows. Use bold rounded sans-serif typography, rounded buttons and closing-duration stamps. Reusable candidates include Postcard, RunStatus, DurationChoices, CoffeeChoice, QuantityControl, RequestSummary and ShopList.
- Use native radio semantics for styled coffee choices, semantic buttons, labelled fields, visible focus and explicit statuses. Every production component needs Storybook coverage of relevant states and variants, including validation, pending/error, permission/access loss and notification setup states. No third-party component library is prescribed.
- Prototypes are visual/interaction evidence, not production code. Do not carry over comparison controls, scenario/reset tools, state debug views, sample identities/menu/prices, avatars, browser-local clock policy, fixed countdowns or prototype lifecycle bugs.

### Shop menus and saved requests

- Designated menu maintainers manage both menus: add, edit, reorder, retire and mark unavailable. Nemanja.Tomic owns initial menu content and receives corrections outside the app; runtime bootstrap assigns permissions without hardcoding a person. Actual menu content is maintained data; prototype shops/items/prices are illustrative. Coffee shop menus support coffee, juices and hot chocolate.
- Every coffee has Blend/Specialty, with Specialty selected before adding. Maintain separate choice prices that may differ. Juice, hot chocolate and non-coffee items have no coffee choice. Blend/Specialty is the only structured option; notes express other preferences without guaranteed availability or extra-charge calculations.
- Quantities are positive whole numbers. Each line can have an optional note. Distinct choices or notes remain distinct lines. Show displayed menu prices and an estimated request total; payment settlement stays outside the app.
- Each colleague, including the runner, owns at most one request per run. Only submitted requests enter the shopping list. Before closing the owner may submit, edit or withdraw; during Shopping requests lock except for runner-recorded unavailable outcomes.
- Snapshot submitted item name, coffee choice and displayed price. Later quantity/note edits retain that snapshot; added or replaced selections use the current menu. Retired items remain readable in history. Menu changes never silently reprice, delete or substitute saved lines.
- Unavailable menu items cannot be newly selected. Flag existing affected lines; allow reduction/removal but no increase. Maintained menu availability is distinct from a run-specific unavailable quantity recorded at the shop.

### Run lifecycle, deadlines and shopping

| State | Permitted behavior | Holds active-run slot |
| --- | --- | --- |
| Accepting requests | Own-request changes strictly before deadline; runner may change deadline or close early; runner/administrator may cancel | Yes |
| Shopping | Requests closed; runner records unavailable outcomes and collects; runner/administrator may cancel | Yes |
| Collected | Terminal, retained details/outcomes | No |
| Cancelled | Terminal, retained requests and optional reason | No |

- Every run visits both shops; there is no shop selector. On successful announcement generate and save a funny day/time-of-day title once; do not ask for a title. Europe/Belgrade defines office display and day periods: morning before 12:00, afternoon 12:00–17:59, evening from 18:00. Show the calendar date in run details.
- Closing choices are exactly 5/10/15/30 minutes, default 15; custom whole minutes 1–180. The window starts at successful announcement, not form opening. Show countdown and closing clock time. While accepting requests the runner may set a new deadline 1–180 minutes from now or Close requests now. Shopping cannot reopen.
- At the deadline automatically enter Shopping, or Cancelled if there are no requested items. Requests submitted, edited or withdrawn exactly at the deadline are too late. Enforce effective closure on writes even before the background transition runs. A non-empty Shopping run continues until collection or cancellation.
- Consolidate the shopping list by shop, item, coffee choice and identical note, with quantities and expandable colleague contributions. Never merge different notes/choices. Preserve submitted detail even if menu data changes.
- The runner may record unavailable quantities for all or part of requested quantities; validate against the original quantity and retain attribution to the affected request lines so each colleague sees their own outcome. No substitutions. Original requested quantities remain available alongside unfulfilled quantities.
- Everything collected is a single whole-run action during Shopping. It ends the run and releases the slot immediately; unavailable quantities remain explicitly unfulfilled. No per-item checkbox, shop-completion action, Returned state or return confirmation. Collection does not promise physical arrival at the office.
- Runner or administrator cancellation is available in either active state, requires confirmation and permits an optional reason. Preserve requests in cancelled history and immediately release the slot. Terminal runs cannot reopen; another trip requires a new announcement.

### Accounts, permissions and personal data

- Support one private office. Administrators manually create accounts; no public signup, invitations or email-domain admission. Future Google/Apple identities can attach to stable account identity, but SSO and linking workflows are deferred.
- All current members can announce runs, manage their own requests within deadlines and read office history. Administrators have equal authority to create users, remove/restore memberships, manage both elevated grants, change email and cancel active runs. Menu maintenance requires its own grant. Protect the last administrator against demotion, removal, departure or deletion, including concurrent actions.
- Require a self-editable display name. Only the account holder and administrators see email. Members can change their own passwords; administrators change email while preserving account/history identity, reject duplicates, end existing sessions and issue a new temporary password.
- Bootstrap via one setup/preparation command loading initial email, display name and password from runtime environment configuration, running schema migrations, then atomically creating initial account, membership, administrator and menu-maintainer grants through an ORM initializer outside versioned migrations. No hardcoded person/password. After initialization reruns leave credentials/grants unchanged even if inputs change. Remove bootstrap secrets after success. Provide a separate explicit operator recovery command for sole-administrator lockout.
- Administrator creation/reset generates a temporary password shown once for private handoff after identity confirmation outside the app. Expire it after 24 hours. It allows setting a personal password but no office access before that change. Store password hashes; do not retrieve/display existing passwords. Forgotten-password guidance directs users to an administrator. Email is an unverified login identifier; no SMTP dependency.
- Use PostgreSQL-backed revocable opaque sessions with Secure/HttpOnly/SameSite cookies and CSRF protection. Absolute lifetime is 30 days, ending earlier on sign-out, applicable access/credential revocation, password change/reset or email change. Push registrations belong to their sessions; expired/signed-out/revoked sessions cannot receive future delivery. Account survival after membership removal does not preserve office authorization.
- Membership removal or confirmed self-departure revokes office access across devices immediately and stops future notifications. If departing member runs an active run, warn and cancel it atomically with removal. If another participant departs during Accepting requests, withdraw their request; during Shopping, preserve it. Retain earlier history and attribution after membership removal.
- Restoration reuses the account but restores neither administrator/menu-maintainer grants nor old requests automatically. Account deletion is separate, administrator-assisted and irreversible, after confirmation of the account holder's request. Apply removal rules first; delete credentials, email, display name, preferences and device registrations; remove identifying attribution from retained runs/requests and display Deleted colleague. Retain shared item/quantity/outcome history and clear free-text notes from that person's requests. A later account does not link to the deleted identity.

### Notifications and durable work

All push events require current access, account category preference and an enabled eligible device/session at send time. Deliver to all eligible devices; actor exclusions below apply.

| Event | Audience | Category |
| --- | --- | --- |
| New run | Current office members except runner | New runs |
| Closing reminder | Members without submitted requests except runner | Closing reminders |
| Closing deadline changed | Submitted-request holders except person changing it | Updates to runs I joined |
| Requests closed early | Submitted-request holders except runner | Updates to runs I joined |
| Manual cancellation | Submitted-request holders plus runner when administrator cancels; exclude cancelling actor | Updates to runs I joined |
| Everything collected | Submitted-request holders except runner | Updates to runs I joined |

- No push for automatic empty-run cancellation, routine request submissions/edits or individual unavailable changes. Show unavailable outcomes in the request and reflect them in completion wording. Use Items collected, without implying arrival.
- Send one logical reminder per colleague/run two minutes before closing. Initially two-minute-or-shorter runs skip reminders. Deadline edits reschedule unsent reminders; shortening to two minutes or less sends an eligible unsent reminder immediately while still open. Already sent reminders never repeat, even after extension. Suppress pending reminders after submission, closing or cancellation and reevaluate current eligibility at send time.
- Three independent account-wide categories are initially selected when push is enabled. Category changes govern future delivery without replay. Device setup is separate on each device; distinguish category preferences from device/session status. Signing out stops that session's future push.
- Push is optional: explain Enable notifications, provide iOS Home Screen guidance and request OS permission only from explicit user action. Denial or unsupported APIs retain full app usability, countdowns and settings guidance without repeated prompts. No email/SMS fallback or persistent notification inbox.
- Lock-screen content may include runner/run identity, event and relevant deadline; omit request items, notes and prices. Completion for an affected colleague may say Some items were unavailable without listing them. Taps load authoritative current state, including terminal outcomes and current access checks. Deduplicate foreground notices without using in-app updates as a replacement for required visible original Web Push notifications.
- Persist business changes and associated notification intent/due work in one PostgreSQL transaction. Worker claims/recovery, bounded useful retries, logical deduplication and obsolete-event suppression must survive crashes/restarts. An external dispatch crash can still duplicate a push; do not promise exactly-once external delivery. No Redis/Celery service initially.
- Required worker availability is 08:00–15:00 Europe/Belgrade, continuing past 15:00 for outstanding runs/work, including a 14:59 announcement. This does not prohibit authorized actions outside that window; leaving the worker idle/available is acceptable. GitHub scheduled jobs do not execute minute-sensitive reminders. Restart reconciliation must not replay obsolete reminders.
- Implement standards-based encrypted Web Push with VAPID and a same-origin service worker for compatibility with the researched iOS 16.4+ Home Screen route. Provide web-app manifest/identity/icons appropriate to installation. Ordinary iOS browser tabs are not the supported push surface. No Apple Developer Program/native APNs account is required for this route. The research also documents newer declarative push and changed iOS installation behavior; do not make newer APIs a baseline requirement or claim every current iOS installation requires a manifest. Selected dependency versions and minimum claimed support require implementation verification.
- Keep subscription endpoints/encryption material server-side with account/session ownership; support invalid/expired endpoint cleanup and bounded transient-error retries with useful TTL. Protect VAPID private keys; allow required outbound HTTPS. Push acceptance is not proof of receipt, viewing or precise timing. OS permission, Focus, offline state and expiry affect delivery; already-dispatched messages may arrive late.

### Delivery, infrastructure and recovery

- Use existing Intel Mac mini/macOS/Docker Desktop. Verify exact hardware capacity, supported OS/runtime, Docker licensing applicability, Compose, persistent storage and correct Docker context under SSH. Keep macOS; Linux, Colima and cloud alternatives are not selected.
- Compose runs Caddy, SPA static assets, FastAPI, same-image worker and PostgreSQL with persistent database/Caddy data. Caddy serves the Vite build, proxies the same-origin API and manages Let's Encrypt issuance/renewal. Verify existing AWS/expected Route 53 hosted zone, app subdomain/static IP, inbound 80/443 routing and firewall, and outbound push reachability. Database remains private. Vite development/preview is not the production server.
- GitHub-hosted Linux CI tests/builds immutable linux/amd64 images, publishes to GHCR and serializes host-key-verified SSH deployments from passing main. Use dedicated deployment identity, readiness/health checks, controlled migrations and recoverable prior images. Test rollback against database compatibility; reverting an image does not undo a migration. Use fresh configuration identifiers and pinned versions during implementation.
- GitHub Actions orchestrates Terraform, automated host configuration, CI/releases and weekly/pre-migration backups. Compose/host automation owns containers, volumes, host services, runtime files and Caddy configuration; Caddy owns TLS private keys. Terraform manages all applicable provider-addressable infrastructure rather than the physical mini or application secret payloads. Each resource has a deliberate owner.
- Terraform manages separate private backup and state S3 buckets in Frankfurt/eu-central-1, public-access blocking, encryption, state versioning, lifecycle rules, policies, narrow IAM roles, GitHub OIDC trust and application DNS record. Deliberately reference/import shared existing resources; do not recreate the zone/domain or duplicate an account-wide OIDC provider. Scope trust to the actual trusted repository branch/environment subject.
- Separate retained-foundation and disposable-application Terraform roots/states. Foundation owns backup/state buckets and their protection/access configuration; application references it. Use native S3 lockfiles with use_lockfile enabled and versioned state. Bootstrap backend/trust through an authenticated operator session, migrate initial state to protected remote storage and preserve independent operator recovery access off the mini.
- Normal application destroy retains foundation buckets and contents. Retained buckets use prevent_destroy enabled and force_destroy disabled; foundation destroy planning must fail while guards remain. These guards do not prevent deliberate configuration removal or authorized direct AWS deletion. Document explicit full retirement; do not automatically empty retained buckets. Backup expiration still applies after application teardown. Keep state history/current state and operator access separate from backup expiry.
- Weekly and pre-migration PostgreSQL-aware backups are encrypted before upload and retained 30 days. Successful pre-migration backup/upload gates migrations of an existing database; initial empty-install setup must work without assuming a prior database backup exists. Verify effective noncurrent backup-version cleanup, not just current-object expiry. Never apply archive expiry to live Terraform state.
- Weekly Actions assumes a narrow backup role through temporary OIDC, invokes backup/public-recipient encryption on the mini over SSH, receives ciphertext and uploads to S3. No permanent AWS credentials or private decryption identity on the mini. Monitor last success/backup age and failures, notify on stale/failed backups and support manual retry. Scheduled jobs may delay/drop: potential loss is approximately seven days, possibly longer after missed jobs. Restore an encrypted S3 archive into an isolated database before first use.
- Brief maintenance outages and manual unlock/login after cold macOS restart are accepted. Automate Docker Desktop/application restart after login and verify recovery. Restoration objective is one working day conditional on working host/replacement, network, access and keys; this is not high availability.
- Generate setup secrets through trusted operator tooling. Password manager retains recoverable database credentials, VAPID private keys, deployment SSH private keys and backup decryption identities; GitHub Actions secrets hold deployment copies. Use a production environment where supported, otherwise repository secrets with trusted workflow/branch administration. Do not assume unavailable approval features. PR/test jobs receive synthetic values only; separate narrow infrastructure and backup OIDC roles replace permanent AWS keys.
- Send minimum required runtime secrets through verified SSH into private files outside the checkout, with restricted directory/file ownership and permissions. Mount only each container's needed files through Compose secrets and explicitly support backend file-based configuration. Verify real Docker Desktop mount readability/permissions. No secret payloads in source, images/build arguments, frontend bundles, Terraform inputs/state, logs or artifacts. Protect sensitive Terraform state even without application secrets.
- Use job-scoped GHCR credentials for publish/pull, verify private-image access and expired-token behavior, and clean up registry authentication on all exit paths including Docker Desktop credential helpers/Keychain. A temporary Docker configuration directory alone is insufficient evidence of cleanup.
- Caddy persists TLS keys locally and can reissue on replacement. Browser gets public configuration only. Remove bootstrap password from runtime files and temporary GitHub secret after successful initialization. Rotate vault copies, deployment copies and running services together; database rotation must change the actual database role. Retain old backup identities until corresponding archives expire and keep independent AWS recovery access.

## Testing Decisions

- **User-confirmed seams (23 November 2026):** primary acceptance seam is Playwright through the React UI with real FastAPI, PostgreSQL and worker, replacing only external push delivery. Supporting seams are backend application operations with real PostgreSQL and controlled clocks for races/recovery, focused frontend interaction tests and Storybook, real-iPhone HTTPS/push acceptance, and isolated deployment/Terraform/restore verification. Do not add independent test interfaces per internal service/module when these boundaries suffice.
- Good tests assert externally meaningful behavior: accepted/rejected actions, visible data, permissions, preserved history, durable work, recipient eligibility and recoverability. Avoid private-helper assertions, implementation-mirroring tests and tests that merely repeat schema declarations. Inject controlled time and a recording/failing push transport at application boundaries; production behavior must not depend on a test endpoint. Keep the real worker and real PostgreSQL in integration/E2E coverage.
- **Prior art:** no application suites or reusable harnesses exist. The selected prototype guide records ad hoc Playwright checks at 390px and 1440px for active/empty states, duration chips, coffee-choice separation, non-coffee controls, collection and overflow. Reuse these scenarios as starting behavioral examples, applying final lifecycle/default rules. They prove neither full-stack persistence nor phone push. The delivery decision supplies the accepted verification matrix.
- **Backend units:** cover request snapshots and editing preservation, availability/quantity validation, shopping grouping and per-colleague unavailable outcomes, lifecycle/deadline boundaries, permissions, temporary credentials, last-administrator protection, departure/restoration/deletion, notification event/audience/privacy/reminder policies and current eligibility. Use controlled clocks around exactly-at-deadline, 12:00/18:00 office periods, 24-hour temporary-password expiry, 30-day session expiry and deadline changes.
- **PostgreSQL integration through application operations:** prove simultaneous announcements, request/close/cancel/collect races, concurrent last-administrator changes and membership removal effects with real transactions/constraints. Prove persisted jobs, worker crash/restart/claim recovery, logical reminder uniqueness across devices, rescheduling, suppression after submission/access loss/closure, and bounded useful retries. SQLite is not concurrency evidence.
- **Frontend units and Storybook:** test useful interactions and all production components' relevant variants/states: duration validation, choice/quantity/note editing, preserved/flagged requests, unavailable outcomes, confirmation, pending/errors, stale-state rejection, expiry/access loss, refreshed countdown/status, and push unsupported/denied/enabled/revoked states. Use accessible roles/labels and observable results.
- **Full-stack Playwright:** exercise bootstrap/forced password change and recovery, authentication/session expiry/revocation, all permission roles, menu maintenance and snapshot preservation, announce/join/edit/withdraw/deadline edits/early close/shopping/unavailable/collection/cancellation/history, membership removal/departure/restoration/deletion, preference/subscription ownership, worker scheduling and notification deep links. Assert persisted results after refresh/re-login, privacy and unauthorized denial, not just button clicks. Include two-user/racing-action scenarios. Capture transport attempts without notifying real colleagues.
- **Browser coverage:** desktop Chromium, Firefox and WebKit plus phone layouts; check at least the prototype reference widths and meaningful phone interactions/overflow. Browser emulation/WebKit cannot establish iPhone Home Screen push behavior.
- **Real-device release acceptance:** valid public HTTPS on a real iPhone at the minimum claimed supported baseline and current iOS; Home Screen installation/opening; explicit permission opt-in, denial, revocation and re-enable; foreground, background, locked and normally closed receipt; offline/reconnect and expiry; notification navigation to current state, including terminal/access-lost cases. Record device/OS/results; assess reboot/force-quit behavior separately rather than promise it. If adding declarative push, exercise both supported capability paths. Push remains best effort after successful trials.
- **Delivery/recovery checks:** gate deployment on applicable CI units/integration/E2E checks; verify pinned-image startup/health, secret mounts, private-registry cleanup, schema migration/initializer reruns without credential/grant changes, separate operator recovery, credential rotation and cold-boot unlock/login recovery. Verify encrypted archive restore before first use. Terraform checks include format, validation, plans, resource ownership, OIDC/bucket permissions, application destroy retaining foundation, foundation destroy-plan guards and archive-version retention. Any live smoke/destroy test uses isolated disposable resources, never production destructive testing.
- Use synthetic credentials, isolated PostgreSQL databases/volumes and independently named namespaces/storage prefixes for parallel jobs. Tests/development never dispatch colleague pushes or reset production state. Record actual completed checks; missing hardware/device/provider checks remain explicit release prerequisites, not implied passes.

## Out of Scope

- Native iOS/Android apps, multi-office behavior, multiple simultaneous active runs, Google/Apple SSO implementation or account-linking workflows.
- Invitations, public signup, automatic domain admission, verified-mailbox claims, SMTP delivery, self-service email recovery and email/SMS notification fallback. Future email verification remains separate backlog awaiting SMTP and policy choices.
- Payments, reimbursement, debt tracking, structured milk/size/other option groups, automatic substitutions, note-based price adjustments, in-app menu-correction reporting, avatars and public profiles.
- Per-item/per-shop collection verification, reopening terminal runs, Returned/back-at-office confirmation, collection messages promising physical arrival, chat, persistent notification inbox, required socket updates or guaranteed/on-time/exactly-once push delivery.
- Replacing macOS or selecting Colima, OCI, Vercel, Render or a paid VM as this release's host; high availability, guaranteed unattended cold boot, immutable storage guarantees or permanently free infrastructure claims.
- Implementing the application, provisioning resources or creating implementation tickets as part of this spec publication. Those are downstream implementation/to-tickets work.

## Further Notes

### Decision provenance and supersession

| Source | Authority carried into this spec and relationships |
| --- | --- |
| [Completed map](map.md) | Destination, scope and complete decision graph; all nine decision tickets are resolved. |
| [03 Visual direction, including comments](issues/03-visual-direction.md) | Approved Postcard Club and design-system approach; both shops, generated titles, choice separation and one collection action. Its remaining policy placeholders are settled by 01/02. |
| [Selected prototype](prototype/frontend-prototype.html), [comparison archive](prototype/frontend-comparison-prototype.html), [guide and recorded checks](prototype/README.md) | Read in full as visual/interaction evidence. Comparison multiple-run cards and selected-preview post-collection slot guard are superseded by 02. Sample Blend default/equal prices are superseded by 01; sample durations/time policy by 02. No decision-rich code snippet overrides those answers. |
| [01 Menus, including comments](issues/01-shop-menus.md) | Maintainer control, Specialty default, separate prices, quantities/notes and snapshot/availability preservation; 02 supplies request editing and run-specific outcomes; 06 supplies grants. |
| [02 Lifecycle, including comments](issues/02-run-lifecycle.md) | Authoritative states, collected terminal/slot release, 15-minute default, duration bounds, time rules, races and history. Supersedes prototype active-after-collection and any earlier Returned proposal. Feeds 05 notification events and 06 departure effects. |
| [04 iOS feasibility](issues/04-ios-web-push.md), [cited research](research/ios-web-push.md) | Platform conditions and test limits constrain 05/07; newer installation/declarative capabilities do not remove the older-baseline compatibility requirement. |
| [05 Notifications, including comments](issues/05-notifications.md) | Exact audiences/categories/reminder logic, optional setup, privacy and best-effort policy; 06 handles access loss and 07 delivery/recovery. |
| [06 Access, including comments](issues/06-office-access.md), [bootstrap research](research/account-bootstrap.md) | Manual creation replaces invitations. Separate accounts/memberships, runtime migration-then-initializer bootstrap, temporary passwords, removal/deletion and recovery. Research proposals are resolved by the ticket, not additional open decisions. |
| [08 Initial hosting comparison](issues/08-free-hosting-feasibility.md), [research](research/free-hosting.md) | Historical 24/7 free-host constraints, alternatives and evidence caveats; not a selected provider. |
| [09 Revised hosting comparison](issues/09-scheduled-worker-and-mac-mini.md), [seven-hour Vercel research](research/scheduled-vercel.md), [mini research](research/mac-mini-hosting.md) | Seven-hour clarification supersedes applying the earlier full-month Vercel rejection unchanged; feasibility is conditional. Linux preference is superseded by 07's macOS choice. |
| [07 Delivery, including all comments](issues/07-delivery-and-verification.md), [macOS/Actions research](research/macos-github-actions.md), [object storage research](research/object-storage.md), [secret audit](research/secret-custody.md) | Final Mac/Docker Desktop, Caddy, same-image worker, Actions, AWS/S3/Frankfurt, secret custody, retained-foundation boundary and verification plan. Weekly backups supersede daily/24-hour assumptions in early comments/research. Actions-orchestrated backup supersedes earlier host scheduling; application worker retains precise reminder responsibility. |
| [Future email verification](../email-verification/issues/01-end-to-end-email-verification.md) | Separate needs-info backlog, not a blocker, signup permission or first-release dependency. |

### Implementation prerequisites and handoff

- All product decisions are settled. Exact domain/zone/IP, repository identity/remote, GitHub plan capabilities, hardware/OS/runtime compatibility, provider/dependency pins, network routing, real menu content, backup sizing/cost and device availability are setup inputs/checks. S3 is metered; research is dated evidence rather than a current deployment, price or capacity guarantee. Verify selected versions/capabilities during implementation. If a prerequisite fails, revisit the affected deployment seam explicitly without silently changing product policy.
- This document is the consolidated build specification. Linked tickets retain original questions, comments and decision relationships; publication does not reopen them or change their resolved status. No implementation tickets are created here. The next planning handoff is to-tickets in dependency order.
- Publication changes planning documents only. No application/unit/Playwright/Storybook, real-device, infrastructure, restore or production checks were run for this handoff; those systems do not yet exist. Prior prototype results remain attributed historical evidence. The user confirmed the testing seams during this to-spec flow before publication.
