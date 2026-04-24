with open('screens/home.html', 'r', encoding='utf-8') as f:
    h = f.read()

OLD_CARD = '<div class="w-full bg-white rounded-lg overflow-hidden">'
NEW_CARD  = '<div class="w-full bg-white rounded-lg overflow-hidden relative">'

# Replace all 9 occurrences: add relative positioning
h = h.replace(OLD_CARD, NEW_CARD)

# Now inject watermark number into each tile's image row
# Target: the image row inside the white card
OLD_IMG_ROW = '              <div class="h-[50px] flex items-center justify-center p-1">'
# We'll replace sequentially using a counter

count = [0]

def add_number(s, num):
    watermark = (
        f'              <div class="h-[50px] flex items-center justify-center p-1 relative">'
        f'<span class="absolute bottom-0 right-1 text-[26px] font-black italic leading-none select-none pointer-events-none" '
        f'style="color:rgba(14,122,78,0.14)">#{num}</span>'
    )
    return watermark

# Replace each occurrence with numbered version
result = []
idx = 0
num = 1
while True:
    pos = h.find(OLD_IMG_ROW, idx)
    if pos == -1:
        result.append(h[idx:])
        break
    result.append(h[idx:pos])
    result.append(add_number(h, num))
    idx = pos + len(OLD_IMG_ROW)
    num += 1

h = ''.join(result)
print(f'Added watermark numbers to {num-1} tiles')

with open('screens/home.html', 'w', encoding='utf-8') as f:
    f.write(h)
