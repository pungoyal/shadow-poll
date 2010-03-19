from __future__ import division
from math import ceil
from django.contrib.gis.db import models
from rapidsms.webui import settings
from poll.models import User, UserResponse, Category, Color

class Geography(models.Model):
    name = models.CharField(max_length=200)
    bounding_box = models.CharField(max_length=1000)

    # geodjango fields
    centroid = models.PointField(srid=4326)
    
    # geodjango internals
    objects = models.GeoManager()

    class Meta:
        abstract= True

    def __unicode__(self):
        return "%s" % (self.name)

    def description(self):
        return "Iraqi Governorate"

    def exposed(self):
        return {'name': self.id}

class Governorate(Geography):
    code = models.CharField(max_length=16, unique=True)

    # this is used by openlayers so that we can manually specify
    # a zoom level which will properly 'fill the image' with the district
    zoom_level = models.IntegerField(null=True, blank=True)

class District(Geography):
    code = models.CharField(max_length=16)
    governorate = models.ForeignKey(Governorate)
    
    class Meta:
        unique_together = ("governorate", "code")
    
class VoiceMessage(models.Model):
    name = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)
    female = models.NullBooleanField(null = True, blank=True)
    district = models.ForeignKey(District, null=True)
    arabic_text = models.TextField(null=True, blank=True, verbose_name="Arabic Translation")
    english_text = models.TextField(null=True, blank=True, verbose_name="English Translation")
    sound_file_name = models.CharField(max_length=150) # full file path on the system
    translated = models.BooleanField(default = False)
    date_recorded = models.DateTimeField()

    @property
    def sound_file_url(self):
        media_url = settings.RAPIDSMS_APPS["charts"]["media_base_url"]
        return media_url + self.sound_file_name

    def fill(self, entry, path):
        self.age = entry.age
        self.female = entry.female
        self.district = District.objects.get(id=entry.district)
        self.sound_file_name = path
        self.date_recorded = entry.updated

    def get_child_image(self):
        if self.female is None:
            return "child_no_identity"
        if self.female:
            return "child_girl"
        return "child_boy"

    def __unicode__(self):
        return "%s %s %s %s" % (self.name, self.female, self.age, self.sound_file_name)
