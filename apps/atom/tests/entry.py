from unittest import TestCase
from apps.atom.models import Entry

class EntryTest (TestCase):
    def test_parse_gender(self):
        self.assertEquals(Entry()._parse_gender('M'), False)
        self.assertEquals(Entry()._parse_gender('m'), False)
        self.assertEquals(Entry()._parse_gender('F'), True)
        self.assertEquals(Entry()._parse_gender('f'), True)
        self.assertEquals(Entry()._parse_gender(None), None)
        self.assertEquals(Entry()._parse_gender(""), None)
        self.assertEquals(Entry()._parse_gender('foo'), False)
