from rapidsms.tests.scripted import TestScript
from poll.app import App
from poll.models import *

class TestApp(TestScript):
    fixtures = ['poll_responses.json']
    apps = (App,)

    testIncorrectResponse = """
      98804 > test
      98804 < Sorry, we did not understand your response. Please re-send as - issue age gender area
    """

    testCorrectResponse = """
      98804 > ED 10 M 110010
      98804 < Thank you for voting. You selected Education as your number one issue.
      10000 > ED 10 J 110010
      10000 < Thank you for voting. You selected Education as your number one issue.
    """
