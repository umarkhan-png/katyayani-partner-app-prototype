# Katyayani Partner App — Complete Design Brief

> **Purpose:** Paste this entire file into a new Claude Design project as context (or upload as a file). It contains every design rule, token, pattern, product list, and screen reference that's been established in the HTML prototype so Claude Design can continue polishing from the same foundation.

---

## 1. Project & Team

- **Product:** Katyayani Partner App — B2B commerce app for pesticide/fertilizer retailers (dukaandars) in semi-urban India
- **Company:** Katyayani Organics (katyayanikrishidirect.com)
- **PM:** Umar
- **Tech:** Flutter app, existing backend (no backend changes)
- **Revenue goal:** 20cr → 120cr in 6 months (6× growth) via UX redesign + new features
- **Current prototype:** https://umarkhan-png.github.io/katyayani-partner-app-prototype/
- **Repo:** https://github.com/umarkhan-png/katyayani-partner-app-prototype
- **Status:** Waves 1-4 complete (commerce, discovery, account, smart tools). Onboarding flow currently being polished.

---

## 2. Target User (CRITICAL)

**Design for the pesticide DUKAAN WALA / baniya mindset — NOT a consumer lifestyle app.**

- Middle-aged male shopkeeper in semi-urban India
- Thinks in margins, credit, bulk, and trust — not "lifestyle"
- Reference: IndiaMART / Udaan B2B, NOT Myntra / Nykaa
- Large tap targets, high contrast, simple icons
- Hindi sub-brand names (Chakraveer, Bhannaat, Bhumiraja) are powerful — feel authentic
- Trust signals: "10,000+ दुकानदारों का भरोसा", "Seedhe Manufacturer Se"
- **Margin % = HERO element on product cards**
- **Credit availability = shown prominently**

**NO:** lifestyle photos, women/girls stock imagery, generic stock, quick-commerce vibes.

---

## 3. Design Language

### Primary inspiration: Blinkit "Bolt" patterns + baniya-B2B overrides

We use Blinkit's clean commerce geometry (ADD buttons, sticky cart bar, pastel tiles, product cutouts on white) — but swap Blinkit's **quick-commerce** identity for **B2B agri trust signals**.

### Secondary aesthetic: Myntra-style image-forward sections

Carousels, magazine-mix layouts, bold sale strips — used sparingly on home/PLP for excitement without losing baniya feel.

### Universal language: ENGLISH primary

Hindi appears as secondary/contextual (brand names, trust copy), but UI labels = proper English.

---

## 4. Design Tokens

### Colors

```
Emerald brand           #0E7A4E      (primary, CTAs, active states)
Emerald deep            #005f3b      (sticky cart bar, checkout CTAs)
Emerald dark header     #083D28
Emerald CTA success     #0C831F
Emerald tint bg         #E8F5EB / #F0FDF5 / #F8FFFE

Gold accent             #D4A537      (sale/premium, margin %, badges)
Gold light bg           #FFF8E6
Gold deep text          #8B6914

Text primary            #1C1C1C
Text body               #606060
Text muted              #9E9E9E
Borders                 #EDEDED
Subtle fill             #F8F8F8
Background              #FFFFFF

Danger/notification     #E23744
Deal-of-day gradient    #FF6B35 → #E23744

Pastel category tiles (Blinkit signature):
  Peach #FFE3D3 · Mint #D8F3E3 · Lemon #FFF4C2
  Sky   #D6ECFA · Lavender #E8DFF5 · Rose #FFD9E0 · Sand #F4E7CE
```

### Typography

**Font: Poppins** (400, 500, 600, 700, 800, 900) — NEVER use Manrope, Inter, Gilroy.

```
Grand total (cart)        font-black  (900)   20–22px    — ONLY place
Hero price (card)         font-extrabold (800) 16px
Section titles            font-semibold (600) 14–18px
Card price                font-semibold (600) 14px
Body / subtitle           font-medium (500)   12–13px
Placeholder / metadata    font-normal (400)   10–11px
```

**Hierarchy rule (strict):** Never stack multiple `font-bold` on one card. If all prices are bold, user can't tell final payable amount.

Brand serif (sparingly): `Playfair Display 900` for hero/poster greetings only.

### Shape & Spacing

