/**
 * <fresh-bar> — a word-sized gauge of age, built into a date.
 * https://eyalev.com/freshbar · Eyal Levin · MIT
 *
 *   <script type="module" src="https://eyalev.com/freshbar/fresh-bar.js"></script>
 *   <fresh-bar datetime="2026-09-12T08:00:00Z"></fresh-bar>          -> "3 weeks ago" over its channel
 *   <fresh-bar datetime="2026-09-12">12 Sep</fresh-bar>              -> your words, same channel
 *
 * The words stay; under them a thin channel, one width in every list, fills
 * from the left with how long ago it was. Five equal sections — a day, a
 * week, a month, a year, two years — log within each, so the recent past,
 * where lists are dense, gets most of the room. Empty for the first five
 * minutes, full at two years.
 *
 * Attributes
 *   datetime  required. An ISO date ("2026-09-12", "2026-09-12T08:00:00Z"), or unix
 *             seconds as a bare number (so a bare year like "2026" is NOT a year).
 *   stops     optional. Section ends, shortest first: "1d 1w 1mo 1y 2y" (the default:
 *             a day, a week, a month, a year, two years). Units: min h d w mo y.
 *   now       optional. Fix "now" (for tests and screenshots).
 *
 * Styling (CSS custom properties, set on fresh-bar or any ancestor)
 *   --freshbar-width   the one width for every bar in a list   (default 7.4em)
 *   --freshbar-height  channel thickness                        (default 3px)
 *   --freshbar-gap     space between the words and the channel  (default 2px)
 *   --freshbar-fill    the part that has passed                 (default currentColor at 55%)
 *   --freshbar-track   the rest of the channel                  (default currentColor at 15%)
 * and ::part(label), ::part(channel), ::part(fill) for anything else.
 */

const UNIT_H = { min: 1 / 60, h: 1, d: 24, w: 168, mo: 730.5, m: 730.5, y: 8766 };
export const DEFAULT_STOPS = '1d 1w 1mo 1y 2y';
const PAD = 0.18; // from a day on, the fill's edge stays in the middle 64% of its section

/** "1d 1w 1mo 1y 2y" -> [0, 24, 168, 730.5, 8766, 17532] (hours) */
export function parseStops(spec = DEFAULT_STOPS) {
  const hours = String(spec).trim().split(/\s+/).map((t) => {
    const m = /^(\d+(?:\.\d+)?)(min|mo|h|d|w|m|y)$/.exec(t);
    if (!m) throw new Error(`fresh-bar: bad stop "${t}" (use e.g. 1d 1w 1mo 1y 2y)`);
    return +m[1] * UNIT_H[m[2]];
  });
  return [0, ...hours];
}

/** How far the fill goes, 0..1, for an age in hours. */
export function fillFor(ageHours, stops = parseStops()) {
  const h = Math.max(0, ageHours);
  if (!Number.isFinite(h)) return 0;
  if (h < 5 / 60) return 0;
  const n = stops.length - 1, L = Math.log1p;
  if (h >= stops[n]) return 1;
  let i = 0;
  while (h >= stops[i + 1]) i++;
  const frac = (L(h) - L(stops[i])) / (L(stops[i + 1]) - L(stops[i]));
  return i === 0 ? (frac * (1 - PAD)) / n : (i + PAD + (1 - 2 * PAD) * frac) / n;
}

/** "Just now", "12 min ago", "3 hours ago", "Yesterday", "4 days ago", "2 weeks ago", "5 months ago", "1 year ago". */
export function relativeLabel(then, now = new Date()) {
  const mins = Math.floor((now - then) / 60000);
  const n = (k, unit) => `${k} ${unit}${k === 1 ? '' : 's'} ago`;
  if (mins < 1) return 'Just now';
  if (mins < 60) return `${mins} min ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return n(hours, 'hour');
  const day = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate());
  const days = Math.round((day(now) - day(then)) / 86400000);
  if (days <= 1) return 'Yesterday';
  if (days < 7) return `${days} days ago`;
  if (days < 30) return n(Math.floor(days / 7), 'week');
  if (days < 365) return n(Math.max(1, Math.floor(days / 30.44)), 'month');
  return n(Math.max(1, Math.floor(days / 365.25)), 'year');
}

export function parseWhen(v) {
  if (v == null || v === '') return null;
  const t = /^\d+$/.test(String(v).trim()) ? Number(v) * 1000 : Date.parse(v);
  return Number.isNaN(t) ? null : new Date(t);
}

const CSS = `
:host { display: inline-block; position: relative; vertical-align: baseline;
  min-width: var(--freshbar-width, 7.4em); font-variant-numeric: tabular-nums;
  padding-bottom: calc(var(--freshbar-gap, 2px) + var(--freshbar-height, 3px));
  margin-bottom: calc(-1 * (var(--freshbar-gap, 2px) + var(--freshbar-height, 3px))); }
:host([hidden]) { display: none; }
[part=channel] { position: absolute; left: 0; right: 0; bottom: 0; height: var(--freshbar-height, 3px);
  border-radius: 999px; overflow: hidden;
  background: var(--freshbar-track, color-mix(in srgb, currentColor 15%, transparent)); }
[part=fill] { display: block; height: 100%; width: calc(var(--f, 0) * 100%);
  background: var(--freshbar-fill, color-mix(in srgb, currentColor 55%, transparent)); }
time { font: inherit; color: inherit; }
button { all: unset; cursor: help; display: inline; border-radius: 2px; }
button:focus-visible { outline: 2px solid currentColor; outline-offset: 2px; }
.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }
[part=tip] { position: absolute; left: 0; top: calc(100% + 6px); z-index: 10; white-space: nowrap; font-size: 0.92em;
  padding: 4px 8px; color: var(--freshbar-tip-fg, Canvas); background: var(--freshbar-tip-bg, CanvasText); border-radius: 3px; }
