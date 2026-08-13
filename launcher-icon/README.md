# PCA Trace — Material Design 3 launcher icon

**App:** PCA Trace (`com.demicode.pcatrace`)  
**Org:** Philippine Coconut Authority (PCA) Region XIII  
**System:** Document Tracking System

Android adaptive launcher assets that follow [Material Design 3 / Material You](https://developer.android.com/develop/ui/compose/system/icon_design_adaptive) rules. No wordmark — the launcher label remains **PCA Trace**.

## Design

The official PCA Region XIII disc is already a flat geometric mark (green hemisphere, yellow annulus, off-white core). This pack keeps that construction, sampled from `source/pca_logo.png`, and places it on a Material 3 adaptive canvas.

| Layer | Role |
| --- | --- |
| Background | Brand green `#0B8A3C`, 108×108 dp, full bleed |
| Foreground | 66 dp circle keyline plate + 60 dp official seal (inside the 66 dp safe zone) |
| Monochrome | Black disc with the left core knocked out — tinted by the system on Android 13+ |

| Token | Hex | Source |
| --- | --- | --- |
| `pca-green` | `#0B8A3C` | Seal field / right hemisphere |
| `pca-yellow` | `#FFF200` | Left annulus (0.522R–0.900R) |
| `pca-surface` | `#F2F2F2` | Left core + keyline plate |

Seal ring ratios (from the official disc): white core **0.429R**, yellow **0.522R–0.900R**, green rim **0.900R–1.0R**.

## Specs followed

- Canvas **108×108 dp**; logo between **48 dp** and **66 dp**
- All critical artwork inside the **66 dp** safe zone (never clipped by OEM masks)
- Two layers for the color icon; optional **monochrome** layer for themed icons
- Clean edges — no baked-in mask, shadow, or rounded-corner padding
- Vectors preferred (`drawable/ic_launcher_*.xml`); PNG mipmaps for legacy API ≤ 25
- Play Store **512×512** is the 72 dp viewport, full bleed, opaque (Play applies its own mask)

## Layout

```
launcher-icon/
  svg/                          SVG masters (108 dp viewBox)
  android/res/
    values/ic_launcher_colors.xml
    drawable/ic_launcher_foreground.xml
    drawable/ic_launcher_monochrome.xml
    mipmap-anydpi-v26/          adaptive-icon XML (fg + bg + mono)
    mipmap-{mdpi..xxxhdpi}/     legacy + layer PNGs
  android/playstore/            512 px high-res icon
  preview/                      masks, themed icons, keylines, before/after
  source/                       current APK icon + official disc
  scripts/render_icons.py
```

## Flutter / Android drop-in

Copy `android/res/` into the Flutter app at `android/app/src/main/res/`.

1. Merge `values/ic_launcher_colors.xml` (or add `ic_launcher_background` to an existing `colors.xml`).
2. Copy `drawable/ic_launcher_foreground.xml` and `drawable/ic_launcher_monochrome.xml`.
3. Copy `mipmap-anydpi-v26/ic_launcher.xml` and `ic_launcher_round.xml`.
4. Copy `mipmap-*/ic_launcher.png` and `ic_launcher_round.png` (API 25 and below).
5. Optional: copy layer PNGs (`ic_launcher_foreground.png`, `ic_launcher_background.png`, `ic_launcher_monochrome.png`) if you prefer bitmaps over vectors.
6. Upload `android/playstore/ic_launcher-playstore-512.png` to Play Console.

Do not keep text in the icon. The system shows **PCA Trace** under the glyph.

```bash
pip install -r launcher-icon/scripts/requirements.txt
python3 launcher-icon/scripts/render_icons.py
```

Requires system Cairo (`libcairo2`).
