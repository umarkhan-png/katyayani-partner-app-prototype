with open('screens/profit-calculator.html', encoding='utf-8') as f:
    html = f.read()

# ── 1. Hide calc content + CTA on load; show empty state ──────────────────────

# Wrap the main p-4 content block in id="calcView" hidden by default
html = html.replace(
    '      <div class="p-4 space-y-3">',
    '      <!-- EMPTY STATE -->\n      <div id="emptyState" class="px-5 pt-10 pb-6 flex flex-col items-center">\n        <div class="w-20 h-20 rounded-2xl bg-[#F0FDF5] border border-[#0E7A4E]/20 flex items-center justify-center mb-5">\n          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#0E7A4E" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/><path d="M7 8h.01M11 8h2M7 11.5h.01M10 11.5h4"/></svg>\n        </div>\n        <div class="brand-font text-[22px] text-[#1C1C1C] text-center leading-tight mb-2">Calculate Before You Buy</div>\n        <div class="text-[13px] text-[#606060] text-center leading-relaxed mb-6">Select any Katyayani product to instantly see margins, profit scenarios, and the best selling price.</div>\n        <button onclick="openProductPicker()" class="w-full bg-[#0C831F] text-white font-bold text-[15px] py-4 rounded-2xl flex items-center justify-center gap-2 mb-4">\n          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>\n          Choose a Product\n        </button>\n        <!-- Recent calculations hint -->\n        <div class="w-full">\n          <div class="text-[12px] font-semibold text-[#9E9E9E] uppercase tracking-wider mb-2 text-center">Recent Calculations</div>\n          <div class="space-y-2">\n            <div onclick="loadCalc(\'chakraveer\')" class="bg-white border border-[#EDEDED] rounded-xl p-3 flex items-center gap-3 cursor-pointer active:bg-[#F8F8F8]">\n              <img src="https://katyayanikrishidirect.com/cdn/shop/files/ChakraveerNewMockup.webp" class="w-10 h-10 object-contain bg-[#F8F8F8] rounded-lg">\n              <div class="flex-1 leading-tight"><div class="text-[14px] font-semibold text-[#1C1C1C]">Chakraveer</div><div class="text-[11px] text-[#606060]">Last used · 10 cases</div></div>\n              <div class="text-right"><div class="text-[14px] font-semibold text-[#0C831F]">&#8377;18,000</div><div class="text-[9px] text-[#9E9E9E]">25.4% margin</div></div>\n            </div>\n            <div onclick="loadCalc(\'imida\')" class="bg-white border border-[#EDEDED] rounded-xl p-3 flex items-center gap-3 cursor-pointer active:bg-[#F8F8F8]">\n              <img src="https://katyayanikrishidirect.com/cdn/shop/files/IMIDA_4.webp" class="w-10 h-10 object-contain bg-[#F8F8F8] rounded-lg">\n              <div class="flex-1 leading-tight"><div class="text-[14px] font-semibold text-[#1C1C1C]">Imida 30.5% SC</div><div class="text-[11px] text-[#606060]">8 Apr · 20 units</div></div>\n              <div class="text-right"><div class="text-[14px] font-semibold text-[#0C831F]">&#8377;2,400</div><div class="text-[9px] text-[#9E9E9E]">22% margin</div></div>\n            </div>\n            <div onclick="loadCalc(\'npk\')" class="bg-white border border-[#EDEDED] rounded-xl p-3 flex items-center gap-3 cursor-pointer active:bg-[#F8F8F8]">\n              <img src="https://katyayanikrishidirect.com/cdn/shop/files/NPK_19-19-19_Front.webp" class="w-10 h-10 object-contain bg-[#F8F8F8] rounded-lg">\n              <div class="flex-1 leading-tight"><div class="text-[14px] font-semibold text-[#1C1C1C]">NPK 19-19-19</div><div class="text-[11px] text-[#606060]">3 Apr · 5 bags</div></div>\n              <div class="text-right"><div class="text-[14px] font-semibold text-[#0C831F]">&#8377;1,850</div><div class="text-[9px] text-[#9E9E9E]">28% margin</div></div>\n            </div>\n          </div>\n        </div>\n      </div>\n\n      <!-- CALC VIEW (hidden until product selected) -->\n      <div id="calcView" class="hidden p-4 space-y-3">'
)

