# coding: utf-8
# http://stackoverflow.com/questions/23039101/using-the-att-speech-to-text-api-with-python
import requests
from functools import wraps


def oauth(func):
    @wraps(func)
    def token(*args, **kwargs):
        selfi = args[0]
        response = requests.post("https://api.att.com/oauth/v4/token", {
            "client_id": selfi.app_key,
            "client_secret": selfi.app_secret,
            "grant_type": "client_credentials",
            "scope": "SPEECH"
        })
        kwargs['token'] = response.json()['access_token']
        return func(*args, **kwargs)
    return token


class SpeechToText(object):

    def __init__(self, key, secret):
        self.app_key = key
        self.app_secret = secret

    @oauth
    def to_text(self, token, file):
        with open(file, 'rb') as audio:
            response = requests.post(
                "https://api.att.com/speech/v3/speechToText",
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

    print s.to_text(file="california.amr")
