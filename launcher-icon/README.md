# PCA Trace — Reimagined Launcher Icon

Drop-in Android adaptive icon assets for **PCA Trace** (`com.demicode.pcatrace`).

## What changed

| Before | After |
| --- | --- |
| Seal + tiny “PCA RXIII / Document Tracking System” wordmark baked into the foreground | Symbol-only mark (legible at 48dp) |
| White adaptive background; black letterboxed legacy mipmaps | Brand-green adaptive background (`#0B8A3C`) |
| Static seal only | Seal + yellow **trace orbit** (custody / live-track cue) |
| No themed icon | Monochrome layer for Android 13+ |

Brand DNA kept: PCA hemispheric seal (green / yellow / off-white).

## Palette

| Token | Hex | Use |
| --- | --- | --- |
| `pca-green` | `#0B8A3C` | Adaptive background, seal right half |
| `pca-yellow` | `#F8F000` | C-band + trace orbit |
| `pca-plate` | `#F4F4F4` | Soft plate + seal core |

## Layout

```
launcher-icon/
  svg/                         # Masters (edit these)
  android/
    mipmap-anydpi-v26/         # adaptive-icon XML
    mipmap-{mdpi..xxxhdpi}/    # foreground, background, legacy, round
    playstore/                 # 512px store icon
    svg/                       # copies of masters
  preview/                     # before/after + mask previews
  source/                      # current APK-extracted icons
  scripts/render_icons.py      # regenerate PNGs from SVG
```

## Flutter / Android integration

Copy into the app module (paths relative to `android/app/src/main/res/`):

1. Replace `mipmap-*/ic_launcher.png` and `ic_launcher_round.png`
2. Replace / add `mipmap-*/ic_launcher_foreground.png`
3. Replace / add `mipmap-*/ic_launcher_background.png` (or use `@color/ic_launcher_background` = `#0B8A3C`)
4. Replace `mipmap-anydpi-v26/ic_launcher.xml` (+ round)
5. Optional: add `ic_launcher_monochrome.png` for Material You
6. Update in-app `assets/images/pca_logo.png` from `svg/ic_launcher_full.svg` if you want the chrome mark to match

Regenerate after SVG edits:

```bash
python3 launcher-icon/scripts/render_icons.py
```

Requires: `pip install cairosvg pillow` and system Cairo.

## Preview

See `preview/before_after.png`, `preview/adaptive_squircle_512.png`, and `preview/homescreen_mock.png`.
