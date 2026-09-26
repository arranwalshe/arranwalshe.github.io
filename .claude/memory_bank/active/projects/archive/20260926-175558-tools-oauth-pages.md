---
slug: tools-oauth-pages
status: "done: in use"
---

# /tools/ pages for Google OAuth consent screens

## What this project is

Three public pages that Arran's personal `gog` automation tools, across several Google Cloud
projects, list on their OAuth consent screens so the projects can be published out of
"Testing". Plus the Search Console HTML verification file for `arranwalshe.com`.

## Current state (as of 2026-09-26)

Done and in use. As the user reported on 2026-09-26 (not checked from this repo):

- Search Console verified `arranwalshe.com` under arranemail@gmail.com on 2026-09-24.
- The five personal Cloud projects list the three `/tools/` pages on their Branding page, and
  all five were published to production on 2026-09-24/25:
  - Writing — 76518172294
  - Creative — 740252122417
  - Life — 70821296159
  - Academic — 916735129621
  - IRCKHF — 96414549687
- Amwaj does not use these pages: its Cloud project is Internal, so it never needed publishing.

Live since commit `6c197ea` (deploy run 35994176795):

- `https://arranwalshe.com/tools/` (homepage: personal tools, not offered to others, not a
  login page) — `content/tools/_index.md`
- `https://arranwalshe.com/tools/privacy/` — `content/tools/privacy.md`. Sections: what data
  is accessed, how data is used, how data is stored and shared (tokens local; content may be
  processed by AI tools including Claude at the owner's direction; not used to train AI
  models; otherwise never shared/sold), Google API Services User Data Policy / Limited Use,
  revoking access, contact (arranemail@gmail.com).
- `https://arranwalshe.com/tools/terms/` — `content/tools/terms.md`
- `https://arranwalshe.com/google7b966efd2a91b4bf.html` — `static/`, copied unchanged from
  `~/Desktop`.

## Must stay

- **`static/google7b966efd2a91b4bf.html` must not be deleted, renamed or edited.** Google
  re-checks the verification file periodically; if it disappears, Search Console ownership of
  `arranwalshe.com` lapses.
- The three `/tools/` URLs are now referenced by five production OAuth consent screens. Moving
  or removing them breaks those Branding pages.

Implementation notes:
- All three use `layouts/page/single.html` (bio-photo background + Home link), same as Bio/CV.
  `_index.md` needs `layout: single`; with `layout: page` the section page falls through to
  the plain `_default/page.html`. privacy/terms use `layout: page` like CV and still get
  `page/single.html`.
- Links carry inline `style="color: white;"` — that template has no link styling (Bio/CV
  have no links), so they rendered default blue on the dark photo.
- Not in any navigation: menus are hardcoded in `layouts/index.html` and `config.toml`; neither
  touched. Checked no built page outside `/tools/` links to them.

## Verified

- All four URLs returned 200 on the live site after the 2026-09-24 deploy; live verification
  file was byte-identical to the Desktop original (`cmp`); live privacy page had the final
  paragraph order.

## Still open (not verified)

These were open on 2026-09-24 and nothing since has resolved them:

- That document content processed by Claude is not used to train AI models — depends on
  which Claude terms/settings Arran uses. The privacy page states it as fact.
- That this setup satisfies Google's Limited Use AI/ML provisions, which the page claims to
  adhere to. Stated from memory; the current policy page was not read.

## History

- 2026-09-24 — Built, reviewed with the user through three privacy-policy revisions,
  committed (`6c197ea`) and pushed at the user's go-ahead; deploy verified live.
- 2026-09-26 — Marked done: in use. User reported Search Console verified (2026-09-24) and
  all five personal Cloud projects (Writing, Creative, Life, Academic, IRCKHF) publishing to
  production with the `/tools/` pages on their Branding page (2026-09-24/25). Amwaj recorded
  as not using them (Internal project). Added the must-stay note for the verification file.
