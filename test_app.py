#test_app.py

import unittest
import os
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_upload_valid_pdf(self):
        with open("sample.pdf", "rb") as file:
            response = self.app.post("/upload", data={"file": file})
            self.assertEqual(response.status_code, 200)
            self.assertIn('report', response.json)

    def test_upload_invalid_file(self):
        response = self.app.post("/upload", data={"file": (open("sample.txt", "rb"), 'sample.txt')})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()