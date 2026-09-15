# Katyayani RetailHub — Cart Request to the Partner App

**Version** 1.0 · **Date** 15 Sep 2026 · **Owner** Product (Umar) · **Audience** Sales Ops · RLM · Development · QA
**Companion to** Phase 2 Execution Document, Feature 3 (Sales cart request) — that document covers the retailer's side; this one covers the portal the caller uses.

---

## 1. What this is

An RLM agent is on a call with a retailer. Today the call ends with *"main WhatsApp pe bhej deta hoon"* and a list that the retailer re-types, or an order the agent books on their behalf with no retailer confirmation.

This feature gives the agent a **cart request**: they build the basket while talking, send it, and it lands in the retailer's app as a reviewable request with prices, margin and profit. The retailer accepts, and the items are in their own cart — they still check out themselves. **Accepting is not ordering.**

The retailer-side screen already exists (`sales-cart-request.html`). **The portal side does not exist at all** — this document specifies it.

---

## 2. Where it lands in RetailHub

The portal already exists and the retailer detail page already carries most of the context this feature needs. **Nothing here is a new console — it is one tab and one board.**

### What is already on the retailer page (`/retailers/KP-271585`)

| Element | Already there | The cart request uses it for |
| --- | --- | --- |
| Header | Retailer name, `KP-…` retailer id, `PII-…` id, **Ask Suggestion · Edit Profile · WhatsApp · Call** | The agent calls from here; the request is composed in the same place, not another tab |
| Serviceability strip | Pincode · **Serviceable** · Delhivery B2C / B2B · Shiprocket · Prepaid/COD | Whether a cart can be delivered at all, and by whom — read before composing |
| Tabs | Profile · Orders · Events · Timeline · Analytics · Coupons · Suggestions · **Expected Price** | Context while composing; Orders for history, Coupons for what can be applied |
| Profile cards | Basic Information (name, contact, email, **language**, joined) · Business Details (shop name, business type, **GST**, annual turnover, **VIP level**) · Address · **Verification** with document thumbs | Language for the request message, VIP for pricing tier, Verification for whether prices are unlocked on the app |
| Left nav | **My Team** Dashboard · Events · Retailers · Orders · RPS Action · Coupons · My Team Reporting | Team scoping already exists — the request board follows the same "My Team" pattern |
| Identity | Agent Id `AO-1126`, role chips (Manager / Super Admin) | created_by, approval routing |

### What this feature adds

| Addition | Where |
| --- | --- |
| **Cart Request** tab on the retailer detail page | Next to Orders / Coupons / Suggestions — composing happens in the retailer's own context, with Call and WhatsApp one click away |
| **My Team Cart Requests** in the left nav, under Main | The board: every request the agent or their team sent, and what happened to it |
| Cart-request column on **My Team Dashboard** | Sent / accepted / converted for the week, next to whatever the dashboard already tracks |

### Two existing tabs the composer should read, not duplicate

- **Expected Price** — if this records the price a retailer expects or has been quoted, the composer must show it beside the current price, because that is the number the retailer will argue with on the call.
- **Suggestions / Ask Suggestion** — if this already proposes products for a retailer, "Seed cart from suggestion" saves the agent typing the same basket again.

**Open Decision:** confirm exactly what those two tabs do today before wiring either — both are marked NEW in the portal, so their semantics may still be moving.

---

## 3. Systems reality (checked against the Knowledge Base, 15 Sep 2026)

This matters more than usual here, because the cart request spans **two different databases**.

