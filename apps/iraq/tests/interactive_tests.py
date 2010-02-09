#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from rapidsms.tests.scripted import TestScript
from poll.app import App
from poll.models import *
from reporters.app import App as reporter_app
from tree.app import App as tree_app

class TestApp(TestScript):
    fixtures = ['poll_responses.json']
    apps = (App, reporter_app, tree_app)

    testBasicPoll = """
      10000 > food
      10000 < What is your favourite fruit?
      10000 > apple
      10000 < Of these vegetables, which is your favourite? Carrot, Tomato, Lettuce, Spinach
      10000 > tomato
      10000 < What is your favourite drink? Please specify one of: lime, kiwi, ginger.
      10000 > kiwi
      10000 < Thank you for sharing your dietary preferences.
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

