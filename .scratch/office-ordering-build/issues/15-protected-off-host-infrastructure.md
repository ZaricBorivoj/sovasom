# 15: Establish protected off-host infrastructure

Status: ready-for-agent
Blocked by: None (can start immediately)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** The operator can bootstrap protected AWS infrastructure, keep Terraform state recoverable off the mini and plan application teardown without losing retained storage.

- [ ] Create reproducible Terraform foundations for separate private S3 backup/state buckets in Frankfurt eu-central-1, encryption, public-access blocking, bucket/access policies, scoped IAM roles, OIDC trust and state version history. Use separate retained-foundation and disposable-application roots/states; application references retained infrastructure.
- [ ] Bootstrap using an authenticated operator session, establish native S3 locking with use_lockfile enabled, migrate initial state to the protected remote backend and document independent operator recovery. Keep Terraform state sensitive even when application secrets are excluded.
- [ ] Reuse/reference or deliberately import shared existing hosted zone and OIDC provider. Define the application DNS record using actual setup inputs. Scope GitHub trust to the real repository and intended trusted branch/environment subject; separate narrow infrastructure and backup workflow roles.
- [ ] Normal application destroy retains foundation buckets and contents. Retained buckets use prevent_destroy enabled and force_destroy disabled; foundation destroy planning fails with guards present. Explain configuration-removal/direct-AWS deletion limits and explicit full retirement. Backup expiry continues after app teardown; preserve state history/current state independently.
- [ ] Keep secret payloads out of Terraform inputs/state and avoid ownership overlap with Compose/host automation or Caddy TLS keys. Resolve actual identifiers, repository access and provider pins as setup configuration; do not fabricate provisioned resources or credentials.
- [ ] Run format/validation and inspect plans, remote locking/version recovery, scoped role/bucket permissions and separate state ownership. Use disposable resources for live smoke tests, verify retained resources on application teardown and guard failure on foundation destroy plans, and record actual evidence. Never perform a production destructive verification.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
