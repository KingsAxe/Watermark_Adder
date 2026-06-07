# Watermark_Adder

`Watermark_Adder` is a Kivy/KivyMD desktop app for applying text and logo watermarks to one or more images.

## Features

- Add text watermarks with configurable text, font size, color, and position.
- Add one or more logo watermarks and place them at common anchor points.
- Preview and save watermark settings through `config.json`.
- Export processed images into `processed_images/`.

## Project Structure

- `main.py` boots the KivyMD app and loads the screens.
- `screens/config.py` contains the main watermark workflow used by the UI.
- `utils/watermark.py` contains lower-level helper functions for text and logo watermarking.
- `kv/` contains the Kivy layout files.
- `processed_images/` stores the generated output images.
- `temp_logos/` stores copied logo assets selected in the app.

## Running The App

This repo already includes local virtual environments. If you want to run the app from the current workspace, use the environment that has the Kivy dependencies installed and start:

```powershell
python main.py
```

If `python` is not using the intended environment, activate the relevant environment first and then run `python main.py`.

## Watermarking Code

The main implementation path is:

- `screens/config.py`
  - `apply_watermark()` opens each selected image, calculates text and logo positions, draws the text watermark, pastes the selected logos, and saves the result to `processed_images/`.

Supporting helper functions live in:

- `utils/watermark.py`
  - `apply_text_watermark()`
  - `apply_logo_watermark()`

## Output

Processed files are written to:

```text
processed_images/
```

JPEG outputs are converted to RGB before saving for compatibility.
