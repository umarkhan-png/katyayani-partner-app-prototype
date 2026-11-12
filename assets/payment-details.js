/* Phase 3 · Payment details — a simple add-on list on Order Status (order-tracking) and Order Details.
   Turned on only by ?pay=prepaid|partial|cod — without it both pages stay as they were.
   Rows mirror what the Razorpay payment entity returns:
   method, vpa / card (network, last4, name) / bank, contact, id (pay_…), acquirer_data.rrn, created_at. */
(function () {
  var qs = new URLSearchParams(location.search);
  var pay = qs.get('pay');
  var slot = document.querySelector('[data-pay-slot]');
  if (!slot || ['prepaid', 'partial', 'cod'].indexOf(pay) < 0) return;

  var delivered = slot.getAttribute('data-stage') === 'delivered';
  var total = +slot.getAttribute('data-total');
  var placedAt = slot.getAttribute('data-placed');
  var doneAt = slot.getAttribute('data-delivered') || '';
  var rs = function (n) { return '₹' + Math.round(n).toLocaleString('en-IN'); };
  var half = Math.round(total / 2), rest = total - half;

  var UPI  = [['UPI ID', 'ramesh.patel@okhdfcbank'], ['Bank', 'HDFC Bank'], ['Mobile', '+91 98260 •••45'], ['Payment ID', 'pay_PQ7xK2mLsa91Bd', 1], ['UTR / RRN', '412398765432', 1]];
  var CARD = [['Card', 'Visa •••• 4321'], ['Name on card', 'RAMESH PATEL'], ['Bank', 'HDFC Bank'], ['Payment ID', 'pay_PQ8bR4tWnc22Lk', 1]];
  var QR   = [['UPI ID', 'rameshks@ybl'], ['Bank', 'State Bank of India'], ['Payment ID', 'pay_PR1dE9vYqk05Ma', 1], ['UTR / RRN', '412455501873', 1]];

  /* summary line (existing card on Order Details) + rows */
  var title, sub, rows, tl;
  if (pay === 'prepaid') {
    title = 'Paid via UPI'; sub = 'HDFC ••7842 · ' + placedAt;
    rows = [['Paid online', rs(total) + ' · ' + placedAt]].concat(UPI);
    tl = 'UPI payment confirmed';
  } else if (pay === 'partial') {
    title = 'Partial payment'; sub = rs(half) + ' online · ' + rs(rest) + (delivered ? ' paid on delivery' : ' on delivery');
    rows = [['Paid online', rs(half) + ' · ' + placedAt]].concat(CARD,
           [[delivered ? 'Paid on delivery' : 'To pay on delivery', rs(rest) + (delivered ? ' · Cash · ' + doneAt : ''), 0, !delivered]]);
    tl = rs(half) + ' paid online · ' + rs(rest) + ' on delivery';
  } else {
    title = 'Cash on Delivery'; sub = delivered ? 'Paid by UPI at delivery · ' + doneAt : rs(total) + ' to pay on delivery';
    rows = delivered ? [['Paid on delivery', rs(total) + ' · ' + doneAt]].concat(QR)
                     : [['To pay on delivery', rs(total), 0, true]];
    tl = 'Cash on Delivery';
  }

  var copyIco = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#0E7A4E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 012-2h10"/></svg>';
  slot.innerHTML =
    '<div style="margin:12px 16px 0;background:#fff;border:1px solid #EDEDED;border-radius:10px;padding:12px 14px;font-family:Poppins,sans-serif">' +
      '<div style="font-size:14px;font-weight:600;color:#1C1C1C;margin-bottom:4px">Payment details</div>' +
      rows.map(function (r, i) {
        return '<div style="display:flex;align-items:center;justify-content:space-between;gap:10px;padding:6px 0;' + (i ? 'border-top:1px dashed #EFEFEF;' : '') + 'font-size:12px">' +
          '<span style="color:#707070;flex-shrink:0">' + r[0] + '</span>' +
          '<span style="display:flex;align-items:center;gap:6px;min-width:0;text-align:right;word-break:break-all;font-weight:600;color:' + (r[3] ? '#8B6914' : '#1C1C1C') + '">' + r[1] +
          (r[2] ? '<button type="button" onclick="pdCopy(this,\'' + r[1] + '\')" style="border:none;background:none;padding:0;cursor:pointer;display:flex" aria-label="Copy">' + copyIco + '</button>' : '') +
          '</span></div>';
      }).join('') +
      (rows.some(function (r) { return r[2]; }) ? '<div style="font-size:10px;color:#9E9E9E;margin-top:4px">From Razorpay</div>' : '') +
    '</div>';

  /* keep the existing summary card, the timeline line and the total label in step with the case */
  var t = document.querySelector('[data-pay-title]'), s = document.querySelector('[data-pay-sub]');
  if (t) t.textContent = title;
  if (s) s.textContent = sub;
  document.querySelectorAll('[data-pay-tl]').forEach(function (el) { el.textContent = el.getAttribute('data-pay-tl') + ' · ' + tl; });
  document.querySelectorAll('[data-pay-total-label]').forEach(function (el) {
    if (!(pay === 'prepaid' || delivered)) el.textContent = 'Order Total';
  });

  /* gallery thumbnails: ?focus=pay scrolls only the screen's own scroller to the details */
  if (qs.get('focus') === 'pay') {
    setTimeout(function () {
      var sa = document.querySelector('.scroll-area');
      if (sa) sa.scrollTop = slot.getBoundingClientRect().top - sa.getBoundingClientRect().top + sa.scrollTop - 150;
    }, 400);
  }

  window.pdCopy = function (btn, v) {
    try { navigator.clipboard.writeText(v); } catch (e) {}
    btn.innerHTML = '<span style="font-size:10px;color:#0C831F;font-weight:700">Copied</span>';
    setTimeout(function () { btn.innerHTML = copyIco; }, 1200);
  };
})();
