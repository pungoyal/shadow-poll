#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import rapidsms
import re

class App(rapidsms.app.App):
    """This app allows callers to send in messages on behalf of other
       callers - even across different backends. This is most useful
       when RapidSMS explodes, and drops important messages. Rather
       than asking the caller to try again, we can inject the message
       on their behalf, ensuring that they receive their response. To
       inject a message, send:
       
       inject <BACKEND> <IDENTITY> <TEXT>"""
    
    prefix  = re.compile(r'^inject(?:\s+(.+))?$', re.I)
    pattern = re.compile(r'^\s*(\S+?)\s+(\S+?)\s+(.+)$', re.I)
    
    def handle(self, msg):
        
        # check if this message was intended
        # for us, via a very liberal regex
        m = self.prefix.match(msg.text)
        if m is None:
            return False
            
        # extract the arguments via a proper regex,
        # and abort if it didn't contain everything
        m = self.pattern.match(m.group(1))
        if m is None:
            msg.respond("Invalid inject syntax.\n" +\
                        "Try: inject <BACKEND> <IDENTITY> <TEXT>")
            return True
        
        # resolve the message into a real backend
        be_name, identity, text = m.groups()
        backend = self.router.get_backend(be_name)
        
        # check that the target backend was valid
        if backend is None:
            msg.respond("There is no backend named: %s. Try one of: %s" %
                (be_name, ", ".join([be.slug for be in self.router.backends])))
        
        # create and send te message, as if it
        # had originated from the named backend
        else:
            backend.route(backend.message(identity, text))
            msg.respond("Your message was injected.")
        
        # short-circuit
	    return True
