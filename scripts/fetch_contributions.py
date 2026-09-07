import json
import re
import requests
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup

USERNAME = "trabelsimedaziz"
URL = f"https://github.com/users/{USERNAME}/contributions"

def parse_count_from_tooltip(text):
    if not text:
        return 0
    text = text.strip()
    if text.lower().startswith("no contributions"):
        return 0
    match = re.match(r"([\d,]+)\s+contribution", text)
    if match:
        return int(match.group(1).replace(",", ""))
    return 0

def fetch():
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    days = []
    cells = soup.select("td.ContributionCalendar-day")
    for cell in cells:
        date = cell.get("data-date")
        level = cell.get("data-level")
        cell_id = cell.get("id")
        if date is None:
            continue

        count = 0
        if cell_id:
            tooltip = soup.find("tool-tip", attrs={"for": cell_id})
            if tooltip:
                count = parse_count_from_tooltip(tooltip.get_text())

        days.append({
            "date": date,
            "level": int(level) if level is not None else 0,
            "count": count,
        })

    return days

def compute_stats(days):
    total = sum(d["count"] for d in days)
    current_streak = 0
    for d in reversed(days):
        if d["count"] > 0:
            current_streak += 1
        else:
            break

    longest_streak = 0
    running = 0
    for d in days:
        if d["count"] > 0:
            running += 1
            longest_streak = max(longest_streak, running)
        else:
            running = 0

    best_day = max(days, key=lambda d: d["count"], default=None)

    return {
        "total": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
    }

def main():
    days = fetch()
    days.sort(key=lambda d: d["date"])  # ensure chronological order
    stats = compute_stats(days)
    data = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "username": USERNAME,
        "days": days,
        "stats": stats,
    }
    Path("data/contributions.json").write_text(json.dumps(data, indent=2))
    print(f"Saved data/contributions.json — {stats['total']} contributions, current streak {stats['current_streak']}")
if __name__ == "__main__":
    main()