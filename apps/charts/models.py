from django.db import models
from iraq.models import Question,PollResponse

class Responses():
    def number_of_answers(self):
        firstQuestion = Question.objects.all()[0]
        return firstQuestion.choice_set.count()
    
        

        
        




