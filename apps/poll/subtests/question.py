from apps.poll.models import *
from apps.reporters.models import Reporter, PersistantConnection, PersistantBackend

from unittest import TestCase
from math import fsum

class QuestionTest(TestCase):
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
        self.assertEquals(str(question), "question 1 a. apple b. bannana c. carrot")

    def test_questions_with_helper_text(self):
        question = Question(text = 'question 1',max_choices = 1, helper_text="(Prioritize)")
        question.save()
        choice1 = Choice(code= 'a',question=question, text="apple")
        choice2 = Choice(code= 'b',question=question, text="bannana")
        choice3 = Choice(code= 'c',question=question, text="carrot")
        choice1.save()
        choice2.save()
        choice3.save()
        self.assertEquals(str(question), "question 1(Prioritize) a. apple b. bannana c. carrot")

    # def test_matching_choices_matches_number_of_allowed_choices(self):
    #     question2 = Question(text = "question 2", max_choices = 3)
    #     self.assertEquals(len(question1.matching_choices('a b')), 0)

    def test_response_break_up(self):
        question = Question(id=1)
        break_up = question.response_break_up()

        self.assertEquals(break_up[0], 22.6)
        self.assertEquals(break_up[1], 18.8)
        self.assertEquals(break_up[2], 52.2)
        self.assertEquals(break_up[3], 6.4)

    def test_sum_of_break_up_values_should_be_100(self):
        question = Question(id=1)
        break_up = question.response_break_up()

        self.assertEquals(fsum(break_up), 100)