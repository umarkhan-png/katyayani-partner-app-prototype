import os

BASE = r'C:\Users\ASUS\katyayani-partner-app\screens'

# ============================================================
# shop-by-disease.html  (items 12 + 13)
# ============================================================
print('\n[shop-by-disease.html]')
with open(os.path.join(BASE, 'shop-by-disease.html'), 'r', encoding='utf-8') as f:
    s = f.read()

# 13. Remove search icon from header
s = s.replace(
    '\n    <a href="search.html" class="w-9 h-9 rounded-full border border-[#EDEDED] flex items-center justify-center">\n      <svg width="17" height="17" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="8" stroke="#1C1C1C" stroke-width="2"/><path d="M21 21l-4.35-4.35" stroke="#1C1C1C" stroke-width="2" stroke-linecap="round"/></svg>\n    </a>',
    ''
)
print('  13. Search bar removed')

# 12. Replace SVG crop icons with real photo-style tiles using color backgrounds + emoji + name
crop_svg_replacements = [
    # Rice
    (
        '        <button class="flex flex-col items-center min-w-[68px]">\n'
        '          <div class="w-[60px] h-[60px] rounded-2xl flex items-center justify-center border-2 border-[#0E7A4E] bg-white">\n'
        '            <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#0E7A4E" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M8 6c0 2 2 4 4 4M16 6c0 2-2 4-4 4M6 10c0 2 3 4 6 4M18 10c0 2-3 4-6 4M8 14c0 2 2 4 4 4M16 14c0 2-2 4-4 4"/></svg>\n'
        '          </div>\n'
        '          <div class="text-[12px] font-semibold text-[#0E7A4E] mt-1.5">Rice</div>\n'
        '        </button>',
        '        <button class="flex flex-col items-center min-w-[68px]">\n'
        '          <div class="w-[60px] h-[60px] rounded-2xl border-2 border-[#0E7A4E] overflow-hidden relative">\n'
        '            <div class="absolute inset-0 flex items-center justify-center text-[28px]" style="background:linear-gradient(135deg,#D8F3E3,#A8DDB5)">🌾</div>\n'
        '          </div>\n'
        '          <div class="text-[12px] font-semibold text-[#0E7A4E] mt-1.5">Rice</div>\n'
        '        </button>',
    ),
    # Chilli
    (
        '        <button class="flex flex-col items-center min-w-[68px]">\n'
        '          <div class="w-[60px] h-[60px] rounded-2xl flex items-center justify-center border border-[#EDEDED] bg-white">\n'
        '            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#1C1C1C" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4c-4 4-4 12 0 16 4-4 4-12 0-16zM9 6c-2 0-3 2-3 4M15 6c2 0 3 2 3 4"/></svg>\n'
        '          </div>\n'
        '          <div class="text-[12px] font-medium text-[#1C1C1C] mt-1.5">Chilli</div>\n'
        '        </button>',
        '        <button class="flex flex-col items-center min-w-[68px]">\n'
        '          <div class="w-[60px] h-[60px] rounded-2xl border border-[#EDEDED] overflow-hidden relative">\n'
        '            <div class="absolute inset-0 flex items-center justify-center text-[28px]" style="background:linear-gradient(135deg,#FFE3D3,#FECACA)">🌶️</div>\n'
        '          </div>\n'
        '          <div class="text-[12px] font-medium text-[#1C1C1C] mt-1.5">Chilli</div>\n'
        '        </button>',
    ),
    # Maize
    (
        '        <button class="flex flex-col items-center min-w-[68px]">\n'
        '          <div class="w-[60px] h-[60px] rounded-2xl flex items-center justify-center border border-[#EDEDED] bg-white">\n'
        '            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#1C1C1C" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="13" rx="6" ry="8"/><path d="M12 5V2M9 8h6M9 12h6M9 16h6"/></svg>\n'
        '          </div>\n'
        '          <div class="text-[12px] font-medium text-[#1C1C1C] mt-1.5">Maize</div>\n'
        '        </button>',
        '        <button class="flex flex-col items-center min-w-[68px]">\n'
        '          <div class="w-[60px] h-[60px] rounded-2xl border border-[#EDEDED] overflow-hidden relative">\n'
        '            <div class="absolute inset-0 flex items-center justify-center text-[28px]" style="background:linear-gradient(135deg,#FFF4C2,#FDE68A)">🌽</div>\n'
        '          </div>\n'
        '          <div class="text-[12px] font-medium text-[#1C1C1C] mt-1.5">Maize</div>\n'
        '        </button>',
    ),
    # Tomato
    (
        '        <button class="flex flex-col items-center min-w-[68px]">\n'
        '          <div class="w-[60px] h-[60px] rounded-2xl flex items-center justify-center border border-[#EDEDED] bg-white">\n'
        '            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#1C1C1C" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="14" r="7"/><path d="M12 7V4M10 4h4"/></svg>\n'
        '          </div>\n'
        '          <div class="text-[12px] font-medium text-[#1C1C1C] mt-1.5">Tomato</div>\n'
        '        </button>',
        '        <button class="flex flex-col items-center min-w-[68px]">\n'
        '          <div class="w-[60px] h-[60px] rounded-2xl border border-[#EDEDED] overflow-hidden relative">\n'
        '            <div class="absolute inset-0 flex items-center justify-center text-[28px]" style="background:linear-gradient(135deg,#FEE2E2,#FECACA)">🍅</div>\n'
        '          </div>\n'
        '          <div class="text-[12px] font-medium text-[#1C1C1C] mt-1.5">Tomato</div>\n'
        '        </button>',
    ),
    # Cotton
    (
        '        <button class="flex flex-col items-center min-w-[68px]">\n'
        '          <div class="w-[60px] h-[60px] rounded-2xl flex items-center justify-center border border-[#EDEDED] bg-white">\n'
        '            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#1C1C1C" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4M5 5l3 3M16 16l3 3M19 5l-3 3M8 16l-3 3"/></svg>\n'
        '          </div>\n'
        '          <div class="text-[12px] font-medium text-[#1C1C1C] mt-1.5">Cotton</div>\n'
        '        </button>',
        '        <button class="flex flex-col items-center min-w-[68px]">\n'
        '          <div class="w-[60px] h-[60px] rounded-2xl border border-[#EDEDED] overflow-hidden relative">\n'
        '            <div class="absolute inset-0 flex items-center justify-center text-[28px]" style="background:linear-gradient(135deg,#F8F8F8,#E8F4E8)">🪴</div>\n'
        '          </div>\n'
        '          <div class="text-[12px] font-medium text-[#1C1C1C] mt-1.5">Cotton</div>\n'
        '        </button>',
    ),
    # Veggies
    (
        '        <button class="flex flex-col items-center min-w-[68px]">\n'
        '          <div class="w-[60px] h-[60px] rounded-2xl flex items-center justify-center border border-[#EDEDED] bg-white">\n'
        '            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#1C1C1C" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c5-5 5-15 0-20-5 5-5 15 0 20zM12 4v18"/></svg>\n'
        '          </div>\n'
        '          <div class="text-[12px] font-medium text-[#1C1C1C] mt-1.5">Veggies</div>\n'
        '        </button>',
        '        <button class="flex flex-col items-center min-w-[68px]">\n'
        '          <div class="w-[60px] h-[60px] rounded-2xl border border-[#EDEDED] overflow-hidden relative">\n'
        '            <div class="absolute inset-0 flex items-center justify-center text-[28px]" style="background:linear-gradient(135deg,#D8F3E3,#A8E6C8)">🥦</div>\n'
        '          </div>\n'
        '          <div class="text-[12px] font-medium text-[#1C1C1C] mt-1.5">Veggies</div>\n'
        '        </button>',
    ),
]

