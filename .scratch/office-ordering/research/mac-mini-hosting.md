# Intel Mac mini hosting feasibility

Checked 2026-11-23 against primary documentation. Recommendation is conditional: exact model, RAM, available disk, supported macOS, T2 presence, and permission to replace macOS remain unanswered. No machine was inspected or provisioned.

## Recommendation and architecture

**An existing Intel Mac mini with reachable public static IP is a plausible single-host deployment. Prefer dedicated Linux with Docker Engine and Compose if hardware compatibility and replacing macOS are confirmed.** This is an operational recommendation, not a capacity guarantee. Linux Docker can start at boot without desktop login; Debian/Ubuntu do this by default. [Docker boot configuration](https://docs.docker.com/engine/install/linux-postinstall/)

Proposed Compose services: Caddy, FastAPI API, PostgreSQL, and a worker using the **same backend image/code** with a separate command. Caddy serves the React/Vite build and proxies API traffic; Node/Vite need not run continuously. Vite builds static assets into `dist`; its preview server is not intended for production. [Vite deployment](https://vite.dev/guide/static-deploy.html)

Use database readiness checks, connection retries, controlled migrations, restart policies, bounded logs, and external availability monitoring. Compose startup order alone does not establish database readiness. `unless-stopped` restarts failed containers and running containers after daemon restart, but preserves explicit stops. [Compose readiness](https://docs.docker.com/compose/how-tos/startup-order/), [restart policies](https://docs.docker.com/engine/containers/start-containers-automatically/)

Worker design recommendation: keep scheduling decisions in shared application code, use `Europe/Belgrade`, persist due work, and process idempotently with database locking. A seven-hour execution window should pause processing, not power off the database/API. Define after-15:00 deadline/reminder behavior and restart catch-up explicitly; hosting does not resolve those product rules.

## Operating system choices

**Dedicated Linux:** least moving parts for unattended service operation. Do not assume generic Linux installs cleanly on every Intel mini. T2 machines can require specialized installation instructions, firmware/drivers and disabling Apple Secure Boot; validate the exact model and wired networking/storage first. [t2linux feature matrix](https://wiki.t2linux.org/state/), [installation prerequisites](https://wiki.t2linux.org/guides/preinstall/)

**Keep macOS with Docker Desktop:** Intel downloads remain available; Docker requires at least 4 GB RAM and supports the current plus two preceding major macOS releases. That minimum is for Desktop, not a sizing promise for this stack. An old mini unable to run a supported macOS fails this route's support requirement. Desktop's documented automatic startup occurs **when signing in**. [Mac requirements](https://docs.docker.com/desktop/setup/install/mac-install/), [startup settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/)

For professional use, Desktop is free for businesses with **fewer than 250 employees AND less than US$10m annual revenue**; larger organizations/government require paid licensing. Ownership of the computer does not establish eligibility for office use. Docker Engine's open-source licensing is separate. [Docker licensing](https://docs.docker.com/subscription-billing/desktop-license/)

**Keep macOS with a lightweight Linux VM:** Colima supports Intel macOS and Docker containers. It is worth evaluating if Desktop licensing matters, but adds VM networking/storage/startup management; confirm supported host dependencies and unattended cold boot before choosing it. It does not remove host unlock requirements. [Colima project](https://github.com/abiosoft/colima)

For either OS, disable sleep and test recovery from power loss. Apple documents automatic restart after power failure; FileVault disables automatic login and can require an authorized unlock before service recovery. Linux disk-encryption unlock needs its own deliberate recovery design. Do not promise unattended cold boot until a real test passes; retain recovery keys separately and consider a UPS. [Apple power recovery](https://support.apple.com/en-by/guide/terminal/apd7d247a89-3560-4c3b-a471-3e66ff607040/2.15/mac/27), [FileVault/login](https://support.apple.com/en-ge/guide/mac-help/mchlp1158/27/mac/27)

## Network, persistence and automation

Provide a domain/subdomain, correct A/AAAA records, router forwarding where NAT exists, host/router firewall rules and ISP allowance for inbound TCP 80/443. A static IP alone is insufficient. Caddy can automate certificate issuance/renewal; DNS challenges can avoid inbound validation ports but do not make an unreachable application accessible. Publish only the proxy; keep PostgreSQL private. [Caddy HTTPS requirements](https://caddyserver.com/docs/quick-starts/https), [ACME challenges](https://caddyserver.com/docs/automatic-https)

Use persistent PostgreSQL and Caddy data volumes. Volumes survive container deletion but remain vulnerable to host/disk loss. Schedule encrypted off-host PostgreSQL dumps, retention and restore drills; copying live database files is not the proposed backup method. [Docker volumes](https://docs.docker.com/engine/storage/volumes/), [PostgreSQL pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html)

**Terraform remains mandatory:** manage provider-addressable DNS, backup storage/access policies and state infrastructure. The existing physical mini cannot be created by Terraform; importing requires a matching provider resource. Use separate idempotent bootstrap/configuration/deployment automation for OS packages, firewall, Compose files, secrets and releases. Avoid presenting shell provisioners as complete declarative host management; HashiCorp recommends purpose-built alternatives. Give each resource one owner; do not also manage Compose-owned containers through Terraform's Docker provider. [Cloudflare provider](https://developers.cloudflare.com/terraform/), [Terraform import](https://developer.hashicorp.com/terraform/language/import/single-resource), [provisioner guidance](https://developer.hashicorp.com/terraform/language/provisioners)

Keep protected remote Terraform state off the mini, with locking/versioning and recovery access independent of it. S3 supports `use_lockfile` and recommends bucket versioning. [S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3)

Budget still includes electricity, connectivity, domain renewal where needed, off-host backup/state storage, maintenance and possible UPS/replacement disks or Desktop licensing. Exact costs and capacity require hardware/provider choices; existing hardware removes server rental, not operational responsibility.
