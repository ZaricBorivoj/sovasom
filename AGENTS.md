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

- Backend: FastAPI.
- Frontend: React 19 single-page application built with Vite.
- Database: PostgreSQL running in a Docker container.

## Frontend design system

Build the frontend from the project's design system. Reuse its components, tokens, and patterns; extend the design system when a reusable component is needed.

Maintain Storybook stories for every frontend component, including its relevant states and variants.

## Testing

- Cover all user-facing workflows end-to-end with Playwright, exercising the frontend, backend, and database together.
- Unit test frontend behavior where applicable, especially logic and interactions that benefit from focused coverage.
- Unit test backend behavior, including business rules, validation, and error cases.
- Update tests and component stories alongside behavior changes. Run the relevant unit and Playwright tests before completing implementation, and report any checks that could not run.
