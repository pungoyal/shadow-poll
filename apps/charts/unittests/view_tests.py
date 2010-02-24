from django.test import TestCase, Client

class ViewTests(TestCase):
    
    fixtures = ['functional_test_data', 'poll_interactive']
    def setUp(self):
        self.client = Client()        

    def test_urls_are_set_up_properly(self):
        self.assertEquals(self.client.get('/charts/').status_code, 200)
        self.assertEquals(self.client.get('/charts/10').status_code, 200)
        self.assertEquals(self.client.get('/charts/question1').status_code, 200)
