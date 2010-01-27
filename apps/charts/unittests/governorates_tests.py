from django.test import TestCase
from charts.postcode_name_map import get_name
from charts.models import Governorates
from mock import Mock

class GovernoratesTest(TestCase):
    def test_num_response(self):
        get_name = Mock()
        get_name.return_value = 31001
        