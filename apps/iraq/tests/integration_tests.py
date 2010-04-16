#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from apps.reporters.app import App as reporter_app
from apps.default.app import App as default_app
from apps.register.app import App as register_app
from apps.internationalization.app import App as i18n_app
from rapidsms.tests.scripted import TestScript
from apps.poll.app import App as poll_app
from apps.bulkpoll.app import App as bulk_app

class TestIntegration(TestScript):
    """ Test our various SMS apps all together now """
    apps = (reporter_app, register_app, default_app, i18n_app, bulk_app, poll_app)

    testHappyPathScenarios = """
        00919980131127 > register poll 2 1
        00919980131127 < Thank you, to initiate the poll sms the keyword Poll with your age and gender
        00919980131127 > poll 12 f
        00919980131127 < I feel happy: (Choose a,b,c or d.) a. Always b. Most of the time c. Rarely d. Never
        00919980131127 > b
        00919980131127 < The three things I need most are: (Prioritize your first, second, and third.) a. Peace and Security b. Go to school regularly c. Health care when sick d. Clean neighbourhood e. Clean drinking water f. Enough food g. Be loved h. Not have to work i. Be listened to j. A place to play k. Family and friends to be safe l. Others
        00919980131127 > l d a
        00919980131127 < Compared to my parents, my life in the future will be: (Choose a,b,c or d.) a. Better b. About the same c. Worse d. I don't know
        00919980131127 > c
        00919980131127 < Your responses have been recorded. Thank you for participating in the poll.
    """

    testBulkPoll = """
        00919980131127 > register poll 2 1
        00919980131127 < Thank you, to initiate the poll sms the keyword Poll with your age and gender
        00919980131127 > bulk 12 f a a b c d
        00919980131127 < Your responses have been recorded. Thank you for participating in the poll.
    """

    testHappyPathScenarios_Arabic = u"""
        00919980131127 > تسجيل التصويت ٤ ٢
        00919980131127 <  شكراً لكم, للشروع في التصويت عن طريق الرسائل القصيرة الرجاء إرسال  التصويت   العمر   الجنس
        00919980131127 > التصويت ١١ انثى
        00919980131127 < انا أشعر بالسعادة : (الرجاء إختيار أ,ب,ج  أو د)   أ.دائماً    ب.معظم الوقت    ج. نادراً    د.لا أشعر بالسعادة أبداً
        00919980131127 > أ
        00919980131127 < أكثر ثلاثة أمور أحتاج إليها هي (الرجاء ترتيبها حسب الأولوية): أ) السلام و الأمان ب) الذهاب إلى المدرسة بانتظام ج) الحصول على العلاج عندما امرض د) العيش في حي نظيف هـ) وجود مياه شرب نظيفة و) وجود طعام كافي ز) الشعور بمحبة الآخرين لي ح) عدم اضطراري للعمل ط) الإصغاء إلى آرائي ي)وجود مكان للعب ك)شعور أسرتي وأصدقائي بالأمان ل) أخرى
        00919980131127 > ح د أ
        00919980131127 < بالمقارنة مع وضع أبي و أمي, أتوقع أن تكون حياتي في المستقبل : (الرجاء إختيار أ,ب,ج  أو د)  أ.أحسن  ب.متشابهة لحياتهما  ج.أسوأ  د.لا أعرف
        00919980131127 > د
        00919980131127 < ردودكم قد سجلت. أشكركم على المشاركة في التصويت
    """
    
    testRegistrationFail = """
        00919980131127 > register 3 2
        00919980131127 < We don't understand. Correct format is register poll governorate-code district-code
        00919980131127 > register poll
        00919980131127 < We don't understand. Correct format is register poll governorate-code district-code
        00919980131127 > register poll 100 
        00919980131127 < We don't understand. Correct format is register poll governorate-code district-code
        00919980131127 > register poll govt 1001
        00919980131127 < Sorry, the geo location entered is incorrect. Please try again.
        00919980131127 > register 
        00919980131127 < We don't understand. Correct format is register poll governorate-code district-code
    """
    testRegistrationFail_Arabic = u"""
        00919980131127 > تسجيل ١٠٠ 
        00919980131127 < عذراً, رسالتك غير مفهومة. الصيغة الصحيحة هي    تسجيل   التصويت    رمز المحافظة    رمز القضاء
        00919980131127 > تسجيل التصويت
        00919980131127 < عذراً, رسالتك غير مفهومة. الصيغة الصحيحة هي    تسجيل   التصويت    رمز المحافظة    رمز القضاء
        00919980131127 > تسجيل التصويت ١٠٠ 
        00919980131127 < عذراً, رسالتك غير مفهومة. الصيغة الصحيحة هي    تسجيل   التصويت    رمز المحافظة    رمز القضاء
        00919980131127 > تسجيل التصويت بغداد ١٠٠١
        00919980131127 < عذراً, رسالتك غير مفهومة. الصيغة الصحيحة هي    تسجيل   التصويت    رمز المحافظة    رمز القضاء
        00919980131127 > تسجيل
        00919980131127 < عذراً, رسالتك غير مفهومة. الصيغة الصحيحة هي    تسجيل   التصويت    رمز المحافظة    رمز القضاء
    """

    testPollCommandWithoutRegister = """
        00919980131127 > poll 14 f
        00919980131127 < I feel happy: (Choose a,b,c or d.) a. Always b. Most of the time c. Rarely d. Never
        """

    testPollCommandWithoutRegister_Arabic = u"""
        00919980131127 > التصويت ١١ انثى
        00919980131127 < انا أشعر بالسعادة : (الرجاء إختيار أ,ب,ج  أو د)   أ.دائماً    ب.معظم الوقت    ج. نادراً    د.لا أشعر بالسعادة أبداً
        """
        
    testPollCommandHappyPath_1 = """
        00919980131127 > poll 6 male
        00919980131127 < I feel happy: (Choose a,b,c or d.) a. Always b. Most of the time c. Rarely d. Never
        """
        
    testPollCommandHappyPath_1_Arabic = u"""
        00919980131127 > التصويت 6 ذكر
        00919980131127 < انا أشعر بالسعادة : (الرجاء إختيار أ,ب,ج  أو د)   أ.دائماً    ب.معظم الوقت    ج. نادراً    د.لا أشعر بالسعادة أبداً
        """
        
    testPollCommandHappyPath_2 = """
        00919980131127 > poll 9 female
        00919980131127 < I feel happy: (Choose a,b,c or d.) a. Always b. Most of the time c. Rarely d. Never
        """
        
    testPollCommandHappyPath_2_Arabic = u"""
        00919980131127 > التصويت 9 أنثى
        00919980131127 < انا أشعر بالسعادة : (الرجاء إختيار أ,ب,ج  أو د)   أ.دائماً    ب.معظم الوقت    ج. نادراً    د.لا أشعر بالسعادة أبداً
        """
        
    testPollCommandHappyPath_3 = """
        00919980131127 > poll 9 m
        00919980131127 < I feel happy: (Choose a,b,c or d.) a. Always b. Most of the time c. Rarely d. Never
        """
    #No need for Arabic test scenario for the above scenario
    
    testPollCommandFailing = """
        00919980131127 > poll 
        00919980131127 < Sorry we did not understand your response. Please may you enter Age as a number and Gender as either M or F
        00919980131127 > pull 
        00919980131127 < Sorry we did not understand your response. Please may you enter Age as a number and Gender as either M or F
        00919980131127 > poll 17
        00919980131127 < Sorry we did not understand your response. Please may you enter Age as a number and Gender as either M or F
        00919980131127 > poll M
        00919980131127 < Sorry we did not understand your response. Please may you enter Age as a number and Gender as either M or F
        00919980131127 > poll 13 14
        00919980131127 < Sorry we did not understand your response. Please may you enter Age as a number and Gender as either M or F
    """
    testPollCommandFailing_Arabic = u"""
        00919980131127 > التصويت 
        00919980131127 < ناسف لاننا لم نفهم ردكم, الرجاء ادخال العمر بالارقام ونوع الجنس إما ذكر او انثى
        00919980131127 > التصوي 
        00919980131127 < ناسف لاننا لم نفهم ردكم, الرجاء ادخال العمر بالارقام ونوع الجنس إما ذكر او انثى
        00919980131127 > التصويت 17 
        00919980131127 < ناسف لاننا لم نفهم ردكم, الرجاء ادخال العمر بالارقام ونوع الجنس إما ذكر او انثى
        00919980131127 > التصويت ذكر 
        00919980131127 < ناسف لاننا لم نفهم ردكم, الرجاء ادخال العمر بالارقام ونوع الجنس إما ذكر او انثى
        00919980131127 > التصويت 17 17 
        00919980131127 < ناسف لاننا لم نفهم ردكم, الرجاء ادخال العمر بالارقام ونوع الجنس إما ذكر او انثى
        """

    testPollQuestion_1_UnhappyPath = """
        00919980131127 > poll 12 f
        00919980131127 < I feel happy: (Choose a,b,c or d.) a. Always b. Most of the time c. Rarely d. Never
        00919980131127 > f
        00919980131127 < You have selected an invalid choice, please choose one among the above listed choice
        00919980131127 > 4
        00919980131127 < You have selected an invalid choice, please choose one among the above listed choice
        00919980131127 > abc
        00919980131127 < Due to errors the poll has been stopped. To restart, type the keyword Poll with your age and gender
        """
        
    testPollQuestion_1_UnhappyPath_Arabic = u"""
        00919980131127 > التصويت ١١ انثى
        00919980131127 < انا أشعر بالسعادة : (الرجاء إختيار أ,ب,ج  أو د)   أ.دائماً    ب.معظم الوقت    ج. نادراً    د.لا أشعر بالسعادة أبداً
        00919980131127 > س
        00919980131127 < لقد اخترت خيارا غير موجودة ، يرجى اختيار واحد من بين الخيارات المذكورة سابقاً
        00919980131127 > ٤
        00919980131127 < لقد اخترت خيارا غير موجودة ، يرجى اختيار واحد من بين الخيارات المذكورة سابقاً
        00919980131127 > أبج
        00919980131127 < نظرا للأخطاء تم إيقاف التصويت. الرجاء إعادة الإرسال كما يلي  التصويت   العمر   الجنس
        """
    
    testPollQuestion_2_UnhappyPath = """
        00919980131127 > poll 12 M
        00919980131127 < I feel happy: (Choose a,b,c or d.) a. Always b. Most of the time c. Rarely d. Never
        00919980131127 > a
        00919980131127 < The three things I need most are: (Prioritize your first, second, and third.) a. Peace and Security b. Go to school regularly c. Health care when sick d. Clean neighbourhood e. Clean drinking water f. Enough food g. Be loved h. Not have to work i. Be listened to j. A place to play k. Family and friends to be safe l. Others
        00919980131127 > c d y
        00919980131127 < You have selected an invalid choice, please choose one among the above listed choice
        00919980131127 > z d a
        00919980131127 < You have selected an invalid choice, please choose one among the above listed choice
        00919980131127 > a b 4
        00919980131127 < Due to errors the poll has been stopped. To restart, type the keyword Poll with your age and gender  
        """
        #Once a decision is made for erroring when entering less than three choices for question # 2, ensure to include the relative test scenarios in the above test
        
    testPollQuestion_2_UnhappyPath_Arabic = u"""
        00919980131127 > التصويت ١١ انثى
        00919980131127 < انا أشعر بالسعادة : (الرجاء إختيار أ,ب,ج  أو د)   أ.دائماً    ب.معظم الوقت    ج. نادراً    د.لا أشعر بالسعادة أبداً
        00919980131127 > أ
        00919980131127 < أكثر ثلاثة أمور أحتاج إليها هي (الرجاء ترتيبها حسب الأولوية): أ) السلام و الأمان ب) الذهاب إلى المدرسة بانتظام ج) الحصول على العلاج عندما امرض د) العيش في حي نظيف هـ) وجود مياه شرب نظيفة و) وجود طعام كافي ز) الشعور بمحبة الآخرين لي ح) عدم اضطراري للعمل ط) الإصغاء إلى آرائي ي)وجود مكان للعب ك)شعور أسرتي وأصدقائي بالأمان ل) أخرى
        00919980131127 > أ و ع
        00919980131127 < لقد اخترت خيارا غير موجودة ، يرجى اختيار واحد من بين الخيارات المذكورة سابقاً
        00919980131127 > أ ب 4
        00919980131127 < لقد اخترت خيارا غير موجودة ، يرجى اختيار واحد من بين الخيارات المذكورة سابقاً
        """

    testPollQuestion_3_UnhappyPath = """
        00919980131127 > poll 12 M
        00919980131127 < I feel happy: (Choose a,b,c or d.) a. Always b. Most of the time c. Rarely d. Never
        00919980131127 > a
        00919980131127 < The three things I need most are: (Prioritize your first, second, and third.) a. Peace and Security b. Go to school regularly c. Health care when sick d. Clean neighbourhood e. Clean drinking water f. Enough food g. Be loved h. Not have to work i. Be listened to j. A place to play k. Family and friends to be safe l. Others
        00919980131127 > A B C
        00919980131127 < Compared to my parents, my life in the future will be: (Choose a,b,c or d.) a. Better b. About the same c. Worse d. I don't know
        00919980131127 > p
        00919980131127 < You have selected an invalid choice, please choose one among the above listed choice
        00919980131127 > 5
        00919980131127 < You have selected an invalid choice, please choose one among the above listed choice
        """
        
    testPollQuestion_3_UnhappyPath_Arabic = u"""
        00919980131127 > التصويت ١١ انثى
        00919980131127 < انا أشعر بالسعادة : (الرجاء إختيار أ,ب,ج  أو د)   أ.دائماً    ب.معظم الوقت    ج. نادراً    د.لا أشعر بالسعادة أبداً
        00919980131127 > أ
        00919980131127 < أكثر ثلاثة أمور أحتاج إليها هي (الرجاء ترتيبها حسب الأولوية): أ) السلام و الأمان ب) الذهاب إلى المدرسة بانتظام ج) الحصول على العلاج عندما امرض د) العيش في حي نظيف هـ) وجود مياه شرب نظيفة و) وجود طعام كافي ز) الشعور بمحبة الآخرين لي ح) عدم اضطراري للعمل ط) الإصغاء إلى آرائي ي)وجود مكان للعب ك)شعور أسرتي وأصدقائي بالأمان ل) أخرى
        00919980131127 > أ ب ج
        00919980131127 < بالمقارنة مع وضع أبي و أمي, أتوقع أن تكون حياتي في المستقبل : (الرجاء إختيار أ,ب,ج  أو د)  أ.أحسن  ب.متشابهة لحياتهما  ج.أسوأ  د.لا أعرف
        00919980131127 > ٤
        00919980131127 < لقد اخترت خيارا غير موجودة ، يرجى اختيار واحد من بين الخيارات المذكورة سابقاً
        00919980131127 > ن
        00919980131127 < لقد اخترت خيارا غير موجودة ، يرجى اختيار واحد من بين الخيارات المذكورة سابقاً
        """
    
    test_registration_message_in_arabic_options_jumbled = u"""
    00919980131127 > التصويت ١١ انثى
    00919980131127 < انا أشعر بالسعادة : (الرجاء إختيار أ,ب,ج  أو د)   أ.دائماً    ب.معظم الوقت    ج. نادراً    د.لا أشعر بالسعادة أبداً
    00919980131127 > أ
    00919980131127 < أكثر ثلاثة أمور أحتاج إليها هي (الرجاء ترتيبها حسب الأولوية): أ) السلام و الأمان ب) الذهاب إلى المدرسة بانتظام ج) الحصول على العلاج عندما امرض د) العيش في حي نظيف هـ) وجود مياه شرب نظيفة و) وجود طعام كافي ز) الشعور بمحبة الآخرين لي ح) عدم اضطراري للعمل ط) الإصغاء إلى آرائي ي)وجود مكان للعب ك)شعور أسرتي وأصدقائي بالأمان ل) أخرى
    00919980131127 >  ل د أ
    00919980131127 < بالمقارنة مع وضع أبي و أمي, أتوقع أن تكون حياتي في المستقبل : (الرجاء إختيار أ,ب,ج  أو د)  أ.أحسن  ب.متشابهة لحياتهما  ج.أسوأ  د.لا أعرف
    00919980131127 > أ
    00919980131127 < ردودكم قد سجلت. أشكركم على المشاركة في التصويت
    """
    testTreeAppWithoutRegister = """
        00919980131127 > poll 14 m
        00919980131127 < I feel happy: (Choose a,b,c or d.) a. Always b. Most of the time c. Rarely d. Never
        00919980131127 > a
        00919980131127 < The three things I need most are: (Prioritize your first, second, and third.) a. Peace and Security b. Go to school regularly c. Health care when sick d. Clean neighbourhood e. Clean drinking water f. Enough food g. Be loved h. Not have to work i. Be listened to j. A place to play k. Family and friends to be safe l. Others
        00919980131127 > c d e
        00919980131127 < Compared to my parents, my life in the future will be: (Choose a,b,c or d.) a. Better b. About the same c. Worse d. I don't know
        00919980131127 > c
        00919980131127 < Your responses have been recorded. Thank you for participating in the poll.
    """
    
    testTreeAppFailSessionEnd_2 = """
        00919980131127 > register poll 5 1
        00919980131127 < Thank you, to initiate the poll sms the keyword Poll with your age and gender
        00919980131127 > poll 16 m
        00919980131127 <  I feel happy: (Choose a,b,c or d.) a. Always b. Most of the time c. Rarely d. Never
        00919980131127 > Always Nevr
        00919980131127 <  You have selected an invalid choice, please choose one among the above listed choice
        00919980131127 > Al Neb
        00919980131127 <  You have selected an invalid choice, please choose one among the above listed choice
        00919980131127 > Alllllll
        00919980131127 < Due to errors the poll has been stopped. To restart, type the keyword Poll with your age and gender
        00919980131127 > a
        00919980131127 < Sorry we did not understand your response. Please may you enter Age as a number and Gender as either M or F
        00919980131127 > poll 10 f
        00919980131127 <  I feel happy: (Choose a,b,c or d.) a. Always b. Most of the time c. Rarely d. Never
    """
    
