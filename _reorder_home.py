"""
One-shot reorder of screens/home.html sections to the requested flow:
  Hero → Flash sale → Best seller → Select crop → Mega Bachat carousel
       → Big colorful cards → Buy again → KKD footer

Sections not in the requested list (Stories, Active Order Tracking, Rabi
Bestsellers, Recently Viewed, Best in MP, Recommended for Area) are wrapped
in HTML comments so they're hidden but recoverable.

Section boundaries are detected via the existing top-level comment markers
already present in the file (e.g. `<!-- ============== STORIES ... -->`).
"""
from pathlib import Path
import re
import sys

HOME = Path(r"C:\Users\ASUS\katyayani-partner-app\screens\home.html")
src = HOME.read_text(encoding="utf-8").splitlines(keepends=True)

# Each entry is (key, line-index-of-the-comment-line). Order = current top→bottom.
# Detected by scanning for known marker lines.
MARKERS = [
    ("stories",       r'<!-- ============== STORIES'),
    ("active_order",  r'<!-- ============== ACTIVE ORDER TRACKING'),
    ("flash_sale",    r'<!-- Flash Deals rail -->'),
    ("rabi",          r'<!-- ============== RABI SEASON BESTSELLERS'),
    ("buy_again",     r'<!-- ============== RECENTLY BOUGHT'),
    ("recently_viewed", r'<!-- ============== RECENTLY VIEWED'),
    ("best_seller",   r'<!-- ============== TOP SELLING PRODUCTS'),
    ("select_crop",   r'<!-- ============== MY CROPS'),
    ("best_state",    r'<!-- ============== BEST IN YOUR STATE'),
    ("recommended",   r'<!-- ============== RECOMMENDED FOR YOUR AREA'),
    ("big_cards",     r'<!-- ============== MY STORE'),
    ("kkd_footer",    r'<!-- CLOSER FOOTER -->'),
]

def find_line(needle):
    for i, line in enumerate(src):
        if needle in line:
            return i
    raise RuntimeError(f"Marker not found: {needle!r}")

starts = []
for key, pat in MARKERS:
    raw = pat.replace(r'\b','')  # simple substring match
    starts.append((key, find_line(raw)))

# Ends: each section ends just before the next section's start
sections = {}
for i, (key, start) in enumerate(starts):
    end = starts[i+1][1] if i+1 < len(starts) else len(src)
    sections[key] = "".join(src[start:end])

# The "kkd_footer" runs through the bottom of the scroll-area. To keep its
# downstream wrappers (h-4 spacer + scroll-area close + FAB + bottom nav)
# intact, we treat everything from CLOSER FOOTER to end-of-file as a single
# trailing block.
trailing_start = starts[-1][1]
trailing = "".join(src[trailing_start:])
# Pull just the visible "footer image div" out of trailing so we can keep
# the spacer + scroll-area-close + FAB in their original position.
footer_match = re.search(r'(\s*<!-- CLOSER FOOTER -->.*?</div>\s*\n)', trailing, flags=re.DOTALL)
if not footer_match:
    sys.exit("Could not isolate CLOSER FOOTER block")
kkd_footer_html = footer_match.group(1)
trailing_after_footer = trailing[footer_match.end():]

