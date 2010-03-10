import logging
import logging.handlers
from django.db import models

import feedparser

DEBUG_LOG_FILENAME = 'debug.log'
ERROR_LOG_FILENAME = 'error.log'

logger = logging.getLogger("FeedParser")
logger.setLevel(logging.DEBUG)

debug_handler = logging.handlers.RotatingFileHandler(DEBUG_LOG_FILENAME)
debug_handler.setLevel(logging.DEBUG)

error_handler = logging.handlers.RotatingFileHandler(ERROR_LOG_FILENAME)
error_handler.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
debug_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

logger.addHandler(debug_handler)
logger.addHandler(error_handler)

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
        feed_xml = stream.read()
        logger.debug(feed_xml)

        try:
            d = feedparser.parse(feed_xml)
        except Exception, e:
            logger.error(feed_xml)
            logger.error(e)            
            raise
        entries = []
        for entry in d.entries:
            e = Entry()
            try:
                e.consume(entry)
                e.save()
            except Exception, e:
                # we make a best-effort attempt to parse all entries
                logger.error(entry)
                logger.error(e)
            else:
                # only append the entry after it saves correctly
                entries.append(e)
        return entries
