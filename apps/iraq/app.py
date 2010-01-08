import rapidsms
import re

from models import *
from datetime import datetime

class App (rapidsms.app.App):
    def handle (self, message):
        querySet = PollResponse.objects.filter(mobile_number=identity)[:1]

        if (querySet.count() == 0):
            poll_response = PollResponse()
        else:
            poll_response = querySet[0]
        
        response_text = poll_response.generateResponse(message.text, message.connection.identity)
        message.respond(response_text)
        return True
