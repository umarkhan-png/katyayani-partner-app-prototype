with open(r'C:\Users\ASUS\katyayani-partner-app\screens\pdp.html', 'r', encoding='utf-8') as f:
    p = f.read()

# 1. Class A badge → pill
p = p.replace(
    '          <!-- Product Classification badge (top-right) -->\n          <div class="absolute top-3 right-3 w-8 h-8 rounded-xl flex flex-col items-center justify-center" style="background:linear-gradient(135deg,#0E7A4E,#0C831F);box-shadow:0 3px 8px rgba(14,122,78,0.35)">\n            <span class="text-[16px] font-extrabold text-white leading-none">A</span>\n            <span class="text-[5.5px] text-white/75 font-bold uppercase tracking-wide leading-none mt-0.5">Class</span>\n          </div>',
    '          <!-- Product Classification badge (top-right) -->\n          <div class="absolute top-3 right-3 flex items-center gap-1 px-2.5 py-1 rounded-full" style="background:linear-gradient(135deg,#0E7A4E,#0C831F);box-shadow:0 4px 10px rgba(14,122,78,0.35)">\n            <span class="text-[8px] text-white/80 font-semibold uppercase tracking-widest leading-none">Class</span>\n            <span class="text-[14px] font-black text-white leading-none">A</span>\n          </div>'
)
print('1. done')

# 2a. Tighten dots row bottom padding
p = p.replace(
    '        <div class="px-5 pb-2 pt-0 flex items-center justify-between gap-2">',
    '        <div class="px-5 pb-1 pt-0 flex items-center justify-between gap-2">'
)
print('2a. done')

# 2b. Tighten product info section
p = p.replace(
    '      <div class="px-4 pt-2">\n        <div class="flex items-start justify-between gap-2">\n          <h1 class="brand-font text-[26px] text-[#1C1C1C] leading-tight">Imida</h1>\n          <div class="mt-1.5 flex-shrink-0 inline-flex items-center bg-[#F0FDF5] text-[#0E7A4E] px-2 py-0.5 rounded-full text-[12px] font-bold">\n            Insecticide\n          </div>\n        </div>\n        <div class="text-[15px] text-[#606060] mt-1 font-medium">Imidacloprid 30.5% SC</div>\n      </div>',
    '      <div class="px-4 pt-1">\n        <div class="flex items-center justify-between gap-2">\n          <h1 class="brand-font text-[24px] text-[#1C1C1C] leading-tight">Imida</h1>\n          <div class="flex-shrink-0 inline-flex items-center bg-[#F0FDF5] text-[#0E7A4E] px-2 py-0.5 rounded-full text-[12px] font-bold">\n            Insecticide\n          </div>\n        </div>\n        <div class="text-[13px] text-[#606060] mt-0.5 font-medium">Imidacloprid 30.5% SC</div>\n      </div>'
)
print('2b. done')

# 3. Pack tiles 10% wider: w-[88px] → w-[97px]
count3 = p.count('w-[88px]')
p = p.replace('w-[88px]', 'w-[97px]')
print(f'3. done ({count3} tiles)')

# 4. Per-case label sizes: text-[8px] → text-[10px]
p = p.replace(
    'class="text-[8px] text-[#606060] font-bold uppercase tracking-wider">Retailer · per case</div>',
    'class="text-[10px] text-[#606060] font-bold uppercase tracking-wider">Retailer · per case</div>'
)
p = p.replace(
    'class="text-[8px] text-[#8B6914] font-bold uppercase tracking-wider">Distributor · per case</div>',
    'class="text-[10px] text-[#8B6914] font-bold uppercase tracking-wider">Distributor · per case</div>'
)
print('4. done')

# 5. Retailer 44% off → separate line below price (mirrors distributor save line)
p = p.replace(
    '                <div class="flex items-baseline gap-1 mt-1 flex-wrap">\n                  <div class="text-[24px] font-black text-[#1C1C1C] leading-none">₹2,880</div>\n                  <div class="text-[12px] text-[#9E9E9E] price-strike font-medium">₹5,140</div>\n                  <div class="text-[12px] text-[#0C831F] font-bold">44% off</div>\n                </div>',
    '                <div class="flex items-baseline gap-1 mt-1">\n                  <div class="text-[24px] font-black text-[#1C1C1C] leading-none">₹2,880</div>\n                  <div class="text-[12px] text-[#9E9E9E] price-strike font-medium">₹5,140</div>\n                </div>\n                <div class="text-[9px] text-[#0C831F] font-semibold mt-0.5">44% off · retailer price</div>'
)
print('5. done')

