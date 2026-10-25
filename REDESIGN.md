# Edifice website rebuild · 25 October 2026

Local implementation; not deployed. The Pinterest reference informed the photographic hero,
compact navigation, clear sans-serif headline, and floating Scripture card. Original artwork,
not a copy of the reference. Frontend-design guidance kept inner pages quieter and content-led.

## Design

- Paper #F7F7F5, ink #20241F, secondary #60655E, accent #245641, rule #D9DDD6.
- Instrument Sans for interface and headings; Newsreader for Scripture.
- Homepage: photograph with left-aligned headline and a floating confession.
- Interior: navigation → breadcrumb → split introduction → distinct useful content → footer.
- Neutral backgrounds, restrained green accents, no automatic animation. Native menus and FAQ
  disclosures work without JavaScript. Visible keyboard focus and a skip link.

## Pages and SEO

Added /daily-confessions/, /glory/, /download/; rewrote /about/. Retained all existing theme,
chapter, legal, campaign and sharing routes. Titles, descriptions, canonical URLs, social
metadata and breadcrumb structured data are included on the new pages. Sitemap contains
38 indexable URLs; 32 existing nonindexable pages remain excluded. No invented ratings,
subscription prices or guaranteed search rankings. Search Console submission is a post-deploy step.

## Maintenance

After running the existing content generator, run these from the sibling edifice-app repository:

    python3 tools/site/build_marketing.py --site ../edificeapp-org
    python3 tools/site/audit_seo.py --site ../edificeapp-org
    python3 tools/site/check_marketing_links.py --site ../edificeapp-org

The marketing postprocessor preserves legal body copy and existing Scripture content. It changes
navigation, links, and presentation. Shared CSS references are versioned for the existing immutable
asset cache policy. Bump asset versions on subsequent edits before publishing.

## Verification

- Metadata/JSON-LD/sitemap audit: 70 pages, zero reported problems.
- Static link audit: 1,687 local references, no missing targets/fragments/assets or duplicate
  indexable titles/descriptions.
- Browser: mobile daily-confessions and Glory pages; menu navigation to Glory; desktop Download,
  Bible scenes and home. No horizontal overflow on measured mobile Glory or desktop Scenes.
- Homepage previously checked at mobile width, including FAQ and mobile menu.
- No production deployment, indexing, live hosting rewrites, or field performance measurement tested.

## Image provenance

Original AI-generated hero, generated with the imagegen tool (generation, not editing), exported
as assets/hero-word-v2.jpg. Prompt:

Use case: photorealistic-natural. Asset: wide landscape 3:2 website hero photograph for Edifice,
a Christian daily Scripture and confession app. Original premium editorial lifestyle photography,
not a webpage mockup. A young adult Caucasian white woman with softly wavy brown hair in a simple
ivory linen blouse sits by a large softly lit window in a quiet dark charcoal room, holding an
open Bible with natural hands, eyes lowered thoughtfully with a subtle peaceful smile. Medium-wide
waist-up composition: woman at centre-right, left half is clean shadowy negative space for white
website headline; face and book remain inside centre region for mobile crop. Soft warm morning
sunlight from the right, authentic skin and linen texture, subtle film grain, deep brown and
charcoal shadows, neutral cream highlights, no green colour cast. Grounded intimate hopeful
atmosphere, not posed corporate stock. No typography, no logos, no watermark, no decorative UI,
no extra people.
