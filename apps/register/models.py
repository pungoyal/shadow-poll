from django.db import models

class Registration(models.Model):
    public_identifier = models.CharField(max_length=10)
    governorate = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    mobile_number = models.IntegerField()
    
    def parse(self, message):
        foo = message.split(' ')
        self.public_identifier = foo[1]
        self.governorate = foo[2]
        self.district = foo[3]
        self.save()

    def __unicode__(self):
        return "%s %s %s %s" % (self.mobile_number, self.public_identifier, self.governorate, self.district)
