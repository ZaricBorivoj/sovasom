# Repository MCP setup

Codex loads the committed [configuration](../.codex/config.toml) for this trusted project. Open Codex from the repository root and trust the checkout when prompted. Restart Codex after configuration or environment changes. Project trust is a per-developer choice; it is not committed. See [Codex MCP configuration](https://developers.openai.com/codex/mcp/).

## Prerequisites

Use the project Node toolchain from `.nvmrc`, with `node` and `npx` available to the process launching Codex. Install Google Chrome stable. The initial launch downloads the pinned npm packages and needs network access; subsequent launches use npm's cache. No global MCP installation is necessary.

## Credentials

For Codex CLI onboarding, fill in these two values in the ignored `.env` copied from `.env.example`:

| Variable           | Purpose                                                                                                                                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GITHUB_PAT_TOKEN` | Personal GitHub token for the repositories you want to inspect. Prefer a fine-grained token restricted to this repository and the read permissions needed for code, issues, pull requests, and Actions. |
| `POSTMAN_API_KEY`  | Personal Postman API key for the workspaces you intend to access.                                                                                                                                       |

Then run from the repository root:

```sh
uv run --frozen python scripts/onboard.py
```

The script reads only the two MCP tokens without shell expansion and writes safely quoted exports in one marked `.zshrc` block. Other shell settings are preserved. Reruns update that block in place, including after token rotation, without duplicating it. Missing, empty, or example tokens stop onboarding before the shell file changes. `.env` and the written shell file are restricted to owner read/write; both contain the tokens as plain text. Keep real values in ignored `.env`, never in `.env.example`.

Open a new terminal and launch `codex` from this checkout. The script honors `ZDOTDIR` and supports `--env-file` and `--zshrc` for alternate paths. It configures the CLI shell environment; desktop launches need their own launcher environment. Codex does not automatically source the application's `.env`. The Postman configuration explicitly forwards its key to the local server.

GitHub uses its hosted [read-only endpoint](https://github.com/github/github-mcp-server/blob/main/docs/server-configuration.md), which filters out write tools even if the token has broader permissions. The hosted server's deployment version is managed by GitHub. Token setup follows [GitHub's Codex guide](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-codex.md).

## Browser tools

Playwright drives application workflows; Chrome DevTools supports console, network, and performance investigation. Both launch visible Chrome windows with separate temporary profiles. Logins and browser storage are discarded when those sessions close; neither attaches to everyday Chrome tabs. Switching tools requires opening the application and signing into the test account again.

Start the application using [the local setup instructions](../README.md#start-locally). Use a dedicated test installation/account with synthetic data for browser checks. Local HTTPS uses Caddy's development certificate: trust the local CA or accept the localhost certificate warning in each isolated browser. The configuration keeps certificate validation enabled.

## Postman

Postman MCP is available for explicitly requested work; it is not part of routine development verification. The local STDIO server can reach local APIs and operates on Postman-hosted collections and environments. It does not control the open Postman desktop application. See [Postman's local server setup](https://learning.postman.com/docs/reference/postman-api/postman-mcp-server/postman-mcp-local-server/).

Use a dedicated coffee-app workspace when Postman work is requested. Workspace creation, uploads, and other shared workspace changes require explicit instruction. This setup creates no workspace or collection and uses the server's default minimal toolset.

## Check connections

From the trusted repository root, run:

```sh
codex mcp list
codex mcp get playwright
codex mcp get chrome_devtools
codex mcp get github
codex mcp get postman
```

These commands inspect configuration; they do not prove server connectivity. In a new Codex session, use `/mcp` to check connection status, then request a browser navigation to the local application. For GitHub and Postman, request a read-only lookup after supplying credentials. Missing keys affect those integrations; the browser servers require no service tokens. Cold npm downloads can take up to the configured startup timeout. Check Node/Chrome availability and project trust when browser servers fail to start.

## Version updates

Exact npm server versions are pinned in `.codex/config.toml`. Verified stable releases on 23 November 2026: [Playwright](https://github.com/microsoft/playwright-mcp/releases/tag/v0.0.86), [Chrome DevTools](https://github.com/ChromeDevTools/chrome-devtools-mcp/releases/tag/chrome-devtools-mcp-v1.13.0), and [Postman](https://github.com/postmanlabs/postman-mcp-server/releases/tag/v2.15.0). Before changing a pin, verify the latest stable upstream release and smoke-test server startup and tool discovery.
