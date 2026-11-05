#!/usr/bin/env python3
"""Tests for sync_publications.py. Run: python3 scripts/test_sync_publications.py"""
import datetime
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sync_publications as sp  # noqa: E402

PAGE = """<div class="section-container">
                <h2>News Analysis</h2>
                <div id="news" class="section-content" style="display: grid;">
                    <h4 class="year-heading">2026</h4>
                    <p>Arran Robert Walshe, "Aug piece." <i>Amwaj.media</i>. Aug. 14, 2026 <a href="https://amwaj.media/a">[link]</a></p>

                    <p>Arran Robert Walshe, "May piece." <i>Amwaj.media</i>. May 27, 2026 <a href="https://amwaj.media/b">[link]</a></p>

                    <h4 class="year-heading">2025</h4>
                    <p>Arran Robert Walshe, "Old piece." <i>Amwaj.media</i>. Jan. 2, 2025 <a href="https://amwaj.media/c">[link]</a></p>
                </div>
            </div>

            <div class="section-container">
                <h2>Book Chapters</h2>
"""

RECORD = """| Date | Title | Byline | Role | Format | URL |
| 2026-06-03 | Fayli Kurds struggle with division | Arran Walshe | wrote | Article | https://amwaj.media/new-june |
| 2026-08-14 | Aug piece | Amwaj.media | wrote | Media Monitor | https://amwaj.media/a/ |
| 2026-09-01 | Someone else's | Paul Iddon | edited | Article | https://amwaj.media/edited |
| 2024-05-30 | Corruption claims, payouts to ‘IS families’ shake fund | Arran Walshe | wrote | Article | https://amwaj.media/2024 |
| 2025-08-06 | Deep Dive: Can Iraqi outreach secure a future? | Arran Walshe | wrote | Deep Dive | https://amwaj.media/dd |
"""


class Sync(unittest.TestCase):
    def setUp(self):
        self.page, self.added = sp.add_entries(PAGE, sp.written_rows(RECORD))
        self.order = re.findall(r'href="([^"]+)"', self.page)

    def test_only_written_and_new(self):
        self.assertEqual(sorted(r["url"] for r in self.added),
                         ["https://amwaj.media/2024", "https://amwaj.media/dd", "https://amwaj.media/new-june"])
        self.assertNotIn("https://amwaj.media/edited", self.page)

    def test_date_order_within_years(self):
        self.assertEqual(self.order[:6], ["https://amwaj.media/a", "https://amwaj.media/new-june",
                                          "https://amwaj.media/b", "https://amwaj.media/dd",
                                          "https://amwaj.media/c", "https://amwaj.media/2024"])

    def test_new_year_heading_after_the_last(self):
        self.assertIn('<h4 class="year-heading">2024</h4>', self.page)
        self.assertLess(self.page.index(">2025<"), self.page.index(">2024<"))
        self.assertLess(self.page.index(">2024<"), self.page.index("Book Chapters"))

    def test_format(self):
        self.assertIn('<p>Arran Robert Walshe, "Fayli Kurds struggle with division." <i>Amwaj.media</i>. '
                      'June 3, 2026 <a href="https://amwaj.media/new-june">[link]</a></p>', self.page)
        self.assertIn('"Deep Dive: Can Iraqi outreach secure a future?" <i>', self.page)   # no extra stop
        self.assertIn("payouts to 'IS families' shake fund.", self.page)                  # straight quotes

    def test_existing_untouched_and_rerun_adds_nothing(self):
        for line in PAGE.splitlines():
            if "<p>" in line:
                self.assertIn(line.strip(), self.page)
        again, added = sp.add_entries(self.page, sp.written_rows(RECORD))
        self.assertEqual((again, added), (self.page, []))

    def test_old_link_without_en_counts_as_present(self):
        page = PAGE.replace('href="https://amwaj.media/b"',
                            'href="https://amwaj.media/media-monitor/will-x"')
        rec = "| 2026-05-27 | May piece | Amwaj.media | wrote | Media Monitor | https://amwaj.media/en/media-monitor/will-x |\n"
        self.assertEqual(sp.add_entries(page, sp.written_rows(rec))[1], [])

    def test_other_sections_untouched(self):
        self.assertTrue(self.page.endswith(PAGE[PAGE.index('<div class="section-container">', 10):]))


if __name__ == "__main__":
    unittest.main()