for old, new in crop_svg_replacements:
    c = s.count(old)
    s = s.replace(old, new)
    print(f'  12. crop icon: {c} hit(s)')

with open(os.path.join(BASE, 'shop-by-disease.html'), 'w', encoding='utf-8') as f:
    f.write(s)
print('  -> shop-by-disease.html saved')


# ============================================================
# my-farmers.html  (items 17 + 18)
# ============================================================
print('\n[my-farmers.html]')
with open(os.path.join(BASE, 'my-farmers.html'), 'r', encoding='utf-8') as f:
    m = f.read()

# 17. Make Add Farmer button open a sheet
m = m.replace(
    '    <button class="bg-[#0C831F] text-white rounded-xl py-2.5 flex items-center justify-center gap-1.5">\n      <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="white" stroke-width="2.5" stroke-linecap="round"/></svg>\n      <span class="text-[14px] font-bold uppercase tracking-wider">Add Farmer</span>\n    </button>',
    '    <button onclick="openAddFarmer()" class="bg-[#0C831F] text-white rounded-xl py-2.5 flex items-center justify-center gap-1.5">\n      <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="white" stroke-width="2.5" stroke-linecap="round"/></svg>\n      <span class="text-[14px] font-bold uppercase tracking-wider">Add Farmer</span>\n    </button>'
)
print('  17. Add Farmer button wired to openAddFarmer()')

