from rapidsms.tests.scripted import TestScript
from app import App

from message_parser import MessageParser

class TestApp (TestScript):
    apps = (App,)

    def test_message_parser_age_sex(self):
        msgParser = MessageParser("bulk m 7 a a b c d")
        parsed_msg = msgParser.parse()
        self.assertEquals(parsed_msg[1], 'm')
        self.assertEquals(parsed_msg[2], '7')
