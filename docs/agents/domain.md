# Domain docs

## Layout and reading rules

This monorepo initially shares one domain context across its FastAPI backend and React frontend:

- `GLOSSARY.md` at the repository root defines domain vocabulary.
- `docs/adr/` holds architecture decision records.

Before exploring the codebase, read the glossary and ADRs relevant to the work. If these files do not exist, proceed silently. Let `domain-modeling`, including through `grill-with-docs`, create them as terms and decisions are resolved.

If a root `GLOSSARY-MAP.md` is introduced later, follow it to the relevant context glossaries and read context-specific ADRs alongside system-wide ADRs.

## Vocabulary

Use glossary terms consistently in issues, code, tests, and explanations. If a needed concept is missing, reconsider the wording or note the gap for `domain-modeling`.

## Decisions

Surface conflicts with an existing ADR explicitly, citing the ADR and explaining why it should be revisited.
