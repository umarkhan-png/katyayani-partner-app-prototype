import re

with open(r'C:\Users\ASUS\katyayani-partner-app\screens\home.html', 'r', encoding='utf-8') as f:
    h = f.read()

# ===== A. PRODUCT CARDS =====

# A1. Tech name gap: add mt-0.5 to tech name divs in product cards
h = h.replace(
    '<div class="text-[11px] text-[#9E9E9E] truncate">',
    '<div class="text-[11px] text-[#9E9E9E] truncate mt-0.5">'
)
print('A1. tech name gap done')

# A2. Case prices + margin pill + per-unit text
def make_old(unit, mrp, off, margin):
    return (
        '<div class="flex items-end justify-between mt-2"><div>'
        '<div class="text-[18px] font-extrabold">₹' + unit + '</div>'
        '<div class="flex items-center gap-1.5 mt-0.5">'
        '<span class="text-[12px] text-[#9E9E9E] price-strike">₹' + mrp + '</span>'
        '<span class="text-[10px] font-bold text-[#9E9E9E]">' + off + '% off</span>'
        '</div></div>'
        '<span class="text-[11px] font-semibold text-[#0E7A4E]">' + margin + '% margin</span>'
        '</div>'
    )

def make_new(case, unit, pack, margin):
    return (
        '<div class="mt-2">'
        '<div class="flex items-end justify-between">'
        '<div>'
        '<div class="text-[18px] font-extrabold">₹' + case + '</div>'
        '<div class="text-[10px] text-[#9E9E9E] mt-0.5">₹' + unit + '/pc · ' + pack + '</div>'
        '</div>'
        '<div class="flex-shrink-0 inline-flex items-center bg-[#F0FDF5] text-[#0C831F] px-2 py-0.5 rounded-full text-[11px] font-bold">' + margin + '% margin</div>'
        '</div>'
        '</div>'
    )

products = [
    # (unit, mrp, off, margin, case, pack)
    ('280', '400', '30', '30', '5,600', '250ml×20'),
    ('330', '480', '31', '31', '3,300', '1kg×10'),
    ('440', '650', '32', '32', '8,800', '150ml×20'),
    ('364', '520', '30', '30', '4,368', '500g×12'),
    ('334', '480', '30', '30', '6,680', '250ml×20'),
    ('310', '450', '31', '31', '6,200', '250ml×20'),
    ('358', '520', '31', '31', '7,160', '250ml×20'),
]

for unit, mrp, off, margin, case, pack in products:
    old = make_old(unit, mrp, off, margin)
    new = make_new(case, unit, pack, margin)
    c = h.count(old)
    h = h.replace(old, new)
    print('A2. Rs' + unit + ' -> Rs' + case + '/case: ' + str(c) + ' replaced')

# A3. Update renderCropGrid JS template to use case price + margin pill
old_crop = (
    "'<div class=\"flex items-end justify-between mt-2\">' +\n"
    "        '<div><span class=\"text-[16px] font-extrabold\">'+p.p+'</span>' +\n"
    "        '<div class=\"flex items-center gap-1 mt-0.5\"><span class=\"text-[10px] text-[#9E9E9E] price-strike\">'+p.mrp+'</span><span class=\"text-[9px] font-bold text-[#9E9E9E]\">'+p.off+'% off</span></div></div>' +\n"
    "        '<span class=\"text-[10px] font-semibold text-[#0E7A4E]\">'+p.m+' margin</span>' +\n"
    "      '</div>'"
)
new_crop = (
    "'<div class=\"mt-2\"><div class=\"flex items-end justify-between\">' +\n"
    "        '<div><div class=\"text-[16px] font-extrabold\">'+p.c+'</div>' +\n"
    "        '<div class=\"text-[10px] text-[#9E9E9E] mt-0.5\">'+p.p+'/pc · '+p.pk+'</div></div>' +\n"
    "        '<div class=\"flex-shrink-0 inline-flex items-center bg-[#F0FDF5] text-[#0C831F] px-2 py-0.5 rounded-full text-[10px] font-bold\">'+p.m+'</div>' +\n"
    "      '</div></div>'"
)
if old_crop in h:
    h = h.replace(old_crop, new_crop)
    print('A3. renderCropGrid case price template done')
