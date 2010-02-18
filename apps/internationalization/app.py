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
        t = Translator()
        msg_text = message.text
        message.language = "ar"
        if t.is_english(msg_text):
            message.language = "en"
        
        translated = t.translate(t.to_lower(msg_text, message.language))
        
        message.text = translated
        self.debug("Translated '%s' to '%s'" % (msg_text, translated))

    def handle (self, message):
        """Add your main application logic in the handle phase."""
        pass

    def cleanup (self, message):
        """Perform any clean up after all handlers have run in the
           cleanup phase."""
        pass

    def outgoing (self, message):
        if hasattr(message, 'error_id'):
            t = Translator()
            self.error_msg = t.get_error_text(message.error_id, message.language)
            if self.error_msg:
                message.text = self.error_msg

    def stop (self):
        """Perform global app cleanup when the application is stopped."""
        pass
