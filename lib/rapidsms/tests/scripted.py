# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

import sys
from django.utils.encoding import smart_str
from harness import MockRouter, EchoApp
from rapidsms.backends.backend import Backend
from rapidsms.message import Message
import unittest, re
try:
    from django.test import TestCase
except:
    from unittest import TestCase
from datetime import datetime

class MetaTestScript (type):
    def __new__(cls, name, bases, attrs):
        for key, obj in attrs.items():
            if key.startswith("test") and not callable(obj):
                cmds = TestScript.parseScript(obj)
                def wrapper (self, cmds=cmds):
                    return self.runParsedScript(cmds)
                attrs[key] = wrapper
        return type.__new__(cls, name, bases, attrs)

class TestScript (TestCase):
    __metaclass__ = MetaTestScript

    """
    The scripted.TestScript class subclasses unittest.TestCase
    and allows you to define unit tests for your RapidSMS apps
    in the form of a 'conversational' script:
    
        from myapp.app import App as MyApp
        from rapidsms.tests.scripted import TestScript

        class TestMyApp (TestScript):
            apps = (MyApp,)
            testRegister = \"""
               8005551212 > register as someuser
               8005551212 < Registered new user 'someuser' for 8005551212!
            \"""

            testDirectMessage = \"""
               8005551212 > tell anotheruser what's up??
               8005550000 < someuser said "what's up??"
            \"""

    This TestMyApp class would then work exactly as any other
    unittest.TestCase subclass (so you could, for example, call
    unittest.main()).
    """
    apps = None

    def setUp (self):
        self.router = MockRouter()
        self.backend = Backend(self.router)
        self.router.add_backend(self.backend)
        if not self.apps:
            raise Exception(
                "You must define a list of apps in your TestScript class!")
        for app_class in self.apps:
            app = app_class(self.router)
            self.router.add_app(app)

    def tearDown (self):
        if self.router.running:
            self.router.stop() 

    @classmethod
    def parseScript (cls, script):
        cmds  = []
        for line in map(lambda(x): x.strip(), script.split("\n")):
            if not line or line.startswith("#"): continue
            tokens = re.split(r'([<>])', line, 1)
            num, dir, txt = map(lambda (x):x.strip(), tokens)
            # allow users to optionally put dates in the number
            # 19232922@200804150730
            if "@" in num:
                num, datestr = num.split("@")
                date = datetime.strptime(datestr, "%Y%m%d%H%M")
            else:
                date = datetime.now()
            cmds.append((num, date, dir, txt))
        return cmds
     
    def runParsedScript (self, cmds):
        self.router.start()
        last_msg = ''
        for num, date, dir, txt in cmds:
            if dir == '>':
                last_received = txt
                msg = self.backend.message(num, txt)
                msg.date = date 
                self.backend.route(msg)  
            elif dir == '<':
                msg = self.backend.next_message()
                if sys.stdout.encoding:
                    # Encode 'strange' characters for proper output on the console
                    # so we don't get 'unprintable assertion errors'
                    encoding = sys.stdout.encoding
                    try:
                        txt = txt.encode(sys.stdout.encoding, 'replace')
                    except UnicodeDecodeError:
                        # This error occurs when the input is not standardized (i.e. unicode)
                        self.fail("Could not encode unit test string to stdout character encoding. Make sure your RapidSMS unit tests are unicode strings!")
                else:
                    """ 
                    This should really be ascii (since this is the most platform-independent)
                    Then again, maybe we should just assume anyone mucking around in unicode
                    has a unicode-friendly console?
                    """
                    encoding = 'utf-8'
                
                if len(txt) == 0 and msg is None:
                    last_msg = txt
                    continue
                    
                # The following 3 try...catch blocks handle the case where the unit test strings
                # are not properly decoded in tests.py. Basically, there is no way to reliably
                # determine the encoding of a character > 127 bits a posteriori. The best we can
                # do is catch errors when these strings prove incompatible and then print out
                # as much as we can.
                try:
                    msgIsNotNoneMsg = "Message was not returned.\nMessage: '%s'\nExpecting: '%s')" % (last_msg, txt)
                except UnicodeDecodeError:
                    msgIsNotNoneMsg = "Message was not returned.\nMessage: '%s')" % (last_msg)
                self.assertTrue(msg is not None, msgIsNotNoneMsg)
                
                if sys.stdout.encoding:
                    msg.text = msg.text.encode(sys.stdout.encoding, 'replace')

                try:
                    msgWrongRecipient = "Expected to send to %s, but message was sent to %s\nMessage: '%s'" % \
                                        (num, msg.peer, last_msg)
                except UnicodeDecodeError:
                    msgWrongRecipient = "Expected to send to one number but got sent to another. \nMessage: '%s'" % (last_msg)
                self.assertEquals(msg.peer, num, msgWrongRecipient)
                
                try:
                    msgUnexpectedReceipt = "\nMessage: %s\nReceived text: %s\nExpected text: %s\n" % \
                                          (last_msg, msg.text, txt)
                except UnicodeDecodeError: 
                    msgUnexpectedReceipt = "Unexpected response. \nReceived text: %s" % \
                                          (msg.text)                    
                self.assertEquals(msg.text.strip(), txt.strip(), msgUnexpectedReceipt.encode(encoding))

                last_msg = txt
        self.router.stop()

    def runScript (self, script):
        self.runParsedScript(self.parseScript(script))

class MockTestScript (TestScript):
    apps = (EchoApp,)

    testScript = """
        8005551212 > hello
        8005551212 < 8005551212: hello
    """
    testScript2 = """
        1234567890 > echo this!
        1234567890 < 1234567890: echo this!
    """
    
    def testClosure (self):
        self.assertEquals(type(self.testScript.func_defaults), tuple)
        self.assertEquals(type(self.testScript.func_defaults[0]), list)
        self.assertNotEquals(self.testScript.func_defaults,
                             self.testScript2.func_defaults)

    def testRunScript (self):
        self.runScript("""
            2345678901 > echo?
            2345678901 < 2345678901: echo?
        """)

if __name__ == "__main__":
    unittest.main()
