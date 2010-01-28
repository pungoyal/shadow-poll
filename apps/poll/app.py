import rapidsms

from models import *
from register.models import *
from datetime import datetime
from poll.models import Phone

class App (rapidsms.app.App):
    def parse(self, message):
        # same as in the reporter app
        phone = Phone.from_message(message)
        message.persistant_connection = phone
        phone.seen()
        
    def handle (self, message):
        phone_number = message.connection.identity

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
