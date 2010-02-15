#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from apps.tree.app import App
from apps.reporters.app import App as reporter_app
from apps.default.app import App as default_app
from apps.register.app import App as register_app
from apps.internationalization.app import App as i18n_app
from rapidsms.tests.scripted import TestScript

class TestIntegration(TestScript):
    """ Test our various SMS apps all together now """
    fixtures = ['poll_interactive.json']
    apps = (App, reporter_app, register_app, default_app, i18n_app)

    testTreeApp = """
        00919980131127 > register poll 100 1001
        00919980131127 < Thanks for registering for the survey.
        00919980131127 > poll
        00919980131127 < I feel happy: a) Always; b) Most of the time; c) Rarely; d) Never. Choose a,b,c or d.
        00919980131127 > a
        00919980131127 < The three things I need most are: (Prioritize your first, second, and third.) a. Peace and Security b. Go to school regularly c. Health care when sick d. Clean neighborhood e. Clean drinking water f. Enough food g. Be loved h. Not have to work i. Be listened to j. A place to play k. Family and friends to be safe
        00919980131127 > c d e
        00919980131127 < Compared to my parents, my life in the future will be: a) Better; b) About the same; c) Worse; d) I don't know. Choose a,b,c or d.
        00919980131127 > c
        00919980131127 < Your responses have been recorded. Thank you for participating in the poll.
    """
    test_registration_message_in_arabic = u"""
    00919980131127 > التصويت
    00919980131127 <  أنا أشعر بالسعادة:
    00919980131127 > أ
    00919980131127 < أكثر ثلاثة أمور لا تجعلني أشعر بالسعادة هي (الرجاء ترتيبها حسب الأولوية):
    00919980131127 > ب ج أ
    00919980131127 < بالمقارنة مع وضع أبي وأمي، أتوقع أن تكون حياتي في المستقبل: (اختر إجابة واحدة)
    00919980131127 > أ
    00919980131127 < ردودكم قد سجلت. أشكركم على المشاركة في الانتخابات.
    """
    testTreeAppWithoutRegister = """
        00919980131127 > poll
        00919980131127 < I feel happy: a) Always; b) Most of the time; c) Rarely; d) Never. Choose a,b,c or d.
        00919980131127 > a
        00919980131127 < The three things I need most are: (Prioritize your first, second, and third.) a. Peace and Security b. Go to school regularly c. Health care when sick d. Clean neighborhood e. Clean drinking water f. Enough food g. Be loved h. Not have to work i. Be listened to j. A place to play k. Family and friends to be safe
        00919980131127 > c d e
        00919980131127 < Compared to my parents, my life in the future will be: a) Better; b) About the same; c) Worse; d) I don't know. Choose a,b,c or d.
        00919980131127 > c
        00919980131127 < Your responses have been recorded. Thank you for participating in the poll.
    """
    
    testTreeAppFail = """
        00919980131127 > register poll 100 1001
        00919980131127 < Thanks for registering for the survey.
        00919980131127 > poll
        00919980131127 < I feel happy: a) Always; b) Most of the time; c) Rarely; d) Never. Choose a,b,c or d.
        00919980131127 > a
        00919980131127 < The three things I need most are: (Prioritize your first, second, and third.) a. Peace and Security b. Go to school regularly c. Health care when sick d. Clean neighborhood e. Clean drinking water f. Enough food g. Be loved h. Not have to work i. Be listened to j. A place to play k. Family and friends to be safe
        00919980131127 > c d y
        00919980131127 < Placeholder error for question number 2. Please re-send.
        00919980131127 > z d a
        00919980131127 < Placeholder error for question number 2. Please re-send.
        00919980131127 > c d a
        00919980131127 < Compared to my parents, my life in the future will be: a) Better; b) About the same; c) Worse; d) I don't know. Choose a,b,c or d.
        00919980131127 > p
        00919980131127 < Placeholder error for question number 3. Please re-send.
        00919980131127 > a
        00919980131127 < Your responses have been recorded. Thank you for participating in the poll.
    """
    
    testTreeAppFailSessionEnd = """
        00919980131127 > register poll 100 1001
        00919980131127 < Thanks for registering for the survey.
        00919980131127 > poll
        00919980131127 < I feel happy: a) Always; b) Most of the time; c) Rarely; d) Never. Choose a,b,c or d.
        00919980131127 > x
        00919980131127 < Placeholder error for question number 1. Please re-send.
        00919980131127 > x
        00919980131127 < Placeholder error for question number 1. Please re-send.
        00919980131127 > x
        00919980131127 < Placeholder error for question number 1. Please re-send.
        00919980131127 < Sorry, invalid answer 3 times. Your session will now end. Please try again later.
        00919980131127 > a
        00919980131127 < We didn't understand your response.
        00919980131127 > poll
        00919980131127 < I feel happy: a) Always; b) Most of the time; c) Rarely; d) Never. Choose a,b,c or d.
    """
    
    testTreeAppJunkMessage = """
        00919980131127 > dfsdsdsdsd
        00919980131127 < We didn't understand your response.
    """
