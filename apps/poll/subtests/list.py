from unittest import TestCase
from apps.poll.list import remove_duplicates

class ListTest(TestCase):

    def test_remove_duplicates(self):
        self.assertEquals([1,2,3], remove_duplicates([1,2,3,1]))
                          
