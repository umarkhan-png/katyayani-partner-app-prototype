# RLM Cart Request — Short Spec

**For** Katyayani RetailHub (`rlm-portel.ko-tech.in`) · **Date** 15 Sep 2026 · **App side** already designed (`sales-cart-request.html`)

---

## What it does

Agent is on a call with a retailer. He builds a cart in RetailHub and sends it. It lands in the retailer's app. Retailer accepts → items go into his own cart → he checks out himself.

**Accepting is not ordering.**

---

## Flow

```
RetailHub                                  Partner App
Open retailer → Cart Request tab
Add products, qty, price
Send (expires in 24h)  ───────────────→   Notification: "Cart request from Rajesh"
                                           Sees items, margin, profit
                                           Accept / Decline
Board shows the result  ←───────────────   Items in cart → retailer checks out
```

---

## Where it goes in RetailHub

| Add | Where |
| --- | --- |
| **Cart Request** tab | On the retailer page, next to Orders / Coupons |
| **My Team Cart Requests** | Left nav, under Main — the board |

Everything else is already there and gets reused: Call and WhatsApp buttons, serviceability strip (pincode, courier, COD), VIP level, Verification, language, Orders history, Coupons, and the existing "My Team" scoping.

---

## Screens

**1. Cart Request tab (compose)**
Product search → qty in cases (unit equivalent shown) → price from the pricing service → each line shows margin %, stock, scheme.
Bottom summary: You pay · Retailer's profit — same numbers the retailer will see.
Buttons: Preview · Send · Save draft.

**2. Preview**
Exactly what the retailer will see. Agent reads it out on the call.

**3. My Team Cart Requests (board)**
Retailer · value · items · status · sent · expires · outcome.
Filters: mine / my team / status / date. Action: resend expired.

---

## Status

```
draft → pending approval → sent → viewed → accepted / partly accepted / declined / expired
                                        → order placed (the number that matters)
```

Sent requests cannot be edited — cancel and send a new one.

---

## Rules

1. Price always comes from the pricing service. Agent cannot type a free price.
2. Below the margin floor → goes to approval first (existing `special_pricing` / `deal_approval` modules). Retailer never sees an unapproved price.
3. Credit-blocked or blacklisted retailer → cannot send.
4. Expiry default 24h, enforced on the server.
5. One active request per retailer at a time.
6. Cancel a sent request → retailer is notified.

---

## Backend

**A cart request is a quotation.** The tables already exist:

```
partner_quotations + quotation_items   (request sent)
        ↓  retailer accepts
partner_cart  (references quotation_item_id)
        ↓  checkout
partner_orders + partner_order_items
```

Events needed: `sent · viewed · accepted · declined · expired · converted`.

---

## Notifications

| Event | Retailer gets | Agent gets |
| --- | --- | --- |
| Sent | "Cart request from _Rajesh_ — 5 items, ₹20,314, your profit ₹6,315. Expires in 22h" | — |
| Viewed / Accepted / Declined | — | Status + reason |
| Expiring | "Cart request ends in 2 hours" | Resend? |

---

## Track this

Sent → viewed → accepted → **order placed**. Plus: time to accept, accepted value vs sent value, decline reasons, per agent.

---

## Needs a decision

1. **Which retailer master** — `retailers_v2` (live, Mongo) or `b2b_partners` (Supabase, empty)? Blocks everything.
2. Who approves discounts, and up to what limit?
3. Expiry — 24h fine?
4. Duplicate SKU already in the retailer's cart — add quantities or replace?
5. Can a request go to a retailer whose KYC is still pending?
6. What do the **Suggestions** and **Expected Price** tabs hold today? Both could feed the composer.
7. Who builds it — RetailHub team or Partner App backend?

---

## Not in this

Agent placing the order himself · chat inside the request · PDF quotations · payment collection · editing after send.
