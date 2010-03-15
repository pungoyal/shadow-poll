from apps.poll.models import DemographicParser, User, Questionnaire, UserSession, Question, Choice
from unittest import TestCase
from apps.poll.valid_answer_responder import ValidAnswerResponder
from apps.poll.messages import TRIGGER_INCORRECT_MESSAGE

class ValidAnswerResponderTest(TestCase):

    def setUp(self):
        self.user = User()
        self.q = Questionnaire(trigger = "trigger", max_retries=3)
        self.q.save()
        self.session = UserSession()
        self.question =Question(text="what")
        self.question.save()
        self.choice1 = Choice(code= 'a',question=self.question, text="a")
        self.choice2 = Choice(code= 'b',question=self.question, text="a")
        self.choice3 = Choice(code= 'c',question=self.question, text="a")
        self.choice1.save()
        self.choice2.save()
        self.choice3.save()
        
        self.next_question  = Question(text="next")

        self.session.question = self.question
        self.kwargs =  {"user": self.user,
                    "next_question" :self.next_question ,
                    "session" : self.session
                        
                    }
        self.trigger_responder  = ValidAnswerResponder(self.kwargs)


    def test_criteria_for_trigger(self):
        self.assertEquals(self.trigger_responder.criteria("c"), True)
        self.assertEquals(self.trigger_responder.criteria("w"), False)
        
    def test_valid_answer_response(self):
        self.assertEquals(self.trigger_responder.action("c"), str(self.next_question))
        

        
