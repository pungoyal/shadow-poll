import unittest
from apps.charts.models import VoiceMessage

class VoiceMessageTest(unittest.TestCase):
    def test_get_child_image(self):
        voice_message = VoiceMessage(female=False)
        self.assertEquals(voice_message.get_child_image(), "child_boy")

        voice_message = VoiceMessage(female=True)
        self.assertEquals(voice_message.get_child_image(), "child_girl")

        voice_message = VoiceMessage()
        self.assertEquals(voice_message.get_child_image(), "child_no_identity")