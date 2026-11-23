# Office membership and account lifecycle

Parent: [Office coffee and bakery ordering](../map.md)
Label: wayfinder:grilling
Type: grilling
Status: resolved
Assignee: Nemanja.Tomic (Codex session)
Blocked by: None

## Question

How will administrator-provisioned office membership and email/password accounts work? Decide how administrators add users and manage membership, how the first administrator starts, verification and password recovery behavior, permissions, and account removal. Determine the identity boundary that will allow later Google or Apple SSO without choosing a provider prematurely.

## Comments

### 20 November 2026 — menu decision handoff

Carry forward the designated menu-maintainer capability and initial maintainer from [Shop menus and item choices](01-shop-menus.md#menu-ownership-and-corrections). Decide who can assign or remove that permission as part of office access; menu ownership and the external correction workflow are already settled.


### 20 November 2026 — lifecycle decision handoff

Carry forward [Run lifecycle and closing rules](02-run-lifecycle.md#answer): office administrators can cancel an active run to recover abandoned runs; decide assignment of this permission here. Current office members can view retained completed/cancelled history and request details. Decide how account removal affects historical attribution and personal data, including removal of a runner with an active run, without reopening the confirmed lifecycle.


### 20 November 2026 — notification decision handoff

Carry forward [Notification experience and preferences](05-notifications.md#answer): category settings are account-wide, push setup is per device, and signing out stops delivery to that session. Notification audiences require current office access. Decide membership/account removal consequences for notification access alongside the existing account lifecycle questions; notification categories, onboarding and sign-out behavior are settled.


### 23 November 2026 — first access round

User confirmed separate accounts and office memberships, limited to the single office in this version. Membership removal revokes office access; account deletion is separate. Future Google/Apple sign-in can attach to the same account.

Confirmed administrator permissions: add/remove members, grant/revoke administrator and menu-maintainer permissions, and cancel active runs. All members may announce runs and manage their own requests. Menu maintenance requires its own permission; retain at least one administrator. The proposed initial administrator is also the initial menu maintainer, but the user explicitly requires runtime provisioning rather than a hardcoded person; bootstrap details remain open.

User replaced invitations with manual user creation by the “superuser.” No invitations or public signup in this version. Clarify whether superuser means the office administrator or a separate authority; initial credentials and recovery remain open.

Confirmed required, self-editable display names; email visible only to the account holder and administrators. No avatars or public profiles in the first version.

Ticket remains claimed and unresolved pending the remaining live discussion.

Bootstrap evidence and proposals: [Initial administrator and manually created accounts](../research/account-bootstrap.md). Runtime provisioning is confirmed; the exact command, credentials, verification and recovery policies await discussion.

### 23 November 2026 — second access round

User answered yes to all three recommendations:

- “Superuser” means office administrator; no separate application role. The runtime-created first administrator can appoint equal administrators.
- Membership removal immediately revokes office access on all devices and stops future notifications. Removing an active runner warns and cancels that run as part of removal. Removing another participant withdraws their request while accepting requests; once Shopping begins, preserve their request. Retain past run/request attribution after membership removal. Block removal of the last administrator.
- Administrators change account email; members can change their own display name and password. Email changes preserve account identity/history, reject duplicate addresses, and end existing sessions. Verification and credential setup remain open.

This ticket remains claimed pending bootstrap, credential, recovery and departure/deletion decisions.

### 23 November 2026 — third access round

User accepted the one-time runtime bootstrap direction, proposing that ORM migrations handle initial administrator creation with credentials supplied through `.env`. The precise relationship between schema migrations and initial account seeding is being clarified; no application configuration or credentials have been created.

User confirmed administrator-assisted credentials and recovery for the first version: generate a temporary password shown once for private handoff; expire it after 24 hours; require a personal password before office access. Administrators confirm identity outside the app. Email is a login identifier, not a verified mailbox. Password reset/change ends existing sessions and their push delivery. Email changes require a new temporary password. Forgotten-password guidance directs users to an administrator, with operator recovery for administrator lockout.

User requested a future backlog ticket for end-to-end email verification after choosing an SMTP server: [End-to-end email verification](../../email-verification/issues/01-end-to-end-email-verification.md). This is implementation backlog outside this wayfinding map, not an unresolved first-version dependency.

User confirmed self-service departure using the agreed removal rules, including active-run warnings and last-administrator protection. The account survives without office access. An administrator can restore membership to the same account; administrator/menu-maintainer permissions do not return automatically, and old requests do not reactivate.

User confirmed separate, administrator-assisted account deletion after the account holder's request is confirmed. Apply membership-removal rules first; delete credentials, email, display name, preferences and device registrations. Retain run/item/quantity/outcome history under “Deleted colleague” and clear free-text notes from that person's requests. Block deletion of the last administrator until another is appointed. Deletion is irreversible; a later account is not linked to the deleted identity.

### 23 November 2026 — bootstrap confirmed

User answered yes to the final bootstrap proposal: one setup command loads runtime `.env` configuration, runs schema migrations, then creates the initial account and permissions through an ORM initializer outside versioned migration files. This settles the remaining decision.

## Answer

Resolved through live discussion, including the final bootstrap confirmation. The following consolidates the accepted decisions; earlier comments preserve the discussion rather than additional unresolved requirements.

### Account and membership boundary

One person has one account, separate from membership of the private office. The first version supports the single office. Administrators manually create users; no invitations, public signup or automatic admission by email domain.

Membership removal revokes office access without deleting the account. Keep account identity independent of a mutable email address or password so later Google/Apple sign-in can attach to the same account. SSO implementation and provider/linking workflows remain outside the first version; no provider is chosen here.

### Permissions and profile

- All current members can announce runs, manage their own requests within the lifecycle rules, and view retained office run history.
- Office administrators create users, remove/restore memberships, grant/revoke administrator and menu-maintainer permissions, change account email, and cancel active runs. “Superuser” refers to this role, not a separate application role. Administrators have equal authority.
- Menu maintenance requires its own permission. The runtime-created initial administrator receives it; additional grants are explicit.
- Preserve at least one administrator: block removing, demoting, leaving or deleting the last administrator.
- Require a self-editable display name. Email is visible only to the account holder and administrators. No avatars or public profiles in this version.
- Members may change their own password. Administrators change email without changing account identity/history; reject duplicate email addresses. Email changes end existing sessions and require a new temporary password.

### Runtime bootstrap and operator recovery

Use one setup command/preparation job that loads the initial administrator's email, display name and password from runtime `.env` configuration, runs schema migrations, then creates the account, office membership, administrator and menu-maintainer permissions through the ORM. Keep this initializer outside versioned schema migration files. No person or password is hardcoded.

Create the initial account and permissions together. After successful initialization, reruns leave credentials and permissions unchanged, even if `.env` values change; bootstrap must not become a recurring password reset or privilege-grant mechanism. Keep `.env` out of Git and remove the bootstrap password after use. Provide a separate explicit operator recovery command for a locked-out sole administrator.

The deployment sequence, configuration wiring and meaningful verification are carried to [Delivery architecture and verification approach](07-delivery-and-verification.md). Supporting primary-source evidence and the distinction between framework guidance and our chosen design are in [Initial administrator and manually created accounts](../research/account-bootstrap.md).

### Initial credentials, password changes and recovery

For administrator-created accounts and administrator-assisted resets, generate a temporary password displayed once for private handoff. It expires after 24 hours. A temporary credential allows choosing a personal password, not office access before that change. Administrators confirm the colleague's identity outside the app before handoff.

Changing or resetting a password ends existing sessions and their push delivery. Forgotten-password guidance directs the person to an administrator; operator recovery covers administrator lockout. Do not retrieve or display existing passwords.

Email is a login identifier; mailbox ownership is not verified in this version. [End-to-end email verification](../../email-verification/issues/01-end-to-end-email-verification.md) is the user-requested future backlog, awaiting SMTP selection and verification policy. It does not block the first version or authorize public registration.

### Leaving, removal and return

Administrators can remove a membership; members can leave with confirmation. Revoke office access on every device immediately and stop future notifications. Apply these rules with the access change:

| Situation | Effect |
| --- | --- |
| Departing member is runner of an active run | Warn and cancel the run as part of removal/departure, preserving cancelled history and releasing the active-run slot. |
| Departing member is another participant while requests are open | Withdraw their request. |
| Departing member is another participant during Shopping | Preserve their request so the shopping list does not unexpectedly lose items. |
| Earlier completed/cancelled runs | Retain attribution and request history after membership removal. |
| Last administrator | Block departure/removal until another administrator is appointed. |

The account survives without office access. An administrator can later restore membership to that same account. Administrator/menu-maintainer permissions are not restored automatically; old requests do not reactivate. Notification audiences still require current access under [Notification experience and preferences](05-notifications.md#answer).

### Account deletion

Deletion is a separate administrator-assisted action after confirming the account holder's request. Apply membership-removal rules first, including active-run handling and last-administrator protection. Delete credentials, email, display name, preferences and device registrations. Remove identifying attribution from retained run/request records and show “Deleted colleague”; retain shared run/item/quantity/outcome history. Clear free-text notes from that person's requests.

Deletion is irreversible. A subsequently created account has no link to the deleted identity. Retaining named history after membership removal does not override these deletion rules.

### Handoff and verification

[Delivery architecture and verification approach](07-delivery-and-verification.md) is now unblocked. It owns deployment, session enforcement and revocation, notification eligibility, bootstrap/recovery mechanics, test isolation and the verification plan. Carry the above product rules into backend/frontend tests, stories for relevant component states, and integrated Playwright workflows when implemented.

No additional in-scope decision ticket emerged. The requested email-verification backlog is outside this map's destination. Only this decision ticket is resolved; no production code, credentials or runtime `.env` file was created. Application tests and Storybook were not run because this session changed planning documents only.
