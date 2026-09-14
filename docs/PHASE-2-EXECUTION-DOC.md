# Katyayani Partner App — Phase 2 Execution Document

**Version** 1.1 · **Date** 12 Sep 2026 · **Owner** Product (Umar) · **Audience** Product · UI/UX · Development · QA · Operations/RLM

> **v1.1 — 12 Sep 2026.** Feature 2 replaced: the pincode-first shop-address form becomes a **map-first location picker** (auto-placed pin, Places search, drag to correct) followed by a single details screen that asks for the shop name prominently and adapts to the address type. Plus-code results (`23XY+TF`) are discarded, keeping only pincode, district and state. Fields are consolidated the way retailers already know them (one premises field + one read-only locality block with **Change**); the shop journey asks no address type. The same two screens serve both journeys — shop details for verification (`?flow=shop`) and add-address inside the app (`?flow=address`). Runnable prototype: **`phase-2.html`** (one link: both flows + all states).

---

## 0. How to read this document

This document covers **Phase 2 only**. Phase 1 (regional languages, Supporting IDs, AI document scan + name match, KYC flow, new home, Shop by Crop, catalog filters, enhanced PDP, Wallet + Coins, Statement, Cash Deposit, Profit Calculator, Leaderboard, VIP Tier, Shop by Disease, Quick Order, Training Videos, Business Dashboard, Poster Generator) is treated as **live**. Phase 1 screens are referenced only where a Phase 2 feature extends them.

### Legend

| Tag | Meaning |
| --- | --- |
| **MH** | Must Have — in Phase 2 scope, blocks release |
| **NH** | Nice to Have — build only if the sprint allows, does not block |
| **Open Decision** | Not decided. Needs Product / Business / Tech confirmation. Nothing is invented here. |
| **Provider-dependent** | Feasibility depends on an external provider / SDK / OS capability, not on our code |

### One distinction used throughout

Most Phase 2 features already have a **designed prototype screen** in `katyayani-partner-app/screens/`. A prototype screen is **UI, not a feature** — it has no API, no state machine, no events. So for every feature this document separates:

1. **Designed** — the screen exists in the prototype
2. **Built** — the app renders it against real data
3. **Wired** — backend, events, notifications and the admin/RLM side exist

### Verified backend reality (checked against the Knowledge Base schema vault, 12 Sep 2026)

This matters because several Phase 2 features assume backend that is *built but empty*:

| Table / Collection | System | Reality today |
| --- | --- | --- |
| `retailers_v2` | CRM Mongo | **Live.** Master retailer record — `is_verified`, `has_document_details`, `referral_code`, `vip_level`, `language`, `pipeline_info`, `rps_info`. ~202 docs. Onboarding/KYC originates from the **RLM Portal**. |
| `orders_v2` | CRM Mongo | **Live.** `order_status` + `order_status_map[]` transition history, `booking_details.courier_status`, AWB. |
| `pincode_map_v2` | CRM Mongo | **Live.** 19,300 pincodes → district / district_id / state / state_id / territory / taluk / `geo{lat,lng}`, `source: india_post`. |
| `products_v2`, `crops_v2`, `crop_problems_v2`, `diseases` | CRM Mongo | **Live.** The only verified agronomy + catalog source. |
| `partner_notifications` | Sales-CRM (Supabase) | **Built, 0 rows.** 8 columns: title, message, type (info/success/warning/error), `link_url`, `is_read`, `created_at`. No channel, no read timestamp, no TTL, no broadcast/segment. |
| `partner_cart` | Sales-CRM | **Built, 0 rows.** Lines reference `quotation_items.id`, **not** `products.id` — i.e. a partner can only cart what was already quoted. |
| `partner_documents` | Sales-CRM | **Built, 0 rows.** `document_type` enum: gst_certificate, sales_license, pan_card, bank_details, address_proof, business_registration, p2p_agreement, license_endorsement, o_form, other. `is_verified` is a **boolean — there is no rejected state**. Has `expiry_date`. |
| `app_events` | Sales-CRM | **Built, 0 rows.** Generic `(who, what, when, payload)` analytics sink. No app telemetry has ever landed here. |
| `app_announcements` | Sales-CRM | **Built, 0 rows.** type enum banner / notification / popup, targeting by `segment_codes` / `cohort_ids` / `state_codes`, start/end window. |
| `tickets` | Sales-CRM | **12 rows, all manual, from the associate app.** Every SLA / routing / escalation column is NULL on every row. |
| KYC provider tables | — | **None found anywhere.** No DigiLocker / UIDAI / NSDL / GSTN provider contract is recorded in any inspected schema. See Feature 1 Open Decisions. |

> **Consequence for planning:** Phase 2 is not mostly a UI project. Notification infrastructure, the partner-cart contract, KYC provider contracts and app telemetry are either empty or undefined. The build sequence in §C reflects this.

### Phase 2 status snapshot

| # | Feature | Roadmap status | Designed | Built | Wired | The real Phase 2 work |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Supporting ID verification via OTP | Enhance | Yes — `kyc-aadhaar/pan/gst.html` | Partial | No | Provider contracts + OTP state machine |
| 2 | Map-first shop location & address | Enhance | Yes — `location-pin.html`, `shop-address-details.html` (new) | No | No | Google Maps/Places/Geocoding contract, plus-code fallback, `pincode_map_v2` reconciliation |
| 3 | Notification inbox | Enhance | Yes — `notifications.html` | No | No | Event catalogue + notification service + deep links |
| 4 | Return request flow | Enhance | Yes — inside `order-details.html` (KKD parity) | No | No | Return backend / reuse of the KKD return service |
| 5 | Refer & Earn | Enhance | Yes — `refer.html` (static) | No | No | Referral attribution + status machine + reward ledger |
| 6 | Testimonial capture | Enhance | Partial — `testimonial.html` is story-level, not product-level | No | No | Re-point to product-in-delivered-order (KKD parity) |
| 7 | Sales cart request (B2B via phone) | Pending | Yes — `sales-cart-request.html` | No | No | **RLM-side composer does not exist** + cart-merge contract |
| 8 | Product catalog download | Pending | None | No | No | Entire feature, including price-visibility rules |
| 9 | Krishi AI chatbot | Pending | Yes — `ai-chatbot.html` (scripted) | No | No | Retrieval layer, tool-calls, guardrails, escalation |
| 10 | My Farmers (CRM-lite) | Enhance | Yes — `my-farmers.html` | No | No | Farmer store + dedupe + reminders |
| 11 | Inventory tracker (per SKU) | Enhance | Yes — `inventory.html` (rich) | No | No | Stock ledger + delivered-order → inventory suggestion |
| 12 | Story rail | Testing | Yes — in `home.html` | Yes | Partial | Test + harden + content pipeline; no redesign |
| 13 | Screen share with support | Pending | Yes — `screen-share.html` | No | No | SDK selection + RLM console; **feasibility not proven** |

---

# FEATURE 1 — Document Verification via OTP for Supporting IDs

## 1. Status
**Enhance** — the screens exist; the verification engine behind them does not.

## 2. Objective
Let a retailer verify Aadhaar and Supporting IDs (PAN, GST, Voter ID) **inside the Partner App** with one familiar pattern — enter ID → OTP → details fetched → confirm — so KYC completion rises and price unlock happens on day one instead of day three.

## 3. Current State
- Aadhaar verification runs through **DigiLocker**: app → DigiLocker → security PIN → consent → OTP → back to app. The user leaves the Partner App.
- `kyc-aadhaar.html` already offers a **method chooser** — "Verify via OTP · Instant · 30 seconds (Fastest)" vs "Upload Aadhaar photo · Manual review · 1-2 days" — plus a 12-digit Aadhaar field with the helper "OTP will be sent to your Aadhaar-linked mobile number via UIDAI". The OTP path is **UI only** today.
- `kyc-pan.html` — PAN number + name + optional photo; copy reads "PAN is verified instantly via NSDL. No manual review needed." No OTP.
- `kyc-gst.html` — GSTIN field with an **auto-fetched details block** (Trade Name, Legal Name, Status, State); copy says details come from the GSTN portal; no upload, no OTP.
- Voter ID exists in the Supporting ID hub as a document choice (Phase 1) but has **no fetch/verify screen**.
- KYC state lives on `retailers_v2` (`is_verified`, `has_document_details`); the RLM Portal is the system of record for onboarding and KYC. `partner_documents` (Supabase) exists with a `document_type` enum and an `is_verified` **boolean**, and holds 0 rows.

## 4. Problem / Gap
1. **Redirect friction (Aadhaar).** Leaving for DigiLocker loses users at the PIN screen — many retailers have never set a DigiLocker PIN, and there is no in-app recovery path for that.
2. **Four different mental models.** Aadhaar = redirect, PAN = instant lookup, GST = silent fetch, Voter ID = nothing. Each ID looks like a different product.
3. **No OTP state machine anywhere** — send, resend, expiry, attempt limit, lockout and failure taxonomy are undefined in the app.
4. **No rejection state in the data model.** `partner_documents.is_verified` is a boolean; a failed verification can only be recorded as "not yet verified" plus a free-text note. The app cannot render "Rejected — re-upload" from that shape.
5. **No provider contract is documented** for UIDAI / NSDL / GSTN / ECI in any system we can inspect.

## 5. Proposed Solution

**One canonical pattern for every Supporting ID:**

`Select ID → Enter ID number (+ minimum fields) → Consent → Send OTP → Enter OTP → Provider verifies → Details fetched → Name-match check → User confirms → Saved + KYC status updated`

Where the provider does not support OTP for that ID type, the same screen chain runs **without the OTP step** — the user sees one step fewer, not a different design:

`Select ID → Enter ID number → Consent → Verify (silent lookup) → Details fetched → Confirm`

**Per-ID direction — product requirement vs provider dependency, kept separate:**

| ID | Product requirement | Provider / technical reality |
| --- | --- | --- |
| **Aadhaar** | Enter the 12-digit number in our UI → OTP to the Aadhaar-linked mobile → verified, name + masked address returned. Never leave the app. | **Provider-dependent.** In-app Aadhaar OTP requires an AUA/KUA-licensed provider or an Aadhaar-OTP-enabled offline-eKYC route. Without that entitlement, DigiLocker redirect stays for Aadhaar and we optimise the return journey instead. **Open Decision.** |
| **PAN** | Enter PAN + name → instant verification, name returned for match. | Standard PAN verification is **lookup-based, not OTP-based**. Treat PAN OTP as **not required** — do not design an OTP screen for PAN. |
| **GST** | Enter GSTIN → fetch Trade Name, Legal Name, Status, State, principal place of business. | Public GST taxpayer lookup is **lookup-based**. OTP appears only in GST-portal-authenticated flows (returns filing), which we are not doing. **Not applicable.** |
| **Voter ID** | Enter EPIC number (+ state or DOB as the provider requires) → fetch name, constituency. | Coverage is **provider-dependent** and typically lookup-based. Voter ID is **NH** for Phase 2 unless a provider confirms coverage. |

**Minimising the Aadhaar redirect if DigiLocker must stay (MH regardless of the provider outcome):**
- **Pre-redirect explainer sheet** — one screen, three lines, plain Hindi/English: what DigiLocker is, that a PIN is needed, that it takes about 40 seconds. Button: "Continue to DigiLocker".
- **Set-up rescue** — an "I don't have a DigiLocker PIN" link that opens DigiLocker's account-creation entry point and returns.
- **Deterministic return** — deep link back to `kyc-aadhaar` carrying a `kyc_session_id`; the app polls verification status rather than trusting the redirect payload, so a killed browser tab does not lose a completed verification.
- **Resume banner** — if the user returns without a result, show "Aadhaar verification in progress — checking…" with Retry, never a blank form.

**Name matching** reuses the Phase 1 AI name-match: provider name vs profile name, three outcomes — auto-pass, manual review, hard fail. Thresholds are an **Open Decision — Business confirmation required**.

## 6. User Flow

**Aadhaar — in-app OTP (target)**
```
Supporting IDs hub → Aadhaar → Method: Verify via OTP → Enter Aadhaar (12 digits)
→ Consent → Send OTP → OTP screen (6 digits + timer) → Verified
→ Details fetched (name, masked Aadhaar, address) → Name match → Confirm
→ Aadhaar Verified → back to Supporting IDs hub (status updated)
```

**Aadhaar — DigiLocker fallback**
```
Aadhaar → Verify via OTP → Pre-redirect explainer → DigiLocker (PIN → consent → OTP)
→ Return deep link → "Checking verification…" → Verified / Failed / Timed out
→ Retry or switch to Upload
```

**Aadhaar — manual upload fallback (exists today)**
```
Aadhaar → Upload photo → Front + Back capture → AI scan + name match (Phase 1)
→ Submitted → Under review (1–2 days) → Approved / Rejected (with reason) → Re-upload
```

**PAN / GST / Voter ID**
```
Supporting IDs hub → Select ID → Enter number (+ required field) → Consent → Verify
→ Fetching… → Details card → Name / entity match → Confirm → Verified
```

## 7. Screen-by-Screen UX

**S1 · Supporting IDs hub** (Phase 1 — extended, not redesigned)
- *Purpose:* one place showing every ID and its status.
- *Key UI:* list rows — ID name, one-line purpose, status chip (Not started / In progress / Under review / Verified / Rejected / Expired), chevron.
- *Rule carried from Phase 1:* **same CTA, subtitle and tag copy across all doc types** — no per-ID wording variants.
- *Primary CTA:* per-row "Verify". *Secondary:* "Why do we need this?" sheet.
- *States:* Default, Loading, All-verified, Action-required.

**S2 · Enter ID details**
- *Purpose:* capture the minimum needed to start verification.
- *Key UI:* title, one-line guidance, ID input with format mask, any required second field (Name on PAN / State for EPIC), **consent checkbox naming the provider explicitly**, primary CTA.
- *Validation:* Aadhaar — numeric, 12 digits, Verhoeff checksum, displayed `#### #### ####`; PAN — `AAAAA9999A`, auto-uppercase; GSTIN — 15 chars, state code 01–38, embedded PAN; EPIC — 3 letters + 7 digits (format varies by state; validate loosely and let the provider reject).
- *Masking:* Aadhaar shows only the last 4 once saved, everywhere including logs.
- *Primary CTA:* "Send OTP" (Aadhaar) / "Verify" (others), disabled until the format is valid. *Secondary:* "Upload instead".
- *States:* Default, Invalid format (inline), Disabled CTA, Submitting, Provider error.

**S3 · OTP screen** — shared component, see §A
- *Purpose:* confirm possession of the linked mobile.
- *Key UI:* masked destination ("OTP sent to mobile ending 4821"), 6 boxes, OS auto-read where available, countdown, Resend (disabled until the timer ends), "Change Aadhaar number", help link.
- *Primary CTA:* "Verify". *Secondary:* "Resend OTP".
- *States:* Default, Auto-filled, Verifying, Invalid OTP (attempts remaining shown), Expired (Resend becomes primary), Locked out, Provider unavailable, Success.

**S4 · Fetched details / confirmation**
- *Purpose:* show exactly what the provider returned before anything is saved.
- *Key UI:* details card (Name, masked ID, DOB / address / entity fields as applicable, provider status chip such as GST "Active"), a "This will be saved to your profile" note, mismatch banner when applicable.
- *Primary CTA:* "Confirm & Continue". *Secondary:* "Edit ID number" / "Use a different document".
- *States:* Default, Name match OK, Name mismatch (soft), Entity inactive (GST cancelled/suspended), Fetched-but-incomplete.

**S5 · Result screens**
- *Verified:* green check, what it unlocked (e.g. "Distributor pricing unlocked"), CTA "Continue KYC" or "Go to Home".
- *Under review:* expected time, what happens next, CTA "Back to Supporting IDs".
- *Failed:* one plain reason and one clear next action. Never a raw provider error code.

## 8. States
Default · Loading (send OTP, verifying, fetching) · Empty (no ID added) · Error (format, OTP, provider) · Success (verified) · Failure (rejected) · Pending (manual review) · Disabled (CTA before valid input; Resend before timer) · Expired (OTP expired; document past `expiry_date`) · Retry (provider down / network) · Locked (attempt limit reached)

## 9. Business Rules
1. Aadhaar is **mandatory**; PAN and GST are marked **Optional** on the existing screens (`3/6`, `4/6`). Licence handling stays exactly as Phase 1 defined it.
2. A verified document cannot be edited — only **replaced**, which resets that document's status.
3. Name-match thresholds (auto-pass / review / fail) — **Open Decision — Business confirmation required**.
4. Whether the **same document number already used by another retailer** blocks, soft-blocks or routes to manual review — **Open Decision — Business confirmation required**.
5. OTP attempt limit, resend cooldown, daily send cap and lockout duration — **Open Decision — Tech + Business (provider limits apply)**.
6. Whether GST status `Cancelled` / `Suspended` blocks verification or is accepted with a warning — **Open Decision — Business confirmation required**.
7. Which KYC level unlocks which pricing is **already defined in Phase 1; Phase 2 must not redefine it**.
8. A manual fallback must always exist for Aadhaar (it does today) — **MH**.

## 10. Backend / System Requirements
- **Verification service** (new) owning: session create, OTP send, OTP verify, detail fetch, name match, persistence, audit. One service with four adapters (Aadhaar, PAN, GST, Voter ID) — not four flows.
- **Provider adapters** — contracts undefined today; no provider record exists in any inspected schema. **Open Decision.**
- **Document store:** `partner_documents` is the natural home but needs (a) a **status enum replacing the `is_verified` boolean** (`pending · verified · rejected · expired`), (b) a rejection-reason column, (c) `voter_id` added to the `document_type` enum. This is a **schema change, not config**.
- **Retailer state:** `retailers_v2.is_verified` / `has_document_details` must be updated in the same transaction as the document result. RLM Portal is the current system of record — **ownership of the write is an Open Decision**.
- **Audit:** every provider call (request id, status, latency, masked payload) logged — required for any KYC dispute.
- **Events emitted:** `kyc.document.submitted`, `kyc.document.verified`, `kyc.document.rejected`, `kyc.document.expiring`, `kyc.status.changed` — consumed by Feature 3.

## 11. Notifications
- KYC submitted — "Your {document} has been submitted for verification."
- Supporting ID verified — "{document} verified. {benefit unlocked}."
- Supporting ID rejected — reason + CTA to re-verify.
- Additional document required.
- Document expiring — licence / GST expiry reminder driven by `expiry_date` (the prototype currently shows a static "Pesticide license expires on 15 May" item). **Lead time is an Open Decision.**

## 12. Analytics
`kyc_id_selected` (id_type) · `kyc_number_entered` · `kyc_consent_given` · `kyc_otp_sent` · `kyc_otp_resent` (count) · `kyc_otp_failed` (reason) · `kyc_otp_verified` (time_to_verify) · `kyc_details_fetched` · `kyc_name_mismatch` (score) · `kyc_confirmed` · `kyc_failed` (stage, reason) · `kyc_fallback_upload_used` · `kyc_digilocker_redirect_started` / `_returned` / `_abandoned` · `kyc_dropoff` (last_screen)

## 13. Edge Cases
- Aadhaar not linked to any mobile → OTP never arrives → after two failures, surface the upload fallback prominently.
- User changes SIM or mobile number between OTP send and entry.
- OTP auto-read captures a different app's OTP.
- Provider returns success with an **empty name** → name match impossible → route to manual review.
- GST returns Active but the Legal Name is a company while the retailer is a proprietor.
- PAN belongs to a firm while the profile name is the individual (or the reverse).
- Same Aadhaar already verified on another retailer account.
- App backgrounded mid-OTP, returned to after expiry.
- DigiLocker returns to the app after the session was already marked failed by timeout.
- Double-tap on Verify creating a duplicate submission.
- Licence already expired at the moment of verification.
- Provider rate-limits us at account level during a campaign spike.

## 14. Dependencies
**Partner App** (Supporting ID hub, Phase 1 AI scan + name match) · **RLM Portal** (system of record for KYC; manual review queue) · **RLM Admin** (rejection reasons, re-verification) · **Support** (KYC help tickets) · **External providers** (UIDAI/AUA-KUA or DigiLocker, PAN, GSTN, ECI — all unconfirmed) · **Legal/Compliance** (consent text, retention, Aadhaar masking)

## 15. Acceptance Criteria
1. From the Supporting IDs hub every listed ID opens the same three-step visual pattern; no ID dead-ends.
2. Aadhaar: an invalid checksum blocks "Send OTP" with an inline message and fires no API call.
3. A correct Aadhaar OTP verifies in ≤ 5 s on 3G and lands on the details card showing the provider-returned name.
4. A wrong OTP shows remaining attempts; after the configured limit the screen locks and offers the upload fallback.
5. OTP expiry converts Resend into the primary CTA, and the expired code is rejected server-side even if entered.
6. Resend stays disabled for the full cooldown and re-enables exactly once.
7. A name mismatch above threshold never silently passes — it blocks or routes to manual review, and the user sees which.
8. A rejected document renders a **Rejected** chip with a reason and a working re-verify CTA (requires the status-enum change).
9. Verified state survives an app restart and reflects on the hub, profile and any price-gated surface within one session refresh.
10. If the provider is down the user sees a retry screen — never an endless spinner, never a raw error code.
11. DigiLocker path: killing the browser tab mid-flow and reopening the app resolves to a definite state within 30 s.
12. Aadhaar is masked to the last 4 digits in every UI surface and in logs.

## 16. Out of Scope
Bank-account penny-drop verification · e-Sign / e-Mandate · periodic re-KYC campaigns · changing which documents are mandatory · pricing-unlock rules (Phase 1) · redesign of the RLM manual-review console.

## 17. Open Decisions
1. Can we obtain in-app **Aadhaar OTP** entitlement (AUA/KUA or an authorised aggregator)? If not, DigiLocker stays — confirm that is acceptable.
2. Which provider(s) for PAN, GST, Voter ID? Cost per hit, rate limits, SLA, sandbox availability.
3. Is **Voter ID** in Phase 2 scope at all, given lookup-only coverage?
4. Name-match thresholds and the manual-review band.
5. Duplicate-document policy across retailer accounts.
6. GST inactive / cancelled — block or warn?
7. Who owns the KYC write — Partner App backend or RLM Portal?
8. Consent text and data-retention period — Legal sign-off.
9. Who approves the `partner_documents` schema change (status enum + rejection reason + voter_id), and when?
10. Are the Supabase `partner_*` tables in use at all, or does live Partner App KYC write into the CRM Mongo / RLM stack? **This blocks estimation for Features 1, 3 and 7.**

---

# FEATURE 2 — Map-First Shop Location & Address

## 1. Status
**Enhance** — the onboarding address step is being replaced by a map-first flow. Both screens are now designed in the prototype (`location-pin.html`, `shop-address-details.html`); no service behind them yet.

## 2. Objective
Stop asking a retailer to type an address. Open a map with the pin already on them, let them correct it by dragging or searching, and then ask for the only thing the map cannot know — **what this place is called** — with everything else auto-filled and editable.

## 3. Current State
- **Today (live + Phase 1 prototype):** `rapido-shop-details.html` is a form — Shop Name, then Pincode\*, City/Tehsil\*, District, State, Shop Number, Village/Area, Landmark, plus a "Use my current location" button and an "Are you at your shop?" confirm sheet. It is address-first: the retailer types, and the map is nowhere.
- `add-address.html` (post-onboarding) repeats the same form with Address Type (Shop / Home / Warehouse / Other).
- **New Phase 2 prototype (designed, in the gallery under "1c. Phase 2 · Map-First Address"):**
  - `location-pin.html` — full-screen map, auto-placed pin, search pill, drag-to-move pin, current-location FAB, bottom sheet with the resolved address and **Confirm location**. States: locating · pin placed · searching · pin moved (re-resolving) · plus-code fallback · location off · network error.
  - `shop-address-details.html` — mini map strip with **Change location**, the prominent name question, **Address Type** tiles (Shop / Warehouse / Home / Other) that change what is asked, the type-specific number/building field, and the auto-filled, editable address block. States: filled · warehouse/home/other · pincode-only (plus-code) · validation error · saved.
