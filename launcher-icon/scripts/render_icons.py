#!/usr/bin/env python3
"""Render PCA Trace launcher SVG masters into Android density packs + previews."""

from __future__ import annotations

import io
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SVG = ROOT / "svg"
OUT_ANDROID = ROOT / "android"
OUT_PREVIEW = ROOT / "preview"
SOURCE = ROOT / "source"

# Android launcher sizes (px)
DENSITIES = {
    "mdpi": 48,
    "hdpi": 72,
    "xhdpi": 96,
    "xxhdpi": 144,
    "xxxhdpi": 192,
}
ADAPTIVE_FG = {
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
    """Compose background + foreground for legacy mipmaps / previews."""
    bg = render_svg(SVG / "ic_launcher_background.svg", size)
    fg = render_svg(SVG / "ic_launcher_foreground.svg", size)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.alpha_composite(bg)
    out.alpha_composite(fg)
    return out


def round_mask(img: Image.Image, radius_ratio: float = 0.5) -> Image.Image:
    """Circular (or squircle-ish via full circle) clipped preview."""
    size = img.size[0]
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size - 1, size - 1), fill=255)
    out = img.copy()
    out.putalpha(mask)
    return out


def squircle_mask(img: Image.Image) -> Image.Image:
    """Approximate Android squircle / rounded-rect mask for preview."""
    size = img.size[0]
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    r = int(size * 0.22)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=r, fill=255)
    out = img.copy()
    out.putalpha(mask)
    return out


def home_screen_mock(icon: Image.Image) -> Image.Image:
    """Simple wallpaper mock with labeled icon."""
    W, H = 1080, 1920
    wall = Image.new("RGB", (W, H), (18, 32, 28))
    # subtle vignette grid
    draw = ImageDraw.Draw(wall, "RGBA")
    for y in range(0, H, 48):
        draw.line((0, y, W, y), fill=(255, 255, 255, 10))
    for x in range(0, W, 48):
        draw.line((x, 0, x, H), fill=(255, 255, 255, 8))

    icon_size = 192
    icon_r = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    icon_r = squircle_mask(icon_r)
    x = (W - icon_size) // 2
    y = int(H * 0.28)
    wall.paste(icon_r, (x, y), icon_r)

    # label
    draw = ImageDraw.Draw(wall)
    label = "PCA Trace"
    # crude centered text without external fonts
    tw = draw.textlength(label) if hasattr(draw, "textlength") else len(label) * 8
    draw.text(((W - tw) / 2, y + icon_size + 28), label, fill=(244, 244, 244))

    # before/after strip at bottom
    legacy = Image.open(SOURCE / "current_foreground_xxxhdpi.png").convert("RGBA")
    legacy = legacy.resize((160, 160), Image.Resampling.LANCZOS)
    # place legacy on black tile then new
    tile = 180
    base_y = H - 280
    draw.rounded_rectangle((120, base_y, 120 + tile, base_y + tile), radius=36, fill=(0, 0, 0))
    wall.paste(legacy.resize((140, 140), Image.Resampling.LANCZOS), (130, base_y + 20), legacy.resize((140, 140), Image.Resampling.LANCZOS))
    draw.text((150, base_y + tile + 12), "Before", fill=(180, 180, 180))

    new_small = squircle_mask(icon.resize((140, 140), Image.Resampling.LANCZOS))
    nx = W - 120 - tile
    draw.rounded_rectangle((nx, base_y, nx + tile, base_y + tile), radius=36, fill=(11, 138, 60))
    wall.paste(new_small, (nx + 20, base_y + 20), new_small)
    draw.text((nx + 40, base_y + tile + 12), "After", fill=(180, 180, 180))

    return wall


def main() -> None:
    OUT_PREVIEW.mkdir(parents=True, exist_ok=True)

    # Master exports
    full_512 = render_svg(SVG / "ic_launcher_full.svg", 512)
    save(full_512, OUT_ANDROID / "playstore" / "ic_launcher-playstore-512.png")
    save(full_512, OUT_PREVIEW / "ic_launcher_512.png")

    # Adaptive layers at xxxhdpi reference + all densities
    for density, size in ADAPTIVE_FG.items():
        fg = render_svg(SVG / "ic_launcher_foreground.svg", size)
        bg = render_svg(SVG / "ic_launcher_background.svg", size)
        save(fg, OUT_ANDROID / f"mipmap-{density}" / "ic_launcher_foreground.png")
        save(bg, OUT_ANDROID / f"mipmap-{density}" / "ic_launcher_background.png")

    # Legacy full mipmaps (pre-API 26 / fallback)
    for density, size in DENSITIES.items():
        full = compose_full(size)
        save(full, OUT_ANDROID / f"mipmap-{density}" / "ic_launcher.png")
        save(round_mask(full), OUT_ANDROID / f"mipmap-{density}" / "ic_launcher_round.png")

    # Monochrome themed icon
    mono = render_svg(SVG / "ic_launcher_monochrome.svg", 432)
    save(mono, OUT_ANDROID / "mipmap-xxxhdpi" / "ic_launcher_monochrome.png")
    save(render_svg(SVG / "ic_launcher_monochrome.svg", 216), OUT_ANDROID / "mipmap-xhdpi" / "ic_launcher_monochrome.png")

    # Previews
    preview = compose_full(512)
    save(preview, OUT_PREVIEW / "adaptive_composed_512.png")
    save(squircle_mask(preview), OUT_PREVIEW / "adaptive_squircle_512.png")
    save(round_mask(preview), OUT_PREVIEW / "adaptive_circle_512.png")

    # Side-by-side comparison
    current = Image.open(SOURCE / "current_foreground_xxxhdpi.png").convert("RGBA")
    current = current.resize((512, 512), Image.Resampling.LANCZOS)
    # place current on black for fair compare
    cur_board = Image.new("RGBA", (512, 512), (0, 0, 0, 255))
    cur_board.alpha_composite(current)
    gap = 32
    compare = Image.new("RGBA", (512 * 2 + gap, 512 + 64), (24, 24, 24, 255))
    compare.paste(cur_board, (0, 32))
    compare.paste(preview, (512 + gap, 32))
    d = ImageDraw.Draw(compare)
    d.text((200, 8), "Current", fill=(200, 200, 200))
    d.text((512 + gap + 210, 8), "Reimagined", fill=(200, 200, 200))
    save(compare, OUT_PREVIEW / "before_after.png")

    mock = home_screen_mock(preview)
    save(mock, OUT_PREVIEW / "homescreen_mock.png")

    # Also copy SVG into android for reference
    for name in [
        "ic_launcher_foreground.svg",
        "ic_launcher_background.svg",
        "ic_launcher_full.svg",
        "ic_launcher_monochrome.svg",
    ]:
        target = OUT_ANDROID / "svg" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text((SVG / name).read_text(encoding="utf-8"), encoding="utf-8")
        print(f"wrote {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
