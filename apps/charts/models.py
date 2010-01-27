from __future__ import division
from math import ceil

from django.contrib.gis.db import models
from apps.poll.models import PollResponse
from postcode_name_map import get_name

class Governorates(models.Model):    
    the_geom = models.PointField(srid=4326)
    name = models.CharField(max_length=200)
    objects = models.GeoManager()
    
    def num_responses(self, name_map = get_name, pollresponse_manager_filter = PollResponse.objects.filter):
        self.post_code = name_map(self.name)
        if self.post_code == "Not Found":
            return None
        return pollresponse_manager_filter(location = self.post_code).count()
    
    def total_responses(self):
        self.poll_responses = PollResponse.objects.all()
        return self.poll_responses.count()
    
    def style(self):
        if self.num_responses():
            print (self.num_responses() / self.total_responses())
            return "s%d" % (int(ceil((self.num_responses() / self.total_responses()) * 100)))
        else:
            return None