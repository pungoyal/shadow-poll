from apps.poll.messages import FINAL_APPRECIATION_MESSAGE,TRIGGER_INCORRECT_MESSAGE
from apps.poll.responder import Responder
clean = lambda s : s.strip().lower()     

class TriggerResponder(Responder):
    
    def __init__(self,kwargs):
        super(TriggerResponder, self).__init__(kwargs)
        self.criteria = lambda message:clean(message).find(clean(self.trigger)) > -1


    def action(self,message):
        
        user_info = dict(iter([(parser.name,parser.parse(message)) for parser in self.parsers]))
        
        if len(user_info) != len(self.parsers):
            return TRIGGER_INCORRECT_MESSAGE
        
        for key in user_info:
            self.user.set_value(key,user_info[key])
            
        self.session.question = self.next_question
        
        return str(self.session.question)    

