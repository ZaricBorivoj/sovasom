# Office ordering implementation tickets

Approved breakdown published on 23 November 2026 using the to-tickets flow.

Source: [approved specification](../office-ordering/spec.md). The source spec, map and resolved decision tickets remain unchanged. Implementation numbering is local to this directory; it does not refer to wayfinding decision numbers.

Each issue is ready-for-agent. Work only the frontier: tickets with no blockers, or whose listed blockers are all done. Initially **01 and 15** can start. Ready-for-agent describes specification readiness, not completion of dependencies. Record implementation completion with Status: done.

| Ticket | What it delivers | Blocked by |
| --- | --- | --- |
| [01](issues/01-bootstrap-private-office.md) | Bootstrap and sign into the private office | None |
| [02](issues/02-colleagues-and-permissions.md) | Add colleagues and assign permissions | [01](issues/01-bootstrap-private-office.md) |
| [03](issues/03-profile-and-credential-recovery.md) | Manage profiles and recover credentials | [02](issues/02-colleagues-and-permissions.md) |
| [04](issues/04-maintained-shop-menus.md) | Maintain and browse both shop menus | [01](issues/01-bootstrap-private-office.md) |
| [05](issues/05-announce-active-run.md) | Announce the office’s single active run | [01](issues/01-bootstrap-private-office.md) |
| [06](issues/06-submit-preserved-request.md) | Submit a request with preserved item details | [04](issues/04-maintained-shop-menus.md), [05](issues/05-announce-active-run.md) |
| [07](issues/07-edit-withdraw-request.md) | Edit and withdraw requests before closing | [06](issues/06-submit-preserved-request.md) |
| [08](issues/08-shop-and-finish-run.md) | Close requests, shop and finish a run | [06](issues/06-submit-preserved-request.md) |
| [09](issues/09-unavailable-outcomes-history.md) | Record unavailable quantities and inspect history | [08](issues/08-shop-and-finish-run.md) |
| [10](issues/10-membership-lifecycle.md) | Leave, remove and restore office membership | [02](issues/02-colleagues-and-permissions.md), [07](issues/07-edit-withdraw-request.md), [09](issues/09-unavailable-outcomes-history.md) |
| [11](issues/11-delete-account.md) | Delete an account while preserving shared history | [10](issues/10-membership-lifecycle.md) |
| [12](issues/12-enable-push-new-runs.md) | Enable device push and receive new-run notifications | [03](issues/03-profile-and-credential-recovery.md), [05](issues/05-announce-active-run.md) |
| [13](issues/13-joined-run-updates.md) | Receive updates to runs joined | [09](issues/09-unavailable-outcomes-history.md), [10](issues/10-membership-lifecycle.md), [12](issues/12-enable-push-new-runs.md) |
| [14](issues/14-closing-reminders.md) | Receive one timely closing reminder | [07](issues/07-edit-withdraw-request.md), [08](issues/08-shop-and-finish-run.md), [12](issues/12-enable-push-new-runs.md) |
| [15](issues/15-protected-off-host-infrastructure.md) | Establish protected off-host infrastructure | None |
| [16](issues/16-backup-and-restore.md) | Back up and restore application data | [01](issues/01-bootstrap-private-office.md), [15](issues/15-protected-off-host-infrastructure.md) |
| [17](issues/17-deploy-mac-mini.md) | Deploy and recover the application on the Mac mini | [16](issues/16-backup-and-restore.md) |
| [18](issues/18-iphone-release-acceptance.md) | Verify real-iPhone push and release readiness | [11](issues/11-delete-account.md), [13](issues/13-joined-run-updates.md), [14](issues/14-closing-reminders.md), [17](issues/17-deploy-mac-mini.md) |

Application tickets include schema/API/UI behavior and meaningful tests/stories together. Infrastructure tickets deliver verifiable operator workflows. Ticket 18 is real-environment/device acceptance; it does not defer automated testing from earlier tickets. Configured host/account/domain/device inputs remain implementation prerequisites from the spec, not reasons to reopen settled product decisions.
