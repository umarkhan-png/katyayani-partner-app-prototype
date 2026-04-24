import re, shutil, os

home_path = r'C:\Users\ASUS\katyayani-partner-app\screens\home.html'

with open(home_path, 'r', encoding='utf-8') as f:
    h = f.read()

# 1. Story ring: lighter gradient + reduce stroke p-[2.5px]->p-[2px]
old_story = 'class="w-[62px] h-[62px] rounded-full p-[2.5px]" style="background:linear-gradient(135deg,#042919 0%,#0E7A4E 100%)"'
new_story = 'class="w-[62px] h-[62px] rounded-full p-[2px]" style="background:linear-gradient(135deg,#D4A537 0%,#22C55E 50%,#0E7A4E 100%)"'
c = h.count(old_story)
h = h.replace(old_story, new_story)
print(f'1. Story rings: {c} replaced')

# 2a. Remove bg-white from top-selling image containers
h = h.replace('h-[50px] bg-white rounded-lg', 'h-[50px] rounded-lg')
print('2a. Removed bg-white from shelf images')

# 2b. Remove number badge divs
badges = [
    '\n            <div class="text-[8.5px] font-bold px-1.5 py-0.5 rounded" style="background:linear-gradient(135deg,#D4A537,#FFE08A);color:#1C1C1C">#1</div>',
    '\n            <div class="text-[8.5px] font-bold px-1.5 py-0.5 rounded" style="background:linear-gradient(135deg,#D4A537,#FFE08A);color:#1C1C1C">#2</div>',
    '\n            <div class="text-[8.5px] font-bold px-1.5 py-0.5 rounded" style="background:rgba(212,165,55,0.35);color:#FFE08A">#3</div>',
    '\n            <div class="text-[8.5px] font-medium px-1.5 py-0.5 rounded" style="background:rgba(255,255,255,0.15);color:rgba(255,255,255,0.7)">#4</div>',
    '\n            <div class="text-[8.5px] font-medium px-1.5 py-0.5 rounded" style="background:rgba(255,255,255,0.15);color:rgba(255,255,255,0.7)">#5</div>',
    '\n            <div class="text-[8.5px] font-medium px-1.5 py-0.5 rounded" style="background:rgba(255,255,255,0.15);color:rgba(255,255,255,0.7)">#6</div>',
    '\n            <div class="text-[8.5px] font-medium px-1.5 py-0.5 rounded" style="background:rgba(255,255,255,0.15);color:rgba(255,255,255,0.7)">#7</div>',
    '\n            <div class="text-[8.5px] font-medium px-1.5 py-0.5 rounded" style="background:rgba(255,255,255,0.15);color:rgba(255,255,255,0.7)">#8</div>',
]
removed = 0
for b in badges:
    if b in h:
        h = h.replace(b, '')
        removed += 1
print(f'2b. Removed {removed}/8 number badges')

# 2c. Replace 47+ More tile with Antivirus (9th product)
old_47 = '''          <a href="categories.html" class="rounded-xl p-1.5 flex flex-col items-center justify-center gap-1.5" style="background:rgba(212,165,55,0.15);border:1px solid rgba(212,165,55,0.35);min-height:100px">
            <div class="w-9 h-9 rounded-full flex items-center justify-center" style="background:rgba(212,165,55,0.25)">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FFE08A" stroke-width="2.5" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
            </div>
            <div class="text-[9.5px] font-bold text-[#FFE08A] text-center leading-tight">47+ More</div>
            <div class="text-[7.5px] text-center" style="color:rgba(255,255,255,0.5)">View All</div>
          </a>'''
new_antivirus = '''          <a href="pdp.html" class="rounded-xl p-1.5 flex flex-col items-center gap-1" style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15)">
            <div class="w-full h-[50px] rounded-lg flex items-center justify-center overflow-hidden p-1"><img src="https://katyayanikrishidirect.com/cdn/shop/files/AntiVirus_75248f94-8de8-47c9-9592-a7aa49e36eeb.webp" class="h-full object-contain"></div>
            <div class="text-[9.5px] font-semibold text-white leading-tight text-center">AntiVirus</div>
            <div class="text-[7.5px] leading-tight text-center" style="color:rgba(255,255,255,0.55)">Viricide</div>
          </a>'''
if old_47 in h:
    h = h.replace(old_47, new_antivirus)
    print('2c. Replaced 47+ tile with Antivirus')
else:
    print('2c. MISS: 47+ tile')

