from unittest import TestCase, mock
import requests


class TestTranslateDeprecated(TestCase):

    METHOD_NOT_ALLOWED = 405
    OK = 200
    URL = "http://127.0.0.1:5000/translate/"
    
    def test_post_method(self):

        SOURCE = "How are you?"
        TRANSLATION = "Com estàs?"

        payload = {"languages" : "eng-cat", "text" : "How are you?"}
        response = requests.post(self.URL, json = payload)
        json = response.json()
        self.assertEquals(self.OK, response.status_code)
        self.assertEquals(SOURCE, json["text"])
        self.assertEquals(TRANSLATION, json["translated"])
        self.assertTrue(len(json["time"]) > 0)

