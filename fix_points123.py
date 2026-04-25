import re

# ═══════════════════════════════════════════════════════════════════
# POINT 1 — language.html: tiles +25% taller + confirmation modal
# ═══════════════════════════════════════════════════════════════════
with open('screens/language.html', encoding='utf-8') as f:
    lang = f.read()

# 1a. py-3.5 → py-6 on all lang-tile anchors (adds ~10px each side = +25% total height)
lang = lang.replace('rounded-2xl px-4 py-3.5 text-left relative block active:bg-[#F0FDF5] active:border-[#0E7A4E]',
                    'rounded-2xl px-4 py-6 text-left relative block active:bg-[#F0FDF5] active:border-[#0E7A4E]')
print(f'1a. tiles: {lang.count("py-6")} hits')

# 1b. Convert <a href> tiles to <div onclick> so we can intercept and show modal
lang = re.sub(
    r'<a href="rapido-phone\.html" class="lang-tile(.*?)</a>',
    lambda m: '<div onclick="selectLang(this)" class="lang-tile cursor-pointer' + m.group(1) + '</div>',
    lang, flags=re.DOTALL
)
print(f'1b. tiles converted to div')

# 1c. Add language confirmation modal + JS before service worker
modal_html = """
  <!-- Language confirmation modal -->
  <div id="langModalBd" class="hidden absolute inset-0 bg-black/40 z-50" style="backdrop-filter:blur(2px)"></div>
  <div id="langModal" class="hidden absolute bottom-0 left-0 right-0 z-50 bg-white rounded-t-[28px] px-5 pt-3 pb-8" style="box-shadow:0 -8px 32px rgba(0,0,0,.18)">
    <div class="mx-auto w-10 h-1 rounded-full bg-[#E8E8E8] mb-5"></div>
    <div class="flex flex-col items-center text-center mb-6">
      <div class="w-16 h-16 rounded-2xl bg-[#F0FDF5] border border-[#0E7A4E]/25 flex items-center justify-center mb-4">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0E7A4E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg>
      </div>
      <div class="text-[13px] font-semibold text-[#606060] uppercase tracking-wider mb-1">App language set to</div>
      <div id="langModalName" class="text-[30px] font-extrabold text-[#1C1C1C] leading-tight mb-1"></div>
      <div id="langModalSub" class="text-[14px] text-[#9E9E9E]"></div>
    </div>
    <a id="langModalCta" href="rapido-phone.html" class="block w-full bg-[#0C831F] text-white text-center font-bold text-[16px] py-4 rounded-2xl uppercase tracking-wider mb-3">Continue</a>
    <button onclick="closeLangModal()" class="w-full text-[14px] font-medium text-[#606060] py-2">Change language</button>
  </div>

  <script>
  function selectLang(el) {
    var name = el.querySelector('.text-\\[20px\\]')?.textContent?.trim() || '';
    var sub  = el.querySelector('.text-\\[13px\\]')?.textContent?.trim() || '';
    document.getElementById('langModalName').textContent = name;
    document.getElementById('langModalSub').textContent  = sub;
    if (name) localStorage.setItem('kk-lang', name);
    document.getElementById('langModalBd').classList.remove('hidden');
    document.getElementById('langModal').classList.remove('hidden');
  }
  function closeLangModal() {
    document.getElementById('langModalBd').classList.add('hidden');
    document.getElementById('langModal').classList.add('hidden');
  }
  </script>
"""
lang = lang.replace('  <script>if("serviceWorker"in navigator)', modal_html + '\n  <script>if("serviceWorker"in navigator)')

with open('screens/language.html', 'w', encoding='utf-8') as f:
    f.write(lang)
print('1. language.html done\n')


# ═══════════════════════════════════════════════════════════════════
# POINT 2 — rapido-shop-details.html: contextual auto-fill warning
# ═══════════════════════════════════════════════════════════════════
with open('screens/rapido-shop-details.html', encoding='utf-8') as f:
    shop = f.read()

# Replace the auto-fill button with a richer version that shows context + warning
old_btn = '''    <!-- LOCATION AUTO-FILL CARD -->
    <button id="locBtn" onclick="detectLocation()" class="w-full flex items-center gap-3 rounded-xl px-4 py-3.5 mb-4 text-left" style="background:linear-gradient(135deg,#F0FDF5 0%,#E8F5EE 100%);border:1.5px solid rgba(14,122,78,0.25);">
      <div class="w-10 h-10 rounded-full bg-[#0E7A4E] flex items-center justify-center flex-shrink-0">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>
      </div>
      <div class="flex-1">
        <div class="text-[14px] font-semibold text-[#0E7A4E] leading-tight">Auto-fill shop address</div>
        <div class="text-[12px] text-[#606060] mt-0.5">Use current location to fill address</div>
      </div>
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="#0E7A4E" stroke-width="2.5" stroke-linecap="round"/></svg>
    </button>'''

