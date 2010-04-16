from rapidsms.tests.scripted import TestScript
from django.test import TestCase
from apps.reporters.models import Reporter, PersistantConnection, PersistantBackend
from apps.poll.models import User

from message_parser import BulkMessageProcessor

class BulkMessageProcessorTest (TestCase):    
    def setUp(self):
        backend = PersistantBackend(slug="MockBackend")
        backend.save()
        reporter = Reporter(alias="ReporterName")
        reporter.save()
        self.connection = PersistantConnection(backend=backend, reporter=reporter, identity="1000", governorate = 2,
                                          district = 4)
        self.connection.save()

    def test_parse_response_for_answers(self):
        processor = BulkMessageProcessor()
        answers = processor.parse_and_create_user("bulk 7 m a a b c d", self.connection)
        self.assertEquals(answers[0], 'a')
        self.assertEquals(answers[1], 'a b c')
        self.assertEquals(answers[2], 'd')

    def test_parse_response_for_user_information(self):
        processor = BulkMessageProcessor()

        answers = processor.parse_and_create_user("bulk 13 f a a b c d", self.connection)
        self.assertEquals(processor.user.age, 13)
        self.assertEquals(processor.user.gender, 'f')

        response = processor.save_user_and_responses(answers)
        self.assertEquals(response, "thanks")
        user = User.objects.latest('id')
        self.assertEquals(user.age, 13)
        self.assertEquals(user.gender, 'f')

    def test_error_for_incorrect_user_information(self):
        processor = BulkMessageProcessor()
        answers = processor.parse_and_create_user("bulk m 7 a a b c d", self.connection)
        self.assertEquals(answers, 'bulk_response_error')
        response = processor.save_user_and_responses(answers)
        self.assertEquals(response, 'bulk_response_error')

    def test_save_user_response(self):
        processor = BulkMessageProcessor()
        answers = processor.parse_and_create_user("bulk 7 m a a b c d", self.connection)
        response = processor.save_user_and_responses(answers)
        self.assertEquals(response, "thanks")

