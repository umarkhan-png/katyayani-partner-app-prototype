with open('screens/poster-generator.html', encoding='utf-8') as f:
    p = f.read()

# ==================== ITEM 14: Rich festival template thumbnails ====================

# Diwali thumbnail — add diya icon + warm glow layers
p = p.replace(
    '<button data-tmpl="diwali" class="tmpl-btn w-[90px] flex-shrink-0 rounded-xl overflow-hidden border-2 border-[#1C1C1C]" aria-pressed="true">\n              <div class="h-[100px] tmpl-diwali relative flex items-center justify-center">\n                <div class="text-[9px] font-bold text-[#FFE08A] serif italic">Diwali</div></div>\n              <div class="text-[9px] font-semibold py-1 text-center bg-white">Diwali Dhamaka</div>\n            </button>',
    '<button data-tmpl="diwali" class="tmpl-btn w-[90px] flex-shrink-0 rounded-xl overflow-hidden border-2 border-[#1C1C1C]" aria-pressed="true">\n              <div class="h-[100px] tmpl-diwali relative overflow-hidden">\n                <div class="absolute inset-0 flex flex-col items-center justify-center">\n                  <div class="text-[32px] leading-none mb-0.5">🪔</div>\n                  <div class="text-[8px] font-black text-[#FFE08A] serif tracking-wider">DIWALI</div>\n                  <div class="text-[6px] text-[#FFD96B]/80 font-semibold mt-0.5">DHAMAKA</div>\n                </div>\n                <div class="absolute top-2 left-2 text-[10px]">✨</div>\n                <div class="absolute top-2 right-2 text-[10px]">✨</div>\n                <div class="absolute bottom-8 left-3 text-[10px]">🌸</div>\n                <div class="absolute bottom-8 right-3 text-[10px]">🌸</div>\n              </div>\n              <div class="text-[9px] font-semibold py-1 text-center bg-white">Diwali Dhamaka</div>\n            </button>'
)

# Holi thumbnail — add color splashes
p = p.replace(
    '<button data-tmpl="holi" class="tmpl-btn w-[90px] flex-shrink-0 rounded-xl overflow-hidden border border-[#E8E8E8]">\n              <div class="h-[100px] tmpl-holi flex items-center justify-center"><div class="text-[9px] font-bold text-white serif">Holi</div></div>\n              <div class="text-[9px] font-semibold py-1 text-center bg-white">Holi Special</div>\n            </button>',
    '<button data-tmpl="holi" class="tmpl-btn w-[90px] flex-shrink-0 rounded-xl overflow-hidden border border-[#E8E8E8]">\n              <div class="h-[100px] tmpl-holi relative overflow-hidden">\n                <div class="absolute inset-0 flex flex-col items-center justify-center">\n                  <div class="text-[28px] leading-none mb-0.5">🎨</div>\n                  <div class="text-[8px] font-black text-white serif tracking-wider" style="text-shadow:0 1px 4px rgba(0,0,0,.4)">HOLI HAI!</div>\n                </div>\n                <div class="absolute top-1 left-1 w-8 h-8 rounded-full opacity-60" style="background:#FF6B9D"></div>\n                <div class="absolute top-3 right-0 w-10 h-10 rounded-full opacity-50" style="background:#FFD93D"></div>\n                <div class="absolute bottom-5 left-0 w-8 h-8 rounded-full opacity-60" style="background:#6BCB77"></div>\n                <div class="absolute bottom-3 right-2 w-7 h-7 rounded-full opacity-50" style="background:#4D96FF"></div>\n              </div>\n              <div class="text-[9px] font-semibold py-1 text-center bg-white">Holi Special</div>\n            </button>'
)

