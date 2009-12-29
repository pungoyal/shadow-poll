import rapidsms
import re

from models import *
from datetime import datetime

class App (rapidsms.app.App):
    def start (self):
        """Configure your app in the start phase."""
        pass

    def parse (self, message):
        """Parse and annotate messages in the parse phase."""
        pass

    def handle (self, message):
        response = message.text.split(";")
        self.debug("answer %s", response[0])
        Respondent(answer=response[0], age=response[1], gender=response[2]).save()
        message.respond("Thanks for your participation.")
        return True

    def cleanup (self, message):
        """Perform any clean up after all handlers have run in the
           cleanup phase."""
        pass

    def outgoing (self, message):
        """Handle outgoing message notifications."""
        pass

    def stop (self):
        """Perform global app cleanup when the application is stopped."""
        pass
