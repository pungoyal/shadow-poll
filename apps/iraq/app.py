import rapidsms
import re

from models import *
from datetime import datetime

class App (rapidsms.app.App):
    def handle (self, message):
        response = Responder(message.text).response()
        response.mobile_number = message.connection.identity
        response.save()
        message.respond(response.our_response)
        return True
