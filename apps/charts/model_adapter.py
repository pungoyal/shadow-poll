from iraq.models import Question, Choice

class ModelAdapter():
    def load_choices_by_question(self, questionId):
        return Choice.objects.filter(question=questionId)
        
    def load_question_by_id(self, questionId):
        return Question.objects.filter(id=questionId)[0]
