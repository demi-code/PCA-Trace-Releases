#!/usr/bin/env python3
"""Render PCA Trace launcher SVG masters (homescreen / adaptive only).

Produces:
  - drawable-*/ic_launcher_foreground.png (matches Flutter APK layout)
  - mipmap-*/ic_launcher(.png|_round.png) for API ≤ 25
  - Play Store 512
  - MD3 mask / themed-icon / 48dp previews

Does not touch in-app assets (pca_logo.png).
"""

from __future__ import annotations

import io
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SVG = ROOT / "svg"
OUT_RES = ROOT / "android" / "res"
OUT_PLAY = ROOT / "android" / "playstore"
OUT_PREVIEW = ROOT / "preview"
SOURCE = ROOT / "source"

PCA_GREEN = (11, 138, 60, 255)

# Legacy launcher icons (48dp @1x)
DENSITIES = {
    "mdpi": 48,
    "hdpi": 72,
    "xhdpi": 96,
    "xxhdpi": 144,
    "xxxhdpi": 192,
}

# Adaptive layers (108dp @1x)
ADAPTIVE = {
    "mdpi": 108,
    "hdpi": 162,
    "xhdpi": 216,
    "xxhdpi": 324,
    "xxxhdpi": 432,
}


def render_svg(svg_path: Path, size: int) -> Image.Image:
    png = cairosvg.svg2png(
        url=str(svg_path),
        output_width=size,
        output_height=size,
        background_color=None,
    )
    return Image.open(io.BytesIO(png)).convert("RGBA")


def save(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG", optimize=True)
    print(f"wrote {path.relative_to(ROOT)} ({img.size[0]}x{img.size[1]})")


def compose_full(size: int) -> Image.Image:
    bg = render_svg(SVG / "ic_launcher_background.svg", size)
    fg = render_svg(SVG / "ic_launcher_foreground.svg", size)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.alpha_composite(bg)
    out.alpha_composite(fg)
    return out


def apply_mask(img: Image.Image, mask: Image.Image) -> Image.Image:
    out = img.copy()
    out.putalpha(mask)
    return out


def mask_circle(size: int) -> Image.Image:
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    return mask


def mask_rounded(size: int, radius_ratio: float) -> Image.Image:
    mask = Image.new("L", (size, size), 0)
    r = max(1, int(size * radius_ratio))
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=r, fill=255)
    return mask


def mask_squircle(size: int) -> Image.Image:
    """Approximate Pixel / Material 3 squircle (superellipse n≈4)."""
    mask = Image.new("L", (size, size), 0)
    px = mask.load()
    n = 4.0
    c = (size - 1) / 2.0
    rn = c**n
    for y in range(size):
        for x in range(size):
            if abs(x - c) ** n + abs(y - c) ** n <= rn:
                px[x, y] = 255
    return mask.filter(ImageFilter.GaussianBlur(radius=size / 512))


def mask_teardrop(size: int) -> Image.Image:
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    # circle with a sharper bottom-right — OEM teardrop approximation
    draw.ellipse((0, 0, size - 1, size - 1), fill=255)
    r = int(size * 0.42)
    draw.pieslice((size - r * 2, size - r * 2, size - 1, size - 1), 0, 90, fill=255)
    return mask


def place_on(bg: Image.Image, fg: Image.Image, xy: tuple[int, int]) -> None:
    bg.paste(fg, xy, fg)


def sheet_masks(icon: Image.Image) -> Image.Image:
    """Five OEM masks on a dark board — Material Design 3 adaptive preview."""
    tile = 220
    gap = 28
    labels = ["Circle", "Squircle", "Rounded", "Square", "Teardrop"]
    masks = [
        mask_circle,
        mask_squircle,
        lambda s: mask_rounded(s, 0.18),
        lambda s: mask_rounded(s, 0.08),
        mask_teardrop,
    ]
    n = len(labels)
    W = gap + n * (tile + gap)
    H = tile + 96
    board = Image.new("RGBA", (W, H), (20, 24, 22, 255))
    draw = ImageDraw.Draw(board)
    draw.text((gap, 16), "Material Design 3 — adaptive masks", fill=(230, 230, 230))
    icon_s = icon.resize((tile, tile), Image.Resampling.LANCZOS)
    for i, (name, mfn) in enumerate(zip(labels, masks)):
        x = gap + i * (tile + gap)
        y = 48
        masked = apply_mask(icon_s, mfn(tile))
        place_on(board, masked, (x, y))
        tw = draw.textlength(name) if hasattr(draw, "textlength") else len(name) * 6
        draw.text((x + (tile - tw) / 2, y + tile + 10), name, fill=(180, 180, 180))
    return board


