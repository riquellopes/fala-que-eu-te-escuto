# coding: utf-8
# http://stackoverflow.com/questions/23039101/using-the-att-speech-to-text-api-with-python
import requests
import urllib
import mimetypes
from functools import wraps

API_URL_ATT = "https://api.att.com"
SPEECH_MIME_TYPE = (
    "audio/x-wav",
)


class SpeechToTextException(Exception):
    pass


def mimetype(types):
    def decorator(function):
        @wraps(function)
        def validation(*args, **kwargs):
            path = kwargs.get("path", None)
            url = urllib.pathname2url(path)
            if mimetypes.guess_type(url)[0] not in SPEECH_MIME_TYPE:
                raise SpeechToTextException("We don't have support.")
            try:
                kwargs['handle'] = open(path, 'rb')
                return function(*args, **kwargs)
            except:
                raise SpeechToTextException("File not exist.")
        return validation
    return decorator


def oauth(func):
    @wraps(func)
    def token(*args, **kwargs):
        selfi = args[0]
        response = requests.post("{0}/oauth/v4/token".format(API_URL_ATT), {
            "client_id": selfi.app_key,
            "client_secret": selfi.app_secret,
            "grant_type": "client_credentials",
            "scope": "SPEECH"
        })
        if response.status_code != 200:
            raise SpeechToTextException("Error on service.")
        kwargs['token'] = response.json()['access_token']
        return func(*args, **kwargs)
    return token


class SpeechToText(object):

    def __init__(self, key, secret):
        self.app_key = key
        self.app_secret = secret

    @oauth
    def to_text(self, token, path, handle):
        with open(path, 'rb') as audio:
            response = requests.post(
                "{0}/speech/v3/speechToText".format(API_URL_ATT),
                headers={
                    "Authorization": "Bearer {0}".format(token),
                    "Accept": "application/json",
                    "Content-Type": "audio/amr",
                    "X-SpeechContext": "Generic"},
                data=audio)
        content = response.json()
        return content

if __name__ == "__main__":
    import os
    s = SpeechToText(
        key=os.environ.get("ATT_APP_KEY"),
        secret=os.environ.get("ATT_APP_SECRET"))

    print s.to_text(file="test/california.amr")
