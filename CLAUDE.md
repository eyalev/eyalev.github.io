# eyalev.com — agent notes

Read `README.md` first: Jekyll on GitHub Pages, no build step, deploy = push to
`master`. `CLAUDE.md` is in `_config.yml` `exclude`, so it is not published.
Contact address on the site is `hello@eyalev.com`.

## Baseline

Public-project baseline (`~/.claude/docs/public-project-baseline.md`), decided 2026-09-27.
A personal portfolio page with no server of its own.

- version: GitHub Pages, no Worker to serve /health.json
- feedback: personal site; the About page gives hello@eyalev.com, which is the channel
- privacy: static pages, no cookies, no analytics, no forms
- analytics: none wanted on a personal portfolio
- crawler-gate: static GitHub Pages, no D1 or paid calls
- og: not needed for a personal site
- alerts: nothing waits for a person
- observability: GitHub Pages, no Worker to observe
- check-390: static content pages, no interactive UI to verify
- 404: GitHub Pages default 404

## /freshbar/

`freshbar/` is the freshbar concept page (`index.html`) and its drop-in web
component (`fresh-bar.js`, MIT, no dependencies, loaded from
`https://eyalev.com/freshbar/fresh-bar.js` by other sites, so keep its URL and its
exports stable). Tests: `node freshbar/test.mjs`. Page styles are inline and use
only the site's tokens. Same baseline as the rest of the site (static, no
analytics, feedback via hello@eyalev.com). Exploration lab:
https://freshbar.kapps.dev (Access). House notes: `~/.claude/docs/freshbar.md`.

