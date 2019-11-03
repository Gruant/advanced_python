import requests
import unittest


class TranslateTest(unittest.TestCase):

    def setUp(self):
        self.API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
        self.URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
        self.params = {
            'key': self.API_KEY,
            'text': 'Hello',
            'lang': '{}-{}'.format('en', 'ru'),
            'option': 1
        }
        self.response = requests.get(self.URL, self.params)
        self.json = self.response.json()
        self.result = ''.join(self.json['text'])

    def test_positive_response(self):
        self.assertEqual(200, self.response.status_code)

    def test_right_translate(self):
        self.assertEqual('Привет', self.result)

    @unittest.expectedFailure
    def test_negative_response(self):
        self.assertEqual(401, self.response.status_code, 'API_KEY is invalid')


if __name__ == '__main__':
    unittest.main()



