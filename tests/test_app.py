
import unittest
from pathlib import Path


class EventPortalTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.html = (
            Path(__file__).resolve().parents[1] / "index.html"
        ).read_text(encoding="utf-8")

    def test_page_title(self):
        self.assertIn("College Event Management Portal", self.html)

    def test_upcoming_events(self):
        self.assertIn("Upcoming College Events", self.html)

    def test_registration_form(self):
        self.assertIn("registrationForm", self.html)

    def test_registration_status(self):
        self.assertIn("checkStatus", self.html)

    def test_faculty_overview(self):
        self.assertIn("Faculty Coordinator", self.html)

    def test_participant_limits(self):
        self.assertIn("limit", self.html)


if __name__ == "__main__":
    unittest.main()
