# CLAUDE.md

Repo-specific guidance. The user-level `~/.claude/CLAUDE.md` covers everything shared across repos.

## This repo is public

The Hugo source for arranwalshe.com, published with GitHub Pages. Anything committed here can be
read by anyone, so two folders are kept out of git by `.gitignore` (settled by Arran 2026-10-04):

- `.claude/`: the memory bank and every other Claude note stay on the computer.
- `inbox/` task files (only `inbox/README.md` is tracked).

Never force-add either, and never write private detail into a tracked file.

## Work here on the MacBook Air only

The memory bank isn't in git, so it exists on one Mac: the Air. Don't do site work on the Mac
mini. **If `.claude/memory_bank/` is missing, you're on the wrong Mac: stop and say so.**

Inbox tasks for this repo are local too. Send them from the Air, or to Hub.

## The Writing page fills itself from the career record

Since 2026-11-05 (Arran: the page "should have everything I've written"; pieces he only edited stay
off; and the update "should push automatically"). `scripts/sync_publications.py` reads the career
record kept by Amwaj-Automations (`core/record.md`, rows with role "wrote", from its GitHub copy) and
adds any piece not yet on the page to its tab in `layouts/writing/single.html` (Articles & Deep
Dives, or Media Monitors; the page is organised by kind of work since 2026-11-05), in its year, in
date order. It only adds: entries already there (matched by link, with or without `/en/`) are never
changed or removed. A launchd job on the Air runs it with `--publish` on the 2nd of each month at
13:05 (`scripts/install-air-sync`), which commits that one file and pushes, so it **publishes the
site without asking**: the one standing exception to "a push here is Arran's to make". Tests:
`python3 scripts/test_sync_publications.py`. Log: `~/Library/Logs/website-publications-sync.log`.

When editing the page by hand, keep the entry format (`Arran Robert Walshe, "Title." <i>Amwaj.media</i>.
Mon. D, YYYY <a href="…">[link]</a>`), so the sync can read dates and links.
