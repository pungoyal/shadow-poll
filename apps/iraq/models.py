from django.db import models

# Create your Django models here, if you need them.

GENDER_CHOICES = ( ('M', 'Male'), ('F', 'Female') )

class Question(models.Model):
    question = models.CharField(null=False, max_length=200)

class Choice(models.Model):
    choice = models.CharField(null=False, max_length=100)
    question = models.ForeignKey('Question')

class Respondent(models.Model):
    answer = models.ForeignKey('Choice')
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
