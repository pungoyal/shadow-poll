# -*- coding: utf-8 -*-
from rapidsms.tests.scripted import TestScript
from utils import is_english
from i18n.app import App

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
