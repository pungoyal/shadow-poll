from rapidsms.tests.scripted import TestScript
from app import App
import reporters.app as reporters_app
import internationalization.app as i18n_app

from models import *
from reporters.models import Reporter, PersistantConnection, PersistantBackend
    
class TestApp (TestScript):
    apps = (App, reporters_app.App)
    # the test_backend script does the loading of the dummy backend that allows reporters
    # to work properly in tests
    fixtures = ['test_backend', 'test_tree']
    
    testTrigger = """
           8005551212 > test
           8005551212 < hello
         """        
    
    testPin = """
           8005551211 > pin
           8005551211 < Please enter your 4-digit PIN
           8005551211 > 1234
           8005551211 < Thanks for entering.
         """
         
    testPinFailure = """
           8005551213 > pin
           8005551213 < Please enter your 4-digit PIN
           8005551213 > abcd
           8005551213 < "abcd" is not a valid answer. You must enter a 4-digit decimal number
           8005551213 > 123
           8005551213 < "123" is not a valid answer. You must enter a 4-digit decimal number
           8005551213 > 123d
           8005551213 < "123d" is not a valid answer. You must enter a 4-digit decimal number
           8005551213 > 12345
           8005551213 < "12345" is not a valid answer. You must enter a 4-digit decimal number
           8005551213 > 
           8005551213 < "" is not a valid answer. You must enter a 4-digit decimal number
           8005551213 > 0000
           8005551213 < Thanks for entering.
         """
         
    def testLocalization(self):
        '''Tests very basic localization of trees'''
        reporter = self._register('0004', 'en', "loc_en")
        script = """
              loc_en > test
              loc_en < hello
            """        
        self.runScript(script)
        reporter = self._register('0005', 'sp', "loc_sp")
        script = """
              loc_sp > test
              loc_sp < ola
            """        
        self.runScript(script)
        reporter = self._register('0006', 'fr', "loc_mult")
        script = """
              loc_mult > test
              loc_mult < bon jour
              loc_mult > blah
              loc_mult < You are done with this survey.  Thanks for participating!
              
            """        
        self.runScript(script)
        reporter.language = 'en'
        reporter.save()
        script = """
              loc_mult > test
              loc_mult < hello
            """        
        self.runScript(script)
        
         
    def _register(self, alias, language, phone):
        """Register a user"""
        # create the reporter object for this person 
        reporter =  Reporter.objects.create(alias=alias, language=language)
        
        # running this script ensures the connection gets created by the reporters app
        self.runScript("%s > hello world" % phone)
        connection = PersistantConnection.objects.get(identity=phone)
        connection.reporter = reporter
        connection.save()
        return reporter
    
        
         
