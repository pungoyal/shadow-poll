from charts.models import Question,Choice,PollResponse

class ChartData():
    def no_of_responses(self, questionId):
        question = self.__load_question(questionId)
        return question.choice_set.count()

    def response_counts(self, questionId):
        choices = Choice.objects.filter(question_id=questionId)
        return choices.count()
        
    def __load_question(self, questionId):
        return Question.objects.filter(id=questionId)[0]


