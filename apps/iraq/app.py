import rapidsms

from models import *
from datetime import datetime

class App (rapidsms.app.App):
    def handle (self, message):
        number = message.connection.identity
        querySet = PollResponse.objects.filter(mobile_number=number)[:1]

        if (querySet.count() == 0):
            poll_response = PollResponse(mobile_number = number)
        else:
            poll_response = querySet[0]
        
        response_text = poll_response.generate_response(message.text)
        message.respond(response_text)
        return True
