class MessageParser(object):
    def __init__(self, message):
        self.message = message
        
    def parse(self):
        message_arr = self.message.split(" ")
        
        return message_arr

        

