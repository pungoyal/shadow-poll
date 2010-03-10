from apps.poll.messages import FINAL_APPRECIATION_MESSAGE,TRIGGER_INCORRECT_MESSAGE

clean = lambda s : s.strip().lower()     

class TriggerResponder(object):
    
    def __init__(self,kwargs):
        self.trigger = kwargs.get("trigger","poll")
        self.parsers = kwargs.get("parsers", [])
        self.user = kwargs.get("user", None)
        self.question =  kwargs.get("question", FINAL_APPRECIATION_MESSAGE)

        self.criteria = lambda message:clean(message).find(clean(self.trigger)) > -1


    def action(self,message):
        
        user_info = dict(iter([(parser.name,parser.parse(message)) for parser in self.parsers]))
        
        if len(user_info) != len(self.parsers):
            return TRIGGER_INCORRECT_MESSAGE
        
        for key in user_info:
            self.user.set_value(key,user_info[key])
            
        return self.question    
