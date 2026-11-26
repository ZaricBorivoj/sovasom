# Infrastructure verification evidence

Public evidence records reproducible checks without operator account IDs,
hostnames, IP addresses, bucket/role names, user identities or OIDC subject IDs.
Keep deployment-specific discovery, plans and live recovery results in private
operator notes alongside the ignored local configuration.

## Automated checks

- Foundation mock plans cover retained/private/encrypted/versioned storage,
  archive lifecycle, TLS-only policy, scoped workflow roles and exact OIDC trust.
- PR and wildcard OIDC subjects are rejected.
- Application mock plans cover DNS creation and invalid address/zone inputs.
- Destroy plans against synthetic local state reject foundation bucket deletion
  and restrict application deletion to the application's DNS record.
- Corporate CA onboarding tests use disposable shell profiles.
- Terraform example checks reject deployment strings in public input templates.

Run the commands in the infrastructure runbook to reproduce these checks.
Synthetic tests establish configuration behavior; actual IAM, locking, recovery,
retention and deployment checks require isolated live resources and private
operator evidence. Infrastructure must be applied only at the operator's request.
