"""Generate the crop circle SVGs used as background masks.

Masking reads only the ALPHA channel (the stylesheet pins `mask-mode: alpha`), so
INK below is free. It is a visible blue rather than white purely so the files
preview in an image viewer instead of appearing blank on white. Changing INK does
not change how the page renders; changing an `opacity` does.

Deterministic by design -- these are precise figures, so nothing is randomised.
"""
import math
from pathlib import Path

INK = "#1f5fa8"          # preview colour only -- masking ignores hue, see docstring
OUT = Path(__file__).resolve().parent.parent / "assets"


def circle(x, y, r, fill=False, w=1.2, op=None):
    if fill:
        return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{INK}" opacity="{op or 0.30}"/>'
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="none" stroke="{INK}" '
            f'stroke-width="{w}" opacity="{op or 0.66}"/>')


def tramlines(w, h, gap=60, start=24):
    return [f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{INK}" stroke-width="1.3" '
            f'opacity="0.24"/>' for y in range(start, h, gap)]


def wrap(parts, w, h, name):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
           f'height="{h}">' + "".join(parts) + '</svg>')
    p = OUT / name
    p.write_text(svg)
    print(f"  {name:24s} {len(svg)/1024:5.1f} KB")


def cosmos():
    W = H = 640
    CX = CY = 320
    FOLD, STEP = 8, 45
    parts = tramlines(W, H)
    ring, solid = [], []

    def at(deg, dist, r, kind):
        a = math.radians(deg)
        (solid if kind == "solid" else ring).append(
            (CX + math.cos(a) * dist, CY + math.sin(a) * dist, r))

    ring.append((CX, CY, 30)); solid.append((CX, CY, 12))
    ARM = [(58, 15), (96, 19), (139, 16), (179, 12.5), (216, 9.5), (250, 7), (280, 5)]
    MID = [(78, 10), (118, 12), (157, 9.5), (195, 7), (231, 5.5)]
    for k in range(FOLD):
        base = k * STEP
        for i, (d, r) in enumerate(ARM):
            at(base, d, r, "ring" if i % 2 == 0 else "solid")
        for d, r in MID:
            at(base + STEP / 2, d, r, "solid")
    ring.append((CX, CY, 302))
    parts += [circle(x, y, r, w=1.6 if r > 12 else 1.1) for x, y, r in ring]
    parts += [circle(x, y, r, fill=True) for x, y, r in solid]
    wrap(parts, W, H, "crop-cosmos.svg")


def moons13():
    W = H = 640
    CX = CY = 320
    N, STEP_K, R = 13, 5, 250          # {13/5} star polygon
    parts = tramlines(W, H)

    pts = [(CX + math.cos(math.radians(-90 + i * 360 / N)) * R,
            CY + math.sin(math.radians(-90 + i * 360 / N)) * R) for i in range(N)]
    order, i = [], 0
    for _ in range(N):
        order.append(pts[i]); i = (i + STEP_K) % N
    d = "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in order) + "Z"
    parts.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.5" opacity="0.72"/>')

    parts += [circle(CX, CY, R), circle(CX, CY, R + 26, w=1.5), circle(CX, CY, 52)]
    parts += [circle(x, y, 7, fill=True) for x, y in pts]      # a point marked at each vertex

    # crescent moon nested at the centre: outer arc of R1, inner arc of R2 offset by dx
    R1, R2, dx = 44.0, 40.0, 17.0
    a = (dx * dx - R2 * R2 + R1 * R1) / (2 * dx)
    h = math.sqrt(max(R1 * R1 - a * a, 0.0))
    x1, y1 = CX + a, CY + h
    x2, y2 = CX + a, CY - h
    parts.append(
        f'<path d="M{x1:.2f} {y1:.2f} A{R1} {R1} 0 1 1 {x2:.2f} {y2:.2f} '
        f'A{R2} {R2} 0 1 0 {x1:.2f} {y1:.2f} Z" fill="{INK}" opacity="0.34"/>')
    wrap(parts, W, H, "crop-13moons.svg")


