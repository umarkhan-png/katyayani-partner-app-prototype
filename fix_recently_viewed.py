with open('screens/home.html', 'r', encoding='utf-8') as f:
    h = f.read()

# ── Step 1: Replace Recently Viewed section content ──────────────────────────
OLD_RV = '''      <!-- ============== RECENTLY VIEWED ============== -->
      <div class="mt-6">
        <div class="flex items-center justify-between px-4 mb-3">
          <div>
            <h2 class="brand-font text-[18px]">Recently Viewed</h2>
            <div class="text-[10px] text-[#606060] mt-0.5">Pick up where you left off</div>
          </div>
          <a href="categories.html" class="text-[11px] font-medium text-[#0E7A4E]">SEE ALL</a>
        </div>
        <div class="overflow-x-auto hide-scrollbar pb-2">
          <div class="flex gap-3 px-4 min-w-max">

            <a href="pdp.html" class="block w-[150px] bg-white rounded-2xl border border-[#EDEDED] overflow-hidden flex-shrink-0">
              <div class="relative h-[120px] flex items-center justify-center p-2"><img src="https://katyayanikrishidirect.com/cdn/shop/files/Bhannat_2.webp" class="h-full w-full object-contain"><div class="absolute top-2 right-2 bg-white/85 text-[9px] font-semibold px-1.5 py-0.5 rounded" style="color:#707070">★4.5</div></div>
              <div class="px-2.5 pb-2.5 leading-tight">
                <div class="h-[28px] leading-tight"><div class="text-[12px] font-medium text-[#1C1C1C] truncate">Bhannaat PGR</div><div class="text-[9px] text-[#9E9E9E] truncate">Mepiquat Chloride 5% AS</div></div>
                <div class="flex items-center justify-between mt-1"><span class="text-[10px] text-[#606060]">250 ml × 20</span><span class="text-[10px] font-semibold text-[#D4A537]">Margin 30%</span></div>
                <div class="flex items-end justify-between mt-1.5"><div class="leading-none"><div class="text-[16px] font-extrabold">₹334</div><div class="text-[10px] text-[#9E9E9E] price-strike mt-0.5">₹480</div></div><button class="add-btn">ADD</button></div>
              </div>
            </a>

            <a href="pdp.html" class="block w-[150px] bg-white rounded-2xl border border-[#EDEDED] overflow-hidden flex-shrink-0">
              <div class="relative h-[120px] flex items-center justify-center p-2"><img src="https://katyayanikrishidirect.com/cdn/shop/files/ChakraveerNewMockup.webp" class="h-full w-full object-contain"><div class="absolute top-2 right-2 bg-white/85 text-[9px] font-semibold px-1.5 py-0.5 rounded" style="color:#707070">★4.7</div></div>
              <div class="px-2.5 pb-2.5 leading-tight">
                <div class="h-[28px] leading-tight"><div class="text-[12px] font-medium text-[#1C1C1C] truncate">Chakraveer 18.5%</div><div class="text-[9px] text-[#9E9E9E] truncate">Chlorantraniliprole 18.5% SC</div></div>
                <div class="flex items-center justify-between mt-1"><span class="text-[10px] text-[#606060]">150 ml × 20</span><span class="text-[10px] font-semibold text-[#D4A537]">Margin 32%</span></div>
                <div class="flex items-end justify-between mt-1.5"><div class="leading-none"><div class="text-[16px] font-extrabold">₹440</div><div class="text-[10px] text-[#9E9E9E] price-strike mt-0.5">₹650</div></div><button class="add-btn">ADD</button></div>
              </div>
            </a>

            <a href="pdp.html" class="block w-[150px] bg-white rounded-2xl border border-[#EDEDED] overflow-hidden flex-shrink-0">
              <div class="relative h-[120px] flex items-center justify-center p-2"><img src="https://katyayanikrishidirect.com/cdn/shop/files/NPK_19-19-19_Front.webp" class="h-full w-full object-contain"><div class="absolute top-2 right-2 bg-white/85 text-[9px] font-semibold px-1.5 py-0.5 rounded" style="color:#707070">★4.8</div></div>
              <div class="px-2.5 pb-2.5 leading-tight">
                <div class="h-[28px] leading-tight"><div class="text-[12px] font-medium text-[#1C1C1C] truncate">NPK 19-19-19</div><div class="text-[9px] text-[#9E9E9E] truncate">Water-soluble Fertilizer</div></div>
                <div class="flex items-center justify-between mt-1"><span class="text-[10px] text-[#606060]">1 kg × 10</span><span class="text-[10px] font-semibold text-[#D4A537]">Margin 31%</span></div>
                <div class="flex items-end justify-between mt-1.5"><div class="leading-none"><div class="text-[16px] font-extrabold">₹330</div><div class="text-[10px] text-[#9E9E9E] price-strike mt-0.5">₹480</div></div><button class="add-btn">ADD</button></div>
              </div>
            </a>

            <a href="pdp.html" class="block w-[150px] bg-white rounded-2xl border border-[#EDEDED] overflow-hidden flex-shrink-0">
              <div class="relative h-[120px] flex items-center justify-center p-2"><img src="https://katyayanikrishidirect.com/cdn/shop/files/AZODHARMA_3.webp" class="h-full w-full object-contain"><div class="absolute top-2 right-2 bg-white/85 text-[9px] font-semibold px-1.5 py-0.5 rounded" style="color:#707070">★4.6</div></div>
              <div class="px-2.5 pb-2.5 leading-tight">
                <div class="h-[28px] leading-tight"><div class="text-[12px] font-medium text-[#1C1C1C] truncate">Azodharma Fungicide</div><div class="text-[9px] text-[#9E9E9E] truncate">Azoxystrobin + Tebuconazole</div></div>
                <div class="flex items-center justify-between mt-1"><span class="text-[10px] text-[#606060]">250 ml × 20</span><span class="text-[10px] font-semibold text-[#D4A537]">Margin 31%</span></div>
                <div class="flex items-end justify-between mt-1.5"><div class="leading-none"><div class="text-[16px] font-extrabold">₹310</div><div class="text-[10px] text-[#9E9E9E] price-strike mt-0.5">₹450</div></div><button class="add-btn">ADD</button></div>
              </div>
            </a>

          </div>
        </div>
      </div>'''

