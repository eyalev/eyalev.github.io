#!/usr/bin/env python3
"""Draw one plant per project for /projects/ -> _includes/plants/<id>.svg.

Each project is a plant chosen for what it is, drawn at the growth stage of
its maturity score (1 seed/sprout ... 5 full grown). 48x48 viewBox, ground at
y=45. Colours are CSS variables from assets/style.css (the --p-* botanical
tokens, see DESIGN.md), so the plants follow light and dark mode.

Run: python3 scripts/plants.py   (writes _includes/plants/*.svg)
"""
import math, os

def n(v): return f"{v:.2f}".rstrip("0").rstrip(".")

LEAF, DEEP, PALE = "var(--p-leaf)", "var(--p-deep)", "var(--p-pale)"
STEM, BARK = "var(--p-stem)", "var(--p-bark)"
GOLD, ROSE, VIOLET, FRUIT, ROOT, WHITE = "var(--p-gold)", "var(--p-rose)", "var(--p-violet)", "var(--p-fruit)", "var(--p-root)", "var(--p-white)"
FAINT = "var(--faint)"

def leaf(x, y, l, w, a=0, fill=LEAF, extra=""):
    # almond leaf: base at (x,y), tip l away, a = degrees clockwise from up
    return (f'<path d="M0 0Q{n(w)} {n(-l*.5)} 0 {n(-l)}Q{n(-w)} {n(-l*.5)} 0 0Z" '
            f'transform="translate({n(x)} {n(y)}) rotate({n(a)})" fill="{fill}"{extra}/>')
def ell(cx, cy, rx, ry, fill, rot=0, extra=""):
    t = f' transform="rotate({n(rot)} {n(cx)} {n(cy)})"' if rot else ""
    return f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(rx)}" ry="{n(ry)}" fill="{fill}"{t}{extra}/>'
def circ(cx, cy, r, fill, extra=""): return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="{fill}"{extra}/>'
def stroke(d, color, w):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{n(w)}" stroke-linecap="round" stroke-linejoin="round"/>'
def shape(d, fill, extra=""): return f'<path d="{d}" fill="{fill}"{extra}/>'
def ground(y=45, x1=11, x2=37): return stroke(f"M{x1} {y}H{x2}", FAINT, 1)
def flower(cx, cy, k, l, w, fill, center=None, cr=1.2, rot0=0, extra=""):
    out = [leaf(cx, cy, l, w, rot0 + i * 360 / k, fill, extra) for i in range(k)]
    if center: out.append(circ(cx, cy, cr, center))
    return out

P = {}
def plant(pid):
    def reg(fn): P[pid] = fn; return fn
    return reg

# ---------- 5: full grown ----------
@plant("olive")
def _():
    return [ground(),
        stroke("M23 45C23.5 40 20.5 36 23 31C25 27.5 24.5 24.5 22.5 21", BARK, 3),
        stroke("M23 31.5C27 29.5 29.5 26.5 30.5 22.5", BARK, 2),
        stroke("M22.8 25C19.5 23.5 17.5 21.5 16.5 19", BARK, 1.6),
        ell(15.5, 18, 8.5, 5.6, PALE), ell(25, 13, 10, 6.4, PALE), ell(33.5, 18.5, 8, 5.2, PALE), ell(24, 20.5, 10.5, 4.6, PALE),
        ell(19, 15, 5, 2.6, LEAF, -12, ' opacity=".55"'), ell(30, 15.5, 5, 2.6, LEAF, 12, ' opacity=".55"'), ell(24.5, 21, 6, 2.2, LEAF, 0, ' opacity=".45"'),
        circ(17.5, 21, 1.35, VIOLET), circ(27, 22.6, 1.35, VIOLET), circ(33, 21.4, 1.35, VIOLET), circ(21.5, 16.5, 1.35, VIOLET), circ(30.5, 13.5, 1.2, VIOLET)]

@plant("sunflower")
def _():
    return [ground(),
        stroke("M24 45C23.5 36 25 28 24 18", DEEP, 2.2),
        leaf(24, 37, 11, 6, -62), leaf(24, 31, 10, 5.4, 58), leaf(24, 25, 7.5, 4, -55, DEEP),
        *flower(24, 12, 16, 8.6, 2.6, GOLD), circ(24, 12, 4.6, BARK),
        circ(23, 11, .6, GOLD, ' opacity=".6"'), circ(25.4, 12.6, .6, GOLD, ' opacity=".6"'), circ(23.6, 13.6, .6, GOLD, ' opacity=".6"')]

