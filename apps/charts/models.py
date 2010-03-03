from __future__ import division
from math import ceil
from django.contrib.gis.db import models

from poll.models import User, UserResponse

MAX_SCALE_LENGTH_IN_STYLE = 18

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

    def num_responses(self):
        return len(UserResponse.objects.filter(user__governorate = self.id))
    
    def total_responses(self):
        return len(UserResponse.objects.all())
    
    def description(self):
        return "Iraqi Governorate"
    
    def style(self, question):
        most_voted_category = question.most_voted_category_by_governorate(self.id)
        if most_voted_category:
            percentage = self._percentage_to_display(question)
            style_id = {'color': most_voted_category.color, 
                        'percentage': percentage }
            return style_id
        return None
    
    def _percentage_to_display(self, question, governorate_id=None):
        """ This formula returns the size of the bubble we want to display 
        Currently this is calculated as 
        (percentage who voted for the popular question / total votes )
        """
        responses_to_most_voted = UserResponse.objects.filter(question=question.id, user__governorate=self.id)
        all_responses = UserResponse.objects.filter(user__governorate=self.id)
        percentage = responses_to_most_voted.count() / all_responses.count()
        return percentage
    
    def exposed(self):
        return {'name': self.id}

class Governorate(Geography):
    pass
        
class District(Geography):
    governorate = models.ForeignKey(Governorate, null=True)
        
class Audio(models.Model):
    location = models.CharField(max_length=150)
    age = models.IntegerField()
    name = models.CharField(max_length=100)
    translation = models.TextField()
