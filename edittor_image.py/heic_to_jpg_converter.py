import os
import imghdr
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()  # Adds HEIC/HEIF support to PIL.Image.open

IMAGE_FOLDER = r"C:/Users/pc/Desktop/Pro_Jets/images_20th_april"

def convert_fake_jpegs(folder_path):
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        if not filename.lower().endswith(('.jpeg', '.jpg')):
            continue

        actual_format = imghdr.what(filepath)

        if actual_format != 'jpeg':
            print(f"[!] {filename} claims to be JPEG but is actually: {actual_format}")

            try:
                image = Image.open(filepath)
                new_filename = filename.rsplit('.', 1)[0] + "_converted.jpg"
                new_path = os.path.join(folder_path, new_filename)
                image.save(new_path, "JPEG")
                print(f"[✓] Converted and saved as: {new_filename}")
            except Exception as e:
                print(f"[x] Failed to convert {filename}: {e}")
        else:
            print(f"[✓] {filename} is a proper JPEG.")

if __name__ == "__main__":
    convert_fake_jpegs(IMAGE_FOLDER)