# 6a. Remove row bg colors from price table
p = p.replace(
    '<div class="grid grid-cols-[1.5fr_1fr_1fr] px-3 py-2 items-center border-t border-[#EDEDED] bg-[#F0FDF5]">',
    '<div class="grid grid-cols-[1.5fr_1fr_1fr] px-3 py-2 items-center border-t border-[#EDEDED]">'
)
p = p.replace(
    '<div class="grid grid-cols-[1.5fr_1fr_1fr] px-3 py-2 items-center border-t border-[#EDEDED] bg-[#FFF8E6]">',
    '<div class="grid grid-cols-[1.5fr_1fr_1fr] px-3 py-2 items-center border-t border-[#EDEDED]">'
)
print('6a. done')

# 6b. Highlight Margin header
p = p.replace(
    '              <div class="text-center">Margin</div>',
    '              <div class="text-center text-[#0E7A4E] font-black">Margin</div>'
)
print('6b. done')

# 6c. Highlight margin value cells
p = p.replace(
    '<div class="text-center text-[13px] text-[#9E9E9E] font-medium">—</div>',
    '<div class="text-center text-[13px] text-[#9E9E9E] font-medium bg-[#F8F8F8] rounded px-0.5">—</div>'
)
p = p.replace(
    '<div class="text-center text-[14px] font-bold text-[#0C831F]">78%</div>',
    '<div class="text-center text-[14px] font-bold text-[#0C831F] bg-[#F0FDF5] rounded px-0.5">78%</div>'
)
p = p.replace(
    '<div class="text-center text-[14px] font-bold text-[#8B6914]">82%</div>',
    '<div class="text-center text-[14px] font-bold text-[#8B6914] bg-[#FFF8E6] rounded px-0.5">82%</div>'
)
print('6c. done')

# 7a. Scheme tile 1: wider + readable name
p = p.replace(
    '          <div class="flex-shrink-0 w-[220px] bg-white border border-[#EDEDED] rounded-2xl p-3.5">\n            <div class="flex items-start justify-between gap-1 mb-1">\n              <div class="text-[13px] font-bold text-[#1C1C1C] leading-tight">KT_KHARIF_SLAB_FY26</div>',
    '          <div class="flex-shrink-0 w-[260px] bg-white border border-[#EDEDED] rounded-2xl p-3.5">\n            <div class="flex items-start justify-between gap-1 mb-1">\n              <div class="text-[13px] font-bold text-[#1C1C1C] leading-tight">Kharif Slab FY26</div>'
)
# 7b. Scheme tile 2
p = p.replace(
    '          <div class="flex-shrink-0 w-[220px] bg-white border border-[#EDEDED] rounded-2xl p-3.5">\n            <div class="flex items-start justify-between gap-1 mb-1">\n              <div class="text-[12px] font-bold text-[#1C1C1C] leading-tight">KT_ANNUAL_DHAMAKA_FY26</div>',
    '          <div class="flex-shrink-0 w-[260px] bg-white border border-[#EDEDED] rounded-2xl p-3.5">\n            <div class="flex items-start justify-between gap-1 mb-1">\n              <div class="text-[13px] font-bold text-[#1C1C1C] leading-tight">Annual Dhamaka FY26</div>'
)
# 7c. Scheme tile 3
p = p.replace(
    '          <div class="flex-shrink-0 w-[220px] bg-white border border-[#EDEDED] rounded-2xl p-3.5">\n            <div class="flex items-start justify-between gap-1 mb-1">\n              <div class="text-[13px] font-bold text-[#1C1C1C] leading-tight">KT_MP_REGION_FY26</div>',
    '          <div class="flex-shrink-0 w-[260px] bg-white border border-[#EDEDED] rounded-2xl p-3.5">\n            <div class="flex items-start justify-between gap-1 mb-1">\n              <div class="text-[13px] font-bold text-[#1C1C1C] leading-tight">MP Region FY26</div>'
)
# Also rename in pricing details breakdown
p = p.replace('KT_KHARIF_SLAB_FY26', 'Kharif Slab FY26')
print('7abc. done')

# 7d. Add 4th realtime tile (Summer Cashback)
fourth_tile = '\n          <!-- Scheme 4 — SUMMER CASHBACK (realtime) -->\n          <div class="flex-shrink-0 w-[260px] border rounded-2xl p-3.5" style="background:linear-gradient(135deg,#F0FDF5,#E4F5EC);border-color:rgba(14,122,78,0.3)">\n            <div class="flex items-start justify-between gap-1 mb-1">\n              <div class="text-[13px] font-bold text-[#1C1C1C] leading-tight">Summer Cashback</div>\n              <div class="flex items-center gap-1 bg-[#0C831F] text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full flex-shrink-0 whitespace-nowrap">\n                <span class="w-1.5 h-1.5 bg-white rounded-full" style="display:inline-block;animation:pulse-ring 1.4s ease-out infinite"></span>LIVE\n              </div>\n            </div>\n            <div class="text-[11px] font-semibold text-[#0E7A4E] mb-2">&#x1F4B0; 1% CASHBACK on any purchase</div>\n            <div class="h-1.5 bg-[#D8EBDF] rounded-full overflow-hidden mb-1">\n              <div class="h-full rounded-full bg-[#0C831F]" style="width:88%"></div>\n            </div>\n            <div class="flex items-center justify-between mb-2">\n              <div class="text-[11px] text-[#0E7A4E]">&#8377;8.8L / &#8377;10L</div>\n              <div class="text-[11px] font-bold text-[#0C831F]">88% done</div>\n            </div>\n            <div class="border-t border-[#D8EBDF] pt-1.5">\n              <div class="text-[11px] text-[#606060]">Auto-credited: <span class="font-semibold text-[#0C831F]">&#8377;880 earned this month</span></div>\n            </div>\n          </div>\n'