# New Year thumbnail
p = p.replace(
    '<button data-tmpl="newyear" class="tmpl-btn w-[90px] flex-shrink-0 rounded-xl overflow-hidden border border-[#E8E8E8]">\n              <div class="h-[100px] flex items-center justify-center" style="background:linear-gradient(135deg,#1a1a1a,#D4A537)"><div class="text-[9px] font-bold text-[#D4A537] serif">2026</div></div>\n              <div class="text-[9px] font-semibold py-1 text-center bg-white">New Year</div>\n            </button>',
    '<button data-tmpl="newyear" class="tmpl-btn w-[90px] flex-shrink-0 rounded-xl overflow-hidden border border-[#E8E8E8]">\n              <div class="h-[100px] relative overflow-hidden" style="background:linear-gradient(135deg,#0d0d1a,#1a1a4e,#D4A537)">\n                <div class="absolute inset-0 flex flex-col items-center justify-center">\n                  <div class="text-[20px] leading-none">🎆</div>\n                  <div class="text-[14px] font-black text-[#FFD96B] leading-none mt-0.5">2026</div>\n                  <div class="text-[6px] text-[#D4A537]/80 font-bold tracking-widest mt-0.5">HAPPY NEW YEAR</div>\n                </div>\n                <div class="absolute top-1 left-2 text-[8px]">⭐</div>\n                <div class="absolute top-2 right-3 text-[8px]">✨</div>\n                <div class="absolute bottom-6 left-1 text-[10px]">🎇</div>\n                <div class="absolute bottom-5 right-2 text-[8px]">⭐</div>\n              </div>\n              <div class="text-[9px] font-semibold py-1 text-center bg-white">New Year</div>\n            </button>'
)

# Republic Day thumbnail
p = p.replace(
    '<button data-tmpl="republic" class="tmpl-btn w-[90px] flex-shrink-0 rounded-xl overflow-hidden border border-[#E8E8E8]">\n              <div class="h-[100px] flex items-center justify-center" style="background:linear-gradient(180deg,#FF9933,#FFFFFF,#138808)"><div class="text-[9px] font-bold text-[#1C1C1C] serif">26 Jan</div></div>\n              <div class="text-[9px] font-semibold py-1 text-center bg-white">Republic Day</div>\n            </button>',
    '<button data-tmpl="republic" class="tmpl-btn w-[90px] flex-shrink-0 rounded-xl overflow-hidden border border-[#E8E8E8]">\n              <div class="h-[100px] relative overflow-hidden">\n                <div class="absolute inset-0" style="background:linear-gradient(180deg,#FF9933 33%,#FFFFFF 33%,#FFFFFF 66%,#138808 66%)"></div>\n                <div class="absolute inset-0 flex flex-col items-center justify-center">\n                  <div class="text-[22px] leading-none">🇮🇳</div>\n                  <div class="text-[7px] font-black text-[#000080] mt-1 bg-white/70 px-1.5 py-0.5 rounded">26 JAN</div>\n                </div>\n              </div>\n              <div class="text-[9px] font-semibold py-1 text-center bg-white">Republic Day</div>\n            </button>'
)

# Eid thumbnail
p = p.replace(
    '<button data-tmpl="holi2" class="tmpl-btn w-[90px] flex-shrink-0 rounded-xl overflow-hidden border border-[#E8E8E8]">\n              <div class="h-[100px] flex items-center justify-center" style="background:linear-gradient(135deg,#E23744,#FFB800)"><div class="text-[9px] font-bold text-white serif">Eid</div></div>\n              <div class="text-[9px] font-semibold py-1 text-center bg-white">Eid Mubarak</div>\n            </button>',
    '<button data-tmpl="holi2" class="tmpl-btn w-[90px] flex-shrink-0 rounded-xl overflow-hidden border border-[#E8E8E8]">\n              <div class="h-[100px] relative overflow-hidden" style="background:linear-gradient(160deg,#0f2027,#1a4a2e,#2d7a4e)">\n                <div class="absolute inset-0 flex flex-col items-center justify-center">\n                  <div class="text-[28px] leading-none">🌙</div>\n                  <div class="text-[8px] font-black text-[#D4A537] mt-0.5 tracking-wider">EID MUBARAK</div>\n                  <div class="text-[5px] text-white/60 font-medium mt-0.5">عيد مبارك</div>\n                </div>\n                <div class="absolute top-2 right-4 text-[10px]">⭐</div>\n                <div class="absolute top-5 left-2 text-[8px]">✨</div>\n              </div>\n              <div class="text-[9px] font-semibold py-1 text-center bg-white">Eid Mubarak</div>\n            </button>'
)
print('14. Template thumbnails done')

# ==================== ITEM 15: Katyayani logo + "Created with Partner App" ====================

