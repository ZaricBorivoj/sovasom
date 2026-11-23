# Shop menus and item choices

Parent: [Office coffee and bakery ordering](../map.md)
Label: wayfinder:grilling
Type: grilling
Status: resolved
Assignee: Nemanja.Tomic (Codex session)
Blocked by: None

## Question

Who maintains shop menus, and how should colleagues select items, quantities, options, and notes? Decide what the first version needs for prices, unavailable items, and menu changes affecting existing requests. Identify who maintains the initial menus and how corrections reach them.

## Comments

### 20 November 2026 — constraints confirmed during frontend selection

Apply the [confirmed product requirements in Explore and choose the frontend direction](03-visual-direction.md#confirmed-product-requirements): coffee has a Blend / Specialty choice; juices and hot chocolate do not. Keep those choices distinct in request and collection summaries. Discuss default choice, specialty pricing and other options here; the prototype’s Blend default and equal example prices do not settle them. This ticket remains open.

### 20 November 2026 — menu decisions confirmed

The user accepted all six recommendations, with one correction: “Let's make Specialty the default”. The agreed decisions are recorded below.

## Answer

Resolved through live discussion with the user. Carry forward the [approved frontend requirements](03-visual-direction.md#confirmed-product-requirements); the decisions below settle the menu policies that preview deliberately left illustrative.

### Menu ownership and corrections

Designated office menu maintainers manage both shop menus. Nemanja.Tomic maintains the initial menu content. Colleagues report corrections to him outside the app; no in-app correction workflow is required for the first version. Maintainers can add, edit, reorder, and retire items. Other colleagues select from those maintained menus.

Assignment and administration of the maintainer permission belong to [Office membership and account lifecycle](06-office-access.md); this decision establishes the capability and initial maintainer.

### Choices, quantities, and notes

- Every run visits both shops, and requests remain grouped by shop.
- Each coffee offers Blend / Specialty, with **Specialty selected by default**. Show the choice before adding the item.
- Preserve the selected coffee choice in request summaries and the runner's shopping list. Keep Blend and Specialty quantities separate when consolidating. A request for one of each has two distinct lines.
- Juices and hot chocolate have no Blend / Specialty choice.
- Quantities are positive whole numbers.
- Each request line may have an optional note. For example, two Blend cappuccinos with an oat-milk note form one line; a regular-milk cappuccino is a separate line.
- Blend / Specialty is the only structured option in the first version. Structured sizes, milk selectors, and other option groups are deferred. Notes communicate preferences without guaranteeing availability or calculating extra charges.

### Prices

Show menu item prices and an estimated request total. Maintain separate Blend and Specialty prices for each coffee; those prices may differ. The prototype's equal example prices are not a pricing rule. Payments and debt tracking remain outside the first version.

### Availability and menu changes

Maintainers can mark an item unavailable. Prevent new selections of unavailable items, preserve existing request lines, and visibly flag affected lines. Never automatically substitute or delete them.

Submitted request lines preserve their item name, coffee choice where applicable, and displayed price when the menu changes. New selections use the updated menu. Retired items remain readable in existing requests and history. Thus changing a cappuccino's menu price does not silently reprice a submitted request.

[Run lifecycle and closing rules](02-run-lifecycle.md) owns request editing/withdrawal and the runner's handling of items unavailable at the shop. It must carry these preservation and availability constraints forward.

### Scope and verification

This resolves a planning decision only. No production code or prototype was changed; the approved preview remains visual evidence, with this ticket superseding its illustrative Blend default and pricing assumptions. Unit tests, Storybook, and integrated Playwright tests were not run because no application behavior was implemented.
