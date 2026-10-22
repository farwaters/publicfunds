"""Checks the published dashboard files, not a copy of their logic."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
MANIFEST = json.loads((ROOT / "public-data" / "v1" / "manifest.json").read_text(encoding="utf-8"))
TEMPLATE = "https://x.ai/bot/7Hr1hnJPXqOQbMmUZ7mTi"


class PublicPage(unittest.TestCase):
    def test_copy_control_uses_the_https_template(self):
        start = HTML.index('id="take-bot"')
        card = HTML[start:HTML.index("</section>", start)]
        self.assertIn("Start my own copy", card)
        self.assertIn(TEMPLATE, card)
        self.assertNotIn("grokbot://", card)

    def test_daily_publication_stamp(self):
        self.assertEqual(MANIFEST["generated_at_sast"], "2026-10-22T03:08:47+02:00")
        self.assertIn("freshness_slo", MANIFEST)
        names = [p.name for p in (ROOT / ".github").rglob("*") if p.is_file()]
        self.assertFalse(any("workflow" in n for n in names))

    def test_pages_custom_domain_file(self):
        text = (ROOT / "CNAME").read_text(encoding="utf-8").strip()
        self.assertEqual(text, "publicfunds.grokforum.site")


if __name__ == "__main__":
    unittest.main()