# ---------- 4: established ----------
@plant("lotus")
def _():
    return [stroke("M6 41Q11 39.5 16 41T26 41T36 41T44 41", FAINT, 1),
        ell(13, 41.6, 7, 2.1, LEAF), ell(14.5, 41.2, 3.2, .7, DEEP, 0, ' opacity=".45"'),
        ell(35.5, 42, 5.6, 1.8, DEEP),
        stroke("M24 41V27", DEEP, 1.4),
        leaf(24, 27, 9, 3.6, -62, ROSE, ' opacity=".75"'), leaf(24, 27, 9, 3.6, 62, ROSE, ' opacity=".75"'),
        leaf(24, 27, 10, 3.8, -30, ROSE), leaf(24, 27, 10, 3.8, 30, ROSE), leaf(24, 27, 11, 4, 0, ROSE),
        circ(24, 25.5, 1.4, GOLD)]

@plant("bamboo")
def _():
    out = [ground()]
    for x, top in [(16, 15), (22.5, 9), (29, 13), (35, 20)]:
        out.append(stroke(f"M{x} 45V{top}", PALE, 3.1))
        y = 41
        while y > top + 2:
            out.append(stroke(f"M{x-1.6} {y}H{x+1.6}", DEEP, .9)); y -= 6
    for x, y, a in [(16, 27, -58), (16, 21, -40), (22.5, 15, 50), (22.5, 23, -55), (29, 19, 52), (29, 27, 60), (35, 26, 48), (22.5, 10, -25)]:
        out.append(leaf(x, y, 8, 1.7, a, LEAF))
    return out

@plant("pea")
def _():
    return [ground(),
        stroke("M31 45V10", STEM, 1.1),
        stroke("M24 45C22 39 29 37 27 31C25 25 31 23 29 17C28 14 30 12 32 11", LEAF, 1.6),
        ell(21.5, 36.5, 3.6, 2.3, LEAF, -30), ell(30, 33.5, 3.6, 2.3, LEAF, 28), ell(23, 26.5, 3.2, 2.1, LEAF, -30), ell(32, 22.5, 3.2, 2.1, LEAF, 30),
        stroke("M32 11c3-1 4 2 2 3.2c-1.2.7-2-.6-1.2-1.3", LEAF, .9),
        leaf(26, 30, 10, 2.6, 170, PALE), leaf(28, 21, 8.5, 2.3, 196, PALE),
        stroke("M25.5 32.5V38.5", DEEP, .6),
        circ(34.2, 15.8, 1.9, WHITE, f' stroke="{FAINT}" stroke-width=".5"'), circ(35.6, 17.4, 1.5, WHITE, f' stroke="{FAINT}" stroke-width=".5"')]

@plant("cactus")
def _():
    return [ground(),
        stroke("M28 34H32.5Q35 34 35 31.5V24", LEAF, 4.6),
        stroke("M20 38H16.5Q14 38 14 35.5V30", LEAF, 4.2),
        shape("M20 45V17.5a4 4 0 0 1 8 0V45Z", LEAF),
        stroke("M22.6 18V44.5", DEEP, .6), stroke("M25.4 18V44.5", DEEP, .6),
        *flower(24, 13.6, 6, 3.6, 1.6, FRUIT, GOLD, .9)]

# ---------- 3: working ----------
@plant("wheat")
def _():
    out = [ground(), leaf(22, 44.6, 13, 1.9, -24, LEAF), leaf(28, 44.6, 12, 1.9, 28, LEAF)]
    for d, tip in [("M21.5 45Q20.5 33 18.5 22", (18.5, 22)), ("M25 45Q25 31 25.6 19", (25.6, 19)), ("M28.5 45Q30.5 34 32.5 24", (32.5, 24))]:
        out.append(stroke(d, LEAF, 1.1))
        x, y = tip
        for i in range(4):
            out.append(leaf(x, y + 2 + i * 1.8, 3.2, 1.25, -28, PALE)); out.append(leaf(x, y + 2 + i * 1.8, 3.2, 1.25, 28, PALE))
        out.append(leaf(x, y + 1.6, 3.2, 1.2, 0, PALE))
    return out

