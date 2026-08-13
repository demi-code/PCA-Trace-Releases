# PCA Trace — Launcher Icon

**App:** PCA Trace  
**Org:** Philippine Coconut Authority (PCA) Region XIII  
**System:** Document Tracking System  

Android adaptive launcher assets for `com.demicode.pcatrace`.

## Concept

Circular PCA disc containing a document-tracking QR motif, with the official PCA hemispheric seal centered.

| Element | Meaning |
| --- | --- |
| Green / yellow / off-white seal | PCA Region XIII brand mark |
| QR finders + modules | Document tracking / QR custody |
| Brand-green background `#0B8A3C` | Adaptive icon field |

No wordmark in the icon (legible at 48dp). App name stays in the launcher label: **PCA Trace**.

## Palette

| Token | Hex |
| --- | --- |
| `pca-green` | `#0B8A3C` |
| `pca-yellow` | `#F8F000` |
| `pca-plate` | `#F4F4F4` |

## Layout

```
launcher-icon/
  svg/                      # Masters
  android/
    mipmap-anydpi-v26/      # adaptive-icon XML
    mipmap-{mdpi..xxxhdpi}/ # foreground, background, legacy, round, mono
    playstore/              # 512px
  preview/                  # before/after + mocks
  source/                   # reference marks from current APK / qrlogo
  scripts/render_icons.py
```

## Flutter / Android drop-in

Copy into `android/app/src/main/res/`:

1. `mipmap-*/ic_launcher.png`, `ic_launcher_round.png`
2. `mipmap-*/ic_launcher_foreground.png`, `ic_launcher_background.png`
3. `mipmap-anydpi-v26/ic_launcher.xml` (+ round)
4. Optional: `ic_launcher_monochrome.png`
5. Optional: sync in-app `assets/images/pca_logo.png` from `svg/ic_launcher_full.svg`

```bash
python3 launcher-icon/scripts/render_icons.py
```

Requires: `pip install cairosvg pillow` and system Cairo.
