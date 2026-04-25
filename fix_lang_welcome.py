with open('screens/rapido-welcome.html', encoding='utf-8') as f:
    h = f.read()

# 1. h-[52px] → height:65px inline (52 × 1.25 = 65px, exactly +25%)
#    Also convert <a href> to <div onclick> to intercept click for modal
LANGS = [
    ('English',   'English'),
    ('Hinglish',  'English + Hindi'),
    ('हिन्दी',    'Hindi'),
    ('मराठी',     'Marathi'),
    ('ગુજરાતી',   'Gujarati'),
    ('తెలుగు',    'Telugu'),
    ('தமிழ்',     'Tamil'),
    ('ಕನ್ನಡ',     'Kannada'),
    ('മലയാളം',   'Malayalam'),
    ('বাংলা',     'Bengali'),
]

# Replace the entire langGrid with new tiles
old_grid_start = '    <!-- 10 languages -->\n    <div id="langGrid" class="grid grid-cols-2 gap-2">'
old_grid_end   = '    </div>\n  </div>\n\n</div>'

# Build new grid HTML
tiles_html = '    <!-- 10 languages -->\n    <div id="langGrid" class="grid grid-cols-2 gap-2">\n'
for name, sub in LANGS:
    tiles_html += (
        f'      <div onclick="selectLang(\'{name}\',\'{sub}\')" '
        f'class="lang-tile bg-white border-[1.5px] border-[#EDEDED] rounded-xl px-3.5 flex flex-col justify-center text-left relative cursor-pointer" '
        f'style="height:65px">'
        f'<svg class="absolute top-1/2 -translate-y-1/2 right-3 opacity-30" width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="#1C1C1C" stroke-width="2.5" stroke-linecap="round"/></svg>'
        f'<div style="font-size:17px;font-weight:600;color:#1C1C1C;line-height:1.2">{name}</div>'
        f'<div style="font-size:9px;color:#909090;margin-top:2px">{sub}</div>'
        f'</div>\n'
    )
tiles_html += '    </div>\n  </div>\n\n'

h = h.replace(
    old_grid_start + '\n' + ''.join([
        f'      <a href="rapido-phone.html" class="lang-tile h-[52px] bg-white border-[1.5px] border-[#EDEDED] rounded-xl px-3.5 flex flex-col justify-center text-left relative block">\n'
        f'        <svg class="absolute top-1/2 -translate-y-1/2 right-3 opacity-30" width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="#1C1C1C" stroke-width="2.5" stroke-linecap="round"/></svg>\n'
        for _ in LANGS  # just build the anchor to find the section
    ]),
    tiles_html + '</div>',
    1
)

# Simpler approach: just replace the full grid block using known delimiters
import re
h = re.sub(
    r'    <!-- 10 languages -->.*?</div>\n  </div>\n\n</div>',
    tiles_html + '</div>',
    h, flags=re.DOTALL, count=1
)

print('1. tiles replaced:', h.count('height:65px'), 'tiles at 65px')

# 2. Add confirmation modal + JS before service worker
modal = """
  <!-- Language confirm modal -->
  <div id="lmBd" class="hidden absolute inset-0 z-50" style="background:rgba(0,0,0,0.45)"></div>
  <div id="lmPanel" class="hidden absolute left-0 right-0 bottom-0 z-50 bg-white" style="border-radius:24px 24px 0 0;padding:16px 20px 32px;box-shadow:0 -8px 32px rgba(0,0,0,0.18)">
    <!-- drag handle -->
    <div style="width:40px;height:4px;border-radius:2px;background:#E0E0E0;margin:0 auto 20px"></div>
    <!-- language display -->
    <div style="text-align:center;margin-bottom:20px">
      <div style="font-size:11px;font-weight:600;color:#909090;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px">App language set to</div>
      <div id="lmName" style="font-size:28px;font-weight:800;color:#1C1C1C;line-height:1.1"></div>
      <div id="lmSub"  style="font-size:13px;color:#909090;margin-top:4px"></div>
    </div>
    <!-- CTA -->
    <a id="lmCta" href="rapido-phone.html" style="display:block;width:100%;background:#0C831F;color:#fff;font-size:15px;font-weight:700;text-align:center;padding:16px;border-radius:14px;text-decoration:none;box-sizing:border-box;text-transform:uppercase;letter-spacing:0.5px">Continue</a>
    <button onclick="closeLm()" style="display:block;width:100%;margin-top:10px;background:none;border:none;font-size:13px;color:#909090;font-family:Poppins,sans-serif;cursor:pointer">Change language</button>
  </div>
  <script>
  function selectLang(name, sub) {
    document.getElementById('lmName').textContent = name;
    document.getElementById('lmSub').textContent  = sub;
    if (name) localStorage.setItem('kk-lang', name);
    document.getElementById('lmBd').classList.remove('hidden');
    document.getElementById('lmPanel').classList.remove('hidden');
  }
  function closeLm() {
    document.getElementById('lmBd').classList.add('hidden');
    document.getElementById('lmPanel').classList.add('hidden');
  }
  </script>
"""

h = h.replace(
    '  <script>if("serviceWorker"in navigator)',
    modal + '\n  <script>if("serviceWorker"in navigator)'
)
print('2. modal added')

with open('screens/rapido-welcome.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('rapido-welcome.html done.')
