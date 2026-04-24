import re

with open('screens/home.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Match each shelf tile's: white image box + product name + tech name
# and wrap all three in a single white card, with dark text
pattern = (
    r'<div class="w-full h-\[50px\] bg-white rounded-lg flex items-center justify-center overflow-hidden p-1">'
    r'<img src="([^"]+)" class="h-full object-contain"></div>\n'
    r'            <div class="text-\[9\.5px\] font-semibold text-white leading-tight text-center">([^<]+)</div>\n'
    r'            <div class="text-\[7\.5px\] leading-tight text-center" style="color:rgba\(255,255,255,0\.55\)">([^<]+)</div>'
)

def replacer(m):
    src   = m.group(1)
    name  = m.group(2)
    tech  = m.group(3)
    return (
        '<div class="w-full bg-white rounded-lg overflow-hidden">\n'
        '              <div class="h-[50px] flex items-center justify-center p-1">'
        '<img src="' + src + '" class="h-full object-contain"></div>\n'
        '              <div class="text-[9px] font-semibold text-[#1C1C1C] leading-tight text-center px-1 pt-1 pb-0.5">' + name + '</div>\n'
        '              <div class="text-[7.5px] leading-tight text-center px-1 pb-1.5" style="color:#888">' + tech + '</div>\n'
        '            </div>'
    )

new_h, count = re.subn(pattern, replacer, h)
print(f'Replaced {count} tiles')

with open('screens/home.html', 'w', encoding='utf-8') as f:
    f.write(new_h)
