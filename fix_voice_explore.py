import re

# === VOICE-ORDER.HTML ===
voice_path = r'C:\Users\ASUS\katyayani-partner-app\screens\voice-order.html'
with open(voice_path, 'r', encoding='utf-8') as f:
    v = f.read()

v = v.replace(
    '<div class="brand-font text-[14px] text-[#1C1C1C]">Parsed items</div>',
    '<div class="brand-font text-[14px] text-[#1C1C1C]">Items Found</div>'
)
v = v.replace(
    '&#10003; OCR complete &middot; 4 items parsed',
    '&#10003; OCR complete &middot; 4 items found'
)
v = v.replace(
    '✓ OCR complete · 4 items parsed',
    '✓ OCR complete · 4 items found'
)
v = v.replace('4 items parsed', '4 items found')
v = v.replace(
    '<div class="brand-font text-[14px] text-[#1C1C1C]">Parsed from photo</div>',
    '<div class="brand-font text-[14px] text-[#1C1C1C]">Items from photo</div>'
)

with open(voice_path, 'w', encoding='utf-8') as f:
    f.write(v)
print('voice-order.html done.')

# === EXPLORE.HTML ===
explore_path = r'C:\Users\ASUS\katyayani-partner-app\screens\explore.html'
with open(explore_path, 'r', encoding='utf-8') as f:
    e = f.read()

# grid-cols-2 -> grid-cols-3, gap-2.5 -> gap-2
e = e.replace('grid grid-cols-2 gap-2.5', 'grid grid-cols-3 gap-2')

# tile padding p-3 -> p-2.5 (only in card tiles, not p-3.5 grow items)
e = e.replace('rounded-2xl p-3 border border-[#EDEDED]"', 'rounded-2xl p-2.5 border border-[#EDEDED]"')
e = e.replace("rounded-2xl p-3 border border-[#EDEDED] relative\"", "rounded-2xl p-2.5 border border-[#EDEDED] relative\"")

# icon container: w-10 h-10 -> w-8 h-8 (grow section uses w-11 h-11, safe)
e = e.replace('w-10 h-10 rounded-xl', 'w-8 h-8 rounded-xl')

# SVG icon size: 20 -> 16 (grow section uses 22, safe)
e = re.sub(r'(<svg) width="20" height="20"', r'\1 width="16" height="16"', e)

# tile title: text-[13px] -> text-[11px], mt-2.5 -> mt-1.5 (grow uses text-[14px], safe)
e = e.replace('text-[13px] font-semibold text-[#1C1C1C] mt-2.5', 'text-[11px] font-semibold text-[#1C1C1C] mt-1.5')

with open(explore_path, 'w', encoding='utf-8') as f:
    f.write(e)
print('explore.html done.')
