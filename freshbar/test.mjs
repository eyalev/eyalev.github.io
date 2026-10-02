// node freshbar/test.mjs — the pure functions of fresh-bar.js (the element is checked in a browser by check.mjs)
import assert from 'node:assert/strict';
globalThis.HTMLElement ??= class {};
globalThis.customElements ??= { get: () => true, define() {} };
const { fillFor, parseStops, relativeLabel, parseWhen } = await import('./fresh-bar.js');

const S = parseStops();
assert.deepEqual(S, [0, 24, 168, 730.5, 8766, 17532], 'default stops: a day, a week, a month, a year, two years');
assert.equal(fillFor(0.05, S), 0, 'empty for the first five minutes');
const H = [0.5, 6, 24, 72, 168, 500, 730.5, 2000, 8766, 12000];
const f = H.map((h) => fillFor(h, S));
assert.ok(f.every((v, i) => i === 0 || v > f[i - 1]), 'older always draws wider');
assert.ok(fillFor(20, S) < 0.2 && fillFor(30, S) > 0.2 && fillFor(30, S) < 0.4, 'the first day is the first fifth, the week the second');
assert.equal(fillFor(20000, S), 1, 'full at two years');
assert.throws(() => parseStops('1d 2fortnights'), /bad stop/);
assert.deepEqual(parseStops('1h 1d'), [0, 1, 24], 'custom stops');
assert.deepEqual(parseStops('1mo 1y'), parseStops('1m 1y'), 'mo is a month; m is kept as an alias');

const now = new Date('2026-10-02T12:00:00Z');
const ago = (h) => new Date(now - h * 3600000);
assert.deepEqual(
  [0.001, 0.2, 5, 30, 80, 24 * 9, 24 * 29, 24 * 31, 24 * 200, 24 * 364, 24 * 365, 24 * 800].map((h) => relativeLabel(ago(h), now)),
  ['Just now', '12 min ago', '5 hours ago', 'Yesterday', '3 days ago', '1 week ago', '4 weeks ago', '1 month ago', '6 months ago', '11 months ago', '1 year ago', '2 years ago'],
);
assert.equal(parseWhen('1790000000')?.toISOString(), '2026-09-21T14:13:20.000Z', 'a bare number is unix seconds');
assert.equal(parseWhen('nonsense'), null);
console.log('fresh-bar: all checks pass');
