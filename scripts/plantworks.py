#!/usr/bin/env python3
"""Plantworks: each project's plant growing out of a factory (plant + plant).

The living plant is the drawing from plants.py (without its ground line),
scaled onto the roof of a factory module whose size follows maturity:
1 lab capsule, 2 module, 3 greenhouse, 4 sawtooth-roof factory with a chimney
that puffs leaves, 5 big plant-factory with pipes, a gear and a conveyor.

Run: python3 scripts/plantworks.py  -> _includes/plantworks/<id>.svg
Reads maturity per plant from _data/projects.yml.
"""
import os, sys, math, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plants as P
P.ground = lambda *a, **k: ""          # the factory is the ground now
from plants import n, leaf, circ, stroke, shape, ell, LEAF, DEEP, PALE, GOLD, FRUIT

WALL, LINE, ROOF, DIM = "var(--wash)", "var(--soft)", "var(--rule)", "var(--dim)"
GLASS, LIT = "var(--p-glass)", "var(--p-lit)"

def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" fill="{fill}"{extra}/>'
def box(x, y, w, h, fill=WALL, sw=.8):
    return rect(x, y, w, h, fill, f' stroke="{LINE}" stroke-width="{n(sw)}" stroke-linejoin="round"')
def windows(x, y, cols, rows, dx, dy=0, w=2.2, h=2.2, fill=LIT):
    return [rect(x + c * dx, y + r * dy, w, h, fill) for r in range(rows) for c in range(cols)]
def gear(cx, cy, r, teeth, fill=DIM):
    out = [circ(cx, cy, r, fill)]
    for i in range(teeth):
        a = i * 360 / teeth
        out.append(rect(cx - .7, cy - r - 1.2, 1.4, 1.6, fill, f' transform="rotate({n(a)} {n(cx)} {n(cy)})"'))
    out.append(circ(cx, cy, r * .42, WALL))
    return out
def leaf_puff(x, y, s=1):
    return [leaf(x, y, 3.2 * s, 1.5 * s, 35, PALE), leaf(x + 2.2 * s, y - 2.6 * s, 2.6 * s, 1.2 * s, -30, LEAF), leaf(x + .6 * s, y - 5 * s, 2 * s, 1 * s, 20, PALE)]
def sawtooth(x0, x1, base, h, teeth):
    w = (x1 - x0) / teeth
    d = f"M{n(x0)} {n(base)}"
    for i in range(teeth):
        a = x0 + i * w
        d += f"L{n(a)} {n(base - h)}L{n(a + w)} {n(base)}"
    out = [shape(d + "Z", ROOF, f' stroke="{LINE}" stroke-width=".8" stroke-linejoin="round"')]
    for i in range(teeth):  # glazing on each tooth's vertical face
        a = x0 + i * w
        out.append(stroke(f"M{n(a + .5)} {n(base - h + 1.2)}V{n(base - .6)}", GLASS, 1))
    return out

# base modules: (svg parts, plant anchor x, anchor y (roof top), plant scale)
def base(stage):
    g = stroke("M5 45.4H43", "var(--faint)", 1)
    if stage == 1:
        parts = [g, rect(14.5, 41.5, 19, 3.5, WALL, f' stroke="{LINE}" stroke-width=".8"'), circ(30.6, 43.25, .7, LIT), circ(28.4, 43.25, .7, GLASS)]
        return parts, 24, 41.5, .95
    if stage == 2:
        parts = [g, stroke("M30.5 37.5V31.5", DIM, .8), circ(30.5, 31, 1, LIT), box(14.5, 37.5, 19, 7.5), *windows(16.5, 40, 3, 1, 3.2), stroke("M33.5 41H37V45", DIM, 1.1), rect(36, 44.2, 2, 1, DIM)]
        return parts, 24, 37.5, .82
    if stage == 3:
        parts = [g, box(12, 36, 24, 9),
                 shape("M12 36L24 29.5L36 36Z", GLASS, f' stroke="{LINE}" stroke-width=".8" opacity=".55" stroke-linejoin="round"'),
                 stroke("M18 32.8V36M24 29.5V36M30 32.8V36", LINE, .5), *windows(14.5, 39.5, 5, 1, 4.2, 0, 2.2, 2.4)]
        return parts, 24, 34.5, .74
    if stage == 4:
        parts = [g, rect(32.5, 22, 3.2, 12, WALL, f' stroke="{LINE}" stroke-width=".8"'), rect(32.1, 21.2, 4, 1.4, DIM),
                 *leaf_puff(33.6, 19.6, .9),
                 box(9, 34, 30, 11), *sawtooth(9, 39, 34, 4, 3), *windows(11.5, 37.2, 6, 1, 4.4, 0, 2.4, 2.6),
                 rect(21.5, 41, 5, 4, DIM)]
        return parts, 17.5, 32.5, .62
    # stage 5
    parts = [g, rect(36, 17, 3.6, 15, WALL, f' stroke="{LINE}" stroke-width=".8"'), rect(35.6, 16.2, 4.4, 1.5, DIM),
             *leaf_puff(37.2, 14.6, 1),
             stroke("M5.5 30V37H8", DIM, 1.3), stroke("M5.5 30H8", DIM, 1.3),
             box(6.5, 32, 35, 11.2), *sawtooth(6.5, 41.5, 32, 4.4, 4),
             *windows(9, 34.6, 7, 2, 4.6, 3.6, 2.4, 2.2),
             *gear(38.4, 39.8, 1.9, 8),
             rect(6.5, 43.2, 35, 1.6, DIM), *[circ(10 + i * 5, 42.6, .9, FRUIT) for i in range(5)]]
    return parts, 18, 31.5, .62

def drawing(pid, stage):
    bparts, ax, ay, s = base(stage)
    plant = "".join(P.P[pid]())
    # plants are drawn on ground y=45 around x=24: move that point onto the roof
    g = f'<g transform="translate({n(ax)} {n(ay)}) scale({n(s)}) translate(-24 -45)">{plant}</g>'
    collar = rect(ax - 1.6, ay - .4, 3.2, 1.2, DIM) if stage >= 3 else ""
    # experiments grow under a glass terrarium dome
    dome = (shape("M15.5 41.5V36a8.5 8.5 0 0 1 17 0V41.5Z", GLASS, f' opacity=".28"') +
            stroke("M15.5 41.5V36a8.5 8.5 0 0 1 17 0V41.5", LINE, .8) +
            stroke("M18.4 32.4a6 6 0 0 1 4-3", "var(--bg)", .9)) if stage == 1 else ""
    return ("".join(bparts) + g + collar + dome)

def svg(pid, stage):
    return f'<svg class="plant works" viewBox="0 0 48 48" width="40" height="40" aria-hidden="true" focusable="false">{drawing(pid, stage)}</svg>\n'

if __name__ == "__main__":
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    items = [p for g in yaml.safe_load(open(os.path.join(root, "_data/projects.yml"))) for p in g["items"]]
    out = os.path.join(root, "_includes", "plantworks"); os.makedirs(out, exist_ok=True)
    for p in items:
        open(os.path.join(out, f'{p["plant"]}.svg'), "w").write(svg(p["plant"], p["maturity"]))
    print(len(items), "plantworks")