# Insert before closing of scheme flex container (unique anchor: SMART TV entry)
p = p.replace(
    '              <div class="text-[11px] text-[#606060]">Entry: <span class="font-semibold text-[#1C1C1C]">SMART TV 43&quot;</span></div>\n            </div>\n          </div>\n\n        </div>',
    '              <div class="text-[11px] text-[#606060]">Entry: <span class="font-semibold text-[#1C1C1C]">SMART TV 43&quot;</span></div>\n            </div>\n          </div>\n' + fourth_tile + '\n        </div>'
)
print('7d. done')

# 8. Pricing Details title outside card border
p = p.replace(
    '      <!-- ============== PRICING DETAILS ============== -->\n      <div class="mx-4 mt-4 rounded-2xl overflow-hidden border border-[#EDEDED] bg-white">\n        <div class="px-4 pt-3.5 pb-2.5 border-b border-[#F0F0F0]">\n          <div class="text-[15px] font-bold text-[#1C1C1C]">Pricing Details</div>\n        </div>\n        <div class="px-4 pt-1 pb-3">',
    '      <!-- ============== PRICING DETAILS ============== -->\n      <div class="px-4 mt-4 mb-2">\n        <div class="text-[15px] font-bold text-[#1C1C1C]">Pricing Details</div>\n      </div>\n      <div class="mx-4 rounded-2xl overflow-hidden border border-[#EDEDED] bg-white">\n        <div class="px-4 pt-1 pb-3">'
)
print('8. done')

# 9. Move delivery section ABOVE Season Heatmap
delivery_marker = '      <!-- ============== DELIVERY (clean 2-row card, softer weights) ============== -->'
about_marker    = '      <!-- ============== ABOUT (moved ABOVE How to Use per new hierarchy) ============== -->'
season_marker   = '      <!-- ============== SEASON HEATMAP (moved above Live Activity per PM) ============== -->'

d_idx = p.index(delivery_marker)
a_idx = p.index(about_marker)
delivery_block = p[d_idx:a_idx]
p = p[:d_idx] + p[a_idx:]
p = p.replace(season_marker, delivery_block + season_marker, 1)
print('9. done')

# 10. FBT text sizes
p = p.replace('<div class="text-[#1C1C1C] font-semibold">Imida</div>',     '<div class="text-[13px] text-[#1C1C1C] font-semibold">Imida</div>')
p = p.replace('<div class="text-[#1C1C1C] font-semibold">Azodharma</div>', '<div class="text-[13px] text-[#1C1C1C] font-semibold">Azodharma</div>')
p = p.replace('<div class="text-[#606060] font-medium">NPK 19:19:19</div>','<div class="text-[13px] text-[#606060] font-medium">NPK 19:19:19</div>')
p = p.replace('<div class="text-[9px] text-[#606060]">250 ml · 20 pcs/case</div>', '<div class="text-[11px] text-[#606060]">250 ml · 20 pcs/case</div>')
p = p.replace('<div class="text-[9px] text-[#9E9E9E]">1 kg · 10 packs/case</div>', '<div class="text-[11px] text-[#9E9E9E]">1 kg · 10 packs/case</div>')
p = p.replace('<div class="text-[9px] text-[#606060]">₹144/pc</div>',  '<div class="text-[11px] text-[#606060]">₹144/pc</div>')
p = p.replace('<div class="text-[9px] text-[#606060]">₹160/pc</div>',  '<div class="text-[11px] text-[#606060]">₹160/pc</div>')
p = p.replace('<div class="text-[9px] text-[#9E9E9E]">₹330/pack</div>','<div class="text-[11px] text-[#9E9E9E]">₹330/pack</div>')
p = p.replace('<span class="text-[16px] font-black text-[#1C1C1C]">₹6,080</span>', '<span class="text-[18px] font-black text-[#1C1C1C]">₹6,080</span>')
print('10. done')

with open(r'C:\Users\ASUS\katyayani-partner-app\screens\pdp.html', 'w', encoding='utf-8') as f:
    f.write(p)
print('\npdp.html done.')
