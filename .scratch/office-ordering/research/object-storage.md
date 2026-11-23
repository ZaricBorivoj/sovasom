# Off-host object storage

Checked **23 November 2026**. Research only; no resources or accounts changed. Context: existing Intel Mac mini with Docker Desktop, AWS DNS, Terraform-managed provider infrastructure, encrypted off-host PostgreSQL backups targeting at most 24 hours of loss, and encrypted remote Terraform state with locking and version history.

## Recommendation

**Use two private AWS S3 Standard buckets if a small ongoing metered bill is acceptable:** one for database archives and one for Terraform state. This reuses the user's AWS account and satisfies the state requirements without another service. This is an engineering recommendation; backup size, retention, region, request volume and account eligibility have not been measured. PostgreSQL's live data stays on its Docker volume; these buckets hold recoverable copies and infrastructure state.

S3 charges for storage, requests and potentially transfer; it is **not a permanently free storage recommendation**. Current new-customer offers are time-limited credits: the free account plan lasts up to six months, and credits expire within twelve months. Do not assume an existing AWS DNS account qualifies. [S3 pricing and Free Tier terms](https://aws.amazon.com/s3/pricing/), [AWS Free Tier](https://aws.amazon.com/free/).

For state, enable bucket versioning and Terraform's `use_lockfile = true`; locking is otherwise off. Native S3 locking removes the need for a new DynamoDB table; DynamoDB locking is deprecated. S3 encrypts all new objects at rest with SSE-S3 at no extra encryption charge. Keep IAM access to state separate from the host's backup credentials. [Terraform S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3), [SSE-S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingServerSideEncryption.html).

## Free alternatives

**OCI Object Storage is the coherent free option for both purposes.** An Always-Free-only account has 20 GB combined storage and 50,000 requests/month. Paid/trial accounts instead have 10 GB per storage tier, so do not describe their Standard allowance as 20 GB. The native Terraform `oci` backend supports conditional-object locking and recommends bucket versioning. OCI encrypts objects at rest by default; versioning retains older and deleted versions, which consume storage. Use separate state/backup buckets and lifecycle retention within the allowance. Account setup and eligibility remain unverified. [Free allocation](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm), [OCI backend](https://developer.hashicorp.com/terraform/language/backend/oci), [encryption](https://docs.oracle.com/en-us/iaas/Content/Security/Reference/objectstorage_security.htm#Data_Encryption), [versioning](https://docs.oracle.com/en-us/iaas/Content/Object/Tasks/usingversioning.htm).

**Cloudflare R2 is attractive for backups, but does not independently meet the agreed state-history requirement.** Standard storage includes 10 GB-month, one million Class A and ten million Class B operations monthly, with free Internet egress; overages are billed. R2 now documents atomic conditional writes, so lack of conditional locking is not the objection. Its current S3 compatibility table still marks bucket versioning APIs unimplemented. Timestamped backup filenames preserve multiple archives, but do not create automatic Terraform state version history. Choose a separate versioned state backend or OCI for both. [R2 pricing](https://developers.cloudflare.com/r2/pricing/), [current API support](https://developers.cloudflare.com/r2/api/s3/api/).

## Before implementation

Resolve AWS metered storage versus another free account, region and retention. Bootstrap state-bucket infrastructure separately and preserve bootstrap state away from the mini. Schedule PostgreSQL-aware encrypted archives sufficiently often to maintain the 24-hour target, alert on stale successful backups, keep recovery keys independently accessible, and verify restoration. No restore or quota-sizing test has run.