- Base unit 4px, rhythm 8 / 12 / 16 / 24
- Screen horizontal padding: 16–20px
- Corner radii: **cards 12-16px · buttons 8-12px · pills 999px · inputs 12px · images 8px**
- Cards: NO shadow by default, 1px `#EDEDED` border, `bg-white`
- Key cards only: subtle `box-shadow: 0 6px 20px -8px rgba(0,0,0,.15)`
- Section separation: edge-to-edge tinted backgrounds (not padded cards)

### Icons — OUTLINE ONLY

```html
<svg stroke="#1C1C1C" stroke-width="2" fill="none"
     stroke-linecap="round" stroke-linejoin="round">...</svg>
```

- Single color (dark `#1C1C1C` or brand `#0E7A4E`)
- Flat `#F8F8F8` tile backgrounds
- NEVER filled / colorful / multi-color / emoji-style icons
- Active state: swap stroke to `#0E7A4E` + bold label (no gradient pill)

---

## 5. Signature Component Specs

### ADD button (product cards) — Blinkit-style

```
Size: 56 × 32 px · Radius: 8px
Fill: #F7FFF9 (mint white — NOT solid green)
Border: 1px #0E7A4E
Label: "ADD" Poppins ExtraBold 12px #0E7A4E UPPERCASE +0.4 tracking
On tap → morphs to pill  "– 1 +"  80×32, same border/fill
```

### Primary CTA (full-width, sticky bottom)

```
Full-bleed · 52px tall · Fill: #005f3b · Radius: 0
Text: white ExtraBold 14-15px UPPERCASE
```

### Sticky cart bar (replaces bottom nav once cart > 0)

```
60-64px tall · fill #005f3b · edge-to-edge
Left: "2 items | ₹248" Bold 14 white
Right: "View cart ›" Bold 14 white
```

### Product card (3-col grid)

```
~106 × 196 px · radius 12 · bg white · 1px #EDEDED · 8px padding
Image: 90 × 90, white bg, product PNG cutout
Pack size above name · Name 13 SemiBold 2-line clamp
Price row: ₹ Bold 14  |  MRP 11 strike #9E9E9E  |  ADD button
```

### Product card (featured/rail, Blinkit + margin twist)

```
Width 150-160px · h-[120-130px] image
Subtitle flex-justify: pack size LEFT #606060  |  "Margin X%" RIGHT #D4A537 font-semibold
Rating pill: #03A685 bg, text white 9px
Sold-count pill: #F0FDF5 bg, #0E7A4E/40 border, #0C831F text 8px
```

### Filter / subcategory chips

```
36px tall · padding 12×8 · radius 999
Off: bg #F4F4F4, text #1C1C1C SemiBold 12
On:  bg #E8F5EB, 1px #0E7A4E border, text #0E7A4E SemiBold 12
```

### Pastel category tile

```
72 × 96 px · pastel bg · 56px product cutout · SemiBold 11 label · 4-col grid
```

### Header patterns

- **Sub-pages:** sticky white, 36×36 back circle `border-[#EDEDED]`, title 18px SemiBold, subtitle 10px `#606060`
- **Home:** unified green gradient (`.hero-wrap`) containing status bar, address+coin+bell, search bar, 6 category icons, deal strip, banners. Categories inside green; order tracking is first white tile below.

### Bottom tab nav (4 tabs)

Identical markup across `home`, `explore`, `orders`, `profile`. Outline SVG icons 1.8 stroke, `#9E9E9E` inactive / `#0E7A4E` active. Active shows small `w-8 h-[2.5px] bg-[#0E7A4E] rounded-full` indicator above + `font-semibold` label.

---

## 6. Hard Rules (Dos / Don'ts)

### ✅ ALWAYS
- English primary UI, Hindi for brand/trust
- Outline SVG icons only
- Real Katyayani product names on cards (list below)
- Margin % on product cards (right-aligned in subtitle)
- "Free Delivery on ₹2,000+", "Pakka Bill", "Verified Supplier" B2B trust pills
- `EDD: Tomorrow` / `EDD: 2-3 days` for delivery
- Consistent font sizes across app (strict scale)
- Complete flow screens per feature (not just hero — entry, loading, empty, populated, action, success, error, edge)
- Build ON TOP of existing app — familiar layout, improved on top

