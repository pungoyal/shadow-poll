from poll.models import User
from poll.models import UserResponse
from poll.models import Questionnaire

class BulkMessageProcessor(object):
    def __init__(self, message):
        self.message = message
        self.answer_list = []
        self.questionnaire = None
        
    def parse_and_create_user(self, connection, message):
        message_arr = self.message.split(" ")
        self.user = User(connection = connection, governorate = connection.governorate, district = connection.district, active = True)
        self.answer_list.append(message_arr[3])
        self.answer_list.append(" ".join(message_arr[4:7]))
        self.answer_list.append(message_arr[7])
        self.answer_list.reverse()
        return self.answer_list

    def save_user_and_responses(self, message_arr):
        self.user.save()
        self._set_default_questionnaire()
        question_list = []
        question = self.questionnaire.first_question()
        while question is not None:
            question_list.append(question)
            question = question.next_question
        
        for (counter, question) in enumerate(question_list):
            choices = question.matching_choices(self.answer_list[counter])
            for ch in choices:
                UserResponse(user = self.user, question = question, choice = ch).save()
    
    def _set_default_questionnaire(self):
        if not self.questionnaire:
            self.questionnaire = Questionnaire.objects.all().order_by('pk')[0]

