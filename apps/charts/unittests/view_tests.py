from django.test import TestCase, Client
from apps.poll.models import Question
from apps.charts.models import Governorate

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
            url = '/charts/question%s' % question.id
            self.assertEquals(self.client.get(url).status_code, 200)
            for governorate in governorates:
                url = '/charts/%s/question%s' % (governorate.id, question.id)
                self.assertEquals(self.client.get(url).status_code, 200)

    def test_kml(self):
        # test all map kmls
        questions = Question.objects.all()
        governorates = Governorate.objects.all()
        for question in questions:
            url = '/get_kml/question%s' % question.id
            self.assertEquals(self.client.get(url).status_code, 200)
            for governorate in governorates:
                url = '/get_kml/%s/question%s' % (governorate.id, question.id)
                self.assertEquals(self.client.get(url).status_code, 200, 
                                  msg = "%s did not return 200" % url)
    
    def test_kml_data(self):
        # test kml contents
        response = self.client.get('/get_kml/question1')
        self.assertContains(response, "<scale>0.782608695652</scale>")
        self.assertContains(response, "<scale>0.878787878788</scale>")

    def test_messaging_page_is_accesible(self):
        response = self.client.get("/messages")
        self.assertEquals(response.status_code, 200)
