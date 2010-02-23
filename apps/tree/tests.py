from rapidsms.tests.scripted import TestScript
from app import App
import reporters.app as reporters_app
import internationalization.app as i18n_app

from models import *
from reporters.models import Reporter, PersistantConnection, PersistantBackend
import unittest

class TestApp (TestScript):
    apps = (App, reporters_app.App)
    # the test_backend script does the loading of the dummy backend that allows reporters
    # to work properly in tests
    fixtures = ['test_backend', 'test_tree','test_charts']
    
    testTrigger = """
           8005551212 > test
           8005551212 < hello
         """
    
    testPin = """
           8005551211 > pin
           8005551211 < Please enter your 4-digit PIN
           8005551211 > a
           8005551211 < Thanks for entering.
         """
    
    def testGetTrigger(self):
        self.msg_txt = "test m 12"
        self.tree_model = Tree()
        self.tree = self.tree_model.parse_information_and_get_tree(self.msg_txt," ")
        self.assertEquals(self.tree['tree'].id , 1)
        
        self.msg_txt = "junk m 12"
        self.tree = self.tree_model.parse_information_and_get_tree(self.msg_txt," ")
        self.assertEquals(self.tree['tree'] , None)
        
        self.msg_txt = "test"
        self.tree = self.tree_model.parse_information_and_get_tree(self.msg_txt," ")
        self.assertEquals(self.tree['tree'].id , 1)
        
        self.msg_txt = "test m"
        self.tree = self.tree_model.parse_information_and_get_tree(self.msg_txt," ")
        self.assertEquals(self.tree['tree'].id , 1)
        
    def testTriggerWithDemoGraphicInformatin(self):
        self.msg_txt = "test m 12"
        self.tree = Tree.objects.get(id=1)
        self.tree_model = Tree()
        self.tree_and_demographics = self.tree_model.parse_information_and_get_tree(self.msg_txt," ")
        self.assertEquals(self.tree_and_demographics , {'tree': self.tree, 'sex': 'm', 'age': '12'})
        
        self.msg_txt = "test f 12"
        self.tree_and_demographics = self.tree_model.parse_information_and_get_tree(self.msg_txt," ")
        self.assertEquals(self.tree_and_demographics , {'tree': self.tree, 'sex': 'f', 'age': '12'})
        
    def testTriggerWithOnlySexInfo(self):
        self.msg_txt = "test m"
        self.tree_model = Tree()
        self.tree_and_demographics = self.tree_model.parse_information_and_get_tree(self.msg_txt," ")
        self.assertEquals(self.tree_and_demographics['tree'].id , 1)
        self.assertEquals(self.tree_and_demographics['sex'] , 'm')
        
    def testGetChoicesForSingleOption(self):
        self.msg_txt = "a"
        self.delim = ";"
        self.ques = Question(id=1, text="What?", max_choices=1)
        self.choices = self.ques.get_choices(self.msg_txt, self.delim)
        self.assertEquals(len(self.choices), 1)
    
    def testGetChoicesForSingleOptionWithDelim(self):
        self.msg_txt = "a;"
        self.delim = ";"
        self.ques = Question(id=1, text="What?", max_choices=1)
        self.choices = self.ques.get_choices(self.msg_txt, self.delim)
        self.assertEquals(len(self.choices), 1)
        self.assertEquals(['a'], self.choices)
    
    def testGetChoicesForSingleOptionWithTwoLetters(self):
        self.delim = ";"
        self.ques = Question(id=1, text="What?", max_choices=1)

        self.msg_txt = "a;b"
        self.choices = self.ques.get_choices(self.msg_txt, self.delim)
        self.assertEquals(self.choices, None)
        
    def test_get_num_entry_for_question(self):
        self.n_question = "1"
        self.e = Entry()
        self.num_entries = self.e.get_num_entries_for_question(self.n_question)
        self.assertEquals(self.num_entries, 5)
        
        # this case should be handled by translator app
#        self.msg_txt = "a b"
#        self.choices = self.ques.get_choices(self.msg_txt, self.delim)
#        self.assertEquals('a', self.choices[0])
        
    def testGetChoicesForMultipleOptions(self):
        self.msg_txt = "a b"
        self.delim = " "
        self.ques = Question(id=1, text="What?", max_choices=2)
        self.choices = self.ques.get_choices(self.msg_txt, self.delim)
        self.assertEquals(len(self.choices), 2)
        
    def testGetChoicesForMultipleOptions(self):
        self.msg_txt = "a b c d"
        self.delim = " "
        self.ques = Question(id=1, text="What?", max_choices=3)
        self.choices = self.ques.get_choices(self.msg_txt, self.delim)
        self.assertEquals(self.choices, None)
        
        self.msg_txt = "a"
        self.delim = " "
        self.choices = self.ques.get_choices(self.msg_txt, self.delim)
        self.assertEquals(len(self.choices), 1)
        self.assertEquals(['a'], self.choices)
        
    def testCheckTransitionsForSingleOption(self):
        self.choices = ['a']
        self.current_state = TreeState.objects.get(id=2)
        self.found_transition = self.current_state.has_transition(self.choices)
        self.assertTrue(self.found_transition)
        
        self.choices = ['b']
        self.found_transition = self.current_state.has_transition(self.choices)
        self.assertEqual(self.found_transition, False)
    
    def testGetTransitionsForSingleOption(self):
        self.choices = ['a']
        self.current_state = TreeState.objects.get(id=2)
        self.transition = self.current_state.get_transition(self.choices)
        self.assertEqual(self.transition.id, 1)
        
        self.choices = ['b']
        self.transition = self.current_state.get_transition(self.choices)
        self.assertEqual(self.transition, None)    
  
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