else:
    print('A3. MISS: renderCropGrid template')


# ===== B. STORIES: tappable with openStory() bottom sheet =====

story_keys = [
    ('Flash Sale', 'flash-sale'),
    ('New Arrivals', 'new-arrivals'),
    ('Pesticides', 'pesticides'),
    ('Fertilizers', 'fertilizers'),
    ('Soybean', 'soybean'),
    ('Cotton', 'cotton'),
    ('Fungicides', 'fungicides'),
    ('Combos', 'combos'),
]

for name, key in story_keys:
    pattern = (
        r'<a href="categories\.html" class="flex flex-col items-center gap-1\.5 flex-shrink-0">'
        r'(.*?)'
        r'<div class="text-\[11px\] font-semibold text-\[#1C1C1C\] text-center leading-tight max-w-\[72px\]">'
        + re.escape(name) +
        r'</div>\s*</a>'
    )
    replacement = (
        '<button onclick="openStory(\'' + key + '\')" class="flex flex-col items-center gap-1.5 flex-shrink-0">'
        r'\1'
        '<div class="text-[11px] font-semibold text-[#1C1C1C] text-center leading-tight max-w-[72px]">' + name + '</div>\n          </button>'
    )
    new_h, count = re.subn(pattern, replacement, h, flags=re.DOTALL)
    if count:
        h = new_h
        print('B1. Story ' + name + ': converted to button')
    else:
        print('B1. MISS: Story ' + name)

