import glob

QUERY = """
  @media screen and (max-width: 480px) {
    html, body { background: #fff !important; margin: 0; padding: 0; overflow: hidden; }
    .device { width: 100vw !important; height: 100vh !important; margin: 0 !important;
              border-radius: 0 !important; border: none !important; box-shadow: none !important; }
    .scroll-area { height: 100vh !important; }
  }"""

files = glob.glob('screens/*.html')
updated = 0
for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        h = f.read()
    if '@media screen and (max-width: 480px)' in h:
        continue
    if '</style>' not in h:
        continue
    h = h.replace('</style>', QUERY + '\n</style>', 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(h)
    updated += 1

print(f'Updated {updated} files')
