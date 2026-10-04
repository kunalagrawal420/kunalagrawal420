import json
from datetime import date

data = json.load(open("data/contributions.json"))
days = data["days"]

CELL, GAP = 12, 3
PITCH = CELL + GAP
PAD_X, PAD_TOP = 24, 56
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

first = date.fromisoformat(days[0]["date"])
first_sunday_offset = (first.weekday() + 1) % 7

cells = []
max_col = 0
for d in days:
    dt = date.fromisoformat(d["date"])
    idx = (dt - first).days + first_sunday_offset
    col, row = idx // 7, idx % 7
    max_col = max(max_col, col)
    delay = (col + row) * 0.025
    cells.append(
        f'<rect class="c" x="{PAD_X + col * PITCH}" y="{PAD_TOP + row * PITCH}" '
        f'width="{CELL}" height="{CELL}" rx="3" fill="{PALETTE[d["level"]]}" '
        f'style="animation-delay:{delay:.3f}s"/>'
    )

cols = max_col + 1
W = PAD_X * 2 + cols * PITCH
H = PAD_TOP + 7 * PITCH + 52

legend_x = W - PAD_X - 5 * PITCH - 70
legend = "".join(
    f'<rect x="{legend_x + 34 + i * PITCH}" y="{H - 34}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>'
    for i, c in enumerate(PALETTE)
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  .c {{ opacity: 0; animation: slide .5s ease-out forwards; }}
  @keyframes slide {{
    from {{ opacity: 0; transform: translateY(-8px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
  }}
</style>
<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>
<circle cx="24" cy="22" r="6" fill="#ff5f56"/>
<circle cx="44" cy="22" r="6" fill="#ffbd2e"/>
<circle cx="64" cy="22" r="6" fill="#27c93f"/>
<text x="{W // 2}" y="27" fill="#8b949e" font-size="13" text-anchor="middle">{data["username"]} -- contributions</text>
{"".join(cells)}
<text x="{PAD_X}" y="{H - 24}" fill="#c9d1d9" font-size="13">{data["total"]:,} contributions in the last year  |  streak {data["current_streak"]}d  |  longest {data["longest_streak"]}d</text>
<text x="{legend_x}" y="{H - 24}" fill="#8b949e" font-size="11">Less</text>
{legend}
<text x="{legend_x + 40 + 5 * PITCH}" y="{H - 24}" fill="#8b949e" font-size="11">More</text>
</svg>'''

open("contrib-heatmap.svg", "w").write(svg)
print(f"wrote contrib-heatmap.svg ({W}x{H})")
