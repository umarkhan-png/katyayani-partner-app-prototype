/* =========================================================================
   KO.data — deterministic mock analytics dataset for the Partner App.
   Seeded PRNG, so every reload and every page shows the SAME numbers.

   CALIBRATION (one coherent business, "today" = 12 Sep 2026):
     verified partner base  24,800        MAU  9.6K      DAU  ~2.4K
     installs               ~240 / day    orders ~113 / day
     AOV                    ~₹10.4k       GMV  ~₹3.5 Cr / month
     annualised GMV         ~₹41 Cr  →  plan target ₹120 Cr
   Every table below is scaled to that model so cross-page numbers agree.
   Replace each generator with a real API call when the warehouse is ready;
   the shape of every object here is the contract the portal reads.
   ========================================================================= */
(function (global) {
  'use strict';

  /* ---------------- seeded PRNG ---------------- */
  function mulberry(seed) {
    return function () {
      seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
      var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  var rnd = mulberry(20260912);
  function rr(a, b) { return a + rnd() * (b - a); }
  function ri(a, b) { return Math.round(rr(a, b)); }
  function pick(arr) { return arr[Math.floor(rnd() * arr.length)]; }

  /* ---------------- calendar ---------------- */
  var TODAY = new Date(2026, 8, 12);           // 12 Sep 2026
  var N = 210;                                  // days of history
  var DAYS = [];
  for (var i = N - 1; i >= 0; i--) {
    var d = new Date(TODAY); d.setDate(d.getDate() - i);
    DAYS.push(d.toISOString().slice(0, 10));
  }
  function dow(iso) { return new Date(iso + 'T00:00:00').getDay(); }

  /* ---------------- headline base (used by goals + copy) ---------------- */
  var BASE = { verifiedBase: 24800, mau: 9600 };

  /* =======================================================================
     DIMENSIONS
     ======================================================================= */

  // Acquisition channels — attribution supplied by Linkrunner (MMP)
  var CHANNELS = [
    { id: 'fieldqr',   name: 'Field Sales QR',      group: 'Owned',   cpi: 980, share: .215, quality: .93, color: '#0E7A4E', mmp: 'Linkrunner deep link' },
    { id: 'google',    name: 'Google Ads (UAC)',    group: 'Paid',    cpi: 420,  share: .162, quality: .72, color: '#2563EB', mmp: 'Linkrunner ⇄ Google' },
    { id: 'meta',      name: 'Meta Ads',            group: 'Paid',    cpi: 340,  share: .141, quality: .66, color: '#7C5CFF', mmp: 'Linkrunner ⇄ Meta' },
    { id: 'referral',  name: 'Partner Referral',    group: 'Owned',   cpi: 520, share: .128, quality: .96, color: '#D4A537', mmp: 'Linkrunner referral link' },
    { id: 'whatsapp',  name: 'WhatsApp Broadcast',  group: 'Owned',   cpi: 45,   share: .103, quality: .81, color: '#0E9C8F', mmp: 'Linkrunner short link' },
    { id: 'organic',   name: 'Organic / Play Store',group: 'Organic', cpi: 0,   share: .092, quality: .74, color: '#5B6670', mmp: 'Linkrunner organic' },
    { id: 'distpush',  name: 'Distributor Push',    group: 'Owned',   cpi: 140,  share: .058, quality: .88, color: '#E08A1E', mmp: 'Linkrunner deep link' },
    { id: 'youtube',   name: 'YouTube Krishi',      group: 'Paid',    cpi: 560,  share: .047, quality: .58, color: '#E23744', mmp: 'Linkrunner ⇄ Google' },
    { id: 'influencer',name: 'Krishi Influencer',   group: 'Paid',    cpi: 300,  share: .033, quality: .61, color: '#C2410C', mmp: 'Linkrunner custom link' },
    { id: 'untracked', name: 'Direct / Untracked',  group: 'Organic', cpi: 0,   share: .021, quality: .69, color: '#9E9E9E', mmp: 'No attribution' }
  ];

  var STATES = [
    { id: 'MP', name: 'Madhya Pradesh', share: .215, aovIx: 1.10 },
    { id: 'MH', name: 'Maharashtra',    share: .168, aovIx: 1.18 },
    { id: 'UP', name: 'Uttar Pradesh',  share: .144, aovIx: .88 },
    { id: 'RJ', name: 'Rajasthan',      share: .102, aovIx: .95 },
    { id: 'GJ', name: 'Gujarat',        share: .091, aovIx: 1.22 },
    { id: 'KA', name: 'Karnataka',      share: .072, aovIx: 1.07 },
    { id: 'BR', name: 'Bihar',          share: .068, aovIx: .74 },
    { id: 'TG', name: 'Telangana',      share: .054, aovIx: 1.03 },
    { id: 'PB', name: 'Punjab',         share: .049, aovIx: 1.31 },
    { id: 'WB', name: 'West Bengal',    share: .037, aovIx: .81 }
  ];

  var TIERS = [
    { id: 'Bronze',   share: .462, aovIx: .62, color: '#96562A', threshold: '₹0' },
    { id: 'Silver',   share: .276, aovIx: .92, color: '#5B6670', threshold: '₹10,000' },
    { id: 'Gold',     share: .159, aovIx: 1.38, color: '#D4A537', threshold: '₹1,00,000' },
    { id: 'Platinum', share: .071, aovIx: 2.10, color: '#2B5FA8', threshold: '₹4,00,000' },
    { id: 'Diamond',  share: .032, aovIx: 3.45, color: '#5B3FD1', threshold: '₹7,00,000' }
  ];

  var SEGMENTS = [
    { id: 'champion',  name: 'Champions',        desc: 'Ordered ≤14d, ≥6 orders, high GMV',    share: .118, color: '#0E7A4E', action: 'Early access to Distributor pricing + ask for a testimonial' },
    { id: 'loyal',     name: 'Loyal Regulars',   desc: 'Orders every 21–30d, steady basket',   share: .197, color: '#2FA871', action: 'Push scheme bundles to lift AOV' },
    { id: 'potential', name: 'Potential Growers',desc: '2–4 orders, rising basket, <90d old',  share: .164, color: '#2563EB', action: 'Tier-unlock nudge: "₹8k more for Gold"' },
    { id: 'newbie',    name: 'New Partners',     desc: 'Verified <30d, 0–1 orders',            share: .143, color: '#0E9C8F', action: 'Day-3 / Day-7 onboarding drip + first-order coupon' },
    { id: 'sleeping',  name: 'Slipping Away',    desc: 'Was regular, no order 45–75d',         share: .152, color: '#E08A1E', action: 'Win-back: 2× coins + free delivery, ASM call' },
    { id: 'churned',   name: 'Churned',          desc: 'No order >90d, no session >45d',       share: .128, color: '#E23744', action: 'Reactivation WhatsApp + Linkrunner re-engagement deep link' },
    { id: 'browser',   name: 'Window Shoppers',  desc: 'Verified, high PDP views, zero orders', share: .098, color: '#7C5CFF', action: 'Margin-first PDP variant + ₹500 off first case' }
  ];

  var VERSIONS = [
    { id: '4.2.0', share: .412, crashFree: 99.71, label: 'Current', released: '2026-08-24' },
    { id: '4.1.3', share: .268, crashFree: 99.58, label: 'Previous', released: '2026-07-19' },
    { id: '4.1.0', share: .161, crashFree: 99.12, label: 'Old', released: '2026-06-28' },
    { id: '4.0.2', share: .094, crashFree: 98.41, label: 'Old', released: '2026-05-30' },
    { id: '3.9.x', share: .065, crashFree: 96.88, label: 'Force-upgrade', released: '2026-04-11' }
  ];

  /* =======================================================================
     DAILY SERIES  — everything else is derived from this
     ======================================================================= */
  var daily = DAYS.map(function (iso, ix) {
    var t = ix / (N - 1);
    var growth = 0.62 + 0.72 * t;                 // steady growth over 7 months
    var wd = dow(iso);
    var week = (wd === 0 ? 0.74 : wd === 6 ? 0.86 : wd === 1 ? 1.12 : 1.0);
    var season = 1 + 0.18 * Math.sin((ix / N) * Math.PI * 2.1);   // kharif spray season
    var m = growth * week * season * rr(.93, 1.07);

    var installs      = Math.round(186 * m);
    var signupStart   = Math.round(installs * rr(.70, .77));
    var otpDone       = Math.round(signupStart * rr(.83, .89));
    var profileDone   = Math.round(otpDone * rr(.86, .91));
    var docsStart     = Math.round(profileDone * rr(.71, .79));
    var docsSubmit    = Math.round(docsStart * rr(.74, .82));
    var verified      = Math.round(docsSubmit * rr(.77, .85));

    var dau           = Math.round(1845 * growth * week * rr(.96, 1.04));
    var sessions      = Math.round(dau * rr(2.5, 3.1));
    var pdpViews      = Math.round(dau * rr(3.4, 4.3));
    var searches      = Math.round(dau * rr(.78, .96));
    var atc           = Math.round(pdpViews * rr(.038, .047));
    var cartViews     = Math.round(atc * rr(.62, .73));
    var checkoutStart = Math.round(cartViews * rr(.55, .66));
    var orders        = Math.round(checkoutStart * rr(.66, .755));
    var aov           = Math.round(rr(7600, 10200) * (1 + .18 * t));

    return {
      d: iso, installs: installs, signupStart: signupStart, otpDone: otpDone,
      profileDone: profileDone, docsStart: docsStart, docsSubmit: docsSubmit, verified: verified,
      dau: dau, sessions: sessions, pdpViews: pdpViews, searches: searches,
      atc: atc, cartViews: cartViews, checkoutStart: checkoutStart, orders: orders,
      aov: aov, gmv: orders * aov,
      exploreUsers: Math.round(dau * rr(.38, .49)),
      notifSent: Math.round(dau * rr(1.1, 1.5)),
      notifOpen: Math.round(dau * rr(.13, .21)),
      crashes: Math.max(1, Math.round(sessions * rr(.0011, .0031))),
      apiP95: Math.round(rr(410, 920)),
      returns: Math.max(0, Math.round(orders * rr(.016, .033))),
      cancels: Math.max(0, Math.round(orders * rr(.028, .055))),
      spend: Math.round(installs * rr(400, 490)),
      coinsIssued: Math.round(orders * rr(48, 92)),
      coinsRedeemed: Math.round(orders * rr(19, 44))
    };
  });

  function slice(days) { return daily.slice(Math.max(0, daily.length - days)); }
  function prevSlice(days) {
    var end = daily.length - days;
    return daily.slice(Math.max(0, end - days), Math.max(0, end));
  }
  function sum(rows, key) { return rows.reduce(function (a, r) { return a + (r[key] || 0); }, 0); }
  function avg(rows, key) { return rows.length ? sum(rows, key) / rows.length : 0; }

  /* =======================================================================
     REGISTRATION → VERIFICATION FUNNEL
     ======================================================================= */
  function regFunnel(days) {
    var r = slice(days), p = prevSlice(days);
    var defs = [
      ['App install',            'installs',    'Linkrunner install callback',       0],
      ['Splash → Language',      null,          'splash.html → language.html',       .968],
      ['Phone number entered',   'signupStart', 'rapido-phone.html',                 0],
      ['OTP verified',           'otpDone',     'rapido-otp.html · 30s resend',      0],
      ['Name + profile saved',   'profileDone', 'rapido-profile.html',               0],
      ['Shop details saved',     null,          'rapido-shop-details.html',          .924],
      ['Documents started',      'docsStart',   'rapido-documents.html',             0],
      ['License uploaded',       null,          'rapido-license-upload.html',        .886],
      ['Supporting ID uploaded', null,          'rapido-aadhaar-upload.html',        .913],
      ['Verification submitted', 'docsSubmit',  'rapido-verification-pending.html',  0],
      ['Verified & activated',   'verified',    'Ops approval · median 19h',         0],
      ['First order placed',     null,          'Activation moment',                 .48]
    ];
    var out = [], cur = null, curPrev = null;
    defs.forEach(function (D, i) {
      var v, pv;
      if (D[1]) { v = sum(r, D[1]); pv = sum(p, D[1]); }
      else { v = Math.round(cur * D[3]); pv = Math.round(curPrev * D[3]); }
      cur = v; curPrev = pv;
      out.push({ step: D[0], where: D[2], value: v, prev: pv, i: i });
    });
    var top = out[0].value;
    out.forEach(function (s, i) {
      s.pctTop = s.value / top;
      s.pctPrevStep = i === 0 ? 1 : s.value / out[i - 1].value;
      s.dropped = i === 0 ? 0 : out[i - 1].value - s.value;
      s.delta = s.prev ? (s.value - s.prev) / s.prev : 0;
    });
    return out;
  }

  // Document rejection reasons — last 90 days of ops decisions (~1,350 rejections)
  var kycRejects = [
    { reason: 'License photo blurred / unreadable',    n: 379, pct: .281, fix: 'On-device blur detection before upload' },
    { reason: 'License expired',                       n: 251, pct: .186, fix: 'OCR the expiry date, warn inline' },
    { reason: 'Name mismatch with Aadhaar',            n: 215, pct: .159, fix: 'Prefill shop name from license OCR' },
    { reason: 'Wrong document (GST uploaded as licence)', n: 181, pct: .134, fix: 'Per-doc sample image on the upload card' },
    { reason: 'Shop photo without board / signage',    n: 124, pct: .092, fix: 'Camera overlay guide frame' },
    { reason: 'Partial / cropped document',            n: 105, pct: .078, fix: 'Edge-detection auto-crop' },
    { reason: 'Duplicate licence (already onboarded)', n: 66,  pct: .049, fix: 'Dedupe check at license-number step' },
    { reason: 'Other / manual ops note',               n: 29,  pct: .021, fix: '—' }
  ];

  var verifyOps = {
    pendingNow: 412, slaBreach: 68, medianHours: 19.4, p90Hours: 47.2,
    approvedRate: .812, autoApproved: .341, reworkRate: .223, opsHeadcount: 6,
    queue: [
      { bucket: '< 6h', n: 138 }, { bucket: '6–12h', n: 96 },
      { bucket: '12–24h', n: 71 }, { bucket: '24–48h', n: 39 },
      { bucket: '> 48h (SLA breach)', n: 68 }
    ]
  };

  /* =======================================================================
     MMP / ATTRIBUTION — Linkrunner
     ======================================================================= */
  function attribution(days) {
    var r = slice(days), p = prevSlice(days);
    var tI = sum(r, 'installs'), pI = sum(p, 'installs');
    var tO = sum(r, 'orders'), tG = sum(r, 'gmv');
    return CHANNELS.map(function (c) {
      var installs = Math.round(tI * c.share);
      var clicks   = Math.round(installs / rr(.055, .105));
      var prevInst = Math.round(pI * c.share * rr(.86, 1.12));
      var signups  = Math.round(installs * (.58 + c.quality * .24));
      var verified = Math.round(signups * (.52 + c.quality * .30));
      var firstOrd = Math.round(verified * (.40 + c.quality * .34));
      var orders   = Math.round(tO * c.share * (.62 + c.quality * .62));
      var gmv      = Math.round(tG * c.share * (.55 + c.quality * .75));
      var spend    = Math.round(installs * c.cpi);
      // cohort GMV = what THIS window's acquired partners bought in their first 90 days
      var cohortGmv = Math.round(firstOrd * avg(r, 'aov') * (1.6 + c.quality * 1.0));
      return {
        id: c.id, name: c.name, group: c.group, color: c.color, mmp: c.mmp,
        clicks: clicks, installs: installs, prevInstalls: prevInst,
        ctit: Math.round(rr(11, 96)),                       // click → install, minutes
        signups: signups, verified: verified, firstOrd: firstOrd,
        orders: orders, gmv: gmv, spend: spend,
        deferredDeepLink: Math.round(installs * (c.id === 'untracked' ? 0 : rr(.18, .46))),
        fraudBlocked: Math.round(installs * (c.group === 'Paid' ? rr(.021, .073) : rr(0, .006))),
        cpi: spend ? +(spend / installs).toFixed(1) : 0,
        cac: spend && verified ? Math.round(spend / verified) : 0,
        cacFirstOrder: spend && firstOrd ? Math.round(spend / firstOrd) : 0,
        cohortGmv: cohortGmv,
        roas: spend ? +(cohortGmv / spend).toFixed(1) : null,
        mRoas: spend ? +(cohortGmv * .18 / spend).toFixed(2) : null,
        d1: +(rr(.28, .62)).toFixed(3), d7: +(rr(.14, .41)).toFixed(3), d30: +(rr(.07, .28)).toFixed(3),
        quality: c.quality,
        ltv90: Math.round(gmv / Math.max(1, verified) * rr(1.6, 2.4))
      };
    }).sort(function (a, b) { return b.installs - a.installs; });
  }

  // campaign-level view — last 90 days (installs total ≈ 21k)
  var campaigns = [
    { name: 'KHARIF-2026-MP-Retailer',       ch: 'google',    installs: 3184, cac: 412, roas: 6.8,  status: 'Live',   link: 'lnkrn.app/kh26mp' },
    { name: 'Meta-Lookalike-Dukaan-3pct',    ch: 'meta',      installs: 2610, cac: 468, roas: 4.9,  status: 'Live',   link: 'lnkrn.app/mlk3' },
    { name: 'Field-ASM-QR-Indore-Cluster',   ch: 'fieldqr',   installs: 4180, cac: 288, roas: 9.4,  status: 'Live',   link: 'lnkrn.app/qr-indr' },
    { name: 'Refer-a-Dukaan (in-app)',       ch: 'referral',  installs: 2480, cac: 204, roas: 11.4, status: 'Live',   link: 'lnkrn.app/ref/{id}' },
    { name: 'WA-Reactivation-Sleeping-45d',  ch: 'whatsapp',  installs: 1840, cac: 38,  roas: 9.1,  status: 'Live',   link: 'lnkrn.app/wa-r45' },
    { name: 'Organic / Play Store listing',  ch: 'organic',   installs: 1920, cac: 0,   roas: null, status: 'Live',   link: '—' },
    { name: 'Distributor-Onboard-Push',      ch: 'distpush',  installs: 1210, cac: 96,  roas: 8.2,  status: 'Live',   link: 'lnkrn.app/dist' },
    { name: 'YT-Krishi-Gyan-Preroll',        ch: 'youtube',   installs: 986,  cac: 688, roas: 2.1,  status: 'Paused', link: 'lnkrn.app/yt-kg' },
    { name: 'Influencer-Kisan-Mitra-Set1',   ch: 'influencer',installs: 692,  cac: 512, roas: 2.8,  status: 'Review', link: 'lnkrn.app/km1' },
    { name: 'Google-Competitor-Keyword',     ch: 'google',    installs: 604,  cac: 742, roas: 1.6,  status: 'Paused', link: 'lnkrn.app/gck' },
    { name: 'Meta-Retarget-CartDrop-7d',     ch: 'meta',      installs: 418,  cac: 288, roas: 7.4,  status: 'Live',   link: 'lnkrn.app/mrc7' }
  ];

  // deep links / deferred deep links — last 90 days
  var deepLinks = [
    { path: '/onboarding/qr/{asmId}',     opens: 6840, installs: 4180, orders: 1918, cvr: .280, note: 'Field QR · best quality' },
    { path: '/refer/{partnerId}',         opens: 8420, installs: 2480, orders: 742,  cvr: .088, note: 'Referral · deferred deep link' },
    { path: '/pdp/katyayani-imida',       opens: 9840, installs: 1104, orders: 918,  cvr: .093, note: 'Top PDP deep link' },
    { path: '/cart',                      opens: 5210, installs: 418,  orders: 604,  cvr: .116, note: 'Cart-drop retargeting' },
    { path: '/scheme/kharif-bonanza',     opens: 4880, installs: 612,  orders: 486,  cvr: .100, note: 'Scheme landing' },
    { path: '/shop-by-disease/leaf-curl', opens: 3240, installs: 384,  orders: 296,  cvr: .091, note: 'Problem-led entry' },
    { path: '/explore/profit-calculator', opens: 2610, installs: 218,  orders: 96,   cvr: .037, note: 'Tool-led acquisition' },
    { path: '/order/{orderId}/track',     opens: 7180, installs: 24,   orders: 0,    cvr: 0,    note: 'Transactional only' }
  ];

  var sdkHealth = {
    provider: 'Linkrunner', sdkVersion: '2.4.1', latestVersion: '2.5.0',
    androidCoverage: .987, iosCoverage: .942,
    initSuccess: .9962, avgInitMs: 184,
    eventsTracked: 42, eventsFiring: 39,
    eventsMissing: ['checkout_gst_added', 'distributor_price_unlocked', 'testimonial_submitted'],
    lastSync: '2026-09-12 08:41 IST',
    s2sPostbacks: { configured: 6, healthy: 5, failing: ['Meta CAPI — 3.1% 400s on the purchase event'] },
    dedupWindowDays: 7, attributionModel: 'Last non-direct click · 7d click / 1d view',
    fraudBlocked90d: 742,
    fraudRules: ['Click flood', 'Install hijack', 'Emulator / rooted', 'CTIT < 10s', 'Duplicate device ID']
  };

  // the tracking plan the app must implement for the portal to stay honest
  var trackingPlan = [
    { ev: 'app_install',              owner: 'Linkrunner SDK', stage: 'Acquisition',  status: 'live',    props: 'channel, campaign, adgroup, deep_link, ctit' },
    { ev: 'app_open',                 owner: 'App',            stage: 'Engagement',   status: 'live',    props: 'session_id, app_version, is_first_open' },
    { ev: 'language_selected',        owner: 'App',            stage: 'Onboarding',   status: 'live',    props: 'language' },
    { ev: 'otp_verified',             owner: 'App',            stage: 'Onboarding',   status: 'live',    props: 'phone_hash, attempts, resend_count' },
    { ev: 'shop_details_saved',       owner: 'App',            stage: 'Onboarding',   status: 'live',    props: 'state, district, shop_type' },
    { ev: 'document_uploaded',        owner: 'App',            stage: 'Verification', status: 'live',    props: 'doc_type, retry_count, blur_score' },
    { ev: 'verification_submitted',   owner: 'App',            stage: 'Verification', status: 'live',    props: 'docs_count, time_to_submit_s' },
    { ev: 'verification_approved',    owner: 'Backend',        stage: 'Verification', status: 'live',    props: 'tat_hours, auto_approved, ops_id' },
    { ev: 'verification_rejected',    owner: 'Backend',        stage: 'Verification', status: 'live',    props: 'reason_code, doc_type' },
    { ev: 'search_performed',         owner: 'App',            stage: 'Discovery',    status: 'live',    props: 'query, results_count, is_zero_result' },
    { ev: 'pdp_viewed',               owner: 'App',            stage: 'Discovery',    status: 'live',    props: 'sku, entry_path, margin_pct, is_distributor_price' },
    { ev: 'scanner_diagnosis_shown',  owner: 'App',            stage: 'Explore',      status: 'live',    props: 'crop, disease, confidence, suggested_skus' },
    { ev: 'explore_tool_opened',      owner: 'App',            stage: 'Explore',      status: 'live',    props: 'tool_id, entry_point' },
    { ev: 'add_to_cart',              owner: 'App',            stage: 'Cart',         status: 'live',    props: 'sku, cases, unit_price, margin_pct' },
    { ev: 'distributor_price_unlocked', owner: 'App',          stage: 'Cart',         status: 'missing', props: 'unlock_condition, cart_value, weight_kg' },
    { ev: 'checkout_started',         owner: 'App',            stage: 'Checkout',     status: 'live',    props: 'cart_value, items, payment_options' },
    { ev: 'checkout_gst_added',       owner: 'App',            stage: 'Checkout',     status: 'missing', props: 'gst_present, skipped' },
    { ev: 'order_placed',             owner: 'App',            stage: 'Checkout',     status: 'live',    props: 'order_id, value, payment_method, coupon, scheme' },
    { ev: 'order_delivered',          owner: 'Backend',        stage: 'Fulfilment',   status: 'live',    props: 'tat_days, courier, cod_collected' },
    { ev: 'return_requested',         owner: 'App',            stage: 'Fulfilment',   status: 'live',    props: 'order_id, reason_code' },
    { ev: 'coins_earned',             owner: 'Backend',        stage: 'Loyalty',      status: 'live',    props: 'coins, source, tier' },
    { ev: 'coins_redeemed',           owner: 'App',            stage: 'Loyalty',      status: 'live',    props: 'coins, order_id' },
    { ev: 'referral_link_shared',     owner: 'App',            stage: 'Loyalty',      status: 'live',    props: 'channel, linkrunner_url' },
    { ev: 'testimonial_submitted',    owner: 'App',            stage: 'Engagement',   status: 'missing', props: 'media_type, duration_s' },
    { ev: 'push_opened',              owner: 'App',            stage: 'Engagement',   status: 'live',    props: 'campaign_id, deep_link' },
    { ev: 'screen_view',              owner: 'App',            stage: 'Journey',      status: 'live',    props: 'screen, previous_screen, dwell_ms' },
    { ev: 'rage_click',               owner: 'App',            stage: 'Journey',      status: 'live',    props: 'screen, element, clicks_in_2s' },
    { ev: 'app_error',                owner: 'App',            stage: 'Health',       status: 'live',    props: 'code, endpoint, screen, app_version' }
  ];

  /* =======================================================================
     PRODUCT DISCOVERY — real Katyayani catalogue
     ======================================================================= */
  var products = [
    { sku: 'KT-IMID-30', name: 'Katyayani Imida',                 cat: 'Insecticide',     price: 280, img: 'IMIDA_4.webp' },
    { sku: 'KT-EMA5',    name: 'Katyayani EMA 5',                 cat: 'Insecticide',     price: 296, img: 'Ema_5_new_Mock_0.5x.webp' },
    { sku: 'KT-CHKV',    name: 'Katyayani Chakraveer',            cat: 'Insecticide',     price: 440, img: 'ChakraveerNewMockup.webp' },
    { sku: 'KT-CHKW',    name: 'Katyayani Chakrawarti',           cat: 'Insecticide',     price: 358, img: 'Chakrawarti_2.webp' },
    { sku: 'KT-TA-LQ',   name: 'Katyayani Triple Attack (Liquid)',cat: 'Bio-Insecticide', price: 509, img: 'Triple_attack_1_2.webp' },
    { sku: 'KT-TA-PW',   name: 'Katyayani Triple Attack Powder',  cat: 'Bio-Insecticide', price: 466, img: 'TripleAttackbox.webp' },
    { sku: 'KT-AZOD',    name: 'Katyayani Azodharma',             cat: 'Fungicide',       price: 310, img: 'AZODHARMA_3.webp' },
    { sku: 'KT-ANTV',    name: 'Katyayani Antivirus',             cat: 'Viricide',        price: 327, img: 'AntiVirus.webp' },
    { sku: 'KT-ANTV-11', name: 'Katyayani Antivirus 1+1 Free',    cat: 'Combo',           price: 490, img: 'Buy1get1free_2.webp' },
    { sku: 'KT-NPK-191', name: 'Katyayani NPK 19-19-19',          cat: 'Fertilizer',      price: 330, img: 'NPK_19-19-19_Front.webp' },
    { sku: 'KT-NPK-005', name: 'Katyayani NPK 00:52:34',          cat: 'Fertilizer',      price: 460, img: 'NPK00-52-34Front.webp' },
    { sku: 'KT-HUM-98',  name: 'Katyayani Humic + Fulvic 98',     cat: 'Fertilizer',      price: 376, img: 'Humic_1.jpg' },
    { sku: 'KT-HUM-11',  name: 'Katyayani Humic Acid 800g 1+1',   cat: 'Combo',           price: 724, img: 'Untitled_design_8_1.webp' },
    { sku: 'KT-BHUM',    name: 'Katyayani Bhumiraja',             cat: 'Bio-Fertilizer',  price: 364, img: 'Bhumiraja_2_1.webp' },
    { sku: 'KT-BHAN',    name: 'Katyayani Bhannaat',              cat: 'Biostimulant',    price: 334, img: 'Bhannat_2.webp' },
    { sku: 'KT-PROG',    name: 'Katyayani Pro Grow',              cat: 'PGR',             price: 290, img: 'Pro_Grow_2_1__11zon.webp' }
  ];

  // fixed per-SKU weights so the split is stable across pages
  var SKU_W = [2.42, 1.86, 2.10, 1.64, 0.92, 0.78, 1.72, 1.34, 1.18, 2.28, 1.02, 1.48, 0.86, 0.94, 1.26, 0.74];

  function skuPerf(days) {
    var r = slice(days);
    var totalPdp = sum(r, 'pdpViews'), totalOrd = sum(r, 'orders'), totalGmv = sum(r, 'gmv');
    var ws = SKU_W.reduce(function (a, b) { return a + b; }, 0);
    var seed = mulberry(4242);
    return products.map(function (p, i) {
      var sh = SKU_W[i] / ws;
      var views = Math.round(totalPdp * sh);
      var atcR = .028 + seed() * .042;
      var atc = Math.round(views * atcR);
      return {
        sku: p.sku, name: p.name, cat: p.cat, price: p.price, img: p.img,
        views: views, atc: atc, atcRate: atcR,
        units: Math.round(atc * (1.8 + seed() * 3.4)),
        orders: Math.round(totalOrd * sh * (.8 + seed() * .5)),
        gmv: Math.round(totalGmv * sh * (.82 + seed() * .38)),
        margin: +(.18 + seed() * .2).toFixed(3),
        repeatRate: +(.22 + seed() * .39).toFixed(3),
        stockOutDays: Math.round(seed() * 9),
        returnRate: +(.004 + seed() * .037).toFixed(3),
        distUnlockShare: +(.08 + seed() * .34).toFixed(3),
        trend: +(-.28 + seed() * .74).toFixed(3)
      };
    }).sort(function (a, b) { return b.gmv - a.gmv; });
  }

  // search terms — scaled to ~62k searches / 30 days
  var searchTerms = [
    { q: 'imida',          n: 9184, ctr: .612, zero: false, conv: .118, results: 6 },
    { q: 'npk 19 19 19',   n: 7280, ctr: .588, zero: false, conv: .142, results: 4 },
    { q: 'sundi ki dawa',  n: 6260, ctr: .214, zero: false, conv: .038, results: 14 },
    { q: 'chakraveer',     n: 5320, ctr: .706, zero: false, conv: .186, results: 2 },
    { q: 'humic acid',     n: 4628, ctr: .564, zero: false, conv: .121, results: 5 },
    { q: 'illi ki dawai',  n: 4096, ctr: .188, zero: true,  conv: .021, results: 0 },
    { q: 'safed makhi',    n: 3542, ctr: .241, zero: false, conv: .044, results: 8 },
    { q: 'sprayer pump',   n: 3264, ctr: .062, zero: true,  conv: .004, results: 0 },
    { q: 'jhulsa rog',     n: 2852, ctr: .203, zero: false, conv: .036, results: 6 },
    { q: 'tomato ke liye', n: 2510, ctr: .176, zero: true,  conv: .018, results: 0 },
    { q: 'bhannaat',       n: 2252, ctr: .684, zero: false, conv: .172, results: 1 },
    { q: 'seeds hybrid',   n: 2170, ctr: .048, zero: true,  conv: .002, results: 0 },
    { q: 'antivirus chilli', n: 1968, ctr: .531, zero: false, conv: .108, results: 3 },
    { q: 'weedicide',      n: 1786, ctr: .071, zero: true,  conv: .006, results: 0 },
    { q: 'mahogany',       n: 470,  ctr: .012, zero: true,  conv: 0,    results: 0 }
  ];

  // PDP views by category — scaled to ~275k PDP views / 30 days
  var categories = [
    { name: 'Insecticides',   views: 74900, atc: .048, gmv: 10420000, skus: 42 },
    { name: 'Fungicides',     views: 55400, atc: .042, gmv:  7180000, skus: 31 },
    { name: 'Fertilizers',    views: 50400, atc: .056, gmv:  8620000, skus: 28 },
    { name: 'Biostimulants',  views: 32300, atc: .038, gmv:  3740000, skus: 19 },
    { name: 'Combos',         views: 25000, atc: .068, gmv:  4880000, skus: 12 },
    { name: 'Bio-Pesticides', views: 16900, atc: .032, gmv:  2040000, skus: 14 },
    { name: 'PGR',            views: 12500, atc: .035, gmv:  1480000, skus: 9 },
    { name: 'Sprayers',       views: 6800,  atc: .018, gmv:   310000, skus: 4 }
  ];

  var discoveryPaths = [
    { name: 'Home shelf → PDP',           share: .284, conv: .048, note: 'Recently bought + Top margin shelves' },
    { name: 'Search → PDP',               share: .213, conv: .062, note: 'Highest intent' },
    { name: 'Category → PDP',             share: .168, conv: .041, note: 'categories.html' },
    { name: 'Shop by Problem → PDP',      share: .112, conv: .074, note: 'Best conversion path' },
    { name: 'Disease Scanner → PDP',      share: .068, conv: .088, note: 'Camera-led — small but deadly' },
    { name: 'Banner / Scheme → PDP',      share: .061, conv: .031, note: 'Low intent, good for awareness' },
    { name: 'Quick Order (voice/photo)',  share: .048, conv: .162, note: 'Power-user path' },
    { name: 'Reorder → Cart (skips PDP)', share: .046, conv: .284, note: 'Direct-to-cart' }
  ];

  /* =======================================================================
     CART → CHECKOUT → ORDER
     ======================================================================= */
  function commerceFunnel(days) {
    var r = slice(days), p = prevSlice(days);
    var steps = [
      ['PDP viewed',            'pdpViews',      'pdp.html'],
      ['Added to cart',         'atc',           'ADD / case stepper'],
      ['Cart viewed',           'cartViews',     'cart.html'],
      ['Checkout started',      'checkoutStart', 'checkout.html'],
      ['Address confirmed',     null,            'addresses.html', .914],
      ['Payment method chosen', null,            'COD / Prepaid / Credit', .872],
      ['Order placed',          'orders',        'order-success.html']
    ];
    var out = [], cur = null, cp = null;
    steps.forEach(function (s, i) {
      var v, pv;
      if (s[1]) { v = sum(r, s[1]); pv = sum(p, s[1]); }
      else { v = Math.round(cur * s[3]); pv = Math.round(cp * s[3]); }
      cur = v; cp = pv;
      out.push({ step: s[0], where: s[2], value: v, prev: pv, i: i });
    });
    var top = out[0].value;
    out.forEach(function (s, i) {
      s.pctTop = s.value / top;
      s.pctPrevStep = i === 0 ? 1 : s.value / out[i - 1].value;
      s.dropped = i === 0 ? 0 : out[i - 1].value - s.value;
      s.delta = s.prev ? (s.value - s.prev) / s.prev : 0;
    });
    return out;
  }

  var cartDropReasons = [
    { reason: 'Waiting for farmer confirmation',       pct: .224, signal: 'Session ends on cart, returns in 2–4 days', fix: 'Saved-cart reminder push at T+18h' },
    { reason: 'Below free-delivery threshold',         pct: .186, signal: 'Cart ₹1.8k–₹4.9k, exits at the delivery line', fix: 'Show "₹X more for free delivery" on cart' },
    { reason: 'Distributor price not unlocked',        pct: .148, signal: 'Views the unlock bar, does not add cases', fix: 'Suggest the exact SKU mix that hits the unlock' },
    { reason: 'Cash / credit limit not enough',        pct: .132, signal: 'Opens credit.html from checkout', fix: 'Pre-approve a credit line before checkout' },
    { reason: 'Comparing with local distributor price',pct: .116, signal: 'Opens price-match.html', fix: 'Surface Price Match Guarantee on the cart' },
    { reason: 'GST prompt friction',                   pct: .078, signal: 'Drops at the GST modal', fix: 'Make GST truly skippable and remember the choice' },
    { reason: 'Out of stock on a line item',           pct: .062, signal: 'Stock error toast', fix: 'Real-time stock on ADD, not at checkout' },
    { reason: 'Payment failure / gateway',             pct: .054, signal: 'error-payment-failed.html', fix: 'Auto-retry plus an alternate PSP' }
  ];

  var payments = [
    { m: 'COD (cash on delivery)', share: .412, success: .984, aov: 8940,  color: '#D4A537' },
    { m: 'UPI',                    share: .268, success: .942, aov: 10820, color: '#0E7A4E' },
    { m: 'Katyayani Credit',       share: .148, success: .976, aov: 21400, color: '#2563EB' },
    { m: 'Wallet + Coins',         share: .086, success: .991, aov: 7240,  color: '#7C5CFF' },
    { m: 'Net banking / RTGS',     share: .054, success: .908, aov: 48600, color: '#0E9C8F' },
    { m: 'Card',                   share: .032, success: .874, aov: 12140, color: '#E23744' }
  ];

  var schemesPerf = [
    { name: 'Kharif Bonanza — 10 cases',   enrolled: 2180, completed: 804,  gmvLift: .184, coinsOut: 108000 },
    { name: 'Buy 5 Imida get 1 free',      enrolled: 1610, completed: 1086, gmvLift: .126, coinsOut: 0 },
    { name: '₹50k in 30 days → Gold tier', enrolled: 1064, completed: 296,  gmvLift: .312, coinsOut: 59200 },
    { name: 'Humic 1+1 combo push',        enrolled: 996,  completed: 752,  gmvLift: .092, coinsOut: 24800 },
    { name: 'First order ₹500 off',        enrolled: 3320, completed: 1918, gmvLift: .044, coinsOut: 0 }
  ];

  var coupons = [
    { code: 'KHARIF500', used: 2180, gmv: 21400000, discount: 1090000, incremental: .62 },
    { code: 'NEWDUKAAN', used: 1240, gmv:  9180000, discount:  620000, incremental: .81 },
    { code: 'WAPAS10',   used: 620,  gmv:  5240000, discount:  524000, incremental: .74 },
    { code: 'COINS2X',   used: 540,  gmv:  6840000, discount:       0, incremental: .58 },
    { code: 'FREEDEL',   used: 430,  gmv:  2610000, discount:   64500, incremental: .34 }
  ];

  /* =======================================================================
     FULFILMENT — last 90 days (~9,400 orders)
     ======================================================================= */
  var orderStatus = [
    { s: 'Delivered',      n: 7180, color: '#0E7A4E' },
    { s: 'In transit',     n: 820,  color: '#2563EB' },
    { s: 'Packed',         n: 410,  color: '#0E9C8F' },
    { s: 'Confirmed',      n: 290,  color: '#7C5CFF' },
    { s: 'Cancelled',      n: 460,  color: '#E23744' },
    { s: 'Returned / RTO', n: 240,  color: '#E08A1E' }
  ];

  var tat = [
    { bucket: 'Same day', n: 318 }, { bucket: 'Next day', n: 2410 },
    { bucket: '2 days',   n: 2880 }, { bucket: '3 days',   n: 1420 },
    { bucket: '4–5 days', n: 682 },  { bucket: '> 5 days',  n: 290 }
  ];

  var returnReasons = [
    { r: 'Farmer changed mind after order', pct: .238 },
    { r: 'Wrong pack size ordered',         pct: .196 },
    { r: 'Damaged in transit (leakage)',    pct: .172 },
    { r: 'Wrong SKU delivered',             pct: .134 },
    { r: 'Batch expiry under 6 months',     pct: .108 },
    { r: 'Price dispute / found cheaper',   pct: .086 },
    { r: 'Other',                           pct: .066 }
  ];

  var cancelReasons = [
    { r: 'COD not ready when courier came',                 pct: .284 },
    { r: 'Partner cancelled — stock came from distributor', pct: .221 },
    { r: 'Address / pincode not serviceable',               pct: .164 },
    { r: 'Out of stock after order',                        pct: .138 },
    { r: 'Payment failed twice',                            pct: .104 },
    { r: 'Duplicate order',                                 pct: .089 }
  ];

  /* =======================================================================
     EXPLORE FEATURE ANALYTICS — the 13 real explore.html tiles
     users = monthly active users of that tool (MAU of the app is 9.6K)
     ======================================================================= */
  var tools = [
    { id: 'aichat',     name: 'Krishi AI Chat',    screen: 'ai-chatbot.html',        icon: 'chat',  users: 3180, sessions: 8904, mins: 5.1, d30: .368, attrOrders: 108, attrGmv: 1090000, nps: 58, crash: .0034, adoptTrend: .418 },
    { id: 'profitcalc', name: 'Profit Calculator', screen: 'profit-calculator.html', icon: 'calc',  users: 2840, sessions: 6816, mins: 2.4, d30: .412, attrOrders: 128, attrGmv: 1580000, nps: 71, crash: .0008, adoptTrend: .242 },
    { id: 'disease',    name: 'Shop by Problem',   screen: 'shop-by-disease.html',   icon: 'leaf',  users: 2610, sessions: 5742, mins: 2.1, d30: .308, attrOrders: 154, attrGmv: 1900000, nps: 66, crash: .0006, adoptTrend: .092 },
    { id: 'scanner',    name: 'Disease Scanner',   screen: 'scanner.html',           icon: 'scan',  users: 1840, sessions: 4048, mins: 3.8, d30: .284, attrOrders: 86, attrGmv: 1100000, nps: 62, crash: .0021, adoptTrend: .186 },
    { id: 'community',  name: 'Community',         screen: 'community.html',         icon: 'globe', users: 1620, sessions: 4050, mins: 6.4, d30: .262, attrOrders: 52,  attrGmv:  480000, nps: 55, crash: .0011, adoptTrend: .118 },
    { id: 'poster',     name: 'Poster Generator',  screen: 'poster-generator.html',  icon: 'image', users: 1180, sessions: 2360, mins: 4.2, d30: .224, attrOrders: 64,  attrGmv:  620000, nps: 74, crash: .0018, adoptTrend: .486 },
    { id: 'training',   name: 'Training Hub',      screen: 'training.html',          icon: 'play',  users: 1040, sessions: 2080, mins: 8.2, d30: .196, attrOrders: 42,  attrGmv:  380000, nps: 72, crash: .0005, adoptTrend: .074 },
    { id: 'farmers',    name: 'My Farmers',        screen: 'my-farmers.html',        icon: 'users', users: 980,  sessions: 3332, mins: 3.1, d30: .446, attrOrders: 72, attrGmv: 920000, nps: 69, crash: .0009, adoptTrend: .164 },
    { id: 'quickorder', name: 'Quick Order',       screen: 'voice-order.html',       icon: 'mic',   users: 920,  sessions: 3220, mins: 1.6, d30: .584, attrOrders: 186, attrGmv: 3100000, nps: 78, crash: .0012, adoptTrend: .312 },
    { id: 'inventory',  name: 'My Inventory',      screen: 'inventory.html',         icon: 'box',   users: 740,  sessions: 2590, mins: 4.8, d30: .512, attrOrders: 96, attrGmv: 1420000, nps: 64, crash: .0014, adoptTrend: .208 },
    { id: 'pricematch', name: 'Price Match',       screen: 'price-match.html',       icon: 'tag',   users: 620,  sessions: 1054, mins: 2.2, d30: .234, attrOrders: 78,  attrGmv: 1180000, nps: 59, crash: .0007, adoptTrend: .284 },
    { id: 'testimonial',name: 'Testimonial Studio',screen: 'testimonial.html',       icon: 'mic2',  users: 240,  sessions: 360,  mins: 5.6, d30: .142, attrOrders: 12,  attrGmv:  140000, nps: 68, crash: .0026, adoptTrend: .624 },
    { id: 'transfer',   name: 'Partner Transfer',  screen: 'partner-transfer.html',  icon: 'swap',  users: 210,  sessions: 504,  mins: 2.8, d30: .188, attrOrders: 24,  attrGmv:  360000, nps: 51, crash: .0042, adoptTrend: -.064 }
  ];

  var exploreFunnels = {
    scanner: [
      { step: 'Opened Explore hub',        v: 7420 }, { step: 'Tapped Disease Scanner', v: 1840 },
      { step: 'Camera permission granted', v: 1512 }, { step: 'Photo captured',         v: 1248 },
      { step: 'Diagnosis shown',           v: 1146 }, { step: 'Tapped suggested product', v: 225 },
      { step: 'Added to cart',             v: 126 },  { step: 'Order placed',           v: 86 }
    ],
    quickorder: [
      { step: 'Opened Quick Order',        v: 3220 }, { step: 'Voice or photo input given', v: 2528 },
      { step: 'Items parsed correctly',    v: 2110 }, { step: 'Cases / qty adjusted',   v: 1752 },
      { step: 'Cart opened',               v: 1344 }, { step: 'Order placed',           v: 186 }
    ],
    profitcalc: [
      { step: 'Opened Profit Calculator',  v: 6816 }, { step: 'Selected a product',     v: 5668 },
      { step: 'Entered selling price',     v: 4662 }, { step: 'Saw the margin result',  v: 4232 },
      { step: 'Tapped "Order this"',       v: 560 },  { step: 'Order placed',           v: 128 }
    ],
    aichat: [
      { step: 'Opened Krishi AI Chat',     v: 8904 }, { step: 'Asked at least one question', v: 7174 },
      { step: 'Rated the answer helpful',  v: 4896 }, { step: 'Tapped a product in the answer', v: 630 },
      { step: 'Added to cart',             v: 250 },  { step: 'Order placed',           v: 108 }
    ],
    disease: [
      { step: 'Opened Shop by Problem',    v: 5742 }, { step: 'Picked a crop',          v: 4880 },
      { step: 'Picked a problem / pest',   v: 4104 }, { step: 'Saw product list',       v: 3860 },
      { step: 'Opened a PDP',              v: 800 },  { step: 'Added to cart',          v: 236 },
      { step: 'Order placed',              v: 154 }
    ]
  };

  var aiTopics = [
    { t: 'Which dawa for this pest?',   n: 3240, resolved: .82, toOrder: .118 },
    { t: 'Dosage / per-acre quantity',  n: 2486, resolved: .91, toOrder: .064 },
    { t: 'My margin on this product',   n: 1668, resolved: .78, toOrder: .142 },
    { t: 'Order / delivery status',     n: 1464, resolved: .88, toOrder: .012 },
    { t: 'Licence & verification help', n: 1122, resolved: .64, toOrder: .008 },
    { t: 'Mixing compatibility',        n: 926,  resolved: .71, toOrder: .086 },
    { t: 'Scheme / coins questions',    n: 780,  resolved: .84, toOrder: .048 },
    { t: 'Complaint / escalation',      n: 476,  resolved: .52, toOrder: .004 }
  ];

  /* =======================================================================
     ENGAGEMENT / RETENTION
     ======================================================================= */
  function engagement(days) {
    var r = slice(days), p = prevSlice(days);
    var dauNow = avg(r, 'dau'), dauPrev = avg(p, 'dau');
    var mau = Math.round(dauNow * 4.1), wau = Math.round(dauNow * 2.2);
    return {
      dau: Math.round(dauNow), dauPrev: Math.round(dauPrev),
      wau: wau, mau: mau,
      stickiness: dauNow / mau,
      sessionsPerUser: avg(r, 'sessions') / dauNow,
      avgSessionSec: 214,
      screensPerSession: 11.4,
      notifCtr: sum(r, 'notifOpen') / sum(r, 'notifSent'),
      pushOptIn: .742,
      storiesOpenRate: .418,
      coinsIssued: sum(r, 'coinsIssued'), coinsRedeemed: sum(r, 'coinsRedeemed')
    };
  }

  // weekly retention cohorts (rows = cohort week, cols = weeks since acquisition)
  var cohorts = (function () {
    var out = [];
    var labels = ['14 Jun','21 Jun','28 Jun','05 Jul','12 Jul','19 Jul','26 Jul','02 Aug','09 Aug','16 Aug','23 Aug','30 Aug'];
    for (var c = 0; c < 12; c++) {
      var base = 1;
      var row = { label: 'W' + (c + 1) + ' · ' + labels[c], size: ri(280, 640), vals: [] };
      for (var w = 0; w < 12 - c; w++) {
        if (w === 0) { row.vals.push(1); continue; }
        base = base * (w === 1 ? rr(.44, .58) : rr(.86, .97));
        row.vals.push(Math.min(1, +(base * (1 + c * .012)).toFixed(3)));   // later cohorts retain better
      }
      out.push(row);
    }
    return out;
  })();

  var notifCampaigns = [
    { name: 'Cart abandoned — T+18h',     sent: 8420,  open: .284, click: .162, orders: 386, type: 'Triggered' },
    { name: 'Kharif scheme live',         sent: 22400, open: .118, click: .042, orders: 214, type: 'Broadcast' },
    { name: 'Verification pending nudge', sent: 3840,  open: .346, click: .241, orders: 0,   type: 'Triggered' },
    { name: 'Coins about to expire',      sent: 6180,  open: .224, click: .118, orders: 142, type: 'Triggered' },
    { name: 'New arrival — Chakraveer',   sent: 19600, open: .096, click: .031, orders: 96,  type: 'Broadcast' },
    { name: 'Order out for delivery',     sent: 9840,  open: .512, click: .284, orders: 0,   type: 'Transactional' },
    { name: 'Win-back 45d sleeping',      sent: 4210,  open: .142, click: .064, orders: 62,  type: 'Triggered' },
    { name: 'Gold tier 80% reached',      sent: 1860,  open: .388, click: .214, orders: 84,  type: 'Triggered' }
  ];

  var loyalty = {
    coinsIssued90d: 712000, coinsRedeemed90d: 313000, liability: 399000,
    redeemRate: .44, avgBalance: 1842,
    tierMove: [
      { from: 'Bronze', to: 'Silver',   n: 418 }, { from: 'Silver',   to: 'Gold',    n: 184 },
      { from: 'Gold',   to: 'Platinum', n: 61 },  { from: 'Platinum', to: 'Diamond', n: 14 },
      { from: 'Silver', to: 'Bronze',   n: 98 },  { from: 'Gold',     to: 'Silver',  n: 41 }
    ],
    referral: { invitesSent: 8420, installs: 2480, verified: 1120, firstOrder: 680, k: 0.34, rewardPaid: 340000 }
  };

  var stories = [
    { name: 'Flash Sale',   views: 28400, completion: .62, ctaTap: .142 },
    { name: 'New Arrivals', views: 24100, completion: .58, ctaTap: .118 },
    { name: 'Quiz',         views: 21800, completion: .71, ctaTap: .284 },
    { name: 'Spray Guide',  views: 17200, completion: .54, ctaTap: .096 },
    { name: 'Tips',         views: 14600, completion: .49, ctaTap: .062 },
    { name: 'Top Earners',  views: 11400, completion: .66, ctaTap: .108 },
    { name: 'Margin Boost', views: 9800,  completion: .61, ctaTap: .188 },
    { name: 'Field Demo',   views: 6200,  completion: .44, ctaTap: .074 }
  ];

  /* =======================================================================
     USER JOURNEY / SCREEN FLOW — views are per 30 days
     ======================================================================= */
  var screens = [
    { s: 'home.html',             n: 'Home',              views: 486000, dwell: 42,  exit: .112, rage: .004, err: .002 },
    { s: 'pdp.html',              n: 'Product detail',    views: 275000, dwell: 68,  exit: .186, rage: .012, err: .004 },
    { s: 'categories.html',       n: 'Categories',        views: 88000,  dwell: 21,  exit: .146, rage: .006, err: .002 },
    { s: 'explore.html',          n: 'Explore hub',       views: 74000,  dwell: 29,  exit: .134, rage: .005, err: .001 },
    { s: 'orders.html',           n: 'Orders',            views: 68000,  dwell: 38,  exit: .162, rage: .008, err: .004 },
    { s: 'search.html',           n: 'Search',            views: 62000,  dwell: 24,  exit: .224, rage: .028, err: .006 },
    { s: 'order-tracking.html',   n: 'Order tracking',    views: 42000,  dwell: 46,  exit: .188, rage: .011, err: .006 },
    { s: 'business.html',         n: 'Business',          views: 34000,  dwell: 52,  exit: .208, rage: .009, err: .003 },
    { s: 'cart.html',             n: 'Cart',              views: 31000,  dwell: 54,  exit: .268, rage: .018, err: .008 },
    { s: 'profile.html',          n: 'Account',           views: 28000,  dwell: 26,  exit: .242, rage: .007, err: .002 },
    { s: 'notifications.html',    n: 'Notifications',     views: 24000,  dwell: 18,  exit: .286, rage: .004, err: .001 },
    { s: 'wallet.html',           n: 'Wallet',            views: 21000,  dwell: 34,  exit: .196, rage: .014, err: .009 },
    { s: 'coins.html',            n: 'Partner Coins',     views: 18000,  dwell: 31,  exit: .174, rage: .006, err: .002 },
    { s: 'rapido-documents.html', n: 'Verification docs', views: 12400,  dwell: 112, exit: .384, rage: .062, err: .041 },
    { s: 'checkout.html',         n: 'Checkout',          views: 9800,   dwell: 76,  exit: .312, rage: .034, err: .021 },
    { s: 'settings.html',         n: 'Settings',          views: 8600,   dwell: 22,  exit: .332, rage: .008, err: .002 },
    { s: 'help.html',             n: 'Help',              views: 6800,   dwell: 64,  exit: .296, rage: .022, err: .004 },
    { s: 'price-match.html',      n: 'Price Match',       views: 5200,   dwell: 58,  exit: .214, rage: .016, err: .007 },
    { s: 'credit.html',           n: 'Katyayani Credit',  views: 4900,   dwell: 71,  exit: .268, rage: .019, err: .011 },
    { s: 'delete-account.html',   n: 'Delete account',    views: 420,    dwell: 48,  exit: .612, rage: .008, err: .002 }
  ];

  var topPaths = [
    { path: ['Home', 'PDP', 'Home', 'PDP', 'exit'],                        n: 24180, conv: 0, note: 'Browse-only loop — price comparison' },
    { path: ['Home', 'Orders', 'Order tracking', 'exit'],                  n: 11840, conv: 0, note: 'Support-shaped session' },
    { path: ['Home', 'Cart', 'Checkout', 'exit'],                          n: 4210,  conv: 0, note: 'Checkout drop — investigate' },
    { path: ['Home', 'PDP', 'Cart', 'Checkout', 'Order placed'],           n: 1420,  conv: 1, note: 'Golden path' },
    { path: ['Home', 'Search', 'PDP', 'Cart', 'Checkout', 'Order placed'], n: 860,   conv: 1, note: 'High-intent search path' },
    { path: ['Verification pending', 'Home (locked)', 'exit'],             n: 3940,  conv: 0, note: 'Blocked by verification' },
    { path: ['Home', 'Explore', 'Quick Order', 'Cart', 'Order placed'],     n: 420,   conv: 1, note: 'Tool-led ordering' },
    { path: ['Home', 'Explore', 'Scanner', 'PDP', 'Cart', 'Order placed'],  n: 310,   conv: 1, note: 'Problem → product' },
    { path: ['Home', 'PDP', 'Price Match', 'exit'],                        n: 2410,  conv: 0, note: 'Price objection' },
    { path: ['Home', 'Business', 'Coins', 'exit'],                         n: 2180,  conv: 0, note: 'Rewards check-in' }
  ];

  var sankey = {
    nodes: ['App open', 'Home', 'Search', 'Category', 'Explore', 'PDP', 'Cart', 'Checkout', 'Order placed', 'Exit'],
    links: [
      { s: 'App open', t: 'Home', v: 100 },
      { s: 'Home', t: 'PDP', v: 34 }, { s: 'Home', t: 'Search', v: 18 },
      { s: 'Home', t: 'Category', v: 14 }, { s: 'Home', t: 'Explore', v: 12 }, { s: 'Home', t: 'Exit', v: 22 },
      { s: 'Search', t: 'PDP', v: 13 }, { s: 'Search', t: 'Exit', v: 5 },
      { s: 'Category', t: 'PDP', v: 11 }, { s: 'Category', t: 'Exit', v: 3 },
      { s: 'Explore', t: 'PDP', v: 6 }, { s: 'Explore', t: 'Cart', v: 2 }, { s: 'Explore', t: 'Exit', v: 4 },
      { s: 'PDP', t: 'Cart', v: 9 }, { s: 'PDP', t: 'Exit', v: 55 },
      { s: 'Cart', t: 'Checkout', v: 6 }, { s: 'Cart', t: 'Exit', v: 5 },
      { s: 'Checkout', t: 'Order placed', v: 4 }, { s: 'Checkout', t: 'Exit', v: 2 }
    ]
  };

  /* =======================================================================
     PARTNERS — 260-row sample of the 24,800 verified base
     ======================================================================= */
  var FIRST = ['Ramesh','Suresh','Mahesh','Rakesh','Dinesh','Vijay','Ajay','Sanjay','Manoj','Anil','Sunil','Prakash','Ashok','Rajesh','Deepak','Naresh','Yogesh','Hitesh','Bhavesh','Kailash','Gopal','Mohan','Shyam','Hari','Pankaj','Vinod','Arun','Amit','Rohit','Sachin'];
  var LAST  = ['Patel','Sharma','Verma','Yadav','Singh','Chouhan','Rathore','Gupta','Jain','Agrawal','Pawar','Deshmukh','Kushwaha','Maurya','Tiwari','Mishra','Dubey','Sahu','Thakur','Bhandari'];
  var SHOPN = ['Krishi Kendra','Beej Bhandar','Agro Agency','Khad Beej Store','Kisan Seva Kendra','Krishi Seva Kendra','Agri Junction','Fasal Centre','Hariyali Agro','Annadata Agro'];
  var CITY = {
    MP: ['Indore','Bhopal','Ujjain','Dewas','Sehore','Ratlam','Khargone'],
    MH: ['Nashik','Pune','Jalgaon','Nagpur','Aurangabad','Solapur'],
    UP: ['Kanpur','Lucknow','Varanasi','Meerut','Bareilly','Gorakhpur'],
    RJ: ['Kota','Jaipur','Bharatpur','Sri Ganganagar','Alwar'],
    GJ: ['Rajkot','Junagadh','Surat','Bhavnagar','Mehsana'],
    KA: ['Belagavi','Hubballi','Raichur','Davangere'],
    BR: ['Patna','Muzaffarpur','Begusarai','Purnia'],
    TG: ['Warangal','Nizamabad','Karimnagar'],
    PB: ['Bathinda','Ludhiana','Patiala','Moga'],
    WB: ['Bardhaman','Malda','Hooghly']
  };

  function weightedPick(list) {
    var r = rnd(), acc = 0;
    for (var i = 0; i < list.length; i++) { acc += list[i].share; if (r <= acc) return list[i]; }
    return list[list.length - 1];
  }

  var partners = (function () {
    var arr = [];
    for (var i = 0; i < 260; i++) {
      var stt = weightedPick(STATES);
      var tier = weightedPick(TIERS);
      var seg = weightedPick(SEGMENTS);
      var ch = weightedPick(CHANNELS);
      var joinedAgo = ri(3, 400);
      var jd = new Date(TODAY); jd.setDate(jd.getDate() - joinedAgo);
      var lastAgo = seg.id === 'churned' ? ri(46, 180) : seg.id === 'sleeping' ? ri(12, 45) : ri(0, 11);
      var ld = new Date(TODAY); ld.setDate(ld.getDate() - lastAgo);
      var orders = seg.id === 'browser' ? 0 : seg.id === 'newbie' ? ri(0, 1) : ri(1, 42);
      var aov = Math.round(9200 * tier.aovIx * stt.aovIx * rr(.8, 1.25));
      var verified = seg.id === 'browser' ? true : rnd() > .09;
      arr.push({
        id: 'KP' + (100000 + i * 7 + ri(0, 6)),
        name: pick(FIRST) + ' ' + pick(LAST),
        shop: pick(FIRST) + ' ' + pick(SHOPN),
        city: pick(CITY[stt.id]), state: stt.id, stateName: stt.name,
        tier: tier.id, segment: seg.id, segmentName: seg.name,
        channel: ch.id, channelName: ch.name,
        joined: jd.toISOString().slice(0, 10), joinedAgo: joinedAgo,
        lastActive: ld.toISOString().slice(0, 10), lastActiveAgo: lastAgo,
        orders: orders, aov: aov, gmv: orders * aov,
        coins: ri(0, 14000), sessions30: seg.id === 'churned' ? 0 : ri(1, 46),
        pdpViews30: ri(0, 240), exploreTools: ri(0, 8),
        verified: verified,
        verifyStatus: verified ? 'Verified' : (rnd() > .5 ? 'Pending' : 'Rejected'),
        creditLimit: tier.id === 'Bronze' ? 0 : ri(2, 12) * 25000,
        version: weightedPick(VERSIONS).id,
        churnRisk: +(seg.id === 'churned' ? rr(.82, .99) : seg.id === 'sleeping' ? rr(.52, .81) :
                     seg.id === 'champion' ? rr(.02, .14) : rr(.14, .52)).toFixed(2),
        ltv: 0, farmers: ri(0, 180), returns: ri(0, 4), nps: ri(2, 10)
      });
      var p = arr[arr.length - 1];
      p.ltv = Math.round(p.gmv * rr(1.3, 2.6));
    }
    return arr.sort(function (a, b) { return b.gmv - a.gmv; });
  })();

  function partnerTimeline(p) {
    var ev = [
      { k: 'install',  l: 'Installed the app',            d: p.channelName + ' · attributed by Linkrunner', t: p.joined },
      { k: 'signup',   l: 'OTP verified',                 d: 'Phone +91 ••••• ' + p.id.slice(-4), t: p.joined },
      { k: 'profile',  l: 'Shop details saved',           d: p.shop + ', ' + p.city + ' (' + p.state + ')', t: p.joined },
      { k: 'doc',      l: 'License + Aadhaar uploaded',   d: 'rapido-documents.html', t: p.joined }
    ];
    if (p.verified) ev.push({ k: 'verified', l: 'Verified & activated', d: 'Ops approval in ' + ri(4, 60) + 'h', t: p.joined });
    else ev.push({ k: 'risk', l: 'Verification ' + p.verifyStatus.toLowerCase(), d: 'Blocked from pricing and ordering', t: p.joined });
    if (p.orders > 0) {
      ev.push({ k: 'order', l: 'First order placed', d: '₹' + fmtNum(p.aov) + ' · ' + pick(products).name, t: p.joined });
      ev.push({ k: 'order', l: p.orders + ' orders lifetime', d: '₹' + fmtNum(p.gmv) + ' GMV · AOV ₹' + fmtNum(p.aov), t: p.lastActive });
    } else {
      ev.push({ k: 'risk', l: 'No order yet', d: p.pdpViews30 + ' PDP views in 30d but zero add-to-cart', t: p.lastActive });
    }
    if (p.exploreTools > 0) ev.push({ k: 'tool', l: 'Used ' + p.exploreTools + ' Explore tools', d: 'Most used: ' + pick(tools).name, t: p.lastActive });
    ev.push({ k: 'session', l: 'Last session', d: p.lastActiveAgo + 'd ago · ' + p.sessions30 + ' sessions in 30d · v' + p.version, t: p.lastActive });
    if (p.churnRisk > .6) {
      var s = SEGMENTS.filter(function (x) { return x.id === p.segment; })[0];
      ev.push({ k: 'risk', l: 'Churn risk ' + Math.round(p.churnRisk * 100) + '%', d: s ? s.action : '', t: p.lastActive });
    }
    return ev;
  }

  /* =======================================================================
     EXPERIMENTS + FEATURE FLAGS
     ======================================================================= */
  var experiments = [
    { name: 'Home hero: dark gradient vs light',  metric: 'Home → PDP CTR',  a: .342, b: .388, n: 8420, lift: .134,  sig: .982, status: 'Winner B', owner: 'Umar',   screen: 'home-experiment.html' },
    { name: 'Margin % on card vs ₹ amount',       metric: 'PDP → ATC',       a: .038, b: .046, n: 7840, lift: .211,  sig: .996, status: 'Winner B', owner: 'Umar',   screen: 'pdp.html' },
    { name: 'GST prompt: modal vs skippable row', metric: 'Checkout CVR',    a: .688, b: .742, n: 4180, lift: .078,  sig: .941, status: 'Running',  owner: 'Umar',   screen: 'checkout.html' },
    { name: 'Verify modal auto-pop 3s vs manual', metric: 'Docs submitted',  a: .612, b: .684, n: 3620, lift: .118,  sig: .968, status: 'Winner B', owner: 'Ops',    screen: 'home-pending.html' },
    { name: 'Quick Order voice-first vs photo',   metric: 'Order per open',  a: .182, b: .164, n: 1840, lift: -.099, sig: .812, status: 'Winner A', owner: 'Umar',   screen: 'voice-order.html' },
    { name: 'Distributor unlock: gold vs teal',   metric: 'Unlock rate',     a: .284, b: .241, n: 2840, lift: -.151, sig: .974, status: 'Winner A', owner: 'Umar',   screen: 'pdp.html' },
    { name: 'Free-delivery nudge on cart',        metric: 'Cart → Checkout', a: .612, b: .661, n: 3140, lift: .080,  sig: .889, status: 'Running',  owner: 'Growth', screen: 'cart.html' }
  ];

  var flags = [
    { flag: 'explore_quick_order_v2',   rollout: 1.00, users: 'All',            since: '2026-07-04', kill: false },
    { flag: 'credit_line_preapproval',  rollout: 0.35, users: 'Gold+ · MP/MH',  since: '2026-08-18', kill: false },
    { flag: 'price_match_guarantee',    rollout: 1.00, users: 'All verified',   since: '2026-06-21', kill: false },
    { flag: 'ai_chat_hindi_voice',      rollout: 0.50, users: 'A/B holdout',    since: '2026-09-01', kill: false },
    { flag: 'testimonial_studio',       rollout: 0.15, users: 'Champions only', since: '2026-08-29', kill: false },
    { flag: 'screen_share_support',     rollout: 0.10, users: 'Support-flagged',since: '2026-09-08', kill: true },
    { flag: 'new_checkout_gst_row',     rollout: 0.50, users: 'Experiment',     since: '2026-08-11', kill: false }
  ];

  /* =======================================================================
     APP HEALTH — 30-day window
     ======================================================================= */
  var apiEndpoints = [
    { ep: 'POST /linkrunner/event', calls: 1240000, p50: 42,   p95: 118,  err: .0006, note: 'MMP event pipe' },
    { ep: 'GET /catalog/shelf',     calls: 986000,  p50: 128,  p95: 412,  err: .0021, note: 'Home shelves' },
    { ep: 'GET /pdp/:sku',          calls: 482000,  p50: 164,  p95: 528,  err: .0034, note: 'PDP + price tiers' },
    { ep: 'GET /search',            calls: 368000,  p50: 184,  p95: 688,  err: .0018, note: '' },
    { ep: 'GET /orders',            calls: 148000,  p50: 142,  p95: 396,  err: .0014, note: '' },
    { ep: 'POST /cart/add',         calls: 92000,   p50: 96,   p95: 284,  err: .0042, note: 'ADD button' },
    { ep: 'GET /wallet/coins',      calls: 76000,   p50: 88,   p95: 212,  err: .0009, note: '' },
    { ep: 'POST /ai/chat',          calls: 41000,   p50: 1840, p95: 4120, err: .0088, note: 'LLM latency' },
    { ep: 'POST /order/place',      calls: 12400,   p50: 412,  p95: 1840, err: .0128, note: 'Slowest critical path' },
    { ep: 'POST /kyc/upload',       calls: 9600,    p50: 1240, p95: 4820, err: .0412, note: 'Doc upload — worst error rate' }
  ];

  var crashes = [
    { sig: 'NullPointerException · PdpPriceTier.build()',  n: 118, users: 84, ver: '4.1.3', screen: 'pdp.html',              trend: .284 },
    { sig: 'PlatformException · camera/permission_denied', n: 84,  users: 76, ver: '4.2.0', screen: 'rapido-camera.html',    trend: -.118 },
    { sig: 'OutOfMemoryError · PosterGenerator.render()',  n: 62,  users: 41, ver: '4.2.0', screen: 'poster-generator.html', trend: .462 },
    { sig: 'SocketTimeout · order/place',                  n: 48,  users: 44, ver: 'all',   screen: 'checkout.html',         trend: .064 },
    { sig: 'StateError · CartBloc._recalc',                n: 36,  users: 29, ver: '4.1.0', screen: 'cart.html',             trend: -.342 },
    { sig: 'FormatException · voiceOrder.parseQty',        n: 29,  users: 22, ver: '4.2.0', screen: 'voice-order.html',      trend: .188 },
    { sig: 'RangeError · StoriesViewer.next',              n: 19,  users: 16, ver: '4.2.0', screen: 'home.html',             trend: -.062 }
  ];

  var appHealth = {
    crashFree: .9968, anrRate: .0021, coldStartMs: 1840, warmStartMs: 620,
    apkSizeMb: 38.4, appRatingPlay: 4.3, ratingsCount: 3184,
    p95Api: 688, errorRate: .0038, offlineSessions: .082,
    lowEndDeviceShare: .412, androidVersionOldShare: .186
  };

  /* =======================================================================
     GOALS / OKR — the 20 Cr → 120 Cr plan
     ======================================================================= */
  var goals = [
    { name: 'Annual GMV run-rate',       current: 41.5,  target: 120, unit: 'Cr', by: 'Mar 2027', status: 'on-track', owner: 'Umar' },
    { name: 'Verified partner base',     current: 24.8,  target: 75,  unit: 'K',  by: 'Mar 2027', status: 'at-risk',  owner: 'Ops' },
    { name: 'Monthly active partners',   current: 9.6,   target: 45,  unit: 'K',  by: 'Mar 2027', status: 'on-track', owner: 'Umar' },
    { name: 'Install → first order',     current: 12.8,  target: 25,  unit: '%',  by: 'Dec 2026', status: 'behind',   owner: 'Growth' },
    { name: 'Cart → order CVR',          current: 43.0,  target: 60,  unit: '%',  by: 'Dec 2026', status: 'on-track', owner: 'Umar' },
    { name: 'Verification TAT (median)', current: 19.4,  target: 8,   unit: 'h',  by: 'Dec 2026', status: 'at-risk',  owner: 'Ops',    lowerBetter: true },
    { name: 'D30 retention',             current: 34.8,  target: 45,  unit: '%',  by: 'Mar 2027', status: 'on-track', owner: 'Umar' },
    { name: 'Explore tool adoption',     current: 43.6,  target: 65,  unit: '%',  by: 'Mar 2027', status: 'on-track', owner: 'Umar' },
    { name: 'CAC per verified partner',  current: 1655,  target: 1100, unit: '₹',  by: 'Dec 2026', status: 'at-risk',  owner: 'Growth', lowerBetter: true },
    { name: 'Crash-free sessions',       current: 99.68, target: 99.9,unit: '%',  by: 'Nov 2026', status: 'on-track', owner: 'Eng' }
  ];

  /* =======================================================================
     FORMATTERS
     ======================================================================= */
  function fmtNum(v) {
    if (v === null || v === undefined || isNaN(v)) return '—';
    v = Math.round(v);
    var s = String(Math.abs(v)), out;
    if (s.length > 3) {
      var last3 = s.slice(-3), rest = s.slice(0, -3);
      rest = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ',');
      out = rest + ',' + last3;
    } else out = s;
    return (v < 0 ? '-' : '') + out;
  }
  function fmtCr(v) {
    if (v === null || v === undefined || isNaN(v)) return '—';
    var a = Math.abs(v), sg = v < 0 ? '-₹' : '₹';
    if (a >= 10000000) return sg + (a / 10000000).toFixed(a / 10000000 >= 100 ? 0 : 2) + ' Cr';
    if (a >= 100000)   return sg + (a / 100000).toFixed(a / 100000 >= 100 ? 0 : 1) + ' L';
    if (a >= 1000)     return sg + (a / 1000).toFixed(1) + 'k';
    return sg + fmtNum(a);
  }
  function fmtK(v) {
    if (v === null || v === undefined || isNaN(v)) return '—';
    var a = Math.abs(v), sg = v < 0 ? '-' : '';
    if (a >= 10000000) return sg + (a / 10000000).toFixed(2) + 'Cr';
    if (a >= 100000)   return sg + (a / 100000).toFixed(1) + 'L';
    if (a >= 1000)     return sg + (a / 1000).toFixed(1) + 'k';
    return sg + fmtNum(a);
  }
  function fmtPct(v, dp) {
    if (v === null || v === undefined || isNaN(v)) return '—';
    return (v * 100).toFixed(dp === undefined ? 1 : dp) + '%';
  }
  function fmtDate(iso) {
    var d = new Date(iso + 'T00:00:00');
    return d.getDate() + ' ' + ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][d.getMonth()];
  }
  function fmtDur(sec) {
    if (sec < 60) return Math.round(sec) + 's';
    return Math.floor(sec / 60) + 'm ' + Math.round(sec % 60) + 's';
  }

  /* =======================================================================
     EXPORT
     ======================================================================= */
  global.KO = {
    TODAY: TODAY, DAYS: DAYS, daily: daily, BASE: BASE,
    CHANNELS: CHANNELS, STATES: STATES, TIERS: TIERS, SEGMENTS: SEGMENTS, VERSIONS: VERSIONS,
    slice: slice, prevSlice: prevSlice, sum: sum, avg: avg,
    regFunnel: regFunnel, kycRejects: kycRejects, verifyOps: verifyOps,
    attribution: attribution, campaigns: campaigns, deepLinks: deepLinks,
    sdkHealth: sdkHealth, trackingPlan: trackingPlan,
    products: products, skuPerf: skuPerf, searchTerms: searchTerms,
    categories: categories, discoveryPaths: discoveryPaths,
    commerceFunnel: commerceFunnel, cartDropReasons: cartDropReasons, payments: payments,
    schemesPerf: schemesPerf, coupons: coupons,
    orderStatus: orderStatus, tat: tat, returnReasons: returnReasons, cancelReasons: cancelReasons,
    tools: tools, exploreFunnels: exploreFunnels, aiTopics: aiTopics,
    engagement: engagement, cohorts: cohorts, notifCampaigns: notifCampaigns,
    loyalty: loyalty, stories: stories,
    screens: screens, topPaths: topPaths, sankey: sankey,
    partners: partners, partnerTimeline: partnerTimeline,
    experiments: experiments, flags: flags,
    apiEndpoints: apiEndpoints, crashList: crashes, appHealth: appHealth,
    goals: goals,
    fmtNum: fmtNum, fmtCr: fmtCr, fmtK: fmtK, fmtPct: fmtPct, fmtDate: fmtDate, fmtDur: fmtDur
  };
})(typeof window !== 'undefined' ? window : globalThis);