# B2. Add story sheet HTML + JS before service worker
story_sheet = r"""
  <!-- Story sheet -->
  <div id="storySheetBd" class="hidden absolute inset-0 bg-black/60 z-50" onclick="closeStory()"></div>
  <div id="storySheet" class="hidden absolute left-0 right-0 bottom-0 z-50 bg-white rounded-t-[28px] overflow-hidden" style="max-height:82%;box-shadow:0 -8px 30px rgba(0,0,0,.18)">
    <div class="px-5 pt-3 pb-6 overflow-y-auto" id="storyContent" style="max-height:72vh">
      <div class="mx-auto w-10 h-1 rounded-full bg-[#E8E8E8] mb-4"></div>
    </div>
  </div>
  <script>
  var STORY_DATA = {
    'flash-sale': {
      title: '⚡ Flash Sale — Today Only',
      body: '<div class="bg-gradient-to-br from-[#F0FDF5] to-[#E4F5EC] border border-[#0C831F]/20 rounded-2xl p-4 mb-3"><div class="text-[13px] font-bold text-[#0C831F] mb-2">🔥 Deal of the Day</div><div class="flex items-center justify-between mb-2"><div><div class="text-[20px] font-black text-[#1C1C1C]">Imida 30.5%</div><div class="text-[12px] text-[#606060]">250ml × 20 pcs / case</div></div><div class="text-right"><div class="text-[22px] font-black text-[#0C831F]">₹5,600</div><div class="text-[11px] text-[#9E9E9E] line-through">₹8,000</div></div></div><div class="h-2 bg-[#D8EBDF] rounded-full overflow-hidden"><div class="h-full bg-[#0C831F] rounded-full" style="width:72%"></div></div><div class="flex justify-between mt-1"><div class="text-[11px] text-[#0C831F]">72 cases sold</div><div class="text-[11px] text-[#606060]">28 left · ends tonight</div></div></div><a href="pdp.html" class="block bg-[#0C831F] text-white text-center py-3 rounded-xl font-bold text-[15px]">Buy Now →</a>'
    },
    'new-arrivals': {
      title: '✨ New Arrivals',
      body: '<div class="space-y-3 mb-3"><div class="flex items-center gap-3 bg-[#F8F8F8] rounded-2xl p-3"><img src="https://katyayanikrishidirect.com/cdn/shop/files/Bhumiraja_2_1.webp" class="w-16 h-16 object-contain rounded-xl bg-white p-1 flex-shrink-0"><div><div class="text-[14px] font-bold text-[#1C1C1C]">Bhumiraja Myco</div><div class="text-[12px] text-[#606060]">Humic Acid + Mycorrhiza</div><div class="text-[13px] font-extrabold text-[#0C831F] mt-1">₹4,368<span class="text-[10px] font-normal text-[#9E9E9E]"> /case</span></div></div></div><div class="flex items-center gap-3 bg-[#F8F8F8] rounded-2xl p-3"><img src="https://katyayanikrishidirect.com/cdn/shop/files/AntiVirus_75248f94-8de8-47c9-9592-a7aa49e36eeb.webp" class="w-16 h-16 object-contain rounded-xl bg-white p-1 flex-shrink-0"><div><div class="text-[14px] font-bold text-[#1C1C1C]">AntiVirus</div><div class="text-[12px] text-[#606060]">Viricide · Broad spectrum</div><div class="text-[13px] font-extrabold text-[#0C831F] mt-1">New Arrival</div></div></div></div><a href="categories.html" class="block bg-[#0C831F] text-white text-center py-3 rounded-xl font-bold text-[15px]">Browse All New →</a>'
    },
    'pesticides': {
      title: '🐛 Pesticide Tip of the Week',
      body: '<div class="bg-[#FFF8E6] border border-[#D4A537]/30 rounded-2xl p-4 mb-3"><div class="text-[13px] font-bold text-[#8B6914] mb-2">💡 Pro Tip</div><div class="text-[14px] text-[#1C1C1C] leading-relaxed">Mix <strong>Imida 30.5%</strong> + <strong>EMA 5</strong> at 50:50 for cotton bollworm control. Reduces cost by 18% vs single product. Best applied early morning.</div></div><div class="bg-white border border-[#EDEDED] rounded-2xl p-3"><div class="text-[12px] font-bold text-[#606060] mb-2 uppercase tracking-wider">Top Pesticides This Week</div><div class="space-y-2"><div class="flex justify-between"><span class="text-[13px] text-[#1C1C1C]">Imida 30.5%</span><span class="text-[13px] font-bold text-[#0C831F]">47 cases sold</span></div><div class="flex justify-between"><span class="text-[13px] text-[#1C1C1C]">Chakraveer 18.5%</span><span class="text-[13px] font-bold text-[#0C831F]">31 cases sold</span></div><div class="flex justify-between"><span class="text-[13px] text-[#1C1C1C]">EMA 5</span><span class="text-[13px] font-bold text-[#0C831F]">28 cases sold</span></div></div></div>'
    },
    'fertilizers': {
      title: '🌿 Fertilizer Market Intel',
      body: '<div class="bg-white border border-[#EDEDED] rounded-2xl overflow-hidden mb-3"><div class="px-4 py-2 bg-[#F0FDF5] border-b border-[#EDEDED]"><div class="text-[12px] font-bold text-[#0E7A4E]">Price Trend — MP Market</div></div><div class="divide-y divide-[#F0F0F0]"><div class="px-4 py-2.5 flex justify-between"><span class="text-[13px] text-[#1C1C1C]">NPK 19-19-19</span><span class="text-[12px] font-bold text-[#0C831F]">↑ Demand up 23%</span></div><div class="px-4 py-2.5 flex justify-between"><span class="text-[13px] text-[#1C1C1C]">DAP (market)</span><span class="text-[12px] font-bold text-[#8B6914]">→ Stable</span></div><div class="px-4 py-2.5 flex justify-between"><span class="text-[13px] text-[#1C1C1C]">Bhumiraja Myco</span><span class="text-[12px] font-bold text-[#0C831F]">↑ New stock in</span></div></div></div><a href="categories.html" class="block bg-[#0C831F] text-white text-center py-3 rounded-xl font-bold text-[15px]">Order Fertilizers →</a>'
    },
    'soybean': {
      title: '🌾 Soybean Season Quiz',
      body: '<div class="text-[15px] font-bold text-[#1C1C1C] mb-3">Which product gives best ROI on soybean this kharif?</div><div class="space-y-2" id="quizOptions"><button onclick="storyQuizAnswer(this,true)" class="w-full text-left p-3 rounded-xl border-2 border-[#EDEDED] bg-white text-[14px] font-medium text-[#1C1C1C]">A. Chakrawarti ZC (1% dose)</button><button onclick="storyQuizAnswer(this,false)" class="w-full text-left p-3 rounded-xl border-2 border-[#EDEDED] bg-white text-[14px] font-medium text-[#1C1C1C]">B. Imida 30.5% (spray)</button><button onclick="storyQuizAnswer(this,false)" class="w-full text-left p-3 rounded-xl border-2 border-[#EDEDED] bg-white text-[14px] font-medium text-[#1C1C1C]">C. EMA 5 (foliar)</button></div><div id="quizResult" class="hidden mt-3 bg-[#F0FDF5] border border-[#0C831F]/20 rounded-xl p-3 text-[13px] text-[#0C831F]">✅ Correct! Chakrawarti ZC gives 82% margin on soybean. <a href="pdp.html" class="font-bold underline">View product →</a></div>'
    },
    'cotton': {
      title: '🐛 Cotton Pest Alert — Indore',
      body: '<div class="bg-[#FFE3D3] border border-[#FF6B35]/30 rounded-2xl p-4 mb-3"><div class="flex items-center gap-2 mb-2"><div class="text-[18px]">⚠️</div><div class="text-[14px] font-bold text-[#8B3500]">High Risk: Bollworm</div></div><div class="text-[13px] text-[#8B3500] leading-relaxed">Reports from 14 Indore retailers: bollworm activity high in cotton fields this week. Recommend stocking EMA 5 and Imida 30.5%.</div></div><div class="text-[13px] font-bold text-[#1C1C1C] mb-2">Recommended for Cotton:</div><div class="space-y-2"><div class="flex justify-between items-center bg-white border border-[#EDEDED] rounded-xl px-3 py-2"><span class="text-[13px] text-[#1C1C1C]">EMA 5 SG</span><span class="text-[12px] font-bold text-[#0C831F]">₹5,920/case · 32%↑</span></div><div class="flex justify-between items-center bg-white border border-[#EDEDED] rounded-xl px-3 py-2"><span class="text-[13px] text-[#1C1C1C]">Imida 30.5%</span><span class="text-[12px] font-bold text-[#0C831F]">₹5,600/case · 30%↑</span></div></div>'
    },
    'fungicides': {
      title: '🍄 Fungicide Guide — 3 Steps',
      body: '<div class="space-y-3 mb-3"><div class="flex gap-3 bg-[#F0FDF5] rounded-2xl p-3 items-start"><div class="w-8 h-8 rounded-full bg-[#0C831F] text-white flex items-center justify-center font-black text-[14px] flex-shrink-0">1</div><div><div class="text-[13px] font-bold text-[#1C1C1C]">Identify the disease</div><div class="text-[12px] text-[#606060]">Use Disease Scanner in Explore tab for AI-based ID</div></div></div><div class="flex gap-3 bg-[#F0FDF5] rounded-2xl p-3 items-start"><div class="w-8 h-8 rounded-full bg-[#0C831F] text-white flex items-center justify-center font-black text-[14px] flex-shrink-0">2</div><div><div class="text-[13px] font-bold text-[#1C1C1C]">Choose Azodharma</div><div class="text-[12px] text-[#606060]">Azoxystrobin + Tebuconazole — works on 12+ fungal diseases</div></div></div><div class="flex gap-3 bg-[#F0FDF5] rounded-2xl p-3 items-start"><div class="w-8 h-8 rounded-full bg-[#0C831F] text-white flex items-center justify-center font-black text-[14px] flex-shrink-0">3</div><div><div class="text-[13px] font-bold text-[#1C1C1C]">Stock before season</div><div class="text-[12px] text-[#606060]">Order now at ₹6,200/case · 31% margin guaranteed</div></div></div></div><a href="pdp.html" class="block bg-[#0C831F] text-white text-center py-3 rounded-xl font-bold text-[15px]">Order Azodharma →</a>'
    },
    'combos': {
      title: '📦 Combo Deal — Save More',
      body: '<div class="bg-gradient-to-br from-[#FFF8E6] to-[#FFFBF0] border border-[#D4A537]/40 rounded-2xl p-4 mb-3"><div class="text-[13px] font-bold text-[#8B6914] mb-3">🎁 Bundle &amp; Save</div><div class="space-y-2 mb-3"><div class="flex justify-between"><span class="text-[13px] text-[#1C1C1C]">Imida 30.5% (1 case)</span><span class="text-[13px] font-bold">₹5,600</span></div><div class="flex justify-between"><span class="text-[13px] text-[#1C1C1C]">Azodharma (1 case)</span><span class="text-[13px] font-bold">₹6,200</span></div><div class="flex justify-between border-t border-[#D4A537]/20 pt-2 mt-1"><span class="text-[13px] font-bold text-[#8B6914]">Combo Price</span><span class="text-[13px] font-bold text-[#0C831F]">₹11,200 <span class="text-[11px] line-through text-[#9E9E9E]">₹11,800</span></span></div></div><div class="text-[12px] text-[#8B6914]">Save ₹600 on this combo</div></div><a href="cart.html" class="block bg-[#D4A537] text-[#1C1C1C] text-center py-3 rounded-xl font-bold text-[15px]">Add Combo to Cart →</a>'
    }
  };
  function openStory(key) {
    var data = STORY_DATA[key]; if (!data) return;
    document.getElementById('storyContent').innerHTML =
      '<div class="mx-auto w-10 h-1 rounded-full bg-[#E8E8E8] mb-4"></div>' +
      '<div class="flex items-center justify-between mb-3">' +
        '<div class="brand-font text-[20px] text-[#1C1C1C]">' + data.title + '</div>' +
        '<button onclick="closeStory()" class="text-[13px] font-medium text-[#606060] border border-[#EDEDED] rounded-full px-3 py-1 flex-shrink-0 ml-2">Close</button>' +
      '</div>' + data.body;
    document.getElementById('storySheetBd').classList.remove('hidden');
    document.getElementById('storySheet').classList.remove('hidden');
  }
  function closeStory() {
    document.getElementById('storySheetBd').classList.add('hidden');
    document.getElementById('storySheet').classList.add('hidden');
  }
  function storyQuizAnswer(btn, correct) {
    var opts = document.getElementById('quizOptions');
    if (!opts) return;
    Array.from(opts.querySelectorAll('button')).forEach(function(b){b.disabled=true;b.style.opacity='0.6';});
    btn.style.opacity='1';
    btn.style.borderColor = correct ? '#0C831F' : '#EF4444';
    btn.style.background  = correct ? '#F0FDF5' : '#FEF2F2';
    if (correct) { var r=document.getElementById('quizResult'); if(r) r.classList.remove('hidden'); }
  }
  </script>
"""

