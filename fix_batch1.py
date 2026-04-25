import re, os

BASE = r'C:\Users\ASUS\katyayani-partner-app\screens'

def patch(fname, changes):
    path = os.path.join(BASE, fname)
    with open(path, 'r', encoding='utf-8') as f:
        h = f.read()
    for label, old, new in changes:
        c = h.count(old)
        h = h.replace(old, new)
        print(f'  {label}: {c} hit(s)')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(h)
    print(f'  -> {fname} saved')

# ============================================================
# 1. explore.html
# ============================================================
print('\n[explore.html]')
with open(os.path.join(BASE, 'explore.html'), 'r', encoding='utf-8') as f:
    e = f.read()

# 1a. Remove "Smart Tools" title block
e = e.replace(
    '    <div class="flex items-center mb-2.5">\n      <div class="text-[13px] font-semibold text-[#1C1C1C] uppercase tracking-wider">Smart Tools</div>\n\n    </div>\n',
    ''
)
print('  1a. Smart Tools title removed')

# 1b. Remove all tile subtitles (text-[12px] text-[#606060] mt-0.5)
old_count = len(re.findall(r'<div class="text-\[12px\] text-\[#606060\] mt-0\.5">[^<]+</div>', e))
e = re.sub(r'\n        <div class="text-\[12px\] text-\[#606060\] mt-0\.5">[^<]+</div>', '', e)
print(f'  1b. {old_count} tile subtitles removed')

# 1c. Make tile name text slightly bigger: text-[13px] font-semibold → text-[14px] font-semibold
# Only in the tool grid tiles (mt-1.5 signals it's a tile name, not header)
e = e.replace(
    '<div class="text-[13px] font-semibold text-[#1C1C1C] mt-1.5">',
    '<div class="text-[14px] font-semibold text-[#1C1C1C] mt-2">'
)
print('  1c. Tile name size bumped to 14px')

# 1d. Fix Business nav text-[14px] → text-[12px]
e = e.replace(
    '<span class="text-[14px] font-medium text-[#9E9E9E]">Business</span>',
    '<span class="text-[12px] font-medium text-[#9E9E9E]">Business</span>'
)
print('  1d. Business nav font fixed')

# 1e. Add mt-4 grid spacing (remove old mt-5 since title gone)
e = e.replace(
    '  <div class="px-4 mt-5">',
    '  <div class="px-4 mt-4">'
)
print('  1e. Section top margin adjusted')

with open(os.path.join(BASE, 'explore.html'), 'w', encoding='utf-8') as f:
    f.write(e)
print('  -> explore.html saved')

# ============================================================
# 2. scanner.html
# ============================================================
print('\n[scanner.html]')
with open(os.path.join(BASE, 'scanner.html'), 'r', encoding='utf-8') as f:
    s = f.read()

# 2a. Replace ! button in header with Scan Another button
s = s.replace(
    '        <button class="w-9 h-9 rounded-full border border-[#EDEDED] flex items-center justify-center">\n          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#1C1C1C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/></svg>\n        </button>',
    '        <button onclick="openScanOptions()" class="flex items-center gap-1 border border-[#0E7A4E]/50 text-[#0E7A4E] text-[12px] font-bold px-3 py-2 rounded-full">\n          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0E7A4E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="3"/><circle cx="12" cy="12" r="4"/><path d="M7 5l2-2h6l2 2"/></svg>\n          Scan\n        </button>'
)
print('  2a. ! button replaced with Scan button')

# 2b. Add scan options sheet before service worker
scan_sheet = '''
  <!-- Scan options sheet -->
  <div id="scanOptBd" class="hidden absolute inset-0 bg-black/45 z-50" onclick="closeScanOptions()"></div>
  <div id="scanOptPanel" class="hidden absolute bottom-0 left-0 right-0 z-50 bg-white rounded-t-[24px] p-5" style="box-shadow:0 -4px 24px rgba(0,0,0,.14)">
    <div class="mx-auto w-10 h-1 rounded-full bg-[#E8E8E8] mb-5"></div>
    <div class="brand-font text-[18px] text-[#1C1C1C] mb-4">Scan Another</div>
    <div class="grid grid-cols-2 gap-3 pb-2">
      <button onclick="closeScanOptions()" class="flex flex-col items-center gap-2 bg-[#F0FDF5] border border-[#0E7A4E]/20 rounded-2xl p-4">
        <div class="w-12 h-12 rounded-2xl bg-[#0E7A4E] flex items-center justify-center">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="3"/><circle cx="12" cy="12" r="4"/><path d="M7 5l2-2h6l2 2"/></svg>
        </div>
        <div class="text-[13px] font-bold text-[#1C1C1C]">Camera</div>
        <div class="text-[11px] text-[#606060]">Take a photo</div>
      </button>
      <button onclick="closeScanOptions()" class="flex flex-col items-center gap-2 bg-[#F8F8F8] border border-[#EDEDED] rounded-2xl p-4">
        <div class="w-12 h-12 rounded-2xl bg-[#1C1C1C] flex items-center justify-center">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
        </div>
        <div class="text-[13px] font-bold text-[#1C1C1C]">Gallery</div>
        <div class="text-[11px] text-[#606060]">Upload from phone</div>
      </button>
    </div>
  </div>
  <script>
  function openScanOptions(){document.getElementById('scanOptBd').classList.remove('hidden');document.getElementById('scanOptPanel').classList.remove('hidden');}
  function closeScanOptions(){document.getElementById('scanOptBd').classList.add('hidden');document.getElementById('scanOptPanel').classList.add('hidden');}
  </script>
'''
s = s.replace('  <script>if("serviceWorker"in navigator)', scan_sheet + '  <script>if("serviceWorker"in navigator)')
print('  2b. Scan options sheet added')

