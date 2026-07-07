#!/usr/bin/env python3
"""Render localized mobile store preview images from simulator screenshots."""

from __future__ import annotations

import argparse
import json
import math
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit(
        "Pillow is required. Use the Codex bundled Python runtime or install Pillow."
    ) from exc


DEFAULT_FONT = "/System/Library/Fonts/SFNS.ttf"
DEFAULT_PALETTE = {
    "top": "#F7FAFF",
    "bottom": "#E8F1FB",
    "text": "#121F32",
    "muted": "#5B6C82",
    "accent": "#1A70D2",
}


@dataclass(frozen=True)
class Canvas:
    width: int
    height: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="Path to renderer JSON config.")
    parser.add_argument(
        "--contact-sheet",
        help="Optional output path for a small visual overview of generated previews.",
    )

    return parser.parse_args()


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    raw = value.strip().lstrip("#")
    if len(raw) != 6:
        raise ValueError(f"Expected 6-digit hex color, got {value!r}")

    return tuple(int(raw[index : index + 2], 16) for index in (0, 2, 4))


def resolve_path(base_dir: Path, value: str | None) -> Path | None:
    if not value:
        return None

    path = Path(value).expanduser()
    return path if path.is_absolute() else base_dir / path


def load_font(path: str | None, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    candidates = [path, DEFAULT_FONT, "/System/Library/Fonts/AppleSDGothicNeo.ttc"]
    for candidate in candidates:
        if not candidate:
            continue
        try:
            return ImageFont.truetype(candidate, size=size, index=index)
        except OSError:
            continue

    raise RuntimeError("No usable TrueType font found.")


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.multiline_textbbox((0, 0), text, font=font, spacing=10, align="center")

    return box[2] - box[0], box[3] - box[1]


def draw_centered(
    draw: ImageDraw.ImageDraw,
    x: float,
    y: float,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    spacing: int = 10,
) -> None:
    box = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing, align="center")
    width = box[2] - box[0]
    draw.multiline_text((x - width / 2, y), text, font=font, fill=fill, spacing=spacing, align="center")


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)

    return mask


def build_background(canvas: Canvas, palette: dict[str, str]) -> Image.Image:
    top = hex_to_rgb(palette.get("top", DEFAULT_PALETTE["top"]))
    bottom = hex_to_rgb(palette.get("bottom", DEFAULT_PALETTE["bottom"]))
    accent = hex_to_rgb(palette.get("accent", DEFAULT_PALETTE["accent"]))
    image = Image.new("RGB", (canvas.width, canvas.height), top)
    pixels = image.load()

    for y in range(canvas.height):
        ratio = y / (canvas.height - 1)
        color = tuple(round(top[i] * (1 - ratio) + bottom[i] * ratio) for i in range(3))
        for x in range(canvas.width):
            pixels[x, y] = color

    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.ellipse(
        (-270, math.floor(canvas.height * 0.65), 620, math.floor(canvas.height * 0.97)),
        fill=(*accent, 22),
    )
    draw.ellipse(
        (math.floor(canvas.width * 0.64), 430, math.floor(canvas.width * 1.22), 1230),
        fill=(255, 255, 255, 92),
    )

    return Image.alpha_composite(image.convert("RGBA"), overlay)


def build_phone(screen: Image.Image, width: int, rotate: float = 0) -> tuple[Image.Image, Image.Image]:
    screen_width, screen_height = screen.size
    target_width = width
    target_height = round(target_width * screen_height / screen_width)
    screenshot = screen.resize((target_width, target_height), Image.Resampling.LANCZOS)
    bezel = 28
    outer_width = target_width + bezel * 2
    outer_height = target_height + bezel * 2
    phone = Image.new("RGBA", (outer_width, outer_height), (0, 0, 0, 0))

    shadow = Image.new("RGBA", (outer_width + 120, outer_height + 120), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        (60, 60, 60 + outer_width, 60 + outer_height),
        radius=94,
        fill=(13, 24, 38, 82),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(26))

    draw = ImageDraw.Draw(phone)
    draw.rounded_rectangle((0, 0, outer_width - 1, outer_height - 1), radius=96, fill=(10, 16, 26))
    draw.rounded_rectangle(
        (8, 8, outer_width - 9, outer_height - 9),
        radius=88,
        outline=(66, 76, 92),
        width=4,
    )
    phone.paste(screenshot, (bezel, bezel), rounded_mask((target_width, target_height), 72))
    draw.rounded_rectangle((-3, 300, 7, 430), radius=5, fill=(8, 13, 22))
    draw.rounded_rectangle((outer_width - 7, 430, outer_width + 3, 590), radius=5, fill=(8, 13, 22))

    if rotate:
        phone = phone.rotate(rotate, expand=True, resample=Image.Resampling.BICUBIC)
        shadow = shadow.rotate(rotate, expand=True, resample=Image.Resampling.BICUBIC)

    return phone, shadow


