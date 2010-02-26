from __future__ import division
from math import ceil
from django.contrib.gis.db import models

from poll.models import User, UserResponse


class Governorates(models.Model):    
    the_geom = models.PointField(srid=4326)
    name = models.CharField(max_length=200)
    objects = models.GeoManager()
    bounding_box = models.CharField(max_length=1000)

    def num_responses(self):
        return len(UserResponse.objects.filter(user__governorate = self.id))
    
    def total_responses(self):
        return len(UserResponse.objects.all())
    
    def description(self):
        return "Iraqi Governorates"
    
    def style(self, question):
        most_voted_category = question.most_voted_category_by_governorate(self.id)
        number_of_response
        if most_voted_category:
            style_id = "s%d-%d" % (most_voted_category.color.id, int(ceil(( len(UserResponse.objects.filter(question = question, user__governorate=self.id)) / question.get_number_of_responses_by_governorate(self.id)) * 18)))
            return style_id
        return ''
    
    def exposed(self):
        return {'name': self.id}
