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
import re
import sys
from pathlib import Path

import matplotlib.cm as cm
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
# Lightness boost for Viridis background (0.0 = original, 1.0 = white)
VIRIDIS_LIGHTEN = 0.65


def slug_to_viridis(slug: str) -> tuple[int, int, int]:
    """Convert a slug to a deterministic Viridis-based RGB color.

    Maps the slug's MD5 hash to a position on the Viridis colormap,
    then lightens the result so it works as a background behind the
    white-circled cat icon.
    """
    hv = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    t = (hv % 10000) / 10000.0
    r, g, b, _ = cm.viridis(t)
    # Lighten: blend toward white
    r = r + (1.0 - r) * VIRIDIS_LIGHTEN
    g = g + (1.0 - g) * VIRIDIS_LIGHTEN
    b = b + (1.0 - b) * VIRIDIS_LIGHTEN
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
    bg_color = slug_to_viridis(slug)
    og = Image.new("RGBA", (OG_WIDTH, OG_HEIGHT), bg_color + (255,))

    scale = TARGET_DIAMETER / (CIRCLE_RADIUS * 2)
    new_size = int(CIRCLE_RADIUS * 2 * scale)
    scaled = circle_icon.resize((new_size, new_size), Image.LANCZOS)

    paste_x = (OG_WIDTH - new_size) // 2
    paste_y = (OG_HEIGHT - new_size) // 2
    og.paste(scaled, (paste_x, paste_y), scaled)
    og.save(output_path)
    print(f"  {output_path.relative_to(output_path.parent.parent)} -> RGB{bg_color}")


def has_custom_og(qmd_path: Path) -> bool:
    """Check if the post declares a custom OG image via og-source (chart, custom, etc.)."""
    text = qmd_path.read_text()
    match = re.match(r"^---\n(.*?\n)---\n", text, re.DOTALL)
    if not match:
        return False
    return bool(re.search(r"^og-source:\s*\S+", match.group(1), re.MULTILINE))


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
        qmd_path = post_dir / "index.qmd"

        if has_custom_og(qmd_path) and output.exists():
            print(f"  {slug}: skipped (custom OG exists)")
        else:
            generate_og(circle_icon, slug, output)

        ensure_image_frontmatter(qmd_path)

    print("Done.")


def ensure_image_frontmatter(qmd_path: Path) -> None:
    """Add 'image: og-image.png' to front matter if missing."""
    text = qmd_path.read_text()

    # Extract front matter block (between --- delimiters)
    match = re.match(r"^---\n(.*?\n)---\n", text, re.DOTALL)
    if not match:
        return

    frontmatter = match.group(1)
    if re.search(r"^image:", frontmatter, re.MULTILINE):
        return

    # Insert image field before the closing ---
    new_text = text[: match.end(1)] + "image: og-image.png\n" + text[match.end(1) :]
    qmd_path.write_text(new_text)
    print(f"  Added 'image: og-image.png' to {qmd_path.name}")


if __name__ == "__main__":
    main()
