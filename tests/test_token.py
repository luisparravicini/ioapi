import unittest
import os
import json
import requests
import requests_mock
from ioapi import api_url, IOService, AuthorizationError, UnexpectedResponseCodeError


class APITokenTestCase(unittest.TestCase):

    def setUp(self):
        self.service = IOService()

    @requests_mock.mock()
    def test_login_bad_cred(self, mock):
        data = self._read_mock_response('token_bad_cred')
        self._setup_response(mock, data, 401)

        usr = 'abc'
        passw = '1234'
        with self.assertRaises(AuthorizationError):
            self.service.get_token(usr, passw)

    @requests_mock.mock()
    def test_login(self, mock):
        data = self._read_mock_response('account_state')
        self.service = IOService()
        self._setup_response(mock, data)

        usr = 'ok'
        passw = '12345678'
        self.assertEqual(self.service.get_token(usr, passw), data)
        self.fail("auth missing")

    def _read_mock_response(self, name):
        path = os.path.join(os.path.dirname(__file__), name + '.json')
        with open(path, 'r') as file:
            data = json.loads(file.read())
        return data

    def _setup_response(self, mock, response, code=None):
        if code is None:
            code = requests.codes.ok
        mock.post(
            self.service.api + api_url.URL_TOKEN,
            json=response,
            status_code=code)
