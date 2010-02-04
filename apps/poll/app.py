import rapidsms

from models import *
from register.models import *
from datetime import datetime
from poll.models import Question

class App (rapidsms.app.App):
    def parse(self, message):
        pass
        
    def handle (self, message):
        phone_number = message.connection.identity
        
        # allow them to query the question
        if message.text.lower().startswith("poll"):
            # return any question
            qs = Question.objects.all()
            if qs:
                message.respond(qs[0].question)
            else: 
                message.respond("No survey questions defined")
            return True
        
        # allow them to submit a response
        result = Registration.objects.filter(phone__identity = phone_number)
        poll_response = PollResponse(mobile_number = phone_number)
        if(result != None and result.count() > 0):
            poll_response.set_location(result.iterator().next())
        try:
            response_text = poll_response.generate_response(message.text)
        except ValueError:
            # message was not a poll response. 
            return False
        message.respond(response_text)
        return True
