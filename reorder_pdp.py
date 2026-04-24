with open('screens/pdp.html', 'r', encoding='utf-8') as f:
    h = f.read()

markers = [
    '      <!-- ============== EFFECTIVE ON CROPS',
    '      <!-- ============== CONTROLS THESE PESTS',
    '      <!-- ============== RETAILER TESTIMONIAL VIDEOS',
    '      <!-- ============== FARMER VIDEOS',
    '      <!-- ============== RATINGS & REVIEWS',
]

positions = []
for m in markers:
    pos = h.find(m)
    if pos == -1:
        print(f'NOT FOUND: {repr(m)}'); exit(1)
    positions.append(pos)
    print(f'Found at {pos}: {m[:60]}')

names = ['effective_crops', 'controls_pests', 'retailer_videos', 'farmer_videos']
sections = {}
for i, name in enumerate(names):
    sections[name] = h[positions[i]:positions[i+1]]

before = h[:positions[0]]
after  = h[positions[-1]:]

# New order: retailer → farmer → effective on crops → controls pests → reviews
new_h = before + sections['retailer_videos'] + sections['farmer_videos'] + sections['effective_crops'] + sections['controls_pests'] + after

with open('screens/pdp.html', 'w', encoding='utf-8') as f:
    f.write(new_h)

print('Done!')
