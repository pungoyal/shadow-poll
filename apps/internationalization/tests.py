# -*- coding: utf-8 -*-
from django.test import TestCase 
from rapidsms.tests.scripted import TestScript

from app import App
from models import *


class TestTranslator(TestCase):
    fixtures = ['dictionary']
    def test_translate_from_english_to_english(self):
        t = Translator()
        self.assertEquals(t.translate("poll"), "poll")

    def test_english_text_is_left_untouched(self):
        t = Translator()
        translated_text = t.understand_and_translate_if_required("register poll")
        self.assertEquals(translated_text, False)


    def test_understand_and_translate(self):
        t = Translator()
        translated_text = t.understand_and_translate_if_required(u"التصويت تسجيل")
        self.assertEquals(translated_text, "poll register")
        translated_text = t.understand_and_translate_if_required(u"٥ ١٠ التصويت تسجيل")
        self.assertEquals(translated_text, "5 10 poll register")

    def test_translate_from_arabic_to_english(self):
        t = Translator()
        self.assertEquals(t.translate(u"تسجيل"), u"register")
        self.assertEquals(t.translate(u"poll تسجيل"), u"poll register")
        self.assertEquals(t.translate(u"التصويت تسجيل"), u"poll register")

    def test_translate_numbers(self):
        t = Translator()
        self.assertEquals(t.translate_number(u"٠١٢٣٤٥٦٧٨٩"), u"0123456789")
        self.assertEquals(t.translate_number(u"0123456789"), u"0123456789")
        self.assertEquals(t.translate_number(u"0١2٣4٥6٧8٩"), u"0123456789")
        
    def test_reverse_input_string_on_translation(self):
        t = Translator()
        self.assertEquals(t.translate(u"register poll"), "register poll")

    def test_if_a_string_is_numbers(self):
        t = Translator()
        self.assertFalse(u"a".isdigit())
        self.assertFalse(u"a12".isdigit())
        self.assertFalse(u"12a".isdigit())
        self.assertFalse(u"0a".isdigit())
        self.assertFalse(u"a0".isdigit())
        self.assertFalse(u"001a010".isdigit())

        self.assertTrue(u"1".isdigit())
        self.assertTrue(u"100".isdigit())
        self.assertTrue(u"0011".isdigit())
        self.assertTrue(u"1234567890".isdigit())

        self.assertTrue(u"٠١٢٣٤٥٦٧٨٩".isdigit())
        self.assertTrue(u"٩٠٠".isdigit())
        self.assertTrue(u"1".isdigit())

        self.assertTrue(u"١1٩".isdigit())
        self.assertFalse(u"١a٩".isdigit())
        
        
class TestDictionaryEntry(TestCase):
    fixtures = ['dictionary']
    def test_get_meaning(self):
        dictionary = Translation.load_dictionary()
        self.assertEquals(dictionary["register"], "register")
        
    def test_to_string(self):
        c = Language()
        c.code = 'en'
        d = Translation()
        d.code = "text"
        d.translation = "meaning"
        d.language = c
        self.assertEquals(str(d), "text -> meaning (en)")
        
    def test_load_dictionary(self):
        d = Translation.load_dictionary()
        self.assertEquals(d["register"], "register")

class TestInferArabic(TestScript):
    apps = (App,)
    
    def setUp(self):
        self.translator = Translator()

    def test_arabic_is_not_english(self):
        arabic_string = u"""تسجيل التصويت 100 1001"""
        self.assertFalse(self.translator.is_english(arabic_string))
        
    def test_english_is_english(self):
        english_string = u"""sfdsadfsafan3242498277asdkjfndsaf"""
        self.assertTrue(self.translator.is_english(english_string))
        
    def test_mixed_is_not_english(self):
        mixed_string = u"""sfdsadfsafالتصويتan3242498277asdkjfndsaf"""
        self.assertFalse(self.translator.is_english(mixed_string))
    
#    TODO - put arabic numbers here
#    def test_arabic_numbers_is_not_english(self):
#        numbers_string = u"3242498277"
#        self.assertFalse(is_english(numbers_string))
        
    def test_empty_string_should_raise_exception(self):
        empty_string = u""
        self.assertRaises(ValueError, self.translator.is_english, empty_string)
        
    def tearDown(self):
        pass
