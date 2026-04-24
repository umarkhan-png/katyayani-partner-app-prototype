import os, glob

PWA_HEAD = '''  <link rel="manifest" href="/katyayani-partner-app-prototype/manifest.json">
  <meta name="theme-color" content="#0E7A4E">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="KT Partner">'''

SW_SCRIPT = '  <script>if("serviceWorker"in navigator){navigator.serviceWorker.register("/katyayani-partner-app-prototype/sw.js")}</script>'

files = glob.glob('screens/*.html')
updated = 0
for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        h = f.read()
    if 'rel="manifest"' in h:
        continue
    h = h.replace('<meta name="viewport"', PWA_HEAD + '\n  <meta name="viewport"', 1)
    if '</body>' in h:
        h = h.replace('</body>', SW_SCRIPT + '\n</body>', 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(h)
    updated += 1

print(f'Updated {updated} files')
