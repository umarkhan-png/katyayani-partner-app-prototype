# Katyayani Partner App — Prototype

Clickable HTML prototype for the Katyayani Partner App revamp (B2B agri-commerce, retailer/distributor app — 20cr → 120cr target).

**Live:** https://umarkhan-png.github.io/katyayani-partner-app-prototype/

## What's here

| File / Folder | Purpose |
|---|---|
| `index.html` | Phone-frame gallery — every screen as a clickable preview |
| `screens/` | 80+ HTML screens (full app flow: onboarding → KYC → home → PDP → cart → checkout → orders → tracking + every supporting feature) |
| `screens/design-system.html` | **Comprehensive dev hand-off design system** — tokens, components, patterns, illustrations, assets, Flutter mapping. Has WebP export buttons on every asset/icon/illustration (individual + section-bulk .zip) |
| `screens/ui-philosophy.html` | Design rationale + manifesto (why-we-did-what) |
| `assets/` | Logos, KYC sample docs, footer illustrations, presenter image |
| `partner-app-development-plan.csv` | **Sprint planning master sheet** — 196 rows: every screen / component / feature / flow / infra item with Phase, Priority, and Effort |

## Where to start

- **Designer / PM:** open `screens/design-system.html` for the full token + component catalogue
- **Flutter dev:** open `screens/design-system.html` (§19 "Developer Hand-off" has the Flutter mapping table) + import `partner-app-development-plan.csv` into Excel/Sheets and filter by Phase/Priority
- **Stakeholder demo:** open `index.html` in a browser, click any phone tile to enter the flow

## Tech

Static HTML + Tailwind (CDN) + vanilla JS. No build step. Hosted on GitHub Pages from `main` branch.

## Conventions

- Mobile-first 390×780 device shell
- Poppins font, emerald `#0E7A4E` + gold `#D4A537` brand
- Outline icons only (no filled / colourful illustrations)
- Real Katyayani SKUs only (no generic placeholders)
- B2B, baniya-mindset (margin-first, no consumer/lifestyle vibes)
- English-first labels
