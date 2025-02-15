from PIL import Image, ImageDraw, ImageFont, ImageColor
import os

def apply_text_watermark(image_path, config, image = None):
    try:
        if image is None:
            img = Image.open(image_path).convert("RGBA")  # RGBA for transparency
        
        else:
            # img = Image.open(image_path).convert("RGBA")  # RGBA for transparency
            draw = ImageDraw.Draw(img)

        text = config.get("text_watermark", "")
        font_size = config.get("font_size", 24)
        color = config.get("text_color", (255, 255, 255, 255))  # Default white
        # Convert color if it's in [0-1] range
        if all(0 <= c <= 1 for c in color):
            color = tuple(int(c * 255) for c in color)

        font_path = "arial.ttf"  # Replace with your font path or a default font
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            print("Font not found. Using default font.")
            font = ImageFont.load_default()

        # Calculate text size and position (example: centered)
        text_width, text_height = draw.textsize(text, font=font)
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2

        draw.text((x, y), text, fill=color, font=font)

        return img

    except FileNotFoundError:
        print(f"Image not found: {image_path}")
        return None
    except Exception as e:
        print(f"Error applying text watermark: {e}")
        return None
    


def apply_logo_watermark(image_path, config, image = None):
    try:

        if image is None:
            img = Image.open(image_path).convert("RGBA")
        else:
            img = image

        # img = Image.open(image_path).convert("RGBA")
        logo_path = config.get("logo_path")  # Path to the logo image
        opacity = config.get("logo_opacity", 1.0)

        if not logo_path or not os.path.exists(logo_path):
            print("Logo path not found or invalid.")
            return img # Return the image without logo

        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize((100,100)) #Example resize, make it dynamic later

        # Apply opacity
        logo.putalpha(int(255 * opacity))

        # Calculate position (example: bottom right)
        x = img.width - logo.width - 10
        y = img.height - logo.height - 10

        img.paste(logo, (x, y), logo) # Use logo as mask to preserve transparency

        return img

    except FileNotFoundError:
        print(f"Image or logo not found: {image_path} or {logo_path}")
        return None
    except Exception as e:
        print(f"Error applying logo watermark: {e}")
        return None