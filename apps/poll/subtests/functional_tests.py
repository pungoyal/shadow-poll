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
      00919880438062 > A 10 M
      00919880438062 < Thank you for voting. You selected Apple.
      00919980131127 > M 10 J
      00919980131127 < Thank you for voting. You selected Mango.
    """

    testIncorrectResponse = """
      00919980131127 > B 10
      00919980131127 < Sorry, we did not understand your response. Please re-send as - answer age gender
    """

    testSendOutPollQuestion = """
      00919880438062 > poll
      00919880438062 < What is your favourite fruit?
    """
