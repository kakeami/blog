"""Generate OG images for blog posts.

Creates a 1200x630 OG image with the cat icon in a white circle
on a pastel background. The background color is deterministically
derived from the post directory name via MD5 hash, so the same
post always gets the same color.

Usage:
    # Generate for all posts
    python scripts/generate_og.py

    # Generate for a specific post
    python scripts/generate_og.py posts/2026-02-why-quarto
"""

import colorsys
import hashlib
import sys
from pathlib import Path

from PIL import Image, ImageDraw

# --- Configuration ---
ICON_PATH = Path(__file__).parent.parent / "icon.png"
POSTS_DIR = Path(__file__).parent.parent / "posts"
OG_WIDTH, OG_HEIGHT = 1200, 630
CIRCLE_RADIUS = 390
# Circle center in source image (shifted up so ears have room, clothing cut)
CX_SRC, CY_SRC = 440, 382
# Circle diameter in OG image
TARGET_DIAMETER = 540
# HSL parameters for pastel background
SATURATION = 0.40
LIGHTNESS = 0.88


def slug_to_pastel(slug: str) -> tuple[int, int, int]:
    """Convert a slug to a deterministic pastel RGB color."""
    hv = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    hue = (hv % 360) / 360.0
    r, g, b = colorsys.hls_to_rgb(hue, LIGHTNESS, SATURATION)
    return (int(r * 255), int(g * 255), int(b * 255))


def build_circle_icon(icon_path: Path) -> Image.Image:
    """Create a circular crop of the icon on a transparent background."""
    img = Image.open(icon_path).convert("RGBA")
    canvas_size = CIRCLE_RADIUS * 2

    # Place source image on canvas so circle center aligns with canvas center
    offset_x = CIRCLE_RADIUS - CX_SRC
    offset_y = CIRCLE_RADIUS - CY_SRC
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 255))
    canvas.paste(img, (offset_x, offset_y))

    # Circle mask
    mask = Image.new("L", (canvas_size, canvas_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, canvas_size, canvas_size), fill=255)

    # Apply mask
    white_bg = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 255))
    circle = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 0))
    circle = Image.composite(white_bg, circle, mask)
    circle.paste(canvas, (0, 0), mask)

    return circle


def generate_og(circle_icon: Image.Image, slug: str, output_path: Path) -> None:
    """Generate an OG image for a given slug."""
    bg_color = slug_to_pastel(slug)
    og = Image.new("RGBA", (OG_WIDTH, OG_HEIGHT), bg_color + (255,))

    scale = TARGET_DIAMETER / (CIRCLE_RADIUS * 2)
    new_size = int(CIRCLE_RADIUS * 2 * scale)
    scaled = circle_icon.resize((new_size, new_size), Image.LANCZOS)

    paste_x = (OG_WIDTH - new_size) // 2
    paste_y = (OG_HEIGHT - new_size) // 2
    og.paste(scaled, (paste_x, paste_y), scaled)
    og.save(output_path)
    print(f"  {output_path.relative_to(output_path.parent.parent)} -> RGB{bg_color}")


def main() -> None:
    if not ICON_PATH.exists():
        print(f"Error: icon not found at {ICON_PATH}")
        sys.exit(1)

    circle_icon = build_circle_icon(ICON_PATH)

    # Determine which posts to process
    if len(sys.argv) > 1:
        post_dirs = [Path(sys.argv[1])]
    else:
        post_dirs = sorted(
            d for d in POSTS_DIR.iterdir()
            if d.is_dir() and (d / "index.qmd").exists()
        )

    if not post_dirs:
        print("No posts found.")
        return

    print(f"Generating OG images for {len(post_dirs)} post(s):")
    for post_dir in post_dirs:
        slug = post_dir.name
        output = post_dir / "og-image.png"
        generate_og(circle_icon, slug, output)

    print("Done.")


if __name__ == "__main__":
    main()
