from django.test import TestCase
from apps.charts.models import *

class GovernoratesTest(TestCase):
    fixtures = ['test_charts']
    
    def test_num_response(self):
        states = Governorates.objects.all()

        self.assertEquals(states[0].num_responses(), 2)
        self.assertEquals(states[1].num_responses(), 1)
        self.assertEquals(states[2].num_responses(), 2)
        self.assertEquals(states[3].num_responses(), 0)
        self.assertEquals(states[4].num_responses(), 0)

    def test_style(self):
        states = Governorates.objects.all()

        self.assertEquals(states[0].style(), "s14")
        self.assertEquals(states[2].style(), "s14")
        self.assertEquals(states[9].style(), "s0")
        self.assertEquals(states[1].style(), "s7")
        
    def test_get_category_from_id(self):
        self.color_map = ColorMap()
        self.cat_id = "3"
        self.color = self.color_map.get_color_for_category(self.cat_id)
        self.assertEquals(str(self.color), "Green")
