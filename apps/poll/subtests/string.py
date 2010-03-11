from unittest import TestCase
from apps.poll.string import has_word

class StringTest(TestCase):
    def test_has_word(self):
        self.assertTrue(has_word(("poll 12 f","poll")))
        self.assertTrue(has_word(("12 f poll","poll")))
        self.assertFalse(has_word(("12 f pull","poll")))
        self.assertFalse(has_word(("12 f apoll","poll")))        
