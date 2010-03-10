from apps.poll.messages import FINAL_APPRECIATION_MESSAGE
from apps.poll.responder import Responder

class ValidAnswerResponder(Responder):

    def __init__(self,kwargs):
        super(ValidAnswerResponder,self).__init__(kwargs)
        self.criteria = lambda message : len(self.session.question.matching_choices(message)) > 0

    def action(self,message):
        pass
        