| System | What is there | Reality |
| --- | --- | --- |
| **CRM Mongo** `retailers_v2` | Retailer master — `retailer_id`, `shop_name`, `is_verified`, `vip_level`, `pipeline_info`, `rps_info`, `call_info`, `language` | **Live.** ~202 docs. Retailer search and call context come from here. |
| **CRM Mongo** `orders_v2`, `products_v2`, `pincode_map_v2` | Orders, catalog, serviceability geography | **Live.** |
| **Sales-CRM (Supabase)** `agents` | Agent roster — **the spine**, 50 FKs from 49 tables point at it | **Live-ish.** 626 rows, all inserted 2026-07-02; treat as a roster of names, codes and emails, not a performance record. |
| **Sales-CRM** `partner_quotations` → `quotation_items` → `partner_orders` | Quotation header (number, status, approval cycle, total, **expiry**), lines (product, variation, qty, **quoted price**, packaging note), converted order | **Built, wired, 0 rows.** |
| **Sales-CRM** `partner_cart` | The partner's cart — lines reference **`quotation_items.id`, not `products.id`** | **Built, 0 rows.** |
| **Sales-CRM** `partner_price_rules` | Discount rules by segment / cohort / partner / product, quantity bands, **minimum-margin floor**, draft → approval → active → expired, two-person trail | **Built, 0 rows.** |
| **Sales-CRM** `partner_credit_controls` | Credit limit, outstanding, ordering/COD block flags, dunning stage — 1 row per partner | **Built, 0 rows.** |
| **Sales-CRM** `partner_product_visibility` | Who may see which product / category | **Built, 0 rows.** |
| **Sales-CRM** `b2b_partners` | Partner master the whole `partner_*` module hangs off — **18 dependants** | **0 rows.** |
| **Sales-CRM** `agent_districts`, `agent_pincodes` | Territory map | **0 rows, and cannot be filled** — the `districts` table they point at is also empty. Territory is scaffolding. |
| **Sales Ops portal modules** | `b2b_quotations/` (proxy to b2bsales quotations, FM-scoped) · `deal_approval/` (large-quantity orders needing manager sign-off) · `special_pricing/` (bottom-price requests, scoped by product/state/agent) · `serviceability/` · `inventory/` · `blacklist/` | **Live modules** the cart request should extend, not duplicate. |

### The finding that shapes the design

**A cart request is a quotation.** The `partner_*` module already models exactly this flow — a quotation with an expiry and an approval cycle, whose approved lines are pushed into the partner's cart (`partner_cart.quotation_item_id`), and which converts into an order. The odd constraint flagged in the Phase 2 doc — *"the cart references quoted lines, not products"* — is not a bug to work around; **it is this feature's design, already written down.**

So:

```
RLM builds a cart request   →  partner_quotations + quotation_items   (status: sent)
Retailer accepts in the app →  partner_cart rows (quotation_item_id)  (status: accepted)
Retailer checks out         →  partner_orders + partner_order_items
```

**Open Decision:** `b2b_partners` is empty while `retailers_v2` is live, so the two must be reconciled before a single row is written — see §12, decision 1. This is the one thing that blocks everything else.

---

## 4. Who does what

| Role | Can | Cannot |
| --- | --- | --- |
| **RLM / calling agent** | Search their retailers, build a request, apply approved scheme prices, send, track, cancel before acceptance, resend | Give a price below the approved floor without approval · order on the retailer's behalf · edit a request after it is sent |
| **Manager / FM** (the role chip on the profile, e.g. `AO-1126 · Manager`) | Everything an agent can, for their team · approve discount/quantity requests inside their limit · see the team board | Approve their own discount request (**Open Decision** — needs a policy call) |
| **Super Admin** | Configure expiry defaults, request caps, scheme catalogues, approval limits · see every board | — |
| **Finance / Accounts** | Set credit limits and blocks (`partner_credit_controls`) that the composer reads | Build or send requests |

Existing portal scoping is **FM-scoped** (B2B Quotations, Deal Approvals). The cart request follows the same scoping — no new permission model.

---

## 5. End-to-end flow

```
RLM PORTAL                                         PARTNER APP
─────────────────────────────────────────────      ─────────────────────────────────
Call lands / agent opens retailer
  → Retailer context (KYC, tier, credit, last order)
  → Build cart request
      add product → qty (cases/units) → price
      price below floor?  → Special pricing request → FM approves
      quantity above band? → Deal approval        → FM approves
  → Preview exactly as the retailer will see it
  → Send  (expiry, short message)
        └──────────── push + inbox ─────────────→  Notification: "Cart request from Rajesh"
                                                    → Opens cart request screen
                                                    → Reviews items, margin, profit
                                                    → Accept / Accept part / Decline
        ←─────────── outcome event ─────────────┘
  → Board updates: viewed / accepted / declined
  → Agent logs the call disposition                 → Items land in the retailer's cart
                                                    → Retailer checks out themselves
```

---

## 6. Screens (inside RetailHub)

### S1 · Getting to the retailer — existing
The agent is already on `/retailers/KP-271585` (from **My Team Retailers**, from the call, or from a search by phone). No new search screen. The only addition is that the **Cart Request** tab is visible from the moment the page opens, with a badge if a request is already live.

