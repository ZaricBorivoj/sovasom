# 18: Verify real-iPhone push and release readiness

Status: ready-for-agent
Blocked by: [11: Delete an account while preserving shared history](11-delete-account.md), [13: Receive updates to runs joined](13-joined-run-updates.md), [14: Receive one timely closing reminder](14-closing-reminders.md), [17: Deploy and recover the application on the Mac mini](17-deploy-mac-mini.md)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** The operator has recorded evidence that the assembled release and optional push experience work on the claimed iPhone baseline and current iOS, with recovery and automated checks already in place.

- [ ] Use valid public HTTPS and synthetic office accounts on an isolated acceptance deployment. Record actual device/OS and minimum claimed support; test Home Screen add/open, user-gesture opt-in, denial, revocation and re-enable. Ordinary iOS tabs and Playwright WebKit do not establish installed-app push delivery.
- [ ] Observe delivery in foreground/background/locked/normally closed states, offline/reconnect before/after useful TTL, and current-state navigation for open/collected/cancelled or access-lost runs. Check privacy, relevant categories and stale-event behavior. Assess force-quit/reboot separately; do not turn an observed delivery into a guarantee. If declarative push is added, verify both supported capability paths.
- [ ] Verify logout/session expiry/credential reset, office departure and account deletion stop future eligible delivery across configured devices, while current request/history outcomes and non-push usability remain correct. Only controlled synthetic acceptance recipients may receive real test pushes.
- [ ] Confirm applicable CI units, real-PostgreSQL concurrency/recovery coverage, integrated Playwright in desktop Chromium/Firefox/WebKit and phone layouts, and all component stories are present and passing. Tests belong to their preceding slices; this ticket records assembled release evidence and resolves environment/device defects rather than postponing core implementation testing.
- [ ] Collect actual deployment, cold-boot, encrypted-restore, backup-retention and Terraform protection results from operator slices. List failed/unperformed device/setup checks explicitly and do not claim unsupported coverage. Complete the first-usable-release checklist only when the agreed device and operational prerequisites are verified.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
