#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from rapidsms.tests.scripted import TestScript
from poll.app import App
from reporters.app import App as reporter_app
from default.app import App as default_app
from register.app import App as register_app
from internationalization.app import App as i18n_app

class TestIntegration(TestScript):
    """ Test our various SMS apps all together now """
    fixtures = ['poll_responses.json']
    apps = (App, reporter_app, register_app, default_app, i18n_app)

    testCorrectResponse = """
      00919980131127 > poll
      00919980131127 < What is your favourite fruit?
      00919980131127 > register poll 10 8
      00919980131127 < Thanks for registering for the survey.
      00919980131127 > M 10 J
      00919980131127 < Thank you for voting. You selected Mango.
      00919980131127 > A 10 M
      00919980131127 < Thank you for voting. You selected Apple.
      00919980131127 > poll
      00919980131127 < What is your favourite fruit?
      00919980131127 > register asdfas
      00919980131127 < We could not understand the register message. Please send as - register survey governorate district
      00919980131127 > M
      00919980131127 < Sorry, we did not understand your response. Please re-send as - answer age gender
    """
