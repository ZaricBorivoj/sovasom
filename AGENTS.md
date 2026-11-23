# Project

Monorepo with a FastAPI backend and a React single-page frontend built with Vite.

## Agent skills

### Issue tracker

Track specs and issues as local Markdown under `.scratch/<feature-slug>/`. Before creating, reading, or updating tracked work, read `docs/agents/issue-tracker.md`.

### Triage labels

Use the five default triage roles as issue statuses. Before triaging or changing a triage status, read `docs/agents/triage-labels.md`.

### Domain docs

Use a single shared domain context across the monorepo. Before exploring or changing the project, read `docs/agents/domain.md` for glossary and ADR rules.

## Application stack

- Backend: FastAPI with SQLAlchemy as the ORM and Alembic for database migrations.
- Frontend: React single-page application built with Vite.
- Database: PostgreSQL running in a Docker container.

## Development tools

- Use Prettier for frontend formatting, ESLint for frontend linting, and a `check-types` script for TypeScript type checking.
- Configure the pre-commit hook to run all three checks and block the commit if any check fails. Prettier and ESLint may target staged frontend files; `check-types` must check the frontend project.
- Run these checks before completing frontend work, even when no commit is being made.
- Use uv for backend dependency management, Python installation, and virtual environment management. Run backend commands through `uv run`.
- Use Ruff for backend static analysis and linting. Run `uv run ruff check` before completing backend work and in the pre-commit hook; failures must block the commit.

## Versions and dependencies

- Use the latest stable Python release and the latest stable versions of tools and dependencies when setting up the projects or adding or upgrading dependencies. Verify current releases against official sources at that time.
- Pin the exact Python version in `.python-version` and declare the supported Python version in `pyproject.toml`.
- Pin all direct runtime and development dependencies to exact versions in both projects: use `==` in backend dependency declarations and exact versions without ranges in frontend package manifests.
- Commit `uv.lock` and the frontend package manager's lockfile to pin transitive dependencies. Update manifests and lockfiles together, and use frozen lockfile installs in CI.
- Pin development tools alongside other development dependencies; record exact versions for tools installed outside the project manifests in checked-in tool configuration.

## Frontend design system

Build the frontend from the project's design system. Reuse its components, tokens, and patterns; extend the design system when a reusable component is needed.

Maintain Storybook stories for every frontend component, including its relevant states and variants.

## Testing

- Always run the relevant tests before completing a piece of work. Fix failures caused by the changes and report the checks run, their results, and any checks that could not run with the reason.
- For frontend work, run Storybook tests, unit tests, and visual regression tests covering the affected components and workflows.
- For backend work, add or update unit tests and integration tests for new or changed code, and run the relevant suites. Cover business rules, validation, error cases, and database interactions where applicable.
- Update tests and component stories alongside behavior changes. Review visual differences before accepting updated regression baselines.
- Cover all user-facing workflows end-to-end with Playwright, exercising the frontend, backend, and database together. Maintain these tests alongside workflow changes; the build server runs end-to-end and other long-running tests, so local completion does not require running those suites.
