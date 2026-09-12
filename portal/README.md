# Partner App — PM Analytics Portal

A working web portal for tracking the whole Katyayani Partner App: registration → verification →
product discovery → cart → checkout → delivery, every Explore feature, user engagement, behaviour,
journeys and flows — plus **MMP attribution via Linkrunner**, segments, churn risk, experiments,
app health and an evidence-backed test backlog.

**Live:** https://umarkhan-png.github.io/katyayani-partner-app-prototype/portal/
**Local:** open `portal/index.html` (no build step, no server needed)

---

## The 14 pages

| Page | What it answers |
|---|---|
| `index.html` — **Overview** | One screen for the whole app: north-star KPIs, GMV/order trend, the full install→first-order funnel, auto-generated alerts, state / channel / tier / SKU / tool breakdowns, goal gauges, app health, live experiments |
| `insights.html` — **Insights & Goals** | Computed insights, ranked leaks across all four funnels, opportunity sizing in ₹, 2σ anomaly detection with alert rules, the 20 Cr → 120 Cr scoreboard, a weekly review pack, and a decision log |
| `attribution.html` — **MMP · Attribution** | **Linkrunner**: channel performance (click→install→signup→verified→first order), CPI / CAC / cohort ROAS, campaigns, deep links & deferred deep links, CTIT and fraud, cohort quality, SDK health and the full event tracking plan |
| `funnel.html` — **Register → Verify** | The 12-step onboarding funnel with per-step breakdowns, verification & KYC ops (queue age, TAT, rejection reasons, auto-approve opportunity), a drop-off deep dive with hypotheses and fixes, and onboarding screen friction |
| `discovery.html` — **Discovery & Search** | Entry-path economics, search terms and the zero-result backlog, the real Katyayani SKU leaderboard, category detail, stock-out cost, and PDP behaviour incl. distributor-price unlock |
| `commerce.html` — **Cart & Checkout** | The cart→order funnel, abandonment causes with behavioural signals and fixes, payments & credit, basket/AOV levers, and schemes / coupons / coins with incrementality |
| `fulfilment.html` — **Orders & Delivery** | Order status pipeline, delivery TAT by state and district, cancellations & returns with root causes, the return-request flow, and post-order behaviour incl. reorder gaps |
| `explore.html` — **Explore Features** | All 13 Explore tools scored on reach × value × retention, a computed invest / fix / kill verdict per tool, in-tool funnels, Krishi AI Chat topic analysis, and a proposed hub re-ordering |
| `engagement.html` — **Engagement & Retention** | DAU/WAU/MAU and stickiness, the dormancy problem, power-user concentration, weekly retention cohorts, what first-week behaviour predicts, notifications & push, loyalty / coins / tiers, and home stories |
| `journeys.html` — **Journeys & Flows** | A session flow map, screen-by-screen analytics with a per-screen profile drawer, top paths, friction and error surfaces, and the full lifecycle with a single-partner event timeline |
| `segments.html` — **Segments & Cohorts** | RFM segments with the play for each, the churn-risk list ranked by GMV exposure, geography and expansion priority, tier value analysis, and an ad-hoc segment builder that exports a campaign audience |
| `partners.html` — **Partner Explorer** | Every partner searchable, leaderboards, the new-this-period cohort, the verification queue ranked by intent, and the verified-but-never-ordered list |
| `experiments.html` — **Experiments & Flags** | Every A/B test with a significance-aware read-out and priced business impact, feature flags and flag hygiene, a prioritised evidence-backed test backlog, and the rules we read tests by |
| `health.html` — **App Health** | Crash signatures and regressions, API latency and error rates, version & device spread, the force-upgrade case, and technical debt priced in GMV |

---

## What actually works

Everything is functional, not a static mockup:

- **Global filter bar** — date range (7 / 30 / 90 / 180 days) plus state, tier, segment, MMP channel
  and app version. Changing any of them re-renders every chart, table, KPI and **the wording of the
  insight cards** on the current page. Filters persist across pages via `localStorage`.
- **Period comparison** — every KPI delta is computed against the immediately preceding period of the
  same length, with "lower is better" handled correctly for CAC, crashes, cancellations and TAT.
- **Sortable tables** — click any column header; click again to reverse. Paginated where long,
  searchable where useful, with computed footer totals.
- **Drill-downs** — click a funnel step for its breakdown; click a table row to open a side drawer
  (partner profile with event timeline, screen profile, crash context, tool profile, experiment read-out).
- **Cross-filtering** — clicking a state, tier or segment row filters the whole portal to it.
- **CSV export** — the Export button is wired per tab and exports exactly what you are looking at.
- **Command palette** — `Ctrl/Cmd + K` searches pages, tools, MMP channels, SKUs, partners and screens.
- **Anomaly detection** — z-scores over the daily series, surfacing any 2σ+ move in the last 10 days.
- **Computed verdicts** — the Explore invest/fix/kill calls, the experiment ship/hold decisions and the
  opportunity sizing are all derived from the data, not hardcoded copy.

