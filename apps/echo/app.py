import rapidsms
import re

class App(rapidsms.app.App):
    prefix = re.compile(r'^echo\s+',re.I)
    def handle(self, message):
        pass