h = h.replace('  <script>if("serviceWorker"in navigator)', story_sheet + '  <script>if("serviceWorker"in navigator)')
print('B2. Story sheet + JS added')


# ===== C. LIVE ACTIVITY STRIP: remove old, add auto-scroll below Best in MP =====

# C1. Remove old static strip
old_strip = (
    '\n      <!-- Live activity strip -->\n'
    '      <div class="mx-4 mt-4 bg-gradient-to-r from-[#F0FDF5] to-[#E8F5EB] border border-[#0E7A4E]/20 rounded-2xl p-3 flex items-center gap-3">\n'
    '        <div class="flex -space-x-2">\n'
    '          <div class="w-8 h-8 rounded-full bg-[#FFE3D3] border-2 border-white flex items-center justify-center text-base">\U0001f468</div>\n'
    '          <div class="w-8 h-8 rounded-full bg-[#D8F3E3] border-2 border-white flex items-center justify-center text-base">\U0001f469</div>\n'
    '          <div class="w-8 h-8 rounded-full bg-[#FFF4C2] border-2 border-white flex items-center justify-center text-base">\U0001f468</div>\n'
    '        </div>\n'
    '        <div class="flex-1 leading-tight">\n'
    '          <div class="text-[14px] font-medium text-[#1C1C1C]"><span class="text-[#0C831F]">24 retailers</span> in Indore</div>\n'
    '          <div class="text-[12px] text-[#606060] whitespace-nowrap">ordered Imida 30.5% today</div>\n'
    '        </div>\n'
    '        <div class="w-2 h-2 rounded-full bg-[#0C831F] animate-pulse"></div>\n'
    '      </div>'
)
if old_strip in h:
    h = h.replace(old_strip, '')
    print('C1. Old live strip removed')