def sheet_themed(mono: Image.Image) -> Image.Image:
    """Material You themed-icon previews (Android 13+)."""
    palettes = [
        ("Default", (11, 138, 60), (232, 245, 233)),
        ("Tangerine", (122, 68, 16), (255, 223, 186)),
        ("Ocean", (16, 73, 122), (186, 220, 255)),
        ("Blush", (122, 28, 64), (255, 205, 220)),
        ("Slate", (48, 54, 60), (210, 216, 220)),
    ]
    tile = 200
    gap = 28
    n = len(palettes)
    W = gap + n * (tile + gap)
    H = tile + 96
    board = Image.new("RGBA", (W, H), (20, 24, 22, 255))
    draw = ImageDraw.Draw(board)
    draw.text((gap, 16), "Material You — themed icons (monochrome layer)", fill=(230, 230, 230))
    glyph = mono.resize((tile, tile), Image.Resampling.LANCZOS)
    squircle = mask_squircle(tile)
    for i, (name, fg, bg) in enumerate(palettes):
        x = gap + i * (tile + gap)
        y = 48
        layer = Image.new("RGBA", (tile, tile), bg + (255,))
        # tint glyph
        g = glyph.copy()
        alpha = g.split()[-1]
        tinted = Image.new("RGBA", (tile, tile), fg + (255,))
        tinted.putalpha(alpha)
        layer.alpha_composite(tinted)
        layer = apply_mask(layer, squircle)
        place_on(board, layer, (x, y))
        tw = draw.textlength(name) if hasattr(draw, "textlength") else len(name) * 6
        draw.text((x + (tile - tw) / 2, y + tile + 10), name, fill=(180, 180, 180))
    return board


