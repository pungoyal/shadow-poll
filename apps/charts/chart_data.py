from poll.models import Question, Choice, PollResponse
from model_adapter import ModelAdapter

class ChartData():

    data_adapter = ModelAdapter()

    def __init__(self,data_adapter=None):
        self.data_adapter = data_adapter or self.data_adapter
    
    def no_of_choices(self, questionId):
        question = self.data_adapter.load_question_by_id(questionId)
        return question.choice_set.count()

    def responses_by_choice(self, questionId):
        responses_by_choice = {}
        choices = self.data_adapter.load_choices_by_question(questionId)
        for choice in choices:
            responses_by_choice[choice.choice] = choice.pollresponse_set.all().count()
        return responses_by_choice


