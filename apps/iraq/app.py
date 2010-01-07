import rapidsms
import re

from models import *
from datetime import datetime

class App (rapidsms.app.App):
    def handle (self, message):

        poll_response = PollResponse()
        our_response = poll_response.generateResponse(message.text, message.connection.identity)
        message.respond(our_response)
        return True
