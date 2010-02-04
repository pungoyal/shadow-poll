from django.db import models
from utils import *

class DictionaryEntry(models.Model):
    text = models.CharField(null=False, max_length=100)
    meaning = models.CharField(null=False,max_length=100)
        
    class Meta:
        db_table = 'Dictionary'
    
    def __unicode__(self):
        return "%s -> %s" % (self.text, self.meaning)
    
    @staticmethod
    def load_dictionary():
        dictionary_entries = DictionaryEntry.objects.all()
        dictionary = {}
        
        for entry in dictionary_entries:
            dictionary[entry.text] = entry.meaning
        return dictionary
        
class Translator(models.Model):
    def __init__(self):
        self.dictionary = DictionaryEntry.load_dictionary()

    def understand_and_translate_if_required(self, text):
        self.arabic = False
        parts = text.split(" ")
        for part in parts:
            if not is_english(part):
                t = Translator()
                translated = t.translate(text)
                return translated
        
        return False
    
    def translate(self, text):
        parts = text.split(' ')
        result = ""
        for part in parts:
            if part.isdigit():
                translated = self.translate_number(part)
            else:
                translated = self.translate_word(part)
            result += translated + " "
        return result.strip()

    def translate_number(self, number):
        result = ""
        for c in number:
            result += self.translate_word(c)
        return result

    def translate_word(self, text):
        """ encapsulate all dictionary accesses here,
        in case we decide to change lookup table later
        """
        try:
            return self.dictionary[text]
        except KeyError:
            # fall back to English -s TODO: fix unit tests and remove 'return False' above
            return text
