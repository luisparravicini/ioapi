import unittest
import os
import json
import requests
import requests_mock
from ioapi import IOService, AuthorizationError, UnexpectedResponseCodeError


class IOServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.service = IOService()

    def _read_mock_response(self, name):
        path = os.path.join(os.path.dirname(__file__), name + '.json')
        with open(path, 'r') as file:
            data = json.loads(file.read())
        return data

    @requests_mock.mock()
    def test_account_state_without_auth(self, mock):
        data = self._read_mock_response('account_state_without_auth')
        mock.get(
            self.service.api + IOService.URL_ACCOUNT_STATE,
            json=data,
            status_code=401)

        with self.assertRaises(AuthorizationError):
            self.service.get_account_state()

    @requests_mock.mock()
    def test_account_state_auth_not_ok(self, mock):
        data = self._read_mock_response('account_state_not_ok')

        for code in range(201, 600):
            # skip 401 status code (unauthorized)
            if code == 401:
                continue

            mock.get(
                self.service.api + IOService.URL_ACCOUNT_STATE,
                json=data,
                status_code=code)

            with self.assertRaises(UnexpectedResponseCodeError) as cm:
                self.service.get_account_state()
            self.assertEqual(cm.exception.status_code, code)

    @requests_mock.mock()
    def test_account_state(self, mock):
        data = self._read_mock_response('account_state')
        self.service = IOService()
        mock.get(
            self.service.api + IOService.URL_ACCOUNT_STATE,
            json=data)

        self.assertEqual(self.service.get_account_state(), data)
        self.fail("auth missing")
