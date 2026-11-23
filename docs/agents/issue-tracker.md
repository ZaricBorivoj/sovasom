# Issue tracker: Local Markdown

Issues and specs live as Markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`.
- Spec: `.scratch/<feature-slug>/spec.md`.
- Implementation tickets: one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order.
- Record triage state as a `Status:` line near the top of each issue. Use the role strings in `triage-labels.md`.
- Record dependencies as a `Blocked by:` line listing ticket numbers, or `None`.
- Append comments and conversation history under `## Comments`.

## Tracker operations

When a skill says to publish, create the corresponding file under the feature directory. When it says to fetch a ticket, read the referenced file. Resolve bare ticket numbers within the named feature; ask if the reference is ambiguous.

Work tickets whose blockers are complete. Record completion as `Status: done`; completion is separate from the five triage roles.

## Wayfinding operations

- Map: `.scratch/<effort>/map.md`, containing Notes, Decisions-so-far, and Fog.
- Decision tickets: `.scratch/<effort>/issues/<NN>-<slug>.md`, numbered from `01`, with the question in the body.
- Record `Type:` as `research`, `prototype`, `grilling`, or `task`.
- Record dependencies in `Blocked by:`. A decision ticket is unblocked when all its blockers are `resolved`.
- Select an open, unblocked, unclaimed ticket, lowest number first. Set `Status: claimed` before working.
- To resolve, append `## Answer`, set `Status: resolved`, and add a summary and link to Decisions-so-far in the map.
