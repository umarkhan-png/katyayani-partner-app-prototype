/* =========================================================================
   P — portal shell runtime.
   Renders sidebar + topbar, owns the global filter state, and gives pages
   helpers for KPIs, tables, CSV export, drawers and the command palette.
   ========================================================================= */
(function (global) {
  'use strict';

  var NAV = [
    { g: 'Dashboard', items: [
      { h: 'index.html',        t: 'Overview',              i: 'grid' },
      { h: 'insights.html',     t: 'Insights & Goals',      i: 'bulb', badge: 6 }
    ]},
    { g: 'Acquisition', items: [
      { h: 'attribution.html',  t: 'MMP · Attribution',     i: 'link', nw: 'MMP' },
      { h: 'funnel.html',       t: 'Register → Verify',     i: 'funnel' }
    ]},
    { g: 'Commerce', items: [
      { h: 'discovery.html',    t: 'Discovery & Search',    i: 'search' },
      { h: 'commerce.html',     t: 'Cart & Checkout',       i: 'cart' },
      { h: 'fulfilment.html',   t: 'Orders & Delivery',     i: 'truck' }
    ]},
    { g: 'Product usage', items: [
      { h: 'explore.html',      t: 'Explore Features',      i: 'compass' },
      { h: 'farmers.html',      t: 'Farmers & Inventory',   i: 'leaf', nw: 'NEW' },
      { h: 'engagement.html',   t: 'Engagement & Retention',i: 'pulse' },
      { h: 'journeys.html',     t: 'Journeys & Flows',      i: 'route' }
    ]},
    { g: 'Partners', items: [
      { h: 'segments.html',     t: 'Segments & Cohorts',    i: 'layers' },
      { h: 'partners.html',     t: 'Partner Explorer',      i: 'user' }
    ]},
    { g: 'Platform', items: [
      { h: 'experiments.html',  t: 'Experiments & Flags',   i: 'flask' },
      { h: 'ratings.html',      t: 'Ratings & Reviews',     i: 'star', nw: 'NEW' },
      { h: 'health.html',       t: 'App Health',            i: 'heart' }
    ]}
  ];

  var ICONS = {
    grid:   '<path d="M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z"/>',
    bulb:   '<path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/>',
    link:   '<path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/>',
    funnel: '<path d="M3 4h18l-7 8v7l-4 2v-9z"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    cart:   '<circle cx="9" cy="20" r="1.6"/><circle cx="18" cy="20" r="1.6"/><path d="M2 3h3l2.7 12h11L21 7H6"/>',
    truck:  '<path d="M2 7h11v9H2zM13 10h4l4 3v3h-8"/><circle cx="6" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/>',
    compass:'<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    pulse:  '<path d="M2 12h4l3-8 4 16 3-8h6"/>',
    route:  '<circle cx="5" cy="19" r="2.4"/><circle cx="19" cy="5" r="2.4"/><path d="M7.5 19H14a4 4 0 0 0 0-8H9a4 4 0 0 1 0-8h2"/>',
    layers: '<path d="M12 2l9 5-9 5-9-5z"/><path d="M3 12l9 5 9-5M3 17l9 5 9-5"/>',
    user:   '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/>',
    flask:  '<path d="M9 2h6M10 2v6L4 19a2 2 0 0 0 2 3h12a2 2 0 0 0 2-3l-6-11V2"/><path d="M7 15h10"/>',
    heart:  '<path d="M12 20s-8-4.9-8-10a4.7 4.7 0 0 1 8-3 4.7 4.7 0 0 1 8 3c0 5.1-8 10-8 10z"/>',
    down:   '<path d="M12 5v14M19 12l-7 7-7-7"/>',
    up:     '<path d="M12 19V5M5 12l7-7 7 7"/>',
    x:      '<path d="M18 6L6 18M6 6l12 12"/>',
    dl:     '<path d="M12 3v12M7 11l5 5 5-5M4 21h16"/>',
    ref:    '<path d="M21 12a9 9 0 1 1-3-6.7M21 4v5h-5"/>',
    ext:    '<path d="M14 3h7v7M21 3l-9 9M19 14v6H4V5h6"/>',
    info:   '<circle cx="12" cy="12" r="9"/><path d="M12 16v-5M12 8h.01"/>',
    alert:  '<path d="M12 3l9.5 17H2.5z"/><path d="M12 10v4M12 17h.01"/>',
    check:  '<path d="M20 6L9 17l-5-5"/>',
    flag:   '<path d="M4 21V4h12l-1.5 4L16 12H4"/>',
    clock:  '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l4 2"/>',
    coin:   '<circle cx="12" cy="12" r="9"/><path d="M15 9.5A3 3 0 0 0 9 11c0 3 6 1.5 6 4a3 3 0 0 1-6-1"/>',
    bolt:   '<path d="M13 2L4 14h6l-1 8 9-12h-6z"/>',
    star:   '<path d="M12 3l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 17.8 6.2 20.9l1.1-6.5L2.6 9.8l6.5-.9z"/>',
    leaf:   '<path d="M11 20A7 7 0 0 1 4 13c0-5 4-9 16-9 0 12-4 16-9 16z"/><path d="M4 21c2-8 7-12 12-13"/>',
    box:    '<path d="M21 8l-9-5-9 5v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>'
  };
  function ico(n, c, w) {
    return '<svg width="' + (w || 15) + '" height="' + (w || 15) + '" viewBox="0 0 24 24" fill="none" stroke="' +
      (c || 'currentColor') + '" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">' + (ICONS[n] || '') + '</svg>';
  }

  /* ---------------- filter state ---------------- */
  var DEF = { range: 30, state: 'all', tier: 'all', channel: 'all', segment: 'all', version: 'all', compare: true };
  var st;
  try { st = Object.assign({}, DEF, JSON.parse(localStorage.getItem('ko.pm.filters') || '{}')); }
  catch (e) { st = Object.assign({}, DEF); }
  function save() { try { localStorage.setItem('ko.pm.filters', JSON.stringify(st)); } catch (e) {} }

  var listeners = [];
  function onChange(fn) { listeners.push(fn); }
  function emit() {
    save(); renderChips();
    listeners.forEach(function (f) { try { f(); } catch (e) { console.error('render error', e); } });
  }

  function shareOf(list, id) {
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i].share;
    return 1;
  }
  function mult() {
    var m = 1;
    if (st.state !== 'all')   m *= shareOf(KO.STATES, st.state);
    if (st.tier !== 'all')    m *= shareOf(KO.TIERS, st.tier);
    if (st.channel !== 'all') m *= shareOf(KO.CHANNELS, st.channel);
    if (st.segment !== 'all') m *= shareOf(KO.SEGMENTS, st.segment);
    if (st.version !== 'all') m *= shareOf(KO.VERSIONS, st.version);
    return m;
  }
  function aovIndex() {
    var x = 1;
    if (st.state !== 'all') KO.STATES.forEach(function (s) { if (s.id === st.state) x *= s.aovIx; });
    if (st.tier !== 'all')  KO.TIERS.forEach(function (t) { if (t.id === st.tier) x *= t.aovIx; });
    return x;
  }
  var SCALE_KEYS = ['installs','signupStart','otpDone','profileDone','docsStart','docsSubmit','verified','dau','sessions',
                    'pdpViews','searches','atc','cartViews','checkoutStart','orders','exploreUsers','notifSent','notifOpen',
                    'crashes','returns','cancels','spend','coinsIssued','coinsRedeemed'];
  function scaleRow(r) {
    var m = mult(), ax = aovIndex();
    var o = { d: r.d, apiP95: r.apiP95 };
    SCALE_KEYS.forEach(function (k) { o[k] = Math.round(r[k] * m); });
    o.aov = Math.round(r.aov * ax);
    o.gmv = o.orders * o.aov;
    return o;
  }
  function rows()     { return KO.slice(st.range).map(scaleRow); }
  function prevRows() { return KO.prevSlice(st.range).map(scaleRow); }
  function isFiltered() {
    return st.state !== 'all' || st.tier !== 'all' || st.channel !== 'all' || st.segment !== 'all' || st.version !== 'all';
  }

  /* filtered partner list (client-side, real filtering) */
  function partners() {
    return KO.partners.filter(function (p) {
      if (st.state !== 'all' && p.state !== st.state) return false;
      if (st.tier !== 'all' && p.tier !== st.tier) return false;
      if (st.channel !== 'all' && p.channel !== st.channel) return false;
      if (st.segment !== 'all' && p.segment !== st.segment) return false;
      if (st.version !== 'all' && p.version !== st.version) return false;
      return true;
    });
  }

  /* ---------------- shell render ---------------- */
  var PAGE = (location.pathname.split('/').pop() || 'index.html');
  function buildShell(opts) {
    var side = '<aside class="side">' +
      '<a class="side-brand" href="index.html">' +
        '<div class="lg"><img src="https://www.katyayaniorganics.com/wp-content/uploads/2022/06/cropped-logo-3.webp" alt="Katyayani"></div>' +
        '<div><div class="t">Partner&nbsp;App</div><div class="s">PM Analytics</div></div>' +
      '</a><div class="side-scroll">';
    NAV.forEach(function (grp) {
      side += '<div class="nav-grp">' + grp.g + '</div>';
      grp.items.forEach(function (it) {
        side += '<a class="nav-i' + (it.h === PAGE ? ' on' : '') + '" href="' + it.h + '">' + ico(it.i) +
          '<span>' + it.t + '</span>' +
          (it.nw ? '<span class="nw">' + it.nw + '</span>' : '') +
          (it.badge ? '<span class="bdg">' + it.badge + '</span>' : '') + '</a>';
      });
    });
    side += '</div><div class="side-foot"><div class="u"><div class="av">U</div>' +
      '<div style="min-width:0"><div class="n">Umar</div><div class="r">Product Manager</div></div></div></div></aside>';

    var top = '<header class="top"><div class="top-r1">' +
      '<div style="min-width:0"><h1>' + opts.title + '</h1><div class="sub">' + opts.sub + '</div></div>' +
      '<div class="spacer"></div>' +
      '<span class="live"><i></i>Live · synced 08:41 IST</span>' +
      '<button class="btn" id="pCmd">' + ico('search', '#606060', 13) + ' Search <span class="kbd">Ctrl K</span></button>' +
      '<button class="btn" id="pRef">' + ico('ref', '#606060', 13) + '</button>' +
      '<button class="btn pri" id="pExp">' + ico('dl', '#fff', 13) + ' Export</button>' +
      '</div><div class="top-r2" id="pFilters"></div></header>';

    document.body.insertAdjacentHTML('afterbegin',
      '<div class="shell">' + side + '<div class="main">' + top + '<div class="page" id="pPage"></div></div></div>' +
      '<div class="ovl" id="pOvl"></div>' +
      '<div class="cmd" id="pCmdBox"><input id="pCmdIn" placeholder="Jump to a page, metric, partner or SKU…" autocomplete="off"><div class="cmd-l" id="pCmdList"></div></div>' +
      '<div class="drw" id="pDrw"><div class="drw-h" id="pDrwH"></div><div class="drw-b" id="pDrwB"></div></div>' +
      '<div class="toast" id="pToast"></div>');
  }

  function renderFilters() {
    var RANGES = [7, 30, 90, 180];
    var h = '<div class="seg" id="fRange">';
    RANGES.forEach(function (r) { h += '<button data-r="' + r + '"' + (st.range === r ? ' class="on"' : '') + '>' + r + 'd</button>'; });
    h += '</div>';
    h += sel('fState', 'All states', KO.STATES.map(function (s) { return [s.id, s.name]; }), st.state);
    h += sel('fTier', 'All tiers', KO.TIERS.map(function (t) { return [t.id, t.id]; }), st.tier);
    h += sel('fSeg', 'All segments', KO.SEGMENTS.map(function (s) { return [s.id, s.name]; }), st.segment);
    h += sel('fCh', 'All channels (MMP)', KO.CHANNELS.map(function (c) { return [c.id, c.name]; }), st.channel);
    h += sel('fVer', 'All app versions', KO.VERSIONS.map(function (v) { return [v.id, 'v' + v.id]; }), st.version);
    h += '<span id="fChips" style="display:flex;gap:6px;flex-wrap:wrap"></span>';
    h += '<div class="spacer"></div><span class="hint" style="margin:0" id="fNote"></span>';
    document.getElementById('pFilters').innerHTML = h;

    document.getElementById('fRange').addEventListener('click', function (e) {
      var b = e.target.closest('button[data-r]'); if (!b) return;
      st.range = +b.dataset.r;
      Array.prototype.forEach.call(this.children, function (c) { c.classList.toggle('on', c === b); });
      emit();
    });
    bind('fState', 'state'); bind('fTier', 'tier'); bind('fSeg', 'segment'); bind('fCh', 'channel'); bind('fVer', 'version');
  }
  function sel(id, all, opts, cur) {
    var h = '<select class="sel" id="' + id + '"><option value="all">' + all + '</option>';
    opts.forEach(function (o) { h += '<option value="' + o[0] + '"' + (cur === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; });
    return h + '</select>';
  }
  function bind(id, key) {
    var e = document.getElementById(id);
    if (e) e.addEventListener('change', function () { st[key] = this.value; emit(); });
  }
  function renderChips() {
    var box = document.getElementById('fChips'); if (!box) return;
    var chips = [];
    function label(list, id, key) {
      list.forEach(function (o) { if (o.id === id) chips.push([o.name || o.id, key]); });
    }
    if (st.state !== 'all') label(KO.STATES, st.state, 'state');
    if (st.tier !== 'all') label(KO.TIERS, st.tier, 'tier');
    if (st.segment !== 'all') label(KO.SEGMENTS, st.segment, 'segment');
    if (st.channel !== 'all') label(KO.CHANNELS, st.channel, 'channel');
    if (st.version !== 'all') chips.push(['v' + st.version, 'version']);
    box.innerHTML = chips.map(function (c) {
      return '<span class="chipf">' + c[0] + '<button data-k="' + c[1] + '">&times;</button></span>';
    }).join('') + (chips.length > 1 ? '<span class="chipf" style="background:#FEF2F2;border-color:rgba(226,55,68,.25);color:#E23744">Clear all<button data-k="__all">&times;</button></span>' : '');
    Array.prototype.forEach.call(box.querySelectorAll('button'), function (b) {
      b.addEventListener('click', function () {
        if (b.dataset.k === '__all') { st.state = st.tier = st.segment = st.channel = st.version = 'all'; renderFilters(); }
        else { st[b.dataset.k] = 'all'; renderFilters(); }
        emit();
      });
    });
    var note = document.getElementById('fNote');
    if (note) {
      var n = partners().length;
      note.innerHTML = isFiltered()
        ? 'Filtered slice ≈ <b>' + (mult() * 100).toFixed(1) + '%</b> of base · ' + n + ' partners in sample'
        : 'Full base · ' + KO.partners.length + ' partners in sample · last ' + st.range + ' days vs previous ' + st.range + ' days';
    }
  }

  /* ---------------- KPI helper ---------------- */
  function delta(cur, prev, lowerBetter) {
    if (!prev) return '<span class="delta fl">—</span>';
    var d = (cur - prev) / Math.abs(prev);
    var good = lowerBetter ? d < 0 : d > 0;
    var cls = Math.abs(d) < .002 ? 'fl' : good ? 'up' : 'dn';
    var arrow = Math.abs(d) < .002 ? '' : (d > 0 ? '&#9650;' : '&#9660;');
    return '<span class="delta ' + cls + '">' + arrow + ' ' + (Math.abs(d) * 100).toFixed(1) + '%</span>';
  }
  /* k: {lab, val, prev, cur, fmt, hint, spark:[], sparkColor, hero, gold, lowerBetter, icon} */
  function kpi(k) {
    var id = 'spk' + Math.random().toString(36).slice(2, 8);
    var h = '<div class="kpi' + (k.hero ? ' hero' : k.gold ? ' gold' : '') + '">' +
      '<div class="lab">' + (k.icon ? ico(k.icon, k.hero ? 'rgba(255,255,255,.6)' : '#9E9E9E', 12) : '') + k.lab + '</div>' +
      '<div class="val">' + k.val + '</div>' +
      '<div class="row"><div>' + (k.cur !== undefined ? delta(k.cur, k.prev, k.lowerBetter) : (k.badge || '')) + '</div>' +
      (k.spark ? '<div class="spk" id="' + id + '"></div>' : '') + '</div>' +
      (k.hint ? '<div class="hint">' + k.hint + '</div>' : '') + '</div>';
    if (k.spark) setTimeout(function () {
      KC.spark(document.getElementById(id), { data: k.spark, color: k.sparkColor || (k.hero ? '#8FE3B8' : '#0E7A4E') });
    }, 0);
    return h;
  }
  function kpiRow(host, list, cls) {
    var e = typeof host === 'string' ? document.getElementById(host) : host;
    e.className = 'grid ' + (cls || 'g4');
    e.innerHTML = list.map(kpi).join('');
  }

  /* ---------------- table helper ---------------- */
  /* cols: [{k, l, num, fmt(v,row), cls, sortVal(row), w}] */
  function table(host, o) {
    var e = typeof host === 'string' ? document.getElementById(host) : host;
    if (!e) return;
    var state = { sort: o.sort || (o.cols[0] && o.cols[0].k), dir: o.dir || -1, page: 0, q: '' };
    var size = o.pageSize || 0;

    function data() {
      var d = o.rows.slice();
      if (state.q && o.searchKeys) {
        var q = state.q.toLowerCase();
        d = d.filter(function (r) {
          return o.searchKeys.some(function (k) { return String(r[k] || '').toLowerCase().indexOf(q) >= 0; });
        });
      }
      var c = o.cols.filter(function (c) { return c.k === state.sort; })[0];
      if (c) d.sort(function (a, b) {
        var av = c.sortVal ? c.sortVal(a) : a[c.k], bv = c.sortVal ? c.sortVal(b) : b[c.k];
        if (typeof av === 'string') return state.dir * av.localeCompare(bv);
        return state.dir * ((av || 0) - (bv || 0));
      });
      return d;
    }
    function draw() {
      var d = data();
      var total = d.length;
      var pages = size ? Math.max(1, Math.ceil(total / size)) : 1;
      if (state.page >= pages) state.page = 0;
      var view = size ? d.slice(state.page * size, state.page * size + size) : d;
      var h = '<div class="tblw"><table class="tbl"><thead><tr>';
      o.cols.forEach(function (c) {
        h += '<th class="' + (c.num ? 'num ' : '') + 'sortable' + (state.sort === c.k ? ' act' : '') + '" data-k="' + c.k + '"' +
             (c.w ? ' style="width:' + c.w + '"' : '') + '>' + c.l +
             '<span class="ar">' + (state.sort === c.k ? (state.dir < 0 ? '▼' : '▲') : '▾') + '</span></th>';
      });
      h += '</tr></thead><tbody>';
      if (!view.length) h += '<tr><td colspan="' + o.cols.length + '"><div class="empty">Nothing matches this filter</div></td></tr>';
      view.forEach(function (r, ri) {
        h += '<tr' + (o.onRow ? ' class="clk"' : '') + ' data-i="' + ri + '">';
        o.cols.forEach(function (c) {
          h += '<td class="' + (c.num ? 'num ' : '') + (c.cls || '') + '">' + (c.fmt ? c.fmt(r[c.k], r, ri + state.page * size) : (r[c.k] === undefined ? '—' : r[c.k])) + '</td>';
        });
        h += '</tr>';
      });
      h += '</tbody>';
      if (o.footer) {
        h += '<tfoot><tr>';
        o.cols.forEach(function (c) { h += '<td class="' + (c.num ? 'num' : '') + '">' + (o.footer(c, d) || '') + '</td>'; });
        h += '</tr></tfoot>';
      }
      h += '</table></div>';
      if (size && pages > 1) {
        h += '<div class="pager"><span>' + (state.page * size + 1) + '–' + Math.min(total, (state.page + 1) * size) + ' of ' + total + '</span>' +
             '<div class="spacer"></div>' +
             '<button class="pg" data-p="-1"' + (state.page === 0 ? ' disabled' : '') + '>‹</button>' +
             '<span>' + (state.page + 1) + ' / ' + pages + '</span>' +
             '<button class="pg" data-p="1"' + (state.page >= pages - 1 ? ' disabled' : '') + '>›</button></div>';
      } else if (size) {
        h += '<div class="pager"><span>' + total + ' rows</span></div>';
      }
      e.innerHTML = h;
      Array.prototype.forEach.call(e.querySelectorAll('th[data-k]'), function (th) {
        th.addEventListener('click', function () {
          if (state.sort === th.dataset.k) state.dir *= -1;
          else { state.sort = th.dataset.k; state.dir = -1; }
          draw();
        });
      });
      Array.prototype.forEach.call(e.querySelectorAll('.pg'), function (b) {
        b.addEventListener('click', function () { state.page += +b.dataset.p; draw(); });
      });
      if (o.onRow) Array.prototype.forEach.call(e.querySelectorAll('tbody tr[data-i]'), function (tr) {
        tr.addEventListener('click', function () { o.onRow(view[+tr.dataset.i]); });
      });
    }
    draw();
    return {
      redraw: draw,
      search: function (q) { state.q = q; state.page = 0; draw(); },
      data: data
    };
  }

  /* ---------------- CSV export ---------------- */
  function csv(name, cols, rows) {
    var out = [cols.map(function (c) { return '"' + c.l.replace(/"/g, '""') + '"'; }).join(',')];
    rows.forEach(function (r) {
      out.push(cols.map(function (c) {
        var v = c.raw ? c.raw(r) : r[c.k];
        if (v === undefined || v === null) v = '';
        v = String(v).replace(/<[^>]*>/g, '');
        return '"' + v.replace(/"/g, '""') + '"';
      }).join(','));
    });
    var blob = new Blob(['﻿' + out.join('\r\n')], { type: 'text/csv;charset=utf-8;' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = name.replace(/\s+/g, '-').toLowerCase() + '-' + new Date().toISOString().slice(0, 10) + '.csv';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    toast('Exported ' + rows.length + ' rows to CSV');
  }

  var exportFn = null;
  function setExport(fn) { exportFn = fn; }

  function toast(msg) {
    var t = document.getElementById('pToast');
    t.textContent = msg; t.classList.add('on');
    clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove('on'); }, 2200);
  }

  /* ---------------- drawer ---------------- */
  function drawer(titleHtml, bodyHtml) {
    document.getElementById('pDrwH').innerHTML = titleHtml + '<div class="spacer"></div><button class="x" onclick="P.closeDrawer()">' + ico('x', '#606060', 14) + '</button>';
    document.getElementById('pDrwB').innerHTML = bodyHtml;
    document.getElementById('pDrw').classList.add('on');
    document.getElementById('pOvl').classList.add('on');
  }
  function closeDrawer() {
    document.getElementById('pDrw').classList.remove('on');
    document.getElementById('pOvl').classList.remove('on');
    document.getElementById('pCmdBox').classList.remove('on');
  }

  /* ---------------- command palette ---------------- */
  function cmdItems() {
    var out = [];
    NAV.forEach(function (g) { g.items.forEach(function (i) { out.push({ t: i.t, s: g.g, h: i.h, ic: i.i }); }); });
    KO.tools.forEach(function (t) { out.push({ t: t.name, s: 'Explore tool', h: 'explore.html#' + t.id, ic: 'compass' }); });
    KO.CHANNELS.forEach(function (c) { out.push({ t: c.name, s: 'MMP channel', h: 'attribution.html#' + c.id, ic: 'link' }); });
    KO.products.slice(0, 16).forEach(function (p) { out.push({ t: p.name, s: 'SKU · ' + p.cat, h: 'discovery.html#' + p.sku, ic: 'cart' }); });
    KO.partners.slice(0, 40).forEach(function (p) { out.push({ t: p.name + ' · ' + p.shop, s: 'Partner ' + p.id, h: 'partners.html#' + p.id, ic: 'user' }); });
    KO.screens.forEach(function (s) { out.push({ t: s.n, s: 'Screen · ' + s.s, h: 'journeys.html#' + s.s, ic: 'route' }); });
    if (KO.CROPS) KO.CROPS.forEach(function (c) { out.push({ t: c, s: 'Crop · My Farmers', h: 'farmers.html', ic: 'leaf' }); });
    if (KO.stores) KO.stores.forEach(function (x) { out.push({ t: x.store + ' rating', s: 'Ratings & Reviews', h: 'ratings.html', ic: 'star' }); });
    return out;
  }
  var CMD = null, cmdSel = 0, cmdView = [];
  function openCmd() {
    if (!CMD) CMD = cmdItems();
    document.getElementById('pCmdBox').classList.add('on');
    document.getElementById('pOvl').classList.add('on');
    var i = document.getElementById('pCmdIn'); i.value = ''; i.focus();
    drawCmd('');
  }
  function drawCmd(q) {
    q = q.toLowerCase().trim();
    cmdView = (q ? CMD.filter(function (c) { return (c.t + ' ' + c.s).toLowerCase().indexOf(q) >= 0; }) : CMD.slice(0, 14)).slice(0, 30);
    cmdSel = 0;
    document.getElementById('pCmdList').innerHTML = cmdView.length
      ? cmdView.map(function (c, i) {
          return '<div class="cmd-i' + (i === 0 ? ' on' : '') + '" data-i="' + i + '">' + ico(c.ic, '#0E7A4E', 14) +
                 '<span>' + c.t + '</span><span class="k">' + c.s + '</span></div>';
        }).join('')
      : '<div class="empty">No match</div>';
    Array.prototype.forEach.call(document.querySelectorAll('#pCmdList .cmd-i'), function (d) {
      d.addEventListener('click', function () { location.href = cmdView[+d.dataset.i].h; });
    });
  }

  /* ---------------- insight engine (computed, not hardcoded) ---------------- */
  function autoInsights() {
    var r = rows(), p = prevRows(), out = [];
    function d(k) { var a = KO.sum(r, k), b = KO.sum(p, k); return b ? (a - b) / b : 0; }
    var gmvD = d('gmv'), ordD = d('orders'), instD = d('installs'), verD = d('verified');

    // PDP -> ATC is always the biggest percentage drop and is expected B2B browsing,
    // so the actionable commerce leak is the worst step from the cart onward.
    var f = KO.commerceFunnel(st.range);
    var worst = null;
    f.forEach(function (s, i) { if (i >= 2 && (!worst || s.pctPrevStep < worst.pctPrevStep)) worst = s; });
    // likewise, restrict the onboarding leak to steps inside onboarding (not the first-order step,
    // which already has its own insight card below)
    var rf = KO.regFunnel(st.range);
    var rworst = null;
    rf.forEach(function (s, i) { if (i > 0 && i < rf.length - 1 && (!rworst || s.pctPrevStep < rworst.pctPrevStep)) rworst = s; });

    out.push({
      sev: gmvD > .05 ? 'good' : gmvD < -.03 ? 'crit' : 'info',
      icon: gmvD >= 0 ? 'up' : 'down',
      h: 'GMV ' + (gmvD >= 0 ? 'up' : 'down') + ' ' + KO.fmtPct(Math.abs(gmvD)) + ' vs previous ' + st.range + ' days',
      p: KO.fmtCr(KO.sum(r, 'gmv')) + ' from ' + KO.fmtNum(KO.sum(r, 'orders')) + ' orders · AOV ' + KO.fmtCr(KO.avg(r, 'aov')) +
         '. Orders moved ' + KO.fmtPct(ordD) + ', so the change is ' + (Math.abs(ordD) > Math.abs(gmvD - ordD) ? 'volume-led' : 'basket-led') + '.',
      mt: ['GMV', 'Orders', 'AOV'], go: 'commerce.html'
    });
    out.push({
      sev: 'crit', icon: 'alert',
      h: 'Biggest commerce leak: ' + worst.step + ' (−' + KO.fmtPct(1 - worst.pctPrevStep) + ')',
      p: KO.fmtNum(worst.dropped) + ' sessions lost at this step on ' + worst.where + '. Top stated reason: "' +
         KO.cartDropReasons[0].reason + '" (' + KO.fmtPct(KO.cartDropReasons[0].pct) + ' of drops). Fix on deck: ' + KO.cartDropReasons[0].fix + '.',
      mt: ['Cart & Checkout', 'P0'], go: 'commerce.html'
    });
    out.push({
      sev: 'warn', icon: 'funnel',
      h: 'Onboarding leak: ' + rworst.step + ' (−' + KO.fmtPct(1 - rworst.pctPrevStep) + ')',
      p: 'Only ' + KO.fmtPct(rf[rf.length - 1].value / rf[0].value, 2) + ' of installs reach a first order. ' +
         KO.fmtNum(KO.verifyOps.pendingNow) + ' docs are waiting in the ops queue, ' + KO.verifyOps.slaBreach + ' past the 48h SLA. ' +
         'Top rejection: ' + KO.kycRejects[0].reason + ' (' + KO.fmtPct(KO.kycRejects[0].pct) + ').',
      mt: ['Register → Verify', 'Ops'], go: 'funnel.html'
    });

    // compare like with like — paid channels only, never paid vs owned re-engagement
    var paid = KO.attribution(st.range).filter(function (c) { return c.group === 'Paid' && c.spend > 0; });
    var best = paid.slice().sort(function (a, b) { return b.roas - a.roas; })[0];
    var worstCh = paid.slice().sort(function (a, b) { return a.roas - b.roas; })[0];
    out.push({
      sev: 'good', icon: 'link',
      h: 'Shift paid budget: ' + worstCh.name + ' returns ' + worstCh.roas + '× vs ' + best.name + ' at ' + best.roas + '×',
      p: 'Linkrunner attributes ' + KO.fmtNum(worstCh.installs) + ' installs to ' + worstCh.name + ' at ₹' + KO.fmtNum(worstCh.cac) +
         ' CAC per verified partner (' + worstCh.mRoas + '× on gross margin). Moving 30% of that spend to ' + best.name +
         ' would add roughly ' + KO.fmtCr(worstCh.spend * .3 * (best.roas - worstCh.roas)) + ' of 90-day cohort GMV at current rates.',
      mt: ['MMP · Attribution', 'Growth'], go: 'attribution.html'
    });

    var topTool = KO.tools.slice().sort(function (a, b) { return b.attrGmv / b.users - a.attrGmv / a.users; })[0];
    var lowTool = KO.tools.slice().sort(function (a, b) { return a.adoptTrend - b.adoptTrend; })[0];
    out.push({
      sev: 'info', icon: 'compass',
      h: topTool.name + ' drives ' + KO.fmtCr(topTool.attrGmv / topTool.users) + ' GMV per user — promote it on Home',
      p: topTool.name + ' has only ' + KO.fmtNum(topTool.users) + ' users but ' + KO.fmtPct(topTool.d30) + ' D30 retention. ' +
         'Meanwhile ' + lowTool.name + ' adoption is ' + KO.fmtPct(lowTool.adoptTrend) + ' — consider demoting it in the Explore grid.',
      mt: ['Explore Features'], go: 'explore.html'
    });

    var zero = KO.searchTerms.filter(function (s) { return s.zero; });
    var zeroN = zero.reduce(function (a, b) { return a + b.n; }, 0);
    out.push({
      sev: 'warn', icon: 'search',
      h: KO.fmtNum(zeroN) + ' searches returned nothing — ' + zero.length + ' queries to fix',
      p: 'Biggest gaps: ' + zero.slice(0, 3).map(function (z) { return '"' + z.q + '" (' + KO.fmtK(z.n) + ')'; }).join(', ') +
         '. "sprayer pump" and "seeds hybrid" are catalogue gaps; "illi ki dawai" and "tomato ke liye" are synonym/Hinglish mapping gaps.',
      mt: ['Discovery & Search', 'Catalogue'], go: 'discovery.html'
    });

    var risky = partners().filter(function (p) { return p.churnRisk > .6; });
    var riskyGmv = risky.reduce(function (a, b) { return a + b.gmv; }, 0);
    out.push({
      sev: 'crit', icon: 'user',
      h: risky.length + ' partners at high churn risk — ' + KO.fmtCr(riskyGmv) + ' of lifetime GMV exposed',
      p: 'Slipping Away + Churned segments. Recommended play: ' + KO.SEGMENTS.filter(function (s) { return s.id === 'sleeping'; })[0].action + '.',
      mt: ['Segments', 'Retention'], go: 'segments.html'
    });

    var crash = KO.crashList.filter(function (c) { return c.trend > .2; })[0];
    out.push({
      sev: 'warn', icon: 'heart',
      h: 'Crash regression: ' + crash.sig.split(' · ')[0] + ' up ' + KO.fmtPct(crash.trend),
      p: KO.fmtNum(crash.n) + ' crashes hitting ' + KO.fmtNum(crash.users) + ' partners on ' + crash.screen +
         ' (' + crash.ver + '). Crash-free sessions at ' + KO.fmtPct(KO.appHealth.crashFree, 2) + ' vs 99.9% target.',
      mt: ['App Health', 'Eng'], go: 'health.html'
    });

    var mm = KO.sdkHealth;
    if (mm.eventsMissing.length) out.push({
      sev: 'warn', icon: 'link',
      h: mm.eventsMissing.length + ' Linkrunner events are not firing',
      p: 'Missing: ' + mm.eventsMissing.join(', ') + '. Until these fire, cohort and ROAS attribution for those flows is blind. ' +
         'SDK v' + mm.sdkVersion + ' installed, v' + mm.latestVersion + ' available.',
      mt: ['MMP · Attribution', 'Eng'], go: 'attribution.html'
    });

    return out;
  }
  function insightCard(i) {
    return '<a class="ins ' + i.sev + '" href="' + (i.go || '#') + '">' +
      '<div class="ic">' + ico(i.icon, i.sev === 'crit' ? '#E23744' : i.sev === 'warn' ? '#E08A1E' : i.sev === 'good' ? '#0C831F' : '#2563EB', 15) + '</div>' +
      '<div style="min-width:0"><h4>' + i.h + '</h4><p>' + i.p + '</p>' +
      (i.mt ? '<div class="mt">' + i.mt.map(function (m) { return '<span>' + m + '</span>'; }).join('') + '</div>' : '') +
      '</div></a>';
  }

  /* ---------------- tabs ---------------- */
  function tabs(host, list, onPick) {
    var e = typeof host === 'string' ? document.getElementById(host) : host;
    e.className = 'tabs';
    e.innerHTML = list.map(function (t, i) { return '<button data-i="' + i + '"' + (i === 0 ? ' class="on"' : '') + '>' + t + '</button>'; }).join('');
    e.addEventListener('click', function (ev) {
      var b = ev.target.closest('button[data-i]'); if (!b) return;
      Array.prototype.forEach.call(e.children, function (c) { c.classList.toggle('on', c === b); });
      onPick(+b.dataset.i);
    });
    onPick(0);
  }

  function sectionTitle(t, note) {
    return '<div class="sec-t">' + t + '<span class="ln"></span>' + (note ? '<span class="n">' + note + '</span>' : '') + '</div>';
  }
  function card(title, desc, bodyId, actions, cls) {
    return '<div class="card ' + (cls || '') + '">' +
      '<div class="card-h"><div style="min-width:0"><h3>' + title + '</h3>' + (desc ? '<div class="d">' + desc + '</div>' : '') + '</div>' +
      '<div class="spacer"></div>' + (actions || '') + '</div>' +
      '<div class="card-b" id="' + bodyId + '"></div></div>';
  }

  /* ---------------- boot ---------------- */
  function init(opts) {
    buildShell(opts);
    renderFilters(); renderChips();
    document.getElementById('pRef').addEventListener('click', function () { emit(); toast('Refreshed from source'); });
    document.getElementById('pExp').addEventListener('click', function () {
      if (exportFn) exportFn();
      else csv(opts.title, [{ k: 'd', l: 'Date' }, { k: 'installs', l: 'Installs' }, { k: 'verified', l: 'Verified' },
        { k: 'dau', l: 'DAU' }, { k: 'orders', l: 'Orders' }, { k: 'gmv', l: 'GMV' }, { k: 'aov', l: 'AOV' }], rows());
    });
    document.getElementById('pCmd').addEventListener('click', openCmd);
    document.getElementById('pOvl').addEventListener('click', closeDrawer);
    document.getElementById('pCmdIn').addEventListener('input', function () { drawCmd(this.value); });
    document.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openCmd(); return; }
      if (e.key === 'Escape') closeDrawer();
      if (!document.getElementById('pCmdBox').classList.contains('on')) return;
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        cmdSel = Math.max(0, Math.min(cmdView.length - 1, cmdSel + (e.key === 'ArrowDown' ? 1 : -1)));
        Array.prototype.forEach.call(document.querySelectorAll('#pCmdList .cmd-i'), function (d, i) { d.classList.toggle('on', i === cmdSel); });
      }
      if (e.key === 'Enter' && cmdView[cmdSel]) location.href = cmdView[cmdSel].h;
    });
    var ro = null;
    window.addEventListener('resize', function () { clearTimeout(ro); ro = setTimeout(emit, 220); });
    return document.getElementById('pPage');
  }

  global.P = {
    init: init, onChange: onChange, emit: emit, state: st,
    rows: rows, prevRows: prevRows, mult: mult, isFiltered: isFiltered, partners: partners,
    kpi: kpi, kpiRow: kpiRow, delta: delta, table: table, csv: csv, setExport: setExport,
    drawer: drawer, closeDrawer: closeDrawer, toast: toast, tabs: tabs,
    sectionTitle: sectionTitle, card: card, ico: ico,
    autoInsights: autoInsights, insightCard: insightCard,
    range: function () { return st.range; }
  };
})(window);
