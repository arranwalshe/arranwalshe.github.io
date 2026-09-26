---
slug: tools-oauth-pages
status: live on production — waiting on user-side Google Cloud / Search Console steps
---

# /tools/ pages for Google OAuth consent screens

## What this project is

Three public pages that Arran's personal `gog` automation tools, across several Google Cloud
projects, list on their OAuth consent screens so the projects can be published out of
"Testing". Plus the Search Console HTML verification file for `arranwalshe.com`.

## Current state (as of 2026-09-24)

Live, commit `6c197ea`, deploy run 35994176795 succeeded:

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

- All four URLs return 200 on the live site after deploy; live verification file is
  byte-identical to the Desktop original (`cmp`); live privacy page has the final paragraph
  order.

## Not verified

- That document content processed by Claude is not used to train AI models — depends on
  which Claude terms/settings Arran uses. The page states it as fact.
- That this setup satisfies Google's Limited Use AI/ML provisions, which the page claims to
  adhere to. Stated from memory; the current policy page was not read.
- Google's requirements for moving sensitive/restricted-scope projects to "In production"
  (authorized domain, verification) — from memory, not checked.

## Blockers (user's action)

1. Click Verify in Search Console for `arranwalshe.com`.
2. Add `arranwalshe.com` as an authorized domain on each Cloud project's consent screen.
3. Enter the three `/tools/` URLs in each consent screen's branding fields, then publish.
4. Confirm the two unverified privacy-page claims above hold.

## History

- 2026-09-24 — Built, reviewed with the user through three privacy-policy revisions,
  committed (`6c197ea`) and pushed at the user's go-ahead; deploy verified live.
