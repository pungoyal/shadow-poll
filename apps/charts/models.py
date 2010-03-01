from __future__ import division
from math import ceil
from django.contrib.gis.db import models

from poll.models import User, UserResponse

MAX_SCALE_LENGTH_IN_STYLE = 18

class Governorate(models.Model):    
    the_geom = models.PointField(srid=4326)
    name = models.CharField(max_length=200)
    objects = models.GeoManager()
    bounding_box = models.CharField(max_length=1000)
    
    def __unicode__(self):
        return "%s" % (self.name)

    def num_responses(self):
        return len(UserResponse.objects.filter(user__governorate = self.id))
    
    def total_responses(self):
        return len(UserResponse.objects.all())
    
    def description(self):
        return "Iraqi Governorate"
    
    def style(self, question):
        most_voted_category = question.most_voted_category_by_governorate(self.id)
        if most_voted_category:
            style_id = {'color': most_voted_category.color, 'percentage': len(UserResponse.objects.filter(question=question.id, user__governorate=self.id)) / len(UserResponse.objects.filter(user__governorate=self.id))}
            return style_id
        return None
    
    def exposed(self):
        return {'name': self.id}
