#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import rapidsms
from rapidsms.message import StatusCodes

class App(rapidsms.app.App):
    """When an incoming message is received, this application is notified
       last, to send a default response in case no other App responded."""
    
    PRIORITY = "lowest"
    
    def handle(self, msg):
        if not msg.responses:
            
            # TODO: i18n from the reporters app
            msg.respond("We didn't understand your response.", StatusCodes.GENERIC_ERROR)
            return True
