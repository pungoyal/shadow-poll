#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from rapidsms.tests.scripted import TestScript
from internationalization.app import App as i18n_app
from reporters.app import App as reporter_app
from poll.app import App as poll_app

class TestApp(TestScript):
    fixtures = ['dietary_preferences.json']
    apps = (reporter_app, poll_app, i18n_app)

    # testBasicPoll = u"""
    #   10000 > food
    #   10000 < What is your favourite fruit?
    #   10000 > apple
    #   10000 < Of these vegetables, which is your favourite? Carrot, Tomato, Lettuce, Spinach
    #   10000 > tomato
    #   10000 < What is your favourite drink? Please specify one of: lime, kiwi, ginger.
    #   10000 > kiwi
    #   10000 < Thank you for sharing your dietary preferences.
    # """

    # testBasicError = u"""
    #   10000 > food
    #   10000 < What is your favourite fruit?
    #   10000 > apple
    #   10000 < Of these vegetables, which is your favourite? Carrot, Tomato, Lettuce, Spinach
    #   10000 > tree
    #   10000 < You have selected an invalid choice, please choose one among the above listed choice
    # """

    # testBasicPollArabic = u"""
    #   10000 > طعام
    #   10000 < ما هي الفاكهة المفضلة لديك؟
    #   10000 > تفاح
    #   10000 < ما هي الخضراوات المفضلة اليك ؟ جزر, طماطم, خس, سبانخ
    #   10000 > طماطم
    #   10000 < ما هو عصيرك المفضل؟ الرجاء إختيار : ليمون, كيوي, زنجبيل
    #   10000 > كيوي
    #   10000 < شكراً لك لمشاركتك معنا بالأغذية المفضلة لديك.
    # """

    # testBasicErrorArabic = u"""
    #   10000 > طعام
    #   10000 < ما هي الفاكهة المفضلة لديك؟
    #   10000 > تفاح
    #   10000 < ما هي الخضراوات المفضلة اليك ؟ جزر, طماطم, خس, سبانخ
    #   10000 > فtreeطماطم
    #   10000 < كنت قد اخترت خيار غير المشروعة ، يرجى اختيار واحد من بين الخيارات المذكورة أعلاه
    # """