- **`pincode_map_v2` (CRM Mongo) is live** — 19,300 pincodes → district, district_id, state, state_id, territory, territory_id, taluk, `geo{lat,lng}`, sourced from India Post.
- **No Google Maps Platform integration exists today** in any inspected system, and no maps/geocoding provider account is recorded.

## 4. Problem / Gap
1. **Typing is the bottleneck.** A B2B retailer on a 6-inch phone types eight fields; most abandon or fill them badly, and Dispatch pays for it later.
2. **A typed address has no coordinates.** Delivery partners need a point, not a paragraph. Today nothing captures one.
3. **Nothing is wired** — neither the old form nor the new screens fetch anything.
4. **Google results are not always addresses.** For rural and semi-urban India, reverse geocoding frequently returns a **Plus Code** (`23XY+TF Sanwer, Madhya Pradesh`) instead of a street address. Showing that to a retailer is meaningless and showing it to a delivery partner is worse. **This must be handled as a first-class case, not an error.**
5. **Two sources of truth for geography.** Google returns its own district/state naming; `pincode_map_v2` is what our routing, territory and serviceability logic actually uses. Without an explicit reconciliation rule, orders will be territory-mapped incorrectly.
6. `pincode_map_v2` caveats still apply: `pincode` is **not indexed** (collection scan today); `taluk` is missing on 418 docs and is the literal `"NA"` on 1,047; `geo.lat` is null on 1,096.

## 5. Proposed Solution

**Two screens. The map does the work; the retailer names the place.**

### Two journeys, one pair of screens (MH)

The same `location-pin.html` + `shop-address-details.html` pair serves both places a retailer gives us an address. **No separate screens are built for the second journey** — only the context changes.

| | **A · Shop details (verification)** | **B · Add address (inside the app)** |
| --- | --- | --- |
| Entry | Onboarding, after "Tell us about you" | Account → Addresses → Add new address |
| Purpose | Shop identity + location for **KYC verification**, and the same record becomes the **default delivery address** | An additional delivery point — second shop, godown, home |
| Context line | "Used for business verification — and saved as your default delivery address." | "Saved to your addresses. Pick the type so we deliver to the right place." |
| Address type | **Not asked.** It is the shop, by definition | Retailer picks: Shop / Warehouse / Home / Other |
| Fields | Shop name\* · shop no./floor/building\* · landmark | Type · name\* · no./floor/building\* · contact name\* · 10-digit mobile\* · alternate phone · landmark |
| Default address | Implicit — it is the first and only one | Explicit **"Make this my default address"** toggle |
| Save CTA | "Save & continue" → next onboarding step (`home-pending`) | "Save address" → back to Addresses |
| Back | Previous onboarding step | Addresses list |
| Flag | `?flow=shop` | `?flow=address` |

Both journeys write the **same address record** (name, type, unit, area, city, pincode, district_id, state_id, territory_id, lat/long, completeness). Journey A additionally sets the shop name used by KYC — see Open Decision 6 on whether that is the same field as `retailers_v2.shop_name`.

### Screen 1 — Set shop location (map)
- Opens with the device location requested and the pin auto-placed; the map is the screen, not a widget inside a form.
- **Three ways to get the pin right**, all equal citizens: (a) auto-detect, (b) **search** (Google Places Autocomplete — area, street, mandi, landmark), (c) **drag the map** under a fixed centre pin.
- The bottom sheet always shows what will be saved, and **Confirm location** is the only way forward.
- **Never block on GPS** — with permission denied the search path alone completes the flow.

### The plus-code rule (MH — this is the requirement that shapes the whole feature)
When the reverse-geocode result for the pin is a **Plus Code** (global code `7JXQ23XY+TF` or compound code `23XY+TF Sanwer`), or has no `route`/`sublocality`-level component:
1. **Discard the code entirely.** It is never shown to the retailer, never stored as the address line, never printed on a label.
2. **Keep only** `postal_code` (pincode), `administrative_area_level_1` (state) and the district component.
3. The sheet says so plainly — *"No street address is available for this pin. We have taken the pincode, district and state — you can add the area and landmark on the next screen."*
4. Screen 2 then treats **Area / locality as a required, empty field** and surfaces the landmark field, because the retailer is now the only source for it.
5. The pin's lat/long is still saved — the coordinates are the accurate part, and they are what the delivery partner navigates to.

### Screen 2 — Address details

Modelled on the pattern retailers already know from Flipkart/Swiggy-style address sheets: **the map's result is one consolidated block, not five inputs.**

- **Name first, mandatory.** `Shop name *` on the shop journey; on the address journey the label follows the type (`Warehouse name *`, `Full name *`, `Place name *`).
- **One free-text line for the premises** — `Shop no. / Floor / Building name *`. Required in both journeys; the label changes with type (`Gate no. / Godown`, `House no. / Floor`, `Unit no. / Floor`).
- **One consolidated locality block** replaces the old Area / City / Pincode / District / State inputs: a read-only card headed **Area / Locality** showing the resolved lines (e.g. *Krishi Mandi Road, Sanwer Road* / *Indore, Madhya Pradesh, 452001*) with a single **Change** button that returns to the map. Nothing in that block is typed; if it is wrong, the pin is wrong.
- **Area is asked only when the map could not give one** (the plus-code case) — then `Area / Village / Locality *` appears as a required field.
- **Landmark** stays optional in both journeys.
- **Shop journey asks no address type.** It is the shop; showing type tiles there is a question with one answer.
- **Address journey asks type first**, then the type-specific labels, then the contact block: `Contact person name *` and `10-digit mobile number *` (validated `[6-9]` + 9 digits), with `Alternate phone number` optional, and a **Make this my default address** toggle.
- **Change location** returns to the map with the pin where it was — the retailer never loses their place.

| Type (address journey only) | Name field | Premises field |
| --- | --- | --- |
| **Shop** | Shop name * | Shop no. / Floor / Building name * |
| **Warehouse** | Warehouse name * | Gate no. / Godown / Building name * |
| **Home** | Full name * | House no. / Floor / Building name * |
| **Other** | Place name * | Unit no. / Floor / Building name * |

### Reconciliation rule (MH)
Google gives the pin and the address text; **`pincode_map_v2` remains the authority for district, state and territory.** On confirm, the returned `postal_code` is looked up in `pincode_map_v2`; the mapped district/state (normalised from UPPERCASE India Post to Title Case) is what is stored and displayed. If Google's pincode is absent from the collection, the flow still completes, the Google values are stored, and the case is logged for a data refresh. Territory is always ours, never Google's.

### What is stored
Shop/place name · address type · unit/building · area · city · pincode · district_id · state_id · territory_id · **lat/long** · accuracy · source (`gps` | `search` | `manual`) · `address_completeness` (`full` | `pincode_only`) · the raw Google `place_id` for support lookups.

## 6. User Flow
```
A · Onboarding → Shop details        B · Account → Addresses → Add new address
→ Set shop location (map opens, permission requested)
   ├─ Allowed  → pin auto-placed → address resolved in the sheet
   ├─ Denied   → sheet offers "Turn on location" / "Search my area instead"
   └─ Search   → Places suggestions → select → pin moves → address resolved
→ [optional] drag map → pin lifts → "Getting address…" → re-resolved
→ Confirm location
   ├─ street address found → Shop & address details (address auto-filled)
   └─ plus code only       → Shop & address details (pincode + district + state only,
                              area required, plus-code note shown)
→ Enter name (prominent) → choose Address type → enter number/building
→ Review auto-filled address (edit if needed) → Landmark (optional)
→ Save address → Saved sheet (summary + type + "Pin saved") → Continue
```

## 7. Screen-by-Screen UX

**S1 · Set shop location** — `location-pin.html`
- *Purpose:* place an accurate pin with as little effort as possible.
- *Key UI:* top bar titled **"Shop Location"** (shop journey) or **"Add new address"** (address journey); search bar — *"Search by area, name, street"*; full-bleed map; fixed centre pin with a "Your shop location" chip that becomes "Move pin to your shop" while dragging; hint chip *"Move the map to place the pin on your shop"*; current-location FAB; bottom sheet.
- *Sheet content by state:* locating (spinner + "Keep your phone still for a moment", CTA disabled) · resolved (locality title, full address line, **Change**, optional low-accuracy warning "We could not pin this exactly (±240 m)") · re-resolving after a drag (skeleton + "Getting address…") · plus-code (explanation + three chips: pincode, district, state) · permission off · network error.
- *Primary CTA:* **"Add shop details"** / **"Add address details"**. *Secondary:* "Change" / "Search my area instead" / "Retry".
- *Navigation:* back → previous onboarding step; forward → S2.

**S2 · Search location** — overlay inside `location-pin.html`
- *Purpose:* find a place by name when GPS is wrong or unavailable.
- *Key UI:* focused input, "Use my current location" row pinned at the top, **Recent** list, then Places-style predictions (bold main text + grey secondary), no-result state offering "Drop pin on map".
- *States:* Recent (empty query) · Results · No result · Selected (returns to map with "Getting address…").

**S3 · Shop & address details** — `shop-address-details.html`
- *Purpose:* name the place and confirm the address in one screen.
- *Key UI:* mini map strip with the pin + **Change location**; confirmed address line; the prominent name question and a large input; Address Type tiles; the type-specific number/building field; auto-filled address block with the "Auto-filled from map" badge; landmark; sticky **Save address**.
- *Validation:* name required → *"Please enter a name for this address"*; number/building required → *"Delivery needs this — please add the number or building"*; area required → *"Please add the area or village name"*. Errors are inline and scroll the offending field into view.
- *States:* Default (auto-filled) · Pincode-only (plus-code note, area empty and required) · Type switched · Address unlocked/edited · Validation error · Saving · Saved.

**S4 · Saved sheet**
- *Purpose:* confirm what was saved before moving on.
- *Key UI:* tick, "Shop address saved", one-line summary (name · unit, area, city, state, pincode), chips for type and "Pin saved", **Continue**, and a quiet "Edit address".

## 8. States
Default · Loading (locating, resolving, saving) · Empty (no saved address) · Error (permission, network, geocode failure, save failure) · Success (saved) · Disabled (Confirm while resolving) · Retry · Denied (permission) · Not-found (no prediction matches) · Pincode-only (plus-code fallback) · Edited (locked fields overridden)

## 9. Business Rules
1. An address cannot be saved without a **confirmed pin** (lat/long). **MH.**
1a. Journey A (shop details) always saves as the **default** address and feeds KYC; journey B makes default an explicit choice. **MH.**
2. **Mandatory:** name and premises (no./floor/building) in both journeys; plus contact name and a valid 10-digit mobile on the address journey; plus area **only** when the map returned no street address. Landmark and alternate phone are optional. **MH.**
2a. The resolved locality is **not editable as text** — it is one read-only block with a **Change** button back to the map. A wrong locality is corrected by moving the pin, not by retyping. **MH.**
2b. The shop journey does **not** ask for an address type. **MH.**
3. A plus-code result is never shown or stored as the address line; only pincode, district, state and the coordinates survive. **MH.**
4. `pincode_map_v2` is authoritative for district / state / territory; Google's values are a cross-check, not the record. **MH.**
5. If the retailer insists the resolved locality is wrong but the pin is right, that is an **Open Decision** — today the only path is moving the pin.
6. Serviceability check on the confirmed pincode — **Open Decision — Business confirmation required** (`pincodeblacklists` exists; whether onboarding hard-blocks is a business call).
7. Address change after KYC approval — does it need re-verification? **Open Decision — Business confirmation required.**
8. Maximum saved addresses per retailer, and whether a warehouse address can be the default delivery address — **Open Decision.**
9. Whether the shop name captured here is the same field as the KYC/business name on `retailers_v2.shop_name`, or a separate display name — **Open Decision. If they are the same field, a change here must follow the KYC rules, not overwrite silently.**

## 10. Backend / System Requirements
- **Google Maps Platform** (all provider-dependent, none contracted today):
  - *Maps SDK for Android/iOS* — map display and the drag interaction.
  - *Geocoding API* — reverse geocode the confirmed pin into address components.
  - *Places API — Autocomplete + Place Details* — the search path (use **session tokens**, or autocomplete billing will be materially higher).
  - *Address Validation API* — **NH**, only if Business wants a quality score on the typed portion.
  - Device GPS via the OS, not a Google API.
- **Component mapping** (Google → our fields): `postal_code` → pincode · `administrative_area_level_1` → state · `administrative_area_level_3` / `_2` → district (cross-checked against `pincode_map_v2`) · `locality` / `sublocality` / `neighborhood` → area · `route` + `street_number` → address line · `premise` / `subpremise` → building hint. **Anything matching the plus-code pattern is dropped before mapping.**
- **Pincode lookup endpoint** over `pincode_map_v2` — still required, both for the reconciliation rule and for the manual path. **Needs an index on `pincode`** before app traffic.
- **Address persistence** — `addresses` (CRM Mongo) is the candidate store; the schema must gain lat/long, accuracy, source, place_id and `address_completeness`. **Open Decision.**
- **Normalisation utility** shared by app and backend: UPPERCASE India Post → Title Case; `"NA"` taluk → empty.
- **API key security** — restricted keys per platform, quota alerts, and a server-side proxy for geocoding if key exposure is a concern. **Open Decision — Tech.**
- **Events:** `address.location_confirmed` (source, accuracy, completeness), `address.created`, `address.updated`, `address.override_used`.

## 11. Notifications
None inherent to this feature. Whether Dispatch is alerted when an address or pin changes on an in-flight order is an **Open Decision**.

## 12. Analytics
`location_screen_viewed` (context: onboarding | add_address) · `location_permission_prompted` / `_granted` / `_denied` · `location_autodetect_succeeded` (accuracy_m, time_ms) / `_failed` · `location_search_opened` · `location_search_query` (length) · `location_search_result_selected` (rank) · `location_search_no_result` (query) · `map_pin_dragged` (distance_m, count) · `geocode_returned_pluscode` — **the key metric: it sizes the rural fallback problem** · `location_confirmed` (source: gps | search | drag, completeness) · `address_form_viewed` · `address_type_selected` (type) · `address_autofill_edited` (field) · `address_locked_field_overridden` (field) · `address_saved` (fields_typed_count, completeness) · `address_save_failed` (reason) · funnel: map opened → pin confirmed → details saved

## 13. Edge Cases
- **Plus-code-only result** (the headline case) — handled above; must be tested in a real rural pincode, not only in staging.
- Retailer is at home, not at the shop, when onboarding — the pin is wrong by kilometres; the "Change location" path and the drag hint are the mitigation.
- GPS accuracy > 200 m (common indoors in a concrete market building) — low-accuracy warning shown; confirmation still allowed.
- Pin dragged across a district or state boundary — reconciliation must re-resolve everything, not just the address line.
- Google returns a pincode absent from `pincode_map_v2`.
- Google's district name differs from India Post's (very common) — ours wins.
- Permission granted once, revoked later in OS settings.
- Mock/spoofed location.
- Places returns nothing for a small village name — the "Drop pin on map" escape must be visible in the no-result state.
- Search in a regional script.
- Network drops between confirming the pin and saving the details — the pin and form state must survive.
- Map SDK fails to load (old device, Play Services missing) — the flow must fall back to the pincode form rather than dead-end. **MH.**
- Two retailers at the same premises save the same pin — allowed.
- Retailer taps Confirm while the address is still resolving — CTA is disabled in that state.

## 14. Dependencies
**Partner App** onboarding + Addresses · **Google Maps Platform** (Maps SDK, Geocoding, Places — **contract and billing not in place**) · **CRM Mongo** (`pincode_map_v2`, `addresses`, `pincodeblacklists`) · **Dispatch** (pin quality, serviceability, label format) · **RLM** (address corrections during onboarding calls) · **Finance/Tech** (Maps billing account, key restrictions)

## 15. Acceptance Criteria
1. The map opens with the pin auto-placed within 3 s of permission being granted, and the resolved address appears in the sheet without any further tap.
2. Dragging the map lifts the pin, shows "Getting address…", and resolves to the new address within 1.5 s on 3G.
3. Searching returns Places predictions; selecting one moves the pin and resolves that address.
4. Denying location permission never blocks the flow — search and manual pin placement still complete it.
5. **A plus-code result never appears anywhere in the UI or in the saved record.** The sheet shows the pincode/district/state explanation, and the next screen marks Area as required and empty.
6. The saved record always contains lat/long, and `district_id` / `state_id` / `territory_id` resolved via `pincode_map_v2` — not Google's district string.
7. The locality block shows Title Case names, never UPPERCASE India Post strings, and never an empty or "NA" line.
8. On the address journey, changing the type changes the name and premises labels; the shop journey shows no type control at all.
9. Saving is blocked with an inline message, and the field scrolled into view, when: name is empty · premises is empty · area is empty in the plus-code case · contact name is empty or the mobile is not a valid 10-digit number (address journey).
10. The locality block is read-only and its **Change** button returns to the map with the pin intact.
11. "Change location" returns to the map with the pin at its confirmed position, and returning re-fills the form without losing what was typed.
12. If the Maps SDK cannot load, the retailer is offered the pincode form and can still finish onboarding.
13. The saved sheet's summary matches exactly what was stored.

## 16. Out of Scope
Turn-by-turn navigation or delivery-partner routing UI · saved-address map clustering · geofenced attendance or visit verification · address autocomplete inside the details form (search lives on the map screen) · Street View · bulk address import · changing what Dispatch prints on a label.

## 17. Open Decisions
1. **Google Maps Platform account, billing owner and monthly cost ceiling** — Autocomplete + Geocoding at onboarding scale is the main cost driver. Who owns this?
2. Are session tokens and key restrictions in place before launch? (Tech.)
3. Is `addresses` (CRM Mongo) the store of record, and who approves adding lat/long, accuracy, source, place_id and completeness?
4. Who approves the `pincode` index on `pincode_map_v2` (production DB change)?
5. Do blacklisted / non-serviceable pincodes block onboarding, warn, or pass through?
6. Is the shop name captured here the same record as `retailers_v2.shop_name` / the KYC business name?
7. Does a post-KYC address or pin change trigger re-verification or an RLM check?
8. Is Address Validation API worth adding (**NH**), or is the pin plus our pincode reconciliation enough?
9. Fallback policy when the Maps SDK is unavailable — pincode form (recommended) or block?
10. Does the old `rapido-shop-details.html` pincode form stay as the fallback path, or is it retired once this ships?

---

# FEATURE 3 — Notification Inbox

## 1. Status
**Enhance** — `notifications.html` is designed. The event catalogue and the service behind it do not exist.

## 2. Objective
One feed for everything that happened to the retailer's orders, money, KYC and requests — each row a one-tap route to the screen where they can act.

## 3. Current State & Gap

| | Today |
| --- | --- |
| In the app | Push on order placement only. No inbox, no read state, no history. |
| Designed | `notifications.html` — unread count, Mark all read, tabs **All / Orders / Offers / System**, day groups, relative time, end-of-list. States added: `?state=empty\|loading\|error`. |
| `partner_notifications` (Supabase) | Built, **0 rows**. Has title, message, type, `link_url`, `is_read`, `created_at`. **Missing:** category, `read_at`, priority, entity ref, expiry, audience/broadcast. |
| `app_announcements` | Built, **0 rows**. Broadcast + segment targeting. Unused. |
| Missing entirely | Event catalogue · notification service + templates · deep-link registry · push provider mapping · retention rule. |

---

## 4. Notification Catalogue

**How to read:** _italics_ = dynamic value filled at send time. **Push** = also fires a device notification (not only inbox). **Type A** = action required (sorts above informational, allowed outside quiet hours).

### 4.1 Orders

| # | Event | Title | Message | Opens | Push | Type |
| --- | --- | --- | --- | --- | --- | --- |
| O1 | `order.placed` | Order placed | Order _#KAT-2026-09-1284_ for _₹20,314_ is confirmed. We will tell you when it ships. | Order details | Yes | Info |
| O2 | `order.confirmed` | Order confirmed | _5 items_ confirmed and sent to the _Indore_ warehouse. | Order details | No | Info |
| O3 | `order.packed` | Packed | Your order is packed at _Indore_ warehouse and waiting for pickup. | Order details | No | Info |
| O4 | `order.shipped` | Shipped | _#1284_ has been picked up by _Delhivery_ · AWB _46095296957_. Arriving by _15 Sep_. | Order tracking | Yes | Info |
| O5 | `order.out_for_delivery` | Out for delivery | _#1284_ is out for delivery — arriving by _6 PM_ today. Keep _₹12,400_ ready for COD. | Order tracking | Yes | Info |
| O6 | `order.delivered` | Delivered | _#1284_ delivered at _11:04 AM_, signed by _Rakesh_. | Order details | Yes | Info |
| O7 | `order.delayed` | Taking longer | _#1284_ is delayed at _Bhopal hub_. New delivery date is _16 Sep_. Sorry for the wait. | Order tracking | Yes | Info |
| O8 | `order.cancelled` | Order cancelled | _#1284_ has been cancelled. _₹2,000_ advance will be refunded in _3–5 working days_. | Order details | Yes | Info |
| O9 | `order.failed` | Order could not be placed | _#1284_ could not be confirmed — _stock ran out for 2 items_. Nothing was charged. | Cart | Yes | **A** |
| O10 | `order.payment_pending` | Payment pending | _₹20,314_ for _#1284_ is still pending. Pay by _14 Sep_ or the order will be released. | Order details | Yes | **A** |
| O11 | `order.payment_failed` | Payment failed | Payment of _₹20,314_ failed at your bank. Money is not deducted — please try again. | Checkout | Yes | **A** |

### 4.2 Returns

| # | Event | Title | Message | Opens | Push | Type |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | `return.requested` | Return request sent | Return for _Katyayani Bhumiraja, 3 units_ is submitted. Request _#RTN-4471_. | Return status | Yes | Info |
| R2 | `return.approved` | Return approved | Return _#RTN-4471_ approved. _Full refund_ pre-approved, pickup will be scheduled. | Return status | Yes | Info |
| R3 | `return.rejected` | Return not approved | Return _#RTN-4471_ was not approved — _seal was opened and partly used_. Tap to see details or talk to support. | Return status | Yes | **A** |
| R4 | `return.info_needed` | More details needed | We need _clearer photos of the damaged box_ for return _#RTN-4471_ to move ahead. | Return status | Yes | **A** |
| R5 | `return.pickup_scheduled` | Pickup scheduled | _Delhivery_ will pick up _#RTN-4471_ on _14 Sep, 10 AM–6 PM_. Keep the units in the original box. | Return status | Yes | **A** |
| R6 | `return.picked_up` | Picked up | _#RTN-4471_ picked up. Refund starts after quality check at the warehouse. | Return status | No | Info |
| R7 | `replacement.dispatched` | Replacement on the way | Replacement for _Imida 30.5% SC, 6 units_ has been dispatched · AWB _46095296957_. | Order tracking | Yes | Info |
| R8 | `refund.initiated` | Refund started | _₹1,092_ refund for _#RTN-4471_ has been sent to your _wallet_. | Wallet | Yes | Info |
| R9 | `refund.completed` | Refund completed | _₹1,092_ is now in your _wallet_. Reference _UTR 4471029_. | Wallet | Yes | Info |

### 4.3 KYC & documents

| # | Event | Title | Message | Opens | Push | Type |
| --- | --- | --- | --- | --- | --- | --- |
| K1 | `kyc.submitted` | Document submitted | Your _Aadhaar_ is submitted. We check it within _1–2 working days_. | Documents | No | Info |
| K2 | `kyc.verified` | _Aadhaar_ verified | _Aadhaar_ verified. _Distributor pricing is now unlocked_ on your account. | Documents | Yes | Info |
| K3 | `kyc.rejected` | _Aadhaar_ not verified | _Aadhaar_ could not be verified — _name did not match your profile_. Tap to try again. | Documents | Yes | **A** |
| K4 | `kyc.document_required` | One more document needed | To finish verification we need your _pesticide licence_. It takes a minute. | Documents | Yes | **A** |
| K5 | `kyc.completed` | Verification complete | Your business is verified. Prices, credit and bulk orders are open now. | Home | Yes | Info |
| K6 | `kyc.document_expiring` | _Licence_ expiring | Your _pesticide licence_ expires on _15 May_. Upload the renewed copy to keep ordering. | Documents | Yes | **A** |

