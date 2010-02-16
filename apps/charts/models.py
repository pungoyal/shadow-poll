from __future__ import division

from math import ceil

from apps.tree.models import Entry
from django.contrib.gis.db import models

class Governorates(models.Model):    
    the_geom = models.PointField(srid=4326)
    name = models.CharField(max_length=200)
    objects = models.GeoManager()
    bounding_box = models.CharField(max_length=1000)
    
    def num_responses(self):
        return len(Entry.objects.filter(governorate = self.id))
    
    def total_responses(self):
        return len(Entry.objects.all())
    
    def style(self):
        return "s%d" % int(ceil((self.num_responses() / self.total_responses()) * 100))

    def exposed(self):
        return {'name': self.id}
