from apps.poll.models import DemographicParser, User, Questionnaire, UserSession, Question
from unittest import TestCase
from apps.poll.trigger_responder import TriggerResponder
from apps.poll.messages import TRIGGER_INCORRECT_MESSAGE

class TriggerResponderTest(TestCase):

    def setUp(self):
        self.q = Questionnaire(trigger = "poll")
        ageParser = DemographicParser(questionnaire=self.q, name='age', regex='[0-9]+', 
                        order=1, type='i')
        genderParser = DemographicParser(questionnaire=self.q, name='gender', 
                        regex='m|f|male|female', order=2, type='c')

        self.parsers = [ageParser, genderParser]
        self.user = User()
        self.session = UserSession()
        self.question =Question(text="what")
        self.kwargs =   {"parsers": self.parsers, 
                         "user": self.user,
                         "trigger" : self.q.trigger,
                         "next_question" : self.question ,
                         "session" : self.session
                         }
        self.trigger_responder  = TriggerResponder(self.kwargs)


    def test_criteria_for_trigger(self):
        self.assertEquals(self.trigger_responder.criteria("poll"), True)
        

    def test_action_for_trigger(self):
        response = self.trigger_responder.action("poll 12 f")
        self.assertNotEquals(response, TRIGGER_INCORRECT_MESSAGE)
        self.assertEquals(self.user.age, 12)
        self.assertEquals(self.user.gender, "f")
        self.assertEquals(response, str(self.question))

        
