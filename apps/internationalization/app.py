import rapidsms
from models import *

class App (rapidsms.app.App):
#    PRIORITY = "first"

    def priority(self):
        return 1

    def start (self):
        """Configure your app in the start phase."""
        pass

    def parse (self, message):
        message.language = "en"
        t = Translator()
        processed = t.understand_and_translate_if_required(message.text)

        if processed:
            message.language = "ar"
            message.text = processed

    def handle (self, message):
        """Add your main application logic in the handle phase."""
        pass

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
