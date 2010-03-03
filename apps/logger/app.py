#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import rapidsms

import models
from models import OutgoingMessage, IncomingMessage

class App(rapidsms.app.App):
    """ 
    logger app must be the first one called on incoing
    and the last one called on outgoing so that we can
    properly catch the end user's experience
    (after translation, censorship, etc.)
    """
    PRIORITY = "highest"
    
    def parse(self, message):
        # make and save messages on their way in and 
        # cast connection as string so pysqlite doesnt complain
        msg = IncomingMessage(identity=message.connection.identity, text=message.text,
            backend=message.connection.backend.slug)
        msg.save()
        self.debug(msg)
    
    def outgoing(self, message):
        # make and save messages on their way out and 
        # cast connection as string so pysqlite doesnt complain
        msg = OutgoingMessage.objects.create(identity=message.connection.identity, text=message.text, 
                                             backend=message.connection.backend.slug)
        self.debug(msg)
        # inject this id into the message object.
        message.logger_id = msg.id;