else:
    print('C1. MISS: old live strip (trying alternate)')
    # Try without leading \n
    old_strip2 = (
        '      <!-- Live activity strip -->\n'
        '      <div class="mx-4 mt-4 bg-gradient-to-r from-[#F0FDF5] to-[#E8F5EB] border border-[#0E7A4E]/20 rounded-2xl p-3 flex items-center gap-3">\n'
        '        <div class="flex -space-x-2">\n'
        '          <div class="w-8 h-8 rounded-full bg-[#FFE3D3] border-2 border-white flex items-center justify-center text-base">\U0001f468</div>\n'
        '          <div class="w-8 h-8 rounded-full bg-[#D8F3E3] border-2 border-white flex items-center justify-center text-base">\U0001f469</div>\n'
        '          <div class="w-8 h-8 rounded-full bg-[#FFF4C2] border-2 border-white flex items-center justify-center text-base">\U0001f468</div>\n'
        '        </div>\n'
        '        <div class="flex-1 leading-tight">\n'
        '          <div class="text-[14px] font-medium text-[#1C1C1C]"><span class="text-[#0C831F]">24 retailers</span> in Indore</div>\n'
        '          <div class="text-[12px] text-[#606060] whitespace-nowrap">ordered Imida 30.5% today</div>\n'
        '        </div>\n'
        '        <div class="w-2 h-2 rounded-full bg-[#0C831F] animate-pulse"></div>\n'
        '      </div>'
    )
    if old_strip2 in h:
        h = h.replace(old_strip2, '')
        print('C1. Old live strip removed (alternate)')
    else:
        print('C1. STILL MISS: check manually')

