import rapidsms
import re

from models import *
from datetime import datetime

class App (rapidsms.app.App):
    def handle (self, message):

        poll_response = PollResponse().parse(message.text, message.connection.identity)
        poll_response.save()
        message.respond(poll_response.our_response)
        return True
