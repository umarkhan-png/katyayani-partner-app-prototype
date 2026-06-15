# Design System — Asset Export & Animations

How the downloadable assets in `screens/design-system.html` work, and the animated assets in `assets/`.
Last updated: 2026-06-15.

## Download library

Every asset in the design system has a hover **⬇ download** button (and each section has a
"Download all" zip via JSZip). The format is decided per element, in `injectDlButton`:

| Element attribute | Download format | Used for |
|---|---|---|
| `data-dl-gif="path.svg"` | **Animated GIF** (gif.js) | The 3 animated illustrations |
| `data-dl-src="path"` | the **raw file as-is** (anchor `download`) | shipping a `.svg` unchanged |
| _(none)_ | **WebP** still (canvas → `toBlob`) | all static icons/tiles/bg's |

Optional GIF attributes: `data-dl-dur` (loop seconds), `data-dl-w`, `data-dl-h`, `data-dl-bg`.

Libraries are loaded from CDN: **JSZip** (zip) and **gif.js 0.2.0** (GIF encoding).

### How the animated GIF export works (`exportGif`)

1. Loads the animated SVG into an `<img>` and draws it to a canvas every `1000/fps` ms (fps = 12),
   feeding each canvas frame to gif.js.
2. **gif.js worker is cross-origin-blocked on cdnjs** → we fetch `gif.worker.js` and pass a
   **same-origin blob URL** as `workerScript`.
3. **The capture `<img>` must be painted on-screen**, otherwise Chrome throttles its repaint and the
   SVG/SMIL animation freezes — every captured frame becomes identical and the GIF looks static.
   So capture happens behind a full-screen "Rendering GIF…" overlay, then it's removed.

> WebP and the zip are always a single still frame. **GIFs are the only animated download.**
> An animated `.svg` only plays in a browser / the app — not in Windows Photos. The GIF plays anywhere.

## Animated SVG assets (`assets/`)

SMIL animations baked inside; they animate when used via `<img>` or in a browser.

- **`welcome-language-hero.svg`** — onboarding hero: Katyayani logo + "Welcome" + glass A/आ tiles.
  Front tile cycles scripts (A → अ → অ …), tiles float, sparkles twinkle. Aspect 390×480.
- **`verify-unlock-animating.svg`** — cream badge + padlock + expanding gold radar pulse rings.
- **`language-globe-animating.svg`** — spinning globe + cycling scripts (A/अ/অ) + rotating dashed
  gold orbit + orbit dot. Also embedded live on the **language screen** (`language.html`) by the title.

## Coin / Notification icons

In the "Screen Animations & Glass Components" card. These are **border + glassy fill + icon ONLY** —
the count pill and red unread badge are intentionally **removed** (they're added in app code).

- Single self-contained SVG, square ~52px.
- Glass = translucent white gradient `rgba(255,255,255, .22 → .06)` + gold `#D4A537` border (1.2px).
  No solid fill — the background behind shows through the layer.
- Exported as a transparent WebP.

The **distributor** and **farmer** role icons live in the §06 Icon Library (24×24, stroke `#1C1C1C`).

## Verifying animation output

Don't trust file size / "multi-frame" to mean it animates. Decode the GIF and count **unique** frames:

```python
from PIL import Image
im = Image.open('asset.gif'); frames=[]
try:
    while True:
        frames.append(im.convert('RGB').tobytes()); im.seek(im.tell()+1)
except EOFError: pass
print(len(frames), 'frames,', len(set(frames)), 'unique')   # unique≈frames → animates
```