@plant("strawberry")
def _():
    out = [ground(), stroke("M30 44.6Q37 41.5 42 44.6", STEM, .8)]
    for x, y in [(16, 32), (24, 28.5), (32, 33)]:
        out.append(stroke(f"M24 44.6Q{n((24+x)/2)} {n(y+6)} {x} {y}", LEAF, 1))
        for a in (-50, 0, 50): out.append(leaf(x, y, 4.6, 2.5, a, LEAF))
    out += flower(29, 38.5, 5, 2.2, 1.2, WHITE, GOLD, .7, extra=f' stroke="{FAINT}" stroke-width=".35"')
    out.append(shape("M17 39.5Q20 38.6 22.6 39.5Q22.2 43.6 19.8 44.4Q17.2 43.4 17 39.5Z", FRUIT))
    out += [circ(18.8, 41, .35, GOLD), circ(20.8, 41.6, .35, GOLD), circ(19.8, 43, .35, GOLD), leaf(19.8, 39.6, 1.8, 1, -40, LEAF), leaf(19.8, 39.6, 1.8, 1, 40, LEAF)]
    return out

@plant("bonsai")
def _():
    return [shape("M14 40H34L32 45H16Z", BARK),
        stroke("M24 40C24 36 20 34.5 21 30.5C22 27.5 27 27 27 22.5", BARK, 2.6),
        stroke("M21.2 31.5C18.5 30.5 16.5 29.6 14.5 28.5", BARK, 1.3),
        ell(14.5, 26.8, 5, 2.5, DEEP), ell(27, 20, 7.2, 3.2, DEEP), ell(32, 25.4, 4.4, 2.2, DEEP),
        ell(26, 19, 4, 1.4, LEAF, 0, ' opacity=".6"')]

@plant("succulent")
def _():
    out = [shape("M15.5 37H32.5L31 45H17Z", BARK)]
    for a, l in [(-80, 13), (-54, 16), (-27, 18), (0, 19), (27, 18), (54, 16), (80, 13)]:
        out.append(leaf(24, 37, l, 4, a, PALE))
    for a, l in [(-40, 12), (-14, 13.5), (14, 13.5), (40, 12)]:
        out.append(leaf(24, 37, l, 3.4, a, LEAF))
    out.append(leaf(24, 37, 9, 2.6, 0, DEEP))
    return out

# ---------- 2: early ----------
@plant("tomato")
def _():
    return [ground(), stroke("M24 45Q24 35 25 27", DEEP, 1.4),
        leaf(24, 40, 6.5, 2.1, -72, PALE), leaf(24, 40, 6.5, 2.1, 72, PALE),
        stroke("M24.6 33Q20.5 30.5 18.5 31.5", DEEP, .8), leaf(18.6, 31.6, 4, 2.2, -85), leaf(21.2, 31.6, 3.4, 1.9, -20),
        leaf(25, 27, 6, 3, -42), leaf(25, 27, 6, 3, 42), leaf(25, 27.2, 6.2, 3.1, 0)]

@plant("ivy")
def _():
    out = [ground(), stroke("M8 44C14 40 18 44 24 40.5C30 37 34 40.5 41 36", STEM, 1)]
    for x, y, s in [(13.5, 41.6, 1), (23.5, 40.6, 1.15), (32.5, 38.3, 1.05), (40, 36.2, .9)]:
        for a in (-48, 0, 48): out.append(leaf(x, y, 4.6 * s, 2.2 * s, a, DEEP))
    return out

@plant("clover")
def _():
    out = [ground()]
    for x0, x, y, s in [(19, 17, 33, 1), (24, 25, 29, 1.15), (29, 31.5, 35.5, .9)]:
        out.append(stroke(f"M{x0} 44.8Q{x0} {y+5} {x} {y}", LEAF, .9))
        for a in (-60, 60, 180):
            r = math.radians(a); out.append(circ(x + 2.2 * s * math.sin(r), y - 2.2 * s * math.cos(r), 2.25 * s, LEAF))
        out.append(circ(x, y, .7, DEEP))
    out.append(circ(21.3, 38.6, 1.9, WHITE, f' stroke="{FAINT}" stroke-width=".5"'))
    return out

@plant("dandelion")
def _():
    out = [ground(), leaf(24, 44.6, 9, 2.6, -64), leaf(24, 44.6, 9, 2.6, 64), leaf(24, 44.6, 8, 2.4, -32, DEEP), leaf(24, 44.6, 8, 2.4, 32, DEEP),
           stroke("M24 44.6Q25.2 36 24 27.5", DEEP, 1)]
    for i in range(16):
        a = math.radians(i * 22.5); x2, y2 = 24 + 5.4 * math.sin(a), 24 - 5.4 * math.cos(a)
        out.append(stroke(f"M24 24L{n(x2)} {n(y2)}", FAINT, .5)); out.append(circ(x2, y2, .7, FAINT))
    out += [circ(24, 24, 1.1, STEM), stroke("M35 16.5L36.8 14.2", FAINT, .5), circ(37.1, 13.8, .8, FAINT)]
    return out

