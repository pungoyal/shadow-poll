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
            style_id = {'color': most_voted_category.color,
                        'percentage': len(UserResponse.objects.filter(question=question.id, user__governorate=self.id)
                                ) / len(UserResponse.objects.filter(user__governorate=self.id))}
            return style_id
        return None

    def exposed(self):
        return {'name': self.id}

class Governorate(Geography):
    pass

class District(Geography):
    governorate = models.ForeignKey(Governorate, null=True)

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
