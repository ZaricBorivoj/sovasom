# Explore and choose the frontend direction

Parent: [Office coffee and bakery ordering](../map.md)
Label: wayfinder:prototype
Type: prototype
Status: resolved
Assignee: Nemanja.Tomic (Codex session)
Blocked by: None

## Question

Which visual direction and interaction model make announcing and joining office runs easiest? Use the `prototype` UI workflow to compare warm café and playful social board (clean office utility rejected in live review) using the same representative run announcement, maintained-menu selection, and runner shopping-list flows. Explore phone and desktop layouts. Mark unresolved product behaviors as illustrative assumptions, not decisions. Choose a direction and a compatible design-system approach through live user feedback; link the prototype and record the verdict here.

## Comments

### 20 November 2026 — prototype ready for live review

Claimed for Nemanja.Tomic with Codex. Built a [throwaway frontend comparison](../prototype/frontend-prototype.html), with [run instructions, assumptions and verification evidence](../prototype/README.md).

Compare warm café, clean office utility and playful social board on the same representative run, maintained menus, request selection, announcement form and runner shopping-list flows. The bottom switcher preserves the direction in the URL. No data persists. The prototype includes phone and desktop layouts and explicitly marks undecided behavior as illustrative.

Playwright workflow checks passed for all three directions at 390px and 1440px widths. All five screens fit at phone width without horizontal overflow. Integrated application tests, unit suites and Storybook are unavailable because the production application does not exist yet; this is a standalone planning artifact.

Agent's proposed starting point: warm café, with compact, easily scanned menu and shopping lists. This is a recommendation awaiting user feedback, not a resolution. The compatible production design-system approach also awaits discussion. No Answer recorded and no map decision added yet.

### 20 November 2026 — live feedback and second exploration

User-confirmed requirements for every direction:

- Every runner visits both shops; remove shop selection.
- Generate a funny run title that clearly identifies the day and time of day, with no title entry field.
- Ask how many minutes until requests close, rather than requesting an absolute closing time.
- Provide one action to mark everything collected, replacing individual item verification.

User rejected clean office utility and requested further warm café and playful social board examples. The updated prototype compares four layouts: The counter and The daily journal (warm café); Postcard club and Office lounge (playful social). This is still an open visual choice, and the design-system approach remains to be selected. Exact generated jokes, day-period boundaries, duration defaults/range, timezone and detailed lifecycle policy remain illustrative.

Revised-preview verification: eight Playwright workflow runs passed across all four layouts at 390px and 1440px. All five screens fit at both widths. Checked generated titles, removed fields, duration presets/custom input and draft preservation across direction switching, request submission, whole-run collection and switcher URLs. No JavaScript page errors occurred. All four home layouts were visually inspected at phone and desktop sizes. See [updated preview instructions and evidence](../prototype/README.md).

### 20 November 2026 — selected Postcard Club and refined the preview

User selected Postcard Club. Their further feedback is incorporated into the [selected prototype](../prototype/frontend-prototype.html). The earlier alternatives remain in a [local comparison archive](../prototype/frontend-comparison-prototype.html), preserving the primary source without promoting prototype code into production.

### 20 November 2026 — final approval

User approved the refined Postcard Club prototype: “this is good, I approve.” Approval includes the prominent single active run with completed runs below, the coffee-specific choices, non-coffee drinks without those choices, and revised closing-duration chips. This confirms the frontend direction and interaction layout; the explicitly listed illustrative defaults and remaining menu/lifecycle policies stay with their existing tickets.

## Answer

**Chosen direction: Postcard Club**, explicitly selected by the user. Retain the peach and lavender postcard surfaces, soft green accents, bold rounded sans-serif typography, strong plum/ink borders, offset shadows, rounded buttons and playful closing-duration stamps. The design works on phone and desktop layouts.

### Confirmed product requirements

- At most one run is active in the office. The user may revisit this later.
- Every run visits both the coffee shop and the bakery.
- Generate a funny run title identifying the day and time of day; no title input.
- Ask for a closing duration in minutes. Offer exactly **5, 10, 15 and 30 minutes** as quick choices; custom numeric input is retained in the preview.
- Each coffee has a **Blend / Specialty** choice. Preserve the selected choice in the request and runner’s shopping list, and keep different choices separate when consolidating quantities.
- The coffee shop also offers juices and hot chocolate. Those items have no Blend / Specialty choice.
- One action marks everything collected, replacing per-item verification.

### Approved interaction layout

The office home has one prominent active-run postcard, followed by quieter completed-run summaries. Rename “Open runs” to “Office runs.” The user approved this layout, including past-run summaries below the active run. An empty state offers announcing the next run. The preview guards against announcing a second run, including after collection: collected is not assumed to mean finished/returned.

### Compatible design-system approach

Build a project-owned React design system from shared tokens and accessible primitives, with Storybook stories for each production component and relevant state. Initial visual references: background `#f4f0fc`, peach `#f9ce98`, lavender `#dad1f6`, green `#e5eec7`, primary plum `#4c2864`, ink border `#41294e`; 2px postcard borders, roughly 24px corners, 5px offset shadows. Use native radios styled as a segmented coffee choice, semantic buttons, labelled form fields and explicit statuses. Extract reusable Postcard, RunStatus, DurationChoices, CoffeeChoice, QuantityControl, RequestSummary and ShopList primitives when implementing. The preview is visual evidence, not production component code. No third-party component package was selected; delivery planning can choose any additional dependency without reopening the visual direction.

### Remaining decisions and illustrative details

[Shop menus and item choices](01-shop-menus.md) retains ownership of menu maintenance, availability, remaining options, default coffee choice and specialty pricing. [Run lifecycle and closing rules](02-run-lifecycle.md) retains exact active/finished boundaries, concurrent announcement enforcement, closing-time changes, unavailable items, history scope and return/cancellation actions. Sample prices, menu contents, historical dates, blend preselection, a 15-minute default, 1–180 minute input limits, jokes, clock policy and period boundaries remain illustrative. The prototype stops accepting requests after collection as an example, not a settled lifecycle policy.

### Evidence and verification

[Preview guide](../prototype/README.md) links the selected and archived prototypes and explains how to run them. Playwright passed at 390px and 1440px: one active run plus past summaries, active-run announcement guard, empty state and announcement, exact duration chips, separate coffee choices in request summaries and consolidated shopping lists, juices/hot chocolate without choices, and one-click collection. All five screens fit without horizontal overflow; mobile menu overflow was also checked before collection. No JavaScript page errors occurred. Home layouts were visually inspected on phone and desktop, and menu controls on phone.

Production frontend/backend unit suites, Storybook and integrated frontend/backend/database E2E checks cannot run yet: the application and its test infrastructure have not been created. No prototype has been promoted. Branch publication remains unavailable without an initial commit and remote; the comparison is retained locally as linked evidence.
