import rapidsms

from models import *
from register.models import *
from datetime import datetime

class App (rapidsms.app.App):
    def handle (self, message):
        phone_number = message.connection.identity

        result = Registration.objects.filter(mobile_number = phone_number)
        poll_response = PollResponse(mobile_number = phone_number)
        if(result != None and result.count() > 0):
            poll_response.set_location(result.iterator().next())

        response_text = poll_response.generate_response(message.text)
        message.respond(response_text)
        return True
