---
slug: writing-page-refresh
status: mostly done — one follow-up open (Amwaj byline/URL spot-check)
---

# Writing page refresh (publications update + redesign)

## What this project is

Bringing `/writing/` up to date with new publications (Amwaj, MERIP) and reorganizing/
restyling the page, prompted by the site having gone stale since Feb 2025.

## Current state (as of 2026-09-04)

All of the following is live on `arranwalshe.com/writing/` and deployed via the normal
`main` → GitHub Actions (`hugo.yml`) → `gh-pages` pipeline:

- Section structure changed from a single "Policy & Journalism" list into three: **News
  Analysis** (Amwaj only, grouped under year subheadings 2024/2025/2026), **Book Chapters**
  (unchanged), **Features & Essays** (renamed from "Other Writing", now also holds the MERIP
  piece).
- Each section's list is a two-column CSS grid (row-major order, so chronological reading
  order is preserved left-to-right) instead of one column.
- Added one MERIP piece (Aug 20, 2026, "Alternative Amman...") — fully verified against
  `~/Documents/Writing/published/alternative-amman-merip/README.md`, confirmed live URL.
- Added 23 Amwaj pieces spanning Feb 2026–Aug 2026, sourced from bylined draft text in
  `~/Documents/Amwaj/Amwaj-Automations/editorial/voice_corpus/{gold,pilot}/Walshe-*.txt`.
  One of these (the Aug 14, 2026 PMU-offices piece) was fully confirmed via that repo's own
  piece tracker (`'.claude/memory_bank/active/pieces/archive/20260828-final-Walshe-...md'`,
  live URL user-confirmed 2026-08-14). **The other 22 were NOT independently confirmed by
  loading the live amwaj.media page** — amwaj.media has been rate-limiting/bot-blocking
  automated fetches all session (a known, pre-existing issue also documented in that repo's
  own memory bank). They were matched via web search snippet content (title/topic/details
  aligning with the draft text), and added on the user's explicit go-ahead to proceed at that
  confidence level rather than wait.
- Fixed two real bugs surfaced by this work, unrelated to the content changes themselves:
  1. `layouts/page/publications.html` had unresolved git merge-conflict markers left over
     from an old merge (`ead9b76`/`d50ab56`) that broke the Hugo build outright. This had
     never been caught before because the `hugo.yml` GitHub Actions workflow had never
     successfully completed a run prior to this session.
  2. That same first successful deploy overwrote the `gh-pages` branch without a `CNAME`
     file (Hugo doesn't copy the repo-root `CNAME` into `public/`), which made GitHub Pages
     drop the `arranwalshe.com` custom domain entirely. Fixed by restoring it via
     `gh api -X PUT repos/.../pages -f cname=arranwalshe.com` immediately, and by adding
     `cname: arranwalshe.com` to the `peaceiris/actions-gh-pages` step in `hugo.yml` so it's
     written on every future deploy.
  3. `layouts/_default/index.html` was a leftover placeholder ("TEST TEXT FROM DEFAULT
     INDEX") that Hugo 0.165 (what CI's `hugo-version: 'latest'` installs) resolves the
     homepage to instead of the real `layouts/index.html`, unlike the older Hugo that had
     been installed locally. Deleted it — the real homepage is now the only candidate.
  4. The Writing page's fixed "Home" nav had no background, so once the lists got long
     enough to actually scroll, passing text became unreadable behind the transparent nav
     text. Fixed with a scroll-triggered backdrop (transparent at rest so the hero photo
     still shows through, solid+blurred once `scrollY > 10`).

## Verified vs unverified

- **Verified directly**: every CI/deploy fix above, by checking `gh run list` /
  `gh api repos/.../pages` / `curl` against the live site after each push — not assumed from
  a green build alone (a build was already known to be able to succeed while the pipeline
  silently didn't ship, per the merge-conflict incident).
- **Verified directly**: the nav fix, via local Hugo dev server + browser screenshots at
  both scroll positions before pushing.
- **Not verified**: the headline/date/URL for 22 of the 23 new Amwaj entries (see above) —
  content-matched via search only, not confirmed against the live page or its byline.

## Blockers needing the user specifically

1. **Spot-check the 22 unconfirmed Amwaj entries** once amwaj.media's rate-limit/bot-block
   clears — ideally re-run a WebFetch against each URL in `content/writing.md` /
   `layouts/writing/single.html`'s "News Analysis" 2026 section to confirm headline, date,
   and byline match what's live. If any don't match, fix or remove them.
2. There's an unquantified further backlog: the voice-corpus folders only had pilot/gold
   samples for Feb–May 2026 specifically (used for a voice-style-training exercise, not an
   exhaustive publication log) — there may be more of the user's Amwaj bylines beyond what's
   already listed, and none between May 2026 and the Aug 14 2026 piece were found. Worth
   asking the user whether they know of any gaps once the rate-limit issue is resolved.

## Next steps (ordered)

1. Once amwaj.media stops blocking automated fetches, re-verify the 22 pieces flagged above.
2. Ask the user if there are other Amwaj bylines (particularly May–Aug 2026) not covered by
   the voice-corpus sample.
3. No other open work on this project — the redesign, MERIP addition, and nav bug are done
   and confirmed live.
