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
        def hello(handle, path=None):
            pass
        assert_raises(SpeechToTextException, hello, path="california.mp3")

    def test_2(self):
        """
            Should audio/amr file is permitted.
        """
        @mimetype(["wav", "amr"])
        def hello(handle, path=None):
            return str(type(handle))
        str_hello = hello(path="speech_to_text/tests/boston_celtics.wav")
        assert str_hello == "<type 'file'>"
