import unittest
import requests
import requests_mock
from ioapiwrapper import IOService


class IOServiceTestCase(unittest.TestCase):
    @requests_mock.mock()
    def test_a(self, mock):
        service = IOService()
        # service.api = None#'http://localhost:8080'
        mock.get(service.api + IOService.URL_ACCOUNT_STATE, text='data')

        service.get_account_state()
        self.assertEqual(fun(3), 4)
