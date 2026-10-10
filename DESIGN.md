# eyalev.com design

Text-first personal site. One column, white page, a serif for names and a sans for reading.

- **Type pair:** Newsreader (names, headings; 19–76 px, weight 400, tight tracking) + Geist (everything else; 13–18 px). No monospace, no all-caps.
- **Greys:** `--text #161615`, `--soft #3d3d3a`, `--dim #73736d`, `--faint #a3a39c`, `--rule #e6e6e1`, `--wash #f3f3ef`, page `#ffffff`. Dark mode mirrors them on `#121211`.
- **Accent:** one, `--accent #b4441a` (dark `#ee8f5f`). Used for hover/press and the current nav underline only.
- **Botanical palette (project plants only):** `--p-leaf #5f8a4a`, `--p-deep #3f6532`, `--p-pale #9fbc8c`, `--p-stem #8a7258`, `--p-bark #6b5440`, `--p-gold #dfa630`, `--p-rose #d98a7c`, `--p-violet #8576bd`, `--p-fruit #c2462b`, `--p-root #d9792c`, `--p-white #ffffff`, each with a dark-mode value. Used only inside the plant drawings on `/projects/`; never for text, links or UI.
- **Spacing:** 4 / 8 / 12 / 16 / 24 / 32 / 48 / 72 (`--s1`…`--s8`). 16 px side gutter on phones.
- **Radius:** none. Hairline rules (`1px var(--rule)`) separate rows; group headings get a full-strength rule.
- **Motion:** one move: on hover a home link's name slides 8 px right and turns accent (180 ms, `--ease`). Off under reduced motion; press colours on touch.
- **Pages:** home is only the name, one line and a list of links. Projects live in `_data/projects.yml` and render on `/projects/` in maturity tiers, most mature first. Each project has a plant (flat SVG, 48×48 viewBox, inline, 56 px; 48 px on phones) chosen for what it is and drawn at the growth stage of its maturity: sprout (1) to full grown (5).
