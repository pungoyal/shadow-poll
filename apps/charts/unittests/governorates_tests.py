from django.test import TestCase
from charts.postcode_name_map import get_name
from charts.models import Governorates
from mox import Mox

class GovernoratesTest(TestCase):
    def test_num_response(self):
        poll_resp = Mock()
        poll_resp.count.return_value = 1
        
        code_name_map = Mock()
        code_name_map.return_value = 31001
        
        gov = Governorates()
        print gov.num_responses(code_name_map, poll_resp)