import os
import sys
from PIL import Image, ImageDraw, ImageFont
from rembg import remove
import argparse

# ──────────────────────────────────────────
#  SETUP FOLDERS
# ──────────────────────────────────────────

INPUT_FOLDER  = "input"
OUTPUT_FOLDER = "output"

def setup_folders():
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    print("✅ Folders ready!")

# ──────────────────────────────────────────
#  HELPER - GET IMAGES
# ──────────────────────────────────────────

def get_images(folder):
    """Get all images from a folder."""
    supported = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")
    images = [
        f for f in os.listdir(folder)
        if f.lower().endswith(supported)
    ]
    if not images:
        print("❌ No images found in input folder!")
        sys.exit()
    return images

# ──────────────────────────────────────────
#  1. RESIZE IMAGES IN BULK
# ──────────────────────────────────────────

def resize_images(width, height):
    """
    Resize all images in the input folder.
    Args:
        width  (int): Target width in pixels
        height (int): Target height in pixels
    """
    print(f"\n🔄 Resizing images to {width}x{height}...")
    images = get_images(INPUT_FOLDER)

    save_folder = os.path.join(OUTPUT_FOLDER, "resized")
    os.makedirs(save_folder, exist_ok=True)

    for filename in images:
        try:
            img_path = os.path.join(INPUT_FOLDER, filename)
            img = Image.open(img_path)

            resized = img.resize((width, height), Image.LANCZOS)

            save_path = os.path.join(save_folder, filename)
            resized.save(save_path)

            print(f"  ✅ Resized: {filename} → {width}x{height}")

        except Exception as e:
            print(f"  ❌ Error resizing {filename}: {e}")

    print(f"\n🎉 Done! Resized images saved to: {save_folder}")

# ──────────────────────────────────────────
#  2. ADD WATERMARK TO PHOTOS
# ──────────────────────────────────────────

