with open('screens/home.html', 'r', encoding='utf-8') as f:
    h = f.read()

markers = [
    '      <!-- Flash Deals rail -->',
    '      <!-- ============== RECENTLY VIEWED ============== -->',
    '      <!-- ============== MY STORE — 2x2 grid + VIP banner ============== -->',
    '      <!-- ============== TOP SELLING PRODUCTS — 3x3 shelf ============== -->',
    '      <!-- ============== BEST IN YOUR STATE (social proof) ============== -->',
    '      <!-- ============== MY CROPS (Shop by Crop) ============== -->',
    '      <!-- ============== RABI SEASON BESTSELLERS ============== -->',
    '      <!-- ============== RECOMMENDED FOR YOUR AREA ============== -->',
    '      <!-- Live activity strip -->',
    '      <!-- New Launches rail -->',
    '      <!-- CLOSER FOOTER -->',
    '      <div class="h-4"></div>',
]

positions = []
for m in markers:
    pos = h.find(m)
    if pos == -1:
        print(f'NOT FOUND: {repr(m)}')
        exit(1)
    positions.append(pos)
    print(f'Found: {m[:50]}... at {pos}')

names = ['flash_deals','recently_viewed','my_store','top_selling',
         'best_in_state','my_crops','rabi_season','recommended',
         'live_activity','new_launches','footer']

sections = {}
for i, name in enumerate(names):
    sections[name] = h[positions[i]:positions[i+1]]

before = h[:positions[0]]
after  = h[positions[-1]:]

new_order = [
    'flash_deals',
    'recently_viewed',
    'rabi_season',
    'my_crops',
    'top_selling',
    'my_store',
    'best_in_state',
    'recommended',
    'live_activity',
    'new_launches',
    'footer',
]

new_h = before + ''.join(sections[s] for s in new_order) + after

with open('screens/home.html', 'w', encoding='utf-8') as f:
    f.write(new_h)

print('Done! Sections reordered.')
