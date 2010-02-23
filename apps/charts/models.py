from __future__ import division
from math import ceil
from django.contrib.gis.db import models

from polls.models import User, UserResponse
# class ColorMap(models.Model):
#     category = models.ForeignKey(Category)
#     color = models.CharField(max_length=20)
    
#     def get_color_for_category(self, cat_id):
#         return ColorMap.objects.get(category = cat_id)
    
#     def __unicode__(self):
#         return self.color
    
class Governorates(models.Model):    
    the_geom = models.PointField(srid=4326)
    name = models.CharField(max_length=200)
    objects = models.GeoManager()
    bounding_box = models.CharField(max_length=1000)
    
    def num_responses(self):
        return len(User.objects.filter(location = self.id))
    
    def total_responses(self):
        return len(UserResponse.objects.all())
    
    def style(self):
        return "s%d" % int(ceil((self.num_responses() / self.total_responses()) * 100))

    def exposed(self):
        return {'name': self.id}
