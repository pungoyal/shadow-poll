from django.db import models

GENDER = ( ('M', 'Male'), ('F', 'Female') )

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

class PollResponse(models.Model):
    issue = models.ForeignKey('Choice')
    age = models.IntegerField()
    location = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER)
    mobile_number = models.IntegerField()

    def generateResponse(self, text, identity):
        old_response = PollResponse.objects.filter(mobile_number=identity)
        
        if (old_response != None):
            foo = text.split(";")
            self.issue = Choice.objects.get(short_code=foo[0])
            self.age = foo[1]
            self.gender = foo[2]
            self.mobile_number = identity
            our_response = "Thanks for participating. You selected %s." % (self.issue)
        else:
            pass
        self.save()
        return our_response
