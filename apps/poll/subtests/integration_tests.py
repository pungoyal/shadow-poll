#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from rapidsms.tests.scripted import TestScript
from poll.app import App
from reporters.app import App as reporter_app
from default.app import App as default_app
from register.app import App as register_app

class TestIntegration(TestScript):
    """ Test our various SMS apps all together now """
    fixtures = ['poll_responses.json']
    apps = (App, reporter_app, register_app, default_app)

    testCorrectResponse = """
      100 > poll
      100 < What is your favourite fruit?
      100 > register poll 100 1001
      100 < Thanks for registering for the survey.
      100 > M 10 J 110010
      100 < Thank you for voting. You selected Mango.
      100 > A 10 M 110010
      100 < Thank you for voting. You selected Apple.
      100 > poll
      100 < What is your favourite fruit?
      100 > register asdfas
      100 < We could not understand the register message. Please send as - register survey governorate district
      100 > Mango
      100 < Sorry, we didn't understand your response. Please re-send as - issue age gender area
    """
