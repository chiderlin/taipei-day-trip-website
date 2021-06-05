import unittest
import sys
sys.path.append("C:\\Users\\user\\Desktop\\GitHub\\taipei-day-trip-website")
from app import app


class TestPageConnection(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        res = tester.get("/")
        statuscode = res.status_code
        self.assertEqual(statuscode, 200)

    def test_attraction(self):
        tester = app.test_client(self)
        res = tester.get("/attraction/1")
        statuscode = res.status_code
        self.assertEqual(statuscode, 200)

    def test_booking(self):
        tester = app.test_client(self)
        res = tester.get("/booking")
        statuscode = res.status_code
        self.assertEqual(statuscode, 200)

    def test_thankyou(self):
        tester = app.test_client(self)
        res = tester.get("/thankyou")
        statuscode = res.status_code
        self.assertEqual(statuscode, 200)

    def test_historyorder(self):
        tester = app.test_client(self)
        res = tester.get("/historyorder")
        statuscode = res.status_code
        self.assertEqual(statuscode, 200)



if __name__ == "__main__":
    unittest.main()