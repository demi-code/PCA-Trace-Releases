# PCA Trace — Launcher icon only

**App:** PCA Trace (`com.demicode.pcatrace`)  
**Scope:** Android **homescreen / launcher** icon only.  
**Do not** replace in-app branding (`assets/images/pca_logo.png` or any Flutter UI asset).

## Design

Document page + yellow check on brand-green field (PCA Region XIII colors).

| Layer | Role |
| --- | --- |
| Background | `#0B8A3C` via `@color/ic_launcher_background` |
| Foreground | `@drawable/ic_launcher_foreground` — document + check (66 dp safe zone) |
| Monochrome | `@drawable/ic_launcher_monochrome` — Android 13+ themed icons |

| Token | Hex |
| --- | --- |
| `pca-green` | `#0B8A3C` |
| `pca-yellow` | `#FFF200` |
| `pca-surface` | `#F2F2F2` |

## What to copy (launcher only)

Copy these into the Flutter app’s `android/app/src/main/res/` — **nothing under** `assets/` or Dart UI:

| From `launcher-icon/android/res/` | Purpose |
| --- | --- |
| `values/ic_launcher_colors.xml` | Merge `ic_launcher_background` into existing `colors.xml` if present (current APK uses white — replace with `#0B8A3C`) |
| `drawable-*/ic_launcher_foreground.png` | Adaptive foreground (replaces existing launcher foreground PNGs) |
| `drawable/ic_launcher_monochrome.xml` | Themed-icon layer (new) |
| `mipmap-anydpi-v26/ic_launcher.xml` | Adaptive icon (no 16% inset — artwork already safe-zoned) |
| `mipmap-anydpi-v26/ic_launcher_round.xml` | Round adaptive (optional; add if you use `roundIcon`) |
| `mipmap-*/ic_launcher.png` (+ `_round.png`) | Legacy API ≤ 25 |

**Do not copy / do not replace**

- `assets/flutter_assets/assets/images/pca_logo.png` (or source `assets/images/pca_logo.png`)
- Any other Flutter image, splash logo widget, or in-app header that uses the official PCA disc
- Concept art under `launcher-icon/source/` (reference only)

Splash (`windowSplashScreenAnimatedIcon` → `@mipmap/ic_launcher`) will follow the launcher icon automatically. That is still the system launch glyph, not in-app content. Keep the official disc for in-app UI.

## Layout

```
launcher-icon/
  svg/                     masters
  android/res/             drop-in launcher resources only
  android/playstore/       Play Console 512
  preview/
  source/                  reference only (current icon, pca_logo, concept)
  scripts/render_icons.py
```

```bash
pip install -r launcher-icon/scripts/requirements.txt
python3 launcher-icon/scripts/render_icons.py
```

Requires Cairo (`libcairo2`).
