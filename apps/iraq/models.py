from django.db import models

GENDER_CHOICES = ( ('M', 'Male'), ('F', 'Female') )

class Question(models.Model):
    question = models.CharField(null=False, max_length=200)

    def __unicode__(self):
        return self.question

class Choice(models.Model):
    choice = models.CharField(null=False, max_length=100)
    short_code = models.CharField(null=False, max_length=2)
    question = models.ForeignKey('Question')

    def __unicode__(self):
        return self.choice

class Respondent(models.Model):
    answer = models.ForeignKey('Choice')
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    mobile_number = models.IntegerField()
    our_response = models.CharField(max_length=160)

class Responder(models.Model):
    def __init__(self, message):
        self.message = message

    def response(self):
        poll_response = self.message.split(";")
        selected_choice = Choice.objects.get(short_code=poll_response[0])
        our_response = "Thanks for your participation. You selected %s." % (selected_choice)
        return Respondent(answer=selected_choice, age=poll_response[1], gender=poll_response[2], our_response=our_response)