### 4.4 Money

| # | Event | Title | Message | Opens | Push | Type |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | `wallet.credited` | _₹500_ added | _₹500_ credited to your wallet — _referral reward from Ramesh Agro Centre_. | Wallet | Yes | Info |
| M2 | `wallet.debited` | _₹4,820_ used | _₹4,820_ used from wallet for order _#KAT-2026-09-1284_. | Statement | No | Info |
| M3 | `coins.earned` | _250 coins_ earned | You earned _250 coins_ on order _#1284_. _1 coin = ₹1_ on your next order. | Coins | Yes | Info |
| M4 | `coins.redeemed` | Coins used | _50 coins_ used — _₹50_ off on order _#1284_. | Coins | No | Info |
| M5 | `coins.expiring` | _180 coins_ expiring | _180 coins_ expire on _30 Sep_. Use them on your next order. | Coins | Yes | **A** |
| M6 | `deposit.received` | Cash deposit received | Your deposit of _₹50,000_ at _HDFC Indore_ is credited to your account. | Statement | Yes | Info |
| M7 | `deposit.mismatch` | Deposit needs a check | We received _₹48,000_ against your slip of _₹50,000_. Our team will call you today. | Cash deposit | Yes | **A** |
| M8 | `credit.due` | Payment due in _3 days_ | _₹42,800_ for invoice _#KAT-1102_ is due on _18 Sep_. | Statement | Yes | **A** |
| M9 | `credit.overdue` | Payment overdue | _₹42,800_ for invoice _#KAT-1102_ is _4 days_ overdue. New orders are on hold until it is cleared. | Statement | Yes | **A** |

### 4.5 Business & features

| # | Event | Title | Message | Opens | Push | Type |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | `cart_request.received` | Cart request from _Rajesh_ | Your advisor _Rajesh_ sent a cart — _5 items, ₹20,314_, your profit _₹6,315_. Expires in _22 hours_. | Cart request | Yes | **A** |
| B2 | `cart_request.expiring` | Cart request ends soon | _Rajesh's_ cart request expires in _2 hours_. | Cart request | Yes | **A** |
| B3 | `cart_request.expired` | Cart request expired | The cart request from _Rajesh_ has expired. Ask him to send it again. | Notifications | No | Info |
| B4 | `inventory.delivered_stock` | Add _36 units_ to inventory | _36 units_ from order _#1284_ were delivered. Add them to your stock in one tap? | Add delivered stock | Yes | **A** |
| B5 | `inventory.low_stock` | _3 products_ running low | _Chakraveer_ is down to _8 cases_ (your alert is _10_). Reorder before the season picks up. | Inventory | Yes | **A** |
| B6 | `referral.joined` | _Vikas_ joined | _Vikas Kheti Mart_ signed up with your code. _₹500_ comes after their first delivered order of _₹2,000+_. | Refer & Earn | Yes | Info |
| B7 | `referral.step_done` | _Vikas_ completed KYC | _Vikas Kheti Mart_ is verified. One step left — their first order of _₹2,000+_. | Refer & Earn | No | Info |
| B8 | `referral.rewarded` | _₹500_ referral reward | _₹500_ credited for referring _Ramesh Agro Centre_. | Wallet | Yes | Info |
| B9 | `referral.rejected` | Referral not eligible | _Sharma Krishi Kendra_ was already a Katyayani retailer, so this referral does not qualify. | Refer & Earn | No | Info |
| B10 | `review.requested` | Rate what you received | How did _Katyayani Bhumiraja_ work? Your review helps other retailers. | Rate products | Yes | Info |
| B11 | `review.published` | Your review is live | Your review of _Katyayani Bhumiraja_ is now on the product page. | PDP | No | Info |
| B12 | `review.rejected` | Review not published | Your review of _Chakraveer_ was not published — _competitor name mentioned_. You can edit and resubmit. | Rate products | No | Info |
| B13 | `scheme.new` | New scheme · _NPK 10+1_ | Buy _10 NPK 19-19-19_ bags, get _1 free_. Valid till _30 Sep_. | Scheme / PDP | Yes | Info |
| B14 | `price.drop` | Price drop · _Chakraveer_ | _Chakraveer 250 ml_ is now _₹440_ (was _₹480_) — margin up to _22%_. | PDP | Yes | Info |
| B15 | `stock.back` | Back in stock | _Antivirus 1+1_ is available again at _Indore_ warehouse. Limited stock. | PDP | Yes | Info |
| B16 | `vip.tier_up` | You are _Gold_ now | You reached _Gold_ — _60 coins per ₹1,000_ and _7% Coins OFF_ from today. | VIP | Yes | Info |
| B17 | `vip.tier_risk` | _Gold_ ends in _12 days_ | Order _₹38,000_ more by _26 Sep_ to stay on _Gold_. | VIP | Yes | Info |
| B18 | `leaderboard.rank` | You are _#4 in MP_ | You moved up _2 places_ this week. _₹18,000_ more to reach _#3_. | Leaderboard | No | Info |
| B19 | `training.new` | New course · _Rabi season_ | _8 videos, 45 minutes_. Finish it to earn _200 coins_. | Training | No | Info |
| B20 | `support.replied` | Support replied | _Priya_ replied on ticket _#TKT-2291_ about your _delayed order_. | Help | Yes | **A** |

---

## 5. Inbox UX

| Element | Rule |
| --- | --- |
| Entry | Bell on Home with **unread** count, capped at "9+" |
| Tabs | **All** · **Orders** (orders + returns) · **Offers** (business) · **System** (KYC + money) |
| Row | Category icon · title (1 line) · message (max 2 lines) · relative time · unread dot · inline CTA + expiry chip for **Type A** |
| Read | Tap marks read. Opening the inbox does **not** mark everything read. |
| Order | Type A above Info inside the same day group; newest first otherwise |
| States | Loading (skeletons) · Default · Empty per tab · Error/offline · End of list · Paginating |

| State | Screen |
| --- | --- |
| Default | `notifications.html` |
| Loading | `notifications.html?state=loading` |
| Empty | `notifications.html?state=empty` |
| Offline / error | `notifications.html?state=error` |

---

## 6. Backend

| Need | Detail |
| --- | --- |
| Event layer | Every feature emits `event_name`, `retailer_id`, `entity_type`, `entity_id`, `payload`, `occurred_at` |
| Notification service | Event → template (title, message, category, deep link, priority, channels) → inbox row + push |
| Templates | One per event **per language**; language from `retailers_v2.language` |
| Inbox API | Cursor-paginated feed · unread count · mark read · mark all read |
| Schema gaps | `category`, `read_at`, `priority`, `entity_type`+`entity_id`, `expires_at`, audience model |
| Deep links | One enumerated route registry shared by app, backend and templates |
| De-dupe | Unique on `(retailer_id, event_name, entity_id)` |
| Push | Reuse whatever sends order-placed today — **provider to be identified** |

---

## 7. Analytics

`notification_inbox_opened` · `notification_tab_switched` · `notification_viewed` · `notification_tapped` (category, event, age) · `notification_deeplink_failed` · `notification_marked_read` · `notification_mark_all_read` · `notification_push_received` / `_opened` / `_dismissed` · `notification_empty_viewed`

---

## 8. Acceptance Criteria

| # | Must be true |
| --- | --- |
| 1 | Every event in §4 produces its inbox row end-to-end in staging, with the exact copy shown |
| 2 | Unread badge equals unread count; Mark all read clears it |
| 3 | Every row opens the screen in its **Opens** column; no route in the registry is unhandled |
| 4 | Tapping marks read within one refresh, on both devices of a two-device account |
| 5 | Each tab filters correctly and has its own empty state |
| 6 | 200+ items paginate with no duplicates or gaps |
| 7 | A push tapped from a cold start lands on the target screen, not Home |
| 8 | A repeated event creates no second row |
| 9 | An expired Type A item renders as Expired and opens a read-only view |
| 10 | Copy renders in the retailer's language for every template |
| 11 | Offline shows the cached feed; mark-read syncs on reconnect |

---

## 9. Open Decisions

| # | Decision | Owner |
| --- | --- | --- |
| 1 | Inbox store — `partner_notifications` (needs columns) / new table / the live CRM stack | Tech |
| 2 | Broadcasts — fan-out rows or an audience row resolved at read time | Tech |
| 3 | Which push provider sends order-placed today | Tech |
| 4 | Retention / auto-archive window | Business |
| 5 | Quiet hours and per-retailer frequency caps | Business |
| 6 | Who authors and approves marketing/scheme notifications | Operations |
| 7 | Per-category opt-out in Settings (**NH** for Phase 2) | Product |

## 10. Out of Scope
In-app chat · WhatsApp/SMS campaign management · rich media in notifications · a marketing scheduling UI inside the app.

---

# FEATURE 4 — Return Request Flow

## 1. Status
**Enhance** — the KKD-parity flow is already designed inside `order-details.html`; the backend and tracking are missing.

## 2. Objective
Let a retailer raise a return or replacement for a specific product in a delivered order, with evidence, and then track it to refund or replacement — without a phone call to RLM.

## 3. Current State
- **Partner App:** `order-details.html` already contains a **KKD-parity return & refund flow** (the code is explicitly labelled so): T&C modal with a consent checkbox → return/replace segmented choice → product select with a **return-quantity stepper capped at the ordered quantity** → reason dropdown (Damaged / leaking on arrival · Wrong product delivered · Not as described · Missing item in package · Quality issue · Other) → description → photo/video upload with preview → success toast → **return status timeline** opened from the product row's "Return requested · Tap to view return details" strip.
- `orders.html` exposes a **Return** CTA per order (→ `order-details.html?return=1`) alongside "Rate products".
- A separate, older `return-request.html` screen also exists (single product, reason radio list, Replacement/Refund tiles, up to 5 photos). **It is superseded by the in-`order-details` flow — the duplicate should be retired to avoid two return UIs.**
- **KKD App (reference implementation):** same structure, plus (a) a **7-day return window gate** — the return CTA auto-hides once the window from delivery expires, while "Need help" stays available; (b) an **auto-attached unboxing video** as pre-attached proof; (c) `refund-status.html` — a refund timeline (Issue reported → Refund approved → Initiated to your bank → Credited by date, "3-5 business days", refund-to line, UTR note); (d) a returns policy document at `policy.html?doc=returns`.
- **Backend:** no return/refund/complaint table appears in either the CRM Mongo or Sales-CRM schema vault. Whatever serves KKD returns is the candidate service to reuse — **it must be identified before estimation.**

## 4. Problem / Gap
1. No return backend wired to the Partner App; the designed flow submits nothing.
2. **Two competing return UIs** in the prototype (`return-request.html` vs the flow inside `order-details.html`).
3. Return **eligibility rules are not encoded** — window length, which products are non-returnable, whether partial quantities are allowed, whether opened packs qualify.
4. No **return tracking surface outside order details** — there is no "My Returns" list, so a retailer with returns across three orders must remember which orders.
5. Refund destination logic is undefined for the Partner App (KKD refunds to original payment source; Partner App has Wallet, Coins and Credit in play).

## 5. Proposed Solution
**Adopt the KKD flow as-is and reuse the KKD return service.** Do not build a second return system.

Partner-App-specific additions on top of KKD parity:
- **Multi-product, single request (MH).** A Partner App order is a B2B order with many SKUs; the form must allow selecting several products in one request, each with its own return quantity and reason.
- **Returns list (MH).** A "My Returns" entry from Orders (tab or filter chip) showing every request and its status — the KKD single-order timeline is not enough for a retailer with many orders.
- **Resolution choice** — Replacement or Refund, as already designed; refund destination follows the business rule (below), not user choice, unless Business says otherwise.
- **Window gate identical to KKD** — the Return CTA disappears after the window while Need help stays. Window length for the Partner App is an **Open Decision**.
- **Evidence rules** — photos mandatory for Damaged / Wrong product / Quality issue; optional for Missing item (where a packing-list check matters more); video optional. Confirmed against the KKD pattern; final matrix is an **Open Decision — Business**.

## 6. User Flow
```
Orders → Order (Delivered) → Return
→ Returns T&C (consent checkbox) → Proceed
→ Return or Replace (segmented) → Select product(s) → Set return qty (capped at ordered qty)
→ Select reason → Add description → Upload photos/video
→ Review → Submit
→ Request submitted (request id) → Status: Requested
→ [Ops] Approved / Rejected (reason) → Pickup scheduled → Picked up → QC
→ Replacement dispatched  OR  Refund initiated → Refund completed
→ Tracked from: Order details product row · My Returns list · Notification deep link
```

## 7. Screen-by-Screen UX

**S1 · Order details — Return entry** (existing)
- *Purpose:* start a return in the context of the order.
- *Key UI:* sticky footer Return (outline) + Reorder (primary); per-product "Return requested · Tap to view return details" strip once a request exists.
- *States:* Eligible (CTA visible) · Window expired (CTA hidden, Need help visible) · Request in progress (strip shown) · Not delivered (no CTA).

**S2 · Returns T&C modal** (existing)
- *Purpose:* set expectations and capture consent before the form.
- *Key UI:* window statement, policy link (`policy.html?doc=returns`), "I have read and agree…" checkbox, "Proceed to Return & Refund".
- *States:* Default · Checkbox unchecked (CTA disabled) · Policy opened.

**S3 · Return / replace form** (existing — extended to multi-product)
- *Purpose:* capture what, how much, why and the evidence.
- *Key UI:* Return ⇄ Replace segmented control; order-id chip; product rows with checkbox + quantity stepper (capped); reason dropdown per product; description; media uploader with thumbnails and remove.
- *Primary CTA:* "Submit request". *Secondary:* "Read returns & refund policy".
- *States:* Default · Nothing selected (CTA disabled) · Evidence required but missing (inline) · Uploading (per-thumbnail progress) · Upload failed (retry per file) · Submitting · Submitted · Duplicate blocked.

**S4 · Success confirmation** (existing)
- *Purpose:* confirm and set the next expectation.
- *Key UI:* calm app-native confirmation (per the design system — **not** a coin celebration), request id, expected decision time, CTA "Track return" / "Done".

**S5 · Return details timeline** (existing)
- *Purpose:* single source of truth for one request.
- *Key UI:* status stepper (Requested → Approved → Pickup → QC → Refund/Replacement → Completed), per-product list with quantities, submitted evidence, rejection reason when rejected, refund amount + destination + expected date when refunding, help entry.
- *States:* Requested · Approved · Rejected (reason + support CTA) · Pickup scheduled · Picked up · QC in progress · Replacement dispatched · Refund initiated · Refund completed · Cancelled by user · Expired.

**S6 · My Returns list** (**new, MH**)
- *Purpose:* find any return without remembering the order.
- *Key UI:* rows — product thumbnail(s), order id, request id, status chip, date, amount.
- *Primary CTA:* row → S5. *States:* Loading · Empty ("No returns yet") · Default · Error.

## 8. States
Default · Loading · Empty (no returns) · Error (submit/upload failure) · Success (submitted) · Pending (awaiting approval) · Approved · Rejected · Failure (pickup failed) · Expired (window over) · Disabled (ineligible product/CTA) · Retry (upload/network) · Cancelled

## 9. Business Rules
1. Returns are available only on **Delivered** orders. **MH.**
2. **Return window length for the Partner App — Open Decision — Business confirmation required.** (KKD uses 7 days from delivery; B2B may differ.)
3. **Non-returnable categories — Open Decision — Business confirmation required.** Agri-input specifics (opened packs, cold-chain, batch-coded pesticides, seed) must come from Business, not from the app team.
4. **Partial quantity returns** — the designed stepper implies yes, capped at the ordered quantity. Confirm. **Open Decision.**
5. One open request per (order, product) at a time; a second attempt is blocked with a link to the existing request. **MH.**
6. Already-returned quantity is deducted from the returnable quantity on subsequent requests. **MH.**
7. **Refund destination** (original payment source vs Wallet vs Credit adjustment) and whether **coins used on the order are reversed** — **Open Decision — Accounts + Business confirmation required.**
8. Whether the retailer may **cancel** a submitted request before pickup — recommended yes until "Picked up". **Open Decision.**
9. Who approves — RLM, Support or automated rules — **Open Decision — Operations confirmation required.**

## 10. Backend / System Requirements
- **Reuse the KKD return service** — identify it first (it is not in the inspected schema vault) and confirm whether it is multi-tenant enough to serve Partner App orders from `orders_v2`.
- Required capabilities: create request (multi-product), eligibility check, media upload + storage, status transitions with actor + timestamp, rejection reason, pickup/AWB linkage, refund initiation with UTR, and a request-to-order/product linkage.
- **Order linkage:** `orders_v2.order_status` / `order_status_map[]` provide delivery date and status — the eligibility window must be computed from the delivered timestamp in `order_status_map[]`, not from order date.
- **Events:** `return.requested`, `return.approved`, `return.rejected`, `return.pickup_scheduled`, `return.picked_up`, `return.qc_done`, `replacement.dispatched`, `refund.initiated`, `refund.completed`, `return.cancelled` → all consumed by Feature 3.
- **Ops console** — an RLM/Support-side approval queue must exist. If KKD has one, reuse; if not, that is additional scope. **Open Decision.**

## 11. Notifications
Return request created · Return approved · Return rejected (with reason) · Pickup scheduled / rescheduled · Picked up · Replacement dispatched (with tracking) · Refund initiated · Refund completed · Additional information required.

## 12. Analytics
`return_cta_viewed` (order_id, eligible: true/false) · `return_tnc_opened` / `_accepted` · `return_form_started` · `return_product_selected` (count) · `return_reason_selected` (reason) · `return_media_uploaded` (count, type) · `return_submitted` (products, qty, resolution) · `return_submit_failed` (reason) · `return_status_viewed` (status) · `return_cancelled_by_user` · `returns_list_viewed` · `return_window_expired_view`

## 13. Edge Cases
- Return raised on the last day of the window while the request lands after midnight server-side.
- Order partially delivered — only delivered lines are returnable.
- Product replaced once already; a second issue on the replacement unit.
- Quantity returned exceeds the remaining returnable quantity after an earlier partial return.
- Media upload succeeds on the client but fails server-side → request must not be created without its evidence.
- Retailer uploads a 40 MB video on 2G.
- Order cancelled or refunded through another channel while the return is open.
- Duplicate submit via double-tap.
- Pickup attempted but the shop is closed (pickup failed state).
- Refund fails at the payment gateway (bounced UTR).
- Retailer deletes the app between request and pickup.
- Return on an order whose SKU has since been delisted.

## 14. Dependencies
**Partner App** Orders/Order details · **KKD return service** (to be identified) · **Dispatch / 3PL** (pickup, AWB) · **Accounts** (refunds, credit notes, coin reversal) · **RLM / Support** (approval, rejection, disputes) · **Sales Operation Portal** (if the approval queue lives there) · **Notification service** (F3)

## 15. Acceptance Criteria
1. The Return CTA appears only on delivered orders and disappears exactly when the configured window ends; Need help remains.
2. The return-quantity stepper cannot exceed the ordered quantity minus any already-returned quantity.
3. Reasons requiring evidence block submission until at least one photo is attached, with an inline message.
4. A multi-product request creates one request carrying all selected lines with their own quantities and reasons.
5. Submission yields a request id displayed on the success screen and visible in My Returns within one refresh.
6. A second request for the same (order, product) while one is open is blocked and links to the existing request.
7. Every status transition made by Ops appears on the timeline and produces the matching notification.
8. Rejection shows the Ops-supplied reason verbatim plus a support CTA.
9. Refund states show amount, destination and expected date; completion shows the reference/UTR where supplied.
10. Failed media upload can be retried per file without losing form input.
11. Non-returnable products show a disabled row with a one-line reason rather than being silently absent.
12. `return-request.html` is retired; there is exactly one return UI in the app.

## 16. Out of Scope
Self-serve return-label printing · doorstep QC by the retailer · partial-quantity refunds calculated at a different unit price than charged · warranty claims · return of free/scheme items as standalone requests (**Open Decision** whether these are even returnable).

## 17. Open Decisions
1. Which service backs KKD returns, and can the Partner App reuse it as-is?
2. Return window length for B2B orders.
3. Non-returnable product/category list — who owns and maintains it?
4. Refund destination policy (source / Wallet / Credit note) and coin reversal.
5. Approval model — manual (who) or rule-based?
6. Can a retailer cancel a request, and until which state?
7. Do free / scheme / combo items follow the parent line's return?
8. Is an Ops approval console already available, or is it net-new scope?

---

# FEATURE 5 — Refer & Earn

## 1. Status
**Enhance** — a static screen exists; there is no referral engine.

## 2. Objective
Turn referral from a poster into a working acquisition channel by making the reward condition, progress and payout completely visible — so a retailer knows exactly what has to happen for their ₹ to arrive.

## 3. Current State
- `refer.html` is designed and static: hero "Refer & Earn ₹500", a three-step "How It Works" (Share your code → Friend signs up & completes Verification → Both earn ₹500 once the friend places a first order of ₹2,000+), a referral code card (`MAH8234`) with Copy & Share plus WhatsApp / SMS / Link buttons, an earnings strip (8 Invited · 5 Joined · ₹2,500 Earned) and a Recent Referrals list with per-row status ("✓ Joined • Order placed +₹500", "⏳ Verification pending").
- `retailers_v2` carries a **`referral_code`** field — so a code concept already exists on the master record.
- Nothing is wired: no attribution, no status transitions, no reward ledger, no expiry.

## 4. Problem / Gap
1. **No attribution mechanism.** There is no defined way a new retailer's signup is tied to a referrer — no referral link parameter handling, no code entry field documented in onboarding, no RLM-side capture.
2. **Amounts and conditions are hard-coded copy**, not configured business rules. "₹500" and "₹2,000+ first order" exist only as prototype text and must be confirmed.
3. **The status vocabulary is too thin.** "Joined" and "Verification pending" do not tell a retailer *what is left to do*.
4. **No reward ledger.** Whether a reward lands in Wallet, as Coins, or as a credit note is undefined — and the Partner App already has all three concepts, so the choice matters.
5. **No fraud controls.** Self-referral, circular referrals and fake shops are unaddressed.

## 5. Proposed Solution

**A transparent, staged referral with explicit statuses.**

**Referral status machine (MH):**

| Status | Meaning | What the referrer sees |
| --- | --- | --- |
| `invited` | Code shared, nobody signed up yet | "Invite sent — not joined yet" |
| `signed_up` | Referred retailer created an account with the code attached | "Joined — KYC pending" |
| `kyc_pending` | Onboarding started, documents incomplete | "Waiting for their KYC — 1 of 2 steps done" |
| `kyc_verified` | Referred retailer is verified | "Verified — waiting for first order" |
| `qualifying_order_placed` | First order placed, meeting the threshold | "First order placed — reward after delivery" |
| `qualified` | Order delivered / return window passed | "Reward unlocked" |
| `rewarded` | Reward credited | "₹500 credited on 12 Sep" |
| `expired` | Referral validity lapsed | "Invite expired" |
| `rejected` | Fraud / duplicate / ineligible | "Not eligible — {reason}" |

**Progress made explicit (MH).** Each pending referral row shows a 3-dot progress (Joined → Verified → First order) with the exact next action, e.g. *"Ramesh needs to complete KYC. Remind →"* with a WhatsApp remind CTA. This is the single biggest change from the current screen.

**Both-sided clarity (MH).** The referred retailer must see their own side: "You joined with Suresh's code — complete KYC and your first order of ₹X to get ₹Y." Placed on the referred user's home/KYC banner, not hidden in Refer & Earn.

**Configurable, not hard-coded (MH).** Reward amounts, the qualifying-order threshold, validity and reward type must come from configuration so Business can change them without an app release.

**Reward type** — Wallet credit, Coins, or credit note: **Open Decision — Business + Accounts**. The prototype implies ₹ (Wallet). The loyalty model already defines coins at 1 coin = ₹1, so either is expressible.

