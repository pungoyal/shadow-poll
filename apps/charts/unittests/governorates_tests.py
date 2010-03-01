from django.test import TestCase
from apps.charts.models import *
from poll.app import App as poll_app
from poll.models import Question, Color
class GovernorateTest(TestCase):
    fixtures = ['test_charts', 'functional_test_data.json', 'poll_interactive']
    apps = (poll_app,)

    def fails_test_num_response(self):
        states = Governorate.objects.all()

        self.assertEquals(states[0].num_responses(), 2)
        self.assertEquals(states[1].num_responses(), 1)
        self.assertEquals(states[2].num_responses(), 2)
        self.assertEquals(states[3].num_responses(), 0)
        self.assertEquals(states[4].num_responses(), 0)

    def fails_test_style(self):
        states = Governorate.objects.all()

        self.assertEquals(states[0].style(), "s14")
        self.assertEquals(states[2].style(), "s14")
        self.assertEquals(states[9].style(), "s0")
        self.assertEquals(states[1].style(), "s7")
    
    def test_style(self):
        gov1 = Governorate.objects.get(id = 7)
        gov = Governorate.objects.get(id = 5)
        question = Question.objects.get(id = 1)
        color = Color.objects.get(id=1)
        color1 = Color.objects.get(id=2)
        self.assertEquals(gov.style(question), {'color': color, 'percentage': 0.78260869565217395})
        self.assertEquals(gov1.style(question), {'color': color1, 'percentage': 0.87878787878787878} )
