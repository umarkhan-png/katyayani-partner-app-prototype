pdp_path = r'C:\Users\ASUS\katyayani-partner-app\screens\pdp.html'

with open(pdp_path, 'r', encoding='utf-8') as f:
    p = f.read()

# 7. Add search icon to PDP header (before shareBtn)
old_btns = '''        <div class="flex items-center gap-1.5">
          <button id="shareBtn" class="w-9 h-9 rounded-full border border-[#EDEDED] flex items-center justify-center" title="Share">'''
new_btns = '''        <div class="flex items-center gap-1.5">
          <a href="search.html" class="w-9 h-9 rounded-full border border-[#EDEDED] flex items-center justify-center">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="8" stroke="#1C1C1C" stroke-width="2"/><path d="M21 21l-4.35-4.35" stroke="#1C1C1C" stroke-width="2" stroke-linecap="round"/></svg>
          </a>
          <button id="shareBtn" class="w-9 h-9 rounded-full border border-[#EDEDED] flex items-center justify-center" title="Share">'''
if old_btns in p:
    p = p.replace(old_btns, new_btns)
    print('7. Added PDP search icon')
else:
    print('7. MISS: header buttons')

# 8. Wrap PDP header in sticky outer div
old_hdr_open = '      <div class="px-4 pt-3 pb-2 flex items-center justify-between sticky top-0 bg-white z-20 border-b border-[#EDEDED]">'
new_hdr_open = '      <div class="sticky top-0 bg-white z-20 border-b border-[#EDEDED]">\n      <div class="px-4 pt-3 pb-2 flex items-center justify-between">'
if old_hdr_open in p:
    p = p.replace(old_hdr_open, new_hdr_open)
    print('8a. Wrapped PDP header in sticky outer')
else:
    print('8a. MISS: header opening div')

# 8b. After inner header closes, add mini bar + close outer wrapper
old_after_hdr = '''        </div>
      </div>

      <!-- ============== GALLERY (compact, white bg, static 30s demo button) ============== -->'''
new_after_hdr = '''        </div>
      </div>
      <div id="pdpStickyBar" class="overflow-hidden transition-all duration-200" style="max-height:0">
        <div class="px-4 pb-2 pt-1 flex items-center gap-2.5 border-t border-[#EDEDED]/60">
          <img src="https://katyayanikrishidirect.com/cdn/shop/files/IMIDA_4.webp" class="w-8 h-8 object-contain bg-[#F8F8F8] rounded-lg p-0.5 flex-shrink-0">
          <div class="flex-1 min-w-0">
            <div class="text-[11.5px] font-bold text-[#1C1C1C] truncate leading-tight">Imida 30.5% SC</div>
            <div class="text-[9px] text-[#606060] truncate">Imidacloprid 30.5% SC</div>
          </div>
          <div class="text-[14px] font-extrabold text-[#1C1C1C] flex-shrink-0">&#8377;2,880</div>
        </div>
      </div>
      </div>

      <!-- ============== GALLERY (compact, white bg, static 30s demo button) ============== -->'''
if old_after_hdr in p:
    p = p.replace(old_after_hdr, new_after_hdr)
    print('8b. Added PDP sticky mini bar')
else:
    print('8b. MISS: after-header context')

