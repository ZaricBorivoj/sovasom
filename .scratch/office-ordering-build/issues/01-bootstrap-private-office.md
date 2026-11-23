# 01: Bootstrap and sign into the private office

Status: done
Blocked by: None (can start immediately)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** The operator initializes the private office at runtime and signs in to a responsive Postcard Club office home. This first working path establishes the application and its verification harness.

- [x] One setup command loads runtime initial email, display name and password, applies schema migrations, then atomically creates the account, office membership, administrator and menu-maintainer grants through an ORM initializer outside versioned migrations. No person or credential is hardcoded. Reruns, including changed inputs, leave credentials and permissions unchanged; bootstrap secrets are removed after success.
- [x] Email/password sign-in and sign-out work through the React UI and FastAPI with password hashes and PostgreSQL-backed revocable opaque sessions. Enforce a 30-day absolute lifetime, Secure/HttpOnly/SameSite cookies, CSRF protection and current access checks. Unauthorized users cannot read office data. Keep stable account identity separate from membership and mutable email.
- [x] The phone/desktop home uses shared Postcard Club tokens and accessible primitives, an Office runs heading and a truthful empty state. Do not offer nonworking run actions; later run slices activate announcement. Email is visible only to its account holder and administrators. No signup, invitations, avatars or public profiles.
- [x] Provide a runnable Compose path with persistent PostgreSQL, FastAPI and Caddy serving the Vite-built React 19 SPA and same-origin API. Keep the database private. Establish modular backend boundaries without separate domain services; add the shared-image worker when due work first needs it.
- [x] Establish backend/frontend unit tooling, Storybook and integrated Playwright with isolated PostgreSQL and synthetic credentials, plus Linux CI. Prove runtime bootstrap, unchanged reruns, login/logout, expired/revoked sessions, CSRF/authorization denial, persistence after reload and phone layout. Configure desktop Chromium/Firefox/WebKit and meaningful component stories; later tickets extend this harness rather than defer tests to release.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.

## Comments

### Implemented — 23 November 2026

- Added runtime migration-then-ORM bootstrap with serialized atomic initialization, explicit membership/grants, unchanged reruns and consumed-file removal. Added stable account IDs, Argon2 passwords, hashed opaque PostgreSQL sessions, exact 30-day expiry, revocation, secure cookies, session-bound CSRF and current access checks.
- Added the responsive Postcard Club sign-in and Office runs empty home, shared tokens/primitives, and stories for every component and its relevant states. No inactive announcement action or prototype identities were shipped.
- Added persistent/private PostgreSQL 19, FastAPI and Caddy/React Compose services, pinned manifests and lockfiles, blocking pre-commit checks, Linux CI and operator instructions in the root README. Worker remains deferred until durable work is introduced.
- Verification passed: Ruff; Prettier; ESLint; TypeScript; 4 frontend units; 18 backend units/integration tests on isolated PostgreSQL; 16 Linux Storybook interaction/visual checks with all 8 initial baselines visually reviewed; 24 integrated browser checks across Chromium, Firefox, WebKit and phone; 8 checks saving/restoring the same sessions around database/backend restart. Both runtime bootstrap reruns and secret-file consumption were exercised. Disposable resources were cleaned up.
- Code review against starting commit ec403de: Standards found 2 issues (direct Pydantic pin, App state stories), both fixed; Spec found 1 CSRF cookie replacement/sign-out defect, reproduced red then fixed green with HTTP and real cross-site browser regression coverage. Both reviewers confirmed no remaining findings.
- GitHub Actions was not run remotely because no Git remote is configured. Linux images, backend tests and canonical component checks ran locally; the checked-in workflow runs the complete gate when connected. Production rollout and physical iPhone acceptance belong to later tickets.
