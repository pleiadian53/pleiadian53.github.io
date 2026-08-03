"""Crop-formation SVG used as a CSS mask (white = pattern, transparent = ground).

After the Zeals Knoll formation near Mere, Wiltshire, 5 July 2026 — catalogued by
Temporary Temples as "free standing bubbles in a flower-like design". Original
geometry, not a traced image: eight-fold rotational symmetry, bubbles that never
touch, radii grading down toward the rim.

Fully deterministic — exact symmetry is the point. A real formation reads as
designed because it is precise, so nothing here is randomised.
"""
import math
from pathlib import Path

W = H = 640
CX = CY = 320
FOLD = 8
STEP = 360 / FOLD

ring, solid, tram = [], [], []

def at(angle_deg, dist, r, kind):
    a = math.radians(angle_deg)
    x, y = CX + math.cos(a) * dist, CY + math.sin(a) * dist
    (solid if kind == "solid" else ring).append((x, y, r))

# tramlines: the tractor tracks every formation is laid across
for i in range(11):
    y = 24 + i * 60
    tram.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#fff" '
                f'stroke-width="1.3" opacity="0.26"/>')

# centre: a ringed circle, the recurring Wiltshire motif
ring.append((CX, CY, 30)); solid.append((CX, CY, 12))

# eight primary arms — bubbles grading down and out
ARM = [(58, 15), (96, 19), (139, 16), (179, 12.5), (216, 9.5), (250, 7), (280, 5)]
# eight secondary arms, offset half a step, shorter and finer
MID = [(78, 10), (118, 12), (157, 9.5), (195, 7), (231, 5.5)]

for k in range(FOLD):
    base = k * STEP
    for i, (dist, r) in enumerate(ARM):
        at(base, dist, r, "ring" if i % 2 == 0 else "solid")
    for dist, r in MID:
        at(base + STEP / 2, dist, r, "solid")

# outer boundary, held off the bubbles so nothing touches
ring.append((CX, CY, 302))

parts = list(tram)
for x, y, r in ring:
    parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="none" stroke="#fff" '
                 f'stroke-width="{1.6 if r > 12 else 1.1}" opacity="0.66"/>')
for x, y, r in solid:
    parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="#fff" opacity="0.30"/>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
       + "".join(parts) + '</svg>')

out = Path.home() / "work/pleiadian53.github.io/assets/crop-field.svg"
out.write_text(svg)
print(f"{out}\n  bubbles={len(ring)+len(solid)}  {FOLD}-fold  {len(svg)/1024:.1f} KB")
