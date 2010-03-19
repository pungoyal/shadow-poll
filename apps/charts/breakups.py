from django.utils.translation import ugettext as _
from poll.models import Color

class ResponseBreakUp():
    def __init__(self, text=_("No responses yet"), percentage=0, color = '#FAAFBE'):
        self.percentage = percentage
        self.color = color
        self.text = text

    @classmethod
    def create_from(klass, responses, categories):
        breakups = []
        total_responses = sum([response_for_category["votes"] for response_for_category in responses])

        if len(responses) == 0:
            return [ResponseBreakUp(text = "No responses yet")]

        for response in responses:
            category = filter(lambda cat: cat.id == response["choice__category"], categories)[0]
            breakup  = ResponseBreakUp(percentage = round(response["votes"]*100/total_responses,1), color = category.color.code, text = category.name )
            breakups.append(breakup)
        return breakups


class ChoiceBreakUp():
    def __init__(self, text=_("No responses yet"), votes=0, color = Color('#FAAFBE', 'grey_dot.gif')):
        self.votes = votes
        self.color = color
        self.text = text

    @classmethod
    def create_from(klass, responses, choices):
        breakups = []
        for choice in choices :
            response = filter(lambda r : r["choice"] == choice.id, responses)
            breakup = ChoiceBreakUp(votes = response[0]["votes"] if len(response) > 0 else 0, color = choice.category.color, text = choice.text )
            breakups.append(breakup)
        return breakups
