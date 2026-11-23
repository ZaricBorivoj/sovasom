# Out & About

A private office home for coffee and bakery trips. This first slice supports runtime office setup, sign-in, persistent sessions and sign-out. Run announcement arrives in a later slice.

The modular FastAPI application lives in `backend/office` (accounts/access first), with SQLAlchemy and schema-only Alembic migrations. `frontend/src/design-system` owns Postcard Club tokens and accessible primitives; React 19/Vite builds the SPA. Caddy serves the build and the same-origin `/api` proxy. PostgreSQL has persistent storage and no published port. A worker will use the backend image when durable work is introduced.

## Start an office

Install the pinned tools in `.tool-versions` / `.nvmrc`, Docker with Compose, then run `uv sync --frozen` and `npm ci --prefix frontend`. Dependency versions were checked against the official registries on 23 November 2026; see [version sources](docs/dependency-versions.md).

Copy `.env.example` to `.env` and set the public HTTPS origin, hostname and an absolute secrets directory outside this checkout. Create that directory with mode `0700` and these files:

- `database_password`: a generated database password.
- `database_url`: `postgresql+psycopg://office:<URL-encoded-password>@db/office`.
- `bootstrap.json`: runtime JSON with `email`, `display_name` and `password` (12–1024 characters).

Keep bootstrap input mode `0600`. The two database files must be readable by container UID 10001: with Compose file mounts, mode `0444` within the private `0700` directory works on the verified Docker Desktop path. Retain database credentials in your password manager. Only PostgreSQL receives the password file and only FastAPI receives the connection URL; neither is embedded in an image. Verify equivalent ownership/readability on another host.

Run one preparation command from the repository root:

```sh
uv run --frozen python scripts/setup.py --bootstrap-file /absolute/private/path/bootstrap.json
```

It builds the images, starts PostgreSQL, applies migrations, atomically creates the initial account, membership, administrator and menu-maintainer grants, removes the consumed bootstrap file, then starts the application. The operator chooses the initial identity; nothing seeds a person or password. `INITIAL_EMAIL`, `INITIAL_DISPLAY_NAME` and `INITIAL_PASSWORD` are also supported when `--bootstrap-file` is omitted; clear these from the invoking shell/secret store after success. Prefer the file path for automatic removal. Bootstrap input never enters container configuration or build arguments. Setup errors deliberately omit input values.

Reruns leave account credentials, membership and grants unchanged, even with changed inputs or removed grants. Without bootstrap input an initialized installation is still a no-op. Bootstrap is not an administrator recovery/reset command; explicit recovery is delivered by ticket 03. Initial setup is intended for a new database. Backups and controlled upgrades of existing installations are delivered by later operational tickets; migration rollback must be assessed separately from image rollback.

For local HTTPS, set `SITE_ADDRESS=localhost`, `PUBLIC_ORIGIN=https://localhost:8443`, `HTTPS_PORT=8443`, `HTTP_PORT=8080`. Caddy uses its local CA; trust that CA locally or accept its certificate for this development instance. Production hostnames use automatic public HTTPS with inbound 80/443. The database volume and Caddy keys survive `docker compose down`; do not use `down --volumes` on an office installation.

## Verify changes

```sh
uv run --frozen ruff check
cd frontend
npm run format:check
npm run lint
npm run check-types
npm test
npm run build-storybook
npx playwright install chromium firefox webkit
npm run test:storybook
cd ..
uv run --frozen python scripts/verify-stack.py
```

The last command builds an independently named Compose stack, uses only synthetic credentials and private temporary runtime files, runs backend units/integration against new PostgreSQL databases, and runs UI flows in desktop Chromium/Firefox/WebKit and a 390px phone viewport. It verifies changed bootstrap reruns, cookie protection, authorization, CSRF denial, persisted login after reload, expired/revoked sessions, sign-out and persistence through database/application restart. Cleanup removes only that test project's containers and volumes. Direct session mutations in Playwright are gated by this isolated harness; production exposes no test endpoints. CI runs the same commands on Linux with frozen lockfiles.

For focused backend work, set `TEST_DATABASE_URL` to a disposable PostgreSQL server on which the test user can create databases, then run `uv run --frozen pytest backend/tests/test_auth.py`. Each test creates and drops a uniquely named database; it never resets the configured database. Run all backend tests with `uv run --frozen pytest`.

Visual baselines use the pinned Linux browser image to keep fonts/rendering consistent with CI:

```sh
docker run --rm --ipc=host -e STORYBOOK_STATIC=1 -e CI=1 \
  -v "$PWD:/work" -w /work/frontend \
  mcr.microsoft.com/playwright:v1.65.1-noble \
  node node_modules/@playwright/test/cli.js test --config playwright.components.config.ts
```

Use `--grep @visual --update-snapshots` only for deliberate visual changes, and inspect every changed image before committing. Component interaction tests also run locally with `npm run test:storybook`. Every production component has stories, including pending, rejected, offline and access-loss states. Pre-commit blocks on frontend Prettier/ESLint/project type checking and backend Ruff.
