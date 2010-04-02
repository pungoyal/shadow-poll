from rapidsms.tests.scripted import TestScript
from django.test import TestCase
from apps.reporters.models import Reporter, PersistantConnection, PersistantBackend
from app import App

from message_parser import BulkMessageProcessor

class TestApp (TestCase):
    apps = (App,)
    fixtures = ['poll_interactive']
    
    def setUp(self):
        backend = PersistantBackend(slug="MockBackend")
        backend.save()
        reporter = Reporter(alias="ReporterName")
        reporter.save()
        self.connection = PersistantConnection(backend=backend, reporter=reporter, identity="1000", governorate = 2,
                                          district = 4)
        self.connection.save()

    def test_message_parser_age_sex(self):
        msgProcessor = BulkMessageProcessor("bulk m 7 a a b c d")
        parsed_msg = msgProcessor.parse_and_create_user(self.connection, "bulk m 7 a a b c d")
        self.assertEquals(parsed_msg[-1], 'a')
        self.assertEquals(parsed_msg[-2], 'a b c')
    
    def test_save_user_response(self):
        msgProcessor = BulkMessageProcessor("bulk m 7 a a b c d")
        parsed_msg = msgProcessor.parse_and_create_user(self.connection, "bulk m 7 a a b c d")
        
        response = msgProcessor.save_user_and_responses(parsed_msg)
        self.assertEquals(response, "Thanks")