def render_item(
    *,
    canvas: Canvas,
    config_dir: Path,
    source_dir: Path,
    output_dir: Path,
    language: dict[str, Any],
    item: dict[str, Any],
    y_shift: int,
    badge: str,
) -> Path:
    code = language["code"]
    palette = {**DEFAULT_PALETTE, **language.get("palette", {})}
    text_color = hex_to_rgb(palette["text"])
    muted_color = hex_to_rgb(palette.get("muted", DEFAULT_PALETTE["muted"]))
    accent = hex_to_rgb(palette["accent"])
    font_path = language.get("font")
    title_font = load_font(font_path, int(item.get("title_size", language.get("title_size", 82))))
    subtitle_font = load_font(font_path, int(item.get("subtitle_size", language.get("subtitle_size", 34))))
    badge_font = load_font(font_path, int(item.get("badge_size", 26)))

    image = build_background(canvas, palette)
    draw = ImageDraw.Draw(image)

    badge_y = int(item.get("badge_y", 62)) + y_shift
    badge_width, _ = text_size(draw, badge, badge_font)
    badge_x = (canvas.width - badge_width) / 2 - 32
    draw.rounded_rectangle(
        (badge_x, badge_y, badge_x + badge_width + 64, badge_y + 44),
        radius=22,
        fill=(255, 255, 255, 190),
        outline=(214, 226, 240, 180),
        width=2,
    )
    draw.text((canvas.width / 2 - badge_width / 2, badge_y + 6), badge, font=badge_font, fill=muted_color)

    draw_centered(
        draw,
        canvas.width / 2,
        int(item.get("title_y", 150)) + y_shift,
        item["title"],
        title_font,
        text_color,
        spacing=int(item.get("title_spacing", 8)),
    )
    draw_centered(
        draw,
        canvas.width / 2,
        int(item.get("subtitle_y", 354)) + y_shift,
        item["subtitle"],
        subtitle_font,
        muted_color,
        spacing=int(item.get("subtitle_spacing", 4)),
    )

    source_path = resolve_path(config_dir, item["source"])
    if source_path is None or not source_path.exists():
        source_path = source_dir / item["source"]
    screen = Image.open(source_path).convert("RGBA")
    phone, shadow = build_phone(
        screen,
        width=int(item.get("phone_width", 820)),
        rotate=float(item.get("rotate", 0)),
    )
    phone_y = int(item.get("phone_y", 540)) + y_shift
    phone_x = (canvas.width - phone.size[0]) // 2
    shadow_x = phone_x - (shadow.size[0] - phone.size[0]) // 2
    shadow_y = phone_y - (shadow.size[1] - phone.size[1]) // 2 + 28
    image.alpha_composite(shadow, (shadow_x, shadow_y))
    image.alpha_composite(phone, (phone_x, phone_y))

    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (canvas.width // 2 - 74, canvas.height - 118, canvas.width // 2 + 74, canvas.height - 108),
        radius=5,
        fill=(*accent, 210),
    )

    lang_dir = output_dir / code
    lang_dir.mkdir(parents=True, exist_ok=True)
    output_path = lang_dir / item["file"]
    image.convert("RGB").save(output_path, "PNG", optimize=True)

    return output_path


def write_zip(zip_path: Path, outputs: list[Path], output_dir: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in outputs:
            archive.write(path, path.relative_to(output_dir))


def write_contact_sheet(path: Path, outputs_by_lang: dict[str, list[Path]]) -> None:
    thumb_width = 260
    padding = 24
    rows: list[tuple[str, list[Image.Image]]] = []
    for code, outputs in outputs_by_lang.items():
        thumbs = []
        for output in outputs:
            image = Image.open(output).convert("RGB")
            height = round(thumb_width * image.height / image.width)
            thumbs.append(image.resize((thumb_width, height), Image.Resampling.LANCZOS))
        rows.append((code, thumbs))

    if not rows:
        return

    width = padding * 4 + thumb_width * max(len(row[1]) for row in rows)
    height = padding * (len(rows) + 1) + sum(row[1][0].height for row in rows)
    sheet = Image.new("RGB", (width, height), (245, 247, 250))
    draw = ImageDraw.Draw(sheet)
    y = padding
    for code, thumbs in rows:
        x = padding
        draw.text((x, y - 18), code, fill=(30, 40, 55))
        for thumb in thumbs:
            sheet.paste(thumb, (x, y))
            x += thumb_width + padding
        y += thumbs[0].height + padding
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, quality=92)


def main() -> None:
    args = parse_args()
    config_path = Path(args.config).expanduser().resolve()
    config_dir = config_path.parent
    config = json.loads(config_path.read_text(encoding="utf-8"))
    canvas = Canvas(
        width=int(config.get("canvas", {}).get("width", 1290)),
        height=int(config.get("canvas", {}).get("height", 2796)),
    )
    source_dir = resolve_path(config_dir, config.get("source_dir")) or config_dir / "source"
    output_dir = resolve_path(config_dir, config.get("output_dir")) or config_dir
    zip_path = resolve_path(config_dir, config.get("zip_path"))
    y_shift = int(config.get("y_shift", 0))
    badge = config.get("badge", "")
    outputs: list[Path] = []
    outputs_by_lang: dict[str, list[Path]] = {}

    for language in config["languages"]:
        code = language["code"]
        outputs_by_lang[code] = []
        for item in language["items"]:
            output = render_item(
                canvas=canvas,
                config_dir=config_dir,
                source_dir=source_dir,
                output_dir=output_dir,
                language=language,
                item=item,
                y_shift=y_shift,
                badge=badge,
            )
            outputs.append(output)
            outputs_by_lang[code].append(output)

    if zip_path:
        write_zip(zip_path, outputs, output_dir)
    if args.contact_sheet:
        write_contact_sheet(Path(args.contact_sheet).expanduser().resolve(), outputs_by_lang)

    print(f"Rendered {len(outputs)} preview image(s).")
    if zip_path:
        print(f"Wrote {zip_path}")


if __name__ == "__main__":
    main()
