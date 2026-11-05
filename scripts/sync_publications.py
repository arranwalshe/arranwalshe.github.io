#!/usr/bin/env python3
"""Add Arran's newly published Amwaj pieces to the Writing page, from Amwaj's career record.

    python3 scripts/sync_publications.py            # show what would be added
    python3 scripts/sync_publications.py --apply    # add them to layouts/writing/single.html
    python3 scripts/sync_publications.py --publish  # add, commit and push (publishes the site)

Arran, 2026-11-05: the Writing page "should have everything I've written"; pieces he only edited stay
off; and the monthly update publishes on its own. The source is the career record kept in the
Amwaj-Automations repo (core/record.md, rows whose role is "wrote"), read from its GitHub copy
(git fetch, then git show origin/main), never from a working tree. Only adds: an entry already on
the page (matched by its link) is left exactly as it is, and nothing is ever removed or reordered.
New entries go under News Analysis, in their year, in date order, written like the others:
    Arran Robert Walshe, "Title." <i>Amwaj.media</i>. Mon. D, YYYY <a href="URL">[link]</a>

Run monthly on the Air by launchd (scripts/install-air-sync), the day after the career-record job.
Tests: python3 scripts/test_sync_publications.py
"""
import datetime
import html
import os
import re
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
PAGE = SITE / "layouts" / "writing" / "single.html"
AMWAJ = Path.home() / "codes" / "Amwaj-Automations"
RECORD = ".claude/memory_bank/core/record.md"
MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
GIT_ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, env=GIT_ENV)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r


def written_rows(record_text):
    """Rows of the record where Arran's role is 'wrote': {date, title, url}."""
    rows = []
    for line in record_text.splitlines():
        if not line.startswith("| 20"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 6 and cells[3] == "wrote":
            rows.append({"date": datetime.date.fromisoformat(cells[0]), "title": cells[1], "url": cells[5]})
    return rows


def norm(url):
    """One key per piece: Amwaj serves the same page at /en/... and, on older links, without /en/."""
    path = re.sub(r"^https?://(www\.)?amwaj\.media", "", url.strip()).rstrip("/")
    return re.sub(r"^/en(?=/)", "", path)


def entry(row):
    title = row["title"].replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    title = html.escape(title, quote=False)
    end = "" if title.endswith(("?", "!", ".")) else "."
    d = row["date"]
    return (f'<p>Arran Robert Walshe, "{title}{end}" <i>Amwaj.media</i>. '
            f'{MONTHS[d.month - 1]} {d.day}, {d.year} <a href="{row["url"]}">[link]</a></p>')


DATE_IN_ENTRY = re.compile(r"</i>\. ([A-Z][a-z]+\.?) (\d{1,2}), (\d{4})")


def entry_date(p_html):
    m = DATE_IN_ENTRY.search(p_html)
    if not m:
        return None
    mon = m.group(1)
    names = {n: i + 1 for i, n in enumerate(MONTHS)} | {"Jul.": 7, "Jun.": 6, "Sep.": 9}
    if mon not in names:
        return None
    return datetime.date(int(m.group(3)), names[mon], int(m.group(2)))


def add_entries(page, rows):
    """Return (new page text, rows added). Only News Analysis is touched."""
    start = page.index('<div id="news" class="section-content"')
    end = page.index('<div class="section-container">', start)
    news = page[start:end]
    present = {norm(u) for u in re.findall(r'href="([^"]+)"', news)}
    todo = sorted((r for r in rows if norm(r["url"]) not in present), key=lambda r: r["date"], reverse=True)
    indent = "                    "
    def list_end(text):
        # The region ends "...</p>\n  </div>\n  </div>\n": the news list closes at the second-last </div>.
        return text.rfind("</div>", 0, text.rfind("</div>"))

    for row in todo:
        year = str(row["date"].year)
        heading = f'<h4 class="year-heading">{year}</h4>'
        if heading not in news:
            # A new year block, before the first older year, or after the last year.
            older = [m.start() for m in re.finditer(r'<h4 class="year-heading">(\d{4})</h4>', news)
                     if m.group(1) < year]
            at = news.rindex("\n", 0, older[0]) + 1 if older else news.rindex("\n", 0, list_end(news)) + 1
            news = news[:at] + indent + heading + "\n\n" + news[at:]
        h = news.index(heading) + len(heading)
        nxt = news.find('<h4 class="year-heading">', h)
        block_end = nxt if nxt != -1 else list_end(news)
        # Before the first entry in this year that is older; else after the year's last entry.
        insert_at = None
        for m in re.finditer(r"<p>.*?</p>", news[h:block_end], re.S):
            d = entry_date(m.group(0))
            if d and d < row["date"]:
                insert_at = h + m.start()
                break
        text = entry(row)
        if insert_at is None:
            last = list(re.finditer(r"<p>.*?</p>", news[h:block_end], re.S))
            at = h + last[-1].end() if last else h
            news = news[:at] + "\n\n" + indent + text + news[at:]
        else:
            news = news[:insert_at] + text + "\n\n" + indent + news[insert_at:]
    return page[:start] + news + page[end:], todo


def read_record():
    git(AMWAJ, "fetch", "--quiet", "origin")
    return git(AMWAJ, "show", f"origin/main:{RECORD}").stdout


def main(argv):
    apply = "--apply" in argv or "--publish" in argv
    publish = "--publish" in argv
    if publish:
        if git(SITE, "symbolic-ref", "--short", "HEAD").stdout.strip() != "main":
            print("sync_publications: not on main, so nothing done")
            return 1
        git(SITE, "pull", "--ff-only", "--quiet", "origin", "main")
    page = PAGE.read_text(encoding="utf-8")
    new_page, added = add_entries(page, written_rows(read_record()))
    for row in added:
        print(f"  {'adding' if apply else 'would add'}: {row['date']}  {row['title']}")
    if not added:
        print("sync_publications: nothing new")
        return 0
    if not apply:
        return 0
    PAGE.write_text(new_page, encoding="utf-8")
    if publish:
        rel = str(PAGE.relative_to(SITE))
        git(SITE, "add", "--", rel)
        git(SITE, "commit", "-q", "-m", f"Writing page: {len(added)} new piece(s) from the career record "
            "(scripts/sync_publications.py)", "--", rel)
        r = git(SITE, "push", "-q", "origin", "main", check=False)
        print("sync_publications: published" if r.returncode == 0
              else f"sync_publications: PUSH FAILED, committed on this Mac only: {r.stderr.strip()}")
        return 0 if r.returncode == 0 else 1
    print(f"sync_publications: {len(added)} added to {PAGE.relative_to(SITE)} (not committed)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
