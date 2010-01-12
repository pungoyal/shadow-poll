import unittest
import rapidsms
from rapidsms.tests.scripted import TestScript
from charts.chart_data import ChartData

class ChartDataTests (unittest.TestCase):
    def test_count_of_answers_for_first_question(self):
        chartData = ChartData()
        self.assertEquals(chartData.no_of_responses(1),5)

    def test_response_counts(self):
        responses = ChartData().response_counts(1)
        self.assertEquals(responses.count(),5)

        