# Close the calcView div before the sticky CTA
html = html.replace(
    '    </div>\n\n    <!-- Sticky CTA -->',
    '    </div><!-- /calcView -->\n\n    <!-- Sticky CTA -->'
)

# Hide sticky CTA by default, only show in calc state
html = html.replace(
    '    <!-- Sticky CTA -->\n    <div class="absolute bottom-0 left-0 right-0 bg-white border-t border-[#EDEDED] p-3 grid grid-cols-2 gap-2" style="padding-bottom:env(safe-area-inset-bottom,20px);">',
    '    <!-- Sticky CTA -->\n    <div id="stickyCalcCta" class="hidden absolute bottom-0 left-0 right-0 bg-white border-t border-[#EDEDED] p-3 grid grid-cols-2 gap-2" style="padding-bottom:env(safe-area-inset-bottom,20px);">'
)

# ── 2. Wire Change button to openProductPicker ────────────────────────────────
html = html.replace(
    '            <button class="flex items-center gap-1 text-[12px] font-semibold text-[#0E7A4E] px-2 py-1 border border-[#0E7A4E]/40 rounded-full">\n              Change\n              <svg width="10" height="10" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="#0E7A4E" stroke-width="2.5" stroke-linecap="round"/></svg>\n            </button>',
    '            <button onclick="openProductPicker()" class="flex items-center gap-1 text-[12px] font-semibold text-[#0E7A4E] px-2 py-1 border border-[#0E7A4E]/40 rounded-full">\n              Change\n              <svg width="10" height="10" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="#0E7A4E" stroke-width="2.5" stroke-linecap="round"/></svg>\n            </button>'
)

