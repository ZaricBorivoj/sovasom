# 01: Bootstrap and sign into the private office

Status: ready-for-agent
Blocked by: None (can start immediately)
Parent: [Approved office-ordering specification](../../office-ordering/spec.md)

**What to build:** The operator initializes the private office at runtime and signs in to a responsive Postcard Club office home. This first working path establishes the application and its verification harness.

- [ ] One setup command loads runtime initial email, display name and password, applies schema migrations, then atomically creates the account, office membership, administrator and menu-maintainer grants through an ORM initializer outside versioned migrations. No person or credential is hardcoded. Reruns, including changed inputs, leave credentials and permissions unchanged; bootstrap secrets are removed after success.
- [ ] Email/password sign-in and sign-out work through the React UI and FastAPI with password hashes and PostgreSQL-backed revocable opaque sessions. Enforce a 30-day absolute lifetime, Secure/HttpOnly/SameSite cookies, CSRF protection and current access checks. Unauthorized users cannot read office data. Keep stable account identity separate from membership and mutable email.
- [ ] The phone/desktop home uses shared Postcard Club tokens and accessible primitives, an Office runs heading and a truthful empty state. Do not offer nonworking run actions; later run slices activate announcement. Email is visible only to its account holder and administrators. No signup, invitations, avatars or public profiles.
- [ ] Provide a runnable Compose path with persistent PostgreSQL, FastAPI and Caddy serving the Vite-built React 19 SPA and same-origin API. Keep the database private. Establish modular backend boundaries without separate domain services; add the shared-image worker when due work first needs it.
- [ ] Establish backend/frontend unit tooling, Storybook and integrated Playwright with isolated PostgreSQL and synthetic credentials, plus Linux CI. Prove runtime bootstrap, unchanged reruns, login/logout, expired/revoked sessions, CSRF/authorization denial, persistence after reload and phone layout. Configure desktop Chromium/Firefox/WebKit and meaningful component stories; later tickets extend this harness rather than defer tests to release.

## Implementation and verification context

Use the approved spec and its resolved decision provenance as authority. No product discovery is required. Use existing shared design-system and application test seams where available; add only the pieces this slice needs. All application behavior is server-authorized and PostgreSQL-backed; applicable tests use synthetic isolated data and never notify colleagues. Add component stories and focused units with behavior changes, and run the relevant full-stack Playwright workflows before completion. Record checks that cannot run. Operational slices record equivalent plan/smoke/recovery evidence on isolated resources. Do not alter the parent spec or resolved decision tickets as part of claiming/completing this ticket.
