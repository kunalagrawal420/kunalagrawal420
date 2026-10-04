import json, re, sys, os
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup

username = sys.argv[1] if len(sys.argv) > 1 else os.environ["GH_USER"]

html = requests.get(
    f"https://github.com/users/{username}/contributions",
    headers={"User-Agent": "profile-readme-bot"},
    timeout=30,
).text
soup = BeautifulSoup(html, "html.parser")

tips = {t["for"]: t.get_text() for t in soup.find_all("tool-tip")}

days = []
for cell in soup.select("td.ContributionCalendar-day[data-date]"):
    m = re.match(r"(\d+)", tips.get(cell.get("id"), ""))
    days.append({
        "date": cell["data-date"],
        "level": int(cell["data-level"]),
        "count": int(m.group(1)) if m else 0,
    })

if not days:
    sys.exit("No contribution cells parsed - GitHub markup may have changed.")

days.sort(key=lambda d: d["date"])

longest = run = 0
for d in days:
    run = run + 1 if d["count"] > 0 else 0
    longest = max(longest, run)

current, today = 0, date.today()
by_date = {d["date"]: d["count"] for d in days}
cursor = today
if by_date.get(cursor.isoformat(), 0) == 0:
    cursor -= timedelta(days=1)
while by_date.get(cursor.isoformat(), 0) > 0:
    current += 1
    cursor -= timedelta(days=1)

out = {
    "username": username,
    "total": sum(d["count"] for d in days),
    "current_streak": current,
    "longest_streak": longest,
    "days": days,
}
json.dump(out, open("data/contributions.json", "w"), indent=2)
print(f"{out['total']} contributions, streak {current}, longest {longest}")
