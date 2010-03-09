""" 
This would be in governorates_tests, except that we're also testing
districts, and we want to load a different fixture
"""

from django.test import TestCase

from apps.reporters.models import PersistantBackend, PersistantConnection
from apps.charts.models import Governorate, District
from apps.poll.models import User, UserResponse, Category, Choice, Color, Question

class StyleTest(TestCase):
    def setUp(self):
        # clean up
        Question.objects.all().delete()
        UserResponse.objects.all().delete()
        
        # user
        self.backend = PersistantBackend(slug="MockBackend1")
        self.backend.save()
        self.pconnection = PersistantConnection(backend=self.backend, 
                                                reporter=None, 
                                                identity="user_1_identity")
        self.pconnection.save()
        self.governorate1 = Governorate.objects.get(pk=1)
        self.district1 = District.objects.get(pk=29)
        
        self.user = User(connection=self.pconnection, age=12, gender='m', 
                         governorate=self.governorate1.code, district=self.district1.code)
        self.user.save()
        
        # create categorical poll
        self.question1 = Question(text = 'question1', max_choices = 1)
        self.question1.save()
        yellow = Color(file_name="yellow.png", code="#yellow")
        yellow.save()
        fruits = Category(name="fruits", color=yellow)
        fruits.save()
        red = Color(file_name="red.png", code="#red")
        red.save()
        meat = Category(name="meat", color=red)
        meat.save()
        self.green = Color(file_name="green.png", code="#green")
        self.green.save()
        vegetables = Category(name="vegetables", color=self.green)
        vegetables.save()
        self.apple =Choice(code= 'a',question = self.question1, 
                           text="apple", category=fruits)
        self.apple.save()
        self.bear = Choice(code= 'b',question = self.question1, 
                           text="bear", category=meat)
        self.bear.save()
        self.cabbage = Choice(code= 'c',question = self.question1, 
                              text="cabbage", category=vegetables)
        self.cabbage.save()
        self.dillpickle = Choice(code= 'd',question = self.question1, 
                                 text="dillpickle", category=vegetables)
        self.dillpickle.save()
        
    def test_styles_for_basic_poll(self):
        # populate it with responses
        UserResponse(user = self.user, question = self.question1, 
                     choice = self.apple).save()
        UserResponse(user = self.user, question = self.question1, 
                     choice = self.bear).save()
        UserResponse(user = self.user, question = self.question1, 
                     choice = self.bear).save()
        UserResponse(user = self.user, question = self.question1, 
                     choice = self.cabbage).save()
        UserResponse(user = self.user, question = self.question1, 
                     choice = self.cabbage).save()
        UserResponse(user = self.user, question = self.question1, 
                     choice = self.cabbage).save()
        
        self.assertEquals(self.governorate1.style(self.question1), 
                          {'color': self.green, 'percentage': 0.5})
        self.assertEquals(self.district1.style(self.question1), 
                          {'color': self.green, 'percentage': 0.5} )

    def test_styles_for_categorical_poll(self):        
        # populate it with responses
        UserResponse(user = self.user, question = self.question1, 
                     choice = self.apple).save()
        UserResponse(user = self.user, question = self.question1, 
                     choice = self.bear).save()
        UserResponse(user = self.user, question = self.question1, 
                     choice = self.cabbage).save()
        UserResponse(user = self.user, question = self.question1, 
                     choice = self.dillpickle).save()
        
        self.assertEquals(self.governorate1.style(self.question1), 
                          {'color': self.green, 'percentage': 0.5})
        self.assertEquals(self.district1.style(self.question1), 
                          {'color': self.green, 'percentage': 0.5} )
        
        