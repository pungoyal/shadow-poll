import rapidsms

from models import *
from register.models import *
from datetime import datetime

class App (rapidsms.app.App):
    def handle (self, message):
        phone_number = message.connection.identity

        r = Registration.objects.filter(mobile_number = phone_number)
        if(r != None):
            pass
        
        poll_response = PollResponse(mobile_number = phone_number)
        response_text = poll_response.generate_response(message.text)
        message.respond(response_text)
        return True
