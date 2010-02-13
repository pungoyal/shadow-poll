#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import rapidsms
from datetime import datetime, timedelta
from rapidsms.message import StatusCodes

# App dependencies: logger, reporter
from logger.models import IncomingMessage

# number of duplicate messages during TIMEOUT
# before we decide we are talking to a bot
MAX_NUM_DUPLICATES = 4
# timeout in minutes 
# before we decide we are talking to a bot
TIMEOUT = 3

class App(rapidsms.app.App):
    """When an incoming message is received, this application is notified
       last, to send a default response in case no other App responded."""
    
    PRIORITY = "lowest"
    
    def handle(self, msg):
        if not msg.responses and not msg.persistant_connection.is_bot:
            if not _test_and_set_bot(msg.persistant_connection):
                # TODO: i18n from the reporters app
                msg.respond("We didn't understand your response.", 
                            StatusCodes.GENERIC_ERROR)
                return True

def _test_and_set_bot(connection):
    """ Test whether this connection is a bot. 
    If true, set conn.is_bot and return True
    If false, return False
    
    We do not place this in the reporters model 
    since it creates a dependency on logger
    
    Note that we assume that once a connection is marked 'bot'
    it stays 'bot' until an administrator remarks it
    """
    history = IncomingMessage.objects.filter(
        identity=str(connection.identity), 
        backend=str(connection.backend)
        ).order_by('-pk')[:MAX_NUM_DUPLICATES]
    if history and history.count() == MAX_NUM_DUPLICATES:
        # if the last X messages had the same text
        # and all occurred within Y minutes of each
        # assume we are talking to a bot and ignore
        all_same = True
        for i in range(1, MAX_NUM_DUPLICATES):
            all_same = all_same and ( history[i].text == history[i-1].text )
        if all_same and history[MAX_NUM_DUPLICATES-1].received > (datetime.now() - timedelta(minutes=TIMEOUT)):
            connection.is_bot = True
            connection.save()
            return True
    return False