new_btn = '''    <!-- LOCATION AUTO-FILL CARD -->
    <div class="mb-4">
      <button id="locBtn" onclick="confirmLocDetect()" class="w-full flex items-center gap-3 rounded-xl px-4 py-3.5 text-left" style="background:linear-gradient(135deg,#F0FDF5 0%,#E8F5EE 100%);border:1.5px solid rgba(14,122,78,0.25);">
        <div class="w-10 h-10 rounded-full bg-[#0E7A4E] flex items-center justify-center flex-shrink-0">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>
        </div>
        <div class="flex-1">
          <div class="text-[14px] font-semibold text-[#0E7A4E] leading-tight">Auto-fill shop address</div>
          <div class="text-[12px] text-[#606060] mt-0.5">Uses your <b class="text-[#0E7A4E]">current GPS location</b> to fill the address</div>
        </div>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="#0E7A4E" stroke-width="2.5" stroke-linecap="round"/></svg>
      </button>
      <!-- Context hint -->
      <div class="flex items-start gap-2 mt-2 px-1">
        <svg class="flex-shrink-0 mt-0.5" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#D4A537" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
        <div class="text-[11.5px] text-[#8B6914] font-medium leading-snug">Only tap this if you are <b>currently at your shop</b>. Your phone&apos;s GPS location will be used as your shop address.</div>
      </div>
    </div>'''

shop = shop.replace(old_btn, new_btn)

# Add confirmation sheet + updated detectLocation()
confirm_sheet = """
  <!-- Location confirm sheet -->
  <div id="locConfirmBd" class="hidden absolute inset-0 bg-black/40 z-50"></div>
  <div id="locConfirmPanel" class="hidden absolute bottom-0 left-0 right-0 z-50 bg-white rounded-t-[28px] px-5 pt-3 pb-8" style="box-shadow:0 -8px 32px rgba(0,0,0,.18)">
    <div class="mx-auto w-10 h-1 rounded-full bg-[#E8E8E8] mb-5"></div>
    <div class="flex flex-col items-center text-center mb-5">
      <div class="w-16 h-16 rounded-2xl bg-[#FFF8E6] border border-[#D4A537]/30 flex items-center justify-center mb-4">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#D4A537" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>
      </div>
      <div class="text-[20px] font-extrabold text-[#1C1C1C] mb-2">Are you at your shop?</div>
      <div class="text-[14px] text-[#606060] leading-relaxed">Your current GPS location will be saved as your <b class="text-[#1C1C1C]">shop address</b>. Make sure you&apos;re physically at your shop before continuing.</div>
    </div>
    <button onclick="closeLocConfirm();detectLocation();" class="w-full bg-[#0C831F] text-white font-bold text-[15px] py-4 rounded-2xl mb-3">Yes, I&apos;m at my shop — Detect location</button>
    <button onclick="closeLocConfirm()" class="w-full border border-[#EDEDED] text-[#606060] font-semibold text-[14px] py-3.5 rounded-2xl">No, I&apos;ll enter manually</button>
  </div>
"""

# Add confirmLocDetect function to existing script
shop = shop.replace(
    'function detectLocation() {',
    'function confirmLocDetect() {\n  document.getElementById(\'locConfirmBd\').classList.remove(\'hidden\');\n  document.getElementById(\'locConfirmPanel\').classList.remove(\'hidden\');\n}\nfunction closeLocConfirm() {\n  document.getElementById(\'locConfirmBd\').classList.add(\'hidden\');\n  document.getElementById(\'locConfirmPanel\').classList.add(\'hidden\');\n}\nfunction detectLocation() {'
)

# Insert confirm sheet before service worker script
shop = shop.replace('  <script>if("serviceWorker"in navigator)', confirm_sheet + '\n  <script>if("serviceWorker"in navigator)')

with open('screens/rapido-shop-details.html', 'w', encoding='utf-8') as f:
    f.write(shop)
print('2. rapido-shop-details.html done\n')


# ═══════════════════════════════════════════════════════════════════
# POINT 3 — pdp.html: Price Match feature (Agrim-style)
# ═══════════════════════════════════════════════════════════════════
with open('screens/pdp.html', encoding='utf-8') as f:
    pdp = f.read()