### S2 · Context the composer must surface (mostly already on the page)
The agent should never have to leave the tab to answer *"kya main ye bhej sakta hoon?"* Most of this is already on the Profile tab and in the serviceability strip; the composer repeats the four that decide whether a cart is sendable — **verification, credit, serviceability, blacklist** — in a single line above the basket.

| Block | Shows | Source |
| --- | --- | --- |
| Identity | Shop name, `KP-…` retailer id, owner, phone, language | Profile tab · `retailers_v2`, `contacts_v2` |
| Compliance | Verification card (Verified / pending) · licence expiry | Profile tab · `retailers_v2.is_verified` |
| Commercial | VIP level (bronze…diamond), RPS score, pipeline stage, expected price if recorded | Profile tab · **Expected Price** tab · `retailers_v2` |
| Money | Credit limit, outstanding, ordering blocked?, dunning stage | `partner_credit_controls` |
| History | Last 3 orders (date, value, items), last call + disposition | **Orders** and **Timeline** tabs · `orders_v2`, `calls_v2` |
| Serviceability | Pincode serviceable? which courier (Delhivery B2B / Shiprocket), prepaid vs COD | **The strip already at the top of the page** |

**Rule:** if ordering is blocked (credit or blacklist), the composer opens **read-only** with the reason at the top. Sending a cart the retailer cannot check out wastes the call and the retailer's trust.

### S3 · Build the cart request
- **Product search:** name, technical name, crop, pest — same catalog the app uses (`products_v2`), filtered by `partner_product_visibility`.
- **Seed from Suggestions** (if that tab already proposes products) and **Repeat last order** — two clicks that build most carts, because B2B reorders repeat.
- **Coupons** the retailer is eligible for are shown from the existing Coupons module, so the agent does not promise one that does not apply.
- **Each line shows:** pack size · case size and the **case ⇄ unit conversion** · retailer-applicable price · MRP · **margin %** · live stock at the mapped warehouse · scheme if one applies (e.g. *10+1*).
- **Quantity entry in cases by default** (that is how B2B orders are placed), with the unit equivalent shown under it.
- **Running summary:** subtotal · MRP saving · scheme value · delivery · **You pay** · **retailer's profit** — the same four numbers the retailer will see, so the agent is arguing from the retailer's screen, not their own.
- **Blocked lines** are shown, not hidden: out of stock, not visible to this partner, not serviceable → greyed with the reason.
- *Primary:* Preview & send · *Secondary:* Save draft · Request approval.

### S4 · Approvals (uses existing modules)
| Trigger | Goes to | Existing module |
| --- | --- | --- |
| Price below the approved floor (`partner_price_rules.min_margin`) | FM / pricing approver | `special_pricing/` |
| Quantity above the agreed band, or unusually large value | FM sign-off | `deal_approval/` |
| Both | Both, in one request — the agent should not file two forms | — |

While an approval is pending the request sits in **Pending approval** and **cannot be sent**. The retailer never sees a price that was not approved.

### S5 · Preview as the retailer
A faithful render of `sales-cart-request.html` — same items, margins, totals, expiry chip and advisor card. **The agent reads this aloud on the call.** Nothing in the app should surprise them.

