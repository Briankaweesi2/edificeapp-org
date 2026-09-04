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

Vercel, as a static site. There is no build step and no framework — point a Vercel project at
this repo and leave the build command empty with the output directory as the root.

`vercel.json` sets `trailingSlash` (the app links to `/privacy/` with the slash and it must not
redirect away), long-lived caching for `/assets/`, and a Content-Security-Policy that allows
exactly one third party: Google Fonts for the stylesheet, `fonts.gstatic.com` for the faces.
Nothing else is permitted and `script-src` is `'none'`, because the site runs no JavaScript.

### The domain

In the Vercel project, add `edificeapp.org` and `www.edificeapp.org` under Settings -> Domains,
then set the records Vercel shows you at Namecheap. Delete the registrar's parking records for
`@` and `www` first, or they keep winning — `www` currently points at `parkingpage.namecheap.com`.
The certificate is issued automatically once the records resolve.

If you would rather Vercel ran the DNS, switch the domain to Custom DNS at Namecheap and use
Vercel's nameservers instead of individual records.

### Once the domain answers

Change `LegalUrls.SITE` in the app from the Vercel preview host to `https://edificeapp.org`, and
ship it. Until that release is out, the app's Settings links still point at the old host, so keep
that host serving.

## Still to do

- Replace `[APP STORE URL]` and `[GOOGLE PLAY URL]` in `index.html` once the listings are live.
- `assetlinks.json.template` — turn on Android App Links when there is a fingerprint to use.
- The privacy policy of record still describes email-and-password accounts. The app moved to
  Google and Apple sign-in on 2026-09-04, so that text needs revising at the source.
