# Verified toolchain, 23 November 2026

Direct dependency releases were resolved from the official [npm registry](https://registry.npmjs.org/) and [PyPI JSON API](https://docs.pypi.org/api/json/). Exact versions are recorded in `frontend/package.json` and `pyproject.toml`; `package-lock.json` and `uv.lock` lock transitives.

| Tool | Exact version | Official source |
| --- | --- | --- |
| Python | 3.15.2 | [Python downloads](https://www.python.org/downloads/) |
| Node | 26.13.1 | [Node release index](https://nodejs.org/dist/index.json) (stable; excludes 27 alpha) |
| uv | 0.13.9 | [uv on PyPI](https://pypi.org/project/uv/) |
| PostgreSQL | 19.0 | [Supported releases](https://www.postgresql.org/support/versioning/) |
| Caddy | 2.11.9 | [Official releases](https://github.com/caddyserver/caddy/releases) |
| Playwright browser image | 1.65.1-noble | [Official Playwright Docker guidance](https://playwright.dev/docs/docker) |

Dockerfiles pin runtime/tool versions; CI action references pin exact releases. Docker/Compose are host-provided; this implementation was verified with Docker 29.9.3 and Compose 5.7.0. Host installation/lifecycle automation belongs to deployment ticket 17.

TypeScript 7.0.2 is used for project checking. Current typescript-eslint 8.73.0 only accepts TypeScript below 6.1, so ESLint uses current Babel 8 TypeScript syntax parsing and React Hooks rules; TypeScript owns type checking. Storybook docgen is disabled because its compiler integration expects an earlier TypeScript API. Stories and interactions are still compiled, type checked and browser tested.

Infrastructure tools verified on 26 November 2026: Terraform **1.17.2** from the
[official release index](https://releases.hashicorp.com/terraform/), AWS provider
**6.74.0** from the [official registry](https://registry.terraform.io/providers/hashicorp/aws/latest),
and AWS CLI **2.42.4** from the [v2 changelog](https://github.com/aws/aws-cli/blob/v2/CHANGELOG.rst).
Developer Terraform/AWS CLI versions are not pinned; install current stable
releases through the official instructions in [local infrastructure setup](../infra/local-setup/README.md).
The roots accept Terraform 1.10 or newer within 1.x. CI tests Terraform 1.17.2;
both roots pin the AWS provider and commit its dependency lockfile. New actions
use exact official releases:
[setup-terraform v4.0.1](https://github.com/hashicorp/setup-terraform/releases/tag/v4.0.1)
and [configure-aws-credentials v6.3.1](https://github.com/aws-actions/configure-aws-credentials/releases/tag/v6.3.1).
