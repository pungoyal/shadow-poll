#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from rapidsms.tests.scripted import TestScript
from poll.app import App
from poll.models import *
from reporters.app import App as reporter_app

class TestApp(TestScript):
    fixtures = ['poll_responses.json']
    apps = (App, reporter_app)

    testCorrectResponse = """
      98804 > A 10 M
      98804 < Thank you for voting. You selected Apple.
      10000 > M 10 J
      10000 < Thank you for voting. You selected Mango.
    """

    testIncorrectResponse = """
      1234 > B 10
      1234 < Sorry, we did not understand your response. Please re-send as - answer age gender
    """

    testSendOutPollQuestion = """
      98804 > poll
      98804 < What is your favourite fruit?
    """