def add_watermark(watermark_text=None, watermark_image=None, opacity=128, position="bottom-right"):
    """
    Add text or image watermark to all photos.
    Args:
        watermark_text  (str)  : Text to use as watermark
        watermark_image (str)  : Path to watermark image file
        opacity         (int)  : 0 (invisible) to 255 (solid)
        position        (str)  : top-left, top-right, bottom-left, bottom-right, center
    """
    print(f"\n💧 Adding watermarks...")
    images = get_images(INPUT_FOLDER)

    save_folder = os.path.join(OUTPUT_FOLDER, "watermarked")
    os.makedirs(save_folder, exist_ok=True)

    for filename in images:
        try:
            img_path = os.path.join(INPUT_FOLDER, filename)
            img = Image.open(img_path).convert("RGBA")
            img_w, img_h = img.size

            # ── TEXT WATERMARK ──
            if watermark_text:
                overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(overlay)

                # Try to load a font, fallback to default
                try:
                    font = ImageFont.truetype("arial.ttf", size=max(30, img_w // 20))
                except:
                    font = ImageFont.load_default()

                # Get text size
                bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]

                # Calculate position
                x, y = get_position(position, img_w, img_h, text_w, text_h, padding=20)

                # Draw text with shadow
                draw.text((x + 2, y + 2), watermark_text, font=font, fill=(0, 0, 0, opacity))
                draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, opacity))

                watermarked = Image.alpha_composite(img, overlay)

            # ── IMAGE WATERMARK ──
            elif watermark_image and os.path.exists(watermark_image):
                wm = Image.open(watermark_image).convert("RGBA")

                # Scale watermark to 20% of image width
                wm_ratio = 0.20
                wm_w = int(img_w * wm_ratio)
                wm_h = int(wm.height * (wm_w / wm.width))
                wm = wm.resize((wm_w, wm_h), Image.LANCZOS)

                # Apply opacity
                r, g, b, a = wm.split()
                a = a.point(lambda p: p * opacity // 255)
                wm.putalpha(a)

                # Calculate position
                x, y = get_position(position, img_w, img_h, wm_w, wm_h, padding=20)

                watermarked = img.copy()
                watermarked.paste(wm, (x, y), wm)

            else:
                print("  ⚠️ No watermark text or image provided!")
                return

            # Convert back to RGB if saving as JPG
            name, ext = os.path.splitext(filename)
            if ext.lower() in (".jpg", ".jpeg"):
                watermarked = watermarked.convert("RGB")

            save_path = os.path.join(save_folder, filename)
            watermarked.save(save_path)

            print(f"  ✅ Watermarked: {filename}")

        except Exception as e:
            print(f"  ❌ Error watermarking {filename}: {e}")

    print(f"\n🎉 Done! Watermarked images saved to: {save_folder}")


def get_position(position, img_w, img_h, item_w, item_h, padding=20):
    """Calculate x, y coordinates based on position name."""
    positions = {
        "top-left"     : (padding, padding),
        "top-right"    : (img_w - item_w - padding, padding),
        "bottom-left"  : (padding, img_h - item_h - padding),
        "bottom-right" : (img_w - item_w - padding, img_h - item_h - padding),
        "center"       : ((img_w - item_w) // 2, (img_h - item_h) // 2),
    }
    return positions.get(position, positions["bottom-right"])

# ──────────────────────────────────────────
#  3. CONVERT IMAGE FORMATS
# ──────────────────────────────────────────

def convert_format(target_format):
    """
    Convert all images to a target format.
    Args:
        target_format (str): jpg, png, webp, bmp, gif
    """
    target_format = target_format.lower().strip(".")
    print(f"\n🔄 Converting images to .{target_format}...")

    images = get_images(INPUT_FOLDER)

    save_folder = os.path.join(OUTPUT_FOLDER, f"converted_{target_format}")
    os.makedirs(save_folder, exist_ok=True)

    format_map = {
        "jpg"  : "JPEG",
        "jpeg" : "JPEG",
        "png"  : "PNG",
        "webp" : "WEBP",
        "bmp"  : "BMP",
        "gif"  : "GIF",
    }

    pil_format = format_map.get(target_format)
    if not pil_format:
        print(f"❌ Unsupported format: {target_format}")
        print(f"   Supported: {list(format_map.keys())}")
        return

    for filename in images:
        try:
            img_path = os.path.join(INPUT_FOLDER, filename)
            img = Image.open(img_path)

            # Convert RGBA to RGB for JPG (JPG doesn't support transparency)
            if pil_format == "JPEG" and img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            name = os.path.splitext(filename)[0]
            new_filename = f"{name}.{target_format}"
            save_path = os.path.join(save_folder, new_filename)

            img.save(save_path, pil_format)

            print(f"  ✅ Converted: {filename} → {new_filename}")

        except Exception as e:
            print(f"  ❌ Error converting {filename}: {e}")

    print(f"\n🎉 Done! Converted images saved to: {save_folder}")

# ──────────────────────────────────────────
#  4. REMOVE BACKGROUND
# ──────────────────────────────────────────

def remove_background():
    """
    Remove background from all images in input folder.
    Output images will be saved as PNG (supports transparency).
    """
    print(f"\n✂️  Removing backgrounds...")
    images = get_images(INPUT_FOLDER)

    save_folder = os.path.join(OUTPUT_FOLDER, "no_background")
    os.makedirs(save_folder, exist_ok=True)

    for filename in images:
        try:
            img_path = os.path.join(INPUT_FOLDER, filename)

            with open(img_path, "rb") as f:
                input_data = f.read()

            print(f"  🔄 Processing: {filename} (this may take a moment...)")
            output_data = remove(input_data)

            name = os.path.splitext(filename)[0]
            new_filename = f"{name}_no_bg.png"
            save_path = os.path.join(save_folder, new_filename)

            with open(save_path, "wb") as f:
                f.write(output_data)

            print(f"  ✅ Done: {filename} → {new_filename}")

        except Exception as e:
            print(f"  ❌ Error removing background from {filename}: {e}")

    print(f"\n🎉 Done! Images saved to: {save_folder}")

# ──────────────────────────────────────────
#  5. ALL IN ONE
# ──────────────────────────────────────────

def process_all(width, height, watermark_text, target_format):
    """Run all processing steps on images."""
    print("\n🚀 Running ALL processing steps...\n")
    resize_images(width, height)
    add_watermark(watermark_text=watermark_text)
    convert_format(target_format)
    remove_background()
    print("\n✅ All processing complete!")

# ──────────────────────────────────────────
#  MENU
# ──────────────────────────────────────────

def show_menu():
    print("""
╔══════════════════════════════════════╗
║       🖼  IMAGE PROCESSOR BOT        ║
╠══════════════════════════════════════╣
║  1. Resize Images                    ║
║  2. Add Watermark (Text)             ║
║  3. Add Watermark (Image)            ║
║  4. Convert Format                   ║
║  5. Remove Background                ║
║  6. Run ALL Steps                    ║
║  7. Exit                             ║
╚══════════════════════════════════════╝
    """)

# ──────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────

def main():
    setup_folders()

    while True:
        show_menu()
        choice = input("👉 Choose an option (1-7): ").strip()

        if choice == "1":
            w = int(input("   Enter width  (px): "))
            h = int(input("   Enter height (px): "))
            resize_images(w, h)

        elif choice == "2":
            text = input("   Enter watermark text: ")
            pos  = input("   Position (top-left / top-right / bottom-left / bottom-right / center): ").strip()
            op   = int(input("   Opacity (0-255, default 128): ") or 128)
            add_watermark(watermark_text=text, opacity=op, position=pos)

        elif choice == "3":
            wm_path = input("   Enter watermark image path: ").strip()
            pos     = input("   Position (top-left / top-right / bottom-left / bottom-right / center): ").strip()
            op      = int(input("   Opacity (0-255, default 128): ") or 128)
            add_watermark(watermark_image=wm_path, opacity=op, position=pos)

        elif choice == "4":
            fmt = input("   Enter target format (jpg / png / webp / bmp): ").strip()
            convert_format(fmt)

        elif choice == "5":
            remove_background()

        elif choice == "6":
            w    = int(input("   Enter resize width  (px): "))
            h    = int(input("   Enter resize height (px): "))
            text = input("   Enter watermark text: ")
            fmt  = input("   Enter target format (jpg / png / webp): ").strip()
            process_all(w, h, text, fmt)

        elif choice == "7":
            print("\n👋 Goodbye!")
            break

        else:
            print("❌ Invalid option! Please choose 1-7.")

if __name__ == "__main__":
    main()
