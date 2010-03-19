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
        question1 = Question(text = 'question 1', num_answers_expected = 3)
        question2 = Question(text = 'question 2', num_answers_expected = 3)

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
        question = Question(text = 'question 1',num_answers_expected = 1)
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
        question = Question(text = 'question 1',num_answers_expected = 1, helper_text="(Prioritize)")
        question.save()
        choice1 = Choice(code= 'a',question=question, text="apple")
        choice2 = Choice(code= 'b',question=question, text="bannana")
        choice3 = Choice(code= 'c',question=question, text="carrot")
        choice1.save()
        choice2.save()
        choice3.save()
        self.assertEquals(str(question), "question 1: (Prioritize) a. apple b. bannana c. carrot")

    def test_get_categories(self):
        self.setup_question_choices_and_categories()

        categories = self.question.get_categories()
        self.assertEquals(len(categories), 2)
        self.assertEquals(categories[0].name, self.fruits.name)
        self.assertEquals(categories[1].name, self.vegetables.name)


    def setup_question_choices_and_categories(self):
        self.question = Question(text = 'question 1',num_answers_expected = 1, helper_text="(Prioritize)")
        self.question.save()

        self.blue = Color(file_name="blue.png", code="#blue")
        self.red = Color(file_name="red.png", code="#red")
        self.blue.save()
        self.red.save()

        self.fruits = Category(name="fruits", color=self.red)
        self.fruits.save()
        self.vegetables = Category(name="vegetables",color=self.blue)
        self.vegetables.save()

        self.carrot = Choice(code= 'b',question=self.question, text="carrot", category=self.vegetables)
        self.apple = Choice(code= 'a',question=self.question, text="apple", category=self.fruits)
        self.banana = Choice(code= 'c',question=self.question, text="banana", category=self.fruits)
        self.ginger = Choice(code= 'd',question=self.question, text="ginger", category=self.vegetables)
        self.apple.save()
        self.carrot.save()
        self.banana.save()
        self.ginger.save()

    def test_get_response_break_up(self):
        self.setup_question_choices_and_categories()

        UserResponse(user = self.user, question = self.question, choice = self.apple).save()
        UserResponse(user = self.user, question = self.question, choice = self.apple).save()
        UserResponse(user = self.user, question = self.question, choice = self.apple).save()
        UserResponse(user = self.user, question = self.question, choice = self.carrot).save()
        UserResponse(user = self.user, question = self.question, choice = self.carrot).save()
        UserResponse(user = self.user, question = self.question, choice = self.carrot).save()
        UserResponse(user = self.user, question = self.question, choice = self.carrot).save()
        UserResponse(user = self.user, question = self.question, choice = self.banana).save()
        UserResponse(user = self.user, question = self.question, choice = self.banana).save()
        UserResponse(user = self.user, question = self.question, choice = self.ginger).save()

        response_break_up = self.question.response_break_up()
        
        self.assertEquals(response_break_up["by_choice"].count(), 4)
        
        #apple
        apple = filter( lambda r : r["choice"] == self.apple.id,  response_break_up["by_choice"])[0]
        self.assertEquals(apple["votes"], 3)
