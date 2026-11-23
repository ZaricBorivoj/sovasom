# Free hosting feasibility for office ordering

Parent: [Office coffee and bakery ordering](../map.md)
Label: wayfinder:research
Type: research
Status: resolved
Assignee: Nemanja.Tomic (research agent)
Blocked by: None

## Question

Can free hosting, especially Vercel Hobby, support this private office ordering app and its agreed architecture? Compare current primary-source plan eligibility, commercial/internal office use restrictions, FastAPI and React hosting, continuously available scheduled work (one-minute runs and two-minute-before-close reminders), PostgreSQL durability, sleep/reclamation/expiration, outbound Web Push, Terraform coverage, backups and state needs. Contrast credible free alternatives with a small paid single-host baseline. Distinguish free ongoing allocations from trials, remaining costs, and any architecture/product changes required. Provider selection remains the live decision in [Delivery architecture and verification approach](07-delivery-and-verification.md).

Capture checked-date findings and direct citations in `../research/free-hosting.md`. Do not provision resources or assume permission to change the architecture. Record platform facts and evidence gaps; conclude with design recommendations clearly marked as recommendations.

## Answer

Resolved through primary-source research checked 23 November 2026. See [Free hosting feasibility](../research/free-hosting.md) for the comparison, citations, discrepancies between cached and live documentation, and unverified deployment assumptions.

OCI Always Free is the evaluated ongoing free option compatible with the accepted single-host Compose architecture, subject to capacity and idle reclamation. Free compute cannot assure replacement within the recovery target. Current Vercel Hobby includes beta container Daemons, but the minimum instance exhausts the documented free memory allowance before a full month; its scheduled alternatives are too imprecise for closing reminders. Render Free has idle sleep, ephemeral web-service storage, an expiring database and no free dedicated worker. A small paid EU VM is the operational baseline; the report labels the Hetzner price evidence provisional rather than a verified live quote.

Terraform providers exist for the evaluated services; new Vercel beta feature coverage remains unestablished. OCI Object Storage with its native Terraform backend offers a possible free encrypted, locking, versioned state store independent of the host, sharing storage/request allowances with any backups. Provider selection, fallback, region and operational details remain with [Delivery architecture and verification approach](07-delivery-and-verification.md); research does not approve a deployment or alter the architecture.

No resources were provisioned, tests run, or payment commitments made. Repository has no commits or remote, confirmed during research; evidence remains local because a research branch could not be published.
