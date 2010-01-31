#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import unittest
import smtplib, imaplib
import time
from email.mime.text import MIMEText
from email import message_from_string

from rapidsms.message import Message
from harness import MockRouter, EchoApp
from rapidsms.backends.email import Backend, Connection



CONF = {"smtp_host": "smtp.gmail.com",
        "smtp_port": 587,
        "imap_host": "imap.gmail.com",
        "imap_port": 993,
        "username": "rapidsms.org@gmail.com",
        "password": "rapidsms123",
        "use_tls": True,
        "poll_interval": 3
        }
CONF2 = {
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 587,
        "imap_host": "imap.gmail.com",
        "imap_port": 993,
        "username": "rapidsms.org2@gmail.com",
        "password": "rapidsms123",
        "use_tls": True,
        "poll_interval": 3
        }

    
class TestBackendEmail(unittest.TestCase):
    
    
    def setUp(self):
        # setup a router with the email backend and echo app enabled.
        # also mark the inboxes of both accounts read
        self._read_all(CONF)
        self._read_all(CONF2)
        self.assertEqual(0, len(self._get_mail(CONF)))
        self.assertEqual(0, len(self._get_mail(CONF2)))
        
        router = MockRouter()
        backend = Backend(router)
        backend.configure(**CONF)
        router.add_backend(backend)
        router.add_app(EchoApp(router))
        self.backend = backend
        self.router = router
        
    def tearDown(self):
        if self.router.running:
            self.router.stop()
        
    def test_backend_configuration(self):
        self.assertEquals(type(self.backend), Backend, "Email backend loads")
        for conf_key, value in CONF.items():
            self.assertEqual(value, getattr(self.backend, conf_key), "Email backend set %s" % conf_key)
            
    
    def test_basic(self):
        self.router.start()
        to_send = "hello world!"
        msg_to = CONF["username"]
        subject = "hello"
        self._send_mail(text=to_send, to_addr=msg_to, conf=CONF2,
                        subject=subject)
        # on each iteration, sleep for a while to let the email 
        # traverse the internets
        time.sleep(15)
        self._check_response(msg_to, CONF2["username"], subject, to_send)
        self._read_all(CONF2)
        
        to_send = "empty subject!"
        subject = ""
        self._send_mail(text=to_send, to_addr=msg_to, conf=CONF2,
                        subject=subject)
        time.sleep(15)
        self._check_response(msg_to, CONF2["username"], subject, to_send)
        self._read_all(CONF2)
        
        to_send = ""
        subject = "empty body!"
        self._send_mail(text=to_send, to_addr=msg_to, conf=CONF2, subject=subject)
        time.sleep(15)
        self._check_response(msg_to, CONF2["username"], subject, to_send)
            
        
    
    def _read_all(self, conf):
        imap_connection = self._imap_connection(conf)
        typ, data = imap_connection.search(None, 'UNSEEN')
        for num in data[0].split():
            typ, data = imap_connection.fetch(num, '(RFC822)')
            imap_connection.store(num, "+FLAGS", "\\Seen")
        
    def _send_mail(self, subject="hello", to_addr="rapidsms.org@gmail.com", 
                   text="hello world!", conf=CONF2):
        
        msg = MIMEText(text)
        msg['Subject'] = subject
        msg['From'] = conf["username"]
        msg['To'] = to_addr
        
        s = smtplib.SMTP(host=conf["smtp_host"], port=conf["smtp_port"])
        s.ehlo()
        if conf["use_tls"]:
            s.starttls()
        s.login(conf["username"], conf["password"])
        s.sendmail(conf["username"], [to_addr], msg.as_string())
        s.quit()

    def _get_mail(self, conf=CONF2):
        all_msgs = []
        imap_connection = self._imap_connection(conf)
        # this assumes any unread message is a new message
        typ, data = imap_connection.search(None, 'UNSEEN')
        for num in data[0].split():
            typ, data = imap_connection.fetch(num, '(RFC822)')
            # get a rapidsms message from the data
            email_message = parsed = message_from_string(data[0][1])
            all_msgs.append(email_message)
        imap_connection.close()
        imap_connection.logout()
        return all_msgs
    
    def _imap_connection(self, conf):
        """Gets a new connection ready to search"""
        imap_connection = imaplib.IMAP4_SSL(conf["imap_host"], conf["imap_port"])
        imap_connection.login(conf["username"], conf["password"])
        imap_connection.select()
        return imap_connection
    
    def _check_echo(self, person, message_in, message_back):
         expected = "%s: %s" % (person, message_in)
         self.assertEqual(expected.lower().strip(), 
                          message_back.lower().strip())
         
    def _check_response(self, msg_to, msg_from, subject, msg_body):
        msgs = self._get_mail()
        self.assertEqual(1, len(msgs), "Expected exactly 1 response but got %s." % len(msgs))
        msg = msgs[0]
        self.assertEqual(msg_to, msg["From"], "From address matched")
        self._check_echo(msg_from, msg_body, msg.get_payload())
        expected_subject = "re: %s" % subject
        self.assertEqual(expected_subject.strip(), msg["Subject"].strip())
        

if __name__ == "__main__":
    unittest.main()