Charts are a hand-rolled SVG library (`assets/charts.js`) — line/area, grouped and stacked bars,
horizontal bars, donut, sparkline, funnel, cohort heatmap, flow/sankey, scatter and gauge — all with
hover tooltips. No external chart dependency.

---

## Files

```
portal/
  index.html insights.html attribution.html funnel.html discovery.html
  commerce.html fulfilment.html explore.html engagement.html journeys.html
  segments.html partners.html experiments.html health.html
  assets/
    portal.css    design tokens + components (Partner App brand: emerald/gold/Poppins)
    data.js       the whole dataset + formatters  ← swap this for real APIs
    charts.js     SVG chart library
    portal.js     shell: sidebar, filters, tables, CSV, drawers, command palette, insight engine
```

---

## The data

`assets/data.js` is a **deterministic seeded dataset** — a fixed PRNG seed means every reload and
every page shows the same numbers, so the portal can be reviewed and screenshotted reliably.

It is calibrated to one coherent business as of 12 Sep 2026, so numbers agree across pages:

| | |
|---|---|
| Verified partner base | 24,800 (goal 75K by Mar 2027) |
| MAU / DAU | 9.6K / ~2.4K (24% stickiness) |
| Installs | ~240 / day |
| Orders | ~110 / day, AOV ~₹10.4k |
| GMV | ~₹3.5 Cr / month → **₹41 Cr annualised** (goal ₹120 Cr) |
| Install → first order | 12.9% (goal 25%) |
| Cart → order | 43% (goal 60%) |
| CAC per verified partner | ~₹1,650 (goal ₹1,100) |

Product data uses the **real Katyayani catalogue** (Imida, Chakraveer, Chakrawarti, Azodharma,
Bhannaat, Bhumiraja, NPK 19-19-19, Humic + Fulvic 98, Triple Attack, Antivirus, Pro Grow …), the
real 13 Explore tools from `screens/explore.html`, and the real screen filenames from the prototype.

### Going live

Each exported function in `data.js` is the contract the portal reads — replace the generator body
with an API call and the UI needs no changes:

| Function / object | Replace with |
|---|---|
| `KO.daily` | daily metrics table from the warehouse |
| `KO.regFunnel()` / `KO.commerceFunnel()` | funnel queries |
| `KO.attribution()` / `KO.campaigns` / `KO.deepLinks` / `KO.sdkHealth` | **Linkrunner reporting API** |
| `KO.skuPerf()` / `KO.searchTerms` / `KO.categories` | catalogue + search analytics |
| `KO.tools` / `KO.exploreFunnels` | product analytics events (`explore_tool_opened` + step events) |
| `KO.cohorts` / `KO.notifCampaigns` / `KO.loyalty` | retention + CRM + loyalty ledger |
| `KO.screens` / `KO.topPaths` / `KO.sankey` | `screen_view` + `rage_click` events |
| `KO.partners` / `KO.partnerTimeline()` | partner table + event store |
| `KO.crashList` / `KO.apiEndpoints` / `KO.appHealth` | Crashlytics + APM |

The **tracking plan** on `attribution.html` → *SDK health & tracking plan* lists all 28 events the
portal depends on, who owns each one, and which three are currently specified but not firing
(`checkout_gst_added`, `distributor_price_unlocked`, `testimonial_submitted`). That tab is the
engineering brief for making this portal real.

---

## MMP — Linkrunner

Attribution is modelled on Linkrunner throughout, not bolted on:

- Install, click and deferred-deep-link attribution with a **7-day click / 1-day view** window and
  last non-direct click model, stated explicitly on the SDK tab.
- Channel economics carry both **GMV ROAS** and **gross-margin ROAS** (at 18%), and the insight engine
  only ever compares paid channels with paid channels — never paid acquisition against owned
  re-engagement.
- Cohort ROAS is the 90-day GMV of the partners acquired *in that window*, not total GMV in the window.
- Deep-link table includes the broken/unrouted links that open the app but land on Home.
- Fraud rules (click flood, install hijack, emulator, CTIT < 10s, duplicate device) with blocked counts,
  and CTIT flagged where it is suspiciously fast.
- Every campaign row carries its Linkrunner tracking link, plus naming and link-hygiene rules for the
  growth team.

---

## Design

Follows the Partner App design system: Poppins, emerald `#0E7A4E` / CTA `#0C831F` / dark `#083D28`,
gold `#D4A537` for anything loyalty or premium, `#E23744` for danger, `rounded-[10px]`, outline-only
SVG icons. Desktop-first (it is an internal tool), responsive down to tablet.
