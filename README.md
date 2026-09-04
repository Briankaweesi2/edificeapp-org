# edificeapp.org

The Edifice website. Static HTML, no build step, no dependencies.

## What is here

| Path | Notes |
|---|---|
| `/` | The home page |
| `/privacy/` `/terms/` `/delete-account/` `/support/` | **Compiled into the shipping app.** Do not move or rename them — the app links to these exact URLs from Settings, so a change means a store release. |
| `/assets/site.css` | The whole design system: Dawn and Vesper, both driven by `prefers-color-scheme` |
| `/assets/logo.svg` | The mark, monochrome so CSS recolours it per scheme |

The legal copy is carried over verbatim from the app repo
(`composeApp/src/wasmJsMain/resources/*.html`), which is the text of record. Edit it there and
re-carry it, rather than editing it here and letting the two drift.

## Design

Everything is lifted from the app's `Theme.kt` so the site and the product are one thing.

- **Dawn** — page ramp `#E3ECE4` → `#DCE7E9` → `#E2DFEA`, ink `#141C17`, accent `#1C5B42`
- **Vesper** — page ramp `#131218` → `#16151C` → `#1B1A22`, ink `#F5F1E8`, accent `#7FBF9B`
- Newsreader for confessions, titles and headings; Instrument Sans for everything else
- Surfaces are flat. The page ramp is the only gradient. There is no gold in the dark scheme.
- Motion is long-cycle and stops entirely under `prefers-reduced-motion`

## Deploying

GitHub Pages serves it from the default branch. `CNAME` claims `edificeapp.org`.

DNS at the registrar, for an apex domain:

    A     @   185.199.108.153
    A     @   185.199.109.153
    A     @   185.199.110.153
    A     @   185.199.111.153
    CNAME www <owner>.github.io

Delete the registrar's parking records first, or they keep winning. HTTPS is issued
automatically once the records resolve; tick **Enforce HTTPS** in the repo's Pages settings
after that.

## Still to do

- Replace `[APP STORE URL]` and `[GOOGLE PLAY URL]` in `index.html` once the listings are live.
- `assetlinks.json.template` — turn on Android App Links when there is a fingerprint to use.
- The privacy policy of record still describes email-and-password accounts. The app moved to
  Google and Apple sign-in on 2026-09-04, so that text needs revising at the source.
