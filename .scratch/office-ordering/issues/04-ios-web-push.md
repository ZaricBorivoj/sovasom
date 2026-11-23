# Establish iOS web push feasibility

Parent: [Office coffee and bakery ordering](../map.md)
Label: wayfinder:research
Type: research
Status: resolved
Blocked by: None

## Question

What does a React/Vite web application need to deliver push notifications to colleagues on iOS? Establish supported OS/browser and installation conditions, permission and user-gesture requirements, HTTPS/service-worker/subscription requirements, server delivery options compatible with FastAPI, operational limits, and what can be verified with Playwright versus a real iOS device. Describe foreground, background, and closed-app expectations and what cannot be guaranteed. Separate facts from design recommendations; cite current primary sources and report a checked date.

Record evidence as a linked local Markdown asset. Research resolves platform facts; notification and onboarding product choices remain for the human decision ticket.

## Answer

Checked **2026-11-20**: Web Push is feasible for installed Home Screen web apps on iOS/iPadOS 16.4+, with HTTPS, explicit gesture-based permission and a subscription. No Apple Developer Program/APNs account setup is needed. Original Web Push needs a service worker and visible notifications; 18.4+ adds a declarative option without a required worker. iOS/iPadOS 26 also changes installation defaults, so a manifest is no longer universally required. Delivery is best effort, including when the app is inactive; Playwright cannot establish actual iOS/Apple delivery or OS behavior.

See [cited platform facts, FastAPI options and acceptance boundaries](../research/ios-web-push.md). Product choices remain open. No device tests or production changes were made. With no commits or remote, this research is retained locally; no research branch or push was possible.
