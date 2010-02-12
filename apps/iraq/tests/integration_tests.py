#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from rapidsms.tests.scripted import TestScript
from tree.app import App
from reporters.app import App as reporter_app
from default.app import App as default_app
from register.app import App as register_app
from internationalization.app import App as i18n_app

class TestIntegration(TestScript):
    """ Test our various SMS apps all together now """
    fixtures = ['poll_interactive.json']
    apps = (App, reporter_app, register_app, default_app, i18n_app)

    testTreeApp = """
        00919980131127 > register poll 100 1001
        00919980131127 < Thanks for registering for the survey.
        00919980131127 > poll
        00919980131127 < What do you feel happy?
        00919980131127 > a
        00919980131127 < What are the three things do you need the most?
        00919980131127 > c,d,x
        00919980131127 < Compare to my parents?
        00919980131127 > e
        00919980131127 < Thank you for participating in the poll.
    """