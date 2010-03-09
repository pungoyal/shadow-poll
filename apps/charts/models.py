from __future__ import division
from math import ceil
from django.contrib.gis.db import models

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

    def total_responses(self):
        return len(UserResponse.objects.all())

    def description(self):
        return "Iraqi Governorate"

    def style(self, question, selected_options=None):
        most_voted_category = self.most_popular_category(question)
        if most_voted_category:
            scale = self._bubble_size(question, selected_options)
            if scale:
                style = {'color': most_voted_category.color, 
                         'percentage': scale }
                return style
        # default to grey
        style = {'color': Color.objects.get(file_name="grey_dot.png"), 
                 'percentage': 0.6 }
        return style
    
    def _percentage_to_display(self, count, total):
        """ This formula returns the size of the bubble we want to display 
        responses - count of userresponses
        all_responses - count of all userresponses
        """
        if total == 0:
            return 0
        
        percentage = float(count) / float(total)
        return percentage
    
    def exposed(self):
        return {'name': self.id}
AGE_RANGE = {'a1': '6,7,8,9,10,11', 'a2': '12,13,14', 'a3': '15,16,17'}
class Governorate(Geography):
    code = models.CharField(max_length=16, unique=True)

    # this is used by openlayers so that we can manually specify
    # a zoom level which will properly 'fill the image' with the district
    zoom_level = models.IntegerField(null=True, blank=True)
    
    def _bubble_size(self, question, selected_options=None):
        """ number of responses in the most popular category for this question
        divided by total responses to this question 
        """
        category = self.most_popular_category(question)
        if category is None:
            return 0
        responses = UserResponse.objects.filter(choice__category=category, 
                                                question=question, 
                                                user__governorate=self.code)
        #filter by selected options from check box's
        gender = selected_options["gender"] # m,f
        age_code = selected_options["age"] # a1,a2,a3
        
        if gender <> "" :
            gender = str(gender).split(",")
        if age_code <>"":
            age_code = age_code.split(",")
        age_range = ""
               
        if len(age_code) > 0:
            for a in age_code:
                age_range = age_range +  AGE_RANGE[a] + ","
        if len(age_code) > 0:
            age_range = age_range[:len(age_range)-1]
            age_range = age_range.split(",")
        #**************************************
        #retrieve users depends on what what filter has been selected
        if len(age_range) > 0 and len(gender) > 0 :
            selected_users = User.objects.filter(gender__in=gender,age__in=age_range)
        elif len(age_range) > 0 and len(gender) == 0 :
            selected_users = User.objects.filter(age__in=age_range)
        elif len(gender) > 0 and len(age_range) == 0 :
            selected_users =User.objects.filter(gender__in=gender )           
        
        #**************************************
        user_ids=[]
        for current in selected_users:
            user_ids.append(current.id)

        responses=responses.filter(user__in=user_ids)
        #end of modifications

        all_responses = UserResponse.objects.filter(question=question, 
                                                    user__governorate=self.code)
        return self._percentage_to_display(responses.count(), all_responses.count())

    def most_popular_category(self, question):
        relevant_responses = UserResponse.objects.filter(user__governorate = self.code, question=question)
        return Category.most_popular(relevant_responses)

    def num_responses(self):
        return len(UserResponse.objects.filter(user__governorate = self.code))

class District(Geography):
    code = models.CharField(max_length=16)
    governorate = models.ForeignKey(Governorate)
    
    class Meta:
        unique_together = ("governorate", "code")

    def _bubble_size(self, question, selected_options=None):
        """ number of responses in the most popular category for this question
        divided by total responses to this question 
        """
        category = self.most_popular_category(question)
        if category is None:
            return 0
        responses = UserResponse.objects.filter(choice__category=category, 
                                                question=question, 
                                                user__district=self.code, 
                                                user__governorate=self.governorate.code)
        
        #filter by selected options from check box's
        gender = selected_options["gender"] # m,f
        age_code = selected_options["age"] # a1,a2,a3
        
        if gender <> "" :
            gender = gender.split(",")
        
        if age_code <>"":
            age_code = age_code.split(",")
        
        age_range = ""
        
        if len(age_code) > 0:
            for a in age_code:
                age_range = age_range +  AGE_RANGE[a] + ","
        if len(age_code) > 0:
            age_range = age_range[:len(age_range)-1]
            age_range = age_range.split(",")
        #**************************************
        #retrieve users depends on what what filter has been selected
        if len(age_range) > 0 and len(gender) > 0 :
            selected_users = User.objects.filter(gender__in=gender ) & User.objects.filter(age__in=age_range)
        elif len(age_range) > 0 and len(gender) == 0 :
            selected_users = User.objects.filter(age__in=age_range)
        elif len(gender) > 0 and len(age_range) == 0 :
            selected_users =User.objects.filter(gender__in=gender )           
        
        #**************************************
        user_ids=[]
        for current in selected_users:
            user_ids.append(current.id)
        
        responses=responses.filter(user__in=user_ids)
        #end of modifications
        
        
        all_responses = UserResponse.objects.filter(question=question, 
                                                    user__district=self.code, 
                                                    user__governorate=self.governorate.code)
        
        return self._percentage_to_display(responses.count(), all_responses.count())

    def most_popular_category(self, question):
        relevant_responses = UserResponse.objects.filter(user__district = self.code, user__governorate=self.governorate.code, question=question)
        return Category.most_popular(relevant_responses)

    def num_responses(self):
        return len(UserResponse.objects.filter(user__district = self.code, user__governorate=self.governorate.code))

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