### S6 · Send
- **Expiry:** default from config (the app's designed chip says *Expires in 22h*, i.e. a 24 h default) · agent may shorten, not extend beyond the cap.
- **Message:** short free-text note in the retailer's language (`retailers_v2.language`), shown above the items in the app.
- **Channel:** in-app notification + push. The page already has a **WhatsApp** button, so the fallback is a deep link sent through it when the retailer has not opened the app in N days — **Open Decision** on N and on whether that is in v1.
- On send: quotation created with status `sent`, expiry stamped, event emitted.

### S7 · Request board — **My Team Cart Requests**
Same shape as the existing My Team Orders / My Team Retailers screens, so it needs no new navigation habit.

| Column | Notes |
| --- | --- |
| Retailer | shop, city |
| Value | request total, and accepted value once decided |
| Items | count, hover for the list |
| Status | draft · pending approval · sent · **viewed** · accepted · partially accepted · declined (+ reason) · expired · cancelled |
| Sent | timestamp + who |
| Expires | live countdown |
| Outcome | order placed? value? — the number the whole feature is judged on |

Filters: my requests · my team (FM) · status · date · retailer. Bulk action: **resend expired**.

### S8 · Outcome & follow-up
- **Accepted** → agent sees which lines, and whether checkout happened. If the cart sits unconverted for X hours, the retailer appears in a **follow-up queue** (this is where the revenue actually leaks).
- **Partially accepted** → dropped lines with the retailer's decline reason, so the next cart is closer.
- **Declined** → reason chip from the app (*quantity too high · price high · already stocked · not the season · will order later · other*), written to the call record.
- **Expired** → one-tap **resend** creates a new request with today's prices, never the stale ones.

---

## 7. Status model

```
draft ──► pending_approval ──► sent ──► viewed ──┬─► accepted ────────► converted (order placed)
  │                                              ├─► partially_accepted ─► converted
  │                                              ├─► declined
  │                                              └─► expired ──► (resend → new draft)
  └─► cancelled_by_agent                          
sent ──► superseded   (a newer request replaced this one)
```

Rules: a status never moves backwards · `sent` is immutable (edits require cancel + new request) · only one **active** request per retailer at a time (**Open Decision** to confirm) · expiry is enforced server-side, not by the countdown in the UI.

---

## 8. Data model mapping

| Concept | Table | Notes |
| --- | --- | --- |
| Cart request header | `partner_quotations` | number, status, total, **valid_until** = expiry, created_by = agent, approved_by |
| Request lines | `quotation_items` | product, variation, qty, **quoted_price**, packaging note |
| Retailer accepts | `partner_cart` | one row per accepted line, `quotation_item_id` FK, `UNIQUE (partner_id, quotation_item_id)` → accepting twice is an upsert, not a duplicate |
| Checkout | `partner_orders` + `partner_order_items` | `quotation_item_id` carried through, so the quoted price is never re-keyed |
| Price floor | `partner_price_rules` | min-margin guard + approval trail |
| Credit gate | `partner_credit_controls` | blocks composing and checkout |
| Visibility | `partner_product_visibility` | filters the product search |
| Notification to retailer | `partner_notifications` | needs the columns listed in the Phase 2 doc (category, priority, expiry, read_at) |

**Events** (both directions): `cart_request.created` · `.submitted_for_approval` · `.approved` / `.rejected` · `.sent` · `.viewed` · `.accepted` (lines) · `.partially_accepted` · `.declined` (reason) · `.expired` · `.cancelled` · `.converted` (order id, value).

**APIs the portal needs** (names to be agreed, not invented here): retailer search · retailer context · product search with partner price · stock check · serviceability check · create/update request · submit for approval · send · cancel · board query · outcome webhook from the app.

---

## 9. Business rules

| # | Rule |
| --- | --- |
| 1 | An agent may only compose for retailers assigned to them; an FM for their team. **Open Decision:** territory tables are empty, so assignment has to come from somewhere else — most likely `retailers_v2` ownership. |
| 2 | Prices always come from the pricing service for **that** retailer. An agent can never type a free price — only request an approved one. |
| 3 | A request below the margin floor cannot be sent until approved. |
| 4 | If ordering is blocked (credit / blacklist), no request can be sent. |
| 5 | Accepting does **not** place an order, and the app says so. |
| 6 | Expiry is server-enforced; after it, the request is read-only for both sides. |
| 7 | Out-of-stock lines may be composed but are flagged; if stock disappears before acceptance, the app shows it at merge time rather than silently dropping it. |
| 8 | Every request is attributable: created_by, approved_by, sent_by, with timestamps. |
| 9 | Cancelling a sent request notifies the retailer — a request that vanishes silently is worse than one that expires. |

---

## 10. Notifications

| Event | To retailer (app) | To agent (portal) |
| --- | --- | --- |
| Sent | "Cart request from _Rajesh_ — _5 items, ₹20,314_, your profit _₹6,315_. Expires in _22 hours_." | — |
| Viewed | — | Retailer opened the request |
| Expiring | "Cart request ends in _2 hours_" | Request expiring, resend? |
| Accepted | — | Accepted — _₹18,900_ of _₹20,314_ |
| Declined | — | Declined — _price is high_ |
| Expired | "Cart request expired. Ask _Rajesh_ to send it again." | Expired without action |
| Converted | — | Order _#KAT-…_ placed from your request |

---

## 11. Analytics — what this feature is judged on

**Funnel:** requests sent → viewed → accepted → **converted to order** → delivered value.

| Metric | Why |
| --- | --- |
| Send → view rate | Is the notification reaching them at all |
| View → accept rate | Is the cart any good |
| **Accept → order rate** | The leak this feature is meant to close |
| Time to accept (median) | Whether 24 h expiry is right |
| Accepted / requested value | Cart quality per agent |
| Decline reasons | Product and pricing feedback with names attached |
| Requests per agent per day, and per call | Adoption — and misuse, if it spikes |

Per-agent and per-FM rollups, since the portal is already FM-scoped.

---

## 12. Open Decisions

| # | Decision | Owner | Blocks |
| --- | --- | --- | --- |
| 1 | **Which retailer master?** `retailers_v2` (CRM Mongo, live) vs `b2b_partners` (Supabase, 0 rows, 18 dependants). The cart request needs one identity across both. | Tech + Product | Everything |
| 2 | Is the cart request implemented **as a quotation** (`partner_quotations`/`quotation_items`), as this document recommends? | Tech | Data model |
| 3 | Agent → retailer assignment, given empty territory tables | Sales Ops | Rule 1 |
| 4 | Expiry default and cap; may an agent shorten it? | Business | S6 |
| 5 | Discount authority: who approves, up to what, and may an FM approve their own? | Business + Finance | S4 |
| 6 | One active request per retailer, or many? | Product | Status model |
| 7 | Duplicate-SKU merge in the app cart — sum or replace? (Open in the Phase 2 doc too; must be answered once, for both sides.) | Business | Accept |
| 8 | WhatsApp fallback in v1? | Product + Ops | S6 |
| 9 | Can a request go to a retailer whose KYC is pending (prices are gated for them)? | Business | S2 |
| 10 | Who builds the portal module — the RetailHub team or Partner App backend? | Tech leadership | Staffing |
| 11 | What do the **Suggestions** and **Expected Price** tabs actually hold today? Both are marked NEW and both are natural inputs to the composer. | RetailHub team | S3 |
| 12 | Does RetailHub read the same catalogue and pricing service the app uses, or its own? If they differ, the agent will quote a price the app refuses. | Tech | Rule 2 |

---

## 13. Acceptance criteria (QA)

1. Searching by phone number opens the right retailer in one step, with the context panel populated from live data.
2. A retailer who is blacklisted or credit-blocked opens read-only, with the reason stated.
3. Product search shows only products visible to that retailer, at that retailer's price, with stock and margin.
4. Quantity entered in cases shows the unit equivalent, and the summary totals match the retailer's app to the rupee.
5. A price below the floor cannot be sent — it routes to approval and the request stays **Pending approval**.
6. Preview matches the app screen exactly (items, margins, totals, expiry).
7. Sending creates the quotation with its expiry and produces the retailer notification within 60 s.
8. The board reflects **viewed / accepted / partially accepted / declined / expired** within one refresh of the app action, with the decline reason.
9. An expired request is read-only on both sides; resend creates a new request priced today.
10. Cancelling a sent request notifies the retailer and closes it on both sides.
11. Accepted lines appear in the retailer's cart referencing the quoted lines, at the quoted price.
12. Checkout from an accepted request is attributable back to the request and the agent in the board's Outcome column.
13. Every state change carries actor and timestamp, visible on the request's history.

---

## 14. Dependencies

**Katyayani RetailHub** — retailer detail page, My Team screens, Coupons, Suggestions, Expected Price · **Sales Ops portal** — existing modules: `b2b_quotations/`, `deal_approval/`, `special_pricing/`, `serviceability/`, `inventory/`, `blacklist/` · **CRM Mongo** — `retailers_v2`, `orders_v2`, `products_v2`, `calls_v2`, `pincode_map_v2` · **Sales-CRM** — the `partner_*` module and `agents` · **Partner App** — cart request screen, cart, checkout, notification inbox (Phase 2 Feature 2) · **Finance** — credit controls · **Marketing** — scheme catalogue

---

## 15. Out of scope

Agent placing the order on the retailer's behalf · negotiation threads or chat inside the request · PDF quotation documents for the retailer · payment collection by the agent · editing a request after it is sent (cancel and resend instead) · any change to how the retailer checks out.
