from django.test import TestCase
from charts.feature_info_request_parser import convert_text_to_dicts
from charts.unittests.mock_geo_server import MockGeoServer

class ViewTests(TestCase):
    
    def test_feature_info_request_parse(self):
        geo_server = MockGeoServer()
        response_dict = convert_text_to_dicts(geo_server.get_feature_info())
        dict_to_assert={'NAME_2': 'Ar Rutbah', 'NAME_0': 'Iraq', 'NAME_1': 'Al-Anbar', 'VARNAME_2': '', 'Shape_Area': '9.37942880399', 'NL_NAME_2': '', 'VALIDTO_2': '', 'HASC_2': '', 'REMARKS_2': '', 'ID_2': '16581', 'TYPE_2': '', 'ID_0': '109', 'ID_1': '1378', 'ISO': 'IRQ', 'CC_2': '', 'Shape_Leng': '14.0594266947', 'VALIDFR_2': '', 'the_geom': '[GEOMETRY (MultiPolygon) with 564 points]', 'ENGTYPE_2': ''}
        self.assertEqual(dict_to_assert, response_dict)
