from django.test import TestCase, Client
from apps.poll.models import Question, User
from apps.charts.models import Governorate
from math import ceil

query="?gender=m,f&age=a1,a2,a3"
class ViewTests(TestCase):
    fixtures = ['functional_test_data', 'messages']
    def setUp(self):
        self.client = Client()

    def test_urls_are_set_up_properly(self):
        # test all map views
        self.assertEquals(self.client.get('/charts/').status_code, 200)
        questions = Question.objects.all()
        governorates = Governorate.objects.all()
        for question in questions:
            url = '/charts/question%s/' % question.id
            self.assertEquals(self.client.get(url).status_code, 200)
            for governorate in governorates:
                url = '/charts/question%s/governorate%s/' % (question.id, governorate.id)
                self.assertEquals(self.client.get(url).status_code, 200)

    def test_kml(self):
        # test all map kmls
        questions = Question.objects.all()
        governorates = Governorate.objects.all()
        for question in questions:
            url = '/get_kml/question%s' % question.id
            self.assertEquals(self.client.get(url).status_code, 200)
            for governorate in governorates:
                url = '/get_kml/question%s/governorate%s/' % (question.id, governorate.id)
                self.assertEquals(self.client.get(url).status_code, 200, 
                                  msg = "%s did not return 200" % url)
    
    def test_kml_data(self):        
        response = self.client.get('/get_kml/question1' + query)
        self.assertContains(response, "<scale>0.758620689655</scale>")
        response = self.client.get('/get_kml/question1/governorate7' + query)
        self.assertContains(response, "<scale>0.758620689655</scale>")
        response = self.client.get('/get_kml/question2/governorate5' + query)
        self.assertContains(response, "<scale>0.666666666667</scale>")
        response = self.client.get('/get_kml/question2/governorate7' + query)
        self.assertContains(response, "<scale>0.5</scale>")

    def test_messaging_pages_is_accesible(self):
        response = self.client.get("/messages/")
        self.assertEquals(response.status_code, 200)
        login = self.client.login(username='a', password='a')
        self.failUnless(login, 'Could not log in')
        response = self.client.get("/messages/translate/")
        self.assertEquals(response.status_code, 200)
        response = self.client.get("/message/translate/1")
        self.assertEquals(response.status_code, 200)


    def test_all_governorates(self):
        response1 = self.client.get("/charts/question1")
        response2 = self.client.get("/charts/question1/all")
        self.assertEquals(response1.content,response2.content)