# 18. Make all farmer cards tappable (wrap existing div with onclick)
# Cards 1, 2, 4, 5 are standard; card 3 has due-payment style
# Replace the opening div of each card to add onclick
FARMER_CARDS = [
    ('Sohan Patel', 'sohan_patel', 'Cotton · 12 acre · Dhar', 'SP', '#F0FDF5', '#0E7A4E', '30', 'VIP'),
    ('Ramesh Yadav', 'ramesh_yadav', 'Soybean · 8 acre · Dewas', 'RY', '#FFF4D6', '#8B6914', '22', None),
    ('Sitaram Bhilala', 'sitaram_bhilala', 'Maize · 6 acre · Mhow', 'SB', '#F0FDF5', '#0E7A4E', '12', None),
    ('Prakash Kumar', 'prakash_kumar', 'Chilli · 3 acre · Sehore', 'PK', '#FFF4D6', '#8B6914', '8', None),
]

# Wrap each regular farmer card div with onclick
for name, fid, sub, initials, bg, color, orders, badge in FARMER_CARDS:
    old_div = f'    <div class="bg-white border border-[#EDEDED] rounded-2xl p-3">\n      <div class="flex items-center gap-3">\n        <div class="w-12 h-12 rounded-full bg-[{bg}] border border-[{color}]/30 flex items-center justify-center brand-font text-[16px] text-[{color}]">{initials}</div>\n        <div class="flex-1 leading-tight">'
    new_div = f'    <div class="bg-white border border-[#EDEDED] rounded-2xl p-3" onclick="openFarmerDetail(\'{fid}\')" style="cursor:pointer">\n      <div class="flex items-center gap-3">\n        <div class="w-12 h-12 rounded-full bg-[{bg}] border border-[{color}]/30 flex items-center justify-center brand-font text-[16px] text-[{color}]">{initials}</div>\n        <div class="flex-1 leading-tight">'
    c = m.count(old_div)
    m = m.replace(old_div, new_div)
    print(f'  18. {name}: {c} card made tappable')

