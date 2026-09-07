import json
from pathlib import Path
from datetime import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
BOX_SIZE = 11
BOX_GAP = 3
CELL = BOX_SIZE + BOX_GAP
LEFT_PAD = 30
TOP_PAD = 30
LEGEND_H = 30

MONTH_LABELS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
DAY_LABELS = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]

def load_data(path="data/contributions.json"):
    return json.loads(Path(path).read_text())

def build_weeks(days):
    days_by_date = {d["date"]: d for d in days}
    sorted_dates = sorted(days_by_date.keys())
    if not sorted_dates:
        return []

    first_date = datetime.strptime(sorted_dates[0], "%Y-%m-%d")
    # find the Sunday on/before first_date to align columns
    offset = (first_date.weekday() + 1) % 7  # Python Monday=0; GitHub week starts Sunday
    weeks = []
    current_week = [None] * 7

    for date_str in sorted_dates:
        d = days_by_date[date_str]
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        weekday = (dt.weekday() + 1) % 7  # 0=Sunday
        if weekday == 0 and any(current_week):
            weeks.append(current_week)
            current_week = [None] * 7
        current_week[weekday] = d

    if any(current_week):
        weeks.append(current_week)

    return weeks

def build_svg(data, out_path="contrib-heatmap.svg"):
    days = data["days"]
    stats = data["stats"]
    weeks = build_weeks(days)

    n_weeks = len(weeks)
    width = LEFT_PAD + n_weeks * CELL + 20
    height = TOP_PAD + 7 * CELL + LEGEND_H + 20

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    parts.append(f'<rect width="100%" height="100%" fill="#0d1117"/>')
    parts.append(f'<style>@keyframes reveal {{ from {{ opacity: 0; transform: translate(-6px,-6px); }} to {{ opacity: 1; transform: translate(0,0); }} }} .box {{ animation: reveal 0.3s ease-out forwards; opacity: 0; }} text {{ font-family: monospace; fill: #8b949e; }}</style>')

    # month labels (approximate, based on first day of each week)
    last_month = None
    for wi, week in enumerate(weeks):
        first_valid = next((d for d in week if d), None)
        if not first_valid:
            continue
        dt = datetime.strptime(first_valid["date"], "%Y-%m-%d")
        month = dt.month
        if month != last_month:
            x = LEFT_PAD + wi * CELL
            parts.append(f'<text x="{x}" y="{TOP_PAD - 12}" font-size="10">{MONTH_LABELS[month-1]}</text>')
            last_month = month

    # day-of-week labels (Mon, Wed, Fri)
    for di, label in enumerate(DAY_LABELS):
        if di % 2 == 1:
            y = TOP_PAD + di * CELL + BOX_SIZE
            parts.append(f'<text x="0" y="{y}" font-size="10">{label}</text>')

    # boxes
    delay_step = 0.01
    idx = 0
    for wi, week in enumerate(weeks):
        for di, d in enumerate(week):
            x = LEFT_PAD + wi * CELL
            y = TOP_PAD + di * CELL
            if d is None:
                color = PALETTE[0]
            else:
                level = min(d["level"], len(PALETTE) - 1)
                color = PALETTE[level]
            delay = round(idx * delay_step, 3)
            parts.append(
                f'<rect class="box" x="{x}" y="{y}" width="{BOX_SIZE}" height="{BOX_SIZE}" rx="2" fill="{color}" style="animation-delay:{delay}s"/>'
            )
            idx += 1

    # legend
    legend_y = TOP_PAD + 7 * CELL + 20
    parts.append(f'<text x="{LEFT_PAD}" y="{legend_y+8}" font-size="10">Less</text>')
    lx = LEFT_PAD + 35
    for color in PALETTE:
        parts.append(f'<rect x="{lx}" y="{legend_y}" width="{BOX_SIZE}" height="{BOX_SIZE}" rx="2" fill="{color}"/>')
        lx += CELL
    parts.append(f'<text x="{lx+5}" y="{legend_y+8}" font-size="10">More</text>')

    footer = f"{stats['total']:,} contributions in the last year"
    parts.append(f'<text x="{width - 20}" y="{legend_y+8}" font-size="10" text-anchor="end">{footer}</text>')

    parts.append('</svg>')
    Path(out_path).write_text("\n".join(parts), encoding="utf-8")
    print(f"Saved {out_path}")

if __name__ == "__main__":
    data = load_data()
    build_svg(data)