# -*- coding: utf-8 -*-
import rapidsms
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
        if message.text.lower().startswith("register") or message.text.lower().startswith(u'تسجيل'):
            try:
                r = Registration()
                r.parse(message)
                message.respond(_t("Thanks for registering.", message.persistant_connection.language ))
            except Exception, e:
                message.respond(_t("Register not understood."), message.persistant_connection.language )
            finally:
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
