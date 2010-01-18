import rapidsms

from models import *
from datetime import datetime

class App (rapidsms.app.App):
    def handle (self, message):
        poll_response = PollResponse(mobile_number = message.connection.identity)
        response_text = poll_response.generate_response(message.text)
        message.respond(response_text)
        return True