def trine():
    W = H = 560
    CX = CY = 280
    R = 236
    parts = tramlines(W, H, gap=56, start=22)
    parts += [circle(CX, CY, R, w=1.6), circle(CX, CY, R - 20, w=1.0, op=0.40),
              circle(CX, CY, 96), circle(CX, CY, 40, fill=True)]
    for turn, rr in ((-90, R - 20), (-30, R - 20), (-90, 96)):
        pts = [(CX + math.cos(math.radians(turn + i * 120)) * rr,
                CY + math.sin(math.radians(turn + i * 120)) * rr) for i in range(3)]
        d = "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z"
        parts.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.5" opacity="0.70"/>')
        for x, y in pts:
            parts += [circle(x, y, 26 if rr > 150 else 16),
                      circle(x, y, 12 if rr > 150 else 7, fill=True)]
    wrap(parts, W, H, "crop-trine.svg")


def helix():
    W = H = 560
    CX = CY = 280
    TURNS, STEPS, RMAX = 2.3, 460, 244
    parts = tramlines(W, H, gap=56, start=22)
    for arm in (0.0, math.pi):
        pts = []
        for i in range(STEPS + 1):
            t = i / STEPS
            th = arm + t * TURNS * math.tau
            r = 26 + t * (RMAX - 26)
            pts.append((CX + math.cos(th) * r, CY + math.sin(th) * r))
        d = "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in pts)
        parts.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.7" opacity="0.72"/>')
        for i in range(3, STEPS, 38):                    # beads along each arm
            x, y = pts[i]
            parts.append(circle(x, y, 4.5 + 5.5 * (i / STEPS), fill=True))
    parts += [circle(CX, CY, 20, fill=True), circle(CX, CY, RMAX + 16, w=1.4, op=0.44)]
    wrap(parts, W, H, "crop-helix.svg")


def cipher():
    W, H = 1240, 260
    MY = 130
    parts = [f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{INK}" stroke-width="1.3" '
             f'opacity="0.22"/>' for y in (34, 96, 164, 226)]
    parts.append(f'<line x1="40" y1="{MY}" x2="{W-40}" y2="{MY}" stroke="{INK}" '
                 f'stroke-width="1.5" opacity="0.55"/>')

    def key(x, flip=1):
        r, stem = 26, 74
        g = [circle(x, MY, r, w=1.5), circle(x, MY, 12, fill=True)]
        x2 = x + flip * (r + stem)
        g.append(f'<line x1="{x + flip*r}" y1="{MY}" x2="{x2}" y2="{MY}" stroke="{INK}" '
                 f'stroke-width="2.4" opacity="0.62"/>')
        for off in (26, 46, 66):                          # the teeth
            tx = x + flip * (r + off)
            g.append(f'<line x1="{tx}" y1="{MY}" x2="{tx}" y2="{MY + 20}" stroke="{INK}" '
                     f'stroke-width="2.0" opacity="0.58"/>')
        return g

    GLYPHS = [(96, "ringed", 34), (196, "solid", 18), (268, "rings3", 40),
              (392, "key+", 0),  (600, "solid", 26), (676, "ringed", 30),
              (772, "rings3", 22), (900, "key-", 0),  (1088, "ringed", 38),
              (1176, "solid", 14)]
    for x, kind, r in GLYPHS:
        if kind == "ringed":
            parts += [circle(x, MY, r), circle(x, MY, r * 0.45, fill=True)]
        elif kind == "solid":
            parts.append(circle(x, MY, r, fill=True, op=0.34))
        elif kind == "rings3":
            parts += [circle(x, MY, r), circle(x, MY, r * 0.68, w=1.0, op=0.5),
                      circle(x, MY, r * 0.34, w=1.0, op=0.5)]
        elif kind.startswith("key"):
            parts += key(x, 1 if kind.endswith("+") else -1)
    wrap(parts, W, H, "crop-cipher.svg")


if __name__ == "__main__":
    print("formations:")
    cosmos(); moons13(); trine(); helix(); cipher()
