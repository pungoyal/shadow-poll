from django.db import models

# some really bare bones models for localization
class Language(models.Model):
    code = models.CharField(max_length = 16) # e.g. "en" or "en-us" or "eng"
    name = models.CharField(max_length = 64) # e.g. "English"

    def __unicode__(self):
        return "%s (%s)" % (self.code, self.name)

class Translation(models.Model):
    # not all translations are associated with a language. for example, numbers...
    language = models.ForeignKey(Language, null=True, blank=True)
    # The actual original (probably english) string will be 
    # used as the key into the other languages.  This is 
    # similar to the python/django _() i18n support.  
    translation = models.CharField(max_length=700)
    code = models.CharField(max_length=700)
        
    class Meta:
        db_table = 'Dictionary'
    
    def __unicode__(self):
        return "%s -> %s (%s)" % (self.translation, self.code, self.language.code)
    
    @staticmethod
    def load_dictionary():
        dictionary_entries = Translation.objects.all()
        dictionary = {}
        
        for entry in dictionary_entries:
            dictionary[entry.translation] = entry.code
        return dictionary
        
class Translator(models.Model):
    def __init__(self):
        self.dictionary = Translation.load_dictionary()

    def understand_and_translate_if_required(self, text):
        self.arabic = False
        parts = text.split(" ")
        for part in parts:
            if not self.is_english(part):
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

    def is_english(self, string):
        string = string.strip()
        if not string:
            raise ValueError("Cannot infer language from empty string")
        try:
            string.encode('ascii')
            return True
        except Exception, e:
            return False
    
