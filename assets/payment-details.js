/* Phase 3 · Payment details card on Order Status (order-tracking) and Order Details.
   Turned on only by ?pay=prepaid|partial|cod — without it both pages stay as they were.
   Payer fields mirror what the Razorpay payment entity returns:
   method, vpa / card (network, last4, name) / bank, contact, id (pay_…), acquirer_data.rrn, created_at. */
(function () {
  var pay = new URLSearchParams(location.search).get('pay');
  var slot = document.querySelector('[data-pay-slot]');
  if (!slot || ['prepaid', 'partial', 'cod'].indexOf(pay) < 0) return;

  var stage = slot.getAttribute('data-stage');           // transit | delivered
  var total = +slot.getAttribute('data-total');
  var delivered = stage === 'delivered';
  var placedAt = slot.getAttribute('data-placed');        // e.g. "8 Apr, 2:15 PM"
  var doneAt = slot.getAttribute('data-delivered') || '';
  var rs = function (n) { return '₹' + Math.round(n).toLocaleString('en-IN'); };

  var UPI = { label: 'UPI', rows: [
    ['UPI ID', 'ramesh.patel@okhdfcbank'],
    ['Bank', 'HDFC Bank'],
    ['Mobile', '+91 98260 •••45'],
    ['Payment ID', 'pay_PQ7xK2mLsa91Bd', 1],
    ['UTR / RRN', '412398765432', 1]
  ]};
  var CARD = { label: 'Debit card', rows: [
    ['Card', 'Visa •••• 4321'],
    ['Name on card', 'RAMESH PATEL'],
    ['Bank', 'HDFC Bank'],
    ['Mobile', '+91 98260 •••45'],
    ['Payment ID', 'pay_PQ8bR4tWnc22Lk', 1]
  ]};
  var QR = { label: 'UPI · scanned at delivery', rows: [
    ['UPI ID', 'rameshks@ybl'],
    ['Bank', 'State Bank of India'],
    ['Payment ID', 'pay_PR1dE9vYqk05Ma', 1],
    ['UTR / RRN', '412455501873', 1]
  ]};

  var ICON = {
    ok: '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg>',
    clock: '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    copy: '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#0E7A4E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 012-2h10"/></svg>',
    card: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0C831F" stroke-width="2"><rect x="2" y="6" width="20" height="14" rx="2"/><path d="M2 11h20"/></svg>',
    cash: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8B6914" stroke-width="2" stroke-linecap="round"><rect x="2" y="7" width="20" height="12" rx="2"/><circle cx="12" cy="13" r="2.5"/><path d="M6 11v4M18 11v4"/></svg>',
    doc: '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#1C1C1C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6"/></svg>'
  };
  function pill(t, kind) {
    var c = kind === 'ok' ? 'background:#E8F5E9;color:#0C831F' : 'background:#FFF4DC;color:#8B6914';
    return '<span style="display:inline-flex;align-items:center;gap:4px;' + c + ';font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;padding:3px 8px;border-radius:20px">' + ICON[kind === 'ok' ? 'ok' : 'clock'] + t + '</span>';
  }
  /* one payment leg: amount line + Razorpay payer rows */
  function leg(title, amount, when, m) {
    return '<div style="border:1px solid #EDEDED;border-radius:10px;overflow:hidden;margin-top:10px">' +
      '<div style="display:flex;align-items:center;gap:10px;padding:10px 12px;background:#F7FBF8">' +
        '<div style="width:34px;height:34px;border-radius:9px;background:#E8F5E9;display:flex;align-items:center;justify-content:center;flex-shrink:0">' + ICON.card + '</div>' +
        '<div style="flex:1;min-width:0;line-height:1.25"><div style="font-size:13px;font-weight:600;color:#1C1C1C">' + title + '</div>' +
        '<div style="font-size:11px;color:#707070;margin-top:2px">' + m.label + ' · ' + when + '</div></div>' +
        '<div style="font-size:15px;font-weight:700;color:#0C831F">' + rs(amount) + '</div></div>' +
      '<div style="padding:4px 12px 8px">' +
        '<div style="font-size:9.5px;font-weight:700;color:#9E9E9E;text-transform:uppercase;letter-spacing:.6px;margin:6px 0 2px">Paid by</div>' +
        m.rows.map(function (r) {
          return '<div style="display:flex;align-items:center;justify-content:space-between;gap:10px;padding:5px 0;border-top:1px dashed #EFEFEF;font-size:12px">' +
            '<span style="color:#707070;flex-shrink:0">' + r[0] + '</span>' +
            '<span style="display:flex;align-items:center;gap:6px;min-width:0;color:#1C1C1C;font-weight:600;text-align:right;word-break:break-all">' + r[1] +
            (r[2] ? '<button type="button" onclick="pdCopy(this,\'' + r[1] + '\')" style="border:none;background:none;padding:0;cursor:pointer;display:flex" aria-label="Copy">' + ICON.copy + '</button>' : '') +
            '</span></div>';
        }).join('') +
      '</div></div>';
  }
  /* money that is still to come, or was taken in cash */
  function due(title, amount, sub, done) {
    return '<div style="display:flex;align-items:center;gap:10px;padding:10px 12px;margin-top:10px;border-radius:10px;' +
      (done ? 'border:1px solid #EDEDED;background:#fff' : 'border:1px dashed #E6C878;background:#FFFBF0') + '">' +
      '<div style="width:34px;height:34px;border-radius:9px;background:#FFF4DC;display:flex;align-items:center;justify-content:center;flex-shrink:0">' + ICON.cash + '</div>' +
      '<div style="flex:1;min-width:0;line-height:1.25"><div style="font-size:13px;font-weight:600;color:#1C1C1C">' + title + '</div>' +
      '<div style="font-size:11px;color:#707070;margin-top:2px">' + sub + '</div></div>' +
      '<div style="font-size:15px;font-weight:700;color:' + (done ? '#0C831F' : '#8B6914') + '">' + rs(amount) + '</div></div>';
  }

  var head, body = '', tl;
  if (pay === 'prepaid') {
    head = ['Prepaid · paid online', pill('Paid', 'ok')];
    body = leg('Paid online', total, placedAt, UPI);
    tl = 'UPI payment confirmed';
  } else if (pay === 'partial') {
    var now = Math.round(total / 2), rest = total - now;
    head = ['Partial payment · 50% now', delivered ? pill('Fully paid', 'ok') : pill(rs(rest) + ' due', 'due')];
    body =
      '<div style="margin-top:10px"><div style="height:6px;border-radius:6px;background:#F1E6C8;overflow:hidden"><div style="height:100%;width:' + (delivered ? 100 : 50) + '%;background:#0C831F;border-radius:6px"></div></div>' +
      '<div style="display:flex;justify-content:space-between;font-size:11px;margin-top:5px"><span style="color:#0C831F;font-weight:600">' + rs(delivered ? total : now) + ' paid</span><span style="color:' + (delivered ? '#9E9E9E' : '#8B6914') + ';font-weight:600">' + (delivered ? 'Nothing due' : rs(rest) + ' at delivery') + '</span></div></div>' +
      leg('Advance paid online', now, placedAt, CARD) +
      (delivered ? due('Balance collected on delivery', rest, 'Cash · ' + doneAt, true)
                 : due('Balance to pay on delivery', rest, 'Cash or UPI to the delivery partner', false));
    tl = '50% paid online (' + rs(now) + ') · ' + rs(rest) + ' on delivery';
  } else {
    head = ['Cash on Delivery', delivered ? pill('Paid', 'ok') : pill('Pay on delivery', 'due')];
    body = delivered
      ? leg('Paid on delivery', total, doneAt, QR)
      : due('To pay on delivery', total, 'Cash or UPI to the delivery partner', false) +
        '<div style="font-size:11px;color:#909090;margin-top:8px;line-height:1.45">Payer details show here once the delivery partner collects the money.</div>';
    tl = 'Cash on Delivery · ' + rs(total) + ' to pay';
  }

  slot.innerHTML =
    '<div style="margin:12px 16px 0;background:#fff;border:1px solid #EDEDED;border-radius:10px;padding:14px;font-family:Poppins,sans-serif">' +
      '<div style="display:flex;align-items:center;justify-content:space-between;gap:8px">' +
        '<div style="line-height:1.2"><div style="font-size:14px;font-weight:600;color:#1C1C1C">Payment details</div>' +
        '<div style="font-size:11px;color:#707070;margin-top:2px">' + head[0] + '</div></div>' + head[1] + '</div>' +
      body +
      '<div style="display:flex;align-items:center;justify-content:space-between;margin-top:10px">' +
        '<span style="font-size:10px;color:#9E9E9E">Payment details from Razorpay</span>' +
        (delivered ? '<a href="#" style="display:flex;align-items:center;gap:5px;background:#F8F8F8;border:1px solid #EDEDED;border-radius:8px;padding:6px 10px;font-size:11px;font-weight:600;color:#1C1C1C;text-transform:uppercase;letter-spacing:.4px;text-decoration:none">' + ICON.doc + 'Invoice</a>' : '') +
      '</div></div>';

  /* keep the rest of the page in step with the case */
  document.querySelectorAll('[data-pay-hide]').forEach(function (el) { el.style.display = 'none'; });
  document.querySelectorAll('[data-pay-tl]').forEach(function (el) { el.textContent = el.getAttribute('data-pay-tl') + ' · ' + tl; });
  document.querySelectorAll('[data-pay-total-label]').forEach(function (el) {
    el.textContent = (pay === 'prepaid' || delivered) ? el.textContent : 'Order Total';
  });

  /* gallery thumbnails: ?focus=pay scrolls only the screen's own scroller to the card */
  if (new URLSearchParams(location.search).get('focus') === 'pay') {
    setTimeout(function () {
      var sa = document.querySelector('.scroll-area');
      if (sa) sa.scrollTop = slot.getBoundingClientRect().top - sa.getBoundingClientRect().top + sa.scrollTop - 70;
    }, 400);
  }

  window.pdCopy = function (btn, v) {
    try { navigator.clipboard.writeText(v); } catch (e) {}
    btn.innerHTML = '<span style="font-size:10px;color:#0C831F;font-weight:700">Copied</span>';
    setTimeout(function () { btn.innerHTML = ICON.copy; }, 1200);
  };
})();
