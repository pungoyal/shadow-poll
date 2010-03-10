from django.test import TestCase, Client
from apps.poll.models import Question, User
from apps.charts.models import Governorate
from math import ceil

query="?gender=m,f&age=a1,a2,a3"
class ViewTests(TestCase):
    fixtures = ['functional_test_data']
    def setUp(self):
        self.client = Client()

    def test_urls_are_set_up_properly(self):
        # test all map views
        self.assertEquals(self.client.get('/charts/').status_code, 200)
        questions = Question.objects.all()
        governorates = Governorate.objects.all()
        for question in questions:
            url = '/charts/question%s' % question.id + query
            self.assertEquals(self.client.get(url).status_code, 200)
            for governorate in governorates:
                url = '/charts/%s/question%s' % (governorate.id, question.id) + query
                self.assertEquals(self.client.get(url).status_code, 200)

    def test_kml(self):
        # test all map kmls
        questions = Question.objects.all()
        governorates = Governorate.objects.all()
        for question in questions:
            url = '/get_kml/question%s' % question.id + query
            self.assertEquals(self.client.get(url).status_code, 200)
            for governorate in governorates:
                url = '/get_kml/%s/question%s' % (governorate.id, question.id) + query
                self.assertEquals(self.client.get(url).status_code, 200, 
                                  msg = "%s did not return 200" % url)
    
    def test_kml_data(self):        
        response = self.client.get('/get_kml/question1' + query)
        self.assertContains(response, "<scale>0.758620689655</scale>")
        response = self.client.get('/get_kml/7/question1' + query)
        self.assertContains(response, "<scale>0.758620689655</scale>")
        response = self.client.get('/get_kml/5/question2' + query)
        self.assertContains(response, "<scale>0.666666666667</scale>")
        response = self.client.get('/get_kml/7/question2' + query)
        self.assertContains(response, "<scale>0.5</scale>")
        response = self.client.get('/get_kml/question1' + "?gender=f&age=a1,a2")        
        self.assertContains(response, "<scale>0.6</scale>")
    def test_user_filter(self):
        governorate = Governorate.objects.get(id=7)
        self.assertEquals(governorate.user_filter({'gender': 'm,f', 'age': 'a1,a2,a3'}),[1, 2])
        
    def test_messaging_page_is_accesible(self):
        response = self.client.get("/messages/")
        self.assertEquals(response.status_code, 200)
