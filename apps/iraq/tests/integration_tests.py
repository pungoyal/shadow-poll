#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from apps.reporters.app import App as reporter_app
from apps.default.app import App as default_app
from apps.register.app import App as register_app
from apps.internationalization.app import App as i18n_app
from rapidsms.tests.scripted import TestScript
from apps.poll.app import App as poll_app

class TestIntegration(TestScript):
    """ Test our various SMS apps all together now """
    fixtures = ['poll_interactive.json']
    apps = (reporter_app, register_app, default_app, i18n_app, poll_app)

    testTreeApp = """
        00919980131127 > register poll 100 1001
        00919980131127 < Thank you, to initiate the poll sms the keyword Poll with your age and gender
        00919980131127 > poll
        00919980131127 < I feel happy Choose a,b,c or d. a. Always b. Most of the time c. Rarely d. Never
        00919980131127 > most of the time
        00919980131127 < The three things I need most are (Prioritize your first, second, and third.) a. Peace and Security b. Go to school regularly c. Health care when sick d. Clean neighbourhood e. Clean drinking water f. Enough food g. be loved h. Not have to work i. Be listened to j. A place to place k. Family and friends to be safe
        00919980131127 > c d e
        00919980131127 < Compared to my parents, my life in the future will be Choose a,b,c or d. a. Better b. About the same c. Worse d. I don't know
        00919980131127 > worse
        00919980131127 < Your responses have been recorded. Thank you for participating in the poll.
    """
    # test_registration_message_in_arabic = u"""
    # 00919980131127 > التصويت
    # 00919980131127 <  أنا أشعر بالسعادة:
    # 00919980131127 > أ
    # 00919980131127 < أكثر ثلاثة أمور لا تجعلني أشعر بالسعادة هي (الرجاء ترتيبها حسب الأولوية): أ) السلام و الأمان ب) الذهاب إلى المدرسة بانتظام ج) الحصول على العلاج عندما امرض د) العيش في حي نظيف هـ) وجود مياه شرب نظيفة و) وجود طعام كافي ز) الشعور بمحبة الآخرين لي ح) عدم اضطراري للعمل ط) الإصغاء إلى آرائي ي)وجود مكان للعب ك)شعور أسرتي وأصدقائي بالأمان ل) أخرى (إجابة مفتوحة). ستستخدم الردود على هذه النقطة خلال المرحلة التجريبية للحصول على المعلومات اللازمة لإجراء التعديلات المحتملة للخيارات.
    # 00919980131127 > ب ج أ
    # 00919980131127 < بالمقارنة مع وضع أبي وأمي، أتوقع أن تكون حياتي في المستقبل: (اختر إجابة واحدة)
    # 00919980131127 > أ
    # 00919980131127 < ردودكم قد سجلت. أشكركم على المشاركة في الانتخابات.
    # """
    
    # test_registration_message_with_words_in_arabic = u"""
    # 00919980131127 > التصويت
    # 00919980131127 <  أنا أشعر بالسعادة:
    # 00919980131127 > على الدوام      
    # 00919980131127 < أكثر ثلاثة أمور لا تجعلني أشعر بالسعادة هي (الرجاء ترتيبها حسب الأولوية): أ) السلام و الأمان ب) الذهاب إلى المدرسة بانتظام ج) الحصول على العلاج عندما امرض د) العيش في حي نظيف هـ) وجود مياه شرب نظيفة و) وجود طعام كافي ز) الشعور بمحبة الآخرين لي ح) عدم اضطراري للعمل ط) الإصغاء إلى آرائي ي)وجود مكان للعب ك)شعور أسرتي وأصدقائي بالأمان ل) أخرى (إجابة مفتوحة). ستستخدم الردود على هذه النقطة خلال المرحلة التجريبية للحصول على المعلومات اللازمة لإجراء التعديلات المحتملة للخيارات.
    # 00919980131127 > ب ج أ
    # 00919980131127 < بالمقارنة مع وضع أبي وأمي، أتوقع أن تكون حياتي في المستقبل: (اختر إجابة واحدة)
    # 00919980131127 > أ
    # 00919980131127 < ردودكم قد سجلت. أشكركم على المشاركة في الانتخابات.
    # """
    
    testTreeAppWithoutRegister = """
        00919980131127 > poll
        00919980131127 < I feel happy Choose a,b,c or d. a. Always b. Most of the time c. Rarely d. Never
        00919980131127 > a
        00919980131127 < The three things I need most are (Prioritize your first, second, and third.) a. Peace and Security b. Go to school regularly c. Health care when sick d. Clean neighbourhood e. Clean drinking water f. Enough food g. be loved h. Not have to work i. Be listened to j. A place to place k. Family and friends to be safe
        00919980131127 > c d e
        00919980131127 < Compared to my parents, my life in the future will be Choose a,b,c or d. a. Better b. About the same c. Worse d. I don't know
        00919980131127 > c
        00919980131127 < Your responses have been recorded. Thank you for participating in the poll.
    """
    
    testTreeAppFail = """
        00919980131127 > register poll 100 1001
        00919980131127 < Thank you, to initiate the poll sms the keyword Poll with your age and gender
        00919980131127 > poll
        00919980131127 <  I feel happy Choose a,b,c or d. a. Always b. Most of the time c. Rarely d. Never
        00919980131127 > a
        00919980131127 < The three things I need most are (Prioritize your first, second, and third.) a. Peace and Security b. Go to school regularly c. Health care when sick d. Clean neighbourhood e. Clean drinking water f. Enough food g. be loved h. Not have to work i. Be listened to j. A place to place k. Family and friends to be safe
        00919980131127 > c d y
        00919980131127 < You have selected an invalid choice, please choose one among the above listed choice
        00919980131127 > z d a
        00919980131127 < You have selected an invalid choice, please choose one among the above listed choice
        00919980131127 > c d a
        00919980131127 < Compared to my parents, my life in the future will be Choose a,b,c or d. a. Better b. About the same c. Worse d. I don't know
        00919980131127 > p
        00919980131127 < You have selected an invalid choice, please choose one among the above listed choice
        00919980131127 > a
        00919980131127 < Your responses have been recorded. Thank you for participating in the poll.
    """
    
    # testTreeAppFailSessionEnd = """
    #     00919980131127 > register poll 100 1001
    #     00919980131127 < Thank you, to initiate the poll sms the keyword Poll with your age and gender
    #     00919980131127 > poll
    #     00919980131127 <  I feel happy Choose a,b,c or d. a. Always b. Most of the time c. Rarely d. Never
    #     00919980131127 > x
    #     00919980131127 < You have selected an invalid choice, please choose one among the above listed choice
    #     00919980131127 > x
    #     00919980131127 < You have selected an invalid choice, please choose one among the above listed choice
    #     00919980131127 > x
    #     00919980131127 < You have selected an invalid choice, please choose one among the above listed choice
    #     00919980131127 < Due to errors the poll has been stopped. To restart, type the keyword Poll with your age and gender
    #     00919980131127 > a
    #     00919980131127 < We didn't understand your response.
    #     00919980131127 > poll
    #     00919980131127 < I feel happy: a) Always; b) Most of the time; c) Rarely; d) Never. Choose a,b,c or d.
    # """
    
    # testTreeAppFailSessionEnd_2 = """
    #     00919980131127 > register poll 100 1001
    #     00919980131127 < Thank you, to initiate the poll sms the keyword Poll with your age and gender
    #     00919980131127 > poll
    #     00919980131127 < I feel happy: a) Always; b) Most of the time; c) Rarely; d) Never. Choose a,b,c or d.
    #     00919980131127 > Always Nevr
    #     00919980131127 < Please choose one option
    #     00919980131127 > Al Neb
    #     00919980131127 < Please choose one option
    #     00919980131127 > Alllllll
    #     00919980131127 < You have selected an invalid choice, please choose one among the above listed choice
    #     00919980131127 < Due to errors the poll has been stopped. To restart, type the keyword Poll with your age and gender
    #     00919980131127 > a
    #     00919980131127 < We didn't understand your response.
    #     00919980131127 > poll
    #     00919980131127 < I feel happy: a) Always; b) Most of the time; c) Rarely; d) Never. Choose a,b,c or d.
    # """
    
    # testTreeAppFailMultipleResponse = """
    #     00919980131127 > register poll 100 1001
    #     00919980131127 < Thank you, to initiate the poll sms the keyword Poll with your age and gender
    #     00919980131127 > poll
    #     00919980131127 < I feel happy: a) Always; b) Most of the time; c) Rarely; d) Never. Choose a,b,c or d.
    #     00919980131127 > always never
    #     00919980131127 < Please choose one option
    #     00919980131127 > a b
    #     00919980131127 < Please choose one option
    #     00919980131127 > always
    #     00919980131127 < The three things I need most are: (Prioritize your first, second, and third.) a. Peace and Security b. Go to school regularly c. Health care when sick d. Clean neighborhood e. Clean drinking water f. Enough food g. Be loved h. Not have to work i. Be listened to j. A place to play k. Family and friends to be safe
    # """
    
    # testTreeAppJunkMessage = """
    #     00919980131127 > dfsdsdsdsd
    #     00919980131127 < We didn't understand your response.
    # """