@plant("apple")
def _():
    return [ground(), stroke("M24 45V25.5", BARK, 1.8), stroke("M24 33L19 29", BARK, 1.1), stroke("M24 30L29 26", BARK, 1.1),
        ell(18.2, 28.2, 2.7, 1.7, LEAF, -30), ell(29.8, 25.2, 2.7, 1.7, LEAF, 30), ell(24, 24, 2.9, 1.8, LEAF), ell(21, 32.6, 2.3, 1.4, LEAF, -20), ell(27, 30, 2.2, 1.3, LEAF, 25),
        *flower(26.6, 33.6, 5, 1.7, 1, ROSE, GOLD, .5)]

@plant("pine")
def _():
    return [ground(), stroke("M24 45V40", BARK, 1.6),
        shape("M24 23L30 31H18Z", DEEP), shape("M24 28L32 37H16Z", DEEP), shape("M24 33L33.5 41.5H14.5Z", DEEP),
        shape("M24 28L27 31.6H21Z", LEAF, ' opacity=".5"')]

@plant("poppy")
def _():
    return [ground(), leaf(22, 44.6, 6.5, 2, -52), leaf(26, 44.6, 6.5, 2, 52),
        stroke("M22.5 45Q20.5 35 23 26.5", LEAF, 1), stroke("M26.5 45Q30 38 29.5 33.5", LEAF, .9), ell(29.6, 32.3, 1.5, 2.3, PALE, 25),
        circ(21.2, 23.6, 3.2, FRUIT), circ(25, 23.6, 3.2, FRUIT), circ(23.1, 22, 3, FRUIT, ' opacity=".85"'), circ(23.1, 24.3, 1.2, BARK)]

@plant("snakeplant")
def _():
    e = f' stroke="{GOLD}" stroke-width=".55"'
    return [ground(), leaf(18.5, 45, 12, 2.8, -22, DEEP, e), leaf(21.5, 45, 19, 3.4, -8, DEEP, e), leaf(25, 45, 22, 3.6, 3, DEEP, e), leaf(28.5, 45, 15, 3.2, 16, DEEP, e),
        stroke("M24.6 40L25.5 30", PALE, .5), stroke("M21 40L20.3 32", PALE, .5)]

@plant("morningglory")
def _():
    return [ground(), stroke("M30 45V21.5", STEM, 1),
        stroke("M24 45C24 41 32.5 40.5 31 37C29.5 34 28 35.5 29 32C30 29 32 30 31 27C30.2 25 29 24 30.8 22.5", LEAF, 1.1),
        leaf(27.5, 40, 5, 3.4, -78), leaf(31.8, 33, 4.6, 3.2, 72), stroke("M30.8 22.5c2-.8 3 1 1.6 1.8", LEAF, .7),
        shape("M31.4 29.2L36.6 26.2L37 31Z", VIOLET), circ(36.8, 28.6, .6, WHITE)]

@plant("mint")
def _():
    return [ground(), stroke("M24 45V25.5", DEEP, 1.3),
        leaf(24, 40, 6, 3.4, -66), leaf(24, 40, 6, 3.4, 66), leaf(24, 34, 5.6, 3.2, -60), leaf(24, 34, 5.6, 3.2, 60),
        leaf(24, 29, 4.8, 2.8, -52), leaf(24, 29, 4.8, 2.8, 52), leaf(24, 26.5, 3.6, 2.2, 0, PALE)]

@plant("daisy")
def _():
    e = f' stroke="{FAINT}" stroke-width=".35"'
    return [ground(), leaf(22, 44.6, 6, 2, -60), leaf(26, 44.6, 6, 2, 60),
        stroke("M20.5 45Q19 37 19.5 30", LEAF, .9), stroke("M27.5 45Q29.5 39 29 34", LEAF, .9),
        *flower(19.5, 28, 11, 3.8, 1.3, WHITE, GOLD, 1.4, extra=e), *flower(29, 32.4, 10, 3.2, 1.15, WHITE, GOLD, 1.2, extra=e)]

