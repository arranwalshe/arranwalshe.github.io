#!/usr/bin/env python3
"""Tests for sync_publications.py. Run: python3 scripts/test_sync_publications.py"""
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sync_publications as sp  # noqa: E402

PAGE = """            <div class="section-container">
                <h2>Articles &amp; Deep Dives</h2>
                <div id="articles" class="section-content" style="display: grid;">
                    <h4 class="year-heading">2026</h4>
                    <p>Arran Robert Walshe, "Deep Dive: March piece." <i>Amwaj.media</i>. Mar. 11, 2026 <a href="https://amwaj.media/en/article/dd-march">[link]</a></p>

                    <h4 class="year-heading">2025</h4>
                    <p>Arran Robert Walshe, "Old article." <i>Amwaj.media</i>. Jan. 2, 2025 <a href="https://amwaj.media/en/article/old">[link]</a></p>
                </div>
            </div>

            <div class="section-container">
                <h2>Media Monitors</h2>
                <div id="monitors" class="section-content" style="display: none;">
                    <h4 class="year-heading">2026</h4>
                    <p>Arran Robert Walshe, "Aug piece." <i>Amwaj.media</i>. Aug. 14, 2026 <a href="https://amwaj.media/a">[link]</a></p>

                    <p>Arran Robert Walshe, "May piece." <i>Amwaj.media</i>. May 27, 2026 <a href="https://amwaj.media/b">[link]</a></p>
                </div>
            </div>

            <div class="section-container">
                <h2>Features &amp; Essays</h2>
"""

RECORD = """| Date | Title | Byline | Role | Format | URL |
| 2026-06-03 | Fayli Kurds struggle with division | Arran Walshe | wrote | Article | https://amwaj.media/en/article/fayli |
| 2026-06-20 | A June monitor | Amwaj.media | wrote | Media Monitor | https://amwaj.media/en/media-monitor/june |
| 2026-08-14 | Aug piece | Amwaj.media | wrote | Media Monitor | https://amwaj.media/a/ |
| 2026-09-01 | Someone else's | Paul Iddon | edited | Article | https://amwaj.media/edited |
| 2024-05-30 | Corruption claims, payouts to ‘IS families’ shake fund | Arran Walshe | wrote | Article | https://amwaj.media/en/article/2024 |
| 2025-08-06 | Deep Dive: Can Iraqi outreach secure a future? | Arran Walshe | wrote | Deep Dive | https://amwaj.media/en/article/dd |
"""


def tab_of(page, url):
    i = page.index(url)
    return "articles" if page.rfind('id="articles"', 0, i) > page.rfind('id="monitors"', 0, i) else "monitors"


class Sync(unittest.TestCase):
    def setUp(self):
        self.page, self.added = sp.add_entries(PAGE, sp.written_rows(RECORD))

    def test_only_written_and_new(self):
        self.assertEqual(sorted(r["url"].rsplit("/", 1)[1] for r in self.added), ["2024", "dd", "fayli", "june"])
        self.assertNotIn("https://amwaj.media/edited", self.page)

    def test_each_kind_in_its_tab(self):
        for url in ("article/fayli", "article/dd", "article/2024"):
            self.assertEqual(tab_of(self.page, url), "articles", url)
        self.assertEqual(tab_of(self.page, "media-monitor/june"), "monitors")

    def test_date_order_within_years(self):
        arts = self.page[self.page.index('id="articles"'):self.page.index('id="monitors"')]
        self.assertEqual([u.rsplit("/", 1)[1] for u in re.findall(r'href="([^"]+)"', arts)],
                         ["fayli", "dd-march", "dd", "old", "2024"])
        mons = self.page[self.page.index('id="monitors"'):]
        self.assertEqual(re.findall(r'href="([^"]+)"', mons),
                         ["https://amwaj.media/a", "https://amwaj.media/en/media-monitor/june", "https://amwaj.media/b"])

    def test_new_year_heading_in_the_right_tab(self):
        arts = self.page[self.page.index('id="articles"'):self.page.index('id="monitors"')]
        self.assertIn('<h4 class="year-heading">2024</h4>', arts)
        self.assertLess(arts.index(">2025<"), arts.index(">2024<"))

    def test_format(self):
        self.assertIn('<p>Arran Robert Walshe, "Fayli Kurds struggle with division." <i>Amwaj.media</i>. '
                      'June 3, 2026 <a href="https://amwaj.media/en/article/fayli">[link]</a></p>', self.page)
        self.assertIn('"Deep Dive: Can Iraqi outreach secure a future?" <i>', self.page)   # no extra stop
        self.assertIn("payouts to 'IS families' shake fund.", self.page)                  # straight quotes

    def test_existing_untouched_and_rerun_adds_nothing(self):
        for line in PAGE.splitlines():
            if "<p>" in line:
                self.assertIn(line.strip(), self.page)
        again, added = sp.add_entries(self.page, sp.written_rows(RECORD))
        self.assertEqual((again, added), (self.page, []))

    def test_media_monitor_address_wins_over_deep_dive_title(self):
        row = {"title": "Deep Dive: Mounting regional confrontation", "format": "Deep Dive",
               "url": "https://amwaj.media/en/media-monitor/deep-dive-mounting"}
        self.assertEqual(sp.tab(row), "monitors")

    def test_old_link_without_en_counts_as_present(self):
        page = PAGE.replace('href="https://amwaj.media/b"', 'href="https://amwaj.media/media-monitor/will-x"')
        rec = "| 2026-05-27 | May piece | Amwaj.media | wrote | Media Monitor | https://amwaj.media/en/media-monitor/will-x |\n"
        self.assertEqual(sp.add_entries(page, sp.written_rows(rec))[1], [])

    def test_other_sections_untouched(self):
        tail = PAGE[PAGE.index("<h2>Features"):]
        self.assertTrue(self.page.endswith(tail))


if __name__ == "__main__":
    unittest.main()
