import glob, re

files = glob.glob('screens/*.html')
updated = 0

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        h = f.read()
    orig = h

    # 1. Add viewport-fit=cover to meta viewport
    h = h.replace(
        'content="width=device-width,initial-scale=1"',
        'content="width=device-width,initial-scale=1,viewport-fit=cover"'
    )

    # 2. Update existing mobile JS to inject safe-area CSS
    OLD_JS = ('if(window.innerWidth>=768)return;'
              'document.body.style.cssText="background:#fff;margin:0;padding:0;overflow:hidden";'
              'var d=document.querySelector(".device");'
              'if(d)d.style.cssText="width:100vw;height:100vh;margin:0;border-radius:0;border:none;box-shadow:none;background:#fff;overflow:hidden;position:relative";'
              'var s=document.querySelector(".scroll-area");'
              'if(s)s.style.height="100vh";')

    NEW_JS = ('if(window.innerWidth>=768)return;'
              'document.body.style.cssText="background:#fff;margin:0;padding:0;overflow:hidden";'
              'var d=document.querySelector(".device");'
              'if(d)d.style.cssText="width:100vw;height:100vh;margin:0;border-radius:0;border:none;box-shadow:none;background:#fff;overflow:hidden;position:relative";'
              'var s=document.querySelector(".scroll-area");'
              'if(s)s.style.height="100vh";'
              # Inject CSS to push bottom-0 elements above system nav bar
              'var st=document.createElement("style");'
              'st.textContent="[class*=\'bottom-0\']{bottom:env(safe-area-inset-bottom,0px)!important}"'
              '+"{padding-bottom:env(safe-area-inset-bottom,0px)!important}";'
              'document.head.appendChild(st);')

    h = h.replace(OLD_JS, NEW_JS)

    if h != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(h)
        updated += 1

print(f'Updated {updated} files')
