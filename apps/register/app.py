# -*- coding: utf-8 -*-
import rapidsms
from rapidsms.webui import settings
from rapidsms.i18n import ugettext_from_locale as _t
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
            r = Registration()
            if not hasattr(message, 'language'):
                # fail gracefully
                message.language = settings.LANGUAGE_CODE
            try:
                r.parse(message)
                # ro: why on earth is a successful outcome marked with an 'error_id'?
                message.error_id = "err2"
            except Exception, e:
                message.error_id = "err1"
            message.respond(_t(response, message.language ))
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
