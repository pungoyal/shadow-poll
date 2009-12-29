import rapidsms
from django.db import models

# Create your Django models here, if you need them.

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

class Responder(models.Model):
    def __init__(self, message):
        self.message = message

    def response(self):
        poll_response = self.message.text.split(";")
        selected_choice = Choice.objects.get(short_code=poll_response[0])
        
        Respondent(answer=selected_choice, age=poll_response[1], gender=poll_response[2]).save()
        our_response = "Thanks for your participation. You selected %s." % (selected_choice)
        return our_response

#        response = message.text.split(";")
#        answer = response[0]
#        self.debug("answer %s", answer)
#        selected_choice = Choice.objects.get(short_code=answer)
#        Respondent(answer=selected_choice, age=response[1], gender=response[2]).save()
#        message.respond("Thanks for your participation. You selected %s." % (selected_choice))
#        return True
