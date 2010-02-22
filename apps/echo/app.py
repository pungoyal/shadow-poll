#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

import rapidsms
import re

class App(rapidsms.app.App):
    prefix = re.compile(r'^echo\s+',re.I)
    def handle(self, message):
        self.debug("got message %s", message.text)
        # for purposes of demonstration, have this 
        # app respond to everything
        response = "You said: %s" % message.text
        self.debug("responding with %s", response)
        message.respond(response)
#        if self.prefix.search(message.text):
#            response = self.prefix.sub("",message.text)
#            self.debug("responding with %s", response)
#            message.respond(response)
        return True
