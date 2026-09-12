/* =========================================================================
   KO extension — added 2026-09-12 on Umar's request:
     1. KYC: manual vs auto, and WHICH documents drove each auto-approval
     2. My Farmers + My Inventory — the data partners actually enter
     3. Per-tool content/utilisation data for all 13 Explore features
     4. Ratings & reviews — Play Store, App Store, in-app good/bad, per-product
     5. Refunds & returns detail
   Same contract style as data.js: replace each object with an API call.
   ========================================================================= */
(function (KO) {
  'use strict';
  function mulberry(seed) {
    return function () {
      seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
      var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  var rnd = mulberry(773311);
  function ri(a, b) { return Math.round(a + rnd() * (b - a)); }
  function rr(a, b) { return a + rnd() * (b - a); }
  function pick(a) { return a[Math.floor(rnd() * a.length)]; }

  /* =======================================================================
     1. KYC — AUTO vs MANUAL
     Every submission runs the rule engine first. A submission is auto-decided
     only if EVERY mandatory document clears its own automated checks.
     90-day window: ~7,100 submissions.
     ======================================================================= */
  var KYC_TOTAL = 7104;

  // the five outcomes a submission can land in
  var kycPaths = [
    { path: 'Auto-approved',              n: 2060, decided: 'Rule engine',        medianTat: 0.4,  accuracy: .982, color: '#0E7A4E',
      note: 'All 3 mandatory documents cleared every check. No human touched it.' },
    { path: 'Auto-approved · QA sampled', n: 363,  decided: 'Rule engine + audit', medianTat: 0.6,  accuracy: .991, color: '#2FA871',
      note: '5% of auto-approvals are re-checked by a human after the fact to keep the rules honest.' },
    { path: 'Manual approved',            n: 3345, decided: 'Ops reviewer',        medianTat: 26.4, accuracy: .968, color: '#D4A537',
      note: 'At least one automated check was inconclusive, so a reviewer decided.' },
    { path: 'Manual rejected',            n: 1015, decided: 'Ops reviewer',        medianTat: 22.1, accuracy: .944, color: '#E08A1E',
      note: 'Reviewer found a problem the engine only flagged as uncertain.' },
    { path: 'Auto-rejected',              n: 321,  decided: 'Rule engine',         medianTat: 0.3,  accuracy: .997, color: '#E23744',
      note: 'Hard fail — expired licence or a duplicate licence number. Safe to reject without a human.' }
  ];

  // WHICH documents were submitted, and how that changes the auto rate.
  // L = pesticide licence, A = Aadhaar, S = shop photo (all three mandatory);
  // PAN / GST / Bank are optional but each adds a corroborating name match.
  var kycAutoByDocSet = [
    { set: 'Licence + Aadhaar + Shop photo',             short: 'L+A+S',       n: 3842, auto: .284, tat: 18.2, why: 'The mandatory minimum. Name match rests on two documents only, so a fuzzy match below 0.85 sends it to a human.' },
    { set: 'Licence + Aadhaar + Shop photo + PAN',       short: '+PAN',        n: 1486, auto: .462, tat: 11.4, why: 'PAN gives a third independent name string — the strongest single lift to auto-approval.' },
    { set: 'Licence + Aadhaar + Shop photo + GST',       short: '+GST',        n: 864,  auto: .584, tat: 8.1,  why: 'GST carries a verified trade name and address, so shop-name and pincode checks both resolve automatically.' },
    { set: 'Licence + Aadhaar + Shop photo + PAN + GST', short: '+PAN+GST',    n: 512,  auto: .742, tat: 4.2,  why: 'Highest auto rate in the system. Three-way name agreement plus a verified address.' },
    { set: 'Full set incl. bank proof',                  short: 'Full set',    n: 286,  auto: .786, tat: 3.4,  why: 'Bank proof adds nothing to identity but resolves the payout branch, so nothing is left for a human.' },
    { set: 'Licence + Shop photo (no Aadhaar)',          short: 'No Aadhaar',  n: 114,  auto: 0,    tat: 41.8, why: 'Aadhaar is mandatory — these can never auto-approve and sit in the queue until the partner uploads it.' }
  ];

  // the rule engine itself — this is the "pattern" of auto-approval
  var kycAutoRules = [
    { rule: 'licence_ocr_readable',     doc: 'Pesticide licence', check: 'Blur score above 0.72 and all 4 key fields readable', fires: .884, clears: .812, precision: .991, blocking: true,
      fail: 'Photo too blurred or a field is cut off → manual' },
    { rule: 'licence_format_valid',     doc: 'Pesticide licence', check: 'Licence number matches the state agriculture-department format', fires: .812, clears: .946, precision: .998, blocking: true,
      fail: 'Unrecognised format → manual (some states still issue handwritten licences)' },
    { rule: 'licence_not_expired',      doc: 'Pesticide licence', check: 'OCR expiry date is more than 90 days away', fires: .812, clears: .868, precision: .999, blocking: true,
      fail: 'Expired → AUTO-REJECT. Expiring within 90 days → manual with a warning' },
    { rule: 'licence_not_duplicate',    doc: 'Pesticide licence', check: 'Licence number not already on an active account', fires: .812, clears: .982, precision: 1.0, blocking: true,
      fail: 'Duplicate → AUTO-REJECT, flagged to the ASM as a possible second shop' },
    { rule: 'aadhaar_masked_correctly', doc: 'Aadhaar',           check: 'First 8 digits masked as required, last 4 readable', fires: .962, clears: .924, precision: .996, blocking: true,
      fail: 'Unmasked Aadhaar → manual, and the image is re-masked before storage' },
    { rule: 'aadhaar_name_match',       doc: 'Aadhaar + licence', check: 'Fuzzy name match against the licence holder, threshold 0.85', fires: .924, clears: .784, precision: .972, blocking: true,
      fail: 'Below threshold → manual. The single biggest reason submissions leave the auto path' },
    { rule: 'shop_signage_detected',    doc: 'Shop photo',        check: 'Vision model finds a shop board or signage in frame', fires: .946, clears: .842, precision: .958, blocking: true,
      fail: 'No board detected → manual (many rural shops genuinely have no board)' },
    { rule: 'shop_geo_in_pincode',      doc: 'Shop photo',        check: 'Photo EXIF / capture GPS falls inside the declared pincode', fires: .724, clears: .912, precision: .988, blocking: true,
      fail: 'No GPS on the photo → manual. This is why 27.6% never even reach the check' },
    { rule: 'pan_name_corroborates',    doc: 'PAN (optional)',    check: 'Third-way name agreement with licence and Aadhaar', fires: .281, clears: .944, precision: .994, blocking: false,
      fail: 'Not blocking — its absence just removes a shortcut' },
    { rule: 'gst_trade_name_match',     doc: 'GST (optional)',    check: 'Verified GST trade name and address match the shop details', fires: .193, clears: .962, precision: .997, blocking: false,
      fail: 'Not blocking — but when present it resolves the shop-name and address checks outright' }
  ];

  // per-document automation view
  var kycDocAuto = [
    { doc: 'Pesticide licence', mandatory: true,  submitted: 7104, autoCleared: .684, manualNeeded: .316, ocrConf: .882,
      topManualReason: 'Blur / unreadable field (28.1% of all rejections)' },
    { doc: 'Aadhaar',           mandatory: true,  submitted: 6842, autoCleared: .724, manualNeeded: .276, ocrConf: .914,
      topManualReason: 'Name does not fuzzy-match the licence (15.9% of rejections)' },
    { doc: 'Shop photo',        mandatory: true,  submitted: 6480, autoCleared: .768, manualNeeded: .232, ocrConf: .846,
      topManualReason: 'No signage in frame (9.2% of rejections)' },
    { doc: 'PAN',               mandatory: false, submitted: 3840, autoCleared: .944, manualNeeded: .056, ocrConf: .962,
      topManualReason: 'Rarely a blocker' },
    { doc: 'GST certificate',   mandatory: false, submitted: 2410, autoCleared: .962, manualNeeded: .038, ocrConf: .971,
      topManualReason: 'Rarely a blocker' },
    { doc: 'Bank proof',        mandatory: false, submitted: 1862, autoCleared: .886, manualNeeded: .114, ocrConf: .928,
      topManualReason: 'Cheque images with handwriting' }
  ];

  // what it would take to push auto-approval from 34% to 77%
  var kycAutoUnlift = [
    { lever: 'Currently auto-decided',                      add: .386, cum: .386, effort: '—',  note: 'Auto-approved + auto-rejected today' },
    { lever: 'Prefill shop name from licence OCR',          add: .118, cum: .504, effort: 'S',  note: 'Removes most aadhaar_name_match failures by not letting the partner retype the name' },
    { lever: 'Force GPS capture on shop photo', add: .092, cum: .596, effort: 'S', note: '27.6% of submissions never reach shop_geo_in_pincode because the photo has no location' },
    { lever: 'On-device blur + field-crop check before upload', add: .086, cum: .682, effort: 'M', note: 'Stops unreadable licences being submitted at all' },
    { lever: 'Accept "no board" shops with an ASM geo-tag',  add: .054, cum: .736, effort: 'M',  note: 'Many rural shops genuinely have no signage — the rule is wrong, not the partner' },
    { lever: 'DigiLocker / Aadhaar XML instead of a photo',  add: .048, cum: .784, effort: 'L',  note: 'Removes OCR from the identity path entirely' }
  ];

  // individual decision audit trail
  var KYC_REVIEWERS = ['ops.priya', 'ops.rahul', 'ops.sneha', 'ops.imran', 'ops.kavya', 'ops.manoj'];
  var kycAudit = (function () {
    var out = [];
    var sets = kycAutoByDocSet;
    for (var i = 0; i < 120; i++) {
      var ds = sets[Math.min(sets.length - 1, Math.floor(Math.pow(rnd(), 1.5) * sets.length))];
      var isAuto = rnd() < ds.auto;
      var hardFail = !isAuto && rnd() < .085;
      var path = hardFail ? 'Auto-rejected'
        : isAuto ? (rnd() < .148 ? 'Auto-approved · QA sampled' : 'Auto-approved')
        : (rnd() < .258 ? 'Manual rejected' : 'Manual approved');
      var auto = path.indexOf('Auto') === 0;
      var st = KO.STATES[Math.floor(rnd() * KO.STATES.length)];
      var d = new Date(KO.TODAY); d.setDate(d.getDate() - ri(0, 89));
      var blockers = kycAutoRules.filter(function (r) { return r.blocking; });
      out.push({
        id: 'KYC' + (40000 + i * 3 + ri(0, 2)),
        partner: 'KP' + (100000 + ri(0, 1800)),
        state: st.id, stateName: st.name,
        docSet: ds.short, docSetFull: ds.set,
        path: path, auto: auto,
        decidedBy: auto ? 'Rule engine' : pick(KYC_REVIEWERS),
        rule: path === 'Auto-rejected' ? pick(['licence_not_expired', 'licence_not_duplicate'])
            : auto ? 'all blocking rules cleared'
            : pick(blockers).rule,
        confidence: auto ? +(rr(.88, .99)).toFixed(3) : +(rr(.42, .86)).toFixed(3),
        tatH: auto ? +(rr(.1, 1.2)).toFixed(1) : +(rr(4, 62)).toFixed(1),
        submitted: d.toISOString().slice(0, 10),
        outcome: path.indexOf('approved') > 0 || path.indexOf('QA') > 0 ? 'Approved' : 'Rejected'
      });
    }
    return out.sort(function (a, b) { return a.submitted < b.submitted ? 1 : -1; });
  })();

  /* =======================================================================
     2. MY FARMERS + MY INVENTORY — what partners actually entered
     ======================================================================= */
  var CROPS = ['Soybean', 'Cotton', 'Wheat', 'Gram (chana)', 'Tomato', 'Chilli', 'Onion', 'Maize',
               'Paddy', 'Mustard', 'Sugarcane', 'Brinjal', 'Potato', 'Groundnut', 'Garlic'];

  var farmersData = {
    farmersAdded: 18420, partnersUsing: 980, avgPerPartner: 18.8, medianPerPartner: 11,
    villagesCovered: 2410, totalAcreage: 96840, avgAcreage: 5.3,
    withPhone: .884, withCrop: .742, withAcreage: .512, withLandRecord: .118,
    ordersTagged: 1842, orderTagRate: .268, repeatFarmers: .412,
    addedLast30d: 2184, staleOver90d: .284,
    distribution: [
      { b: '1–5 farmers', n: 386 }, { b: '6–15', n: 284 }, { b: '16–30', n: 168 },
      { b: '31–60', n: 92 }, { b: '61–120', n: 38 }, { b: '120+', n: 12 }
    ],
    topCrops: CROPS.slice(0, 10).map(function (c, i) {
      var n = Math.round(18420 * [.182, .164, .121, .096, .084, .072, .061, .054, .048, .038][i]);
      return { crop: c, farmers: n, acreage: Math.round(n * rr(3.2, 8.4)),
               linkedGmv: Math.round(n * rr(240, 1180)),
               topSku: KO.products[Math.floor(rnd() * KO.products.length)].name };
    }),
    byState: KO.STATES.map(function (s) {
      return { state: s.id, stateName: s.name, farmers: Math.round(18420 * s.share * rr(.8, 1.25)),
               avgAcreage: +(rr(3.1, 9.2)).toFixed(1), tagRate: +(rr(.14, .41)).toFixed(3) };
    }),
    valueProof: [
      { g: 'Partners with 30+ farmers tagged', orders: 8.4, aov: 1.42, retention: .684, n: 142 },
      { g: 'Partners with 6–29 farmers',        orders: 4.6, aov: 1.12, retention: .512, n: 452 },
      { g: 'Partners with 1–5 farmers',         orders: 2.8, aov: .96,  retention: .388, n: 386 },
      { g: 'Partners using My Farmers at all',  orders: 4.8, aov: 1.14, retention: .518, n: 980 },
      { g: 'Partners not using it',             orders: 2.1, aov: 1.00, retention: .342, n: 8620 }
    ]
  };

  var inventoryData = {
    partnersUsing: 740, skusTracked: 9860, avgSkusPerPartner: 13.3, medianSkusPerPartner: 9,
    stockValueTracked: 41200000, avgStockValue: 55676,
    stockOutFlags30d: 1842, reordersFromInventory: 618, reorderGmv: 6240000,
    syncedLast7d: .624, staleOver30d: .218, manualEntry: .884, scannedEntry: .116,
    deadStockValue: 4860000, deadStockShare: .118,
    distribution: [
      { b: '1–5 SKUs', n: 214 }, { b: '6–15', n: 268 }, { b: '16–30', n: 152 },
      { b: '31–60', n: 74 }, { b: '60+', n: 32 }
    ],
    topTracked: KO.products.slice(0, 10).map(function (p, i) {
      var n = Math.round(9860 * [.124, .112, .098, .092, .084, .078, .071, .064, .058, .048][i] / 1.2);
      return { sku: p.sku, name: p.name, partners: n,
               unitsHeld: Math.round(n * rr(8, 42)),
               stockOuts: Math.round(n * rr(.06, .31)),
               reorders: Math.round(n * rr(.04, .18)),
               daysOfCover: +(rr(6, 48)).toFixed(0) };
    }),
    alerts: [
      { a: 'Below reorder level', n: 1842, acted: .336, note: 'Partner set a threshold and stock fell under it' },
      { a: 'Zero stock on a fast mover', n: 684, acted: .482, note: 'Highest-intent alert in the system' },
      { a: 'Expiry within 90 days', n: 412, acted: .218, note: 'Should trigger a clearance suggestion, currently does not' },
      { a: 'Dead stock 60+ days', n: 386, acted: .096, note: 'Ignored almost entirely — no action offered with the alert' },
      { a: 'Overstocked vs season', n: 184, acted: .064, note: 'Too abstract to act on' }
    ],
    valueProof: [
      { g: 'Inventory synced in last 7 days', orders: 7.2, aov: 1.38, retention: .642, n: 462 },
      { g: 'Inventory stale 8–30 days',       orders: 4.1, aov: 1.08, retention: .484, n: 116 },
      { g: 'Inventory stale 30 days+',        orders: 2.6, aov: .94,  retention: .362, n: 162 },
      { g: 'Not using My Inventory',          orders: 2.1, aov: 1.00, retention: .342, n: 8860 }
    ]
  };

  /* =======================================================================
     3. PER-TOOL CONTENT / UTILISATION DATA (all 13 Explore tools)
     ======================================================================= */
  var toolData = {
    scanner: { unit: 'diagnoses run', created: 4048, createdPer: 2.2, quality: 'Model confidence 0.84 avg · 71% of partners agreed with the diagnosis',
      rows: [
        { k: 'Diagnoses run (30d)', v: '4,048' }, { k: 'Unique crops scanned', v: '18' },
        { k: 'Top crop', v: 'Cotton (24.1%)' }, { k: 'Top disease detected', v: 'Leaf curl virus (18.6%)' },
        { k: 'Avg model confidence', v: '0.84' }, { k: 'Partner agreed with diagnosis', v: '71.2%' },
        { k: 'Marked "wrong" by partner', v: '8.4%' }, { k: 'Diagnosis → PDP tap', v: '18.6%' },
        { k: 'Retake rate (bad photo)', v: '21.4%' }
      ],
      detail: [
        { a: 'Cotton', b: 'Pink bollworm', n: 412 }, { a: 'Cotton', b: 'Leaf curl virus', n: 386 },
        { a: 'Tomato', b: 'Early blight', n: 324 }, { a: 'Chilli', b: 'Thrips', n: 286 },
        { a: 'Soybean', b: 'Girdle beetle', n: 241 }, { a: 'Tomato', b: 'Leaf miner', n: 218 },
        { a: 'Wheat', b: 'Yellow rust', n: 196 }, { a: 'Chilli', b: 'Anthracnose', n: 184 },
        { a: 'Onion', b: 'Purple blotch', n: 162 }, { a: 'Paddy', b: 'Stem borer', n: 148 }
      ], detailCols: ['Crop', 'Detected problem', 'Diagnoses'] },

    profitcalc: { unit: 'calculations run', created: 6816, createdPer: 2.4, quality: 'Avg margin computed 26.4% · 84% of calculations were on a SKU the partner already stocks',
      rows: [
        { k: 'Calculations run (30d)', v: '6,816' }, { k: 'Unique SKUs calculated', v: '16' },
        { k: 'Avg margin computed', v: '26.4%' }, { k: 'Avg selling price entered', v: '₹412' },
        { k: 'Calculated on a stocked SKU', v: '84.2%' }, { k: 'Saved the calculation', v: '18.4%' },
        { k: 'Tapped "Order this"', v: '16.9%' }, { k: 'Recalculated same SKU', v: '34.1%' }
      ],
      detail: KO.products.slice(0, 10).map(function (p, i) {
        return { a: p.name.replace('Katyayani ', ''), b: '₹' + p.price, n: Math.round(6816 * [.142, .124, .112, .096, .088, .081, .074, .068, .058, .044][i]) };
      }), detailCols: ['SKU calculated', 'List price', 'Calculations'] },

    aichat: { unit: 'questions asked', created: 12162, createdPer: 1.4, quality: '81% rated helpful · 8 topic clusters · p95 response 4.1s',
      rows: [
        { k: 'Questions asked (30d)', v: '12,162' }, { k: 'Sessions', v: '8,904' },
        { k: 'Questions per session', v: '1.4' }, { k: 'Rated helpful', v: '81.4%' },
        { k: 'Hindi / Hinglish input', v: '78.2%' }, { k: 'Voice input used', v: '34.6%' },
        { k: 'Escalated to human', v: '4.1%' }, { k: 'p95 response time', v: '4.1s' }
      ],
      detail: KO.aiTopics.map(function (t) { return { a: t.t, b: (t.resolved * 100).toFixed(0) + '% resolved', n: t.n }; }),
      detailCols: ['Topic', 'Resolution', 'Questions'] },

    quickorder: { unit: 'orders parsed', created: 2528, createdPer: 2.7, quality: 'Item parse accuracy 83.5% · quantity is the failing field, not the product name',
      rows: [
        { k: 'Voice/photo inputs (30d)', v: '2,528' }, { k: 'Voice input share', v: '62.4%' },
        { k: 'Photo (written list) share', v: '37.6%' }, { k: 'Items parsed correctly', v: '83.5%' },
        { k: 'Quantity corrected by partner', v: '41.2%' }, { k: 'Product corrected by partner', v: '12.4%' },
        { k: 'Avg items per input', v: '4.8' }, { k: 'Input → order placed', v: '7.4%' }
      ],
      detail: [
        { a: 'Quantity / unit misread', b: 'parse error', n: 412 }, { a: 'Hinglish brand name', b: 'parse error', n: 286 },
        { a: 'Pack size ambiguous', b: 'parse error', n: 241 }, { a: 'Background noise', b: 'input error', n: 184 },
        { a: 'Handwriting unreadable', b: 'photo error', n: 162 }, { a: 'Multiple SKUs in one line', b: 'parse error', n: 118 }
      ], detailCols: ['Failure mode', 'Type', 'Count'] },

    disease: { unit: 'crop→problem lookups', created: 5742, createdPer: 2.2, quality: 'Best-converting discovery path at 7.4% — guided beats a flat result list',
      rows: [
        { k: 'Lookups (30d)', v: '5,742' }, { k: 'Unique crop→problem pairs', v: '142' },
        { k: 'Top crop', v: 'Cotton (21.4%)' }, { k: 'Reached a product list', v: '67.2%' },
        { k: 'Opened a PDP', v: '13.9%' }, { k: 'Order placed', v: '5.5%' },
        { k: 'Abandoned at crop picker', v: '15.0%' }
      ],
      detail: [
        { a: 'Cotton', b: 'Sucking pests', n: 486 }, { a: 'Tomato', b: 'Leaf curl', n: 412 },
        { a: 'Chilli', b: 'Thrips / mites', n: 386 }, { a: 'Soybean', b: 'Caterpillar', n: 324 },
        { a: 'Wheat', b: 'Rust', n: 286 }, { a: 'Onion', b: 'Thrips', n: 241 },
        { a: 'Gram (chana)', b: 'Pod borer', n: 218 }, { a: 'Paddy', b: 'Stem borer', n: 196 }
      ], detailCols: ['Crop', 'Problem group', 'Lookups'] },

    poster: { unit: 'posters created', created: 2360, createdPer: 2.0, quality: '68% downloaded, 41% shared to WhatsApp — the shared ones are the point',
      rows: [
        { k: 'Posters created (30d)', v: '2,360' }, { k: 'Downloaded', v: '68.4%' },
        { k: 'Shared to WhatsApp', v: '41.2%' }, { k: 'Templates available', v: '12' },
        { k: 'Most used template', v: 'Scheme offer (28.4%)' }, { k: 'Own shop name added', v: '84.6%' },
        { k: 'Own photo added', v: '22.1%' }, { k: 'Render failure (OOM crash)', v: '2.6%' }
      ],
      detail: [
        { a: 'Scheme offer', b: 'gold', n: 670 }, { a: 'New arrival', b: 'emerald', n: 486 },
        { a: 'Price drop', b: 'red', n: 412 }, { a: 'Crop advisory', b: 'green', n: 324 },
        { a: 'Shop anniversary', b: 'festive', n: 218 }, { a: 'Festival greeting', b: 'festive', n: 162 },
        { a: 'Blank / custom', b: 'plain', n: 88 }
      ], detailCols: ['Template', 'Style', 'Posters'] },

    farmers: { unit: 'farmers added', created: 2184, createdPer: 2.2, quality: '88% have a phone number, only 51% have acreage — the form asks for too much',
      rows: [
        { k: 'Farmers added (30d)', v: '2,184' }, { k: 'Total farmers on record', v: '18,420' },
        { k: 'Partners using it', v: '980' }, { k: 'Avg farmers per partner', v: '18.8' },
        { k: 'With phone number', v: '88.4%' }, { k: 'With crop recorded', v: '74.2%' },
        { k: 'With acreage recorded', v: '51.2%' }, { k: 'Orders tagged to a farmer', v: '26.8%' },
        { k: 'Records untouched 90d+', v: '28.4%' }
      ],
      detail: farmersData.topCrops.map(function (c) { return { a: c.crop, b: c.acreage.toLocaleString('en-IN') + ' acres', n: c.farmers }; }),
      detailCols: ['Crop', 'Acreage', 'Farmers'] },

    inventory: { unit: 'SKUs tracked', created: 1284, createdPer: 1.7, quality: '62% synced in the last 7 days · 88% still entered by hand',
      rows: [
        { k: 'SKU records added (30d)', v: '1,284' }, { k: 'Total SKUs tracked', v: '9,860' },
        { k: 'Partners using it', v: '740' }, { k: 'Stock value tracked', v: '₹4.12 Cr' },
        { k: 'Synced in last 7 days', v: '62.4%' }, { k: 'Manual entry', v: '88.4%' },
        { k: 'Barcode scan entry', v: '11.6%' }, { k: 'Stock-out alerts fired', v: '1,842' },
        { k: 'Reorders from an alert', v: '618' }
      ],
      detail: inventoryData.topTracked.map(function (t) { return { a: t.name.replace('Katyayani ', ''), b: t.daysOfCover + ' days cover', n: t.partners }; }),
      detailCols: ['SKU', 'Avg cover', 'Partners tracking'] },

    transfer: { unit: 'transfers made', created: 504, createdPer: 2.4, quality: 'Lowest NPS of any tool (51) and the only one with shrinking adoption',
      rows: [
        { k: 'Transfers initiated (30d)', v: '504' }, { k: 'Completed', v: '61.2%' },
        { k: 'Value transferred', v: '₹36.0 L' }, { k: 'Avg transfer value', v: '₹11,680' },
        { k: 'Cancelled mid-flow', v: '28.4%' }, { k: 'Failed (stock mismatch)', v: '10.4%' },
        { k: 'Partners using it', v: '210' }, { k: 'Repeat users', v: '18.8%' }
      ],
      detail: [
        { a: 'Receiver not on the app', b: 'blocker', n: 142 }, { a: 'Stock quantity mismatch', b: 'blocker', n: 96 },
        { a: 'Price disagreement', b: 'drop', n: 74 }, { a: 'Unclear who pays delivery', b: 'drop', n: 62 },
        { a: 'Completed successfully', b: 'ok', n: 308 }
      ], detailCols: ['Outcome', 'Type', 'Transfers'] },

    community: { unit: 'posts & comments', created: 4184, createdPer: 2.6, quality: 'High time-on-tool (6.4 min) but almost no commercial effect — judge it on retention',
      rows: [
        { k: 'Posts created (30d)', v: '684' }, { k: 'Comments', v: '3,500' },
        { k: 'Likes', v: '12,840' }, { k: 'Partners posting', v: '286' },
        { k: 'Partners reading only', v: '1,334' }, { k: 'Avg time per session', v: '6m 24s' },
        { k: 'Reported / moderated', v: '41' }, { k: 'Posts with a product mention', v: '18.4%' }
      ],
      detail: [
        { a: 'Crop problem question', b: 'question', n: 218 }, { a: 'Price / margin discussion', b: 'discussion', n: 164 },
        { a: 'Result photo (field)', b: 'showcase', n: 121 }, { a: 'Scheme / offer chatter', b: 'discussion', n: 84 },
        { a: 'Shop setup / display', b: 'showcase', n: 58 }, { a: 'Off-topic', b: 'moderated', n: 39 }
      ], detailCols: ['Post type', 'Category', 'Posts'] },

    training: { unit: 'modules completed', created: 1842, createdPer: 1.8, quality: 'Highest time-on-tool (8.2 min) and 72 NPS — partners genuinely watch it',
      rows: [
        { k: 'Module views (30d)', v: '4,186' }, { k: 'Modules completed', v: '1,842' },
        { k: 'Completion rate', v: '44.0%' }, { k: 'Certificates issued', v: '412' },
        { k: 'Partners enrolled', v: '1,040' }, { k: 'Avg watch time', v: '8m 12s' },
        { k: 'Quiz attempted', v: '38.4%' }, { k: 'Quiz passed', v: '71.2%' }
      ],
      detail: [
        { a: 'Spray safety & dosage', b: '6 min', n: 486 }, { a: 'Selling margin maths', b: '4 min', n: 412 },
        { a: 'Pesticide licence rules', b: '8 min', n: 324 }, { a: 'Identifying fake product', b: '5 min', n: 286 },
        { a: 'Crop calendar planning', b: '11 min', n: 196 }, { a: 'Using the Partner App', b: '3 min', n: 138 }
      ], detailCols: ['Module', 'Length', 'Completions'] },

    testimonial: { unit: 'testimonials submitted', created: 360, createdPer: 1.5, quality: 'Only 15% rollout (Champions flag) · 58% approval rate',
      rows: [
        { k: 'Submissions (30d)', v: '360' }, { k: 'Approved', v: '58.1%' },
        { k: 'Rejected', v: '24.4%' }, { k: 'Pending review', v: '17.5%' },
        { k: 'Video submissions', v: '68.4%' }, { k: 'Text + photo', v: '31.6%' },
        { k: 'Avg video length', v: '42s' }, { k: 'Coins paid out', v: '52,200' },
        { k: 'Rollout (feature flag)', v: '15% — Champions only' }
      ],
      detail: [
        { a: 'Approved — used in marketing', b: 'approved', n: 128 }, { a: 'Approved — not yet used', b: 'approved', n: 81 },
        { a: 'Rejected — audio unusable', b: 'rejected', n: 38 }, { a: 'Rejected — competitor visible', b: 'rejected', n: 27 },
        { a: 'Rejected — off-brief', b: 'rejected', n: 23 }, { a: 'Pending review', b: 'pending', n: 63 }
      ], detailCols: ['Outcome', 'Status', 'Submissions'] },

    pricematch: { unit: 'claims raised', created: 1054, createdPer: 1.7, quality: '64% approved · pre-order claims pay in coins, post-order in wallet',
      rows: [
        { k: 'Claims raised (30d)', v: '1,054' }, { k: 'Approved', v: '64.2%' },
        { k: 'Rejected', v: '28.4%' }, { k: 'Pending', v: '7.4%' },
        { k: 'Pre-order claims (→ coins)', v: '58.6%' }, { k: 'Post-order claims (→ wallet)', v: '41.4%' },
        { k: 'Avg claim amount', v: '₹412' }, { k: 'Total paid out', v: '₹2.79 L' },
        { k: 'Median resolution time', v: '18h' }
      ],
      detail: [
        { a: 'Approved — listed channel proof', b: 'approved', n: 677 }, { a: 'Rejected — unlisted channel', b: 'rejected', n: 164 },
        { a: 'Rejected — different pack size', b: 'rejected', n: 84 }, { a: 'Rejected — proof unreadable', b: 'rejected', n: 51 },
        { a: 'Pending', b: 'pending', n: 78 }
      ], detailCols: ['Outcome', 'Status', 'Claims'] }
  };

  /* =======================================================================
     4. RATINGS & REVIEWS — Play Store, App Store, in-app, per product
     ======================================================================= */
  var stores = [
    { store: 'Google Play', rating: 4.3, ratings: 3184, reviews: 986, installs: 41800,
      dist: [.062, .048, .084, .214, .592], trend: .12, respRate: .684, respHours: 18.4,
      color: '#0E7A4E', share: .948 },
    { store: 'Apple App Store', rating: 4.1, ratings: 286, reviews: 94, installs: 2410,
      dist: [.084, .062, .112, .238, .504], trend: -.04, respRate: .412, respHours: 41.2,
      color: '#5B6670', share: .052 }
  ];

  var storeRatingTrend = (function () {
    var out = [];
    var labels = ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'];
    var play = [3.9, 4.0, 4.0, 4.1, 4.2, 4.2, 4.3];
    var ios = [4.2, 4.2, 4.1, 4.1, 4.0, 4.1, 4.1];
    labels.forEach(function (l, i) { out.push({ m: l, play: play[i], ios: ios[i] }); });
    return out;
  })();

  var storeRatingByVersion = KO.VERSIONS.map(function (v, i) {
    return { ver: v.id, label: v.label, rating: [4.4, 4.3, 4.1, 3.8, 3.4][i],
             ratings: Math.round(3470 * v.share), crashFree: v.crashFree };
  });

  var reviewThemes = [
    { theme: 'Margin / profit visibility', n: 284, sent: .84, store: 'Both', quote: 'Margin dikhta hai isliye order karna aasan hai', act: 'Working — keep it front and centre' },
    { theme: 'Delivery speed & tracking', n: 241, sent: .52, store: 'Both', quote: 'Order 2 din me aa gaya par tracking update nahi hua', act: 'Proactive dispatch push — see Orders & Delivery' },
    { theme: 'Verification took too long', n: 196, sent: .18, store: 'Play', quote: 'Licence upload karke 3 din wait kiya', act: 'Auto-approval expansion — see Register → Verify' },
    { theme: 'App speed / hangs', n: 164, sent: .22, store: 'Both', quote: 'Phone me app slow chalta hai, khulne me time lagta hai', act: '4.2s cold start on low-end devices — see App Health' },
    { theme: 'Product range / out of stock', n: 148, sent: .34, store: 'Both', quote: 'Sprayer aur seeds bhi hone chahiye', act: 'Catalogue gaps — see Discovery & Search' },
    { theme: 'Coins & scheme confusion', n: 121, sent: .44, store: 'Play', quote: 'Coins kaise use hote hain samajh nahi aaya', act: 'Coins balance not visible enough — see Engagement' },
    { theme: 'Disease scanner is useful', n: 108, sent: .88, store: 'Both', quote: 'Photo se bimari pata chal jati hai, kisan ko dikhata hoon', act: 'Promote it — high value, low reach' },
    { theme: 'Credit / payment terms', n: 96, sent: .62, store: 'Play', quote: '30 din ka credit milta hai to stock rakh sakta hoon', act: 'Expand credit pre-approval' },
    { theme: 'COD / refund issues', n: 84, sent: .16, store: 'Both', quote: 'Return kiya tha, paisa wapas aane me time laga', act: 'Refund TAT — see the Refunds tab' },
    { theme: 'iOS specific bugs', n: 41, sent: .24, store: 'iOS', quote: 'iPhone me camera upload fail hota hai', act: 'iOS SDK coverage is only 94.2%' }
  ];

  // in-app good/bad prompt (the auto-triggered rate-app bottom sheet)
  var inAppRating = {
    shown: 8420, shownRate: .284, dismissed: .386,
    happy: .412, unhappy: .202,
    happyToStore: .486, happyRatedOnStore: .284,
    unhappyGaveFeedback: .742,
    fork: [
      { step: 'Prompt auto-triggered', value: 8420, where: 'home.html · after a delivered order' },
      { step: 'Partner responded', value: 5170, where: 'good / bad selection' },
      { step: 'Selected "Good"', value: 3469, where: '→ Play Store / App Store' },
      { step: 'Tapped through to the store', value: 1686, where: 'store listing opened' },
      { step: 'Actually rated on the store', value: 985, where: 'store review posted' }
    ],
    badFork: [
      { step: 'Selected "Bad"', value: 1701, where: '→ in-app feedback, never the store' },
      { step: 'Picked a feedback tag', value: 1262, where: 'predefined tags' },
      { step: 'Added a free-text note', value: 486, where: 'optional' },
      { step: 'Support followed up', value: 318, where: 'ticket raised' }
    ],
    tags: [
      { tag: 'Delivery was late', n: 284, pct: .225 },
      { tag: 'Verification too slow', n: 241, pct: .191 },
      { tag: 'App is slow / hangs', n: 196, pct: .155 },
      { tag: 'Product not available', n: 164, pct: .130 },
      { tag: 'Price too high', n: 148, pct: .117 },
      { tag: 'Refund pending', n: 108, pct: .086 },
      { tag: 'Wrong item delivered', n: 74, pct: .059 },
      { tag: 'Other', n: 47, pct: .037 }
    ],
    note: 'The prompt never sends an unhappy partner to the store — "Bad" always routes to in-app feedback. That is why the store rating (4.3) reads higher than in-app sentiment (67% good).'
  };

  // product-wise rating
  var productRatings = (function () {
    var seed = mulberry(9911);
    return KO.products.map(function (p, i) {
      var avg = +(3.4 + seed() * 1.5).toFixed(1);
      var n = Math.round(120 + seed() * 880);
      var five = Math.max(.18, Math.min(.74, (avg - 2.6) / 2.4));
      var one = Math.max(.02, .28 - five * .3);
      var rest = 1 - five - one;
      return {
        sku: p.sku, name: p.name, cat: p.cat, price: p.price,
        rating: avg, count: n,
        retailerRating: +(avg + (seed() - .45) * .5).toFixed(1),
        farmerRating: +(avg + (seed() - .55) * .6).toFixed(1),
        dist: [one, rest * .18, rest * .26, rest * .56, five].map(function (x) { return +x.toFixed(3); }),
        withPhoto: +(seed() * .32).toFixed(3),
        verifiedBuyer: +(.72 + seed() * .26).toFixed(3),
        topComplaint: pick(['Result slow to show', 'Leakage in transit', 'Pack size confusing',
                            'Expiry was near', 'Price higher than local', 'Dosage unclear', '—'])
      };
    }).sort(function (a, b) { return b.count - a.count; });
  })();

  /* =======================================================================
     5. REFUNDS
     ======================================================================= */
  var refunds = {
    requested: 1842, approved: 1284, rejected: 386, pending: 172,
    approvalRate: .697, medianTatH: 38.4, p90TatH: 112,
    amount: 14680000, avgAmount: 11432,
    disputes: 148, escalations: 62, ombudsman: 4,
    modes: [
      { m: 'Wallet credit (instant)', n: 642, share: .500, tatH: 2.4, satisfaction: .84, cost: 0,
        note: 'Default. Cheapest and fastest, and the balance usually gets spent with us again.' },
      { m: 'Partner Coins', n: 231, share: .180, tatH: 1.1, satisfaction: .72, cost: 0,
        note: 'Used for price-match pre-order claims. Fast but partners value coins below cash.' },
      { m: 'Bank transfer (NEFT)', n: 244, share: .190, tatH: 96, satisfaction: .58, cost: 12,
        note: 'What partners ask for and what takes the longest — the single worst satisfaction score.' },
      { m: 'Credit note (next order)', n: 141, share: .110, tatH: 4.2, satisfaction: .64, cost: 0,
        note: 'Good for us, mildly resented by partners.' },
      { m: 'Adjusted against credit line', n: 26, share: .020, tatH: 6.8, satisfaction: .78, cost: 0,
        note: 'Only for partners on Katyayani Credit.' }
    ],
    reasons: KO.returnReasons.map(function (r, i) {
      return { r: r.r, pct: r.pct, n: Math.round(1842 * r.pct),
               approvalRate: [.84, .72, .96, .98, .94, .34, .52][i],
               avgAmount: Math.round(11432 * [1.0, .82, 1.14, 1.08, .96, 1.22, .74][i]) };
    }),
    tatBuckets: [
      { b: 'Under 6h', n: 386 }, { b: '6–24h', n: 462 }, { b: '1–2 days', n: 284 },
      { b: '2–4 days', n: 218 }, { b: '4–7 days', n: 142 }, { b: 'Over 7 days', n: 178 }
    ],
    funnel: [
      { step: 'Return requested', value: 1842, where: 'return-request.html' },
      { step: 'Reason + photos submitted', value: 1702, where: '' },
      { step: 'Approved by ops', value: 1284, where: 'median 14h' },
      { step: 'Pickup scheduled', value: 1212, where: '' },
      { step: 'Item collected', value: 1118, where: 'reverse logistics' },
      { step: 'Refund initiated', value: 1064, where: '' },
      { step: 'Money / credit received', value: 986, where: 'wallet.html' }
    ],
    aftermath: [
      { g: 'Refunded in under 24h', reorder: .684, retention: .712, nps: 8.2, n: 848 },
      { g: 'Refunded in 1–4 days', reorder: .486, retention: .548, nps: 6.4, n: 502 },
      { g: 'Refunded after 7 days', reorder: .284, retention: .362, nps: 3.8, n: 178 },
      { g: 'Refund rejected', reorder: .218, retention: .284, nps: 2.9, n: 386 },
      { g: 'Still pending', reorder: .142, retention: .241, nps: 2.1, n: 172 },
      { g: 'No return at all (baseline)', reorder: .484, retention: .586, nps: 7.1, n: 9400 }
    ],
    byState: KO.STATES.map(function (s, i) {
      return { state: s.id, stateName: s.name,
               requests: Math.round(1842 * s.share * rr(.8, 1.3)),
               tatH: +(rr(18, 92)).toFixed(0),
               approvalRate: +(rr(.58, .82)).toFixed(3) };
    })
  };

  /* ---------------- export ---------------- */
  KO.kycPaths = kycPaths;
  KO.kycAutoByDocSet = kycAutoByDocSet;
  KO.kycAutoRules = kycAutoRules;
  KO.kycDocAuto = kycDocAuto;
  KO.kycAutoUnlift = kycAutoUnlift;
  KO.kycAudit = kycAudit;
  KO.KYC_TOTAL = KYC_TOTAL;
  KO.farmersData = farmersData;
  KO.inventoryData = inventoryData;
  KO.toolData = toolData;
  KO.stores = stores;
  KO.storeRatingTrend = storeRatingTrend;
  KO.storeRatingByVersion = storeRatingByVersion;
  KO.reviewThemes = reviewThemes;
  KO.inAppRating = inAppRating;
  KO.productRatings = productRatings;
  KO.refunds = refunds;
  KO.CROPS = CROPS;
})(typeof window !== 'undefined' ? window.KO : globalThis.KO);