# ── 3. Add product picker sheet + JS before service worker ────────────────────
picker_block = """
  <!-- Product picker sheet -->
  <div id="pickerBd" class="hidden absolute inset-0 bg-black/45 z-50" onclick="closeProductPicker()"></div>
  <div id="pickerPanel" class="hidden absolute bottom-0 left-0 right-0 z-50 bg-white rounded-t-[28px]" style="max-height:85%;box-shadow:0 -8px 30px rgba(0,0,0,.15)">
    <div class="px-5 pt-3 pb-2">
      <div class="mx-auto w-10 h-1 rounded-full bg-[#E8E8E8] mb-4"></div>
      <div class="flex items-center justify-between mb-3">
        <div class="brand-font text-[20px] text-[#1C1C1C]">Select Product</div>
        <button onclick="closeProductPicker()" class="text-[13px] font-medium text-[#606060] border border-[#EDEDED] rounded-full px-3 py-1">Close</button>
      </div>
      <!-- Search -->
      <div class="relative mb-3">
        <input type="text" id="pickerSearch" placeholder="Search products…" oninput="filterPicker(this.value)" class="w-full border border-[#EDEDED] rounded-xl pl-9 pr-3 py-2.5 text-[14px] text-[#1C1C1C] outline-none focus:border-[#0E7A4E] bg-[#F8F8F8]">
        <svg class="absolute left-3 top-1/2 -translate-y-1/2" width="14" height="14" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="8" stroke="#9E9E9E" stroke-width="2"/><path d="M21 21l-4.35-4.35" stroke="#9E9E9E" stroke-width="2"/></svg>
      </div>
    </div>
    <div class="overflow-y-auto px-5 pb-6 space-y-2" style="max-height:55vh" id="pickerList">
      <!-- Products injected by JS -->
    </div>
  </div>

  <script>
  var PRODUCTS = [
    {id:'chakraveer', name:'Chakraveer', tech:'Chlorantraniliprole 18.5% SC · 250 ml', img:'https://katyayanikrishidirect.com/cdn/shop/files/ChakraveerNewMockup.webp', buy:440, mrp:650, sell:590, units:'per bottle', case_qty:12},
    {id:'imida',      name:'Imida 30.5% SC', tech:'Imidacloprid 30.5% SC · 250 ml',    img:'https://katyayanikrishidirect.com/cdn/shop/files/IMIDA_4.webp', buy:280, mrp:500, sell:430, units:'per bottle', case_qty:20},
    {id:'ema5',       name:'EMA5',           tech:'Emamectin Benzoate 5% SG · 100 g',   img:'https://katyayanikrishidirect.com/cdn/shop/files/EMA5.webp', buy:296, mrp:480, sell:400, units:'per pack', case_qty:20},
    {id:'npk',        name:'NPK 19-19-19',   tech:'Water Soluble Fertilizer · 1 kg',    img:'https://katyayanikrishidirect.com/cdn/shop/files/NPK_19-19-19_Front.webp', buy:330, mrp:550, sell:470, units:'per kg', case_qty:10},
    {id:'bhannaat',   name:'Bhannaat',        tech:'Thiamethoxam 12.6%+Lambda 9.5% ZC', img:'https://katyayanikrishidirect.com/cdn/shop/files/Bhannat_2.webp', buy:334, mrp:520, sell:445, units:'per bottle', case_qty:20},
    {id:'azodharma',  name:'Azodharma',       tech:'Azoxystrobin 11%+Tebuconazole 18.3% SC', img:'https://katyayanikrishidirect.com/cdn/shop/files/Azodharma_1.webp', buy:310, mrp:500, sell:430, units:'per bottle', case_qty:20},
    {id:'chakrawarti',name:'Chakrawarti ZC',  tech:'Thiamethoxam+Lambda-Cyhalothrin ZC', img:'https://katyayanikrishidirect.com/cdn/shop/files/ChakraveerNewMockup.webp', buy:358, mrp:580, sell:498, units:'per bottle', case_qty:20},
    {id:'bhumiraja',  name:'Bhumiraja',       tech:'Bio Fertilizer · 1 L',              img:'https://katyayanikrishidirect.com/cdn/shop/files/Bhumiraja_1.webp', buy:218, mrp:360, sell:298, units:'per bottle', case_qty:12}
  ];

  function renderPickerList(items){
    var html='';
    items.forEach(function(p){
      var margin = Math.round((p.sell-p.buy)/p.sell*100);
      html += '<div onclick="selectProduct(\\''+p.id+'\\')" class="flex items-center gap-3 py-2.5 border-b border-[#F3F3F3] cursor-pointer active:bg-[#F8F8F8] rounded-xl px-2">' +
        '<img src="'+p.img+'" class="w-12 h-12 object-contain bg-[#F8F8F8] rounded-xl flex-shrink-0">' +
        '<div class="flex-1 leading-tight"><div class="text-[15px] font-semibold text-[#1C1C1C]">'+p.name+'</div><div class="text-[11px] text-[#606060] mt-0.5">'+p.tech+'</div></div>' +
        '<div class="text-right flex-shrink-0"><div class="text-[13px] font-bold text-[#0C831F]">~'+margin+'% margin</div><div class="text-[11px] text-[#9E9E9E]">₹'+p.buy+' '+p.units+'</div></div>' +
        '</div>';
    });
    document.getElementById('pickerList').innerHTML = html;
  }

  function openProductPicker(){
    renderPickerList(PRODUCTS);
    document.getElementById('pickerSearch').value='';
    document.getElementById('pickerBd').classList.remove('hidden');
    document.getElementById('pickerPanel').classList.remove('hidden');
  }
  function closeProductPicker(){
    document.getElementById('pickerBd').classList.add('hidden');
    document.getElementById('pickerPanel').classList.add('hidden');
  }
  function filterPicker(q){
    var filtered = PRODUCTS.filter(function(p){ return p.name.toLowerCase().includes(q.toLowerCase()) || p.tech.toLowerCase().includes(q.toLowerCase()); });
    renderPickerList(filtered);
  }

  function selectProduct(id){
    var p = PRODUCTS.find(function(x){return x.id===id;});
    if(!p) return;
    closeProductPicker();
    // Update product display
    document.querySelector('#calcView .w-14 img').src = p.img;
    document.querySelector('#calcView .text-\\[15px\\].font-semibold.text-\\[\\#1C1C1C\\]').textContent = 'Katyayani '+p.name;
    document.querySelector('#calcView .text-\\[12px\\].text-\\[\\#606060\\].font-medium').textContent = p.tech;
    // Update price inputs
    document.querySelector('input[type="number"]').value = p.buy;
    // Show calc view, hide empty state
    document.getElementById('emptyState').classList.add('hidden');
    document.getElementById('calcView').classList.remove('hidden');
    document.getElementById('stickyCalcCta').classList.remove('hidden');
  }

  function loadCalc(id){ selectProduct(id); }
  </script>
"""

html = html.replace(
    '  <script>if("serviceWorker"in navigator)',
    picker_block + '\n  <script>if("serviceWorker"in navigator)'
)

with open('screens/profit-calculator.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('profit-calculator.html done.')
