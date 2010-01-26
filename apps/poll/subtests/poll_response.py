from django.test import TestCase
import rapidsms
from poll.models import *
from register.models import *

class PollResponseTest(TestCase):
    fixtures = ['poll_responses']
    def setUp(self):
        self.poll_response = PollResponse(mobile_number = 1000)

    def test_parse_response(self):
        response = self.poll_response.generate_response("ED 16 F 110001")

        self.assertEquals(self.poll_response.age, '16')
        self.assertEquals(self.poll_response.gender,'F')
        self.assertEquals(self.poll_response.location,"110001")
        self.assertEquals(response, "Thank you for voting. You selected Education as your number one issue.")
        
    def test_location_is_optional(self):
        response = self.poll_response.generate_response("ED 12 M")

        self.assertEquals(self.poll_response.age, '12')
        self.assertEquals(self.poll_response.gender,'M')
        self.assertEquals(self.poll_response.location, None)
        self.assertEquals(response, "Thank you for voting. You selected Education as your number one issue.")

    def test_extra_info_in_message_is_ignored(self):
        response = self.poll_response.generate_response("ED 16 F 110001 Foo Bar")

        self.assertEquals(self.poll_response.age, '16')
        self.assertEquals(self.poll_response.gender,'F')
        self.assertEquals(self.poll_response.location,"110001")
        self.assertEquals(response, "Thank you for voting. You selected Education as your number one issue.")

    def test_incorrect_response_message_on_bad_parsing(self):
        error_message = "Sorry, we did not understand your response. Please re-send as - issue age gender area"

        response = self.poll_response.generate_response("ED M 12 110001")
        self.assertEquals(response, error_message)
        response = self.poll_response.generate_response("EV")
        self.assertEquals(response, error_message)
        response = self.poll_response.generate_response("ED 12")
        self.assertEquals(response, error_message)
        response = self.poll_response.generate_response("ED")
        self.assertEquals(response, error_message)

    def test_add_location_from_registration(self):
        r = Registration(governorate = 1, district = 2)
        p = PollResponse()
        p.set_location(r)
        self.assertEquals(p.governorate, 1)
        self.assertEquals(p.district, 2)
        
    def testToString(self):
        choice = Choice.objects.get(id=2)
        p = PollResponse(issue=choice, age=10, location=110001, gender="M")

        self.assertEquals(str(p), "%s 10 M 110001" %choice)
