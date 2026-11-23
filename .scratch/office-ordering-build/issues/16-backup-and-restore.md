# 16: Back up and restore application data

Status: ready-for-agent
Blocked by: [01: Bootstrap and sign into the private office](01-bootstrap-private-office.md), [15: Establish protected off-host infrastructure](15-protected-off-host-infrastructure.md)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** The operator produces encrypted off-host backups, sees failures or stale backup age and restores a real archive into an isolated database before relying on recovery.

- [ ] Actions weekly and manual workflows assume a narrow backup AWS role through OIDC, trigger PostgreSQL-aware backup/public-recipient encryption over verified SSH on the mini, receive ciphertext and upload to S3. Reuse this path as a successful backup/upload gate before migrations of an existing database; empty first installation must work without a prior archive.
- [ ] Retain weekly and pre-migration archives for 30 days, including effective cleanup of noncurrent backup object versions if versioned. State lifecycle remains separate; never expire current Terraform state with the archive rule. Verify archive completeness and failed upload/backup outcomes.
- [ ] The mini holds no permanent AWS key or private decryption identity. Keep recoverable encryption identities in the operator password manager, inject private identities only temporarily for recovery and retain old identities until matching archives expire. Avoid plaintext or private secrets in logs/artifacts.
- [ ] Record last successful backup and age, report failed/stale backups and support manual retry. Document weekly cadence as approximately seven days potential data loss, possibly longer after delayed/missed jobs, with a one-working-day restoration objective conditional on host, network, access and keys.
- [ ] Restore an encrypted S3 archive into a fresh isolated PostgreSQL database and verify the ticket-01 sign-in/account data using the application. Prove retention/cleanup and failure/report/retry behavior on disposable namespaces, preserving independent operator access after mini loss. Record actual restore time and results; no reset of production volumes or storage prefixes.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
