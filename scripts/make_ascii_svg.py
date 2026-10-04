import numpy as np
from PIL import Image
from xml.sax.saxutils import escape

COLS = 100
CW, LH = 4.8, 9.6                      # char width / line height: monospace chars are ~2x taller than wide
RAMP = " .:-=+*#%@"                    # dark/blank -> bright/dense (leading space = background)
FILL = "#c9d1d9"                       # one flat color: rainbow ASCII looks like static

img = Image.open("source-prepped.png").convert("L")
rows = int(img.height / img.width * COLS * (CW / LH))   # correct for tall characters
px = np.array(img.resize((COLS, rows), Image.LANCZOS))

W, H = COLS * CW, rows * LH
clips, texts = [], []
for r in range(rows):
    line = "".join(RAMP[int(v) * len(RAMP) // 256] for v in px[r])
    if not line.strip():
        continue                       # skip blank rows entirely
    delay = 0.1 + r * 0.045
    # Each row is revealed by a clip rectangle whose width grows 0 -> W (SMIL runs inside <img> on GitHub).
    clips.append(
        f'<clipPath id="c{r}"><rect x="0" y="{r * LH:.1f}" width="0" height="{LH:.1f}">'
        f'<animate attributeName="width" from="0" to="{W:.0f}" begin="{delay:.2f}s" dur="0.5s" fill="freeze"/>'
        f'</rect></clipPath>'
    )
    # textLength pins every row to the exact same width even if the viewer's font differs.
    texts.append(
        f'<text x="0" y="{(r + 0.8) * LH:.1f}" clip-path="url(#c{r})" textLength="{W:.0f}" '
        f'lengthAdjust="spacing" xml:space="preserve">{escape(line)}</text>'
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}">
<style>text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 8px; fill: {FILL}; }}</style>
<rect width="{W:.0f}" height="{H:.0f}" rx="10" fill="#0d1117" stroke="#30363d"/>
<defs>{"".join(clips)}</defs>
{"".join(texts)}
</svg>'''

open("ascii-portrait.svg", "w").write(svg)
print(f"wrote ascii-portrait.svg ({W:.0f}x{H:.0f}, {rows} rows)")
