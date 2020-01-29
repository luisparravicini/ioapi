import unittest
import os
import json
import requests
import requests_mock
from ioapi import api_url, IOService, AuthorizationError, UnexpectedResponseCodeError


class APIAccountStateTestCase(unittest.TestCase):

    def setUp(self):
        self.service = IOService()

    @requests_mock.mock()
    def test_account_state_without_auth(self, mock):
        data = self._read_mock_response('account_state_without_auth')
        self._setup_response(mock, data, 401)

        with self.assertRaises(AuthorizationError):
            self.service.get_account_state()

    @requests_mock.mock()
    def test_account_state_auth_not_ok(self, mock):
        data = self._read_mock_response('account_state_not_ok')

        for code in range(201, 600):
            # skip 401 status code (unauthorized)
            if code == 401:
                continue

            self._setup_response(mock, data, code)

            with self.assertRaises(UnexpectedResponseCodeError) as cm:
                self.service.get_account_state()
            self.assertEqual(cm.exception.status_code, code)

    @requests_mock.mock()
    def test_account_state(self, mock):
        data = self._read_mock_response('account_state')
        self.service = IOService()
        self._setup_response(mock, data)

        self.assertEqual(self.service.get_account_state(), data)
        self.fail("auth missing")

    def _read_mock_response(self, name):
        path = os.path.join(os.path.dirname(__file__), name + '.json')
        with open(path, 'r') as file:
            data = json.loads(file.read())
        return data

    def _setup_response(self, mock, response, code=None):
        if code is None:
            code = requests.codes.ok
        mock.get(
            self.service.api + api_url.URL_ACCOUNT_STATE,
            json=response,
            status_code=code)