[part=tip][hidden] { display: none; }
`;

const live = new Set();
let timer = 0;
function tick() { for (const el of live) el.render(); }

export class FreshBar extends HTMLElement {
  static observedAttributes = ['datetime', 'stops', 'now'];

  constructor() {
    super();
    const root = this.attachShadow({ mode: 'open' });
    root.innerHTML = `<style>${CSS}</style><button type="button" aria-expanded="false"><time part="label"><slot></slot><span class="auto"></span><span class="sr"></span></time></button><span part="channel" aria-hidden="true"><span part="fill"></span></span><span part="tip" role="status" hidden></span>`;
    this._time = root.querySelector('time');
    this._auto = root.querySelector('.auto');
    this._sr = root.querySelector('.sr');
    this._btn = root.querySelector('button');
    this._tip = root.querySelector('[part=tip]');
    // A phone has no hover: a tap (or Enter) shows the exact date; tapping again, or anywhere else, hides it.
    this._btn.addEventListener('click', (e) => { e.stopPropagation(); this.toggleTip(); });
    this._close = (e) => { if (!e.composedPath().includes(this)) this.toggleTip(false); };
    this._slot = root.querySelector('slot');
    this._slot.addEventListener('slotchange', () => this.render());
  }

  connectedCallback() {
    live.add(this);
    if (!timer) timer = setInterval(tick, 60_000);
    this.render();
  }

  toggleTip(show = this._tip.hidden) {
    this._tip.hidden = !show;
    this._btn.setAttribute('aria-expanded', String(show));
    if (show) {
      // open towards the side with room: anchored left by default, flipped right near the screen's edge
      this._tip.style.left = '0'; this._tip.style.right = 'auto';
      const r = this._tip.getBoundingClientRect();
      if (r.right > document.documentElement.clientWidth - 8) { this._tip.style.left = 'auto'; this._tip.style.right = '0'; }
    }
    if (show) document.addEventListener('click', this._close); else document.removeEventListener('click', this._close);
  }

  disconnectedCallback() {
    document.removeEventListener('click', this._close);
    live.delete(this);
    if (!live.size) { clearInterval(timer); timer = 0; }
  }

  attributeChangedCallback() { if (this.isConnected) this.render(); }

  /** 0..1, how far the fill goes right now (null without a date). */
  get fill() { return this._fill ?? null; }

  render() {
    const then = parseWhen(this.getAttribute('datetime'));
    const now = parseWhen(this.getAttribute('now')) || new Date();
    if (!then) { this._fill = null; this._time.removeAttribute('datetime'); this._auto.textContent = ''; this.style.setProperty('--f', 0); return; }
    let stops;
    try { stops = parseStops(this.getAttribute('stops') || DEFAULT_STOPS); } catch (e) { console.error(e); stops = parseStops(); }
    const f = fillFor((now - then) / 3600000, stops);
    this._fill = f;
    this.style.setProperty('--f', f.toFixed(4));
    const rel = relativeLabel(then, now);
    const own = this._slot.assignedNodes().some((n) => n.textContent.trim());
    this._auto.textContent = own ? '' : rel;
    this._time.setAttribute('datetime', then.toISOString());
    const stamp = then.toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' });
    this.title = own ? `${rel}, ${stamp}` : stamp;
    // Screen readers hear the age and the exact date, not just the visible words.
    this._sr.textContent = own ? `, ${rel}, ${stamp}` : `, ${stamp}`;
    this._tip.textContent = own ? `${stamp} · ${rel}` : stamp;
  }
}

if (!customElements.get('fresh-bar')) customElements.define('fresh-bar', FreshBar);
