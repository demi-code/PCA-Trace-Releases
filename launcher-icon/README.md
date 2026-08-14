# PCA Trace — Document tracker launcher icon

**App:** PCA Trace (`com.demicode.pcatrace`)  
**Org:** Philippine Coconut Authority (PCA) Region XIII  
**System:** Document Tracking System

Android adaptive launcher assets for the document-tracker mark, using official PCA brand colors. No wordmark — the launcher label remains **PCA Trace**.

## Design

Document page with folded corner + yellow checkmark (tracked/verified), on a brand-green adaptive field.

| Layer | Role |
| --- | --- |
| Background | Brand green `#0B8A3C`, 108×108 dp, full bleed |
| Foreground | Surface document `#F2F2F2` + PCA yellow check `#FFF200` (inside the 66 dp safe zone) |
| Monochrome | Black document + check silhouette — tinted by the system on Android 13+ |

| Token | Hex | Source |
| --- | --- | --- |
| `pca-green` | `#0B8A3C` | Official PCA disc / adaptive background |
| `pca-yellow` | `#FFF200` | Official PCA disc annulus / checkmark |
| `pca-surface` | `#F2F2F2` | Document body |

Concept art: `source/doctrack-logo-pca-colors.png` (AI mark matched to `source/pca_logo.png` colors).

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
  source/                       current APK icon + concept + official disc
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
