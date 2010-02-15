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
        message.language = "ar"
        t = Translator()
        incoming = message.text
        translated = t.translate(incoming)

        if t.is_english(incoming):
            message.language = "en"

        message.text = translated
        self.debug("Translated %s to %s" % (incoming, translated))

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
