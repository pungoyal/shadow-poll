from __future__ import division
from math import ceil
from django.contrib.gis.db import models

from poll.models import User, UserResponse, Category, Color

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

    def total_responses(self):
        return len(UserResponse.objects.all())

    def description(self):
        return "Iraqi Governorate"

    def style(self, question):
        most_voted_category = self.most_voted_category()
        if most_voted_category:
            percentage = self._bubble_size(question)
            style_id = {'color': most_voted_category.color, 
                        'percentage': percentage }
            return style_id
        else:
            style_id = {'color': Color.objects.get(file_name="grey_dot.png"), 
                        'percentage': 0.5 }
            return style_id
        return None
    
    def _percentage_to_display(self, count, total):
        """ This formula returns the size of the bubble we want to display 
        responses - count of userresponses
        all_responses - count of all userresponses
        """
        if total == 0:
            return 0
        percentage = count / total
        return percentage
    
    def exposed(self):
        return {'name': self.id}

class Governorate(Geography):
    def _bubble_size(self, question):
        responses = UserResponse.objects.filter(question=question.id, user__governorate=self.id)
        all_responses = UserResponse.objects.filter(user__governorate=self.id)
        return self._percentage_to_display(responses.count(), all_responses.count())

    def most_voted_category(self):
        relevant_responses = UserResponse.objects.filter(user__governorate = self.id)
        return Category.most_popular(relevant_responses)

    def num_responses(self):
        return len(UserResponse.objects.filter(user__governorate = self.id))

class District(Geography):
    governorate = models.ForeignKey(Governorate, null=True)

    def _bubble_size(self, question):
        responses = UserResponse.objects.filter(question=question.id, user__district=self.id)
        all_responses = UserResponse.objects.filter(user__district=self.id)
        return self._percentage_to_display(responses.count(), all_responses.count())

    def most_voted_category(self):
        relevant_responses = UserResponse.objects.filter(user__district = self.id)
        return Category.most_popular(relevant_responses)

    def num_responses(self):
        return len(UserResponse.objects.filter(user__district = self.id))

GENDER = ( ('m', 'Male'), ('f', 'Female') )

class VoiceMessage(models.Model):
    name = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER, default=None, null=True, blank=True)
    district = models.ForeignKey(District, null=True)
    arabic_text = models.TextField(null=True)
    english_text = models.TextField(null=True)
    sound_file_name = models.CharField(max_length=150)

    def get_child_image(self):
        if self.gender == 'm':
            return "child_boy"

        if self.gender == 'f':
            return "child_girl"

        return "child_no_identity"

    def __unicode__(self):
        return "%s %s %s %s" % (self.name, self.gender, self.age, self.sound_file_name)