# Build a placeholder Mega Krishi Bachat Mela carousel section
mega_carousel = '''
      <!-- ============== MEGA KRISHI BACHAT MELA (auto-scroll carousel) ============== -->
      <div class="mt-6 mb-2 px-4">
        <h2 class="brand-font text-[20px] text-[#1C1C1C] leading-tight">Mega Krishi Bachat Mela</h2>
        <p class="text-[12px] text-[#606060] mt-0.5">Partner-only offers · Auto-rotates every 4s</p>
      </div>
      <div class="mb-2 relative">
        <div class="overflow-x-auto hide-scrollbar snap-x snap-mandatory scroll-smooth"
             id="megaMelaRail" style="padding:0 16px;scroll-padding-left:16px">
          <div class="flex gap-3" style="padding-right:32px">

            <!-- Slide 1: Mega Krishi Bachat Mela headline -->
            <a href="categories.html" class="snap-start rounded-[14px] overflow-hidden relative h-[150px] flex-shrink-0"
               style="width:calc(100% - 44px);max-width:340px;background:linear-gradient(120deg,#1C1C1C 0%,#2D1810 50%,#1C1C1C 100%)">
              <div class="absolute top-0 right-0 bottom-0 w-[60%]" style="background:radial-gradient(ellipse at right,#D4A537 0%,transparent 70%);opacity:.22"></div>
              <div class="absolute -right-5 top-1/2 -translate-y-1/2 brand-font text-[140px] text-[#D4A537]/10 leading-none italic select-none">%</div>
              <div class="absolute top-4 left-5">
                <div class="text-[10.5px] font-medium text-[#D4A537] uppercase tracking-[2px]">PARTNER EXCLUSIVE</div>
                <div class="brand-font text-[23px] text-white leading-[0.95] mt-1">Mega Krishi</div>
                <div class="brand-font text-[23px] text-[#D4A537] leading-[0.95] italic">Bachat Mela</div>
              </div>
              <div class="absolute bottom-4 left-5 right-5 flex items-end justify-between">
                <div>
                  <div class="text-[10px] text-white/60 font-bold uppercase tracking-wider">Extra Discount</div>
                  <div class="text-[22px] font-black text-white leading-none mt-0.5">₹500 <span class="text-[15px] font-bold text-white/60">OFF</span></div>
                </div>
                <div class="bg-[#D4A537] text-[#1C1C1C] text-[12px] font-semibold uppercase tracking-wider px-3.5 py-2 rounded-full">SHOP NOW →</div>
              </div>
            </a>

            <!-- Slide 2: Buy 1 Get 1 -->
            <a href="categories.html" class="snap-start rounded-[14px] overflow-hidden relative h-[150px] flex-shrink-0"
               style="width:calc(100% - 44px);max-width:340px;background:linear-gradient(135deg,#0E7A4E 0%,#005f3b 70%,#003820 100%)">
              <div class="absolute top-0 right-0 bottom-0 w-[60%]" style="background:radial-gradient(ellipse at right,#D4A537 0%,transparent 70%);opacity:.15"></div>
              <div class="absolute -right-8 top-1/2 -translate-y-1/2 brand-font text-[140px] text-white/5 leading-none italic select-none">1+1</div>
              <div class="absolute top-4 left-5">
                <div class="text-[10.5px] font-medium text-[#D4A537] uppercase tracking-[2px]">HOT DEAL</div>
                <div class="brand-font text-[23px] text-white leading-[0.95] mt-1">Buy 1 Get 1</div>
                <div class="brand-font text-[23px] text-[#D4A537] leading-[0.95] italic">FREE</div>
              </div>
              <div class="absolute bottom-4 left-5 right-5 flex items-end justify-between">
                <div>
                  <div class="text-[10px] text-white/60 font-bold uppercase tracking-wider">On Antivirus Combo</div>
                  <div class="text-[14px] font-semibold text-white mt-0.5">Chilli • Tomato • Brinjal</div>
                </div>
                <div class="bg-[#D4A537] text-[#1C1C1C] text-[12px] font-semibold uppercase tracking-wider px-3.5 py-2 rounded-full">GRAB →</div>
              </div>
            </a>

            <!-- Slide 3: Fertilizer Fest -->
            <a href="categories.html" class="snap-start rounded-[14px] overflow-hidden relative h-[150px] flex-shrink-0"
               style="width:calc(100% - 44px);max-width:340px;background:linear-gradient(120deg,#FFF8E6 0%,#FFF4D6 50%,#F0D55E 100%)">
              <div class="absolute top-0 right-0 bottom-0 w-[60%]" style="background:radial-gradient(ellipse at right,#1C1C1C 0%,transparent 70%);opacity:.08"></div>
              <div class="absolute -right-4 top-1/2 -translate-y-1/2 brand-font text-[140px] text-[#1C1C1C]/10 leading-none select-none">30</div>
              <div class="absolute top-4 left-5">
                <div class="text-[10.5px] font-medium text-[#8B6914] uppercase tracking-[2px]">FERTILIZER FEST</div>
                <div class="brand-font text-[23px] text-[#1C1C1C] leading-[0.95] mt-1">Save Big</div>
                <div class="brand-font text-[23px] text-[#8B6914] leading-[0.95] italic">on NPK</div>
              </div>
              <div class="absolute bottom-4 left-5 right-5 flex items-end justify-between">
                <div>
                  <div class="text-[10px] text-[#8B6914]/80 font-bold uppercase tracking-wider">Up to</div>
                  <div class="text-[22px] font-black text-[#1C1C1C] leading-none mt-0.5">30% <span class="text-[15px] font-bold text-[#8B6914]">OFF</span></div>
                </div>
                <div class="bg-[#1C1C1C] text-[#D4A537] text-[12px] font-semibold uppercase tracking-wider px-3.5 py-2 rounded-full">EXPLORE →</div>
              </div>
            </a>

          </div>
        </div>
        <!-- Pagination dots -->
        <div class="flex justify-center gap-1.5 mt-3" id="megaMelaDots">
          <span class="block w-1.5 h-1.5 rounded-full bg-[#0E7A4E]" data-mm-dot="0"></span>
          <span class="block w-1.5 h-1.5 rounded-full bg-[#D4CCC0]" data-mm-dot="1"></span>
          <span class="block w-1.5 h-1.5 rounded-full bg-[#D4CCC0]" data-mm-dot="2"></span>
        </div>
      </div>
      <script>
      (function(){
        var rail = document.getElementById('megaMelaRail');
        if(!rail) return;
        var dots = document.querySelectorAll('[data-mm-dot]');
        var slides = rail.querySelectorAll('a');
        var idx = 0, paused = false, timer = null;
        function step(){
          if (paused || !slides.length) return;
          idx = (idx + 1) % slides.length;
          slides[idx].scrollIntoView({behavior:'smooth', inline:'start', block:'nearest'});
          dots.forEach(function(d,i){ d.style.background = (i===idx) ? '#0E7A4E' : '#D4CCC0'; });
        }
        function start(){ if(!timer) timer = setInterval(step, 4000); }
        function stop(){ if(timer){ clearInterval(timer); timer = null; } }
        rail.addEventListener('touchstart', function(){ paused = true; stop(); }, {passive:true});
        rail.addEventListener('touchend',   function(){ paused = false; start(); }, {passive:true});
        rail.addEventListener('scroll', function(){
          // Update active dot based on which slide is closest to scroll-left+16
          var x = rail.scrollLeft;
          var closest = 0, best = Infinity;
          slides.forEach(function(s, i){
            var d = Math.abs(s.offsetLeft - 16 - x);
            if (d < best){ best = d; closest = i; }
          });
          idx = closest;
          dots.forEach(function(d,i){ d.style.background = (i===idx) ? '#0E7A4E' : '#D4CCC0'; });
        }, {passive:true});
        start();
      })();
      </script>

'''

