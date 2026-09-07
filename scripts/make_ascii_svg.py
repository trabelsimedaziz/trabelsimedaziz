from PIL import Image
from pathlib import Path

RAMP = " .·:;+=x*#%@■█"  # bright(sparse) -> dark(dense)
COLS = 100
ROWS = 53
FONT_SIZE = 8
CHAR_W = FONT_SIZE * 0.6
CHAR_H = FONT_SIZE * 1.0

def escape(s):
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))

def image_to_ascii_data(path):
    color_img = Image.open(path).convert("RGB").resize((COLS, ROWS))
    gray_img = color_img.convert("L")

    color_pixels = list(color_img.getdata())
    gray_pixels = list(gray_img.getdata())

    rows = []
    for r in range(ROWS):
        row_chars = []
        row_colors = []
        for c in range(COLS):
            idx = r * COLS + c
            brightness = gray_pixels[idx]
            char_idx = int((255 - brightness) / 255 * (len(RAMP) - 1))
            char = RAMP[char_idx]
            rgb = color_pixels[idx]
            row_chars.append(char)
            row_colors.append(rgb)
        rows.append((row_chars, row_colors))
    return rows

def build_svg(rows, out_path="avi-ascii.svg"):
    width = int(COLS * CHAR_W) + 20
    height = int(ROWS * CHAR_H) + 20

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    parts.append(f'<rect width="100%" height="100%" fill="#0d1117"/>')
    parts.append(f'<style>text {{ font-family: monospace; font-size: {FONT_SIZE}px; white-space: pre; }}</style>')

    for i, (chars, colors) in enumerate(rows):
        y = 15 + i * CHAR_H
        delay = round(i * 0.05, 2)

        # group consecutive same-color chars into tspans for compactness
        spans = []
        current_char = chars[0]
        current_color = colors[0]
        buffer = current_char
        for j in range(1, len(chars)):
            if colors[j] == current_color:
                buffer += chars[j]
            else:
                spans.append((buffer, current_color))
                buffer = chars[j]
                current_color = colors[j]
        spans.append((buffer, current_color))

        tspan_str = ""
        for text, (r, g, b) in spans:
            hexcolor = f"#{r:02x}{g:02x}{b:02x}"
            tspan_str += f'<tspan fill="{hexcolor}">{escape(text)}</tspan>'

        parts.append(
            f'<text x="10" y="{y}" opacity="0">{tspan_str}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="0.3s" fill="freeze"/>'
            f'</text>'
        )

    parts.append('</svg>')
    Path(out_path).write_text("\n".join(parts), encoding="utf-8")
    print(f"Saved {out_path}")

if __name__ == "__main__":
    rows = image_to_ascii_data("source-prepped.png")
    build_svg(rows)