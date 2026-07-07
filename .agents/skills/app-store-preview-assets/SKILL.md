---
name: app-store-preview-assets
description: Generate localized App Store or Play Store preview images from mobile simulator screenshots. Use when creating, refreshing, or polishing store listing screenshots, especially when multiple languages, device frames, hero copy, source captures, preview ZIPs, or repeatable screenshot composition scripts are needed.
---

# App Store Preview Assets

## Workflow

1. Inspect the app's existing screenshot folder, source captures, supported locales, and store target size.
2. Capture fresh device screenshots when app UI changed. Keep raw captures under a `source/` folder and do not upscale low-resolution thumbnails.
3. Create a small JSON config for `scripts/render_store_previews.py`.
4. Run the renderer to create language-specific preview folders and a ZIP.
5. Verify every output image size, inspect a contact sheet, and rebuild after any layout feedback.

## Script

Use the bundled renderer:

```bash
python3 .agents/skills/app-store-preview-assets/scripts/render_store_previews.py \
  --config app-store-screenshots/config.json \
  --contact-sheet /tmp/store-previews.jpg
```

If the system Python lacks Pillow, use the Codex bundled Python when available:

```bash
/Users/eyedroot/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  .agents/skills/app-store-preview-assets/scripts/render_store_previews.py \
  --config app-store-screenshots/config.json
```

## Config Shape

Keep config app-specific and version it only if useful for repeated updates.

```json
{
  "canvas": { "width": 1290, "height": 2796 },
  "source_dir": "app-store-screenshots/source",
  "output_dir": "app-store-screenshots",
  "zip_path": "app-store-screenshots/store-previews.zip",
  "y_shift": 120,
  "badge": "Example App",
  "languages": [
    {
      "code": "en",
      "font": "/System/Library/Fonts/SFNS.ttf",
      "palette": {
        "top": "#F7FAFF",
        "bottom": "#E8F1FB",
        "text": "#121F32",
        "accent": "#1A70D2"
      },
      "items": [
        {
          "file": "01-focus.png",
          "title": "No ads.\nPure focus.",
          "subtitle": "Settle into the app without distractions.",
          "source": "en-main.png",
          "phone_width": 760,
          "phone_y": 560
        }
      ]
    }
  ]
}
```

## Composition Rules

- Prefer real simulator screenshots at device resolution as source images.
- Avoid rotating raster device frames unless the output is rendered at a much higher scale first; rotation often makes black bezels look jagged.
- Move the whole composition with `y_shift` when feedback says the layout feels top-heavy.
- Keep store copy short. Put product/category in the title and supporting value in the subtitle.
- Export language folders separately, such as `ko/`, `en/`, `ja/`, when stores require localized uploads.
- Recreate the ZIP after every image regeneration so it matches the folder output.

## Verification

Run these checks after rendering:

```bash
find app-store-screenshots -maxdepth 2 -type f -name '*.png' -print | sort
unzip -l app-store-screenshots/store-previews.zip
```

Also inspect the contact sheet visually for clipped text, jagged frames, off-center composition, and wrong-language UI.