@plant("carrot")
def _():
    out = [ground(36.5), shape("M20.4 36.5H27.6Q26.4 43.5 24.2 47.4Q21.8 43.6 20.4 36.5Z", ROOT),
           stroke("M22.2 39.5H24", "var(--bg)", .5), stroke("M24.2 42.2H25.6", "var(--bg)", .5)]
    for x2, y2 in [(18.5, 24), (24, 21), (29.5, 25)]:
        out.append(stroke(f"M24 36.5L{x2} {y2}", LEAF, .8))
        for t in (.35, .55, .75, .92):
            x, y = 24 + (x2 - 24) * t, 36.5 + (y2 - 36.5) * t
            out.append(leaf(x, y, 2.5, 1, -50, LEAF)); out.append(leaf(x, y, 2.5, 1, 50, LEAF))
    return out

# ---------- 1: experiments ----------
@plant("fern")
def _():
    return [ground(), stroke("M24 45Q24 39.5 25 36.5", LEAF, 1.5),
        stroke("M25 36.5C25 33 29.4 33 29.4 36C29.4 38.4 26.4 38.4 26.8 36.4", LEAF, 1.5),
        leaf(24.2, 41.5, 2.6, 1, -55), leaf(24.2, 41.5, 2.6, 1, 55), leaf(24.5, 38.8, 2.2, .9, -55), leaf(24.5, 38.8, 2.2, .9, 55)]

@plant("lavender")
def _():
    return [ground(), leaf(24, 44.6, 5.4, 1.2, -52, PALE), leaf(24, 44.6, 5.4, 1.2, 52, PALE), stroke("M24 45V33.5", PALE, .9),
        ell(24, 33.4, 1, 1.4, VIOLET), ell(23.1, 35.2, .9, 1.2, VIOLET), ell(24.9, 35.4, .9, 1.2, VIOLET), ell(24, 37, .8, 1.1, VIOLET)]

@plant("datepalm")
def _():
    return [ground(), ell(19.5, 44.2, 2.8, 1.4, BARK), leaf(21.5, 44.6, 13, 1.9, 9, LEAF), stroke("M21.6 44.4L23.6 32.4", DEEP, .4)]

@plant("bluebell")
def _():
    return [ground(), leaf(22.8, 45, 9, 1.4, -14), leaf(25.2, 45, 8, 1.4, 20),
        stroke("M24 45Q24 37 28 35", LEAF, .9), shape("M26.6 35Q28 33.6 29.6 35.2Q30.4 38 29.4 38.8Q28.6 38 27.4 38.6Q26.4 37.6 26.6 35Z", VIOLET)]

@plant("acorn")
def _():
    return [ground(), ell(21, 42.6, 2.6, 3, BARK), shape("M18.1 41.2Q21 38.2 23.9 41.2Z", STEM),
        stroke("M22.4 39.8Q24 35.5 27 34.4", LEAF, .9), leaf(27, 34.4, 3.4, 1.6, 30), leaf(27, 34.4, 3, 1.4, 100, PALE)]

@plant("radish")
def _():
    return [ground(), shape("M21.4 45A2.6 2.6 0 0 1 26.6 45Z", FRUIT), stroke("M24 43V37", PALE, .9),
        ell(21.4, 36.2, 2.8, 1.8, LEAF, 18), ell(26.6, 36.2, 2.8, 1.8, LEAF, -18)]

@plant("papyrus")
def _():
    out = [ground(), stroke("M24 45V33.5", LEAF, 1)]
    for a in range(-70, 71, 17.5 if False else 17):
        r = math.radians(a); out.append(stroke(f"M24 33.5L{n(24 + 5 * math.sin(r))} {n(33.5 - 5 * math.cos(r))}", PALE, .6))
    return out

@plant("bean")
def _():
    return [shape("M17 37.5H31V45H17Z", "var(--wash)", f' stroke="{BARK}" stroke-width="1"'), stroke("M17 39.5H31", BARK, .6),
        stroke("M24 37.5Q24 32.5 26.2 31.4Q27.8 30.8 27.2 32.6", LEAF, 1.1), ell(26.6, 31.2, 1.7, 1.2, PALE, -20)]

@plant("seed")
def _():
    return [ground(), ell(24, 43.4, 3, 1.9, BARK, -18), stroke("M22.6 44.6Q22 46 21 46.8", STEM, .6),
        stroke("M25.4 41.8Q26.4 39.4 25.6 38.2", LEAF, .9), leaf(25.6, 38.4, 2.2, 1.1, 40)]

def svg(pid):
    body = "".join(P[pid]())
    return (f'<svg class="plant" viewBox="0 0 48 48" width="40" height="40" aria-hidden="true" focusable="false">{body}</svg>\n')

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "_includes", "plants")
    os.makedirs(out, exist_ok=True)
    for pid in P:
        open(os.path.join(out, f"{pid}.svg"), "w").write(svg(pid))
    print(len(P), "plants")
