# Office coffee and bakery ordering

Label: wayfinder:map

Spec handoff: [Consolidated build specification](spec.md) — published with `ready-for-agent` status on 23 November 2026 after user confirmation of testing seams. Next: `to-tickets`.

## Destination

Agree on a build-ready plan for the first usable office ordering web app, including a chosen frontend direction, run and menu behavior, account access, and a feasible iOS web push experience. Hand off to `to-spec`, then `to-tickets`; this map does not implement the application.

## Notes

- User-confirmed direction: a web application, with one private office group initially. Administrators manually add users; invitations and public signup are excluded for the first version, superseding the original invitation-only proposal. Everyone in the group can announce a run. See [Office membership and account lifecycle](issues/06-office-access.md).
- Every run visits both the coffee shop and the bakery; requests remain grouped by shop. See the live feedback in [Explore and choose the frontend direction](issues/03-visual-direction.md).
- Colleagues choose from maintained shop menus. Updated title, closing-duration and collection requirements are recorded in [Explore and choose the frontend direction](issues/03-visual-direction.md).
- Payments and debt tracking stay outside the first version.
- Frontend exploration is resolved; follow the chosen direction and confirmed requirements in [Explore and choose the frontend direction](issues/03-visual-direction.md). The app must work on phones and desktop browsers.
- Notification product policy is resolved in [Notification experience and preferences](issues/05-notifications.md); carry it forward alongside the lifecycle and cited push feasibility constraints. Delivery architecture and verification are resolved in their decision ticket below.
- Start with email/password; Google or Apple SSO is a later extension.
- Follow `AGENTS.md`: FastAPI, React 19/Vite, PostgreSQL in Docker, a frontend design system, Storybook, frontend/backend unit tests, and Playwright end-to-end tests.
- Automate all applicable infrastructure with Terraform, following the ownership and retained-storage boundaries in [Delivery architecture and verification approach](issues/07-delivery-and-verification.md).
- Host on the user's Intel Mac mini running macOS/Docker Desktop, with infrastructure and deployment workflows driven by GitHub Actions. See [Delivery architecture and verification approach](issues/07-delivery-and-verification.md) for configuration, weekly backups, secret custody and verification.
- Consult `grilling` and `domain-modeling` for discussions; use `prototype` for visual exploration and `research` for external facts. Use `GLOSSARY.md` terminology.
- This is a local Markdown tracker. Tickets carry `wayfinder:` labels and the tracker-defined `Type:`, `Status:`, and `Blocked by:` fields. Open tickets are discovered from `issues/`, not listed in this map.
- The repository has no commits or remote at charting time. Research evidence is retained locally and linked from its ticket; branch publication is unavailable in this state.

## Decisions so far

- [Free hosting feasibility for office ordering](issues/08-free-hosting-feasibility.md): Initial 24/7 cloud comparison identified OCI availability risks and Vercel/Render free-plan constraints; the later seven-hour worker clarification is evaluated separately below.

- [Scheduled Vercel worker and Mac mini hosting feasibility](issues/09-scheduled-worker-and-mac-mini.md): Seven-hour Vercel workers are plausible within memory quota; the user's existing mini supports the selected Docker deployment direction, detailed in the delivery decision.

- [Establish iOS web push feasibility](issues/04-ios-web-push.md): Home Screen web push is feasible; installation, opt-in, best-effort delivery, and real-device verification constrain the experience. See the ticket for cited platform details.

- [Explore and choose the frontend direction](issues/03-visual-direction.md): Postcard Club and the refined interaction layout approved; see the prototype and compatible React design-system approach in the decision ticket.

- [Shop menus and item choices](issues/01-shop-menus.md): Maintainer-managed menus, Specialty-default coffee choices, prices, notes, availability, and preservation of submitted request details agreed.

- [Run lifecycle and closing rules](issues/02-run-lifecycle.md): Collection ends the run and releases the slot; request deadlines, editing, cancellation, unavailable outcomes, concurrency and history agreed.

- [Notification experience and preferences](issues/05-notifications.md): Event audiences, one closing reminder, account preferences, optional device setup, private messages and best-effort delivery agreed.

- [Office membership and account lifecycle](issues/06-office-access.md): Administrator-created accounts, runtime bootstrap, temporary passwords, permissions, departure/removal and deletion agreed; email verification deferred.

- [Delivery architecture and verification approach](issues/07-delivery-and-verification.md): macOS mini/Compose, GitHub Actions delivery, Terraform-managed AWS/S3 with retained storage, weekly backups, secret custody and full-stack/device verification agreed.

## Not yet specified

- None. All decision tickets are resolved; the map is ready for `to-spec`, then `to-tickets`. Implementation and environment/device verification are downstream work.

## Out of scope

- Native iOS or Android applications.
- Implementing Google or Apple SSO in the first version; preserve an extension path during account design.
- Mailbox ownership verification in the first version; [End-to-end email verification](../email-verification/issues/01-end-to-end-email-verification.md) is future backlog awaiting SMTP selection.
- Payment processing, reimbursement, and debt tracking.
- Building production application features during wayfinding.