# Add "View Details ›" hint at bottom of each stats row for those 4 cards
# (after the grid grid-cols-3 block)
m = m.replace(
    '<div class="mt-3 pt-2.5 border-t border-[#EDEDED] grid grid-cols-3 gap-2 text-center">',
    '<div class="mt-3 pt-2.5 border-t border-[#EDEDED]"><div class="grid grid-cols-3 gap-2 text-center mb-2">',
    4  # only replace 4 occurrences (not the due-payment card)
)
m = m.replace(
    '      </div>\n    </div>\n\n    <!-- Card 2',
    '        </div>\n        <div class="text-[11px] text-[#0E7A4E] font-semibold text-center">View details & manage →</div>\n      </div>\n    </div>\n\n    <!-- Card 2'
)
m = m.replace(
    '      </div>\n    </div>\n\n    <!-- Card 3 — Due payment',
    '        </div>\n        <div class="text-[11px] text-[#0E7A4E] font-semibold text-center">View details & manage →</div>\n      </div>\n    </div>\n\n    <!-- Card 3 — Due payment'
)
m = m.replace(
    '      </div>\n    </div>\n\n    <!-- Card 4',
    '        </div>\n        <div class="text-[11px] text-[#0E7A4E] font-semibold text-center">View details & manage →</div>\n      </div>\n    </div>\n\n    <!-- Card 4'
)
m = m.replace(
    '      </div>\n    </div>\n\n    <!-- Card 5',
    '        </div>\n        <div class="text-[11px] text-[#0E7A4E] font-semibold text-center">View details & manage →</div>\n      </div>\n    </div>\n\n    <!-- Card 5'
)
m = m.replace(
    '      </div>\n    </div>\n\n  </div>\n\n  <div class="h-6">',
    '        </div>\n        <div class="text-[11px] text-[#0E7A4E] font-semibold text-center">View details & manage →</div>\n      </div>\n    </div>\n\n  </div>\n\n  <div class="h-6">'
)