def sheet_48dp(icon: Image.Image) -> Image.Image:
    """True 48dp (mdpi) and 108dp previews on a launcher-like grid."""
    W, H = 720, 320
    board = Image.new("RGBA", (W, H), (32, 36, 34, 255))
    draw = ImageDraw.Draw(board)
    for y in range(0, H, 24):
        draw.line((0, y, W, y), fill=(255, 255, 255, 18))
    for x in range(0, W, 24):
        draw.line((x, 0, x, H), fill=(255, 255, 255, 14))
    s48 = apply_mask(icon.resize((48, 48), Image.Resampling.LANCZOS), mask_squircle(48))
    s108 = apply_mask(icon.resize((108, 108), Image.Resampling.LANCZOS), mask_squircle(108))
    s192 = apply_mask(icon.resize((192, 192), Image.Resampling.LANCZOS), mask_squircle(192))
    place_on(board, s48, (80, (H - 48) // 2))
    place_on(board, s108, (200, (H - 108) // 2))
    place_on(board, s192, (400, (H - 192) // 2))
    d = ImageDraw.Draw(board)
    d.text((80, H - 36), "48dp", fill=(200, 200, 200))
    d.text((210, H - 36), "108dp", fill=(200, 200, 200))
    d.text((430, H - 36), "192px xxxhdpi", fill=(200, 200, 200))
    return board


def before_after(icon: Image.Image) -> Image.Image:
    current = Image.open(SOURCE / "current_foreground_xxxhdpi.png").convert("RGBA")
    current = current.resize((512, 512), Image.Resampling.LANCZOS)
    cur_board = Image.new("RGBA", (512, 512), (0, 0, 0, 255))
    cur_board.alpha_composite(current)
    new = apply_mask(icon.resize((512, 512), Image.Resampling.LANCZOS), mask_squircle(512))
    gap = 36
    compare = Image.new("RGBA", (512 * 2 + gap + 48, 512 + 80), (24, 24, 24, 255))
    compare.paste(cur_board, (24, 48))
    compare.paste(new, (24 + 512 + gap, 48), new)
    d = ImageDraw.Draw(compare)
    d.text((200, 16), "Current", fill=(200, 200, 200))
    d.text((24 + 512 + gap + 100, 16), "Document tracker", fill=(200, 200, 200))
    return compare


def homescreen_mock(icon: Image.Image) -> Image.Image:
    W, H = 1080, 1920
    wall = Image.new("RGB", (W, H), (18, 32, 28))
    draw = ImageDraw.Draw(wall, "RGBA")
    for y in range(0, H, 48):
        draw.line((0, y, W, y), fill=(255, 255, 255, 10))
    for x in range(0, W, 48):
        draw.line((x, 0, x, H), fill=(255, 255, 255, 8))

    icon_size = 192
    icon_r = apply_mask(icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS), mask_squircle(icon_size))
    x = (W - icon_size) // 2
    y = int(H * 0.28)
    wall.paste(icon_r, (x, y), icon_r)

    d = ImageDraw.Draw(wall)
    label_s = "PCA Trace"
    tw = d.textlength(label_s) if hasattr(d, "textlength") else len(label_s) * 8
    d.text(((W - tw) / 2, y + icon_size + 28), label_s, fill=(244, 244, 244))

    # dock of MD3 neighbors for scale
    dock_y = H - 280
    d.rounded_rectangle((90, dock_y, W - 90, dock_y + 160), radius=48, fill=(30, 48, 40))
    neighbors = [
        ((66, 165, 245), "Phone"),
        ((255, 183, 77), "Files"),
        (PCA_GREEN[:3], "PCA Trace"),
        ((171, 71, 188), "Chat"),
        ((239, 83, 80), "Mail"),
    ]
    slot = (W - 180) // 5
    for i, (color, name) in enumerate(neighbors):
        cx = 90 + slot * i + slot // 2
        r = 52
        tile = Image.new("RGBA", (r * 2, r * 2), color + (255,))
        if name == "PCA Trace":
            small = apply_mask(icon.resize((r * 2, r * 2), Image.Resampling.LANCZOS), mask_squircle(r * 2))
            wall.paste(small, (cx - r, dock_y + 24), small)
        else:
            tile = apply_mask(tile, mask_squircle(r * 2))
            wall.paste(tile, (cx - r, dock_y + 24), tile)
        tw = d.textlength(name) if hasattr(d, "textlength") else len(name) * 6
        d.text((cx - tw / 2, dock_y + 24 + r * 2 + 8), name, fill=(210, 210, 210))
    return wall


def keyline_overlay(icon: Image.Image) -> Image.Image:
    """108dp canvas with MD3 66dp circle keyline + 48dp minimum logo guides."""
    size = 648  # 108dp * 6
    canvas = icon.resize((size, size), Image.Resampling.LANCZOS)
    overlay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    scale = size / 108
    def box(dp, outline, width=3):
        p = (108 - dp) / 2 * scale
        draw.ellipse((p, p, size - p, size - p), outline=outline, width=width)
    box(108, (255, 255, 255, 40), 2)
    box(72, (255, 255, 255, 90), 2)
    box(66, (255, 213, 79, 220), 3)
    box(48, (129, 199, 132, 220), 3)
    out = canvas.convert("RGBA")
    out.alpha_composite(overlay)
    return out


def main() -> None:
    OUT_PREVIEW.mkdir(parents=True, exist_ok=True)
    OUT_PLAY.mkdir(parents=True, exist_ok=True)

    # Play Store high-res: full-bleed 72dp viewport (no adaptive 18dp padding).
    # Google Play applies its own mask; do not round or add alpha.
    master = compose_full(1080)
    pad = int(round(1080 * 18 / 108))
    play = master.crop((pad, pad, 1080 - pad, 1080 - pad)).resize(
        (512, 512), Image.Resampling.LANCZOS
    ).convert("RGB")
    save(play.convert("RGBA"), OUT_PLAY / "ic_launcher-playstore-512.png")
    save(play.convert("RGBA"), OUT_PREVIEW / "ic_launcher_512.png")

    # Adaptive foreground PNGs live under drawable-* (same as current APK).
    for density, size in ADAPTIVE.items():
        fg = render_svg(SVG / "ic_launcher_foreground.svg", size)
        save(fg, OUT_RES / f"drawable-{density}" / "ic_launcher_foreground.png")

    # Legacy launcher mipmaps only — no in-app image assets.
    for density, size in DENSITIES.items():
        full = compose_full(size)
        save(full, OUT_RES / f"mipmap-{density}" / "ic_launcher.png")
        save(apply_mask(full, mask_circle(size)), OUT_RES / f"mipmap-{density}" / "ic_launcher_round.png")

    preview = compose_full(512)
    save(preview, OUT_PREVIEW / "adaptive_composed_512.png")
    save(apply_mask(preview, mask_squircle(512)), OUT_PREVIEW / "adaptive_squircle_512.png")
    save(apply_mask(preview, mask_circle(512)), OUT_PREVIEW / "adaptive_circle_512.png")
    save(apply_mask(preview, mask_rounded(512, 0.18)), OUT_PREVIEW / "adaptive_rounded_512.png")
    save(sheet_masks(preview), OUT_PREVIEW / "md3_masks.png")
    save(sheet_themed(render_svg(SVG / "ic_launcher_monochrome.svg", 512)), OUT_PREVIEW / "md3_themed.png")
    save(sheet_48dp(preview), OUT_PREVIEW / "sizes_48_108.png")
    save(before_after(preview), OUT_PREVIEW / "before_after.png")
    save(homescreen_mock(preview), OUT_PREVIEW / "homescreen_mock.png")
    save(keyline_overlay(preview), OUT_PREVIEW / "md3_keylines.png")

    print("done")


if __name__ == "__main__":
    main()
