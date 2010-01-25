import rapidsms
from models import *

class App (rapidsms.app.App):
    def start (self):
        """Configure your app in the start phase."""
        pass

    def parse (self, message):
        """Parse and annotate messages in the parse phase."""
        pass

    def handle (self, message):
        if message.text.lower().startswith("register"):
            try:
                Registration(mobile_number = message.connection.identity).parse(message.text)
                message.respond("Thanks for registering for the survey.")
                return True
            except:
                message.respond("We could not understand the register message. Please send as - register survey governorate district")

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