# Add farmer detail sheet + add farmer sheet before service worker
farmers_sheets = r"""
  <!-- Farmer detail sheet -->
  <div id="farmerDetailBd" class="hidden absolute inset-0 bg-black/45 z-50" onclick="closeFarmerDetail()"></div>
  <div id="farmerDetailPanel" class="hidden absolute bottom-0 left-0 right-0 z-50 bg-white rounded-t-[28px] overflow-hidden" style="max-height:85%;box-shadow:0 -8px 30px rgba(0,0,0,.15)">
    <div class="overflow-y-auto" style="max-height:85vh">
      <div class="px-5 pt-3 pb-2">
        <div class="mx-auto w-10 h-1 rounded-full bg-[#E8E8E8] mb-4"></div>
        <div id="farmerDetailContent"><!-- injected --></div>
      </div>
    </div>
  </div>

  <!-- Add Farmer sheet -->
  <div id="addFarmerBd" class="hidden absolute inset-0 bg-black/45 z-50" onclick="closeAddFarmer()"></div>
  <div id="addFarmerPanel" class="hidden absolute bottom-0 left-0 right-0 z-50 bg-white rounded-t-[28px] overflow-hidden" style="max-height:90%;box-shadow:0 -8px 30px rgba(0,0,0,.15)">
    <div class="overflow-y-auto" style="max-height:88vh">
      <div class="px-5 pt-3 pb-6">
        <div class="mx-auto w-10 h-1 rounded-full bg-[#E8E8E8] mb-4"></div>
        <div class="brand-font text-[20px] text-[#1C1C1C] mb-4">Add Farmer</div>
        <div class="space-y-3">
          <div>
            <div class="text-[12px] font-semibold text-[#606060] mb-1 uppercase tracking-wider">Full Name *</div>
            <input type="text" placeholder="Ramesh Patel" class="w-full border border-[#EDEDED] rounded-xl px-4 py-3 text-[15px] text-[#1C1C1C] outline-none focus:border-[#0E7A4E]"/>
          </div>
          <div>
            <div class="text-[12px] font-semibold text-[#606060] mb-1 uppercase tracking-wider">Phone Number *</div>
            <input type="tel" placeholder="+91 98765 43210" class="w-full border border-[#EDEDED] rounded-xl px-4 py-3 text-[15px] text-[#1C1C1C] outline-none focus:border-[#0E7A4E]"/>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <div class="text-[12px] font-semibold text-[#606060] mb-1 uppercase tracking-wider">Main Crop</div>
              <input type="text" placeholder="Cotton, Rice..." class="w-full border border-[#EDEDED] rounded-xl px-4 py-3 text-[15px] text-[#1C1C1C] outline-none focus:border-[#0E7A4E]"/>
            </div>
            <div>
              <div class="text-[12px] font-semibold text-[#606060] mb-1 uppercase tracking-wider">Farm Size</div>
              <input type="text" placeholder="5 acres" class="w-full border border-[#EDEDED] rounded-xl px-4 py-3 text-[15px] text-[#1C1C1C] outline-none focus:border-[#0E7A4E]"/>
            </div>
          </div>
          <div>
            <div class="text-[12px] font-semibold text-[#606060] mb-1 uppercase tracking-wider">Village / Town</div>
            <input type="text" placeholder="Indore, Dewas..." class="w-full border border-[#EDEDED] rounded-xl px-4 py-3 text-[15px] text-[#1C1C1C] outline-none focus:border-[#0E7A4E]"/>
          </div>
          <div>
            <div class="text-[12px] font-semibold text-[#606060] mb-1 uppercase tracking-wider">Notes (optional)</div>
            <textarea placeholder="Payment terms, preferred products..." class="w-full border border-[#EDEDED] rounded-xl px-4 py-3 text-[14px] text-[#1C1C1C] outline-none focus:border-[#0E7A4E] h-20 resize-none"></textarea>
          </div>
          <button onclick="closeAddFarmer()" class="w-full bg-[#0C831F] text-white font-bold text-[15px] py-3.5 rounded-xl uppercase tracking-wider mt-2">Save Farmer</button>
        </div>
      </div>
    </div>
  </div>

  <script>
  var FARMER_DATA = {
    sohan_patel:   {name:'Sohan Patel',  initials:'SP', crop:'Cotton', acres:'12 acre', village:'Dhar',    spent:'₹42,800', orders:'18', last:'3 days ago',   phone:'98711 22334', due:null},
    ramesh_yadav:  {name:'Ramesh Yadav', initials:'RY', crop:'Soybean',acres:'8 acre',  village:'Dewas',   spent:'₹18,450', orders:'9',  last:'11 days ago',  phone:'94251 88760', due:null},
    sitaram_bhilala:{name:'Sitaram Bhilala',initials:'SB',crop:'Maize',acres:'6 acre', village:'Mhow',    spent:'₹9,280',  orders:'5',  last:'Today',         phone:'93011 44523', due:null},
    prakash_kumar: {name:'Prakash Kumar',initials:'PK', crop:'Chilli', acres:'3 acre',  village:'Sehore',  spent:'₹6,150',  orders:'3',  last:'45 days ago',  phone:'97551 36892', due:null}
  };
  function openFarmerDetail(id) {
    var f = FARMER_DATA[id]; if(!f) return;
    document.getElementById('farmerDetailContent').innerHTML =
      '<div class="flex items-center gap-3 mb-4">' +
        '<div class="w-16 h-16 rounded-2xl bg-[#F0FDF5] border border-[#0E7A4E]/30 flex items-center justify-center brand-font text-[22px] text-[#0E7A4E]">'+f.initials+'</div>' +
        '<div class="flex-1"><div class="text-[20px] font-black text-[#1C1C1C]">'+f.name+'</div>' +
        '<div class="text-[13px] text-[#606060] mt-0.5">'+f.crop+' · '+f.acres+' · '+f.village+'</div></div>' +
      '</div>' +
      '<div class="grid grid-cols-3 gap-2 mb-4">' +
        '<div class="bg-[#F0FDF5] rounded-xl p-3 text-center"><div class="text-[9px] text-[#606060] font-bold uppercase">Spent</div><div class="text-[16px] font-black text-[#0C831F] mt-0.5">'+f.spent+'</div></div>' +
        '<div class="bg-[#F8F8F8] rounded-xl p-3 text-center"><div class="text-[9px] text-[#606060] font-bold uppercase">Orders</div><div class="text-[16px] font-black text-[#1C1C1C] mt-0.5">'+f.orders+'</div></div>' +
        '<div class="bg-[#F8F8F8] rounded-xl p-3 text-center"><div class="text-[9px] text-[#606060] font-bold uppercase">Last Buy</div><div class="text-[11px] font-bold text-[#1C1C1C] mt-0.5">'+f.last+'</div></div>' +
      '</div>' +
      '<div class="text-[13px] font-semibold text-[#606060] uppercase tracking-wider mb-2">Actions</div>' +
      '<div class="grid grid-cols-2 gap-2 mb-4">' +
        '<button onclick="closeFarmerDetail()" class="flex items-center gap-2 bg-[#F0FDF5] border border-[#0E7A4E]/20 rounded-xl p-3"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0E7A4E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.13.96.37 1.9.72 2.8a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.9.35 1.84.59 2.8.72A2 2 0 0122 16.92z"/></svg><span class="text-[13px] font-semibold text-[#1C1C1C]">Call</span></button>' +
        '<button onclick="closeFarmerDetail()" class="flex items-center gap-2 bg-[#F0FDF5] border border-[#0E7A4E]/20 rounded-xl p-3"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0E7A4E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/></svg><span class="text-[13px] font-semibold text-[#1C1C1C]">WhatsApp</span></button>' +
        '<button onclick="closeFarmerDetail()" class="flex items-center gap-2 bg-[#F8F8F8] border border-[#EDEDED] rounded-xl p-3"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1C1C1C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg><span class="text-[13px] font-semibold text-[#1C1C1C]">Edit Info</span></button>' +
        '<button onclick="closeFarmerDetail()" class="flex items-center gap-2 bg-white border border-[#EDEDED] rounded-xl p-3"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1C1C1C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 6h15l-1.5 9h-12zM6 6L5 3H2M9 20a1 1 0 100 2 1 1 0 000-2zM18 20a1 1 0 100 2 1 1 0 000-2z"/></svg><span class="text-[13px] font-semibold text-[#1C1C1C]">Create Order</span></button>' +
      '</div>' +
      '<button onclick="closeFarmerDetail()" class="w-full border border-[#E23744]/30 text-[#E23744] font-semibold text-[13px] py-2.5 rounded-xl">Remove Farmer</button>';
    document.getElementById('farmerDetailBd').classList.remove('hidden');
    document.getElementById('farmerDetailPanel').classList.remove('hidden');
  }
  function closeFarmerDetail(){document.getElementById('farmerDetailBd').classList.add('hidden');document.getElementById('farmerDetailPanel').classList.add('hidden');}
  function openAddFarmer(){document.getElementById('addFarmerBd').classList.remove('hidden');document.getElementById('addFarmerPanel').classList.remove('hidden');}
  function closeAddFarmer(){document.getElementById('addFarmerBd').classList.add('hidden');document.getElementById('addFarmerPanel').classList.add('hidden');}
  </script>
"""

