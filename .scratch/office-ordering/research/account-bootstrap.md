# Initial administrator and manually created accounts

Researched 23 November 2026. Input to [office access](../issues/06-office-access.md); recommendations below are proposals, not agreed product decisions.

## What FastAPI establishes

FastAPI does not require a particular account-provisioning workflow. Its official full-stack template is explicitly customizable. That template supplies a **configurable** initial superuser: deployment takes `FIRST_SUPERUSER` as configuration and `FIRST_SUPERUSER_PASSWORD` as a secret; a preparation step creates the account before deployment. Its initializer checks for that email and only creates it when absent. These are template choices, not framework requirements. [Official template overview](https://fastapi.tiangolo.com/project-generation/), [deployment configuration](https://github.com/fastapi/full-stack-fastapi-template/blob/master/deployment.md), [initializer](https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/core/db.py).

The template also demonstrates administrator-only user creation, but separately includes public signup and sends new-account passwords by email. It therefore needs adaptation to this app's confirmed no-signup policy and chosen credential-delivery policy; copying the template wholesale would not satisfy the brief. [Official route source](https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/api/routes/users.py).

## Bootstrap recommendation

Use an explicit operator command after migrations to create the first account, office membership, administrator permission and initial menu-maintainer permission atomically. Supply email and display name at runtime; prompt for the password without echo, with a secret input mechanism for automated deployment. Never commit a particular person or credential. Python provides hidden terminal password input through `getpass`. [Python documentation](https://docs.python.org/3/library/getpass.html).

Prefer this one-time command to creating privileged accounts in every web-worker startup. FastAPI recommends executing shared preparation work once, separately from replicated workers. The command can also run as a single deployment preparation job reading runtime secrets, so CLI and environment configuration are compatible. [FastAPI deployment concepts](https://fastapi.tiangolo.com/deployment/concepts/#previous-steps-before-starting).

Proposed safeguards: reruns do not reset passwords, promote existing ordinary accounts, or create additional administrators; refuse bootstrap after initialization. Provide a separately named, deliberate operator recovery command if needed. Remove bootstrap secrets after success. These are our operational recommendations, not FastAPI mandates. Runtime email/name configuration is enough to avoid hardcoding the initial person; it need not remain a permanent setting.

## Credential setup and recovery choices still requiring a product decision

| Choice | Effect and tradeoff |
| --- | --- |
| Administrator creates a temporary password | Works without transactional email. Administrator privately gives it to the colleague; recommend expiry and a restricted first login that requires choosing a personal password before office use. The administrator initially knows a usable credential, and delivery/reissue needs an agreed process. These restrictions are our recommendation. |
| Administrator creates the account; colleague sets a password through a single-use link | Administrator need not know a password; emailed delivery needs an email service. This can activate an already-created account rather than admit new members, but whether any setup-link experience fits the user's “no invitations” intention must be decided explicitly. |
| Administrator-assisted recovery | Fits a small office without email infrastructure, but needs identity checking and a route for recovery when the only administrator is locked out. Reissue a temporary credential or setup link; never retrieve the old password. |
| Self-service email recovery | Less administrator work; introduces email delivery, reset-token storage and abuse controls. Does not require public registration. |

For token-based setup/recovery, OWASP recommends securely generated, user-bound, single-use expiring tokens, consistent responses to avoid account enumeration, and rate limiting. After recovery, notify the account holder and decide session invalidation; OWASP recommends invalidation after compromise. Its reset guidance says not to email the new password. Reusing those controls for initial setup is our application of the guidance. [OWASP Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html).

Whichever workflow is chosen, store password hashes, not recoverable passwords. FastAPI's current tutorial recommends Argon2 with `pwdlib`. [FastAPI password hashing](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#password-hashing).

Unresolved: whether “superuser” means office administrator or a separate operator authority; temporary-password delivery versus setup links; whether email ownership must be verified; self-service versus administrator-assisted recovery; emergency recovery for the last administrator. Sources inform the implementation but do not decide these product policies.

## Migration-driven deployment with `.env` credentials

Recommendation for the requested workflow: expose one deployment command or job that first applies schema migrations, then runs an ORM initializer using credentials loaded from the runtime `.env`, then starts the application after both succeed. This preserves automatic first-administrator creation during deployment. Keep this preparation in one process before starting web workers, consistent with [FastAPI's pre-start guidance](https://fastapi.tiangolo.com/deployment/concepts/#previous-steps-before-starting). This is an implementation proposal; it does not select an ORM or migration tool.

If SQLAlchemy/Alembic is selected, prefer the initializer as a separate step within that same command or job. Alembic describes itself as a schema migration tool, cautions that data migrations need application-specific design, and documents separate data scripts as one approach. It also supports small initial-data inserts directly in revisions, so revision-based seeding is possible. The tradeoff is tying an environment-specific privileged account and its downgrade behavior to schema history; the separate initializer keeps those responsibilities independent. [Alembic data migration guidance](https://alembic.sqlalchemy.org/en/latest/cookbook.html#data-migrations-general-techniques).

Proposed initializer behavior: atomically create the initial account and required permissions only while the installation is uninitialized; after initialization, succeed without changing passwords or permissions even if `.env` credentials change. Require valid bootstrap credentials for an uninitialized installation and stop deployment if creation fails. Use an explicit separate recovery operation to regain administrator access. These safeguards are recommendations for this application, not requirements imposed by FastAPI or Alembic.
