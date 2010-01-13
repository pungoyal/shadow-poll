from rapidsms.tests.scripted import TestScript
from iraq.app import App
from iraq.models import *

class TestApp(TestScript):
    apps = (App,)

    testIncorrectResponse = """
      98804 > test
      98804 < Sorry, we did not understand your response. Please re-send as - issue age gender area
    """

    testCorrectResponse = """
      98804 > ED 10 M 110010
      98804 < Thank you for voting. You selected Education as your number one issue.
    """
