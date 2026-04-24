import glob, re

DESKTOP_MQ = """
  @media screen and (min-width: 500px) {
    html, body { background: #1a1a1a; overflow: auto; }
    .device { width: 390px; height: 780px; margin: 24px auto; border-radius: 36px; border: 8px solid #111; box-shadow: 0 30px 80px rgba(0,0,0,.4); }
    .scroll-area { height: 780px; }
  }"""

def fix_device_block(m):
    s = m.group(0)
    s = re.sub(r'width\s*:\s*390px', 'width: 100%', s)
    s = re.sub(r'height\s*:\s*780px', 'height: 100vh', s)
    s = re.sub(r'margin\s*:\s*24px auto;\s*', '', s)
    s = re.sub(r'border-radius\s*:\s*36px;\s*', '', s)
    s = re.sub(r'border\s*:\s*8px solid #111;\s*', '', s)
    s = re.sub(r'box-shadow\s*:\s*[^;]+;\s*', '', s)
    return s

files = glob.glob('screens/*.html')
updated = 0

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        h = f.read()
    orig = h

    # 1. Remove old max-width:480px block from previous fix
    h = re.sub(
        r'\n?\s*@media screen and \(max-width:\s*480px\)\s*\{.*?\n?\s*\}',
        '', h, flags=re.DOTALL
    )

    # 2. Fix html,body background to white (mobile default)
    h = re.sub(
        r'html,\s*body\s*\{\s*background:\s*#1a1a1a;?\s*\}',
        'html, body { background: #fff; margin: 0; padding: 0; overflow: hidden; }',
        h
    )

    # 3. Fix .device — remove fixed size/frame, make full-screen
    h = re.sub(r'\.device\s*\{[^}]+\}', fix_device_block, h)

    # 4. Fix .scroll-area height: 100% → 100vh
    h = re.sub(
        r'(\.scroll-area\s*\{[^}]*)height\s*:\s*100%',
        r'\1height: 100vh',
        h
    )

    # 5. Add desktop media query (once only)
    if 'min-width: 500px' not in h and '</style>' in h:
        h = h.replace('</style>', DESKTOP_MQ + '\n</style>', 1)

    if h != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(h)
        updated += 1

print(f'Updated {updated} files')
