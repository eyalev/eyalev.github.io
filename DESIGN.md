# eyalev.com design

Text-first personal site. One column, white page, a serif for names and a sans for reading.

- **Type pair:** Newsreader (names, headings; 19–76 px, weight 400, tight tracking) + Geist (everything else; 13–18 px). No monospace, no all-caps.
- **Greys:** `--text #161615`, `--soft #3d3d3a`, `--dim #73736d`, `--faint #a3a39c`, `--rule #e6e6e1`, `--wash #f3f3ef`, page `#ffffff`. Dark mode mirrors them on `#121211`.
- **Accent:** one, `--accent #b4441a` (dark `#ee8f5f`). Used for hover/press and the current nav underline only.
- **Spacing:** 4 / 8 / 12 / 16 / 24 / 32 / 48 / 72 (`--s1`…`--s8`). 16 px side gutter on phones.
- **Radius:** none. Hairline rules (`1px var(--rule)`) separate rows; group headings get a full-strength rule.
- **Motion:** one move: on hover a home link's name slides 8 px right and turns accent (180 ms, `--ease`). Off under reduced motion; press colours on touch.
- **Pages:** home is only the name, one line and a list of links. Projects live in `_data/projects.yml` and render on `/projects/`.
