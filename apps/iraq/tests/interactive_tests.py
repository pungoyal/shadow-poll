#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from rapidsms.tests.scripted import TestScript
from tree.app import App as tree_app
from reporters.app import App as reporter_app
from default.app import App as default_app

class TestApp(TestScript):
    fixtures = ['poll_interactive.json']
    apps = (reporter_app, tree_app, default_app)

    testBasicPoll = """
        00919980131127 > poll
        00919980131127 < What do you feel happy?
        00919980131127 > a
        00919980131127 < What are the three things do you need the most?
        00919980131127 > c
        00919980131127 < Compare to my parents?
        00919980131127 > e
        00919980131127 < Thank you for participating in the poll.
    """

    fails_testBasicPollArabic = """
      10000 > arabicfood
      10000 < arabicWhat is your favourite fruit?
      10000 > arabicapple
      10000 < arabicOf these vegetables, which is your favourite? Carrot, Tomato, Lettuce, Spinach
      10000 > arabictomato
      10000 < arabicWhat is your favourite drink? Please specify one of: lime, kiwi, ginger.
      10000 > arabickiwi
      10000 < arabicThank you for sharing your dietary preferences.
    """