## 6. User Flow
```
Profile / Home → Refer & Earn
→ Understand benefit (How it works, 3 steps)
→ Share code / link (WhatsApp · SMS · Copy link)
→ Referred retailer installs → signup with code attached (auto from link, or typed)
→ Referred completes KYC → status: kyc_verified
→ Referred places first qualifying order → status: qualifying_order_placed
→ Order delivered + validation window → status: qualified
→ Reward generated → credited to referrer and referred → status: rewarded
→ Both notified → visible in Refer & Earn + Wallet/Coins statement
```

## 7. Screen-by-Screen UX

**S1 · Refer & Earn** (`refer.html`, restructured content, same visual language)
- *Purpose:* explain, share, and show progress honestly.
- *Key UI:* hero with the **configured** reward; "How it works" 3 steps with the exact qualifying condition; code card with Copy & Share + channel buttons; earnings strip (Invited / Joined / Earned) with **Pending amount** added; "Your referrals" list with per-row progress and a Remind CTA; "Terms" link.
- *Primary CTA:* "Copy & Share". *Secondary:* WhatsApp / SMS / Link; "How rewards work".
- *States:* Loading · Default · Empty (no referrals — show a single strong share CTA, not a table with zeros) · Error · Program paused (banner: "Referral rewards are paused" — needed, because the program will be switched off at some point).

**S2 · Referral detail sheet** (**new, small, MH**)
- *Purpose:* answer "why hasn't my ₹500 come?"
- *Key UI:* referred name/shop (masked per privacy rules), status stepper, date of each step, expected reward and condition, Remind CTA, "Something wrong? Contact support".
- *States:* Each status above · Rejected (reason shown).

