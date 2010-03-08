from django.utils import simplejson
from django.core import serializers
from django.test import TestCase

from apps.poll.models import ResponseBreakUp,Category

class ResponseBreakUpTest(TestCase):
    # to ensure we do not add 'unserializable' objects in ResponseBreakUp
    def test_serializable(self):
        r = ResponseBreakUp()
        json = simplejson.dumps(r.__dict__)
        self.assertNotEquals(json.find("color"), -1)
        self.assertNotEquals(json.find("text"), -1)
        self.assertNotEquals(json.find("percentage"), -1)
        self.assertEquals(json.find("somerandomtext"), -1)

        list = []
        list.append(r)
        list.append(ResponseBreakUp(choice_text="foo", percentage=12.21, color="#ff0000", category_text="bar"))
        list.append(r)

        json = simplejson.dumps([r.__dict__ for r in list])
        self.assertNotEquals(json.find("#ff0000"), -1)
        self.assertNotEquals(json.find("foo"), -1)
        self.assertNotEquals(json.find("12.21"), -1)
        self.assertNotEquals(json.find("bar"), -1)
