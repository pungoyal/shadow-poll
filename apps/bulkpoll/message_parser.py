from poll.models import User, Question, UserResponse, Questionnaire

class BulkMessageProcessor(object):
    def __init__(self):
        self.questionnaire = None
        
    def parse_and_create_user(self, message, connection):
        answers = []
        message_parts = message.split(" ")

        self.user = User(connection = connection, governorate = connection.governorate, district = connection.district, active = True)

        try:
            self.user.age = int(message_parts[1])
            self.user.gender = message_parts[2]
        except ValueError:
            return "bulk_response_error"

        answers.append(message_parts[3])
        answers.append(" ".join(message_parts[4:7]))
        answers.append(message_parts[7])
        
        return answers

    def save_user_and_responses(self, answers):
        self.user.save()
        self._set_default_questionnaire()

        questions = Question.objects.filter(questionnaire = self.questionnaire).order_by('id')

        matching_choices = []

        for (counter, question) in enumerate(questions):
            choices_for_one_question = question.matching_choices(answers[counter])

            matching_choices.append(choices_for_one_question)

            if len(choices_for_one_question) < 1:
                return "bulk_response_error"

        for (counter, question) in enumerate(questions):
            for choice in matching_choices[counter]:
                UserResponse(user = self.user, question = question, choice = choice).save()

        return "thanks"
    
    def _set_default_questionnaire(self):
        if not self.questionnaire:
            self.questionnaire = Questionnaire.objects.all().order_by('pk')[0]

