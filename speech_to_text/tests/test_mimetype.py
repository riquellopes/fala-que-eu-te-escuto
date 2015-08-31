# coding: utf-8
import unittest
from nose.tools import assert_raises
from speech_to_text import mimetype, SpeechToTextException


class TestMimetype(unittest.TestCase):

    def test_1(self):
        """
            Should exception if mimetype be block.
        """
        @mimetype(["wav", "amr"])
        def mimetype(file):
            pass
        assert_raises(SpeechToTextException, mimetype, "california.mp3")