# C2. Add auto-scroll ticker after Best in MP section
ticker_html = '''
      <!-- Live activity auto-scroll ticker -->
      <div class="mx-4 mt-3 rounded-xl overflow-hidden flex items-center gap-2.5 px-3" style="background:linear-gradient(135deg,#F0FDF5,#E4F5EC);border:1px solid rgba(14,122,78,0.2);height:40px">
        <div class="w-2 h-2 rounded-full bg-[#0C831F] animate-pulse flex-shrink-0"></div>
        <div class="flex-1 text-[12px] text-[#1C1C1C] font-medium overflow-hidden whitespace-nowrap text-ellipsis" id="liveTickerMsg"><span class="text-[#0C831F] font-bold">234 retailers</span> buying on Katyayani Partner App this week</div>
      </div>
      <script>
      (function(){
        var msgs=[
          '<span class="text-[#0C831F] font-bold">234 retailers</span> buying on Katyayani Partner App this week',
          '<span class="text-[#0C831F] font-bold">24 orders</span> delivered in Indore in last 2 days',
          '<span class="text-[#0C831F] font-bold">47 retailers</span> bought 1,800 units of Imida 30.5% in MP',
          '<span class="text-[#0C831F] font-bold">₹12,000 avg/month</span> earned by top Katyayani retailers',
          '<span class="text-[#0C831F] font-bold">New: Azodharma</span> — 16 Indore retailers already stocked'
        ];
        var idx=0, el=document.getElementById('liveTickerMsg');
        if (!el) return;
        setInterval(function(){
          el.style.transition='opacity 0.3s';
          el.style.opacity='0';
          setTimeout(function(){
            idx=(idx+1)%msgs.length;
            el.innerHTML=msgs[idx];
            el.style.transition='opacity 0.3s';
            el.style.opacity='1';
          }, 320);
        }, 2800);
      })();
      </script>'''

old_anchor = '\n      <!-- ============== RECOMMENDED FOR YOUR AREA ============== -->'
new_anchor = '\n' + ticker_html + '\n\n      <!-- ============== RECOMMENDED FOR YOUR AREA ============== -->'

if old_anchor in h:
    h = h.replace(old_anchor, new_anchor, 1)
    print('C2. Auto-scroll ticker added below Best in MP')
else:
    print('C2. MISS: Recommended For Your Area anchor')


with open(r'C:\Users\ASUS\katyayani-partner-app\screens\home.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('\nhome.html done.')
