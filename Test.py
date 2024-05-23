import unittest
import warnings
from Api import app

class MyTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_getemployee(self):
        response = self.app.get("/employee")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("John" in response.data.decode())

    def test_getemployee_by_ssn(self):
        response = self.app.get("/employee/123456789")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("John" in response.data.decode())

if __name__ == "__main__":
    unittest.main()
