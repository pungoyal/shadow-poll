#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

import re
import urllib
import urlparse
from datetime import datetime
from select import select
from SocketServer import ThreadingMixIn
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import rapidsms

def _uni(str):
    ''' Make inbound a unicode str Decoding from utf-8 if needed '''
    try:
        return unicode(str)
    except:
        return unicode(str,'utf-8')

def _str(uni):
    ''' Make inbound a string Encoding to utf-8 if needed '''
    try:
        return str(uni)
    except:
        return uni.encode('utf-8')

class HttpServer(HTTPServer, ThreadingMixIn):
    
    def handle_request (self, timeout=1.0):
        # don't block on handle_request
        reads, writes, errors = (self,), (), ()
        reads, writes, errors = select(reads, writes, errors, timeout)
        if reads:
            HTTPServer.handle_request(self)

class Backend(rapidsms.backends.Backend):
    ''' Kannel backend for rapidSMS

    Should work with most Kannel configuration
    Although only tested with SMPP to SMS Aggregator.
    Check if Kannel is UP on configuration by testing sendsms HTTP server'''


    def configure(self, host="localhost", port=8080, kannel_host='localhost', kannel_port=13013, kannel_username='kannel', kannel_password="kannel"):
              
        self.kannel_host        = kannel_host
        self.kannel_port        = int(kannel_port)
        self.kannel_username    = kannel_username
        self.kannel_password    = kannel_password

        KannelHTTPHandler.kannel_host     = self.kannel_host
        KannelHTTPHandler.kannel_port     = self.kannel_port
        KannelHTTPHandler.kannel_username = self.kannel_username
        KannelHTTPHandler.kannel_password = self.kannel_password

        self.server = HttpServer((host, int(port)), KannelHTTPHandler)
        self.type = "KANNEL"

        # set this backend in the server instance so it 
        # can callback when a message is received
        self.server.backend = self
        KannelHTTPHandler.backend       = self
        
        self._slug = "kannel"

        try:
            # connect to Kannel sendsms server to test if Kannel is up.
            url = "http://%s:%d" % (self.kannel_host, self.kannel_port)
            res = urllib.urlopen(url)
        except Exception, err:
            raise Exception("Unable to connect to Kannel: %s" % err)
        if not res.code in (200, 202, 400, 404):
            raise Exception("Unable to connect to Kannel: %s" % res.code)
        
    def run (self):
        while self.running:
            if self.message_waiting:
                msg = self.next_message()
                KannelHTTPHandler.outgoing(msg)
            self.server.handle_request()

class KannelHTTPHandler(BaseHTTPRequestHandler):

    def respond(self, code, msg):
        self.send_response(code)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(_str(msg))

    def log_message(self, format, *args):
        self.__class__.debug(format, *args)

    def log_debug(self, format, *args):
        self.__class__.debug(format, *args)

    def log_error(self, format, *args):
        self.__class__.error(format, *args)

    def do_GET(self):
        ''' called on SMS arrival by Kannel

            sender and message as parameter
            http://server:port/+number/mymessage'''
    
        def _plus(str):
                return str.replace('%2B', '+')

        # answer to / for testing purpose
        if self.path == "/":
            self.respond(200, "working")
            return
        
        # accepts /+digits/message
        request_regex   = re.compile(r"^/([\%B0-9]+)/([^?]*)")
        match           = request_regex.match(self.path)

        if match:
            
            url = urlparse.urlparse(self.path)
            params = query_string_to_dict(url.query)
                    
            # build the message
            sender_id   = _plus(match.group(1))
            input = match.group(2)
            if 'charset' in params and params['charset'].lower() == 'utf-8':
                # if mo-recode is True, then kannel has already transformed
                # ucs2 to more standard utf-8
                text = urllib.unquote_plus(input).decode('utf-8')
            else:
                # otherwise, we just assume we're dealing with regular ascii
                text = _str(urllib.unquote_plus(input))
            
            # get time
            received = datetime.utcnow()
            
            msg = self.server.backend.message(
                sender_id, 
                text,
                date=received
                )

            # send the message to router
            self.server.backend.route(msg)

            # send HTTP response
            self.respond(200, '')
            return
            
        return

    @classmethod
    def debug(cls, format, *args):
        cls.backend.debug(format, *args)

    @classmethod
    def error(cls, format, *args):
        cls.backend.error(format, *args)

    @classmethod
    def outgoing(cls, msg):
        '''Used to send outgoing messages through this interface.'''

        cls.debug("sending message: %s to %s. %s chars" % (msg.text, msg.connection.identity, msg.text.__len__()))

        # remove non digit from number
        target = re.compile('\D').sub("", msg.connection.identity)
        
        # urlencode for HTTP get
        coding = 0
        try:
            message = msg.text.encode('latin1')
        except Exception, e:
            coding = 2
            message = msg.text.encode('utf-8')
        msg_enc = urllib.quote_plus(message)
        
        # send HTTP GET request to Kannel
        try:
            url = "http://%s:%d/cgi-bin/sendsms?username=%s&password=%s&to=%s&from=&text=%s"\
	            % (cls.kannel_host, cls.kannel_port, cls.kannel_username, cls.kannel_password, target, msg_enc)
            if coding == 2:
                url = url + "&charset=utf-8&coding=2"
            res = urllib.urlopen(url)
            ans = res.read()
        except Exception, err:
            cls.error("Error sending message: %s" % err)
            return False

        if res.code   == 202:
            if ans.startswith('0: Accepted'):
                kw  = 'sent'            
            elif ans.startswith('3: Queued'):
                kw  = 'queued'
            else:
                kw  = 'sent'

            cls.debug("message %s: %s" % (kw, message))

        elif res.code == 503:
            cls.error("message failed to send (temporary error): %s" % ans)
        else:
            cls.error("message failed to send: %s" % ans)

def query_string_to_dict(query):
    params = {}
    for keyval in query.split("&"):
        keyval = keyval.split('=')
        if len(keyval) == 2:
            key, val = keyval
            params[key] = val
    return params
