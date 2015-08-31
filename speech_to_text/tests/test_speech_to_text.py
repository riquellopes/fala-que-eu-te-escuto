# coding: utf-8
import unittest
import responses
import json
from nose.tools import assert_equals, assert_raises
from speech_to_text import API_URL_ATT, oauth, SpeechToTextException


class TestSpeechToText(unittest.TestCase):

    @responses.activate
    def test_1(self):
        """
            Should get token when decorator @auth invoked.
        """
        token = u'BF-ACSI~4~20150830211106~tnBvTSKks0whYTlE8oix3nNX93wLNCi0'
        reponse = {
            'access_token': token,
            'token_type': u'bearer',
            'expires_in': 172799,
            'refresh_token': u'j0A29dO3qzuyoHgtSPLlRICKuxSUdwMW'
        }

        responses.add(
            responses.POST,
            "{0}/oauth/v4/token".format(API_URL_ATT),
            body=json.dumps(reponse),
            status=200)

        class Dummy(object):
            app_key = 123
            app_secret = 456

            @oauth
            def get_token(self, token):
                return token
        dummy = Dummy()
        assert_equals(dummy.get_token(), token)

    @responses.activate
    def test_2(self):
        """
            Should exception if service get status different of 200.
        """
        responses.add(
            responses.POST,
            "{0}/oauth/v4/token".format(API_URL_ATT),
            body="",
            status=500)

        class Dummy(object):
            app_key = 123
            app_secret = 456

            @oauth
            def get_token(self, token):
                return token
        dummy = Dummy()
        assert_raises(SpeechToTextException, dummy.get_token)
