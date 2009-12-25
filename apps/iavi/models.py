from django.db import models
from reporters.models import Reporter, PersistantConnection, Location 
from tree.models import Session
from django.contrib.auth.models import User


class IaviReporter(Reporter):
    """This model represents a reporter in IAVI.  They are an extension of
       the basic reporters, but also have PIN numbers"""  
    pin = models.CharField(max_length=4, null=True, blank=True)
    registered = models.DateTimeField()
    
    @property
    def study_id(self):
        # use some implicit knowledge about how we're storing the
        # aliases to get these.
        if "-" in self.alias:
            return self.alias.split('-')[1]
        return None
        
    @classmethod
    def get_alias(klass, location, study_id):
        return location + "-" + study_id
    
    def __unicode__(self):
        if self.connection():
            return self.connection().identity
        return self.alias
        
        
class IaviProfile(models.Model):
    """ A user profile for IAVI website users.  This allows us to attach
        additional information to the users so that we can access these
        fields from within our views """
    # This is a required field for Django's profile settings
    user = models.ForeignKey(User, unique=True, editable=False)
    # Optionally tie this to an SMS reporter
    reporter = models.ForeignKey(IaviReporter, null=True, blank=True)
    # Users can be associated with zero or more locations
    locations = models.ManyToManyField(Location, null=True, blank=True)
    
    class Meta:
        permissions = (
            ("can_read_participants", "Can view participant data"),
            ("can_write_participants", "Can edit participant data"),
            ("can_see_data", "Can view study data"),
            ("is_admin", "Is an administrator for IAVI"),
        )

    def __unicode__(self):
        return "%s --> %s" % (self.user, self.reporter)
    
class StudyParticipant(models.Model):
    """ This represents a participant in the IAVI study. """
    reporter = models.ForeignKey(IaviReporter)
    start_date = models.DateField()
    # if the end_date is blank the study will go indefinitely
    end_date = models.DateField(null=True, blank=True)
    notification_time = models.TimeField()
    
    def __unicode__(self):
        return "%s: %s - %s" % (self.reporter, self.start_date, self.end_date)
    

class TestSession(models.Model):
    TEST_STATUS_TYPES = (
                         ("A", "Active"),
                         ("P", "Passed"),
                         ("F", "Failed")
                         )
    
    date = models.DateTimeField(auto_now_add=True)
    initiator = models.ForeignKey(PersistantConnection)
    tester = models.ForeignKey(IaviReporter)
    tree_session = models.ForeignKey(Session, null=True, blank=True)
    status = models.CharField(max_length=1, choices=TEST_STATUS_TYPES)
    
    def __unicode__(self):
        return "%s --> %s" % (self.initiator, self.status)
    
class Report(models.Model):
    STATUS_TYPES = (
        ('C', 'Canceled'),
        ('A', 'Active'),
        ('F', 'Finished'),
    )

    reporter = models.ForeignKey(IaviReporter)
    session = models.ForeignKey(Session)
    started = models.DateTimeField()
    completed = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_TYPES)
    
    @classmethod
    def pending_sessions(klass):
        return klass.objects.filter(completed=None)
    
    def __unicode__(self):
        return "%s: %s (%s)" % (self.reporter, self.started, self.get_status_display())
    
    
class KenyaReport(Report):
    sex_past_day = models.PositiveIntegerField(null=True, blank=True)
    condoms_past_day = models.PositiveIntegerField(null=True, blank=True)
    
    

class UgandaReport(Report):
    sex_with_partner = models.BooleanField(null=True, blank=True)
    condom_with_partner = models.BooleanField(null=True, blank=True)
    sex_with_other = models.BooleanField(null=True, blank=True)
    condom_with_other = models.BooleanField(null=True, blank=True)
    