# 3a. Remove My Crops info line
old_info = '''            <div class="flex items-center gap-1 mt-0.5">
              <svg width="9" height="9" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="rgba(255,255,255,0.55)" stroke-width="2.2"/><path d="M12 8v4M12 16h.01" stroke="rgba(255,255,255,0.55)" stroke-width="2.5" stroke-linecap="round"/></svg>
              <span class="text-[9px]" style="color:rgba(255,255,255,0.65)">Sirf is section ke products change honge</span>
            </div>'''
if old_info in h:
    h = h.replace(old_info, '')
    print('3a. Removed My Crops info line')
else:
    print('3a. MISS: info line')

# 3b. Remove empty state icon
old_icon = '''            <div class="w-14 h-14 mx-auto rounded-2xl flex items-center justify-center mb-3" style="background:rgba(14,122,78,0.1)">
              <span class="text-[28px] leading-none">🌱</span>
            </div>'''
if old_icon in h:
    h = h.replace(old_icon, '')
    print('3b. Removed empty state icon')
else:
    print('3b. MISS: empty state icon')

# 3c. py-6 -> py-4 in cropEmptyState
h = h.replace('id="cropEmptyState" class="px-4 py-6 text-center"', 'id="cropEmptyState" class="px-4 py-4 text-center"')
print('3c. Compacted cropEmptyState padding')

# 4. Update footer image reference
h = h.replace('../assets/footer-brand.png', '../assets/footer-kisankapartner.png')
print('4. Updated footer image reference')

# 5. Move search separator from before-mic to between-mic-and-camera
old_sep = '''          <div class="w-px h-5 bg-[#D4D5D9] flex-shrink-0"></div>
          <button class="flex items-center justify-center pl-3 py-3 flex-shrink-0">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1C1C1C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 00-3 3v7a3 3 0 006 0V5a3 3 0 00-3-3zM19 10v2a7 7 0 01-14 0v-2M12 19v3"/></svg>
          </button>
          <button onclick="openHomeImgSearch()" class="flex items-center justify-center px-3 py-3 flex-shrink-0">'''
new_sep = '''          <button class="flex items-center justify-center pl-3 py-3 flex-shrink-0">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1C1C1C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 00-3 3v7a3 3 0 006 0V5a3 3 0 00-3-3zM19 10v2a7 7 0 01-14 0v-2M12 19v3"/></svg>
          </button>
          <div class="w-px h-5 bg-[#D4D5D9] flex-shrink-0"></div>
          <button onclick="openHomeImgSearch()" class="flex items-center justify-center px-3 py-3 flex-shrink-0">'''
if old_sep in h:
    h = h.replace(old_sep, new_sep)
    print('5. Moved search separator')
else:
    print('5. MISS: search separator')

# 9. Add Krishi AI icon to hero header (before coin)
old_hero = '''          <div class="flex items-center gap-2 flex-shrink-0">
            <!-- Premium coin tile -->'''
new_hero = '''          <div class="flex items-center gap-2 flex-shrink-0">
            <!-- Krishi AI -->
            <a href="ai-chatbot.html" class="relative w-10 h-10 rounded-xl flex items-center justify-center" style="background:linear-gradient(145deg,rgba(255,255,255,.18),rgba(255,255,255,.04));backdrop-filter:blur(10px);border:1px solid rgba(212,165,55,.45);box-shadow:0 6px 18px -4px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.2)">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#7ED3A8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
              <span class="absolute -top-0.5 -right-0.5 w-3.5 h-3.5 rounded-full flex items-center justify-center" style="background:linear-gradient(135deg,#D4A537,#FFE08A);border:1px solid #083D28">
                <svg width="7" height="7" viewBox="0 0 24 24" fill="#1C1C1C"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
              </span>
            </a>
            <!-- Premium coin tile -->'''
if old_hero in h:
    h = h.replace(old_hero, new_hero)
    print('9. Added Krishi AI icon')
else:
    print('9. MISS: hero icons')

with open(home_path, 'w', encoding='utf-8') as f:
    f.write(h)
print('\nhome.html done.')

# Copy footer image
src = r'C:\Users\ASUS\Downloads\ChatGPT Image Apr 23, 2026, 07_46_43 PM.png'
dst = r'C:\Users\ASUS\katyayani-partner-app\assets\footer-kisankapartner.png'
if os.path.exists(src):
    shutil.copy(src, dst)
    print('Footer image copied.')
else:
    print('WARNING: footer image not found at', src)