m = m.replace('  <script>if("serviceWorker"in navigator)', farmers_sheets + '  <script>if("serviceWorker"in navigator)')
print('  17/18. Farmer sheets + JS added')

with open(os.path.join(BASE, 'my-farmers.html'), 'w', encoding='utf-8') as f:
    f.write(m)
print('  -> my-farmers.html saved')


# ============================================================
# partner-transfer.html  (item 19)
# ============================================================
print('\n[partner-transfer.html]')
with open(os.path.join(BASE, 'partner-transfer.html'), 'r', encoding='utf-8') as f:
    pt = f.read()

# 19a. "In stock" → "~Available" (softer language)
pt = pt.replace(
    '<div class="text-[8px] font-black text-white bg-[#0C831F] px-1.5 py-0.5 rounded uppercase tracking-wider">In stock</div>',
    '<div class="text-[8px] font-bold text-[#0C831F] bg-[#F0FDF5] border border-[#0E7A4E]/30 px-1.5 py-0.5 rounded uppercase tracking-wider">~Available</div>'
)
print('  19a. In stock -> ~Available')

# 19b. Wire Request buttons to show "Request Sent" confirmation sheet
pt = pt.replace(
    '          <button class="bg-[#0C831F] text-white text-[13px] font-bold uppercase tracking-wider px-3 py-1.5 rounded-lg">Request</button>',
    '          <button onclick="openRequestSent()" class="bg-[#0C831F] text-white text-[13px] font-bold uppercase tracking-wider px-3 py-1.5 rounded-lg">Request</button>'
)
print('  19b. Request buttons wired')