# Hide a section by wrapping in a <template> element — its contents are valid
# HTML5 but the browser never renders them. Restore by moving content out of
# the template into the live DOM.
def hide(html, label):
    safe_label = label.replace('"', '&quot;')
    return f'\n      <template data-hidden="{safe_label}">\n{html.rstrip()}\n      </template>\n\n'

# Build the new flow
new_flow = []
new_flow.append(sections["flash_sale"])                  # 1. Flash sale
new_flow.append(sections["best_seller"])                 # 2. Best seller (Top Selling)
new_flow.append(sections["select_crop"])                 # 3. Select crop
new_flow.append(mega_carousel)                           # 4. Mega Krishi Bachat Mela (carousel)
new_flow.append(sections["big_cards"])                   # 5. Big colorful cards (My Store)
new_flow.append(sections["buy_again"])                   # 6. Buy again (Recently Bought)
new_flow.append(kkd_footer_html)                         # 7. KKD logo footer
new_flow.append(hide(sections["stories"], "STORIES Instagram-style"))
new_flow.append(hide(sections["active_order"], "ACTIVE ORDER TRACKING"))
new_flow.append(hide(sections["rabi"], "RABI SEASON BESTSELLERS"))
new_flow.append(hide(sections["recently_viewed"], "RECENTLY VIEWED"))
new_flow.append(hide(sections["best_state"], "BEST IN YOUR STATE"))
new_flow.append(hide(sections["recommended"], "RECOMMENDED FOR YOUR AREA"))

new_block = "".join(new_flow)

# Splice: keep everything up to the first old section start, replace through to
# old footer end, append the un-changed trailing tail.
first_section_start = starts[0][1]  # line of STORIES marker
prefix = "".join(src[:first_section_start])
out = prefix + new_block + trailing_after_footer

HOME.write_text(out, encoding="utf-8")
print(f"OK — wrote {len(out)} chars ({out.count(chr(10))} lines)")
