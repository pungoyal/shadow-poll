from django.test import TestCase
from apps.poll.models import User
from apps.register.models import Registration
from reporters.models import Reporter, PersistantConnection, PersistantBackend

class UserTest(TestCase):
    def setUp(self):
        self.backend = PersistantBackend(slug="AnotherMockBackend")
        self.backend.save()
        self.reporter = Reporter(alias="ReporterName")
        self.reporter.save()
        self.pconnection = PersistantConnection(backend=self.backend, 
                                                reporter=self.reporter, 
                                                identity="1001")
        self.pconnection.save()
        self.reporter.connections.add(self.pconnection)
        Registration(governorate = 3, district = 4, phone = self.pconnection).save()

    def test_set_user_geolocation(self):
        user = User()
        user.set_user_geolocation_if_registered(self.pconnection)
        self.assertEquals(user.governorate , 3)
        self.assertEquals(user.district, 4)
    

    def test_dont_set_geolocation_when_not_present(self):
        user = User()
        user.set_user_geolocation_if_registered(None)
        self.assertEquals(user.governorate , None)
        self.assertEquals(user.district, None)
        
