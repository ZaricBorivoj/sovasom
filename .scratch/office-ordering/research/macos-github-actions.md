# macOS Mac mini and GitHub Actions feasibility

Checked 2026-11-23 against primary documentation. Planning assumes macOS and automated deployments; exact Mac model, CPU, macOS version, and network reachability remain implementation prerequisites.

## Recommended arrangement

Use GitHub-hosted Ubuntu runners for unit tests, full-stack Playwright tests, image builds, and GHCR publishing. GitHub requires Linux runners for Actions job/service containers; Ubuntu is the hosted option. GitHub documents building and publishing images to its registry from Actions. Publish `linux/amd64` for an Intel Mac; confirm CPU before fixing the platform, or publish both AMD64 and ARM64. Docker documents multi-platform builds in Actions. [GitHub service containers](https://docs.github.com/en/actions/tutorials/use-containerized-services/use-docker-service-containers), [GHCR publishing](https://docs.github.com/en/actions/tutorials/publish-packages/publish-docker-images), [Docker platform builds](https://docs.docker.com/build/ci/github-actions/multi-platform/).

Deployment recommendation: a GitHub workflow invokes a versioned deployment script over SSH through a private network connection, pulling an immutable image and running Compose on the Mac. This is an architecture inference: GitHub supports private-network overlays from hosted runners, but connectivity, SSH identity/host verification, and Mac permissions must be provisioned. [GitHub private networking](https://docs.github.com/en/actions/how-tos/manage-runners/github-hosted-runners/connect-to-a-private-network).

A deploy-only self-hosted runner on the Mac is an alternative when hosted-runner access is inconvenient: it receives jobs through outbound HTTPS on port 443 and supports macOS. It adds a continuously available runner to maintain. macOS runner jobs must use shell commands for Compose rather than Actions' native container/service declarations. Keep CI builds/tests on hosted Ubuntu. [Self-hosted runner requirements](https://docs.github.com/en/actions/reference/runners/self-hosted-runners).

## macOS container runtime

Colima supports Intel and Apple Silicon and currently requires macOS 13+. Pair it with Docker CLI and Compose; Homebrew documents `brew install docker-compose` and the plugin search-path configuration needed for `docker compose`. Colima uses Lima for its Linux runtime. [Colima FAQ](https://github.com/abiosoft/colima/blob/main/docs/FAQ.md), [Colima installation](https://github.com/abiosoft/colima/blob/main/skills/references/install.md), [Compose formula](https://formulae.brew.sh/formula/docker-compose).

Colima recommends `brew services start colima`. Homebrew specifies that ordinary services are LaunchAgents started at **login**, while privileged service registrations use LaunchDaemons at boot. Therefore unattended reboot recovery is a setup-and-test requirement; the documented login command alone does not establish it. Verify the runtime, Compose services, storage, and worker recover after reboot. Do not assume a generic root service is sufficient. [Colima autostart](https://github.com/abiosoft/colima/blob/main/docs/FAQ.md#does-colima-support-autostart), [Homebrew service semantics](https://docs.brew.sh/Manpage#services-subcommand).

Docker Desktop is an alternative with Intel/Apple Silicon installers, a 4 GB RAM minimum, and support for the current and previous two major macOS releases. Its free professional-use eligibility requires a business below both 250 employees and $10 million annual revenue; other professional use requires a subscription, as do government entities. Confirm the organization's eligibility rather than assuming personal installation makes office use free. [Docker installation and terms](https://docs.docker.com/desktop/setup/install/mac-install/).

## Reminder timing

GitHub explicitly warns scheduled workflows can be delayed and queued jobs dropped under load. Recommendation: Actions deploys/manages the application; a database-backed worker on the Mac handles reminder deadlines and retries during 08:00–15:00 plus the agreed overrun. That window is a product assumption, not a GitHub guarantee. [GitHub schedule limitations](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).