# 10+11. Add retailer videos + farmer videos before reviews section
old_reviews_marker = '      <!-- ============== RATINGS & REVIEWS (edge-to-edge tinted bg) ============== -->\n      <div id="reviews"'
new_before_reviews = '''      <!-- ============== RETAILER TESTIMONIAL VIDEOS ============== -->
      <div class="mt-6 px-4">
        <div class="flex items-center justify-between mb-3">
          <div>
            <div class="text-[13px] font-semibold text-[#1C1C1C]">Retailer Reviews</div>
            <div class="text-[10px] text-[#606060] mt-0.5">Real feedback from dukaan partners</div>
          </div>
          <a href="#" class="text-[10px] font-bold text-[#0E7A4E]">SEE ALL (18)</a>
        </div>
        <div class="overflow-x-auto -mx-4 px-4" style="scrollbar-width:none">
          <div class="flex gap-3 min-w-max">
            <div class="w-[140px] h-[180px] rounded-2xl overflow-hidden relative flex-shrink-0" style="background:#1C1C1C">
              <img src="https://katyayanikrishidirect.com/cdn/shop/files/IMIDA_4.webp" class="w-full h-full object-cover" style="opacity:.35;filter:blur(2px)">
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center border border-white/40 mb-2"><svg width="14" height="14" viewBox="0 0 24 24" fill="white"><polygon points="6 3 20 12 6 21 6 3"/></svg></div>
                <div class="text-white text-[9px] font-semibold text-center px-2">Ramesh Patel</div>
                <div class="text-[8px] text-center" style="color:rgba(255,255,255,.6)">Indore Retailer</div>
              </div>
              <div class="absolute bottom-2 left-2 right-2 rounded-lg px-2 py-1" style="background:rgba(0,0,0,.5)"><div class="text-white text-[8px] font-medium leading-tight">"Best results in 3 days"</div></div>
            </div>
            <div class="w-[140px] h-[180px] rounded-2xl overflow-hidden relative flex-shrink-0" style="background:#1C1C1C">
              <img src="https://katyayanikrishidirect.com/cdn/shop/files/ChakraveerNewMockup.webp" class="w-full h-full object-cover" style="opacity:.35;filter:blur(2px)">
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center border border-white/40 mb-2"><svg width="14" height="14" viewBox="0 0 24 24" fill="white"><polygon points="6 3 20 12 6 21 6 3"/></svg></div>
                <div class="text-white text-[9px] font-semibold text-center px-2">Suresh Kumar</div>
                <div class="text-[8px] text-center" style="color:rgba(255,255,255,.6)">Bhopal Retailer</div>
              </div>
              <div class="absolute bottom-2 left-2 right-2 rounded-lg px-2 py-1" style="background:rgba(0,0,0,.5)"><div class="text-white text-[8px] font-medium leading-tight">"Farmers love this product"</div></div>
            </div>
            <div class="w-[140px] h-[180px] rounded-2xl overflow-hidden relative flex-shrink-0" style="background:#1C1C1C">
              <img src="https://katyayanikrishidirect.com/cdn/shop/files/Ema_5_new_Mock_0.5x.webp" class="w-full h-full object-cover" style="opacity:.35;filter:blur(2px)">
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center border border-white/40 mb-2"><svg width="14" height="14" viewBox="0 0 24 24" fill="white"><polygon points="6 3 20 12 6 21 6 3"/></svg></div>
                <div class="text-white text-[9px] font-semibold text-center px-2">Dinesh Sharma</div>
                <div class="text-[8px] text-center" style="color:rgba(255,255,255,.6)">Ujjain Retailer</div>
              </div>
              <div class="absolute bottom-2 left-2 right-2 rounded-lg px-2 py-1" style="background:rgba(0,0,0,.5)"><div class="text-white text-[8px] font-medium leading-tight">"&#8377;500 margin per box"</div></div>
            </div>
          </div>
        </div>
      </div>

      <!-- ============== FARMER VIDEOS ============== -->
      <div class="mt-6 px-4">
        <div class="flex items-center justify-between mb-3">
          <div>
            <div class="text-[13px] font-semibold text-[#1C1C1C]">Farmer Results</div>
            <div class="text-[10px] text-[#606060] mt-0.5">See how it worked on real farms</div>
          </div>
          <a href="#" class="text-[10px] font-bold text-[#0E7A4E]">SEE ALL (42)</a>
        </div>
        <div class="overflow-x-auto -mx-4 px-4" style="scrollbar-width:none">
          <div class="flex gap-3 min-w-max">
            <div class="w-[140px] h-[180px] rounded-2xl overflow-hidden relative flex-shrink-0" style="background:#083D28">
              <img src="https://katyayanikrishidirect.com/cdn/shop/files/IMIDA_4.webp" class="w-full h-full object-cover" style="opacity:.3;filter:blur(2px)">
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center border border-white/40 mb-2"><svg width="14" height="14" viewBox="0 0 24 24" fill="white"><polygon points="6 3 20 12 6 21 6 3"/></svg></div>
                <div class="text-white text-[9px] font-semibold text-center px-2">Kishan Yadav</div>
                <div class="text-[8px] text-center" style="color:rgba(255,255,255,.6)">Soybean &#183; Indore</div>
              </div>
              <div class="absolute bottom-2 left-2 right-2 rounded-lg px-2 py-1" style="background:rgba(0,0,0,.5)"><div class="text-white text-[8px] font-medium leading-tight">"Jassids 100% control"</div></div>
            </div>
            <div class="w-[140px] h-[180px] rounded-2xl overflow-hidden relative flex-shrink-0" style="background:#083D28">
              <img src="https://katyayanikrishidirect.com/cdn/shop/files/Bhumiraja_2_1.webp" class="w-full h-full object-cover" style="opacity:.3;filter:blur(2px)">
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center border border-white/40 mb-2"><svg width="14" height="14" viewBox="0 0 24 24" fill="white"><polygon points="6 3 20 12 6 21 6 3"/></svg></div>
                <div class="text-white text-[9px] font-semibold text-center px-2">Mohan Verma</div>
                <div class="text-[8px] text-center" style="color:rgba(255,255,255,.6)">Cotton &#183; Khandwa</div>
              </div>
              <div class="absolute bottom-2 left-2 right-2 rounded-lg px-2 py-1" style="background:rgba(0,0,0,.5)"><div class="text-white text-[8px] font-medium leading-tight">"Yield up 20%"</div></div>
            </div>
            <div class="w-[140px] h-[180px] rounded-2xl overflow-hidden relative flex-shrink-0" style="background:#083D28">
              <img src="https://katyayanikrishidirect.com/cdn/shop/files/NPK_19-19-19_Front.webp" class="w-full h-full object-cover" style="opacity:.3;filter:blur(2px)">
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center border border-white/40 mb-2"><svg width="14" height="14" viewBox="0 0 24 24" fill="white"><polygon points="6 3 20 12 6 21 6 3"/></svg></div>
                <div class="text-white text-[9px] font-semibold text-center px-2">Balram Kushwaha</div>
                <div class="text-[8px] text-center" style="color:rgba(255,255,255,.6)">Wheat &#183; Sehore</div>
              </div>
              <div class="absolute bottom-2 left-2 right-2 rounded-lg px-2 py-1" style="background:rgba(0,0,0,.5)"><div class="text-white text-[8px] font-medium leading-tight">"Used for 2 seasons"</div></div>
            </div>
          </div>
        </div>
      </div>

      <!-- ============== RATINGS & REVIEWS (edge-to-edge tinted bg) ============== -->
      <div id="reviews"'''
if old_reviews_marker in p:
    p = p.replace(old_reviews_marker, new_before_reviews)
    print('10+11. Added retailer + farmer video sections')
else:
    print('10+11. MISS: reviews marker')

# Add JS for sticky bar scroll behaviour (before wishlist toggle comment)
old_wishlist = '  // Wishlist toggle'
new_js_inject = '''  // PDP sticky mini bar on scroll
  document.getElementById('scroll').addEventListener('scroll', function() {
    var bar = document.getElementById('pdpStickyBar');
    if (bar) bar.style.maxHeight = this.scrollTop > 230 ? '60px' : '0';
  });

  // Wishlist toggle'''
if old_wishlist in p:
    p = p.replace(old_wishlist, new_js_inject)
    print('8c. Added sticky bar JS')
else:
    print('8c. MISS: wishlist comment')

with open(pdp_path, 'w', encoding='utf-8') as f:
    f.write(p)
print('\npdp.html done.')
