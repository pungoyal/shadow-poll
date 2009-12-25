#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import rapidsms
from models import *

class App(rapidsms.app.App):
    
    def handle(self, msg):
        for r in Responder.objects.filter(trigger=msg.text):
            msg.respond(r.response)
            return True
