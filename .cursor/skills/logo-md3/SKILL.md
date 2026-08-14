---
name: logo-md3
description: Generate product logos and app icons with Material Design 3. Use whenever the user asks to generate, create, redesign, or export a logo, brand mark, app icon, or launcher icon.
---
# Logo generation (Material Design 3)

## When this applies

Any request to generate, create, redesign, or export a **logo**, **brand mark**, **app icon**, or **launcher icon** — for any project.

## Hard requirements

1. **Material Design 3** — follow MD3 / Material You icon guidance.
2. **Always ship both formats:**
   - **SVG** — clean vector master (no raster embeds unless unavoidable)
   - **High-quality PNG** — at least **1024×1024** (prefer **2048×2048** for masters); transparent background unless the brief requires opaque

Never deliver only a raster preview or only an SVG.

## Material Design 3 checklist

### Adaptive / launcher icons (Android or general app icons)

- Canvas **108×108 dp**; keep critical artwork inside the **66 dp** safe zone
- Prefer layered adaptive structure when building Android packs:
  - background (flat brand color or simple field)
  - foreground (mark)
  - optional monochrome layer for themed icons
- No baked-in OEM mask, drop shadow, or fake rounded-corner padding on the master
- No wordmark in the launcher glyph unless the user explicitly asks
- Prefer geometric, flat shapes; avoid skeuomorphism and noisy effects

### Brand / standalone marks

- Flat or lightly dimensional MD3-compatible geometry
- Clear silhouette at **24–48 dp** sizes
- Prefer a short brand palette (seed + 1–2 accents); document hex tokens
- If a brand logo already exists, sample colors from it before inventing a new palette

## Delivery layout

Write files into the repo (or artifacts) with clear names, for example:

```
logos/<name>/
  <name>.svg                 # vector master
  <name>-1024.png            # HQ PNG (≥1024)
  <name>-2048.png            # optional ultra HQ
  colors.json                # optional hex tokens
```

For Android launcher packs, also produce density/mipmap assets as needed — still keep the SVG + HQ PNG masters.

## Workflow

1. Resolve brand colors (existing logo / brief) before drawing.
2. Author or refine an **SVG** master first.
3. Rasterize HQ **PNG** from that SVG (Cairo/resvg/ImageMagick — crisp, no JPEG).
4. If GenerateImage was used for ideation, convert the approved concept into SVG; do not ship the AI raster alone.
5. Show the user both the SVG path and the PNG preview/download paths.

## Do not

- Ship emoji, purple-glow “AI slop”, or illegible detail at small sizes
- Replace in-app brand assets unless the user asks (launcher-only when specified)
- Omit SVG or omit HQ PNG
