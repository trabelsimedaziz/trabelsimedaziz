import requests

USERNAME = "trabelsimedaziz"
URL = f"https://github.com/users/{USERNAME}/contributions"

resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
print("Status:", resp.status_code)
with open("debug_contributions.html", "w", encoding="utf-8") as f:
    f.write(resp.text)
print("Saved debug_contributions.html — length:", len(resp.text))