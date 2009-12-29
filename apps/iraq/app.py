import rapidsms
import re

from models import *
from datetime import datetime

class App (rapidsms.app.App):
    def handle (self, message):
        response = Responder(message).response()
        message.respond(response)
        return True