with open(os.path.join(BASE, 'scanner.html'), 'w', encoding='utf-8') as f:
    f.write(s)
print('  -> scanner.html saved')

# ============================================================
# 3. profit-calculator.html
# ============================================================
print('\n[profit-calculator.html]')
with open(os.path.join(BASE, 'profit-calculator.html'), 'r', encoding='utf-8') as f:
    p = f.read()

# 3a. Remove ! button from header
p = p.replace(
    '        <button class="w-9 h-9 rounded-full border border-[#EDEDED] flex items-center justify-center">\n          <svg width="17" height="17" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="#1C1C1C" stroke-width="2"/><path d="M12 8v4M12 16h.01" stroke="#1C1C1C" stroke-width="2" stroke-linecap="round"/></svg>\n        </button>',
    ''
)
print('  3a. ! button removed from profit calc')

# 3b. Make purchase price editable (change static display to input)
p = p.replace(
    '            <div>\n              <div class="text-[12px] font-medium text-[#606060] mb-1">Purchase price / unit</div>\n              <div class="border border-[#EDEDED] rounded-lg px-3 py-2 bg-[#F8F8F8]">\n                <div class="text-[15px] font-semibold text-[#1C1C1C]">&#8377;440</div>\n                <div class="text-[9px] text-[#9E9E9E] font-medium">Auto &middot; from catalog</div>\n              </div>\n            </div>',
    '            <div>\n              <div class="text-[12px] font-medium text-[#606060] mb-1">Purchase price / unit</div>\n              <div class="border border-[#0E7A4E]/35 rounded-lg px-3 py-2 bg-[#F0FDF5]/60 flex items-center justify-between">\n                <div>\n                  <div class="flex items-center gap-0.5"><span class="text-[15px] font-semibold text-[#1C1C1C]">₹</span><input type="number" value="440" class="text-[15px] font-semibold text-[#1C1C1C] outline-none bg-transparent w-14"/></div>\n                  <div class="text-[9px] text-[#0E7A4E] font-medium">Auto-filled · editable</div>\n                </div>\n                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#0E7A4E" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>\n              </div>\n            </div>'
)
print('  3b. Purchase price made editable')

# 3c. Improve "What if you sold" section UI
# Add colored left-border accent + "Best Pick" label on recommended scenario
p = p.replace(
    '        <div class="bg-white border border-[#EDEDED] rounded-2xl p-4">\n          <div class="flex items-center justify-between mb-3">\n            <div class="text-[14px] font-semibold text-[#1C1C1C]">What if you sold at&hellip;</div>\n            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M3 12h18M3 6h18M3 18h18" stroke="#9E9E9E" stroke-width="2" stroke-linecap="round"/></svg>\n          </div>\n          <div class="space-y-2">\n            <div class="flex items-center gap-3 p-2.5 rounded-xl border border-[#EDEDED]">',
    '        <div class="bg-white border border-[#EDEDED] rounded-2xl p-4">\n          <div class="flex items-center justify-between mb-3">\n            <div class="text-[14px] font-bold text-[#1C1C1C]">What if you sold at…</div>\n            <div class="text-[11px] text-[#606060] font-medium">3 scenarios</div>\n          </div>\n          <div class="space-y-2">\n            <div class="flex items-center gap-3 p-2.5 rounded-xl border border-[#EDEDED]" style="border-left:3px solid #D4A537">'
)
# Recommended scenario: add "Best Pick" badge
p = p.replace(
    '            <div class="flex items-center gap-3 p-2.5 rounded-xl border-2 border-[#0E7A4E] bg-[#F5FBF7]">',
    '            <div class="flex items-center gap-3 p-2.5 rounded-xl border-2 border-[#0E7A4E] bg-[#F5FBF7]" style="position:relative">'
)
p = p.replace(
    '              <div class="flex-1 leading-tight">\n                <div class="text-[14px] font-semibold text-[#1C1C1C]">&#8377;590 / unit</div>\n                <div class="text-[12px] text-[#0C831F] font-semibold">Recommended &mdash; balanced</div>',
    '              <div class="flex-1 leading-tight">\n                <div class="flex items-center gap-1.5"><div class="text-[14px] font-semibold text-[#1C1C1C]">₹590 / unit</div><span class="text-[9px] font-bold text-white bg-[#0C831F] px-1.5 py-0.5 rounded-full">Best Pick</span></div>\n                <div class="text-[12px] text-[#0C831F] font-semibold">Recommended — balanced</div>'
)
# Premium scenario: add blue border
p = p.replace(
    '            <div class="flex items-center gap-3 p-2.5 rounded-xl border border-[#EDEDED]">\n              <div class="w-8 h-8 rounded-full bg-[#FFF8E6] border border-[#D4A537]/40 flex items-center justify-center">\n                <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 19V5M5 12l7-7 7 7"',
    '            <div class="flex items-center gap-3 p-2.5 rounded-xl border border-[#EDEDED]" style="border-left:3px solid #0E7A4E">\n              <div class="w-8 h-8 rounded-full bg-[#FFF8E6] border border-[#D4A537]/40 flex items-center justify-center">\n                <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 19V5M5 12l7-7 7 7"'
)
print('  3c. What-if section improved')