### ❌ NEVER
- "10 MIN" / "10 min delivery" / lightning bolt delivery badges (B2B agri = next-day)
- "Express / Quick / Instant delivery" copy
- Countdown timers for delivery
- Lifestyle photos, women/girls imagery, generic stock
- Pure black `#000000` — use `#1C1C1C`
- Filled/colorful/multi-color icons
- Manrope, Inter, Gilroy fonts
- All prices bold (kills hierarchy)
- "API" word in UI — use "Verify Aadhaar" not "Aadhaar API"
- Welcome bonus / promo fluff in onboarding
- Cream backgrounds / glassmorphism / aurora gradients
- Generic placeholder product names ("Product 1")

---

## 7. Real Katyayani Product Catalog (17 SKUs)

All images hosted on Shopify CDN — directly referenceable.

### Insecticides / Pesticides

| Product | Technical | Price | Image |
|---|---|---|---|
| Katyayani Imida | Imidacloprid 30.5% SC | ₹280 | https://katyayanikrishidirect.com/cdn/shop/files/IMIDA_4.webp |
| Katyayani EMA 5 | Emamectin Benzoate 5% SG | ₹296 | https://katyayanikrishidirect.com/cdn/shop/files/Ema_5_new_Mock_0.5x.webp |
| Katyayani Chakraveer | Chlorantraniliprole 18.5% SC | ₹440 | https://katyayanikrishidirect.com/cdn/shop/files/ChakraveerNewMockup.webp |
| Katyayani Chakrawarti | Thiamethoxam 12.6% + Lambda Cyhalothrin 9.5% ZC | ₹358 | https://katyayanikrishidirect.com/cdn/shop/files/Chakrawarti_2.webp |
| Katyayani Triple Attack (Liquid) | V. lecanii + B. bassiana + M. anisopliae | ₹509 | https://katyayanikrishidirect.com/cdn/shop/files/Triple_attack_1_2.webp |
| Katyayani Triple Attack Powder | Same | ₹466 | https://katyayanikrishidirect.com/cdn/shop/files/TripleAttackbox.webp |

### Fungicides / Viricides

| Product | Technical | Price | Image |
|---|---|---|---|
| Katyayani Azodharma | Azoxystrobin 18.2% + Difenoconazole 11.4% SC | ₹310 | https://katyayanikrishidirect.com/cdn/shop/files/AZODHARMA_3.webp |
| Katyayani Antivirus | Viricide (Chilli/Tomato/Brinjal) | ₹327 | https://katyayanikrishidirect.com/cdn/shop/files/AntiVirus_75248f94-8de8-47c9-9592-a7aa49e36eeb.webp |
| Katyayani Antivirus 1+1 Free | Viricide combo | ₹490 | https://katyayanikrishidirect.com/cdn/shop/files/Buy1get1free_2.webp |

### Fertilizers / Nutrients

| Product | Technical | Price | Image |
|---|---|---|---|
| Katyayani NPK 19-19-19 | NPK 19:19:19 water soluble | ₹330 | https://katyayanikrishidirect.com/cdn/shop/files/NPK_19-19-19_Front.webp |
| Katyayani NPK 00:52:34 | Mono Potassium Phosphate | ₹460 | https://katyayanikrishidirect.com/cdn/shop/files/NPK00-52-34Front_a003f055-4bcd-49ed-ab41-c3de4e8cf1ea.webp |
| Katyayani Activated Humic + Fulvic 98 | Humic + Fulvic Acid 98% | ₹376 | https://katyayanikrishidirect.com/cdn/shop/files/Humic_1.jpg |
| Katyayani Humic Acid 800gm 1+1 | Humic Acid combo | ₹724 | https://katyayanikrishidirect.com/cdn/shop/files/Untitled_design_8_1.webp |
| Katyayani Bhumiraja | Mycorrhiza | ₹364 | https://katyayanikrishidirect.com/cdn/shop/files/Bhumiraja_2_1.webp |

### Biostimulants / PGR

| Product | Technical | Price | Image |
|---|---|---|---|
| Katyayani Bhannaat | Biostimulant PGR | ₹334 | https://katyayanikrishidirect.com/cdn/shop/files/Bhannat_2.webp |
| Katyayani Pro Grow | Gibberellic Acid 0.001% | ₹290 | https://katyayanikrishidirect.com/cdn/shop/files/Pro_Grow_2_1__11zon.webp |

