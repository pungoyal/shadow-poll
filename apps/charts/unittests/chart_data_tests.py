import unittest
import rapidsms
import mox
from rapidsms.tests.scripted import TestScript
from iraq.models import Question,Choice
from charts.chart_data import ChartData
from charts.model_adapter import ModelAdapter

class ChartDataTests (unittest.TestCase):
    def test_count_of_answers_for_first_question(self):
        chartData = ChartData()
        self.assertEquals(chartData.no_of_choices(1),5)

    def test_response_counts(self):
        responses = ChartData().responses_by_choice(1)
        self.assertEquals(len(responses),5)

        
