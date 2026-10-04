from xml.sax.saxutils import escape

# ---- EDIT THIS BLOCK: it's the only part you need to change ----
HANDLE = "kunal@github"
ROWS = [
    ("Name",     "Kunal Agrawal"),
    ("Now",      "Backend developer moving into AI / LLM engineering"),
    ("Stack",    "Java, Spring Boot, REST APIs, PostgreSQL"),
    ("Infra",    "Docker, AWS"),
    ("Frontend", "React, TypeScript"),
    ("Learning", "Building real LLM projects, not just tutorials"),
]
WIDTH = 860          # full width for now; we'll shrink it when the portrait goes beside it
# -----------------------------------------------------------------

LINE = 26
PAD_X, PAD_TOP = 24, 64
KEY_X, VAL_X = PAD_X, PAD_X + 110
n_lines = len(ROWS) + 2          # +2 for the handle line and the divider line
H = PAD_TOP + n_lines * LINE + 20

out = []
def text(y, i, parts):
    # i is the line number: it drives the animation delay so lines "print" in order
    spans = "".join(f'<tspan x="{x}" fill="{fill}"{w}>{escape(s)}</tspan>' for x, fill, w, s in parts)
    out.append(f'<text class="l" y="{y}" style="animation-delay:{0.15 + i * 0.18:.2f}s">{spans}</text>')

y = PAD_TOP
text(y, 0, [(KEY_X, "#39d353", ' font-weight="bold"', HANDLE)])
y += LINE
text(y, 1, [(KEY_X, "#484f58", "", "-" * len(HANDLE))])
for i, (k, v) in enumerate(ROWS, start=2):
    y += LINE
    text(y, i, [(KEY_X, "#58a6ff", ' font-weight="bold"', k), (VAL_X, "#c9d1d9", "", v)])

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{H}" viewBox="0 0 {WIDTH} {H}">
<style>
  text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 14px; }}
  .l {{ opacity: 0; animation: in .4s ease-out forwards; }}
  @keyframes in {{
    from {{ opacity: 0; transform: translateX(-10px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
  }}
</style>
<rect width="{WIDTH}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>
<circle cx="24" cy="22" r="6" fill="#ff5f56"/>
<circle cx="44" cy="22" r="6" fill="#ffbd2e"/>
<circle cx="64" cy="22" r="6" fill="#27c93f"/>
<text x="{WIDTH // 2}" y="27" fill="#8b949e" text-anchor="middle" style="font-size:13px">whoami</text>
{"".join(out)}
</svg>'''

open("info-card.svg", "w").write(svg)
print(f"wrote info-card.svg ({WIDTH}x{H})")
