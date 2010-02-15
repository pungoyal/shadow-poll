from __future__ import division

from math import ceil

from apps.tree.models import Entry
from django.contrib.gis.db import models

from postcode_name_map import get_name


class Governorates(models.Model):    
    the_geom = models.PointField(srid=4326)
    name = models.CharField(max_length=200)
    objects = models.GeoManager()
    bounding_box = models.CharField(max_length=1000)
    
    def num_responses(self):
        return Entry.objects.filter(governorate = self.id).count()
    
    def total_responses(self):
        return Entry.objects.all().count()
    
    def style(self):
        number_of_responses = self.num_responses()
        if number_of_responses:
            return "s%d" % (int(ceil((number_of_responses / self.total_responses()) * 100)))
        else:
            return None

    def exposed(self):
        return {'name': self.id}
