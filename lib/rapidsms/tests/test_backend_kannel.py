#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

""" 
Even though these unit tests do not test anything external
to this file, they are useful to verify our understanding 
of how kannel.py deals with various different types of 
input that it receives from the kannel process

"""

import urllib
import unittest

def geturl_to_unicode(input):
    return urllib.unquote_plus(input).decode('utf-8')

class TestBackendSpomc(unittest.TestCase):

    def test_hex_to_ar(self):
        # test basic understanding of encoding and decoding
        x = 'd981'
        a = x.decode('hex_codec').decode('utf-8')
        self.assertEquals(a,u'ف')

        x = '0647'
        a = x.decode('hex_codec').decode('utf-16-be')
        self.assertEquals(a,u'ه')

    def test_percent_to_ar(self):
        # arabic
        in_ = '%d9%81'
        a = geturl_to_unicode(in_)
        self.assertEquals(a,u'ف')

    def test_percentspace_to_ar(self):
        # space
        in_ = '%d9%81+%d9%81'
        a = geturl_to_unicode(in_)
        self.assertEquals(a,u'ف ف')

    def test_percentnum_to_ar(self):
        # number
        in_ = '%d9%81234'
        a = geturl_to_unicode(in_)
        self.assertEquals(a,u'ف234')

    def test_percentplus_to_ar(self):
        # reserved characters
        in_ = '%d9%81%24%26%2b'
        a = geturl_to_unicode(in_)
        self.assertEquals(a,u'ف$&+')

if __name__ == "__main__":
    unittest.main()