NEW_RV = '''      <!-- ============== RECENTLY VIEWED ============== -->
      <div class="mt-6 pt-5 pb-4" style="background:linear-gradient(180deg,#F0FDF5 0%,#DDF4E4 100%);border-top:1px solid #C8E8D3;border-bottom:1px solid #C8E8D3">
        <div class="flex items-center justify-between px-4 mb-3">
          <div>
            <div class="flex items-center gap-1.5"><span class="text-base">🕐</span><h2 class="brand-font text-[18px]">Recently Viewed</h2></div>
            <div class="text-[10px] text-[#606060] mt-0.5">Pick up where you left off</div>
          </div>
          <a href="categories.html" class="text-[11px] font-medium text-[#0E7A4E]">SEE ALL</a>
        </div>
        <div class="overflow-x-auto hide-scrollbar pb-2">
          <div class="flex gap-3 px-4 min-w-max">

            <a href="pdp.html" class="block w-[150px] bg-white rounded-2xl border border-[#EDEDED] overflow-hidden flex-shrink-0">
              <div class="relative h-[120px] flex items-center justify-center p-2"><img src="https://katyayanikrishidirect.com/cdn/shop/files/Bhannat_2.webp" class="h-full w-full object-contain"><div class="absolute top-2 left-2 bg-[#D8F3E3] border border-[#0E7A4E] text-[#0C831F] text-[9px] font-medium px-1.5 py-0.5 rounded">🕐 Today</div><div class="absolute top-2 right-2 bg-white/85 text-[9px] font-semibold px-1.5 py-0.5 rounded" style="color:#707070">★4.5</div></div>
              <div class="px-2.5 pb-2.5 leading-tight">
                <div class="h-[28px] leading-tight"><div class="text-[12px] font-medium text-[#1C1C1C] truncate">Bhannaat PGR</div><div class="text-[9px] text-[#9E9E9E] truncate">Mepiquat Chloride 5% AS</div></div>
                <div class="flex items-center justify-between mt-1"><span class="text-[10px] text-[#606060]">250 ml × 20</span><span class="text-[10px] font-semibold text-[#D4A537]">Margin 30%</span></div>
                <div class="flex items-end justify-between mt-1.5"><div class="leading-none"><div class="text-[16px] font-extrabold">&#8377;334</div><div class="text-[10px] text-[#9E9E9E] price-strike mt-0.5">&#8377;480</div></div><button class="add-btn">ADD</button></div>
              </div>
              <div class="px-2.5 pt-1.5 pb-2 flex items-center gap-1 border-t border-[#F0F0F0]" style="background:#F8FFF9"><span class="text-[8.5px] leading-none"><span class="font-bold" style="color:#0C831F">Last ordered</span><span class="font-medium" style="color:#707070"> &middot; Dec 2025</span></span></div>
            </a>

            <a href="pdp.html" class="block w-[150px] bg-white rounded-2xl border border-[#EDEDED] overflow-hidden flex-shrink-0">
              <div class="relative h-[120px] flex items-center justify-center p-2"><img src="https://katyayanikrishidirect.com/cdn/shop/files/ChakraveerNewMockup.webp" class="h-full w-full object-contain"><div class="absolute top-2 left-2 bg-[#D8F3E3] border border-[#0E7A4E] text-[#0C831F] text-[9px] font-medium px-1.5 py-0.5 rounded">🕐 2 days ago</div><div class="absolute top-2 right-2 bg-white/85 text-[9px] font-semibold px-1.5 py-0.5 rounded" style="color:#707070">★4.7</div></div>
              <div class="px-2.5 pb-2.5 leading-tight">
                <div class="h-[28px] leading-tight"><div class="text-[12px] font-medium text-[#1C1C1C] truncate">Chakraveer 18.5%</div><div class="text-[9px] text-[#9E9E9E] truncate">Chlorantraniliprole 18.5% SC</div></div>
                <div class="flex items-center justify-between mt-1"><span class="text-[10px] text-[#606060]">150 ml × 20</span><span class="text-[10px] font-semibold text-[#D4A537]">Margin 32%</span></div>
                <div class="flex items-end justify-between mt-1.5"><div class="leading-none"><div class="text-[16px] font-extrabold">&#8377;440</div><div class="text-[10px] text-[#9E9E9E] price-strike mt-0.5">&#8377;650</div></div><button class="add-btn">ADD</button></div>
              </div>
              <div class="px-2.5 pt-1.5 pb-2 flex items-center gap-1 border-t border-[#F0F0F0]" style="background:#F8FFF9"><span class="text-[8.5px] leading-none"><span class="font-bold" style="color:#0C831F">Last ordered</span><span class="font-medium" style="color:#707070"> &middot; Nov 2025</span></span></div>
            </a>

            <a href="pdp.html" class="block w-[150px] bg-white rounded-2xl border border-[#EDEDED] overflow-hidden flex-shrink-0">
              <div class="relative h-[120px] flex items-center justify-center p-2"><img src="https://katyayanikrishidirect.com/cdn/shop/files/NPK_19-19-19_Front.webp" class="h-full w-full object-contain"><div class="absolute top-2 left-2 bg-[#D8F3E3] border border-[#0E7A4E] text-[#0C831F] text-[9px] font-medium px-1.5 py-0.5 rounded">🕐 3 days ago</div><div class="absolute top-2 right-2 bg-white/85 text-[9px] font-semibold px-1.5 py-0.5 rounded" style="color:#707070">★4.8</div></div>
              <div class="px-2.5 pb-2.5 leading-tight">
                <div class="h-[28px] leading-tight"><div class="text-[12px] font-medium text-[#1C1C1C] truncate">NPK 19-19-19</div><div class="text-[9px] text-[#9E9E9E] truncate">Water-soluble Fertilizer</div></div>
                <div class="flex items-center justify-between mt-1"><span class="text-[10px] text-[#606060]">1 kg × 10</span><span class="text-[10px] font-semibold text-[#D4A537]">Margin 31%</span></div>
                <div class="flex items-end justify-between mt-1.5"><div class="leading-none"><div class="text-[16px] font-extrabold">&#8377;330</div><div class="text-[10px] text-[#9E9E9E] price-strike mt-0.5">&#8377;480</div></div><button class="add-btn">ADD</button></div>
              </div>
              <div class="px-2.5 pt-1.5 pb-2 flex items-center gap-1 border-t border-[#F0F0F0]" style="background:#F8FFF9"><span class="text-[8.5px] leading-none"><span class="font-bold" style="color:#0C831F">Ordered 3x</span><span class="font-medium" style="color:#707070"> &middot; this season</span></span></div>
            </a>

            <a href="pdp.html" class="block w-[150px] bg-white rounded-2xl border border-[#EDEDED] overflow-hidden flex-shrink-0">
              <div class="relative h-[120px] flex items-center justify-center p-2"><img src="https://katyayanikrishidirect.com/cdn/shop/files/AZODHARMA_3.webp" class="h-full w-full object-contain"><div class="absolute top-2 left-2 bg-[#D8F3E3] border border-[#0E7A4E] text-[#0C831F] text-[9px] font-medium px-1.5 py-0.5 rounded">🕐 1 week ago</div><div class="absolute top-2 right-2 bg-white/85 text-[9px] font-semibold px-1.5 py-0.5 rounded" style="color:#707070">★4.6</div></div>
              <div class="px-2.5 pb-2.5 leading-tight">
                <div class="h-[28px] leading-tight"><div class="text-[12px] font-medium text-[#1C1C1C] truncate">Azodharma Fungicide</div><div class="text-[9px] text-[#9E9E9E] truncate">Azoxystrobin + Tebuconazole</div></div>
                <div class="flex items-center justify-between mt-1"><span class="text-[10px] text-[#606060]">250 ml × 20</span><span class="text-[10px] font-semibold text-[#D4A537]">Margin 31%</span></div>
                <div class="flex items-end justify-between mt-1.5"><div class="leading-none"><div class="text-[16px] font-extrabold">&#8377;310</div><div class="text-[10px] text-[#9E9E9E] price-strike mt-0.5">&#8377;450</div></div><button class="add-btn">ADD</button></div>
              </div>
              <div class="px-2.5 pt-1.5 pb-2 flex items-center gap-1 border-t border-[#F0F0F0]" style="background:#F8FFF9"><span class="text-[8.5px] leading-none"><span class="font-bold" style="color:#0C831F">Last ordered</span><span class="font-medium" style="color:#707070"> &middot; Oct 2025</span></span></div>
            </a>

          </div>
        </div>
      </div>'''

if OLD_RV not in h:
    print('OLD_RV not found!'); exit(1)

h = h.replace(OLD_RV, NEW_RV)
print('Step 1: Restyled Recently Viewed')

# ── Step 2: Swap order — Rabi first, then Recently Viewed ────────────────────
M_RV   = '      <!-- ============== RECENTLY VIEWED ============== -->'
M_RABI = '      <!-- ============== RABI SEASON BESTSELLERS ============== -->'
M_NEXT = '      <!-- ============== MY CROPS'

p_rv   = h.find(M_RV)
p_rabi = h.find(M_RABI)
p_next = h.find(M_NEXT)

if -1 in (p_rv, p_rabi, p_next):
    print('Marker not found'); exit(1)

rv_block   = h[p_rv:p_rabi]
rabi_block = h[p_rabi:p_next]

h = h[:p_rv] + rabi_block + rv_block + h[p_next:]
print('Step 2: Swapped order — Rabi → Recently Viewed')

with open('screens/home.html', 'w', encoding='utf-8') as f:
    f.write(h)

print('Done!')
