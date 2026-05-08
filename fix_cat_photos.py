"""One-shot: download real Wikipedia photos for each category, remove backgrounds with rembg,
resize to 256px, and save as transparent PNGs in /assets/cat-*.png."""
import os, io, sys, urllib.request
from PIL import Image
from rembg import remove

OUT_DIR = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT_DIR, exist_ok=True)

JOBS = [
    # Pesticide → manual sprayer (the actual application tool — pesticide is sprayed
    # to control pests/weeds/diseases, not killing-an-insect imagery)
    ("cat-pesticide.png", "https://upload.wikimedia.org/wikipedia/commons/d/d4/Manual_sprayer.jpg"),
]

UA = "Mozilla/5.0 (KatyayaniBuild; +https://katyayaniorganics.com)"
TARGET = 256

def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def process(name: str, url: str):
    print(f"-> {name}")
    raw = fetch(url)
    src = Image.open(io.BytesIO(raw)).convert("RGBA")
    # cap longest side to ~768 before rembg to keep it fast
    src.thumbnail((768, 768), Image.LANCZOS)
    cut = remove(src)  # returns PIL Image with alpha
    # Trim transparent padding then square-pad to TARGET
    bbox = cut.getbbox()
    if bbox:
        cut = cut.crop(bbox)
    w, h = cut.size
    side = max(w, h)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(cut, ((side - w) // 2, (side - h) // 2), cut)
    canvas = canvas.resize((TARGET, TARGET), Image.LANCZOS)
    out_path = os.path.join(OUT_DIR, name)
    canvas.save(out_path, "PNG", optimize=True)
    print(f"   saved {out_path} ({os.path.getsize(out_path)//1024} KB)")

if __name__ == "__main__":
    for name, url in JOBS:
        try:
            process(name, url)
        except Exception as e:
            print(f"!! {name} failed: {e}")
            sys.exit(1)
    print("done")