**S3 · Referred-user banner** (on the referred retailer's Home/KYC — extension, not a new screen)
- *Purpose:* make the referred side's condition visible.
- *Key UI:* "You were invited by {shop}. Complete KYC + first order of ₹X to earn ₹Y." with progress and CTA to the pending step.
- *States:* Active · Completed · Expired.

**S4 · Reward credited confirmation**
- *Purpose:* close the loop.
- *Key UI:* amount, source ("Referral reward — Ramesh Agro Centre"), where it landed (Wallet/Coins), CTA "View Wallet".

## 8. States
Default · Loading · Empty (no referrals) · Error · Success (reward credited) · Pending (awaiting referred action) · Expired (invite lapsed) · Rejected (ineligible) · Disabled (share while program paused) · Retry

## 9. Business Rules
1. Reward amount for referrer and referred — **Open Decision — Business confirmation required** (₹500/₹500 in the prototype is illustrative only).
2. Qualifying condition — **Open Decision** (prototype says first order ≥ ₹2,000 after verification).
3. Is reward payout **after delivery** or **after order placement**? Recommended after delivery (protects against cancel-for-reward). **Open Decision.**
4. Referral validity period — **Open Decision**.
5. Maximum referrals rewarded per retailer, per month or lifetime — **Open Decision**.
6. Eligibility of the referrer (must be KYC-verified? VIP tier gated?) — **Open Decision**.
7. Reward instrument (Wallet ₹ / Coins / credit note) and whether it is withdrawable — **Open Decision — Accounts**.
8. Fraud rules: same shop, same phone, same GST/PAN, same address or same device between referrer and referred must block. **MH — thresholds are an Open Decision.**
9. Whether an RLM-sourced retailer can be claimed as a referral (attribution conflict with RLM's own acquisition credit) — **Open Decision — Operations confirmation required. This one is politically important and should be settled early.**

## 10. Backend / System Requirements
- **Referral engine:** code issue + uniqueness on `retailers_v2.referral_code`, attribution capture at signup (link parameter and manual code entry), status machine, validation window, reward generation, ledger entry, idempotent payout.
- **Deferred deep link** — for attribution to survive a Play Store install, the share link must carry the code through installation. **This is a technical capability decision — Open Decision.** Without it, attribution depends entirely on manual code entry during onboarding, which changes the onboarding screen requirement.
- **Onboarding change (dependency):** a "Have a referral code?" field must exist in the signup flow if deferred deep links are not used.
- **Reward ledger:** reuses the existing Wallet/Coins ledger from Phase 1 — do **not** create a parallel money system.
- **Events:** `referral.shared`, `referral.signup_attributed`, `referral.kyc_completed`, `referral.order_qualified`, `referral.rewarded`, `referral.expired`, `referral.rejected`.
- **Admin:** the RLM/Sales Ops side needs a view of referrals for dispute handling and fraud review.

## 11. Notifications
Referrer: someone joined using your code · their KYC is verified · they placed their first order · your reward is credited · your invite expired · referral rejected (reason).
Referred: welcome — here is what you must complete · your reward is credited.

## 12. Analytics
`refer_screen_viewed` · `refer_code_copied` · `refer_shared` (channel) · `refer_link_opened` (by referred) · `refer_signup_attributed` (source: link | manual_code) · `refer_status_viewed` (status) · `refer_remind_sent` (channel) · `refer_reward_credited` (amount, type) · `refer_reward_rejected` (reason) · funnel: shared → installed → signed up → verified → first order → rewarded

## 13. Edge Cases
- Referred retailer already exists in the CRM (known lead) — not a new acquisition.
- Referred retailer signs up without the code, then asks for it to be applied later.
- Two referrers claim the same retailer.
- Referrer's account is later blocked or fails KYC after rewards were paid.
- Referred retailer's qualifying order is cancelled or fully returned after the reward is credited.
- Reward triggers while the program is paused mid-cycle.
- Share link opened on desktop.
- Code shared in a WhatsApp group and used by twenty retailers in one day.
- Referred retailer is in a non-serviceable pincode and cannot order.
- Reward crosses a tier/threshold that changes the retailer's VIP level.

## 14. Dependencies
**Partner App** onboarding + Wallet/Coins (Phase 1) · **RLM** (attribution conflict, field-sourced retailers) · **RLM Admin / Sales Operation Portal** (referral oversight, fraud review) · **Accounts** (payout, reversal) · **Marketing** (program terms, amounts) · **Deep-link provider** (if used)

## 15. Acceptance Criteria
1. Each retailer has exactly one referral code, visible and copyable, and it matches `retailers_v2.referral_code`.
2. A signup carrying the code is attributed to the referrer within one refresh and appears in the referrer's list as `signed_up`.
3. Every status in §5 is reachable in staging and renders with its correct label, date and next action.
4. Reward amounts and the qualifying threshold shown in the UI come from configuration — changing config changes the screen without an app release.
5. Reward is credited exactly once per qualified referral; replaying the qualifying event creates no second credit.
6. The credited reward appears in the Wallet/Coins statement with a referral-attributed description.
7. Self-referral (same phone / same shop / same device per the configured rules) is blocked at signup with a clear message.
8. A pending referral row shows what the referred retailer still has to do, and the Remind CTA opens WhatsApp with prefilled text.
9. The referred retailer sees their own condition and progress without opening Refer & Earn.
10. When the program is paused, sharing is disabled with an explanatory banner and no rewards are generated.
11. Expired invites move to `expired` and stop counting toward pending earnings.

## 16. Out of Scope
Multi-level / tiered referral chains · referral leaderboards and contests (Leaderboard already exists for sales; mixing them is out) · referral of farmers (this is retailer→retailer) · cash withdrawal mechanics.

## 17. Open Decisions
1. Reward amount, instrument and qualifying condition.
2. Payout trigger — order placed vs delivered vs return-window closed.
3. Referral validity and per-retailer caps.
4. Deferred deep link (vendor/approach) or manual code entry only?
5. Attribution conflict rules with RLM-sourced retailers — **needs Operations sign-off**.
6. Fraud rule thresholds and who reviews flagged referrals.
7. Reversal policy if the qualifying order is cancelled or returned.
8. Does the referred retailer's reward require their own KYC completion first?

---

# FEATURE 6 — Testimonial Capture

## 1. Status
**Enhance** — a testimonial screen exists, but it captures the wrong object.

## 2. Objective
Collect **product-level** ratings and testimonials from retailers who actually received the product, so PDP social proof is real, attributable and usable by marketing.

## 3. Current State
- **Partner App `testimonial.html`** is a well-built **story-level** feature: hero "Tell your story. Earn coins.", earn 250 coins, a 3-step how-it-works (Record 30–60 s → Submit → Review in 48 hrs → 250 auto-credited), an example testimonial with a video player, approval guidelines (shop interior visible, mention product + farmer feedback, any language, no competitor names), a written-story field with optional video, and a **My submissions** list with Approved / Pending / Rejected states and rejection reasons ("audio not clear"). `testimonial-success.html` closes the loop.
- **Partner App `order-details.html`** *also* already has **product-level review panels** — an expandable "Rate this product" panel per product with Submit Review, a thank-you state and an Edit review link. `orders.html` shows a "Rate products" CTA and a "Rated 4.5" state.
- **KKD (reference):** in `order-details.html`, each delivered product row carries **"Rate this product · +10 on review"** with the honest caption "Optional. Helps other farmers — no extra coins." and a Submit review → "Review submitted" state. This is exactly the pattern the requirement asks for.

## 4. Problem / Gap
1. **Wrong anchor.** The flagship testimonial screen is anchored to the retailer's *story*, not to a **product in a delivered order**. The requirement is explicit: reviews must be captured against the specific product delivered.
2. **Two review systems in one app.** Product review panels in order details and a story testimonial feature elsewhere, with different reward promises (coins 250 vs none vs KKD's +10) and different moderation implications.
3. **No eligibility logic.** Nothing restricts reviewing to products actually delivered to that retailer, which is the entire basis of a trustworthy review.
4. **No destination defined.** Where an approved review appears (PDP reviews section — which exists in Phase 1) and how moderation reaches it is unspecified.
5. **Reward inconsistency.** 250 coins for a video testimonial vs an unspecified reward for a product rating needs a single, stated policy.

## 5. Proposed Solution

**Make the delivered order the only entry point for product reviews**, and keep the story testimonial as a separate, clearly-labelled marketing programme.

- **Product review (MH)** — anchored to `(order_id, product_id)`, opened from: order delivered notification · order details product row (already designed) · Orders list "Rate products" · a home prompt after delivery. Contains: star rating (required), short text (optional), photo/video (optional), submit. **No more than that** — a retailer rating five SKUs will not write five essays.
- **Story testimonial (keep, relabel)** — the existing `testimonial.html` becomes "Share your story" under Profile/Community, explicitly a **marketing programme with a coin reward and 48 h moderation**. It is not the product review system.
- **Multi-product order handling (MH)** — after delivery, show a single "Rate {n} products" entry that walks the eligible products in one sheet: product → rating → optional text → Next. Skip is always available per product.
- **PDP destination (MH)** — approved reviews surface in the existing PDP Reviews section with retailer name/shop and a "Verified purchase" marker. PDP already has a reviews toggle from Phase 1; this feeds it.

## 6. User Flow
```
Order Delivered (notification / order details / orders list)
→ "Rate products" → Eligible product list (delivered lines only)
→ Select product → Star rating (required) → Testimonial text (optional)
→ Add photo/video (optional) → Submit
→ Submitted (thanks + reward statement if any) → Next product / Done
→ Moderation (approve / reject with reason) → Approved review appears on PDP
→ Retailer can Edit review within the edit window
```

## 7. Screen-by-Screen UX

**S1 · Review entry points** (existing surfaces, no new screens)
- Order details product row: "Rate this product" expandable panel — **already designed, keep**.
- Orders list: "Rate products" CTA with a "Rated 4.5" completed state — **already designed, keep**.
- Post-delivery notification deep link → S2.

**S2 · Eligible products sheet** (small, **new**)
- *Purpose:* show what can be reviewed from this order.
- *Key UI:* order chip, product rows (thumbnail, name, pack, delivered qty) with a per-row state — Rate / Rated ★4 / Not eligible (reason).
- *Primary CTA:* row → S3. *Secondary:* "Skip for now".
- *States:* Loading · Default · All rated ("You have rated everything in this order") · None eligible · Error.

**S3 · Rate a product**
- *Purpose:* capture the rating with the least friction.
- *Key UI:* product header, 5-star control (required), one-line label per star value, optional text field with placeholder guidance ("How did it work on your farmers' crop?"), optional media, character counter, submit.
- *Primary CTA:* "Submit review". *Secondary:* "Skip".
- *States:* Default · Rating selected (text/media reveal) · Uploading · Submitting · Submitted · Error · Already reviewed (shows existing review + Edit) · Edit window closed (read-only).

**S4 · Submitted confirmation**
- *Purpose:* close the loop honestly.
- *Key UI:* thank-you, what happens next (moderation, where it appears), reward statement only if a reward actually applies, CTA "Rate next product" / "Done".

**S5 · My reviews** (**NH**)
- List of the retailer's reviews with status (Published / Under review / Rejected + reason) and Edit access. The existing "My submissions" pattern in `testimonial.html` is the template.

## 8. States
Default · Loading · Empty (nothing to review) · Error (submit/upload) · Success (submitted) · Pending (under moderation) · Rejected (with reason) · Disabled (skip-only, ineligible) · Expired (review window closed) · Already-reviewed · Retry

## 9. Business Rules
1. Reviews are allowed **only on products in a Delivered order** for that retailer. **MH.**
2. One review per `(retailer, order, product)`. A repeat purchase of the same SKU in a new order creates a new, separate review opportunity. **Confirm — Open Decision.**
3. Review window after delivery — **Open Decision — Business confirmation required.**
4. Edit window after submission — **Open Decision** (KKD/Partner prototypes both show an Edit link; duration unstated).
5. Rating is required; text and media are optional. **MH.**
6. Reward policy: the story programme promises 250 coins; the KKD product review says "+10 on review" with "no extra coins" copy in a second place. **A single reward policy must be stated — Open Decision — Business confirmation required.**
7. Moderation is required before publication (agri claims carry regulatory risk — product efficacy statements cannot go live unreviewed). **MH.**
8. Rejected reviews must show a reason and allow one resubmission. **MH.**
9. Reviews on returned products — **Open Decision** (recommended: allow, but flag for moderation).

## 10. Backend / System Requirements
- **Reuse the KKD review service if it exists** (KKD PDP shows reviews and order details submits them) — identify before building. The KKD admin already contains `testimonials-manager` and `testimonials` screens, which suggests a moderation console exists to reuse.
- Required: review create/update, eligibility check against delivered order lines, media storage, moderation status + reason, publication to PDP, aggregate rating recomputation per product.
- **Products:** `products_v2` is the catalog of record; the review must key to the same product identity the PDP uses.
- **Events:** `review.submitted`, `review.approved`, `review.rejected`, `review.edited`, `review.published`.
- **Moderation console** — RLM Admin or Marketing; owner is an **Open Decision**.

## 11. Notifications
Order delivered → "Rate the products you received" (the review prompt) · Review approved / published · Review rejected with reason · Reward credited (if the reward policy grants one) · Reminder for unrated delivered products (**NH**, frequency-capped).

## 12. Analytics
`review_prompt_shown` (source: notification | order_details | orders_list | home) · `review_sheet_opened` (order_id, eligible_count) · `review_started` (product_id) · `review_rating_selected` (stars) · `review_text_added` (length) · `review_media_added` (type) · `review_submitted` (product_id, stars, has_text, has_media) · `review_skipped` (product_id) · `review_edit_started` / `_saved` · `review_moderation_result` (approved | rejected, reason) · funnel: delivered → prompted → opened → rated → submitted

## 13. Edge Cases
- Order delivered but the retailer never opened the app for 30 days — is the review window still open?
- Product delisted between delivery and review.
- Partially returned quantity — reviewing a product that was partly returned.
- Retailer rates 12 SKUs in one order (bulk B2B order) — the sheet must not become a chore; cap the prompt, allow the rest from order details.
- Review text in a regional language or script — moderation capability must handle it.
- Media upload fails after the rating is submitted (rating should persist; media retried).
- Same product delivered in two different orders — two independent review opportunities.
- Review submitted while the order is subsequently cancelled/reversed.
- Abusive or competitor-naming content (the existing testimonial guidelines already state the rules — apply them to product reviews too).
- Retailer edits a published review — does it return to moderation? (Recommended: yes.)

## 14. Dependencies
**Partner App** Orders / Order details / PDP reviews (Phase 1) · **KKD review + moderation service** (to be identified) · **Marketing** (moderation, publication, content guidelines) · **Loyalty/Coins** (if a reward applies) · **Notification service** (F3)

## 15. Acceptance Criteria
1. A review can be started only from a delivered order; no other path exposes a rating control.
2. Only delivered product lines appear in the eligible list; undelivered/cancelled lines do not.
3. Star rating is mandatory — submit is disabled without it; text and media are optional.
4. Submitting shows a confirmation and flips the product row to a rated state everywhere it appears (order details and orders list) within one refresh.
5. A second review attempt for the same (order, product) opens the existing review in edit or read-only state, never a blank form.
6. An approved review appears in that product's PDP reviews section with a verified-purchase marker.
7. A rejected review shows the moderator's reason and allows exactly one resubmission.
8. The reward statement shown at submission matches what is actually credited (or no reward is promised).
9. Multi-product orders can be rated in one pass with Skip available at every step, and partial completion is preserved.
10. Media upload failure does not discard the rating.
11. The story-testimonial programme is visually and textually distinct from product reviews; no user can confuse the two rewards.

## 16. Out of Scope
Farmer-facing reviews (KKD's own reviews) · review replies / Q&A threads on PDP · incentivised review campaigns · review-based ranking changes in search/catalog · sentiment analysis.

## 17. Open Decisions
1. Does a KKD review + moderation service exist that the Partner App can reuse?
2. Review window and edit window durations.
3. Single reward policy across product reviews and story testimonials.
4. Who moderates — Marketing, RLM Admin, or Support?
5. Are reviews allowed on returned or partially-returned products?
6. Does editing a published review send it back to moderation?
7. Are retailer reviews shown to farmers in KKD, or only within the Partner App PDP? (A privacy and positioning question.)

---

# FEATURE 7 — Sales Cart Request (B2B Bulk via Phone)

## 1. Status
**Pending** — the retailer-side screen is designed; **the RLM/Agent-side composer does not exist at all**, and that is the larger half of the feature.

## 2. Objective
Let an RLM/Agent build a cart for a retailer during a phone conversation and push it into the retailer's app for one-tap review and acceptance — converting a call into a checkout instead of a follow-up.

## 3. Current State
- **Partner App `sales-cart-request.html` is designed and detailed:** header "Cart Request · From your Katyayani sales advisor" with an **"Expires in 22h"** chip; advisor card (name, "Advisor", ID `KAT-SA-1184 · Indore Zone`, Call and WhatsApp buttons); an advisor message in Hinglish; a **Proposed Cart** of 5 line items each showing pack size, case size or scheme ("1 case = 20 units", "Scheme: 10+1 free"), quantity, **margin %**, partner price and struck-through MRP; a Summary (Subtotal, MRP saving, Advisor bonus, Delivery FREE, **You pay**, **Your profit**); a trust line "Safe · Verified advisor. You can edit quantities in cart after accepting. **Accepting does not place the order**"; and two CTAs — **Decline** and **Accept & Open Cart**.
- `notifications.html` already contains the matching inbox item: *"Cart request from Rajesh (Advisor) · 5 items · ₹20,314 · Tap to review & accept · Expires in 22h"*.
- **Backend:** `partner_cart` exists (Supabase) with **0 rows** and a decisive constraint — cart lines reference **`quotation_items.id`, not `products.id`**, i.e. that design only allows carting items that were already quoted, and `UNIQUE (partner_id, quotation_item_id)` forces upsert-on-repeat. Whether the live Partner App cart follows this model at all is unknown.
- **RLM side:** nothing. No composer screen, no request table, no status model found.

## 4. Problem / Gap
1. **The originating system is missing.** Without an RLM/Agent composer (retailer search, catalog with the retailer's applicable pricing, quantity entry, submit), there is no feature — only a screen waiting for data.
2. **Cart-merge semantics are undefined.** What happens to the retailer's existing cart on Accept is the single most consequential unanswered question in this feature.
3. **Price and stock drift.** A request built at 11:00 and accepted at 09:00 the next day can carry a stale price, a lapsed scheme or an out-of-stock SKU.
4. **`partner_cart`'s quotation-only model** may conflict with a request built from the live catalog. This must be resolved before implementation.
5. **No authority model.** Which agent can create a request for which retailer, and whether special pricing/"Advisor bonus" needs approval, is undefined — and the prototype already shows a discount line.

## 5. Proposed Solution

**Build the request as a first-class object with its own lifecycle, separate from the cart** — the cart is only what happens on acceptance.

**Request lifecycle (MH):** `draft` (agent composing) → `sent` → `viewed` → `accepted` / `partially_accepted` / `declined` / `expired` / `cancelled_by_agent` / `superseded`.

**Cart interaction — the recommended contract (needs sign-off):**
- Accept **merges** the request into the existing cart. Same SKU present → **quantities are summed**, and the merge screen says so explicitly before it happens.
- Accepting does **not** place an order (the prototype already promises this — keep it).
- Prices in the request are **honoured as a price snapshot** until the request expires; on acceptance, any line whose price or scheme has changed is shown in a "what changed" strip before the cart opens. **Whether the snapshot price is honoured after expiry is an Open Decision — Business.**
- Out-of-stock lines are moved into a "couldn't add" list on the confirmation instead of silently vanishing.

**Partial acceptance (MH).** The retailer can deselect lines before accepting (B2B reality — they will not take all five SKUs). Accepting a subset marks the request `partially_accepted` and reports back to the agent which lines were dropped, which is valuable sales signal.

**Modify quantities (NH for Phase 2).** The prototype's promise — "You can edit quantities in cart after accepting" — is a simpler, safer answer than in-request editing. Keep that promise; do not build in-request quantity editing in Phase 2.

**RLM/Agent composer (MH, net-new):** retailer search → open retailer context (KYC status, tier, last order, credit) → add products from the catalog at the retailer's applicable price → set quantities → optional message → preview exactly what the retailer will see → send → track status.

## 6. User Flow
```
[RLM/Agent side]
Agent portal → Search retailer → Open retailer → Create cart request
→ Add products (catalog, retailer-applicable price) → Set quantities → Add message
→ Preview → Send → Request status board (sent / viewed / accepted / declined / expired)

[Partner App side]
Push + inbox notification ("Cart request from {agent} · 5 items · ₹X · Expires in 22h")
→ Cart request screen → Review products, quantities, prices, margin, profit
→ [Deselect optional lines] → Accept & Open Cart  OR  Decline (reason)
→ Merge summary ("3 items added · 1 already in cart, quantity updated · 1 out of stock")
→ Cart → Checkout (existing Phase 1 flow)
→ Agent is notified of the outcome
```

## 7. Screen-by-Screen UX

**S1 · Notification / inbox item** (designed)
- *Key UI:* agent name, item count, total, expiry chip, "Tap to review & accept".
- *States:* Unread · Read · Expired (greyed, opens read-only).

**S2 · Cart request detail** (`sales-cart-request.html`, as designed + selection)
- *Purpose:* let the retailer judge the offer on margin and cash, then act.
- *Key UI:* expiry chip with live countdown; advisor card with Call + WhatsApp; message; line items with pack/case/scheme, qty, margin %, price vs MRP, **per-line checkbox (new)**; summary with You pay + Your profit; trust line.
- *Primary CTA:* "Accept & Open Cart". *Secondary:* "Decline".
- *Navigation:* Accept → S3 → Cart; Decline → S4 → Notifications.
- *States:* Loading · Default · Some lines deselected (summary recalculates live) · Price/stock changed since sent (per-line strip) · Expiring soon (< 2 h emphasis) · Expired (CTAs replaced by "This request expired · Ask advisor to resend") · Already accepted (read-only, "Added to cart on 12 Sep") · Declined (read-only) · Error.

**S3 · Merge confirmation** (small sheet, **new, MH**)
- *Purpose:* prevent the cart from changing in ways the retailer did not expect.
- *Key UI:* "3 items added · Chakraveer was already in your cart — quantity updated to 18 · NPK 19-19-19 is out of stock and was not added".
- *Primary CTA:* "Go to Cart". *Secondary:* "Undo" (**NH**).

**S4 · Decline sheet**
- *Purpose:* capture why, for the agent.
- *Key UI:* reason chips (Too much quantity · Price high · Already stocked · Not the season · Will order later · Other) + optional note.
- *Primary CTA:* "Send decline". *States:* Default · Sent.

**S5 · Agent composer** (RLM side, **new, MH** — outside the Partner App)
- *Purpose:* build and send the request during the call.
- *Key UI:* retailer search + context header (tier, KYC, credit, last order), product search with applicable price and margin shown, quantity entry with case conversion, running totals, message box, expiry selector, Preview-as-retailer, Send.
- *States:* Draft · Validation error (price/stock/eligibility) · Sent · Viewed · Accepted / Partially accepted / Declined / Expired · Cancelled.

## 8. States
Default · Loading · Empty (no requests) · Error · Success (accepted, merged) · Pending (sent, awaiting retailer) · Viewed · Declined · Expired · Partially accepted · Disabled (CTAs after expiry) · Retry · Superseded (a newer request replaced this one)

## 9. Business Rules
1. A request has an **expiry**; the prototype shows 22 h remaining, implying a 24 h default. **Confirm — Open Decision.**
2. Accepting **does not place an order** — the retailer still checks out. **MH (already promised on screen).**
3. Cart merge policy on duplicate SKU (sum vs replace) — **Open Decision — Business confirmation required.** Recommended: sum, disclosed.
4. Price snapshot honoured until expiry; behaviour after a price change during the window — **Open Decision.**
5. "Advisor bonus" / special discount authority and approval limits — **Open Decision — Business + Sales Ops confirmation required.**
6. Can a request be sent to a retailer whose KYC is not verified (prices are gated for them)? — **Open Decision.**
7. Only one active request per retailer at a time; a new one supersedes the previous. **Recommended — Open Decision.**
8. Whether the agent can cancel a sent request before acceptance. **Recommended yes — Open Decision.**
9. Minimum order value / credit-limit checks applied at accept time or checkout time — **Open Decision — Accounts.**

## 10. Backend / System Requirements
- **Cart request service** (new): create, send, expire, accept (full/partial), decline, cancel; snapshot of price, scheme and margin per line; audit of who created and who accepted.
- **Cart contract:** resolve whether the live Partner App cart is the Supabase `partner_cart` (quotation-scoped, and therefore incompatible with a free-catalog request) or a different store. **This blocks design — Open Decision.**
- **Pricing:** the retailer's applicable price must come from the same pricing service the app uses, so the agent cannot quote a price the app will not honour.
- **Stock:** availability at send time and re-check at accept time.
- **Agent identity:** `agents`/`agent_roster` exist in Sales-CRM; retailer↔agent mapping (territory, `agent_districts` / `agent_pincodes`) should govern who may create a request for whom.
- **Events:** `cart_request.created`, `.sent`, `.viewed`, `.accepted`, `.partially_accepted`, `.declined`, `.expired`, `.cancelled` → Feature 3 and the agent's board.

## 11. Notifications
**Retailer:** new cart request received · expiring in 2 hours (**NH**) · request expired · request cancelled by advisor.
**Agent:** retailer viewed the request · accepted (with the accepted value) · partially accepted (with dropped lines) · declined (with reason) · expired without action.

## 12. Analytics
`cart_request_notification_received` / `_opened` · `cart_request_viewed` (items, value, time_since_sent) · `cart_request_line_deselected` (sku) · `cart_request_accepted` (items, value, accepted_ratio) · `cart_request_declined` (reason) · `cart_request_expired` · `cart_merge_conflict` (sku, resolution) · `cart_request_to_order` (order placed within N hours — the conversion metric that justifies the feature) · agent-side: `composer_opened`, `request_sent` (items, value), `request_outcome`

## 13. Edge Cases
- Retailer is mid-checkout when the request arrives → never mutate a cart during an active checkout; hold the merge and apply it after checkout completes or is abandoned, and say so.
- Cart already contains the same SKU at a different price.
- Price changed or a scheme ended between send and accept.
- SKU went out of stock or was delisted.
- Retailer accepts on two devices simultaneously.
- Agent sends a second request before the first expires.
- Retailer's KYC lapsed between send and accept, re-gating prices.
- Retailer accepts after expiry from a stale screen (server must reject; UI must explain).
- Credit limit exceeded by the merged cart.
- Quantity exceeds case multiples or a per-SKU order cap.
- Agent leaves the organisation while a request is open.
- Retailer declines but then calls the agent and asks for the same cart back.

## 14. Dependencies
**Partner App** cart + checkout + pricing + notifications · **RLM / Sales Operation Portal** (agent composer, agent identity, territory mapping, status board) · **RLM Admin** (discount approval) · **Accounts** (credit limits) · **Catalog/Pricing service** · **Inventory/stock service**

## 15. Acceptance Criteria
1. A request sent from the agent composer reaches the retailer's inbox and push within 60 s and renders every line with pack, quantity, price, margin and the summary totals.
2. The expiry chip counts down live and the request becomes read-only at expiry, on screen and server-side.
3. Accepting adds exactly the selected lines to the cart and shows the merge summary naming each duplicate, updated quantity and unavailable item.
4. Accepting never places an order — the retailer lands in the cart with checkout still required.
5. Deselecting lines recalculates You pay and Your profit before acceptance, and the agent sees which lines were dropped.
6. Declining captures a reason and notifies the agent.
7. A request accepted on one device shows as accepted on the other within one refresh, and a second acceptance is rejected.
8. A price or stock change between send and accept is surfaced per line before the merge — never silently applied.
9. A request arriving during an active checkout does not modify the cart being checked out.
10. The agent's board reflects sent / viewed / accepted / partially accepted / declined / expired accurately.
11. An agent cannot create a request for a retailer outside their mapped territory (if that rule is confirmed).

## 16. Out of Scope
In-request quantity editing by the retailer (**NH**; editing happens in the cart) · agent-initiated order placement on the retailer's behalf · negotiation threads · quotation documents / PDF quotes · payment collection by the agent.

## 17. Open Decisions
1. **What is the Partner App's real cart store**, and is the quotation-scoped `partner_cart` model in play? (Blocks everything else here.)
2. Cart merge policy for duplicate SKUs.
3. Request expiry duration; post-expiry price honouring.
4. Discount / "Advisor bonus" authority and approval workflow.
5. Who builds the agent composer — Sales Operation Portal team or Partner App backend team?
6. Territory rules for which agent may request for which retailer.
7. Can requests go to non-KYC-verified retailers?
8. Are credit-limit and MOV checks applied at accept or at checkout?
9. Is partial acceptance allowed in v1? (Recommended yes.)

---

# FEATURE 8 — Product Catalog Download

## 1. Status
**Pending** — a capability that existed in the previous Partner App and has **no screen and no service** in the new one.

## 2. Objective
Give retailers a shareable, offline product catalog — the artefact they actually use at the counter and in WhatsApp groups — without exposing pricing to anyone not entitled to see it.

## 3. Current State
- **Nothing in the new app.** There is no catalog-download screen in `screens/`, and no entry point in Explore, Categories or Profile.
- The previous Partner App offered catalog download; retailers are known to expect it.
- Related capability that already exists: **Poster Generator** (Phase 1) produces shareable single-product creatives — the same sharing instinct, different artefact.
- Catalog data lives in `products_v2` (CRM Mongo) with technicals, packs and categories; crop/pest mapping exists via `crops_v2`, `crop_problems_v2`, `diseases`.
- Price visibility is already **gated by KYC/verification state in Phase 1** (non-verified retailers see blurred prices and locked ADD) — the catalog must honour exactly the same gate.

## 4. Problem / Gap
1. Feature absent entirely — this is the only Phase 2 item with no design at all.
2. **Price exposure is the core risk.** A PDF is forwardable. A catalog carrying distributor pricing will reach competitors and farmers within hours of its first download.
3. No decision on generation strategy (dynamic vs pre-generated vs cached), file size, or how often it refreshes.
4. No definition of what "the catalog" is — full range (hundreds of SKUs) or a filtered subset.

## 5. Proposed Solution

**Ship a filtered, personalised, watermarked PDF — not a raw price list.**

- **Entry points (MH):** Explore/Categories header action "Download catalog"; Profile → "Product catalog"; and from a category or crop listing as "Download this list" (filtered).
- **Scope choice before download (MH):** the user picks — **Full catalog** · **This category** · **This crop** · **My frequently ordered**. Defaulting to "Full" for a range this size produces a file nobody sends.
- **Price visibility (MH):** three variants driven by the retailer's entitlement, decided server-side, never client-side:
  1. **Verified retailer** → partner price + MRP + margin %.
  2. **Non-verified retailer** → MRP only, with a "Verify your business to see your price" line.
  3. **Share-safe variant** → MRP only, always, regardless of entitlement — offered as an explicit "Catalog for sharing (no partner prices)" option, because retailers *will* forward it.
- **Watermark (MH):** every price-bearing page carries the retailer's shop name, code and generation date. This is the practical deterrent against forwarding, and it makes leaks traceable.
- **Content per product (MH):** image, product name, technical name, pack size(s), category, target crops, target pests/diseases, and a short usage line. **Dosage and application detail is Open Decision — Regulatory**, because printed dosage carries label-compliance obligations.
- **Format:** PDF (**MH**). Excel/CSV price list — **NH and not recommended** for price-bearing content.
- **Generation strategy — a technical decision, flagged as such:** pre-generate the public MRP-only catalog nightly (cheap, cacheable); generate price-bearing personalised variants on demand with a short-lived signed link. Final call is **Open Decision — Tech**.

## 6. User Flow
```
Explore / Categories / Profile → Download catalog
→ Choose scope (Full · Category · Crop · Frequently ordered)
→ Choose version (With my prices · MRP only / shareable)   [only if entitled]
→ Generate → Progress (Preparing your catalog… X%)
→ Ready → Open / Save / Share (WhatsApp)
→ [Failure] Retry · [No entitlement] MRP-only path with a Verify CTA
```

## 7. Screen-by-Screen UX

**S1 · Catalog entry point**
- *Purpose:* make the artefact discoverable where browsing already happens.
- *Key UI:* a row/action "Download product catalog · PDF · updated {date}".

**S2 · Catalog options sheet**
- *Purpose:* pick scope and version in one screen.
- *Key UI:* scope chips; version radio (With my prices / MRP only for sharing) with a plain-language caution on the priced version; estimated size and product count; "Last updated {date}".
- *Primary CTA:* "Download PDF". *Secondary:* "Share MRP catalog".
- *States:* Default · Non-verified (priced option disabled with "Verify your business to unlock your prices" + CTA) · Empty filter (no products) · Generating · Error.

**S3 · Generating / progress**
- *Key UI:* determinate progress where possible, product count, cancel.
- *States:* Queued · Generating · Slow (> 15 s → "Still working, you can keep using the app") · Failed (Retry) · Complete.

**S4 · Ready / result**
- *Key UI:* file name, size, generated timestamp, Open · Save · Share; a one-line reminder that the file carries the shop's name when priced.
- *States:* Ready · Share sheet open · Storage permission denied · Expired link (regenerate).

## 8. States
Default · Loading · Empty (filter yields nothing) · Error (generation/network) · Success (file ready) · Pending (queued) · Disabled (priced version for non-verified) · Expired (signed link lapsed) · Retry

## 9. Business Rules
1. Partner/distributor pricing appears **only** for retailers entitled to see it in-app — the Phase 1 gate is the single source of truth. **MH.**
2. A shareable MRP-only variant must always be available. **MH.**
3. Watermarking of priced catalogs with shop identity. **MH — confirm exact fields with Business.**
4. Catalog refresh cadence and the "last updated" promise — **Open Decision — Business.**
5. Whether out-of-stock or delisted SKUs are included (and marked) — **Open Decision.**
6. Whether dosage/application instructions may be printed — **Open Decision — Regulatory/Agronomy confirmation required.**
7. Download rate limit per retailer per day — **Open Decision — Tech + Business** (abuse and cost control).
8. Language of the catalog (English only, or per `retailers_v2.language`) — **Open Decision.**

## 10. Backend / System Requirements
- **Catalog generation service** — renders PDF from `products_v2` + crop/pest mappings + the retailer's price entitlement; applies watermark; returns a short-lived signed URL.
- **Asset pipeline** — product images at print-appropriate resolution; the Shopify CDN images used in the prototype are the likely source; missing-image fallback required.
- **Entitlement check** server-side, reusing the Phase 1 price-gating logic — never recomputed in the client.
- **Caching/CDN** for the public MRP catalog; per-retailer variants must not be cached publicly.
- **Events:** `catalog.generated`, `catalog.downloaded`, `catalog.shared`, `catalog.generation_failed`.

## 11. Notifications
- Catalog ready (only when generation is asynchronous and the user left the screen) — **NH**.
- New catalog version available (monthly/seasonal refresh) — **NH**.

## 12. Analytics
`catalog_entry_viewed` (source) · `catalog_options_opened` · `catalog_scope_selected` (scope) · `catalog_version_selected` (priced | mrp_only) · `catalog_generate_started` · `catalog_generate_succeeded` (duration_ms, size_kb, product_count) · `catalog_generate_failed` (reason) · `catalog_opened` · `catalog_shared` (channel) · `catalog_blocked_not_verified`

## 13. Edge Cases
- Very large full catalog on a low-end device — file size and memory.
- Generation times out on a slow connection; the user backgrounds the app mid-download.
- Storage permission denied or device storage full.
- Product images missing or failing to fetch at generation time.
- Prices change between generation and sharing (the printed date is the mitigation).
- Retailer's verification lapses after a priced catalog was downloaded (nothing can be recalled — this is exactly why watermarking matters).
- Retailer shares the priced catalog in a farmer WhatsApp group.
- Duplicate concurrent generation requests (double-tap) — must be idempotent.
- Regional-language product names rendering in the PDF font.
- Signed link opened after expiry.

## 14. Dependencies
**Partner App** catalog + price gating (Phase 1) · **CRM Mongo** (`products_v2`, crop/pest collections) · **Pricing service** · **Marketing** (catalog design, brand approval) · **Regulatory/Agronomy** (printable claims and dosage) · **CDN/storage**

## 15. Acceptance Criteria
1. A non-verified retailer can never obtain a PDF containing partner prices, verified by inspecting the generated file.
2. A verified retailer's priced PDF carries their shop name, retailer code and generation date on every price-bearing page.
3. The MRP-only shareable variant contains no partner price, margin or discount anywhere in the file.
4. Scope selection is respected exactly — a crop-filtered catalog contains only products mapped to that crop.
5. Each product entry shows image, name, technical name, pack size, category and target crop/pest, with a defined fallback when an image is missing.
6. Generation completes within an agreed time budget for the full catalog, with visible progress and a working cancel.
7. A failed generation offers retry without re-entering choices.
8. The share sheet delivers a file that opens correctly in WhatsApp on both Android and iOS.
9. "Last updated" on screen matches the data actually rendered in the file.
10. Rate limiting (once decided) blocks repeated generation with a clear message, not a silent failure.

## 16. Out of Scope
Print-shop-ready artwork or custom branding per retailer · per-retailer catalog curation by RLM · animated/interactive catalogs · offline in-app catalog browsing (a different feature) · stock quantities in the catalog.

## 17. Open Decisions
1. Generation strategy — pre-generated, on-demand, or hybrid?
2. Catalog refresh cadence and the update promise shown to users.
3. Are dosage and application instructions printable? (Regulatory.)
4. Include delisted/out-of-stock SKUs, and how marked?
5. Watermark content and legal wording.
6. Language variants.
7. Rate limits per retailer.
8. Who owns catalog design — Marketing or the app team?

---

# FEATURE 9 — Krishi AI Chatbot

## 1. Status
**Pending** — a scripted demo screen exists; none of the intelligence, data access or guardrails exist.

## 2. Objective
Give retailers a single conversational entry that answers *"what should I sell for this problem"*, *"where is my order"*, *"what is my balance"* and *"how do I return this"* — resolving routine queries without a call to RLM, and converting agronomy questions into correct product recommendations.

## 3. Current State
- `ai-chatbot.html` ("**Katyaa** by Katyayani · Farming AI · Available 24×7") is a **fully scripted demo**: a Hinglish conversation on chilli leaf curl that names two products, renders **product cards** (name, pack, use, price), a **day-wise dosage schedule** (Day 1 / Day 4 / Day 10 with ml/L), a **price card with margin % and an ADD button**, and quick-reply chips (Check price · Disease help · Scheme details · Dose calculator). None of it is connected to anything.
- A **Krishi AI FAB** is specified in the design system, and `scanner.html` (photo → diagnosis) exists as a sibling concept.
- **Verified data that a real assistant could ground on:** `products_v2` (catalog + technicals), `crops_v2`, `crop_problems_v2`, `diseases`, `orders_v2` (status + timeline), and Phase 1 wallet/coins data. The KB also shows `agronomy_*` collections and an agronomy module in the Sales Ops portal — i.e. **company agronomy content exists** and should be the grounding corpus rather than model knowledge.
- No LLM service, retrieval layer, tool-calling contract, safety policy or escalation path exists today.

## 4. Problem / Gap
1. **Everything behind the screen is missing** — this is the largest single build in Phase 2.
2. **Hallucination risk is not theoretical here.** Wrong dosage on a pesticide is a crop-loss and a liability event, not a bad UX.
3. **No grounding contract.** Which fields of `products_v2` are quotable, who signs off agronomy text, and what the assistant may never say are undefined.
4. **No tool layer.** Order status, wallet balance, KYC status and return eligibility must come from APIs; without a tool contract the model will invent them.
5. **No escalation path.** `tickets` exists but is effectively unused (12 manual rows, all SLA fields NULL), so "connect me to support" has nowhere reliable to land today.

## 5. Proposed Solution

**A tool-using assistant over verified company data, with hard rules about what it may generate.**

### Response-type contract (the core design rule)

Every assistant turn is composed of typed blocks, and **only one of them is free-form generated text**:

| Block | Source | Rule |
| --- | --- | --- |
| **Conversational text** | AI-generated | Explanation, clarification, next-step guidance. May never contain a price, stock, date, dosage, balance or eligibility verdict. |
| **Product card** | Catalog API | Name, pack, price, margin, availability — **rendered from API data only**, never typed by the model. |
| **Agronomy block** (dosage, schedule, target pest) | Company agronomy corpus / product label data | Retrieved verbatim or template-filled from approved content. **Never generated.** If not found → "I don't have the approved dosage for this — here is the label / talk to an expert." |
| **Data block** (order status, wallet, coins, KYC, return eligibility) | Backend tool call | Rendered from the API response. If the tool fails → say so; never estimate. |
| **CTA / deep link** | Route registry | Opens an existing screen (PDP, cart, order details, return flow, KYC hub, wallet). |
| **Human handoff** | Support/RLM | Creates a ticket or a callback request with the conversation context attached. |

### Capability scope for Phase 2

**MH (ship with these):** product discovery by crop + problem · product search by name · add to cart through chat · order status/where-is-my-order · wallet & coins balance and history · KYC status and "why is my price locked" · start the existing return flow · human escalation.

**NH (defer if needed):** dose calculator with acreage maths · scheme/offer explanation · slow-moving stock nudges · voice input (Quick Order already has voice; reuse rather than rebuild) · photo diagnosis (that is `scanner.html`, a separate feature).

### Per-capability behaviour

- **A. Product discovery** — extract crop + problem; ask **at most one** clarifying question (the crop, if missing); retrieve from `crop_problems_v2` / `diseases` → mapped products; return up to 3 product cards with why-this-product in one line each; CTAs: View PDP · Add to cart.
- **B. Product search** — fuzzy-match `products_v2`; one card on a confident match, a short list otherwise; pack selection before cart.
- **C. Recommendation** — never recommend without a crop AND a problem. If either is missing, ask for it, once.
- **D. Add to cart through chat** — identify product → confirm pack size → confirm quantity → call the same cart API the app uses → show the updated cart line → CTAs: Continue shopping / Checkout. Blocked paths: unavailable product ("out of stock — notify me / see alternatives"), unavailable pack ("available in 250 ml and 1 L"), price changed (show the current price and ask again), KYC-gated pricing (show the verify CTA), invalid quantity (state the minimum/case multiple).
- **E. Order support** — resolve the order (last order by default, else ask), read `orders_v2.order_status` + `order_status_map[]` + courier status, render a status block with the real timeline; delay explanations use the courier scan log, not speculation; cancellation routes to the existing cancel flow with its own rules.
- **F. Return/refund** — check eligibility via the return service (F4), then **hand off into the existing return flow** with the order and product pre-selected. The chatbot never collects return evidence itself and never creates a parallel return record.
- **G. KYC support** — read KYC status; explain the specific pending item; deep link to the Supporting ID hub. Never promises an approval timeline beyond the configured SLA.
- **H. Wallet/coins** — read balance and recent transactions via API; explain earn/redeem rules from configured content, not from model memory.
- **I. Product knowledge/agronomy** — retrieval-only, as above.
- **J. Escalation** — after one failed resolution attempt, or immediately on request, offer Support: create a ticket with transcript + retailer context, or a callback request to the mapped RLM agent.

### Guardrails (MH, non-negotiable)

1. **Never generate** prices, stock, delivery dates, dosage, refund status, return eligibility, coin balances or KYC verdicts.
2. **No competitor product recommendations**; no advice to mix products unless the approved corpus states it.
3. **No medical/human-safety advice** beyond directing to label instructions and emergency numbers.
4. **Refuse-and-route** on anything outside scope, with a one-line reason and a support CTA.
5. **Every agronomy answer carries its source** (product label / Katyayani agronomy) and a "consult before large-scale application" line where dosage is shown.
6. **Full transcript logging** with retailer id, tool calls and latencies — required to audit any wrong answer.
7. **Language:** replies follow the user's language (Hinglish is the demo default and is the right register for this audience).

## 6. User Flow
```
Home FAB / Help → Katyaa
→ Greeting + suggestion chips
→ User query → Intent classification
   ├─ Agronomy/product → [clarify once if needed] → retrieve → product cards → PDP / Add to cart
   ├─ Order → resolve order → status block → track / cancel / support
   ├─ Money → balance + transactions block → Wallet deep link
   ├─ KYC → status block → Supporting IDs deep link
   ├─ Return → eligibility check → hand off to return flow (pre-filled)
   └─ Unsupported / failed → clarify once → Offer support → ticket or callback
→ (any point) Human handoff with transcript attached
```

## 7. Screen-by-Screen UX

**S1 · Chat screen** (`ai-chatbot.html`, as designed)
- *Purpose:* one conversational surface.
- *Key UI:* header with assistant identity and availability; message list with typed blocks (text, product card, schedule, price card with ADD, data block); quick-reply chips; input with mic (reuse Quick Order voice) and send; "Talk to support" always reachable from the header overflow.
- *Primary CTA:* send. *Secondary:* chips, per-card CTAs, support.
- *States:* Greeting/empty · Typing indicator · Streaming response · Tool-calling ("Checking your order…") · Card rendered · No result · Ambiguous (clarifying question) · Unsupported query · API failure · Rate-limited · Offline · Escalated (banner: "Support has been notified").

**S2 · Product card block**
- *Key UI:* image, name, pack, price (or a Verify CTA when gated), margin %, ADD button, tap → PDP.
- *States:* In stock · Out of stock (ADD disabled + alternatives) · Price locked (verify CTA) · Added (quantity stepper).

**S3 · Data block** (order / wallet / KYC)
- *Key UI:* compact status card with the authoritative values and a deep-link CTA.
- *States:* Loaded · Stale/refreshing · Unavailable ("I couldn't reach that right now — try again or open Orders").

**S4 · Escalation sheet**
- *Key UI:* summary of the issue (editable), attach-transcript toggle, choose Callback or Ticket, submit → reference id.
- *States:* Default · Submitting · Created (with reference) · Failed.

## 8. States
Default · Loading · Empty (new conversation) · Error (model/tool/API) · Success · Pending (escalation raised) · Disabled (input during a blocking action) · Expired (session/context reset) · Retry · Rate-limited · Offline

## 9. Business Rules
1. The assistant recommends **only Katyayani products**. **MH.**
2. Prices, availability and eligibility always come from APIs, never from the model. **MH.**
3. Dosage and agronomy come from approved company content; unavailable content is stated as unavailable. **MH.**
4. Escalation is offered after one failed resolution attempt or on explicit request. **MH.**
5. Which agronomy corpus is authoritative and who approves it — **Open Decision — Agronomy confirmation required.**
6. Conversation retention period and PII handling in transcripts — **Open Decision — Legal.**
7. Per-retailer usage limits / cost caps — **Open Decision — Tech + Business.**
8. Whether the assistant may proactively push offers — recommended **no** for v1. **Open Decision.**
9. Liability disclaimer wording shown with agronomy answers — **Open Decision — Legal.**

## 10. Backend / System Requirements
- **LLM service** with tool calling; model choice, hosting and cost model — **Open Decision — Tech**.
- **Retrieval layer** over `products_v2`, `crops_v2`, `crop_problems_v2`, `diseases` and the approved agronomy corpus, with content versioning.
- **Tool APIs (must exist and be contract-stable):** product search · crop/problem → product mapping · price + availability for this retailer · cart add · order status (from `orders_v2`) · wallet/coins balance + transactions · KYC status · return eligibility + return-flow handoff · ticket/callback creation.
- **Session store** with transcript, tool-call log, latency and outcome.
- **Safety/eval harness** — a regression suite of real retailer questions with approved answers, run before every model or prompt change. **Without this there is no way to know a change made the assistant worse. MH.**
- **Escalation target:** `tickets` (Sales-CRM) is the candidate but is effectively unused — routing, SLA and ownership must be defined before the chatbot can promise a response.
- **Events:** `chat.session_started`, `chat.message_sent`, `chat.intent_detected`, `chat.tool_called`, `chat.product_recommended`, `chat.added_to_cart`, `chat.escalated`, `chat.failed`.

## 11. Notifications
- Escalation acknowledged / agent replied (via Feature 3).
- Callback scheduled / agent calling now.
- **NH:** "Your question was answered by an expert" follow-up.

## 12. Analytics
`chat_opened` (entry: fab | help | deeplink) · `chat_message_sent` (length, language) · `chat_intent_detected` (intent, confidence) · `chat_clarification_asked` · `chat_tool_called` (tool, latency_ms, success) · `chat_product_card_shown` (skus) · `chat_pdp_opened` · `chat_add_to_cart` (sku, qty) · `chat_order_status_shown` · `chat_return_handoff` · `chat_no_result` (query) · `chat_escalated` (reason) · `chat_session_ended` (turns, duration, resolved: yes/no) · `chat_feedback` (thumbs up/down per response) — **thumbs feedback is MH**, it is the only cheap signal of answer quality.

## 13. Edge Cases
- Crop named in a local dialect or a regional-language script.
- Pest described by symptom only ("patte muraj rahe hain") with no crop given.
- Query mixing two intents ("order kahan hai aur ye product bhejo").
- User asks for a competitor product by name.
- User asks for a dosage the corpus does not contain.
- User asks something unsafe ("can I spray double dose").
- Retailer is non-verified — every price in the conversation must be gated consistently.
- Tool returns stale data (order just delivered a minute ago).
- LLM outage → the assistant must degrade to menu-style quick actions, not a dead screen.
- Very long conversation exceeding context — session summarisation and a visible "starting fresh" boundary.
- Abusive input.
- Two devices in the same conversation.
- Screenshot of a chat answer circulating as company advice (the source line and disclaimer matter here).

## 14. Dependencies
**Partner App** catalog/PDP/cart/orders/wallet/KYC/returns · **CRM Mongo** (products, crops, problems, diseases, orders) · **Agronomy team** (approved corpus, sign-off) · **Support / RLM** (escalation, tickets, callbacks) · **Legal** (disclaimers, retention) · **LLM provider** · **Notification service** (F3)

## 15. Acceptance Criteria
1. For a crop+pest query, the assistant returns only Katyayani products that are actually mapped to that problem in company data — verified against a fixed test set.
2. No response containing a price, stock status, dosage, balance, delivery date, refund status or eligibility verdict is produced without a corresponding tool/retrieval call in the session log.
3. When the agronomy corpus lacks an answer, the assistant says so and offers expert/support — it never improvises a dosage. Verified on a set of deliberately out-of-corpus questions.
4. "Add 2 bottles of {product}" results in the correct SKU, pack and quantity in the same cart the app uses, with a visible confirmation.
5. Out-of-stock, unavailable pack, price-changed, KYC-gated and invalid-quantity cases each produce their specified message and CTA.
6. "Where is my order" renders the actual current status and timeline from order data, matching what Order Details shows for the same order.
7. A return request started in chat continues into the existing return flow with order and product pre-filled, and creates no separate return record.
8. Wallet/coins answers match the Wallet screen exactly at the same moment.
9. Escalation creates a ticket or callback with a reference id and attaches the transcript.
10. A tool failure produces an honest failure message with a deep link, never a fabricated answer.
11. Every agronomy response displays its source and the safety line.
12. The evaluation suite runs and passes its agreed threshold before any prompt/model change ships.
13. Full transcripts with tool calls are retrievable for audit.

## 16. Out of Scope
Photo-based crop diagnosis (that is `scanner.html`) · farmer-facing chat · order placement without the existing cart/checkout · payment actions in chat · autonomous outbound messaging · price negotiation · voice call bot.

## 17. Open Decisions
1. LLM provider, model, hosting and per-conversation cost ceiling.
2. Which agronomy corpus is authoritative, and who signs it off?
3. Are dosage schedules allowed in-app at all, given label-compliance obligations? (**Regulatory.**)
4. Transcript retention, PII handling and whether transcripts are visible to RLM.
5. Escalation destination — `tickets`, a new support queue, or direct RLM callback?
6. Usage limits and abuse controls.
7. Is the chatbot allowed to push offers or upsell proactively?
8. Launch scope — all MH capabilities at once, or agronomy+product first with order/money in a second drop?
9. Which team owns the evaluation suite and the quality bar?

---

# FEATURE 10 — My Farmers (CRM-Lite)

## 1. Status
**Enhance** — a rich screen exists; there is no farmer data store behind it.

## 2. Objective
Give the retailer a simple digital version of the notebook they already keep — who their farmers are, what they bought, who owes money, and who to call next — with enough structure that the app can help (reminders, reorder suggestions) without becoming CRM software.

## 3. Current State
- `my-farmers.html` is designed and substantial: header "48 farmers · 12 this month"; three stat tiles (Total 48 · Active 31 last-30-days · Revenue ₹1.1L this month); **Add Farmer** and **Import Contacts** actions; filter chips **All (48) / Active (31) / Due payment (5) / High value (8) / Not ordered 30d**; farmer rows with initials avatar, name, VIP badge, crop · acreage · village, and a right-hand metric block (Last buy / Total spent / Orders) — with a **Due ₹3,400 · Payment due since 18 days · Remind** variant.
- **Add Farmer** and **Edit Farmer Info** sheets exist with fields: Full Name\*, Phone Number\*, Main Crop, Farm Size, Village/Town, Notes (optional).
- **The screen is connected to Inventory:** `inventory.html`'s "Sell to Farmer" flow starts with *Step 1 of 3 — Select Customer · Saved Customers / Add New Customer*, and the Sold History rows are per-farmer with amounts and Received/Due status. **These two features share one customer list — that is the key architectural fact for Phase 2.**
- No backend: no farmer collection, no import, no reminders.

## 4. Problem / Gap
1. **No data store.** Farmers exist only as prototype rows.
2. **Two entry points, one entity.** Farmers added in "Sell to Farmer" and farmers added in My Farmers must be the same record, or retailers will keep two lists and trust neither.
3. **Displayed metrics have no source.** "Total spent", "Orders", "Revenue this month" can only come from what the retailer records in the app (Inventory sales) — the company has **no visibility into retailer→farmer sales**. This must be stated plainly: **My Farmers metrics are retailer-entered data, not Katyayani order data.**
4. **"Due payment" implies a ledger** (udhaar) that does not exist yet beyond the Inventory sale's Received/Due flag.
5. **Import Contacts** raises a real privacy obligation (uploading a phone book) with no consent design.

## 5. Proposed Solution

**Keep it a notebook, not a CRM. One customer entity shared with Inventory.**

**Must Have**
- One `farmer` record per retailer: name\*, phone\*, village, main crop, farm size, notes. Deduplicated on phone within the retailer's own list.
- Farmer list with search and the designed filter chips.
- Farmer profile: contact actions (Call · WhatsApp), purchase history (from Inventory "Sell to Farmer" records only), outstanding due, notes, last interaction.
- Add farmer from both My Farmers and the Inventory sale flow — same record, same store.
- Manual "Add note" and "Set follow-up date" with a reminder notification.

**Nice to Have**
- Import Contacts (with explicit consent and selective import — never a silent bulk upload).
- Crop-season based follow-up suggestions ("Cotton sowing starts in 2 weeks — 12 of your farmers grow cotton").
- Farmer-wise reorder suggestion driven by their last purchase.
- Export farmer list.

**Explicitly not in Phase 2:** pipelines, stages, tasks, lead scoring, farmer app accounts, linking a retailer's farmer to a KKD farmer account (privacy and identity questions that are not worth opening now).

**Field mandatory/optional (MH):**

| Field | Add farmer | Why |
| --- | --- | --- |
| Name | **Mandatory** | The retailer's own identifier |
| Phone | **Mandatory** | Dedupe key + Call/WhatsApp actions + reminders |
| Village/Town | Optional | Useful for grouping, often known |
| Main crop | Optional (**recommended prompt**) | Powers season suggestions and reorder relevance |
| Farm size | Optional | Rough value signal |
| Notes | Optional | The notebook part |

## 6. User Flow
```
Home / Business → My Farmers
→ List (search · filters) → Farmer profile
   → Call / WhatsApp · Add note · Set follow-up · View purchases · Record a sale (→ Inventory sale flow)
→ Add Farmer (name, phone, crop, village) → Saved → appears in list and in Sell-to-Farmer picker
→ [Reminder due] Notification → Farmer profile → Call → Log outcome
```

## 7. Screen-by-Screen UX

**S1 · My Farmers list** (as designed)
- *Purpose:* find a farmer and see who needs attention.
- *Key UI:* header count, stat tiles, Add Farmer / Import Contacts, filter chips, farmer rows with the right-hand metric block, **search (add — the current design has none and 48+ rows needs it)**.
- *Primary CTA:* Add Farmer. *Secondary:* filters, search, row tap.
- *States:* Loading · **Empty (first-time: explain the feature in one line + Add Farmer + Import)** · Default · Filtered-empty · Search-no-results · Error.

**S2 · Add / Edit farmer** (sheets already designed)
- *Key UI:* the six fields, with phone validation and a duplicate warning.
- *Primary CTA:* Save Farmer / Save Changes.
- *States:* Default · Validation error · Duplicate phone (offer "Open existing farmer") · Saving · Saved · Error.

**S3 · Farmer profile** (**new — the current design has no profile screen**)
- *Purpose:* everything the retailer knows about one farmer, on one screen.
- *Key UI:* header (name, village, crop, acreage, VIP/high-value badge), Call · WhatsApp buttons, due-amount strip when applicable with Remind, purchase history list (date, products, amount, Received/Due, invoice), notes timeline, follow-up date, "Record sale" CTA into the Inventory flow.
- *Primary CTA:* "Record sale". *Secondary:* Call · Add note · Set follow-up · Edit.
- *States:* Loading · Default · No purchases yet · Has dues · Inactive (no purchase in 90 days) · Error.

**S4 · Import contacts** (**NH**)
- *Key UI:* permission explainer, contact list with checkboxes (**selective, never all-at-once**), duplicate detection, import summary.
- *States:* Permission prompt · Denied · Loading contacts · Selecting · Importing · Imported (count) · Partial failure.

## 8. States
Default · Loading · Empty (no farmers) · Error · Success (saved) · Pending (reminder scheduled) · Disabled (Save until required fields) · Retry · Filtered-empty · Duplicate

## 9. Business Rules
1. Farmer records are **private to the retailer who created them**. Not shared with other retailers. **MH.**
2. Whether Katyayani (RLM/Marketing) may access or use this farmer data — **Open Decision — Legal + Business confirmation required. This must be answered before Import Contacts ships**, and the answer must be reflected in the in-app consent text.
3. Phone number is the dedupe key within a retailer's list. **MH.**
4. "Active / Inactive" definition (the design implies last 30 days) — **Open Decision.**
5. "High value" threshold — **Open Decision.**
6. Due/udhaar amounts come only from Inventory sale records marked Due; the app does not compute credit or interest. **MH.**
7. Whether a farmer record can be deleted (and whether sales history survives) — **Open Decision.** Recommended: archive, keep history.
8. Maximum farmers per retailer — **Open Decision** (a practical cap prevents contact-book dumping).

## 10. Backend / System Requirements
- **Farmer store** scoped by retailer, with name, phone (normalised +91), village, crop, farm size, notes, follow-up date, created/updated, archived flag.
- **Shared customer service with Inventory** — one entity, two entry points. Do not create two tables.
- **Sales linkage** — retailer→farmer sale records written by the Inventory "Sell to Farmer" flow (Feature 11) are the only source of purchase history and dues.
- **Reminder scheduler** — follow-up date → notification.
- **Contacts import** (NH) — client-side selection, server stores only chosen contacts.
- **Events:** `farmer.created`, `farmer.updated`, `farmer.archived`, `farmer.note_added`, `farmer.followup_set`, `farmer.reminder_fired`, `farmer.contacted` (call/WhatsApp tap).
- **Privacy:** this is third-party personal data (farmers who are not our users). Retention, access and deletion rules must be defined with Legal.

## 11. Notifications
Follow-up reminder due · Payment due reminder (**Open Decision** — retailer-configured or automatic) · **NH:** season-based suggestion ("12 of your farmers grow cotton — sowing starts soon") · **NH:** inactive-farmer nudge.

## 12. Analytics
`my_farmers_opened` · `farmer_search_used` · `farmer_filter_applied` (filter) · `farmer_add_started` / `_saved` (fields_filled) · `farmer_duplicate_detected` · `farmer_profile_viewed` · `farmer_called` / `farmer_whatsapped` · `farmer_note_added` · `farmer_followup_set` / `_reminder_opened` · `farmer_sale_recorded_from_profile` · `contacts_import_started` / `_completed` (count) · retention: `farmers_added_per_active_retailer`, `weekly_active_my_farmers`

## 13. Edge Cases
- Same farmer buying from two retailers — two independent private records; no merge, by design.
- Phone number reused by a different person.
- Farmer without a phone (cash walk-in) — **Open Decision**: allow a record without phone, or block? (Recommended: allow, with dedupe by name+village and reduced features.)
- Retailer imports 900 contacts including non-farmers.
- A farmer asks to be removed (deletion request) — the retailer must be able to delete; our retention policy must permit it.
- Retailer changes device — data must be server-side, not local.
- Duplicate created via the Inventory flow while one exists in My Farmers.
- Very long notes; notes containing sensitive information.
- Due amount settled in cash outside the app — the retailer must be able to mark it settled (**this belongs to Feature 11's sale record**).

## 14. Dependencies
**Partner App** Inventory "Sell to Farmer" (F11 — shared customer entity) · **Notification service** (F3) · **Legal/Privacy** (third-party data, contacts import) · **Business Dashboard** (Phase 1) if farmer metrics surface there

## 15. Acceptance Criteria
1. A farmer added in My Farmers appears immediately in the Inventory "Sell to Farmer" customer picker, and vice versa — one record, not two.
2. Adding a farmer with an existing phone number in the same retailer's list warns and offers to open the existing record instead of creating a duplicate.
3. Name and phone are enforced as mandatory; all other fields save as empty without error.
4. The farmer profile's purchase history matches the sale records created in Inventory for that farmer, including Received/Due status and amounts.
5. Filter chips return the counts shown on the chips themselves.
6. Search finds a farmer by name, phone or village.
7. Call and WhatsApp open with the correct number pre-filled.
8. A follow-up date produces a notification on that date, deep-linking to the farmer profile.
9. Farmer data is visible after reinstalling the app on a new device (server-persisted).
10. One retailer can never see another retailer's farmers (verified with two accounts).
11. Contacts import (if shipped) imports only explicitly selected contacts, and the consent text matches the agreed policy.
12. Empty state explains the feature and offers Add Farmer rather than showing empty stat tiles.

## 16. Out of Scope
Pipelines/stages/deal tracking · farmer login or farmer app accounts · linking to KKD farmer identities · credit scoring or interest calculation on dues · SMS campaigns to farmers · sharing farmer data between retailers or with RLM (pending the privacy decision).

## 17. Open Decisions
1. **Can Katyayani use retailer-entered farmer data?** (Legal + Business — blocks Import Contacts and any RLM visibility.)
2. Active/inactive and high-value definitions.
3. Are farmers without a phone number allowed?
4. Delete vs archive, and what happens to sale history.
5. Is payment-due reminding automatic or retailer-triggered?
6. Retention policy for third-party personal data.
7. Cap on farmers per retailer.

---

# FEATURE 11 — Inventory Tracker (Per SKU)

## 1. Status
**Enhance** — the richest existing prototype; the adoption mechanic (delivered-order → inventory) is the missing piece.

## 2. Objective
Make the inventory tracker maintain itself wherever possible — starting with delivered Katyayani orders — so retailers keep using it, and so low-stock reorder becomes a reliable demand signal for us.

## 3. Current State
`inventory.html` is the most complete Phase 2 prototype (970 lines) and already contains:
- Header "My Inventory · Katyayani + Other Brands", **Add Item**, tabs **All Stock / Katyayani / Other Brands**, stat tiles **24 Total SKUs · 3 Low Stock · ₹4,280 Today's Sales**, category chips (All / Pesticides / Fertilizers / Seeds / Other).
- A **low-stock banner** — "3 products running low · Tap to reorder from Katyayani".
- Product rows with brand, technical name, quantity in the retailer's own unit (cases/bags/bottles), "Updated 2d ago", **LOW** badge with "Below minimum threshold (min: 10 cases)", and actions **Reorder / Update Stock / Edit**.
- **Add Product** flow: choose source — *From Katyayani Catalog* (search & add) or *Add Other Brand* (Brand, Product, Category, Pack Size, Current Qty, **Min Stock Alert**).
- **Update Stock** sheet with New Stock Count and **Reason** (New purchase arrived · Manual correction · Stock damage/loss · Return from farmer).
- **Sell to Farmer** — 3 steps (Select Customer → Product/Qty/Price/Payment status → Mark as Sold) producing a **Sale Invoice** with Share on WhatsApp.
- **Sold History** — last 30 days, per-farmer rows with amount, product, qty, unit price, date, Received/Due and Invoice.

**Missing entirely:** any backend, and the delivered-order → inventory suggestion that the Phase 2 brief centres on.

## 4. Problem / Gap
1. **Manual entry kills adoption.** Every unit must be typed today; retailers abandon this within a week.
2. **No link to delivered orders** — we know exactly what we delivered and when, and we do not use it.
3. **Unit mismatch is the hidden problem.** Orders are placed in cases/units; inventory is counted in the retailer's own unit ("12 cases", "45 bags", "20 kg bags"). Without a conversion, auto-add will produce wrong numbers and destroy trust in the feature.
4. **No stock ledger** — quantities are shown without an auditable movement history, so "why is my count wrong" is unanswerable.
5. Stat tiles ("Today's Sales", "Inventory value") imply computation that has no defined source.

## 5. Proposed Solution

### The core mechanic (MH) — delivered order → inventory

```
Order delivered → notification: "10 units of Imida 30.5% SC were delivered. Add to your inventory?"
→ Tap → Add-delivered-stock sheet (pre-filled lines, editable quantities)
→ Confirm → Stock increases · ledger entry "Order #KAT-2026-04-1284 · +10 units"
→ Dismissed or ignored → the prompt stays as a card at the top of Inventory for N days
```

Rules that make it trustworthy:
- Pre-filled quantities come from the **delivered** lines of `orders_v2`, in the ordered unit, with the retailer's inventory unit shown alongside ("1 case = 20 units → +10 cases").
- The retailer can **edit each line** before confirming (short delivery, damaged units).
- **Idempotent:** an order can be added to inventory **once**; the card then reads "Added to inventory on 12 Sep".
- Every auto-addition is a ledger entry attributed to the order — never an unexplained jump.
- Products not yet in the retailer's inventory are **created automatically** from the catalog on confirmation, with a default min-stock threshold (**Open Decision** on the default).

### Must Have (v1)
SKU list with Katyayani/Other tabs · current quantity per SKU with unit · add stock · remove/adjust stock with reason (already designed) · low-stock threshold per SKU + LOW badge · low-stock banner with Reorder into the existing cart · search · category filter · **delivered-order suggestion** · **stock ledger/history per SKU** · Sell to Farmer with invoice (already designed) · Sold History.

### Nice to Have (v2)
Inventory value · fast/slow-moving classification · suggested reorder quantity · expiry/batch tracking · barcode scan to update stock (`scanner.html` exists) · CSV export · multi-location stock.

> **Explicitly deferred:** batch/expiry tracking. It is the most requested "real" inventory feature and the most expensive; agri-input batch rules deserve their own scoping, not a corner of Phase 2.

## 6. User Flow
```
[Auto path]  Order delivered → Notification → Add delivered stock sheet (editable)
             → Confirm → Inventory updated + ledger entry
[Manual path] Inventory → Update Stock → New count + reason → Saved → ledger entry
[Add path]   Inventory → Add Item → From Katyayani Catalog / Other Brand → Save
[Sell path]  Inventory → Sell to Farmer → Customer → Product/Qty/Price/Payment → Invoice
             → Stock decreases + ledger entry + farmer purchase history (F10)
[Reorder]    Low-stock banner / row Reorder → Cart (existing) → Checkout
```

## 7. Screen-by-Screen UX

**S1 · Inventory home** (as designed + two additions)
- *Additions:* a **pending "add delivered stock" card** at the top when applicable, and a **History** entry per row.
- *Primary CTA:* Add Item. *Secondary:* tabs, chips, Reorder, Update Stock, Edit, Sell to Farmer.
- *States:* Loading · **Empty (first-run: "Add your stock in 2 minutes — start from your last delivered order")** · Default · Low-stock present · Filtered-empty · Error · Sync pending (offline edits queued).

**S2 · Add delivered stock sheet** (**new, MH**)
- *Purpose:* one tap from delivery to accurate stock.
- *Key UI:* order id + delivery date, line rows (product, delivered qty, unit conversion line, editable inventory qty, include/exclude toggle), total lines, Confirm.
- *Primary CTA:* "Add to inventory". *Secondary:* "Not now" (keeps the card), "Don't ask for this order".
- *States:* Default · Edited · Partially excluded · Confirming · Added (success, ledger written) · Already added (read-only) · Expired (older than the configured window) · Error.

**S3 · Update stock** (as designed)
- *Key UI:* new count, reason select, optional note.
- *States:* Default · Invalid (negative) · Saving · Saved · Error.

**S4 · Stock history / ledger** (**new, MH**)
- *Purpose:* answer "why is this number what it is".
- *Key UI:* chronological movements — +10 (Order #…) · −3 (Sold to Sohan Patel) · −1 (Damage) · set to 12 (Manual correction) — each with date, actor and reference.
- *States:* Loading · Default · Empty · Error.

**S5 · Sell to Farmer** (as designed — 3 steps + invoice)
- *Addition:* stock is decremented and a ledger entry written; the sale is written to the shared farmer record (F10).
- *States:* as designed, plus Insufficient stock (warn, allow override with a reason — retailers sell from stock they forgot to record).

## 8. States
Default · Loading · Empty (no SKUs) · Error · Success · Pending (unconfirmed delivered stock) · Disabled (Confirm until a line is included) · Expired (stale delivered-stock prompt) · Retry · Offline/sync-pending · Low stock · Out of stock

## 9. Business Rules
1. Inventory is **retailer-owned data**; Katyayani does not adjust it. Only the retailer confirms movements. **MH.**
2. Delivered-order additions are **suggestions requiring confirmation** — never automatic. **MH.** (Silent auto-add would produce wrong counts and destroy trust.)
3. One order can be added to inventory once. **MH.**
4. Prompt validity window after delivery — **Open Decision** (recommended 7 days, then the card is archived).
5. Default min-stock threshold for auto-created SKUs — **Open Decision.**
6. Unit conversion (case → units/bottles/bags) must come from catalog pack data, not retailer guesswork. Where the catalog lacks it, ask once and remember. **MH.**
7. Negative stock is not allowed; an over-sale prompts a correction. **MH.**
8. "Today's Sales" and "Inventory value" definitions (cost vs MRP vs partner price) — **Open Decision — Business.**
9. Is inventory data visible to RLM for demand planning? — **Open Decision — Business + Legal** (it is commercially sensitive to the retailer).

## 10. Backend / System Requirements
- **Inventory store** per retailer per SKU: quantity, unit, min threshold, brand (Katyayani vs other), category, last-updated.
- **Stock ledger** — append-only movements with type (order_delivered, manual_add, manual_correction, sale, damage, farmer_return), quantity delta, reference id, actor, timestamp. **This is the backbone; the current quantity should be derived from it.**
- **Delivered-order feed** — from `orders_v2` delivered lines + delivery timestamp from `order_status_map[]`, with per-order "added to inventory" state.
- **Catalog linkage** — `products_v2` for Katyayani SKUs (name, technical, pack, case size); free-text records for other brands.
- **Sales records** — shared with Feature 10 (farmer, products, amount, payment status, invoice).
- **Offline support (MH-lite):** stock updates must queue offline and sync — retailers count stock in the godown where there is no signal.
- **Events:** `inventory.item_added`, `inventory.stock_updated` (reason), `inventory.low_stock_reached`, `inventory.delivered_stock_prompted` / `_added` / `_dismissed`, `inventory.sale_recorded`, `inventory.reorder_clicked`.

## 11. Notifications
**Delivered stock available to add** (the headline notification for this feature) · Low stock on a SKU (frequency-capped) · **NH:** weekly stock summary · **NH:** "you have not updated stock in 30 days" nudge.

## 12. Analytics
`inventory_opened` · `inventory_empty_viewed` · `inventory_item_added` (source: catalog | other_brand | delivered_order) · `delivered_stock_prompt_shown` (order_id, lines) · `delivered_stock_added` (lines, edited_lines) · `delivered_stock_dismissed` · `stock_updated` (reason, delta) · `low_stock_banner_clicked` · `inventory_reorder_clicked` (sku) → **`inventory_reorder_to_order`** (the commercial payoff metric) · `sale_recorded` (amount, payment_status) · `invoice_shared` · `stock_history_viewed` · adoption: `active_inventory_users_weekly`, `skus_per_retailer`, `share_of_deliveries_added_to_inventory`

## 13. Edge Cases
- Delivered quantity differs from what actually arrived (short/damaged delivery).
- Order delivered while the retailer has no inventory record for that SKU → auto-create.
- Partial delivery across two shipments of one order.
- Retailer already added the stock manually before the prompt appeared → duplicate risk; the "Already added / Not now" state and the ledger make this visible, but a warning is needed.
- Returned order after inventory was added — the ledger needs a reversal entry; **Open Decision** whether it is prompted or automatic.
- Case-size change in the catalog after stock was recorded.
- Selling more than recorded stock.
- Two devices editing stock simultaneously — last-write-wins with a ledger trail.
- Offline edits synced hours later, out of order.
- Other-brand product with a duplicate name to a Katyayani SKU.
- Retailer counts in a unit we do not model ("half bag").
- A very large inventory (200+ SKUs) — list performance and search.

## 14. Dependencies
**Partner App** Orders (delivered lines) · Cart/Reorder · `products_v2` catalog · **My Farmers (F10)** shared customer + sales records · **Notification service (F3)** · **Business Dashboard** (Phase 1) if inventory metrics feed it

## 15. Acceptance Criteria
1. Delivering an order produces a notification and an Inventory card offering the delivered lines with correct pre-filled quantities and unit conversions.
2. Confirming adds exactly the confirmed quantities, creates ledger entries referencing the order, and flips the order's state to "Added to inventory".
3. The same order cannot be added twice, from any entry point.
4. Editing a line before confirming stores the edited quantity, and the ledger records the edit.
5. Manual stock updates require a reason and produce a ledger entry showing the delta.
6. The stock ledger for any SKU explains its current quantity — the sum of movements equals the displayed count.
7. LOW badge and the low-stock banner appear exactly when quantity ≤ the SKU's threshold, and Reorder lands the correct SKU in the cart.
8. Selling to a farmer decrements stock, writes the sale to that farmer's history, and generates a shareable invoice.
9. Selling more than available stock is blocked or requires an explicit correction — stock never goes negative.
10. Stock edits made offline sync on reconnect without loss or duplication.
11. An other-brand product can be added with pack size and threshold and behaves identically to a Katyayani SKU except for Reorder.
12. Empty state offers the delivered-order starting path rather than an empty table.

## 16. Out of Scope
Batch/expiry tracking · GST-compliant invoicing and tax filing (the invoice here is a counter receipt) · purchase orders to other brands · multi-warehouse/location stock · barcode scanning (**NH**, `scanner.html` may cover it later) · automatic stock deduction from any source other than the retailer's own recorded sales.

## 17. Open Decisions
1. Prompt validity window after delivery.
2. Default min-stock threshold for auto-created SKUs.
3. Definition of "Today's Sales" and "Inventory value".
4. Reversal behaviour when a delivered order is returned.
5. Is inventory data visible to RLM/Marketing for demand planning? (Commercially sensitive.)
6. Do we model fractional units ("half bag")?
7. Is the Sell-to-Farmer invoice required to carry GST details? (Accounts/Legal.)

---

# FEATURE 12 — Instagram-Style Story Rail

## 1. Status
**Testing** — implemented, under test. **No redesign. This section is a readiness checklist only.**

## 2. Objective
Keep a high-engagement, low-cost surface on Home for schemes, tips, quizzes and success stories — and confirm it is stable enough to ship.

## 3. Current State
- Implemented in `home.html`: a story rail with 8 stories — `flash-sale`, `new-arrivals`, `quiz`, `tips`, `spray-guide`, `success`, `margin-boost`, `demo` — feeding a **full-screen Instagram-style viewer** with segmented progress bars, header title, close, tap-left/tap-right navigation (`prevStory()` / `nextStory()`), a per-story action button, a **5,000 ms auto-advance timer**, and an interactive **quiz story** with correct/incorrect answer handling.
- Story content is currently **hard-coded in the page** (`STORY_KEYS` + `STORY_DATA`).
- The design system documents the story-rail pattern (ring + label).
- `app_announcements` (Supabase, 0 rows, type banner/notification/popup, segment/cohort/state targeting, start/end window) is the only existing table shaped anything like a story CMS — **it is unused, and whether stories will be served from it is undecided.**

## 4. Problem / Gap (release-blocking candidates)
1. **Content is hard-coded.** Shipping as-is means every story change is an app release. Whether Phase 2 ships static stories or a content-served rail is an **Open Decision — but it must be answered before release**, because it changes the test plan entirely.
2. **No seen/unseen persistence** across sessions is evident in the implementation — the ring state must survive an app restart, or the rail looks broken on day two.
3. **No expiry** — a "Flash sale" story that outlives the sale is worse than no story.
4. **No analytics** on a purely engagement-driven surface means we cannot justify keeping it.

## 5. Testing / Readiness Checklist

### A. Story loading
- [ ] Rail renders within the Home first paint budget and never blocks Home content.
- [ ] Rail renders correctly with 1, 3, 8 and 20 stories.
- [ ] Thumbnails lazy-load; failed thumbnails fall back gracefully (no broken-image icon).
- [ ] Rail is horizontally scrollable with momentum and no clipping at either edge.

### B. Full-screen viewer
- [ ] Opens on the tapped story, not the first one.
- [ ] Progress bars match the story count and the active index.
- [ ] Auto-advance is 5 s per story, pauses on long-press, resumes on release.
- [ ] Advancing past the last story closes the viewer (does not loop endlessly).
- [ ] Safe-area handling on notched devices and gesture-navigation phones.
- [ ] Status bar / system UI state restores correctly on close.

### C. Navigation
- [ ] Tap right → next, tap left → previous, at every position including the first and last.
- [ ] Swipe down / X closes; hardware back closes the viewer, not the app.
- [ ] Rapid tapping does not skip two stories or desync the progress bar.
- [ ] Backgrounding mid-story pauses; returning resumes at the same story without replaying the whole set.

### D. Seen / unseen
- [ ] Unseen stories show the active ring; seen stories show the muted ring.
- [ ] Seen state persists across app restart **and** across reinstall behaviour is defined (decide: reset is acceptable).
- [ ] Opening the rail from a seen story does not mark unseen ones as seen.
- [ ] New content resets the ring for that story only.

### E. Interactive stories (quiz)
- [ ] Correct and incorrect answers both render their state and do not break auto-advance.
- [ ] The timer pauses while an answer is being chosen.
- [ ] Re-opening an answered quiz shows the answered state, not a fresh question.
- [ ] Any reward promised by a quiz is actually credited (**or the promise is removed** — an uncredited promise is release-blocking).

### F. Deep links and CTAs
- [ ] Every story action button routes to a valid screen (PDP, scheme, training, cart) — the full list is tested route by route.
- [ ] A CTA for a delisted product or an ended scheme degrades to a sensible screen, not an error.
- [ ] Returning from a CTA re-enters Home cleanly, with the viewer closed.

### G. Content robustness
- [ ] Missing image, missing title, very long title, missing CTA — each renders without layout break.
- [ ] Regional-language and long Hindi strings do not overflow.
- [ ] A malformed story object is skipped, not crashed on.

### H. Network
- [ ] 2G/slow 3G: story media shows a loading state, and a stalled load does not freeze the viewer.
- [ ] Offline: the rail either hides or shows cached stories — **defined behaviour, not accidental**.
- [ ] Mid-story connection loss is handled and retriable.

### I. Content lifecycle
- [ ] Expired stories (past end date) do not appear — requires the expiry decision.
- [ ] Scheduled stories do not appear before their start date.
- [ ] Ordering is deterministic and matches what content owners configured.
- [ ] Empty content set → the rail hides entirely and Home has no empty gap.

### J. Analytics (must be live before release)
- [ ] `story_rail_viewed`, `story_opened` (story_id, position), `story_completed`, `story_skipped` (direction), `story_exited` (story_id, dwell_ms), `story_cta_clicked` (story_id, route), `story_quiz_answered` (correct/incorrect).

### K. Stability
- [ ] No crash on rapid open/close cycles (50×).
- [ ] No memory growth after viewing all stories repeatedly (low-end device).
- [ ] No ANR from media decoding on a 2 GB RAM device.
- [ ] Rotation / split-screen behaviour is defined (recommended: lock portrait).

### L. Production readiness
- [ ] Content update path is decided and documented (static release vs served).
- [ ] Someone owns story content operationally, with a publishing cadence.
- [ ] A kill switch exists to hide the rail without an app release.

## 6. Critical issues that should block release
1. **No kill switch.** A bad story on Home with no way to remove it except a release is the single biggest operational risk.
2. **Hard-coded content with no expiry** — a live "Flash sale" story after the sale ends is a credibility problem, particularly around pricing.
3. **Seen/unseen not persisted** — the rail appears permanently "unread", training users to ignore it.
4. **Any reward promised inside a story (the quiz) that is not actually credited.**
5. **No analytics** — the feature cannot be evaluated or defended in the next planning cycle.

## 7. Out of Scope
Redesigning the rail or viewer · story creation by retailers · reactions/replies · video stories with audio (unless already implemented) · personalised story ordering.

## 8. Open Decisions
1. Static stories for Phase 2, or served from a content source (and if served — `app_announcements`, a new store, or the existing CMS used by `app_content`/`home_banners`)?
2. Who owns story content operationally, and at what cadence?
3. Is a kill switch in scope for this release? (Recommended: yes, blocking.)
4. Story expiry and scheduling rules.
5. Does the quiz carry a real reward?

---

# FEATURE 13 — Screen Share with Support

## 1. Status
**Pending** — the screens are designed convincingly, but the underlying capability is **unproven** and the RLM-side console does not exist.

## 2. Objective
Let a retailer show Support/RLM what is wrong on their screen, live, instead of describing it on a call or sending screenshots — reducing resolution time on app-related issues.

## 3. Current State
- `screen-share.html` is designed end-to-end: hero "Show your issue, get help live" with "Advisors online", a 3-step explainer (Tap start · Talk live · End anytime), three **privacy assurances** — "Only this app is shared · end-to-end encrypted", "Other apps can't record this session", "Advisor can see — not tap or pay"; **Start Screen Share**; a **Connecting** state ("Finding your advisor", estimated wait ~12 s, "Securing your session", "Encrypted channel ready", "Routing to next available advisor"); an **active session** overlay on a real app screen with a timer (00:23) and session controls (**Voice call · Mute · Pause · Highlight · End**); and a **Session ended** screen with advisor name/ID, duration, topic, status (Resolved), a 4-emoji feedback rating, and the assurance "No screen content was stored. Encrypted channel terminated."
- **Support backend reality:** `tickets` (Sales-CRM) holds 12 manual rows with every routing/SLA/escalation column NULL. There is **no live-support queue, no agent presence system and no session infrastructure** today.
- Phase 1/prototype context: `help.html`, `help-topic.html` and RLM contact paths exist.

## 4. Problem / Gap — and the feasibility position stated plainly

**Product requirement vs technical feasibility must not be conflated here.** The designed experience makes four promises. Their feasibility differs:

| Promise on screen | Feasibility | Note |
| --- | --- | --- |
| "Only this app is shared" | **Partly achievable.** In-app view streaming (rendering the app's own view hierarchy to the session) shares only our app and is fully under our control. | This is the recommended approach. |
| Full-device screen share via OS capture | **Achievable but not restricted to our app.** Android `MediaProjection` and iOS ReplayKit capture **the whole device**, including notifications and other apps if the user switches. The "other apps can't record" framing is also not literally what the OS guarantees. | If OS capture is used, the privacy copy must change. |
| "End-to-end encrypted" | **Provider-dependent.** True E2EE is not what most WebRTC/SDK vendors provide by default (media is encrypted in transit, often via relay servers). | Copy must match what the chosen provider actually does. **Do not ship this sentence unverified — it is a compliance claim.** |
| "Advisor can see — not tap or pay" | **Achievable** (view-only, no remote control). | Keep — and never add remote control in Phase 2. |

Additional gaps:
1. **No agent presence/queue** — "Advisors online" and "~12 s wait" require a real presence system.
2. **No session-to-ticket linkage** — the designed "Session ended · Status: Resolved" implies a ticket lifecycle that does not exist.
3. **Sensitive-screen masking is undefined** — wallet, KYC documents, Aadhaar digits and payment screens are all reachable during a session.
4. **Recording policy undefined** — the screen says nothing is stored; if any provider records by default, that copy becomes false.

## 5. Proposed Solution

**Recommended Phase 2 scope: in-app, view-only, one-way screen streaming with an audio call, plus a support session record.**

- **In-app streaming only (MH).** Share the Partner App's own screens. If the user leaves the app, the stream shows a "Paused — app not in foreground" placeholder rather than capturing other apps. This makes the privacy promise true by construction.
- **Automatic masking (MH).** Aadhaar/PAN/GST numbers, document images, wallet balances and payment fields are masked in the shared stream by marking those views as sensitive. The masked regions render as a grey block with "Hidden for your safety".
- **Explicit consent per session (MH).** A consent sheet listing what the advisor can see, what they cannot, that the session can be ended anytime, and the recording policy. Consent is logged with the session.
- **View-only (MH).** No remote control, ever, in Phase 2.
- **Session record (MH).** Every session creates a support record with id, retailer, agent, start/end, duration, topic and outcome — linked to the existing ticket concept if it is usable, otherwise a new session store.
- **Fallback when live share is unavailable (MH).** If no advisor is online or the SDK fails, offer: "Send a screen recording" (OS-native recording shared to Support) or "Request a callback". The feature must never dead-end on "no advisors online".
- **Deferred (NH / later phase):** full-device sharing, session recording for audit, co-browsing, advisor annotation beyond the designed Highlight.

## 6. User Flow
```
[Partner App]
Help / any screen → "Share screen with support"
→ Consent sheet (what is shared, what is hidden, end anytime) → Agree
→ [Permission prompt if the platform requires one]
→ Connecting (queue position / estimated wait) → Advisor accepted
→ Active session (timer, Mute · Pause · Highlight · End; masked regions visible as hidden)
→ Advisor guides over voice → Issue resolved
→ End (by user or advisor) → Session ended screen → Feedback rating
→ Session/ticket updated

[No advisor / failure]
→ "No advisor available right now" → Request callback · Send screen recording · Back to Help

[RLM/Support console]
Incoming request (retailer name, shop, KYC/tier, last order, issue topic, app version, device)
→ Accept / Reject → Live viewer (view-only) + voice → Notes → End → Outcome + ticket update
```

## 7. Screen-by-Screen UX

**S1 · Entry point** (`screen-share.html` hero, as designed)
- *Purpose:* explain and start.
- *Key UI:* value line, advisor-availability indicator, 3-step explainer, the three privacy lines (**wording to be corrected to match the chosen technology**), Start.
- *Primary CTA:* "Start Screen Share". *Secondary:* "How this works".
- *States:* Advisors available · **No advisors / outside support hours (fallbacks shown)** · Feature unavailable on this device/OS version · Default.

**S2 · Consent sheet** (**new, MH** — the current design asserts privacy but does not capture consent)
- *Key UI:* bulleted what-is-shared / what-is-hidden, recording statement, "You can end anytime", Agree / Cancel.
- *States:* Default · Agreed (logged) · Cancelled.

**S3 · Connecting** (as designed)
- *Key UI:* progress steps, estimated wait, Cancel.
- *States:* Queued (with position) · Connecting · Timed out ("No advisor picked up — request a callback") · Failed (network/SDK) · Cancelled by user.

**S4 · Active session** (as designed)
- *Key UI:* persistent session bar with timer and End, visible on every screen; controls Voice call · Mute · Pause · Highlight · End; a clear "You are sharing" indicator that cannot be dismissed.
- *States:* Connected · Paused by user · Paused (app backgrounded) · Advisor speaking · Poor network (quality warning) · Reconnecting · Ended by user · Ended by advisor · Dropped.

**S5 · Session ended** (as designed)
- *Key UI:* advisor name + id, duration, topic, outcome, the "nothing was stored" statement (**only if true**), emoji feedback, Share again / Back to Help.
- *States:* Ended normally · Ended by advisor · Dropped (with retry) · Feedback submitted.

**S6 · Support/RLM console** (**new, MH — outside the Partner App**)
- *Key UI:* incoming request queue with retailer context (shop, tier, KYC status, last order, app version, device, current screen name), Accept/Reject, live view pane, voice controls, notes, End, outcome + ticket linkage, session history.
- *States:* Idle · Incoming · In session · Ended · Missed · Rejected.

## 8. States
Default · Loading (connecting) · Empty (no sessions in history) · Error (SDK/network/permission) · Success (resolved) · Pending (queued) · Disabled (outside support hours) · Expired (request timed out) · Retry · Paused · Dropped

## 9. Business Rules
1. A session requires **explicit per-session consent**; consent is logged. **MH.**
2. The retailer can end the session at any moment, from any screen. **MH.**
3. The advisor has **view-only** access — no control, no input, no transactions. **MH.**
4. Sensitive fields are masked in the stream. **MH — the exact field list is an Open Decision (Legal + Product).**
5. Recording policy — **Open Decision — Legal confirmation required.** If sessions are ever recorded, consent copy, retention and access control must all change.
6. Support hours and availability — **Open Decision — Operations.**
7. Maximum session duration and idle timeout — **Open Decision.**
8. Who may accept sessions (any agent, or only the retailer's mapped RLM?) — **Open Decision — Operations.**
9. Whether a session must be tied to an existing ticket or can stand alone — **Open Decision.**

## 10. Backend / System Requirements
- **Real-time session SDK/provider** — selection pending; must support in-app view streaming, view-only sharing, sensitive-view masking, audio, and a stated encryption posture. **Open Decision — Tech, and a proof-of-concept should precede any commitment.**
- **Agent presence & queue service** — online status, routing, accept/reject, timeout. Does not exist.
- **Session store** — id, retailer, agent, consent record, timestamps, duration, topic, outcome, quality metrics.
- **Ticket linkage** — `tickets` is the candidate but is unused with NULL routing/SLA; using it requires defining routing and ownership first.
- **App instrumentation** — current screen name and app version passed as session context (this is what makes the advisor useful immediately).
- **Events:** `screenshare.requested`, `.consented`, `.queued`, `.accepted`, `.rejected`, `.started`, `.paused`, `.ended`, `.dropped`, `.feedback_submitted`.

## 11. Notifications
Session request received (advisor side) · Advisor connected · Session ended summary · Callback scheduled (fallback path) · Ticket updated after the session.

## 12. Analytics
`screenshare_entry_viewed` (source screen) · `screenshare_consent_shown` / `_agreed` / `_declined` · `screenshare_requested` · `screenshare_queue_wait` (seconds) · `screenshare_accepted` (wait_time) · `screenshare_abandoned_in_queue` · `screenshare_started` · `screenshare_duration` · `screenshare_paused` (reason) · `screenshare_dropped` (reason) · `screenshare_ended` (by: user | advisor) · `screenshare_feedback` (rating) · `screenshare_fallback_used` (callback | recording) · outcome: `issue_resolved_rate`, `repeat_session_rate`

## 13. Edge Cases
- No advisor online (the most common real case — the fallback path is what determines whether this feature is useful).
- Retailer on 2G — video quality collapses; the session must degrade to voice + screenshots rather than freeze.
- Incoming phone call during a session.
- App backgrounded or killed mid-session.
- Retailer navigates to a masked screen and cannot understand why the advisor "can't see" — the masked block must be self-explanatory.
- Retailer switches to another app expecting it to be shared (it is not, by design) — the paused placeholder must explain.
- OS denies the capture permission, or the OS version does not support the SDK.
- Advisor disconnects mid-session.
- Session exceeds maximum duration.
- Device does not meet SDK requirements (old Android) — the entry point must be hidden, not failing.
- Retailer takes a screenshot of the session for their own record.
- Two sessions requested from two devices on the same account.

## 14. Dependencies
**Partner App** Help/Support · **Support / RLM** (console, staffing, hours, SOPs) · **RLM Admin** (agent roles, routing) · **Sales Operation Portal / `tickets`** (session-to-ticket linkage) · **External SDK/provider** (**undecided**) · **Legal** (consent, recording, masking) · **Notification service (F3)**

## 15. Acceptance Criteria
1. The entry point appears only on devices/OS versions the chosen SDK supports; elsewhere the fallback options are shown instead.
2. A session cannot start without explicit consent, and the consent record is stored with the session id.
3. During a session, only Partner App screens are visible to the advisor — leaving the app shows the paused placeholder, verified by an observer on the advisor side.
4. Every field on the agreed sensitive list renders masked on the advisor's view, verified screen by screen (KYC, wallet, payment).
5. The advisor cannot interact with the retailer's app in any way (no tap, no scroll, no input) — verified by attempt.
6. The retailer can end the session from any screen within one tap, and the advisor's view terminates immediately.
7. A session that no advisor accepts within the timeout offers callback and screen-recording fallbacks.
8. The session-ended screen reports the true duration and outcome, and the privacy statement shown matches the provider's actual behaviour.
9. A session record with id, participants, duration and outcome is retrievable by Support afterwards.
10. Network drop produces a reconnect attempt and, on failure, a clean ended state on both sides.
11. Any claim of encryption in the UI is backed by written confirmation from the provider.

## 16. Out of Scope
Remote control of the retailer's device · full-device screen sharing (deferred) · session recording and playback (pending Legal) · advisor-initiated sessions without a retailer request · screen sharing between retailers · co-browsing of web pages.

## 17. Open Decisions
1. **Which SDK/provider**, and is in-app view streaming with masking actually supported? (Needs a proof-of-concept before committing.)
2. Are sessions recorded? If not, is the "nothing was stored" copy verified?
3. Is the "end-to-end encrypted" claim accurate for the chosen provider? (**Compliance risk if not corrected.**)
4. Exact sensitive-field masking list.
5. Support hours, staffing and who accepts sessions.
6. Session-to-ticket model — reuse `tickets` or build a session store?
7. Maximum session duration and idle timeout.
8. Is the fallback (callback / screen recording) acceptable as the v1 experience if live sharing slips?

---

# CROSS-FEATURE REQUIREMENTS

## A. Shared Components

Build these **once**, in the design system, before the features that consume them. Each one is used by three or more Phase 2 features — building them per-feature is where this phase will leak time.

| Component | Used by | What it must do |
| --- | --- | --- |
| **OTP input** | F1 (Aadhaar, any OTP-capable ID); existing login OTP | 6-box input, OS auto-read, countdown, resend with cooldown, attempt counter, expired/locked/verifying states, masked destination line |
| **Consent sheet** | F1 (KYC consent), F2 (location), F10 (contacts import), F13 (screen share) | Title, what-we-do / what-we-don't bullets, provider named, Agree/Cancel, consent logged with a reason code |
| **Permission handler** | F2 (location), F10 (contacts), F11 (camera for stock), F13 (capture), F4/F6 (camera/gallery) | Pre-prompt explainer, OS prompt, denied state, permanently-denied → Open Settings, never re-fires the OS dialog pointlessly |
| **Product card (compact)** | F7 (request lines), F9 (chat cards), F11 (inventory rows), F8 (catalog entries) | Image, name, pack, price with **KYC price-gating built in**, margin %, quantity/stepper slot, CTA slot. Price gating must live **inside** the component so no feature can accidentally leak a gated price |
| **Product selector sheet** | F4 (return products), F6 (review products), F7 (agent composer), F11 (add item) | Multi-select with quantities capped by a maximum, search, per-row eligibility reason, running summary |
| **Status chip + timeline** | F1 (KYC), F4 (return/refund), F5 (referral), F7 (request), F13 (session) | One vocabulary and one colour mapping for pending / approved / rejected / expired / completed, and a vertical stepper with per-step timestamp and actor |
| **Request card** (expiring action) | F7 (cart request), F3 (action-required inbox items), F11 (delivered-stock prompt) | Title, summary line, live countdown, primary/secondary action, expired read-only state |
| **Review / rating control** | F6 (product review), F13 (session feedback), existing rate-app prompt | Star or emoji scale, optional text, optional media, submitted/edit states |
| **Media uploader** | F4 (return evidence), F6 (review media), F10 (NH) | Multi-file, camera or gallery, thumbnails with remove, per-file progress and per-file retry, size/type limits, compression |
| **Empty / error / retry states** | Every feature | One visual language for empty, error, offline and retry, with a slot for feature-specific copy and CTA |
| **Notification row** | F3 (inbox) | Category icon, title, 2-line body, relative time, unread dot, optional inline CTA + expiry chip |
| **Deep-link router** | F3, F5, F7, F9, F11, F12 | One enumerated route registry shared by app, backend templates and story/notification content; unknown route → graceful fallback, logged |
| **Money/amount formatter** | F5, F7, F8, F10, F11 | ₹ formatting, Indian digit grouping, margin/profit display conventions from the Phase 1 design system (margin green, no arrow; off-% grey) |
| **Offline queue** | F11 (stock updates), F10 (notes), F3 (mark-read) | Queue a mutation, show pending state, sync on reconnect, resolve conflicts predictably |

**Design-system rule:** everything above lands in `design-system.html` with its states documented, and no feature ships a private copy.

---

## B. Feature Dependencies

### B.1 Dependency map

```
                     ┌─────────────────────────────────────────────┐
                     │  EVENT BUS + NOTIFICATION SERVICE (F3)      │
                     │  the spine of Phase 2                       │
                     └─────────────────────────────────────────────┘
        emits ▲            ▲          ▲          ▲          ▲          ▲
              │            │          │          │          │          │
      ┌───────┴───┐ ┌──────┴───┐ ┌────┴────┐ ┌───┴────┐ ┌───┴────┐ ┌───┴────┐
      │ KYC (F1)  │ │Returns   │ │Referral │ │Sales   │ │Inventory│ │Reviews │
      │           │ │(F4)      │ │(F5)     │ │Cart(F7)│ │(F11)    │ │(F6)    │
      └───────────┘ └──────────┘ └─────────┘ └────────┘ └─────────┘ └────────┘
             │             │                      │           │
             │             │                      │           │
   ┌─────────▼───┐  ┌──────▼──────┐        ┌──────▼─────┐ ┌───▼────────┐
   │ Address(F2) │  │ Orders      │        │ Cart /     │ │ My Farmers │
   │ shares      │  │ (Phase 1)   │◄───────┤ Checkout   │ │ (F10)      │
   │ permission  │  │ delivered   │        │ (Phase 1)  │ │ shared     │
   │ component   │  │ lines feed  │        └────────────┘ │ customer   │
   └─────────────┘  │ F4, F6, F11 │                       └────────────┘
                    └─────────────┘
        ┌──────────────────────────────────────────────┐
        │ Krishi AI (F9) consumes almost everything:   │
        │ catalog · orders · wallet · KYC · returns    │
        │ · cart · support escalation                  │
        └──────────────────────────────────────────────┘
        ┌──────────────────────────────────────────────┐
        │ Screen Share (F13) + Chatbot escalation (F9) │
        │ both need the SAME support/ticket backbone   │
        └──────────────────────────────────────────────┘
```

### B.2 Explicit dependencies

| Feature | Depends on | Nature |
| --- | --- | --- |
| **F3 Notification inbox** | F1, F4, F5, F6, F7, F11 + Phase 1 Orders/Wallet/Coins/Schemes | Hard — the inbox is empty without their events |
| **F4 Return flow** | Orders (delivered lines, delivery timestamp), KKD return service, F3 | Hard |
| **F6 Testimonial** | Orders (delivered lines), PDP reviews (Phase 1), KKD review/moderation service, F3 | Hard |
| **F7 Sales cart request** | Cart + pricing + stock (Phase 1), F3, **RLM composer (new)** | Hard — and blocked on the cart contract |
| **F5 Refer & Earn** | Onboarding (attribution), KYC (F1) for the qualifying condition, Wallet/Coins (Phase 1), F3 | Hard |
| **F9 Krishi AI** | Catalog, Orders, Wallet, KYC (F1), Returns (F4), Cart, Support | Hard on all — this is why it sequences late |
| **F11 Inventory** | Orders (delivered lines), Catalog (pack/case data), F10 (shared customer), F3, Cart (reorder) | Hard |
| **F10 My Farmers** | F11 (sales records are the only purchase-history source), F3 (reminders) | Hard |
| **F1 KYC OTP** | External providers, F3 | Hard on providers |
| **F2 Map-first address** | Google Maps SDK + Geocoding + Places, `pincode_map_v2` + index | Medium — blocked on the Maps account, not on app work |
| **F8 Catalog download** | Catalog, price entitlement (Phase 1) | Medium — the most independent Phase 2 feature |
| **F12 Story rail** | Content source decision, deep-link router, analytics | Low |
| **F13 Screen share** | SDK proof-of-concept, support queue/console, F3 | Hard on the SDK and on Support Ops |

### B.3 Shared backbones that more than one feature needs

1. **Event bus + notification service** — F3's core, required by seven features.
2. **Support/ticket backbone** — needed by F9 (escalation) and F13 (sessions). Today `tickets` is unused with NULL routing/SLA. **Build once for both.**
3. **Delivered-order data contract** — F4, F6 and F11 all need "which lines were delivered, when". Define one API, not three.
4. **Customer (farmer) entity** — F10 and F11 must share it.
5. **Price entitlement service** — F7, F8, F9 and the shared product card all need "what price may this retailer see". One server-side authority.
6. **Deep-link route registry** — F3, F5, F7, F9, F11, F12.

---

## C. Recommended Build Sequence

Sequenced on dependencies, backend readiness, shared components, user impact and complexity — not preference. Each wave is a shippable increment.

### Wave 0 — Decisions and foundations (before feature code)
*Rationale: five decisions block estimation on eight features. Nothing here is optional.*
1. **Answer the store-of-record question** — is the Partner App on the Supabase `partner_*` tables, the CRM Mongo/RLM stack, or both? (Blocks F1, F3, F7.)
2. **Event bus + notification service + inbox schema** — the spine (F3 backend).
3. **Shared components** — OTP, consent, permission, product card with price gating, status chip/timeline, media uploader, deep-link registry.
4. **Delivered-order data contract** (feeds F4, F6, F11).
5. **KYC provider evaluation** (F1) and **screen-share SDK proof-of-concept** (F13) started **in parallel as spikes**, because both may invalidate their designs.

### Wave 1 — Quick wins on live data
*Rationale: low dependency, high daily value, exercises the new shared components.*
6. **F2 Map-first shop location & address** — both screens are designed and `pincode_map_v2` is live; the work is the Google Maps Platform contract, the plus-code fallback and the pincode reconciliation. Highest effort-to-value ratio in Phase 2, and it improves every order that follows.
7. **F3 Notification inbox (app side)** — the screen is designed; light it up with Orders + KYC events first.
8. **F12 Story rail hardening** — finish testing, add the kill switch and analytics, ship or hold on the content decision.

### Wave 2 — Order lifecycle completion
*Rationale: returns and reviews are the same data contract and the same components, and both are KKD-parity work rather than net-new design.*
9. **F4 Return request flow** — reuse the KKD service; retire the duplicate `return-request.html`.
10. **F6 Testimonial capture (product-level)** — re-anchor to delivered order lines; reuse the KKD review/moderation service.
11. **F11 Inventory tracker** — delivered-order → inventory is the adoption mechanic and shares the same delivered-lines contract. Ledger first, smart features later.
12. **F10 My Farmers** — immediately after F11, sharing the customer entity and sale records.

### Wave 3 — Growth and assisted selling
*Rationale: needs the notification spine (Wave 0) and the cart contract answered; F7 also needs an RLM-side build that must start early in this wave.*
13. **F5 Refer & Earn** — status machine + ledger; attribution decision made in Wave 0.
14. **F7 Sales cart request** — app side is ready; **the RLM composer is the long pole — start it at the beginning of this wave, not the end.**
15. **F8 Product catalog download** — independent, can slot anywhere it fits; placed here because price-entitlement work is already done by F7/F9 preparation.

### Wave 4 — KYC and AI
*Rationale: both are provider-gated and highest-risk; both benefit from everything above existing.*
16. **F1 Supporting ID OTP verification** — ships when the provider contract lands; the DigiLocker-friction improvements (explainer, deterministic return, resume) can ship **earlier and independently** and should.
17. **F9 Krishi AI chatbot** — needs catalog, orders, wallet, KYC, returns, cart and support to all be callable. Launch scope decision (agronomy-first vs everything) is an Open Decision.
18. **F13 Screen share** — ships only if the Wave 0 spike proves in-app streaming with masking; otherwise ship the fallback (callback + screen recording) and defer.

### Sequencing notes
- **F1's friction fixes are separable from F1's OTP.** Do not hold the DigiLocker explainer and resume banner hostage to a provider contract — they are cheap and they recover drop-off now.
- **F9 and F13 share the support backbone.** Whoever builds it first must build it for both.
- **F11 before F10**, always — farmers without purchase history are an empty address book.
- **F7's RLM composer is the single largest non-app build in Phase 2.** If it cannot be resourced, F7 should be deferred rather than shipped half-built, because the app screen alone delivers nothing.

---

## D. Phase 2 Risks

| # | Risk | Features | Impact | Mitigation |
| --- | --- | --- | --- | --- |
| R1 | **Store-of-record ambiguity** — the Supabase `partner_*` tables are built but empty; the live app may be on a different stack entirely | F1, F3, F7 | Estimates unreliable; risk of building against the wrong database | Resolve in Wave 0, in writing, before any backend ticket is opened |
| R2 | **KYC provider entitlement** — in-app Aadhaar OTP may simply not be available to us | F1 | The headline Phase 2 KYC improvement does not happen | Run the provider spike immediately; ship DigiLocker friction fixes regardless so the phase still improves KYC |
| R3 | **Notification architecture built for one row per partner** — no audience/broadcast model, no read timestamp, no TTL | F3 and every emitting feature | Fan-out cost; unmeasurable notification effectiveness; unbounded table growth | Decide the broadcast model and add the missing columns before the inbox goes live |
| R4 | **AI hallucination on agronomy and dosage** | F9 | Crop loss, liability, brand damage | Retrieval-only agronomy, typed response blocks, evaluation suite as a release gate, source line + disclaimer on every agronomy answer |
| R5 | **AI answering money/order questions from model memory** | F9 | Wrong balances and delivery promises given to retailers | Tool-call contract: no price/stock/date/balance/eligibility without an API call in the session log; audit via transcripts |
| R6 | **Screen-share technical feasibility and privacy claims** — "end-to-end encrypted" and "only this app is shared" may not be literally true for the chosen provider | F13 | Compliance exposure from inaccurate in-app claims; feature may not be buildable as designed | Proof-of-concept before commitment; in-app view streaming only; rewrite the privacy copy to match reality; Legal sign-off |
| R7 | **Cart contract conflict** — `partner_cart` is quotation-scoped, which a free-catalog sales request cannot satisfy | F7 | Rework or a second cart system | Settle the cart contract in Wave 0 |
| R8 | **RLM-side builds unresourced** — F7 composer, F4/F6 moderation and approval queues, F13 console all live outside the app | F4, F6, F7, F13 | App screens ship with nothing behind them | Name an owner per RLM-side build at the start of the phase; defer features whose ops side is unfunded |
| R9 | **Location data quality** — Google returns plus codes instead of street addresses across rural India; ~8% of pincodes have missing taluk or null lat; `pincode` is unindexed | F2 | Meaningless addresses on labels, blank fields, wrong district mapping | Plus-code rule (drop the code, keep pincode/district/state + coordinates); `pincode_map_v2` is authoritative for district/state/territory; add the index; log unknown pincodes |
| R10 | **Inventory data accuracy** — unit conversion errors between cases and units | F11, F10 | One wrong auto-add destroys trust in the feature permanently | Confirmation-before-add (never silent), explicit conversion line, editable quantities, full ledger |
| R11 | **Financial consistency** — referral rewards, refunds, coin reversal and cart-request pricing all touch money that Phase 1 already owns | F4, F5, F7 | Double credits, unreversed rewards, disputed refunds | Reuse the Phase 1 wallet/coins ledger; idempotent payouts; explicit reversal rules signed off by Accounts |
| R12 | **Privacy of third-party data** — farmer contacts (F10) and shared screens (F13) involve people who are not our users | F10, F13 | Legal exposure; retailer distrust if data use is unclear | Legal decision on farmer-data use **before** Import Contacts; masking + consent logging for sessions |
| R13 | **Price leakage via the catalog PDF** | F8 | Distributor pricing reaching farmers and competitors | Server-side entitlement, MRP-only share variant as a first-class option, watermarking |
| R14 | **Analytics vacuum** — `app_events` has never received a single row | All | Phase 2 ships with no way to prove any feature worked | Wire telemetry in Wave 0 alongside the event bus; every feature's events listed in this document are part of its definition of done |
| R15 | **Scope compression at the end of the phase** — 13 features, several with net-new ops systems | All | Half-built features shipped | Waves are shippable increments; MH/NH is marked per feature; cut NH items first, never the ops side of a shipped feature |

---

## E. Consolidated Open Decisions

### E.1 Blocking — resolve before development starts

| # | Decision | Owner | Blocks |
| --- | --- | --- | --- |
| 1 | Which stack is the Partner App's store of record — Supabase `partner_*`, CRM Mongo/RLM, or both? | Tech + Product | F1, F3, F7 |
| 2 | Cart contract: is the live cart quotation-scoped (`partner_cart`) or free-catalog? | Tech | F7, F9 |
| 3 | Is in-app **Aadhaar OTP** entitlement obtainable? If not, is DigiLocker acceptable for Phase 2? | Tech + Compliance | F1 |
| 4 | Notification store + broadcast model + required schema additions (category, read_at, priority, entity ref, expiry, audience) | Tech + Product | F3 and 7 emitting features |
| 5 | Does a reusable **KKD return service** and **KKD review/moderation service** exist for Partner App use? | Tech | F4, F6 |
| 6 | Who owns and funds the **RLM-side builds** (F7 composer, return approval queue, review moderation, F13 console)? | Operations + Tech | F4, F6, F7, F13 |
| 7 | Screen-share SDK feasibility (in-app streaming + masking) — proof-of-concept outcome | Tech | F13 |
| 8 | Can Katyayani use retailer-entered **farmer data**? | Legal + Business | F10 (Import Contacts, any RLM visibility) |

### E.2 Business / commercial

9. Referral reward amount, instrument (Wallet ₹ / Coins / credit note), qualifying condition, payout trigger, validity, caps. **(F5)**
10. Referral attribution conflict with RLM-sourced retailers. **(F5 — Operations)**
11. Return window length for B2B orders; non-returnable categories; refund destination; coin reversal on returns. **(F4 — Business + Accounts)**
12. Single reward policy for product reviews vs story testimonials. **(F6)**
13. Cart-request expiry duration, post-expiry price honouring, merge policy, discount/"advisor bonus" authority. **(F7)**
14. Catalog refresh cadence, watermark content, inclusion of out-of-stock SKUs, rate limits. **(F8)**
15. Definitions: "active" farmer, "high value" farmer, "Today's Sales", "Inventory value". **(F10, F11)**
16. Is inventory data visible to RLM/Marketing for demand planning? **(F11 — commercially sensitive)**
17. Support hours, staffing model and who may accept screen-share sessions. **(F13 — Operations)**
18. Notification retention window, push-eligible categories, quiet hours, frequency caps. **(F3)**

### E.3 Product / UX

19. Name-match thresholds and the manual-review band for KYC. **(F1)**
20. Is Voter ID in Phase 2 scope given lookup-only provider coverage? **(F1)**
21. May retailers override auto-filled State/District? **(F2)**
22. Partial acceptance of a cart request in v1. **(F7 — recommended yes)**
23. Review window and edit window durations; are reviews allowed on returned products? **(F6)**
24. Delivered-stock prompt validity window; default min-stock threshold. **(F11)**
25. Farmers without a phone number — allowed? Delete vs archive? **(F10)**
26. Story rail: static content or served; kill switch in scope; expiry/scheduling rules; does the quiz carry a real reward? **(F12)**
27. Krishi AI launch scope — all capabilities at once, or agronomy + product first? **(F9)**

### E.4 Technical

28. Reverse-geocoding approach — provider or nearest-neighbour over `pincode_map_v2.geo`. **(F2)**
29. Approval and timing of the `pincode` index on `pincode_map_v2` (production DB change). **(F2)**
30. `partner_documents` schema change — status enum, rejection reason, `voter_id` value. **(F1)**
31. Deferred deep linking for referral attribution, or manual code entry only? **(F5)**
32. Catalog generation strategy — pre-generated, on-demand, or hybrid; caching model. **(F8)**
33. LLM provider, model, hosting, cost ceiling; session/transcript store; evaluation-suite ownership. **(F9)**
34. Escalation destination for chat and screen share — reuse `tickets` (currently unused, NULL routing) or build a support-session store? **(F9, F13)**
35. Offline mutation queue design shared by inventory, notes and mark-read. **(F10, F11, F3)**
36. Telemetry destination — is `app_events` (0 rows) being adopted, or is there another analytics pipeline? **(All)**

### E.5 Legal / compliance

37. KYC consent text, Aadhaar masking standard, data retention. **(F1)**
38. Printable dosage/application instructions in the catalog and in AI answers — label-compliance position. **(F8, F9)**
39. AI liability disclaimer wording and transcript retention/PII handling. **(F9)**
40. Screen-share recording policy; accuracy of the "end-to-end encrypted" and "only this app is shared" claims; sensitive-field masking list. **(F13)**
41. Retention and deletion policy for farmer personal data; contacts-import consent text. **(F10)**
42. GST requirements on the Sell-to-Farmer invoice. **(F11 — Accounts)**

### E.6 Operations / RLM

43. Who approves returns — RLM, Support, or rules? Is an approval console available? **(F4)**
44. Who moderates product reviews and story testimonials? **(F6)**
45. Territory rules for which agent may raise a cart request for which retailer. **(F7)**
46. Who authors and approves scheme/marketing notifications and story content? **(F3, F12)**
47. Who reviews flagged/fraudulent referrals? **(F5)**
48. Which agronomy corpus is authoritative for Krishi AI, and who signs it off? **(F9)**

---

## Appendix — Prototype screen index for Phase 2

All of it is runnable from one link: **`phase-2.html`** — a feature rail with each feature's flows (live, clickable) and its screen states.

| Feature | Prototype file(s) | Note |
| --- | --- | --- |
| F1 | **`kyc-id-otp.html`** (new — enter ID → OTP → fetched details → verified/pending/failed/locked/duplicate) · `kyc-aadhaar/pan/gst.html`, `rapido-documents.html` | One pattern for every ID; OTP step only where the provider supports it |
| F2 | **`phase-2.html`** — single Phase 2 link: both runnable journeys + all 9 states. Screens: `location-pin.html`, `shop-address-details.html` · legacy: `rapido-shop-details.html`, `add-address.html` | Map-first flow with search, drag-to-move pin, plus-code fallback; `?flow=shop` vs `?flow=address` |
| F3 | `notifications.html` (+ `?state=empty\|loading\|error`) | Inbox wired to cart-request and delivered-stock deep links |
| F4 | **`returns.html`** (new — My Returns list + status timeline, empty/loading/error) · `order-details.html` (KKD-parity return form), `orders.html` · `return-request.html` *(duplicate — retire)* | KKD reference: `kkd-app-revamp/screens/order-details.html`, `refund-status.html` |
| F5 | **`refer.html`** (rebuilt — status machine, per-referral progress, detail sheet, paused/empty) | Reward tied to a delivered first order, stated on screen |
| F6 | **`review-products.html`** (new — eligible delivered lines → rate → submitted → all rated) · `testimonial.html` stays as the separate story programme | Product-level, tied to (retailer, order, product) |
| F7 | `sales-cart-request.html` (+ `?state=changed\|accepted\|declined\|expired`), item in `notifications.html` | Merge summary designed; **RLM composer still does not exist** |
| F8 | **`catalog-download.html`** (new — scope + price version, generating, ready, failed, KYC-locked) | MRP-only share variant and watermark built into the UI |
| F9 | `ai-chatbot.html` (+ `?state=empty\|tool\|noresult\|apifail\|escalate`), `scanner.html` (sibling) | Guardrail states designed: refuses to invent a dose, honest API failure, human handoff |
| F10 | **`farmer-profile.html`** (new — purchases, dues, notes, follow-up, edit) · `my-farmers.html` | Shares one customer record with Inventory |
| F11 | **`inventory-delivered.html`** (new — delivered-stock prompt, partial, added, already, expired, **stock ledger**) · `inventory.html` | The adoption mechanic plus the ledger that explains every count |
| F12 | `home.html` (story rail + viewer, now deep-linkable via `?story=`) | Testing only — see the readiness checklist |
| F13 | `screen-share.html`, `help.html` | Feasibility unproven |

---

*Prepared from the Partner App prototype (`katyayani-partner-app/screens/`), the KKD prototype (`kkd-app-revamp/screens/`), the development plan CSV, and the Katyayani Knowledge Base schema vault (CRM Mongo + Sales-CRM Supabase), 12 Sep 2026. Every backend statement in this document was checked against those sources; everything not found there is marked as an Open Decision rather than assumed.*
