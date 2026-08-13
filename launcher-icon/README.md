# PCA Trace — Reimagined Launcher Icon

Drop-in Android adaptive icon assets for **PCA Trace** (`com.demicode.pcatrace`).

## Concept

**QR code inside a PCA logo mask** — the circular PCA disc is the clip mask; the QR (finders + modules) lives entirely inside that logo silhouette.

| Before (v0.0.3) | After |
| --- | --- |
| Seal + tiny wordmark on black | QR clipped to the PCA logo circle |
| No QR cue | Finders + modules in PCA green + yellow |
| White / black letterboxing | Brand-green adaptive background (`#0B8A3C`) |

QR styling: green finder frames, yellow eyes; modules yellow on the left / green on the right to echo the seal split. A green rim + vertical seam keep the PCA logo shape readable.

## Palette

| Token | Hex | Use |
| --- | --- | --- |
| `pca-green` | `#0B8A3C` | Adaptive background, QR modules, seal |
| `pca-yellow` | `#F8F000` | Seal C-band |
| `pca-plate` | `#F4F4F4` | QR quiet-zone plate + seal core |

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
  source/                      # current APK icons + qrlogo references
  scripts/render_icons.py      # regenerate PNGs from SVG
```

## Flutter / Android integration

Copy into the app module (`android/app/src/main/res/`):

1. Replace `mipmap-*/ic_launcher.png` and `ic_launcher_round.png`
2. Replace / add `mipmap-*/ic_launcher_foreground.png`
3. Replace / add `mipmap-*/ic_launcher_background.png` (or `@color` = `#0B8A3C`)
4. Replace `mipmap-anydpi-v26/ic_launcher.xml` (+ round)
5. Optional: `ic_launcher_monochrome.png` for Material You
6. Optional: sync in-app mark with `svg/ic_launcher_full.svg`

```bash
python3 launcher-icon/scripts/render_icons.py
```

Requires: `pip install cairosvg pillow` and system Cairo.

## Preview

See `preview/before_after.png`, `preview/adaptive_squircle_512.png`, and `preview/homescreen_mock.png`.
