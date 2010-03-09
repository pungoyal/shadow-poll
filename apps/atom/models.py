from django.db import models
import feedparser

class Entry(models.Model):
    title = models.CharField(max_length=255)
    uid = models.CharField(max_length=255)
    updated = models.DateTimeField()

    age = models.IntegerField(null = True)
    female = models.NullBooleanField(null = True)
    phone_number = models.CharField(max_length = 20)

    governorate = models.IntegerField(null = True)
    district = models.IntegerField(null = True)

    file_url = models.CharField(max_length = 255)

    def consume(self, entry):
        self.title = entry.title
        self.uid = entry.id
        self.updated = entry.updated.replace("T", " ").replace("Z", "")
        self.governorate = int(entry.governorate)
        self.district = int(entry.district)
        self.age = int(entry.age)

        self.female = self._parse_gender(entry.gender)
        self.file_url = entry.links[0].href

    def _parse_gender(self, gender):
        if gender is None or len(gender) == 0:
            return None
        gender = gender.strip()
        if gender.lower() == 'f':
            return True
        return False


class IVRFeedParser(object):
    def parse(self, stream):
        d = feedparser.parse(stream)

        entries = []
        for entry in d.entries:
            e = Entry()
            e.consume(entry)
            entries.append(e)
        return entries
        