with open(os.path.join(BASE, 'profit-calculator.html'), 'w', encoding='utf-8') as f:
    f.write(p)
print('  -> profit-calculator.html saved')

# ============================================================
# 4. ai-chatbot.html — rename AI to Katyaa + add attachment
# ============================================================
print('\n[ai-chatbot.html]')
with open(os.path.join(BASE, 'ai-chatbot.html'), 'r', encoding='utf-8') as f:
    a = f.read()

# 4a. Rename page title
a = a.replace('<title>Krishi AI Chat</title>', '<title>Katyaa AI · Katyayani</title>')

# 4b. Update header: title + subtitle
a = a.replace(
    '          <div class="brand-font text-[18px] text-[#1C1C1C]">Krishi AI Chat</div>\n          <div class="text-[12px] text-[#606060] flex items-center gap-1">\n            <span class="w-1.5 h-1.5 rounded-full bg-[#0C831F]"></span>\n            Your farming expert 24×7\n          </div>',
    '          <div class="brand-font text-[18px] text-[#1C1C1C]">Katyaa <span class="text-[12px] font-normal text-[#606060]">by Katyayani</span></div>\n          <div class="text-[12px] text-[#606060] flex items-center gap-1">\n            <span class="w-1.5 h-1.5 rounded-full bg-[#0C831F]"></span>\n            Farming AI · Available 24×7\n          </div>'
)
print('  4b. AI name updated to Katyaa')

# 4c. Update AI greeting message
a = a.replace(
    'Namaste Maheshwari ji. Main Krishi AI hoon, aapka farming expert. Kya problem hai aaj?',
    'Namaste Maheshwari ji! Main Katyaa hoon — Katyayani ka AI farming expert. Kya problem hai aaj? 🌱'
)
print('  4c. AI greeting updated')

# 4d. Add attachment button to input bar (before mic)
a = a.replace(
    '      <!-- Input bar -->\n      <div class="px-3 pb-3 flex items-center gap-2">\n        <button class="w-10 h-10 rounded-full border border-[#EDEDED] flex items-center justify-center flex-shrink-0">',
    '      <!-- Input bar -->\n      <div class="px-3 pb-3 flex items-center gap-2">\n        <button class="w-10 h-10 rounded-full border border-[#EDEDED] flex items-center justify-center flex-shrink-0" onclick="document.getElementById(\'attachPicker\').click()" title="Attach photo/file">\n          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1C1C1C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48"/></svg>\n        </button>\n        <input type="file" id="attachPicker" accept="image/*,.pdf" class="hidden"/>\n        <button class="w-10 h-10 rounded-full border border-[#EDEDED] flex items-center justify-center flex-shrink-0">'
)
print('  4d. Attachment button added')

with open(os.path.join(BASE, 'ai-chatbot.html'), 'w', encoding='utf-8') as f:
    f.write(a)
print('  -> ai-chatbot.html saved')

# ============================================================
# 5. voice-order.html — remove ! button
# ============================================================
print('\n[voice-order.html]')
with open(os.path.join(BASE, 'voice-order.html'), 'r', encoding='utf-8') as f:
    v = f.read()

v = v.replace(
    '        <button class="w-9 h-9 rounded-full border border-[#EDEDED] flex items-center justify-center">\n          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#1C1C1C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/></svg>\n        </button>',
    ''
)
print('  5. ! button removed from voice-order')

with open(os.path.join(BASE, 'voice-order.html'), 'w', encoding='utf-8') as f:
    f.write(v)
print('  -> voice-order.html saved')

print('\nAll done.')
