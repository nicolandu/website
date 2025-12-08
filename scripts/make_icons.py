#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path

from PIL import Image

# Input SVG
FLUSH = "favicon.svg"
DIR = Path("static")
IMAGE_TMP_DIR = Path("img_tmp")
OG_ICON = "og-icon.png"
OG_SIZE = (1200, 630)


subprocess.run(
    [
        "inkscape",
        DIR / FLUSH,
        f"--export-filename={DIR/OG_ICON}",
        f"--export-width={min(*OG_SIZE)}",
        f"--export-height={min(*OG_SIZE)}",
        "--export-background=#ffffff",
    ],
    check=True,
)

subprocess.run(
    [
        "inkscape",
        DIR / FLUSH,
        f"--export-filename={DIR/"favicon.png"}",
        f"--export-width=512",
        f"--export-height=512",
    ],
    check=True,
)
subprocess.run(
    [
        "inkscape",
        DIR / FLUSH,
        f"--export-filename={DIR/"apple-touch-icon.png"}",
        f"--export-width=180",
        f"--export-height=180",
        "--export-background=#ffffff",
    ],
    check=True,
)

os.makedirs(IMAGE_TMP_DIR, exist_ok=True)
# PNG sizes to export
SIZES = [16, 32, 48, 64, 128, 180, 192, 256, 512]
# Convert SVG to PNGs at different sizes using Inkscape
for size in SIZES:
    png_path = IMAGE_TMP_DIR / f"favicon-{size}.png"
    subprocess.run(
        [
            "inkscape",
            DIR / FLUSH,
            f"--export-filename={png_path}",
            f"--export-width={size}",
            f"--export-height={size}",
        ],
        check=True,
    )

img = Image.open(DIR / OG_ICON)
new_img = Image.new("RGB", OG_SIZE, (255, 255, 255))

# center image
x_offset = (OG_SIZE[0] - img.width) // 2
y_offset = (OG_SIZE[1] - img.height) // 2
new_img.paste(img, (x_offset, y_offset))
new_img.save(DIR / OG_ICON)

# Build multi-resolution ICO from previously exported PNGs
ico_path = DIR / "favicon.ico"

# List of sizes to include in the ICO
size = SIZES[-1]
image = Image.open(IMAGE_TMP_DIR / f"favicon-{size}.png")

ico_sizes = [16, 32, 48, 64, 128, 256]
# Save as .ico with all sizes included
image.save(ico_path, format="ICO", sizes=[(size, size) for size in ico_sizes])
shutil.rmtree(IMAGE_TMP_DIR)
