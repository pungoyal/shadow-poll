# -*- coding: utf-8 -*-
from rapidsms.tests.scripted import TestScript
from utils import is_english
from app import App
from django.test import TestCase 
from models import *

class TestTranslator(TestCase):
    fixtures = ['dictionary']
    def test_translate_from_english_to_english(self):
        t = Translator()
        translated_text = t.translate("poll تسجيل")
        self.assertEquals(translated_text, "register poll")

    def test_translate_from_arabic_to_english(self):
        t = Translator()
        translated_text = t.translate("تسجيل")
        self.assertEquals(translated_text, "register")
        
    def test_reverse_input_string_on_translation(self):
        t= Translator()
        translated_text = t.translate("register poll")
        self.assertEquals(translated_text, "poll register")

class TestDictionaryEntry(TestCase):
    fixtures = ['dictionary']
    def test_get_meaning(self):
        dictionary = DictionaryEntry.load_dictionary()
        self.assertEquals(dictionary["register"], "register")
        
    def test_to_string(self):
        d = DictionaryEntry()
        d.text = "text"
        d.meaning = "meaning"
        self.assertEquals(str(d), "text -> meaning")
        
    def test_load_dictionary(self):
        d = DictionaryEntry.load_dictionary()
        self.assertEquals(d["register"], "register")

class TestInferArabic(TestScript):
    apps = (App,)

    def test_arabic_is_not_english(self):
        arabic_string = u"""تسجيل التصويت 100 1001"""
        self.assertFalse(is_english(arabic_string))
        
    def test_english_is_english(self):
        english_string = u"""sfdsadfsafan3242498277asdkjfndsaf"""
        self.assertTrue(is_english(english_string))
        
    def test_mixed_is_not_english(self):
        mixed_string = u"""sfdsadfsafالتصويتan3242498277asdkjfndsaf"""
        self.assertFalse(is_english(mixed_string))
    
    def test_only_numbers_should_raise_exception(self):
        numbers_string = u"3242498277"
        self.assertRaises(ValueError, is_english, numbers_string)
        
#    TODO - put arabic numbers here
#    def test_arabic_numbers_is_not_english(self):
#        numbers_string = u"3242498277"
#        self.assertFalse(is_english(numbers_string))
        
    def test_empty_string_should_raise_exception(self):
        empty_string = u""
        self.assertRaises(ValueError, is_english, empty_string)