**Pack sizes to fabricate:** 250ml / 500ml / 1L (liquids), 500g / 1kg (powders), 25kg bag (fertilizers).
**MRP for price triptych:** ~30-40% above current price.
**Categories in app:** Insecticides · Fungicides · Fertilizers · Biostimulants · Combos · Sprayers · Seeds.

---

## 8. Onboarding Flow (current)

```
splash → language → welcome → login (phone) → OTP
       → profile setup → welcome splash (2s auto)
       → shop details → license upload (MANDATORY, non-skippable)
       → verify identity → complete → home
```

### Verification rules
- **License (pesticide OR fertilizer):** mandatory, non-skippable
- **Supporting ID (required):** pick ONE — Aadhaar / GST / PAN / Voter ID → API verify or manual upload (1-2 days)
- **Extra business proof (optional):** Shop Photo / Bill Book / Visiting Card

### Onboarding principles
- Collect ONLY essential info; everything else goes into profile later
- No "Welcome Bonus" or promo fluff
- Trust-focused copy, not marketing
- Every screen: uniform top nav (same color, button style, height)
- Consistent title alignment across all screens (top-aligned)

---

## 9. Screen Inventory (67 screens — current state)

### Onboarding & Auth
`splash · language · login · otp · role-selection · profile-setup · registration-success · verification-status`
`rapido-welcome · rapido-phone · rapido-otp · rapido-profile · rapido-signup-success · rapido-shop-photo · rapido-license-upload · rapido-license-number · rapido-camera · rapido-camera-preview · rapido-aadhaar-upload · rapido-documents · rapido-complete`

### KYC (separate system)
`kyc · kyc-aadhaar · kyc-license · kyc-gst · kyc-pan · kyc-bank · kyc-shop-photo · pesticide-certificate · shop-details`

### Tab screens (bottom nav — 4)
`home · explore · orders · profile`

### Commerce flow
`categories · search · pdp · cart · checkout · order-success · order-tracking · return-request · sales-cart-request`

### Discovery
`shop-by-disease · scanner · voice-order · ai-chatbot`

### Account & growth
`wallet · vip · credit · credit-activated · leaderboard · target-tracker · community · notifications · refer · training`

### Utilities
`addresses · add-address · settings · language · help · profit-calculator · poster-generator · statement · cash-deposit · pay-advance · farmer-redirect`

---

## 10. Brand Website Reference

From katyayanikrishidirect.com:
- Brand green `#258046` (close enough to our `#0E7A4E` — coexist OK)
- Accent peach `#ffe1da`
- Discount red `#ff3e3e`
- Text `#121212`
- Border radius: 0 (sharp/square — confirms baniya-mindset)
- Wordmark: "Katyayani Krishi Direct"
- Tagline: "Best Online Store for Agriculture Products"

---

## 11. How to use this in Claude Design

1. **Start new project** in claude.ai/design titled "Katyayani Partner App"
2. **Paste this entire brief** as the first message / project context
3. **Additionally import** one of:
   - **Web capture:** `https://umarkhan-png.github.io/katyayani-partner-app-prototype/` — lets Claude Design see actual rendered screens
   - **Codebase reference:** GitHub repo URL `https://github.com/umarkhan-png/katyayani-partner-app-prototype`
   - **File upload:** any specific `.html` screen you want to iterate on
4. **Design system:** after first screen generates, save tokens above as a Design System in Claude Design so every new screen inherits them
5. **When asking for a screen:** always specify device=mobile, 390×780 device frame, and reference ONE of the real product names from section 7

---

## 12. Current polish state (what's done)

- **Waves 1-4 complete:** commerce (pdp, cart, checkout, orders, tracking), discovery (categories, search, shop-by-disease, explore), account (profile, wallet, vip, credit, leaderboard, target-tracker, community, notifications), smart tools (scanner, voice-order, ai-chatbot, profit-calculator, poster-generator), auth (login, splash, verification-status)
- **Onboarding rapido flow:** iteratively polished over 2026-04-13 → 2026-04-17. Latest: Verify Identity screen with chip-based ID selector (Aadhaar/GST/PAN/Voter ID) + required/optional sections.

### What's still rough / WIP
- Deep polish across all 67 screens in Claude Design's visual engine (image fidelity, micro-interactions)
- Empty / loading / error flow states for some secondary features
- Possibly: role-specific entry (retailer vs distributor) flows

---

*End of brief. Save, paste into Claude Design, continue.*
