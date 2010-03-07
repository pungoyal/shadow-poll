from django.test import TestCase
from rapidsms import *
from rapidsms.connection import *
from rapidsms.tests.scripted import TestScript
from register.models import *
from reporters.models import PersistantBackend, PersistantConnection, Reporter
from register.app import App

class RegistrationTest(TestCase):
    fixtures = ['registration']
    
    def setUp(self):
        self.backend = PersistantBackend(slug="MockBackend")
        self.backend.save()
        self.reporter = Reporter(alias="ReporterName")
        self.reporter.save()
        self.connection = Connection(backend=self.backend, identity="1000")
        self.pconnection = PersistantConnection(backend=self.backend, 
                                                reporter=self.reporter, 
                                                identity="1000")
        self.pconnection.save()
        self.reporter.connections.add(self.pconnection)
        
        message = Message(text='register poll 100 1001', connection=self.connection)
        message.persistant_connection = self.pconnection

    
    def test_parse(self):
        # there should only be one registration object in this fixture
        self.reg = Registration.objects.get()
        self.assertEquals(self.reg.public_identifier, 'poll')
        self.assertEquals(self.reg.governorate, "10")
        self.assertEquals(self.reg.district, "8")
        self.assertEquals(self.reg.phone.identity, "1000")

    def test_load_by_mobile_number(self):
        query_result = Registration.objects.filter(phone__identity = '100')
        self.assertEquals(query_result.count(), 0)

        query_result = Registration.objects.filter(phone__identity = '1000')
        self.assertEquals(query_result.count(), 1)
        r = query_result.iterator().next()
        self.assertNotEquals(r, None)

    def test_to_string(self):
        r = Registration()
        r.public_identifier = "Poll"
        r.governorate = "12"
        r.district = "8"
        r.phone = self.pconnection
        self.assertEquals(str(r), "1000 Poll 12 8")
