/* =========================================================================
   KC — tiny SVG chart library for the PM portal.
   No dependencies. Every chart: responsive, tooltip on hover, theme-locked.
   ========================================================================= */
(function (global) {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';
  var PAL = ['#0E7A4E', '#D4A537', '#2563EB', '#7C5CFF', '#0E9C8F', '#E23744', '#E08A1E', '#5B6670'];

  /* ---------------- tooltip ---------------- */
  var tipEl = null;
  function tip() {
    if (!tipEl) { tipEl = document.createElement('div'); tipEl.id = 'tip'; document.body.appendChild(tipEl); }
    return tipEl;
  }
  function showTip(html, x, y) {
    var t = tip(); t.innerHTML = html; t.classList.add('on');
    var r = t.getBoundingClientRect();
    var left = x + 14, top = y - r.height - 10;
    if (left + r.width > window.innerWidth - 8) left = x - r.width - 14;
    if (top < 8) top = y + 16;
    t.style.left = left + 'px'; t.style.top = top + 'px';
  }
  function hideTip() { if (tipEl) tipEl.classList.remove('on'); }
  document.addEventListener('scroll', hideTip, true);

  /* ---------------- helpers ---------------- */
  function el(tag, attrs) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) if (attrs[k] !== null && attrs[k] !== undefined) n.setAttribute(k, attrs[k]);
    return n;
  }
  function mk(host, w, h) {
    host.innerHTML = '';
    var svg = el('svg', { class: 'chart', viewBox: '0 0 ' + w + ' ' + h, preserveAspectRatio: 'none', height: h });
    svg.style.height = h + 'px';
    host.appendChild(svg);
    return svg;
  }
  function nice(max) {
    if (max <= 0) return 1;
    var p = Math.pow(10, Math.floor(Math.log10(max)));
    var n = max / p;
    var m = n <= 1 ? 1 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 5 ? 5 : 10;
    return m * p;
  }
  function idf(v) { return v; }
  function width(host) { return Math.max(240, host.clientWidth || host.parentElement.clientWidth || 600); }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }

  /* =====================================================================
     LINE / AREA
     opts: series[{name,color,data:[n]}], labels[], height, yFmt, area, yMin0
     ===================================================================== */
  function line(host, o) {
    if (!host) return;
    o = o || {};
    var H = o.height || 220, W = width(host);
    var yFmt = o.yFmt || idf;
    var pad = { t: 12, r: 10, b: 22, l: o.left === undefined ? 46 : o.left };
    var svg = mk(host, W, H);
    var series = o.series || [], labels = o.labels || [];
    if (!series.length || !series[0].data.length) { host.innerHTML = '<div class="empty">No data</div>'; return; }
    var n = series[0].data.length;

    var max = 0, min = Infinity;
    series.forEach(function (s) { s.data.forEach(function (v) { if (v > max) max = v; if (v < min) min = v; }); });
    if (o.yMin0 !== false) min = 0;
    max = nice(max * 1.06);
    if (min === max) max = min + 1;
    var iw = W - pad.l - pad.r, ih = H - pad.t - pad.b;
    var X = function (i) { return pad.l + (n === 1 ? iw / 2 : (i / (n - 1)) * iw); };
    var Y = function (v) { return pad.t + ih - ((v - min) / (max - min)) * ih; };

    // gridlines
    for (var g = 0; g <= 4; g++) {
      var gv = min + (max - min) * (g / 4), gy = Y(gv);
      svg.appendChild(el('line', { x1: pad.l, x2: W - pad.r, y1: gy, y2: gy, stroke: g === 0 ? '#E4E7E6' : '#F2F4F3', 'stroke-width': 1 }));
      var tx = el('text', { x: pad.l - 7, y: gy + 3.5, 'text-anchor': 'end', fill: '#9E9E9E', 'font-size': 9, 'font-weight': 600 });
      tx.textContent = yFmt(gv); svg.appendChild(tx);
    }
    // x labels (max 7)
    var stepL = Math.max(1, Math.ceil(n / 7));
    for (var i = 0; i < n; i += stepL) {
      var t2 = el('text', { x: X(i), y: H - 6, 'text-anchor': 'middle', fill: '#9E9E9E', 'font-size': 9, 'font-weight': 600 });
      t2.textContent = labels[i] || (i + 1); svg.appendChild(t2);
    }

    series.forEach(function (s, si) {
      var col = s.color || PAL[si % PAL.length];
      var d = '', ad = '';
      s.data.forEach(function (v, i) { d += (i ? ' L' : 'M') + X(i).toFixed(1) + ' ' + Y(v).toFixed(1); });
      if (o.area !== false && si === 0) {
        ad = d + ' L' + X(n - 1).toFixed(1) + ' ' + (pad.t + ih) + ' L' + X(0).toFixed(1) + ' ' + (pad.t + ih) + ' Z';
        var gid = 'lg' + Math.random().toString(36).slice(2, 8);
        var defs = el('defs', {});
        var lg = el('linearGradient', { id: gid, x1: 0, y1: 0, x2: 0, y2: 1 });
        lg.appendChild(el('stop', { offset: '0%', 'stop-color': col, 'stop-opacity': .22 }));
        lg.appendChild(el('stop', { offset: '100%', 'stop-color': col, 'stop-opacity': 0 }));
        defs.appendChild(lg); svg.appendChild(defs);
        svg.appendChild(el('path', { d: ad, fill: 'url(#' + gid + ')' }));
      }
      svg.appendChild(el('path', {
        d: d, fill: 'none', stroke: col, 'stroke-width': s.dash ? 1.6 : 2,
        'stroke-dasharray': s.dash ? '4 3' : null, 'stroke-linejoin': 'round', 'stroke-linecap': 'round'
      }));
    });

    // hover layer
    var guide = el('line', { y1: pad.t, y2: pad.t + ih, stroke: '#0E7A4E', 'stroke-width': 1, 'stroke-dasharray': '3 3', opacity: 0 });
    svg.appendChild(guide);
    var dots = series.map(function (s, si) {
      var c = el('circle', { r: 4, fill: '#fff', stroke: s.color || PAL[si % PAL.length], 'stroke-width': 2.2, opacity: 0 });
      svg.appendChild(c); return c;
    });
    var hit = el('rect', { x: pad.l, y: pad.t, width: iw, height: ih, fill: 'transparent' });
    svg.appendChild(hit);
    hit.addEventListener('mousemove', function (e) {
      var bb = svg.getBoundingClientRect();
      var rx = (e.clientX - bb.left) / bb.width * W;
      var idx = Math.round((rx - pad.l) / (iw || 1) * (n - 1));
      idx = Math.max(0, Math.min(n - 1, idx));
      guide.setAttribute('x1', X(idx)); guide.setAttribute('x2', X(idx)); guide.setAttribute('opacity', .6);
      var html = '<div class="th">' + esc(labels[idx] || ('#' + (idx + 1))) + '</div>';
      series.forEach(function (s, si) {
        dots[si].setAttribute('cx', X(idx)); dots[si].setAttribute('cy', Y(s.data[idx])); dots[si].setAttribute('opacity', 1);
        html += '<div class="tr"><i style="background:' + (s.color || PAL[si % PAL.length]) + '"></i><span>' + esc(s.name) + '</span><b>' + yFmt(s.data[idx]) + '</b></div>';
      });
      showTip(html, e.clientX, e.clientY);
    });
    hit.addEventListener('mouseleave', function () {
      guide.setAttribute('opacity', 0); dots.forEach(function (d) { d.setAttribute('opacity', 0); }); hideTip();
    });
  }

  /* =====================================================================
     BARS (vertical, grouped or stacked)
     ===================================================================== */
  function bars(host, o) {
    if (!host) return;
    o = o || {};
    var H = o.height || 220, W = width(host), yFmt = o.yFmt || idf;
    var pad = { t: 12, r: 10, b: 24, l: o.left === undefined ? 46 : o.left };
    var svg = mk(host, W, H);
    var labels = o.labels || [], series = o.series || [];
    if (!labels.length) { host.innerHTML = '<div class="empty">No data</div>'; return; }
    var n = labels.length, ns = series.length;
    var max = 0;
    if (o.stacked) {
      for (var i = 0; i < n; i++) { var t = 0; series.forEach(function (s) { t += s.data[i] || 0; }); if (t > max) max = t; }
    } else series.forEach(function (s) { s.data.forEach(function (v) { if (v > max) max = v; }); });
    max = nice(max * 1.08) || 1;
    var iw = W - pad.l - pad.r, ih = H - pad.t - pad.b;
    var slot = iw / n, gap = Math.min(14, slot * .28);
    var bw = o.stacked ? (slot - gap) : (slot - gap) / ns;
    var Y = function (v) { return pad.t + ih - (v / max) * ih; };

    for (var g = 0; g <= 4; g++) {
      var gy = pad.t + ih - (g / 4) * ih;
      svg.appendChild(el('line', { x1: pad.l, x2: W - pad.r, y1: gy, y2: gy, stroke: g === 0 ? '#E4E7E6' : '#F2F4F3', 'stroke-width': 1 }));
      var tx = el('text', { x: pad.l - 7, y: gy + 3.5, 'text-anchor': 'end', fill: '#9E9E9E', 'font-size': 9, 'font-weight': 600 });
      tx.textContent = yFmt(max * g / 4); svg.appendChild(tx);
    }

    labels.forEach(function (lab, i) {
      var x0 = pad.l + i * slot + gap / 2, acc = 0;
      series.forEach(function (s, si) {
        var v = s.data[i] || 0;
        var col = s.color || PAL[si % PAL.length];
        var bx = o.stacked ? x0 : x0 + si * bw;
        var by = o.stacked ? Y(acc + v) : Y(v);
        var bh = Math.max(v > 0 ? 1.5 : 0, (v / max) * ih);
        var r = el('rect', { x: bx.toFixed(1), y: by.toFixed(1), width: Math.max(1, bw - (o.stacked ? 0 : 1.5)).toFixed(1), height: bh.toFixed(1), fill: col, rx: 3 });
        r.style.cursor = 'pointer';
        r.addEventListener('mousemove', function (e) {
          var html = '<div class="th">' + esc(lab) + '</div>';
          if (o.stacked) {
            var tot = 0; series.forEach(function (ss) { tot += ss.data[i] || 0; });
            series.forEach(function (ss, j) {
              html += '<div class="tr"><i style="background:' + (ss.color || PAL[j % PAL.length]) + '"></i><span>' + esc(ss.name) + '</span><b>' + yFmt(ss.data[i]) + '</b></div>';
            });
            html += '<div class="tr" style="margin-top:3px;border-top:1px solid rgba(255,255,255,.15);padding-top:3px"><span>Total</span><b>' + yFmt(tot) + '</b></div>';
          } else {
            html += '<div class="tr"><i style="background:' + col + '"></i><span>' + esc(s.name) + '</span><b>' + yFmt(v) + '</b></div>';
          }
          showTip(html, e.clientX, e.clientY);
        });
        r.addEventListener('mouseleave', hideTip);
        svg.appendChild(r);
        acc += v;
      });
      if (n <= 14 || i % Math.ceil(n / 12) === 0) {
        var t3 = el('text', { x: (x0 + (slot - gap) / 2).toFixed(1), y: H - 7, 'text-anchor': 'middle', fill: '#9E9E9E', 'font-size': 9, 'font-weight': 600 });
        t3.textContent = lab.length > 11 ? lab.slice(0, 10) + '…' : lab; svg.appendChild(t3);
      }
    });
  }

  /* =====================================================================
     HORIZONTAL BARS (DOM based — labels stay readable)
     rows: [{label, value, color, sub, pillHtml}]
     ===================================================================== */
  function hbars(host, o) {
    if (!host) return;
    o = o || {};
    var rows = o.rows || [], fmt = o.fmt || idf;
    var max = o.max || Math.max.apply(null, rows.map(function (r) { return r.value; }).concat([1]));
    var h = '<div class="stat-l">';
    rows.forEach(function (r, i) {
      var w = Math.max(1.5, (r.value / max) * 100);
      h += '<div>';
      h += '<div class="stat-r" style="margin-bottom:4px">';
      if (o.rank) h += '<span class="rank' + (i === 0 ? ' t1' : '') + '">' + (i + 1) + '</span>';
      h += '<span class="nm" title="' + esc(r.label) + '">' + esc(r.label) + (r.sub ? ' <span style="color:#9E9E9E;font-weight:500">· ' + esc(r.sub) + '</span>' : '') + '</span>';
      h += '<span class="vl">' + fmt(r.value) + '</span>';
      if (r.pillHtml) h += r.pillHtml;
      h += '</div>';
      h += '<div class="meter"><i style="width:' + w.toFixed(1) + '%;background:' + (r.color || '#0E7A4E') + '"></i></div>';
      h += '</div>';
    });
    h += '</div>';
    host.innerHTML = rows.length ? h : '<div class="empty">No data</div>';
  }

  /* =====================================================================
     DONUT
     ===================================================================== */
  function donut(host, o) {
    if (!host) return;
    o = o || {};
    var data = (o.data || []).filter(function (d) { return d.value > 0; });
    var size = o.size || 168, sw = o.thickness || 22;
    host.innerHTML = '';
    var wrap = document.createElement('div');
    wrap.style.cssText = 'display:flex;align-items:center;gap:16px;flex-wrap:wrap';
    var svgBox = document.createElement('div');
    svgBox.style.cssText = 'position:relative;flex:0 0 ' + size + 'px;width:' + size + 'px;height:' + size + 'px';
    var svg = el('svg', { viewBox: '0 0 ' + size + ' ' + size, width: size, height: size });
    var total = data.reduce(function (a, b) { return a + b.value; }, 0) || 1;
    var R = size / 2 - sw / 2, cx = size / 2, cy = size / 2, C = 2 * Math.PI * R, off = 0;
    svg.appendChild(el('circle', { cx: cx, cy: cy, r: R, fill: 'none', stroke: '#F2F4F3', 'stroke-width': sw }));
    data.forEach(function (d, i) {
      var frac = d.value / total;
      var arc = el('circle', {
        cx: cx, cy: cy, r: R, fill: 'none', stroke: d.color || PAL[i % PAL.length], 'stroke-width': sw,
        'stroke-dasharray': (frac * C - 1.5).toFixed(2) + ' ' + C,
        'stroke-dashoffset': (-off * C).toFixed(2),
        transform: 'rotate(-90 ' + cx + ' ' + cy + ')', 'stroke-linecap': 'butt'
      });
      arc.style.cursor = 'pointer';
      arc.addEventListener('mousemove', function (e) {
        showTip('<div class="th">' + esc(d.label) + '</div><div class="tr"><i style="background:' + (d.color || PAL[i % PAL.length]) + '"></i><span>' + (o.fmt ? o.fmt(d.value) : d.value) + '</span><b>' + (frac * 100).toFixed(1) + '%</b></div>', e.clientX, e.clientY);
      });
      arc.addEventListener('mouseleave', hideTip);
      svg.appendChild(arc);
      off += frac;
    });
    svgBox.appendChild(svg);
    if (o.center) {
      var c = document.createElement('div');
      c.style.cssText = 'position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center';
      c.innerHTML = '<div style="font-size:20px;font-weight:800;letter-spacing:-.03em;line-height:1.1">' + o.center.t + '</div>' +
                    (o.center.s ? '<div style="font-size:9.5px;color:#9E9E9E;font-weight:600;margin-top:2px">' + o.center.s + '</div>' : '');
      svgBox.appendChild(c);
    }
    wrap.appendChild(svgBox);
    if (o.legend !== false) {
      var lg = document.createElement('div');
      lg.style.cssText = 'flex:1;min-width:150px;display:flex;flex-direction:column;gap:6px';
      data.forEach(function (d, i) {
        var frac = d.value / total;
        lg.innerHTML += '<div style="display:flex;align-items:center;gap:7px;font-size:11px">' +
          '<i style="width:8px;height:8px;border-radius:2px;background:' + (d.color || PAL[i % PAL.length]) + ';flex:0 0 8px"></i>' +
          '<span style="flex:1;font-weight:600;color:#1C1C1C;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + esc(d.label) + '</span>' +
          '<span style="font-weight:700;font-variant-numeric:tabular-nums">' + (frac * 100).toFixed(1) + '%</span></div>';
      });
      wrap.appendChild(lg);
    }
    host.appendChild(wrap);
  }

  /* =====================================================================
     SPARKLINE
     ===================================================================== */
  function spark(host, o) {
    if (!host) return;
    o = o || {};
    var d = o.data || [], W = o.width || 74, H = o.height || 26;
    if (d.length < 2) { host.innerHTML = ''; return; }
    var max = Math.max.apply(null, d), min = Math.min.apply(null, d);
    if (max === min) max = min + 1;
    host.innerHTML = '';
    var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, preserveAspectRatio: 'none' });
    var col = o.color || '#0E7A4E';
    var X = function (i) { return (i / (d.length - 1)) * W; };
    var Y = function (v) { return H - 2 - ((v - min) / (max - min)) * (H - 5); };
    var p = '', ap = '';
    d.forEach(function (v, i) { p += (i ? ' L' : 'M') + X(i).toFixed(1) + ' ' + Y(v).toFixed(1); });
    ap = p + ' L' + W + ' ' + H + ' L0 ' + H + ' Z';
    svg.appendChild(el('path', { d: ap, fill: col, opacity: .12 }));
    svg.appendChild(el('path', { d: p, fill: 'none', stroke: col, 'stroke-width': 1.6, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }));
    svg.appendChild(el('circle', { cx: X(d.length - 1), cy: Y(d[d.length - 1]), r: 2, fill: col }));
    host.appendChild(svg);
  }

  /* =====================================================================
     FUNNEL (DOM) — steps:[{step,value,pctTop,pctPrevStep,dropped,where,delta}]
     ===================================================================== */
  function funnel(host, steps, o) {
    if (!host) return;
    o = o || {};
    var top = steps[0] ? steps[0].value : 1;
    var h = '<div class="fn">';
    steps.forEach(function (s, i) {
      var drop = i === 0 ? null : 1 - s.pctPrevStep;
      var bad = drop !== null && drop > .2;
      h += '<div class="fn-row" data-i="' + i + '" title="' + esc(s.where || '') + '">';
      h += '<div class="fn-lab"><span class="ix">' + (i + 1) + '</span><span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + esc(s.step) + '</span></div>';
      // keep the % label legible: inside the fill only when the fill is wide enough,
      // otherwise sit just outside it in body colour
      var pct = (s.pctTop * 100).toFixed(1);
      var inside = s.pctTop >= .45;
      h += '<div class="fn-bar"><i style="width:' + pct + '%"></i>' +
           '<b style="' + (inside ? '' : 'left:calc(' + pct + '% + 7px);color:#606060;text-shadow:none') + '">' +
           pct + '%</b></div>';
      h += '<div class="fn-num">' + KO.fmtNum(s.value) + '</div>';
      h += '<div class="fn-drop">' + (drop === null
        ? '<span class="pill n">entry</span>'
        : '<span class="pill ' + (bad ? 'r' : drop > .12 ? 'y' : 'g') + '">−' + (drop * 100).toFixed(1) + '%</span>') + '</div>';
      h += '</div>';
    });
    h += '</div>';
    host.innerHTML = h;
    Array.prototype.forEach.call(host.querySelectorAll('.fn-row'), function (row) {
      row.addEventListener('click', function () {
        Array.prototype.forEach.call(host.querySelectorAll('.fn-row'), function (r) { r.classList.remove('on'); });
        row.classList.add('on');
        if (o.onSelect) o.onSelect(steps[+row.dataset.i], +row.dataset.i);
      });
      row.addEventListener('mousemove', function (e) {
        var s = steps[+row.dataset.i], i = +row.dataset.i;
        var html = '<div class="th">' + esc(s.step) + '</div>' +
          '<div class="tr"><span>Users</span><b>' + KO.fmtNum(s.value) + '</b></div>' +
          '<div class="tr"><span>% of entry</span><b>' + (s.pctTop * 100).toFixed(2) + '%</b></div>';
        if (i > 0) html += '<div class="tr"><span>Step conversion</span><b>' + (s.pctPrevStep * 100).toFixed(1) + '%</b></div>' +
          '<div class="tr"><span>Lost here</span><b>' + KO.fmtNum(s.dropped) + '</b></div>';
        if (s.where) html += '<div class="tr" style="margin-top:3px;color:rgba(255,255,255,.6)"><span>' + esc(s.where) + '</span></div>';
        showTip(html, e.clientX, e.clientY);
      });
      row.addEventListener('mouseleave', hideTip);
    });
    if (o.autoSelect !== false) {
      var worst = 0, wd = 0;
      steps.forEach(function (s, i) { if (i > 0 && (1 - s.pctPrevStep) > wd) { wd = 1 - s.pctPrevStep; worst = i; } });
      var r = host.querySelector('.fn-row[data-i="' + worst + '"]');
      if (r) { r.classList.add('on'); if (o.onSelect) o.onSelect(steps[worst], worst); }
    }
  }

  /* =====================================================================
     HEATMAP (cohort retention)  rows:[{label,size,vals:[0..1]}]
     ===================================================================== */
  function heat(host, o) {
    if (!host) return;
    o = o || {};
    var rows = o.rows || [], cols = o.cols || 12;
    function col(v) {
      if (v === null || v === undefined) return 'background:#FAFBFA;color:transparent';
      var a = Math.pow(v, .62);
      return 'background:rgba(14,122,78,' + (0.07 + a * .86).toFixed(3) + ');color:' + (a > .45 ? '#fff' : '#0E5537');
    }
    var h = '<div style="overflow:auto"><table class="heat" style="width:100%"><thead><tr><th></th><th style="text-align:right;padding-right:9px">Size</th>';
    for (var c = 0; c < cols; c++) h += '<th>W' + c + '</th>';
    h += '</tr></thead><tbody>';
    rows.forEach(function (r) {
      h += '<tr><td class="rl">' + esc(r.label) + '</td><td class="rl" style="font-weight:700;color:#1C1C1C">' + KO.fmtNum(r.size) + '</td>';
      for (var c2 = 0; c2 < cols; c2++) {
        var v = r.vals[c2];
        h += '<td><div class="cell" style="' + col(v) + '" data-v="' + (v === undefined ? '' : v) + '" data-l="' + esc(r.label) + '" data-w="' + c2 + '" data-n="' + Math.round((v || 0) * r.size) + '">' +
             (v === undefined ? '' : Math.round(v * 100)) + '</div></td>';
      }
      h += '</tr>';
    });
    h += '</tbody></table></div>';
    host.innerHTML = h;
    Array.prototype.forEach.call(host.querySelectorAll('.cell'), function (c) {
      if (!c.dataset.v) return;
      c.addEventListener('mousemove', function (e) {
        showTip('<div class="th">' + esc(c.dataset.l) + '</div>' +
          '<div class="tr"><span>Week ' + c.dataset.w + '</span><b>' + Math.round(c.dataset.v * 100) + '%</b></div>' +
          '<div class="tr"><span>Partners retained</span><b>' + KO.fmtNum(+c.dataset.n) + '</b></div>', e.clientX, e.clientY);
      });
      c.addEventListener('mouseleave', hideTip);
    });
  }

  /* =====================================================================
     SANKEY-ish flow diagram (layered)
     ===================================================================== */
  function flow(host, o) {
    if (!host) return;
    var nodes = o.nodes, links = o.links;
    var W = width(host), H = o.height || 340;
    // assign layers by BFS from first node
    var layer = {}; nodes.forEach(function (n) { layer[n] = 0; });
    for (var pass = 0; pass < nodes.length; pass++) {
      links.forEach(function (l) { if (layer[l.t] < layer[l.s] + 1) layer[l.t] = layer[l.s] + 1; });
    }
    layer['Exit'] = Math.max.apply(null, nodes.map(function (n) { return n === 'Exit' ? 0 : layer[n]; })) + 1;
    var maxL = Math.max.apply(null, nodes.map(function (n) { return layer[n]; }));
    var byLayer = {};
    nodes.forEach(function (n) { (byLayer[layer[n]] = byLayer[layer[n]] || []).push(n); });
    // node totals
    var tot = {};
    nodes.forEach(function (n) {
      var inc = links.filter(function (l) { return l.t === n; }).reduce(function (a, b) { return a + b.v; }, 0);
      var out = links.filter(function (l) { return l.s === n; }).reduce(function (a, b) { return a + b.v; }, 0);
      tot[n] = Math.max(inc, out) || 1;
    });
    var svg = mk(host, W, H);
    var pad = 14, nw = 12;
    var lw = (W - pad * 2 - nw) / Math.max(1, maxL);
    var pos = {};
    Object.keys(byLayer).forEach(function (L) {
      var list = byLayer[L];
      var sumT = list.reduce(function (a, b) { return a + tot[b]; }, 0);
      var gap = 10, avail = H - pad * 2 - gap * (list.length - 1);
      var y = pad;
      list.forEach(function (n) {
        var hh = Math.max(14, (tot[n] / sumT) * avail);
        pos[n] = { x: pad + L * lw, y: y, h: hh };
        y += hh + gap;
      });
    });
    var colOf = function (n) {
      return n === 'Exit' ? '#E23744' : n === 'Order placed' ? '#0C831F' : n === 'Cart' || n === 'Checkout' ? '#D4A537' : '#0E7A4E';
    };
    // links
    var offS = {}, offT = {};
    links.slice().sort(function (a, b) { return b.v - a.v; }).forEach(function (l) {
      var s = pos[l.s], t = pos[l.t]; if (!s || !t) return;
      var sh = (l.v / tot[l.s]) * s.h, th = (l.v / tot[l.t]) * t.h;
      var sy = s.y + (offS[l.s] = (offS[l.s] || 0)) ; offS[l.s] += sh;
      var ty = t.y + (offT[l.t] = (offT[l.t] || 0)) ; offT[l.t] += th;
      var x1 = s.x + nw, x2 = t.x, mx = (x1 + x2) / 2;
      var d = 'M' + x1 + ' ' + sy + ' C' + mx + ' ' + sy + ' ' + mx + ' ' + ty + ' ' + x2 + ' ' + ty +
              ' L' + x2 + ' ' + (ty + th) + ' C' + mx + ' ' + (ty + th) + ' ' + mx + ' ' + (sy + sh) + ' ' + x1 + ' ' + (sy + sh) + ' Z';
      var p = el('path', { d: d, fill: colOf(l.t), opacity: .17 });
      p.style.cursor = 'pointer';
      p.addEventListener('mouseenter', function () { p.setAttribute('opacity', .42); });
      p.addEventListener('mousemove', function (e) {
        showTip('<div class="th">' + esc(l.s) + ' → ' + esc(l.t) + '</div><div class="tr"><span>of all app opens</span><b>' + l.v + '%</b></div>', e.clientX, e.clientY);
      });
      p.addEventListener('mouseleave', function () { p.setAttribute('opacity', .17); hideTip(); });
      svg.appendChild(p);
    });
    // nodes
    nodes.forEach(function (n) {
      var p = pos[n]; if (!p) return;
      svg.appendChild(el('rect', { x: p.x, y: p.y, width: nw, height: p.h, rx: 3, fill: colOf(n) }));
      var anchor = layer[n] === maxL ? 'end' : 'start';
      var tx = el('text', {
        x: anchor === 'end' ? p.x - 6 : p.x + nw + 6, y: p.y + p.h / 2 + 3.5,
        'text-anchor': anchor, fill: '#1C1C1C', 'font-size': 10, 'font-weight': 700
      });
      tx.textContent = n; svg.appendChild(tx);
      var tv = el('text', {
        x: anchor === 'end' ? p.x - 6 : p.x + nw + 6, y: p.y + p.h / 2 + 14,
        'text-anchor': anchor, fill: '#9E9E9E', 'font-size': 9, 'font-weight': 600
      });
      tv.textContent = tot[n] + '%'; if (p.h > 28) svg.appendChild(tv);
    });
  }

  /* =====================================================================
     SCATTER (impact/effort, adoption vs retention …)
     ===================================================================== */
  function scatter(host, o) {
    if (!host) return;
    o = o || {};
    var H = o.height || 300, W = width(host);
    var pad = { t: 14, r: 16, b: 34, l: 52 };
    var svg = mk(host, W, H);
    var pts = o.points || [];
    var xMax = nice(Math.max.apply(null, pts.map(function (p) { return p.x; })) * 1.1);
    var yMax = nice(Math.max.apply(null, pts.map(function (p) { return p.y; })) * 1.1);
    var iw = W - pad.l - pad.r, ih = H - pad.t - pad.b;
    var X = function (v) { return pad.l + (v / xMax) * iw; };
    var Y = function (v) { return pad.t + ih - (v / yMax) * ih; };
    // quadrants
    svg.appendChild(el('rect', { x: X(xMax / 2), y: pad.t, width: iw / 2, height: ih / 2, fill: '#F0FDF5' }));
    for (var g = 0; g <= 4; g++) {
      var gy = pad.t + ih - (g / 4) * ih;
      svg.appendChild(el('line', { x1: pad.l, x2: W - pad.r, y1: gy, y2: gy, stroke: '#F2F4F3' }));
      var t = el('text', { x: pad.l - 7, y: gy + 3.5, 'text-anchor': 'end', fill: '#9E9E9E', 'font-size': 9, 'font-weight': 600 });
      t.textContent = (o.yFmt || idf)(yMax * g / 4); svg.appendChild(t);
      var gx = pad.l + (g / 4) * iw;
      svg.appendChild(el('line', { x1: gx, x2: gx, y1: pad.t, y2: pad.t + ih, stroke: '#F2F4F3' }));
      var t2 = el('text', { x: gx, y: H - 16, 'text-anchor': 'middle', fill: '#9E9E9E', 'font-size': 9, 'font-weight': 600 });
      t2.textContent = (o.xFmt || idf)(xMax * g / 4); svg.appendChild(t2);
    }
    if (o.xLabel) { var xl = el('text', { x: pad.l + iw / 2, y: H - 3, 'text-anchor': 'middle', fill: '#606060', 'font-size': 9.5, 'font-weight': 700 }); xl.textContent = o.xLabel; svg.appendChild(xl); }
    pts.forEach(function (p, i) {
      var c = el('circle', { cx: X(p.x), cy: Y(p.y), r: p.r || 7, fill: p.color || PAL[i % PAL.length], opacity: .78, stroke: '#fff', 'stroke-width': 1.5 });
      c.style.cursor = 'pointer';
      c.addEventListener('mousemove', function (e) {
        showTip('<div class="th">' + esc(p.label) + '</div>' +
          '<div class="tr"><span>' + esc(o.xLabel || 'x') + '</span><b>' + (o.xFmt || idf)(p.x) + '</b></div>' +
          '<div class="tr"><span>' + esc(o.yLabel || 'y') + '</span><b>' + (o.yFmt || idf)(p.y) + '</b></div>' +
          (p.note ? '<div class="tr" style="color:rgba(255,255,255,.6)"><span>' + esc(p.note) + '</span></div>' : ''), e.clientX, e.clientY);
      });
      c.addEventListener('mouseleave', hideTip);
      svg.appendChild(c);
      if (p.r > 5 || pts.length <= 16) {
        var lb = el('text', { x: X(p.x), y: Y(p.y) - (p.r || 7) - 4, 'text-anchor': 'middle', fill: '#606060', 'font-size': 8.5, 'font-weight': 700 });
        lb.textContent = p.label.length > 15 ? p.label.slice(0, 14) + '…' : p.label; svg.appendChild(lb);
      }
    });
  }

  /* =====================================================================
     GAUGE (goal progress)
     ===================================================================== */
  function gauge(host, o) {
    if (!host) return;
    var size = o.size || 104, pct = Math.max(0, Math.min(1, o.value / o.max));
    var R = size / 2 - 9, cx = size / 2, cy = size / 2;
    var C = Math.PI * R; // half circle
    host.innerHTML = '';
    var svg = el('svg', { viewBox: '0 0 ' + size + ' ' + (size * .62), width: size, height: size * .62 });
    var d = 'M' + (cx - R) + ' ' + cy + ' A' + R + ' ' + R + ' 0 0 1 ' + (cx + R) + ' ' + cy;
    svg.appendChild(el('path', { d: d, fill: 'none', stroke: '#F2F4F3', 'stroke-width': 9, 'stroke-linecap': 'round' }));
    svg.appendChild(el('path', { d: d, fill: 'none', stroke: o.color || '#0E7A4E', 'stroke-width': 9, 'stroke-linecap': 'round', 'stroke-dasharray': (pct * C).toFixed(1) + ' ' + C }));
    var t = el('text', { x: cx, y: cy - 4, 'text-anchor': 'middle', fill: '#1C1C1C', 'font-size': 17, 'font-weight': 800 });
    t.textContent = Math.round(pct * 100) + '%'; svg.appendChild(t);
    host.appendChild(svg);
  }

  global.KC = {
    line: line, bars: bars, hbars: hbars, donut: donut, spark: spark,
    funnel: funnel, heat: heat, flow: flow, scatter: scatter, gauge: gauge,
    PAL: PAL, showTip: showTip, hideTip: hideTip
  };
})(window);
