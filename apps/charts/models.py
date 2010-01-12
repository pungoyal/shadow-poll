from django.db import models
from iraq.models import Responses

class Responses():
    def numberOfAnswers(self):
        firstQuestion = Question.objects.all()[0]
        return firstQuestion.answer_set.count()
    
        

        
        




