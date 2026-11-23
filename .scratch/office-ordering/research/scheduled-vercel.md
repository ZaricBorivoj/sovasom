# Vercel Hobby with a seven-hour worker

Checked **23 November 2026**, supporting [Scheduled Vercel worker and Mac mini hosting feasibility](../issues/09-scheduled-worker-and-mac-mini.md). Research only; no deployment, account access or quota measurements.

## Revised finding

**Yes: 08:00–15:00 operation removes the previously identified full-month daemon-memory blocker if a 1 GiB worker is sufficient and is actually stopped outside the window.** It does not establish that the full application is free, or choose Vercel over the existing single-host architecture. The earlier comparison assumed 24/7 operation and remains valid only under that assumption.

The current daemon-specific Hobby allowance is 420 GB-hours of provisioned memory and five active CPU-hours per month. The smallest instance is 1 GiB; the default is 2 GiB. Memory counts even while waiting. [Daemon limits](https://vercel.com/docs/daemons/limits).

Sizing arithmetic (not a measured bill), before warm-up, shutdown, deployment overlap, tests and other daemons:

| Schedule | Nominal worker hours | 1 GiB memory-hours | 2 GiB memory-hours |
| --- | --- | --- | --- |
| Seven hours daily for 31 days | 217 | 217: below 420 | 434: above 420 |
| Seven hours for 23 weekdays | 161 | 161: below 420 | 322: below 420 |

Actual active CPU and peak RAM must be measured. Reaching either daemon quota stops the team's daemons until the next month or an upgrade. Sleeping inside the worker does not stop memory accounting; scale its instance count to zero.

## Starting and stopping

Vercel documents CLI/API scaling overrides and stopping a daemon by setting every region to zero. Overrides survive deployments, so releases must preserve the intended schedule rather than reset it. [Managing Daemons](https://vercel.com/docs/daemons/managing-daemons).

Proposed automation: a trusted scheduled controller calls the scaling API; start early enough for readiness, then stop after pending time-sensitive work completes. The newer Hobby Schedules has a mandatory 15-minute jitter window and supports named timezones including daylight-saving changes. A daily controller could start ahead of 08:00 and stop after 15:00, while the continuously running worker handles precise reminders during the window. That is a plausible design, not a tested guarantee: scheduled runs can be late, skipped, duplicated or fail, so reconcile desired state and alert on failures. Do not schedule each closing reminder directly through a 15-minute-jitter service. [Schedules limits](https://vercel.com/docs/schedules/limits), [timing, timezones and failure semantics](https://vercel.com/docs/schedules/concepts).

Confirm Europe/Belgrade, weekdays versus every day, permitted startup/shutdown buffers and cutoff behavior. A run announced at 14:59 can have a later deadline under the existing product rules. Stopping the worker at 15:00 can delay its reminders/push, even though API deadline validation still rejects late writes. Restricting run times or guaranteeing later processing requires a live product decision.

## Remaining full-application checks

- Vercel hosts the SPA and FastAPI Functions; PostgreSQL needs an external durable service because daemon disks are ephemeral. This revises the accepted single-host Compose deployment, including production Caddy placement. [FastAPI deployment](https://vercel.com/docs/frameworks/backend/fastapi), [daemon storage limits](https://vercel.com/docs/daemons/limits).
- A managed free PostgreSQL candidate is Neon. Its current Free plan includes 100 CU-hours per project, with a 0.25-CU minimum compute and scale-to-zero after five idle minutes. If database compute stays active for exactly 217 hours, arithmetic is 54.25 CU-hours before other activity; round-the-clock polling would instead approach 186 CU-hours in a 31-day month. The worker must stop database polling outside the window, and foreground/API access, branches, backups and compute autoscaling also consume allowances. This is a candidate sizing inference, not a selected or validated database service. [Neon plan and compute rules](https://neon.com/docs/introduction/plans).
- Five-second per-client refresh, API execution, transfer, database storage, external backups and registry/CI usage need sizing against actual colleagues and active use. A fit for worker memory alone is insufficient. Hobby eligibility remains personal or noncommercial under current terms; the project's actual use would need confirmation if pursuing it. [Hobby quotas](https://vercel.com/docs/plans/hobby), [terms](https://vercel.com/legal/terms#hobby-plan).
- Vercel Daemons are beta. The provider exists, but coverage of beta resources and the chosen controller/database setup has not been proven. Preserve the Terraform requirement and verify pinned-provider coverage; application deployment configuration can describe worker images alongside automated releases. [Vercel Terraform provider](https://github.com/vercel/terraform-provider-vercel).

## Conclusion for the live decision

Scheduled Vercel Hobby is **plausible**, rather than rejected by the 24/7 quota calculation. A focused deployment experiment would be needed before treating its complete free architecture and daily readiness as established. Existing Mac mini hosting is a separate candidate that can preserve the full Compose design without these cloud worker quotas; compare its OS, operational and off-host backup requirements in the companion research.
