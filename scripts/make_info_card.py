import os
import textwrap
from pathlib import Path

NOW = "IT Student & developer"
PREV = "Front-end & full-stack projects"
STACK = "JavaScript, PHP, Java, C#, SQL, HTML/CSS, Python, Unity, Git, Automation, Docker, API handling, API Integration and more"
HIGHLIGHTS = [
    "Automated scripts for emails scanning and customized orders",
    "Built event-booking system (PHP + MySQL)",
    "Library management app (JavaFX + MySQL)",
    "Prompt engineering and AI integration",
    "Website development and maintenance",
    "Terminal-based tools and scripts",
    "Node.js/Express web apps",
    "Unity 2D games",
]

WIDTH = 490
LINE_HEIGHT = 20
FONT_SIZE = 13
TITLE_BAR_H = 34
WRAP_CHARS = 52

BG = "#0d1117"
TITLE_BG = "#161b22"
LABEL_COLOR = "#58a6ff"
VALUE_COLOR = "#c9d1d9"
BORDER = "#30363d"

def escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def wrap(text, width=WRAP_CHARS):
    return textwrap.wrap(text, width=width) or [""]

def build_lines():
    lines = []
    lines.append(("Now", NOW))
    lines.append(("Prev", PREV))
    for j, part in enumerate(wrap(STACK)):
        lines.append(("Stack" if j == 0 else "", part))
    lines.append(("Highlights", ""))
    for h in HIGHLIGHTS:
        for j, part in enumerate(wrap(h)):
            lines.append(("", ("- " + part) if j == 0 else "  " + part))
    return lines

def build_svg(out_path="info-card.svg"):
    static = os.environ.get("STATIC") == "1"
    lines = build_lines()
    height = TITLE_BAR_H + len(lines) * LINE_HEIGHT + 20

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}">')
    parts.append(f'<rect width="100%" height="100%" fill="{BG}" stroke="{BORDER}" stroke-width="1" rx="6"/>')
    parts.append(f'<rect width="100%" height="{TITLE_BAR_H}" fill="{TITLE_BG}" rx="6"/>')
    parts.append(f'ircle cx="18" cy="{TITLE_BAR_H/2}" r="6" fill="#ff5f56"/>')
    parts.append(f'ircle cx="38" cy="{TITLE_BAR_H/2}" r="6" fill="#ffbd2e"/>')
    parts.append(f'ircle cx="58" cy="{TITLE_BAR_H/2}" r="6" fill="#27c93f"/>')
    parts.append(f'<text x="{WIDTH/2}" y="{TITLE_BAR_H/2+4}" text-anchor="middle" font-family="monospace" font-size="12" fill="{VALUE_COLOR}">neofetch</text>')
    parts.append(f'<style>.label {{ font-family: monospace; font-size: {FONT_SIZE}px; fill: {LABEL_COLOR}; font-weight: bold; }} .value {{ font-family: monospace; font-size: {FONT_SIZE}px; fill: {VALUE_COLOR}; }}</style>')

    y = TITLE_BAR_H + 22
    for i, (label, value) in enumerate(lines):
        delay = round(i * 0.06, 2)
        opacity_attr = "1" if static else "0"
        anim = "" if static else f'<animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="0.25s" fill="freeze"/>'
        x = 20

        text_content = ""
        if label:
            text_content += f'<tspan class="label">{escape(label)}:</tspan> '
        text_content += f'<tspan class="value">{escape(value)}</tspan>'

        parts.append(f'<text x="{x}" y="{y}" opacity="{opacity_attr}">{text_content}{anim}</text>')
        y += LINE_HEIGHT

    parts.append('</svg>')
    Path(out_path).write_text("\n".join(parts), encoding="utf-8")
    print(f"Saved {out_path}")

if __name__ == "__main__":
    build_svg()