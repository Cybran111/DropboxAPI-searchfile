__author__ = 'cybran'

import unittest
from SearchCloudFile import MyDropboxAPI
# My token container
import tokens

class MyDropboxAPITest(unittest.TestCase):

    def setUp(self):
        self.app_key = tokens.app_key
        self.app_secret = tokens.app_secret

        self.token_key = tokens.token_key
        self.token_secret = tokens.token_secret

    def testDefaultValues(self):
        api = MyDropboxAPI(self.app_key, self.app_secret)
        api.connect()
        api.isRecentlyChanged()
        self.assertTrue(api.new_file)

    def testValidValues(self):
        api = MyDropboxAPI(self.app_key, self.app_secret)
        api.connect(token_key = self.token_key, token_secret = self.token_secret)
        api.isRecentlyChanged(filename="report.otd", path="")
        self.assertTrue(api.new_file)

    def testInvalidFilename(self):
        api = MyDropboxAPI(self.app_key, self.app_secret)
        api.connect(token_key = self.token_key, token_secret = self.token_secret)
        api.isRecentlyChanged(filename="dummy filename", path="/")
        self.assertFalse(hasattr(api, "new_file"))

    def testInvalidPath(self):
        api = MyDropboxAPI(self.app_key, self.app_secret)
        api.connect(token_key = self.token_key, token_secret = self.token_secret)
        api.isRecentlyChanged(filename="report.otd", path="/dummy_folder")
        self.assertFalse(hasattr(api, "new_file"))

    def testInvalidTokenKey(self):
        api = MyDropboxAPI(self.app_key, self.app_secret)
        from dropbox.rest import ErrorResponse
        self.assertRaises(ErrorResponse, api.connect(token_key = "dummy_key", token_secret = self.app_secret))

    def testInvalidTokenSecret(self):
        api = MyDropboxAPI(self.app_key, self.app_secret)
        from dropbox.rest import ErrorResponse
        self.assertRaises(ErrorResponse, api.connect(token_key = self.token_key, token_secret = 'dummy_key'))

if __name__ == "__main__":
    unittest.main()