# Add watermark to FESTIVAL poster canvas (above footer, below offer pill)
p = p.replace(
    '            <!-- Footer contact -->\n            <div class="absolute bottom-4 left-0 right-0 px-5">',
    '            <!-- Katyayani watermark -->\n            <div class="absolute bottom-[52px] left-0 right-0 flex items-center justify-center gap-1">\n              <div class="w-3 h-3 rounded-full bg-[#0E7A4E] flex items-center justify-center" style="flex-shrink:0"><span class="text-[5px] font-black text-white">K</span></div>\n              <span class="text-[7px] text-white/50 font-medium">Created with Katyayani Partner App</span>\n            </div>\n            <!-- Footer contact -->\n            <div class="absolute bottom-4 left-0 right-0 px-5">'
)

# Add watermark to PRODUCT poster canvas
p = p.replace(
    '            <!-- Footer -->\n            <div class="absolute bottom-4 left-0 right-0 px-5">',
    '            <!-- Katyayani watermark -->\n            <div class="absolute bottom-[52px] left-0 right-0 flex items-center justify-center gap-1">\n              <div class="w-3 h-3 rounded-full bg-[#D4A537] flex items-center justify-center" style="flex-shrink:0"><span class="text-[5px] font-black text-[#1C1C1C]">K</span></div>\n              <span class="text-[7px] text-white/50 font-medium">Created with Katyayani Partner App</span>\n            </div>\n            <!-- Footer -->\n            <div class="absolute bottom-4 left-0 right-0 px-5">'
)
print('15. Katyayani watermark done')

# ==================== ITEM 16: Fix product poster text/image overlap ====================

# Product image: reduce height and push up slightly so text area below is clear
p = p.replace(
    '            <!-- Product image -->\n            <div class="absolute top-[18%] left-0 right-0 flex items-center justify-center" style="height:50%">\n              <img src="https://katyayanikrishidirect.com/cdn/shop/files/IMIDA_4.webp" class="h-full object-contain drop-shadow-2xl">',
    '            <!-- Product image -->\n            <div class="absolute top-[15%] left-0 right-0 flex items-center justify-center" style="height:42%">\n              <img src="https://katyayanikrishidirect.com/cdn/shop/files/IMIDA_4.webp" class="h-full object-contain drop-shadow-2xl">'
)

# Product name area: add frosted background + move down so no overlap
p = p.replace(
    '            <!-- Product name -->\n            <div class="absolute top-[66%] left-0 right-0 text-center px-5">\n              <div class="text-[9px] font-semibold text-[#D4A537] uppercase tracking-[2px]">Featured</div>\n              <div class="serif text-[24px] text-white font-black leading-none mt-1">Imida 30.5% SC</div>\n              <div class="text-[9px] text-white/70 mt-1">Safe • Effective • Certified</div>\n            </div>',
    '            <!-- Product name -->\n            <div class="absolute left-0 right-0 px-4" style="top:58%;bottom:44px;display:flex;flex-direction:column;justify-content:center;background:linear-gradient(to bottom,transparent,rgba(8,61,40,0.92) 30%)">\n              <div class="text-[9px] font-semibold text-[#D4A537] uppercase tracking-[2px]">Featured Product</div>\n              <div class="serif text-[22px] text-white font-black leading-tight mt-0.5">Imida 30.5% SC</div>\n              <div class="text-[9px] text-white/70 mt-0.5">Safe · Effective · Certified</div>\n            </div>'
)

# Price row: move it to be inside the dark band above footer
p = p.replace(
    '            <!-- Price / offer -->\n            <div class="absolute bottom-16 left-0 right-0 flex items-center justify-center gap-2">\n              <div class="text-[22px] font-black text-[#D4A537]">₹280</div>\n              <div class="text-[13px] font-semibold text-white/60 line-through">₹400</div>\n              <div class="bg-[#E23744] text-white text-[9px] font-bold px-2 py-0.5 rounded">30% OFF</div>\n            </div>',
    '            <!-- Price / offer -->\n            <div class="absolute left-4 right-4 flex items-center gap-2" style="bottom:44px">\n              <div class="text-[20px] font-black text-[#D4A537]">&#8377;280</div>\n              <div class="text-[12px] font-semibold text-white/50 line-through">&#8377;400</div>\n              <div class="bg-[#E23744] text-white text-[8px] font-bold px-1.5 py-0.5 rounded">30% OFF</div>\n            </div>'
)
print('16. Product poster layout fixed')

with open('screens/poster-generator.html', 'w', encoding='utf-8') as f:
    f.write(p)
print('\nposter-generator.html done.')
