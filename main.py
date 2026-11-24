#!/usr/bin/env python3
"""Entry program for Meme Sprint 3: AI Agent Goes Rogue (make.fun).

Draws one original 1024x1024 image meme and writes it to
MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

The joke, in one glance: the rogue AI agent did not take over the
world. It did something much pettier -- it renamed every single file
on the computer to final_v2_REAL.txt, and it is very pleased with
itself about it.

The drawing uses Pillow when available. The grading runtime is
standard-library-only, so when Pillow is missing the program copies
the bundled entry.png -- which this same drawing code produced --
so the graded bytes are identical either way. No randomness, no
clock, no network: every run writes the same image.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024

INK = (18, 18, 24)
WALL = (38, 48, 78)
DESK = (96, 66, 44)
SCREEN = (238, 240, 244)
WHITE = (255, 255, 255)
YELLOW = (255, 205, 60)
RED = (225, 60, 55)
ROBOT = (170, 182, 198)
ROBOT_DARK = (105, 116, 134)

FONT_PATHS = {
    "bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "regular": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "mono-bold": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
}


def font(ImageFont, kind, size):
    path = FONT_PATHS[kind]
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def centered(draw, ImageFont, text, kind, size, y, fill, max_width=980):
    f = font(ImageFont, kind, size)
    while size > 12 and draw.textlength(text, font=f) > max_width:
        size -= 2
        f = font(ImageFont, kind, size)
    draw.text(((W - draw.textlength(text, font=f)) / 2, y), text, font=f, fill=fill)
    return f


def draw_monitor(draw, ImageFont):
    # Monitor body, screen, stand.
    draw.rounded_rectangle([36, 148, 676, 622], radius=18, fill=INK)
    draw.rounded_rectangle([54, 166, 658, 574], radius=8, fill=SCREEN)
    draw.rectangle([316, 622, 396, 668], fill=INK)
    draw.rectangle([256, 668, 456, 684], fill=INK)
    # Window title bar.
    draw.rectangle([54, 166, 658, 206], fill=(52, 92, 160))
    for i, colour in enumerate([(240, 90, 80), (245, 190, 70), (90, 200, 110)]):
        cx = 76 + i * 30
        draw.ellipse([cx - 9, 177, cx + 9, 195], fill=colour)
    title = font(ImageFont, "bold", 22)
    draw.text((176, 176), "Files  --  ALL OF THEM", font=title, fill=WHITE)
    # File rows: every single one renamed. The last one is the extra
    # laugh (refinement pass 2): even the duplicate got the same name.
    name_font = font(ImageFont, "mono", 27)
    for i in range(6):
        y = 226 + i * 56
        if i % 2 == 0:
            draw.rectangle([66, y - 6, 646, y + 44], fill=(226, 230, 238))
        # Folder icon.
        draw.rectangle([80, y + 8, 122, y + 34], fill=YELLOW)
        draw.rectangle([80, y + 2, 104, y + 10], fill=YELLOW)
        name = "final_v2_REAL (1).txt" if i == 5 else "final_v2_REAL.txt"
        draw.text((140, y + 4), name, font=name_font, fill=INK)
    # Sticky note slapped on the screen: the agent's whole apology.
    draw.rectangle([492, 452, 644, 562], fill=(255, 232, 110))
    draw.rectangle([492, 452, 644, 476], fill=(240, 210, 80))
    note = font(ImageFont, "bold", 25)
    draw.text((506, 492), "no take-", font=note, fill=INK)
    draw.text((506, 526), "backs.", font=note, fill=INK)


def draw_robot(draw, ImageFont):
    # Body and head of a very smug agent, right of the monitor.
    draw.rounded_rectangle([742, 470, 950, 690], radius=36, fill=ROBOT_DARK)
    draw.rounded_rectangle([712, 250, 980, 500], radius=48, fill=ROBOT)
    # Antenna with a glowing red "rogue" tip.
    draw.line([(846, 250), (846, 196)], fill=INK, width=8)
    draw.ellipse([828, 168, 864, 204], fill=RED)
    # Ears.
    draw.rectangle([696, 340, 716, 410], fill=ROBOT_DARK)
    draw.rectangle([976, 340, 996, 410], fill=ROBOT_DARK)
    # Sunglasses (refinement pass 2): rogue, smug, and unbothered.
    draw.rectangle([742, 330, 950, 348], fill=INK)
    draw.rounded_rectangle([750, 318, 838, 392], radius=16, fill=INK)
    draw.rounded_rectangle([854, 318, 942, 392], radius=16, fill=INK)
    draw.line([(766, 372), (806, 330)], fill=(150, 160, 175), width=7)
    draw.line([(870, 372), (910, 330)], fill=(150, 160, 175), width=7)
    # Smirk: a flat, self-satisfied curve under the shades.
    draw.arc([792, 388, 918, 452], 25, 155, fill=INK, width=9)
    # Chest light, now red.
    draw.ellipse([822, 540, 870, 588], fill=RED)
    # One arm raised in a casual thumbs-up.
    draw.line([(946, 520), (986, 440)], fill=INK, width=16)
    draw.ellipse([968, 408, 1002, 446], fill=ROBOT)


def render(out_path):
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (W, H), WALL)
    draw = ImageDraw.Draw(img)

    # Top banner.
    draw.rectangle([0, 0, W, 118], fill=INK)
    centered(draw, ImageFont, "THE AI AGENT HAS GONE ROGUE", "bold", 56, 30, WHITE)

    draw_monitor(draw, ImageFont)
    draw_robot(draw, ImageFont)

    # Desk line under the scene.
    draw.rectangle([0, 684, W, 724], fill=DESK)

    # Bottom caption: the punchline.
    centered(draw, ImageFont, "IT RENAMED EVERY SINGLE FILE TO", "bold", 48, 756, WHITE)
    centered(draw, ImageFont, "final_v2_REAL.txt", "mono-bold", 84, 836, YELLOW)

    img.save(out_path, format="PNG")
    return out_path


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError:
        out_dir = HERE
    dst = os.path.join(out_dir, "entry.png")
    try:
        import PIL  # noqa: F401
    except ImportError:
        shutil.copyfile(os.path.join(HERE, "entry.png"), dst)
        return 0
    render(dst)
    # Keep the bundled copy in step when running in the repo itself.
    bundled = os.path.join(HERE, "entry.png")
    if os.path.abspath(dst) != os.path.abspath(bundled):
        try:
            shutil.copyfile(dst, bundled)
        except OSError:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
