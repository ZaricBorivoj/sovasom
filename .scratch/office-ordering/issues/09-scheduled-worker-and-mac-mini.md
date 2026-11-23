# Scheduled Vercel worker and Mac mini hosting feasibility

Parent: [Office coffee and bakery ordering](../map.md)
Label: wayfinder:research
Type: research
Status: resolved
Assignee: Nemanja.Tomic (research session)
Blocked by: None

## Question

Does limiting the worker to 08:00–15:00 change Vercel Hobby feasibility, and can the user's existing Intel Mac mini with a public static IP host the agreed app? Check schedule/timezone automation, resource quota arithmetic, PostgreSQL placement, after-hours work implications, native macOS versus dedicated Linux, Docker licensing/startup behavior, persistent storage, HTTPS/network prerequisites, Terraform scope on existing hardware, off-host backups/state and remaining costs. Use current primary sources; preserve unresolved user choices and do not provision or inspect the user's machine without authorization/access.

Record evidence in linked research assets. This follows [Free hosting feasibility for office ordering](08-free-hosting-feasibility.md) using newly supplied facts; the earlier 24/7 quota conclusion must not be applied unchanged to a seven-hour worker.

## Answer

Research checked 23 November 2026. Evidence: [Vercel Hobby with a seven-hour worker](../research/scheduled-vercel.md) and [Intel Mac mini hosting feasibility](../research/mac-mini-hosting.md).

At 1 GiB, seven hours daily over 31 days is nominally 217 memory-hours, below the current 420 daemon allowance. A worker must scale to zero, rather than sleep, outside the window. At default 2 GiB, 434 memory-hours exceeds it if running every day, while 23 weekdays is 322. CPU, traffic, database and other allowances still need sizing and measurement. Scaling through CLI/API is documented; a proposed scheduled controller can start early to accommodate jitter and startup time, but its readiness/recovery behavior is untested. A late run at the 15:00 cutoff requires a product decision. Vercel remains a plausible revised managed-service architecture, not a selected host or a validated free deployment.

The existing Intel Mac mini is a plausible single-host target preserving Compose, Caddy, modular FastAPI, same-image worker and persistent PostgreSQL. Prefer dedicated Linux conditionally on exact hardware compatibility and the user's OS choice. Native macOS alternatives involve supported-version, licensing, VM, sign-in and cold-boot/recovery considerations. Public static IP still requires reachable HTTPS, DNS and firewall/router configuration. Off-host backups and protected remote state remain required. Terraform manages provider-addressable infrastructure; separate automated host configuration and releases cover the existing machine.

Hardware model/RAM/storage, OS choice, exact operating days, cutoff semantics, host selection, domain, state/backup destination and readiness/restore verification remain live decisions in [Delivery architecture and verification approach](07-delivery-and-verification.md). No machine was inspected or provisioned, no configuration deployed and no payment commitment made. No research branch could be published because the repository has no commits or remote.
