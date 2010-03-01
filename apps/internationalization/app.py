import rapidsms
from models import *
from utils import get_translation as _

class App (rapidsms.app.App):
    """
    The priority of internationalization.app should be high, but not highest
    (since logger should be the highest)
    """
    PRIORITY = "high"
    t = None

    def start (self):
        """Configure your app in the start phase."""
        self.t = Translator()

    def parse (self, message):
        msg_text = message.text
        message.language = "ar"
        if self.t.is_english(msg_text):
            message.language = "en"
        
        translated = self.t.translate(self.t.to_lower(msg_text, message.language))
        
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
        message.text = _(message.text, message.language)

    def stop (self):
        """Perform global app cleanup when the application is stopped."""
        pass
