import glob

# Inline JS that runs after DOM ready — forces full-screen on phones (<768px)
# Uses inline styles which override ALL CSS regardless of specificity
MOBILE_JS = (
  '<script>'
  '(function(){'
  'if(window.innerWidth>=768)return;'
  'document.body.style.cssText="background:#fff;margin:0;padding:0;overflow:hidden";'
  'var d=document.querySelector(".device");'
  'if(d)d.style.cssText="width:100vw;height:100vh;margin:0;border-radius:0;'
  'border:none;box-shadow:none;background:#fff;overflow:hidden;position:relative";'
  'var s=document.querySelector(".scroll-area");'
  'if(s)s.style.height="100vh";'
  '})();'
  '</script>'
)

files = glob.glob('screens/*.html')
updated = 0
for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        h = f.read()
    if 'innerWidth>=768' in h:
        continue
    if '</body>' not in h:
        continue
    h = h.replace('</body>', MOBILE_JS + '\n</body>', 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(h)
    updated += 1

print(f'Updated {updated} files')