# 3a. Add "Seen it cheaper?" link near the retailer price section
# Anchor: the 44% off · retailer price line
pdp = pdp.replace(
    '                <div class="text-[9px] text-[#0C831F] font-semibold mt-0.5">44% off · retailer price</div>',
    '                <div class="text-[9px] text-[#0C831F] font-semibold mt-0.5">44% off · retailer price</div>\n                <button onclick="openPriceMatch()" class="flex items-center gap-1 mt-1.5 text-[10px] font-semibold text-[#9E9E9E] hover:text-[#0E7A4E] transition-colors"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg> Seen it cheaper elsewhere?</button>'
)
print('3a. "Seen it cheaper?" link added')

# 3b. Add price match sheet + JS before service worker
price_match_sheet = """
  <!-- ====== PRICE MATCH SHEET ====== -->
  <div id="pmBd" class="hidden absolute inset-0 bg-black/45 z-50" onclick="closePriceMatch()"></div>
  <div id="pmPanel" class="hidden absolute bottom-0 left-0 right-0 z-50 bg-white rounded-t-[28px]" style="max-height:90%;overflow-y:auto;box-shadow:0 -8px 32px rgba(0,0,0,.18)">
    <div class="px-5 pt-3 pb-8">
      <div class="mx-auto w-10 h-1 rounded-full bg-[#E8E8E8] mb-4"></div>

      <!-- Header -->
      <div class="flex items-center justify-between mb-4">
        <div>
          <div class="brand-font text-[20px] text-[#1C1C1C]">Price Match</div>
          <div class="text-[12px] text-[#606060] mt-0.5">Found it cheaper? We'll match it.</div>
        </div>
        <button onclick="closePriceMatch()" class="text-[13px] font-medium text-[#606060] border border-[#EDEDED] rounded-full px-3 py-1">Close</button>
      </div>

      <!-- How it works pill -->
      <div class="flex items-center gap-2 bg-[#F0FDF5] border border-[#0E7A4E]/20 rounded-xl px-3 py-2.5 mb-4">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0E7A4E" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
        <div class="text-[12px] text-[#0E7A4E] font-medium leading-snug">Submit the competitor's price. If verified, we'll match it or offer equivalent credit within 24 hours.</div>
      </div>

      <!-- Current Katyayani price (readonly) -->
      <div class="bg-[#F8F8F8] rounded-xl px-4 py-3 mb-4 flex items-center justify-between">
        <div>
          <div class="text-[10px] font-semibold text-[#606060] uppercase tracking-wider">Katyayani price (retailer)</div>
          <div class="text-[22px] font-black text-[#1C1C1C] mt-0.5">&#8377;2,880 <span class="text-[13px] font-medium text-[#9E9E9E]">/ case</span></div>
        </div>
        <div class="text-right">
          <div class="text-[10px] font-semibold text-[#606060] uppercase tracking-wider">Per bottle</div>
          <div class="text-[16px] font-bold text-[#1C1C1C]">&#8377;144</div>
        </div>
      </div>

      <!-- Competitor details form -->
      <div class="space-y-3 mb-5">
        <div>
          <div class="text-[11px] font-semibold text-[#606060] uppercase tracking-wider mb-1.5">Competitor / Source</div>
          <input type="text" id="pmCompetitor" placeholder="e.g. Local dealer, Amazon, BigHaat, Dehaat…" class="w-full border border-[#EDEDED] rounded-xl px-4 py-3 text-[14px] text-[#1C1C1C] outline-none focus:border-[#0E7A4E]">
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <div class="text-[11px] font-semibold text-[#606060] uppercase tracking-wider mb-1.5">Their price / case</div>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-[14px] font-semibold text-[#606060]">&#8377;</span>
              <input type="number" id="pmPrice" placeholder="2,500" oninput="calcPmDiff()" class="w-full border border-[#EDEDED] rounded-xl pl-7 pr-3 py-3 text-[14px] font-semibold text-[#1C1C1C] outline-none focus:border-[#0E7A4E]">
            </div>
          </div>
          <div>
            <div class="text-[11px] font-semibold text-[#606060] uppercase tracking-wider mb-1.5">Proof (optional)</div>
            <button onclick="document.getElementById('pmProof').click()" class="w-full h-full border border-dashed border-[#EDEDED] rounded-xl flex items-center justify-center gap-1.5 text-[12px] text-[#9E9E9E] font-medium py-3">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#9E9E9E" stroke-width="2" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="M21 15l-5-5L5 21"/></svg>
              Photo
            </button>
            <input type="file" id="pmProof" accept="image/*" class="hidden">
          </div>
        </div>
      </div>

      <!-- Live difference display -->
      <div id="pmDiffCard" class="hidden rounded-2xl p-4 mb-5 border" style="background:linear-gradient(135deg,#F0FDF5,#E4F5EC);border-color:rgba(14,122,78,0.3)">
        <div class="flex items-center justify-between mb-2">
          <div class="text-[12px] font-semibold text-[#0E7A4E] uppercase tracking-wider">You save per case</div>
          <div id="pmSavePct" class="text-[11px] font-bold text-white bg-[#0C831F] px-2 py-0.5 rounded-full"></div>
        </div>
        <div class="flex items-end gap-2">
          <div id="pmSaveAmt" class="text-[32px] font-black text-[#0C831F] leading-none"></div>
          <div class="text-[12px] text-[#0E7A4E] font-medium pb-1">per case · <span id="pmSaveUnit"></span> per bottle</div>
        </div>
        <div class="mt-2.5 h-1.5 bg-[#D8EBDF] rounded-full overflow-hidden">
          <div id="pmSaveBar" class="h-full bg-[#0C831F] rounded-full transition-all duration-500"></div>
        </div>
        <div class="flex justify-between mt-1 text-[10px] text-[#606060]"><span>Competitor</span><span>Katyayani</span></div>
      </div>

      <!-- CTA -->
      <button onclick="submitPriceMatch()" class="w-full bg-[#0C831F] text-white font-bold text-[15px] py-4 rounded-2xl uppercase tracking-wider">Submit Price Match Request</button>
      <div class="text-[11px] text-[#9E9E9E] text-center mt-2.5">Response within 24 hours · Verified before approval</div>
    </div>
  </div>

  <!-- Success toast (price match) -->
  <div id="pmToast" class="hidden absolute left-1/2 -translate-x-1/2 z-[60] flex items-center gap-2 bg-[#1C1C1C] text-white px-4 py-2.5 rounded-full text-[12px] font-semibold shadow-xl whitespace-nowrap" style="bottom:100px">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#7FD0A3" stroke-width="3"><path d="M5 12l5 5L20 7"/></svg>
    Price match request sent! Response in 24 hrs.
  </div>

  <script>
  function openPriceMatch() {
    document.getElementById('pmBd').classList.remove('hidden');
    document.getElementById('pmPanel').classList.remove('hidden');
    document.getElementById('pmDiffCard').classList.add('hidden');
    document.getElementById('pmPrice').value = '';
    document.getElementById('pmCompetitor').value = '';
  }
  function closePriceMatch() {
    document.getElementById('pmBd').classList.add('hidden');
    document.getElementById('pmPanel').classList.add('hidden');
  }
  function calcPmDiff() {
    var their = parseFloat(document.getElementById('pmPrice').value);
    var ours = 2880;
    var card = document.getElementById('pmDiffCard');
    if (!their || their <= 0 || their >= ours) { card.classList.add('hidden'); return; }
    var diff = ours - their;
    var pct  = Math.round(diff / ours * 100);
    var perBottle = Math.round(diff / 20);
    var barWidth  = Math.min(Math.round(diff / ours * 120), 95);
    document.getElementById('pmSaveAmt').textContent  = '\\u20B9' + diff.toLocaleString('en-IN');
    document.getElementById('pmSavePct').textContent  = pct + '% cheaper';
    document.getElementById('pmSaveUnit').textContent = '\\u20B9' + perBottle;
    document.getElementById('pmSaveBar').style.width  = barWidth + '%';
    card.classList.remove('hidden');
  }
  function submitPriceMatch() {
    var comp  = document.getElementById('pmCompetitor').value.trim();
    var price = document.getElementById('pmPrice').value.trim();
    if (!comp || !price) { alert('Please fill competitor name and their price.'); return; }
    closePriceMatch();
    var t = document.getElementById('pmToast');
    t.classList.remove('hidden');
    setTimeout(function(){ t.classList.add('hidden'); }, 3500);
  }
  </script>
"""

pdp = pdp.replace('  <script>if("serviceWorker"in navigator)', price_match_sheet + '\n  <script>if("serviceWorker"in navigator)')
print('3b. Price match sheet added')

with open('screens/pdp.html', 'w', encoding='utf-8') as f:
    f.write(pdp)
print('3. pdp.html done\n')
print('All 3 points done.')
