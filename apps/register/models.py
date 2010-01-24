from django.db import models

class Registration(models.Model):
    public_identifier = models.CharField(max_length=10)
    governorate = models.IntegerField()
    district = models.IntegerField()
    number = models.IntegerField()
    
    def parse(self, message):
        foo = message.split(' ')
        self.public_identifier = foo[1]
        self.governorate = foo[2]
        self.district = foo[3]
        self.save()
