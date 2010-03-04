from apps.poll.models import *
from apps.reporters.models import Reporter, PersistantConnection, PersistantBackend

from django.test import TestCase

class QuestionTest(TestCase):

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

    def setup_question_and_choices(self):
        question = Question(text = 'question 1',max_choices = 1)
        question.save()
        choice1 = Choice(code= 'a',question=question, text="apple")
        choice2 = Choice(code= 'b',question=question, text="bannana")
        choice3 = Choice(code= 'c',question=question, text="carrot")
        choice1.save()
        choice2.save()
        choice3.save()
        return question

    def test_matching_choices(self):
        question = self.setup_question_and_choices()
        self.assertEquals(len(question.matching_choices('jdenjn')), 0)
        self.assertEquals(len(question.matching_choices('a')), 1)
        self.assertEquals(len(question.matching_choices(None)), 0)

    def test_humanize_options(self):
        question = self.setup_question_and_choices()
        self.assertEquals(question.humanize_options(), "a. apple b. bannana c. carrot")

    def test_humanize_questions(self):
        question = self.setup_question_and_choices()
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
        UserResponse(user = self.user, question = question, choice = choice2).save()
        UserResponse(user = self.user, question = question, choice = choice1).save()
        UserResponse(user = self.user, question = question, choice = choice1).save()

        response_break_up = question.response_break_up()

        self.assertEquals(len(response_break_up), 2)
        self.assertEquals(response_break_up[choice2.text], 33.3)
        self.assertEquals(response_break_up[choice1.text], 66.7)