# 19c. Add "Request Sent" next-steps sheet
request_sheet = r"""
  <!-- Request sent confirmation sheet -->
  <div id="reqSentBd" class="hidden absolute inset-0 bg-black/45 z-50" onclick="closeRequestSent()"></div>
  <div id="reqSentPanel" class="hidden absolute bottom-0 left-0 right-0 z-50 bg-white rounded-t-[28px] p-5" style="box-shadow:0 -8px 30px rgba(0,0,0,.15)">
    <div class="mx-auto w-10 h-1 rounded-full bg-[#E8E8E8] mb-4"></div>
    <div class="text-center mb-5">
      <div class="w-16 h-16 rounded-full bg-[#F0FDF5] border border-[#0E7A4E]/30 flex items-center justify-center mx-auto mb-3">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0C831F" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg>
      </div>
      <div class="brand-font text-[22px] text-[#1C1C1C]">Request Sent!</div>
      <div class="text-[13px] text-[#606060] mt-1">Waiting for partner to confirm availability</div>
    </div>
    <div class="space-y-3 mb-5">
      <div class="flex items-start gap-3">
        <div class="w-6 h-6 rounded-full bg-[#0C831F] text-white flex items-center justify-center text-[11px] font-black flex-shrink-0">✓</div>
        <div><div class="text-[13px] font-semibold text-[#1C1C1C]">Request sent to partner</div><div class="text-[11px] text-[#606060]">They'll respond within 2–4 hours</div></div>
      </div>
      <div class="flex items-start gap-3">
        <div class="w-6 h-6 rounded-full bg-[#EDEDED] text-[#9E9E9E] flex items-center justify-center text-[11px] font-black flex-shrink-0">2</div>
        <div><div class="text-[13px] font-semibold text-[#606060]">Partner confirms stock &amp; quotes price</div><div class="text-[11px] text-[#9E9E9E]">Price may vary from listed amount</div></div>
      </div>
      <div class="flex items-start gap-3">
        <div class="w-6 h-6 rounded-full bg-[#EDEDED] text-[#9E9E9E] flex items-center justify-center text-[11px] font-black flex-shrink-0">3</div>
        <div><div class="text-[13px] font-semibold text-[#606060]">You approve &amp; arrange pickup/delivery</div><div class="text-[11px] text-[#9E9E9E]">Settled through Katyayani platform</div></div>
      </div>
    </div>
    <div class="bg-[#FFF8E6] border border-[#D4A537]/30 rounded-xl p-3 mb-4 text-[12px] text-[#8B6914]">
      ⚠️ Stock availability is not guaranteed until the partner confirms. Final quantity may be less than requested.
    </div>
    <button onclick="closeRequestSent()" class="w-full bg-[#0C831F] text-white font-bold text-[15px] py-3.5 rounded-xl">Got it · View My Requests</button>
  </div>
  <script>
  function openRequestSent(){document.getElementById('reqSentBd').classList.remove('hidden');document.getElementById('reqSentPanel').classList.remove('hidden');}
  function closeRequestSent(){document.getElementById('reqSentBd').classList.add('hidden');document.getElementById('reqSentPanel').classList.add('hidden');}
  </script>
"""
pt = pt.replace('  <script>if("serviceWorker"in navigator)', request_sheet + '  <script>if("serviceWorker"in navigator)')
print('  19c. Request-sent confirmation sheet added')

with open(os.path.join(BASE, 'partner-transfer.html'), 'w', encoding='utf-8') as f:
    f.write(pt)
print('  -> partner-transfer.html saved')

print('\nAll done.')
