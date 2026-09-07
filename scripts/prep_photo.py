import sys
from pathlib import Path
from PIL import Image
from rembg import remove

def prep(input_path, output_path="source-prepped.png"):
    input_bytes = Path(input_path).read_bytes()

    # Remove background
    result_bytes = remove(input_bytes)
    img = Image.open(__import__("io").BytesIO(result_bytes)).convert("RGBA")

    # Composite onto white background
    white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    white_bg.alpha_composite(img)
    rgb_img = white_bg.convert("RGB")

    # Simple grayscale conversion — no aggressive contrast boosting
    gray_img = rgb_img.convert("L")

    # Optional: mild contrast enhancement only, using PIL (gentler than CLAHE)
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(gray_img)
    gray_img = enhancer.enhance(1.15)  # very mild boost, 1.0 = no change

    rgb_img.save(output_path)
    print(f"Saved {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <input_photo>")
        sys.exit(1)
    prep(sys.argv[1])