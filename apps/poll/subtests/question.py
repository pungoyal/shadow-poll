from apps.poll.models import *
from apps.reporters.models import Reporter, PersistantConnection, PersistantBackend

from django.test import TestCase

from poll.app import App as poll_App

class QuestionTest(TestCase):

    apps = (poll_App)

    def setUp(self):
        Question.objects.all().delete()
        self.backend = PersistantBackend(slug="MockBackend1")
        self.backend.save()
        self.reporter = Reporter(alias="ReporterName1")
        self.reporter.save()
        self.pconnection = PersistantConnection(backend=self.backend, 
                                                reporter=self.reporter, 
                                                identity="1000")
        self.pconnection.save()

        self.reporter.connections.add(self.pconnection)
        
        self.user = User(connection=self.pconnection, age=12, gender='m', governorate=1, district=1)
        self.user.save()

    def test_save(self):
        initial_no_of_questions = len(Question.objects.all())
        question1 = Question(text = 'question 1', max_choices = 3)
        question2 = Question(text = 'question 2', max_choices = 3)

        question1.next_question = question2
        question1.save()
        question2.save()

    def test_last_question(self):
        question1 = Question(text = 'question 1')
        question1.save()
        next_question = question1.next_question
        self.assertEquals(next_question, None)

    def test_first(self):
        question1 = Question(text = 'question 1')
        question2 = Question(text = 'question 2')
        question3 = Question(text = 'question 3')

        question2.is_first = True

        question1.save()
        question2.save()
        question3.save()

        first_question = Question.first()

        self.assertEquals(first_question, question2)

    def setup_choices(self,question):
        choice1 = Choice(code= 'a',question=question)
        choice2 = Choice(code= 'b',question=question)
        choice3 = Choice(code= 'c',question=question)
        choice1.save()
        choice2.save()
        choice3.save()

    def test_matching_choices(self):
        question1 = Question(text = 'question 1',max_choices = 1)
        question1.save()
        self.setup_choices(question1)
        self.assertEquals(len(question1.matching_choices('jdenjn')), 0)
        self.assertEquals(len(question1.matching_choices('a')), 1)
        self.assertEquals(len(question1.matching_choices(None)), 0)

    def test_humanize_options(self):
        question = Question(text = 'question 1',max_choices = 1)
        question.save()
        choice1 = Choice(code= 'a',question=question, text="apple")
        choice2 = Choice(code= 'b',question=question, text="bannana")
        choice3 = Choice(code= 'c',question=question, text="carrot")
        choice1.save()
        choice2.save()
        choice3.save()
        self.assertEquals(question.humanize_options(), "a. apple b. bannana c. carrot")

    def test_humanize_questions(self):
        question = Question(text = 'question 1',max_choices = 1)
        question.save()
        choice1 = Choice(code= 'a',question=question, text="apple")
        choice2 = Choice(code= 'b',question=question, text="bannana")
        choice3 = Choice(code= 'c',question=question, text="carrot")
        choice1.save()
        choice2.save()
        choice3.save()
        self.assertEquals(str(question), "question 1:  a. apple b. bannana c. carrot")

    def test_questions_with_helper_text(self):
        question = Question(text = 'question 1',max_choices = 1, helper_text="(Prioritize)")
        question.save()
        choice1 = Choice(code= 'a',question=question, text="apple")
        choice2 = Choice(code= 'b',question=question, text="bannana")
        choice3 = Choice(code= 'c',question=question, text="carrot")
        choice1.save()
        choice2.save()
        choice3.save()
        self.assertEquals(str(question), "question 1: (Prioritize) a. apple b. bannana c. carrot")

    def test_get_max_num_of_response_from_location(self):
        question = Question(text = 'question 1',max_choices = 1, helper_text="(Prioritize)")
        question.save()
        choice1 = Choice(code= 'a',question=question, text="apple")
        choice2 = Choice(code= 'b',question=question, text="bannana")
        choice3 = Choice(code= 'c',question=question, text="carrot")
        choice1.save()
        choice2.save()
        choice3.save()
        UserResponse(user = self.user, question = question, choice = choice1).save()
        UserResponse(user = self.user, question = question, choice = choice2).save()
        UserResponse(user = self.user, question = question, choice = choice2).save()
        num_responses_for_governorate = UserResponse.objects.filter(question = question, 
                                                                    user__governorate = 1).count()
        self.assertEquals(num_responses_for_governorate, 3)

