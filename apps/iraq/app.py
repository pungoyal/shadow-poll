import rapidsms
import re

from models import *
from datetime import datetime

class App (rapidsms.app.App):
    def handle (self, message):
        response = message.text.split(";")
        answer = response[0]
        self.debug("answer %s", answer)
        selected_choice = Choice.objects.get(short_code=answer)
        Respondent(answer=selected_choice, age=response[1], gender=response[2]).save()
        message.respond("Thanks for your participation. You selected %s." % (selected_choice))
        return True
