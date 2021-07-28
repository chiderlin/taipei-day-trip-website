import json
from dotenv import load_dotenv
import os
import unittest
import sys
sys.path.append("C:\\Users\\user\\Desktop\\GitHub\\taipei-day-trip-website")
from app import app
from model.db import DB_controller

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PWD")
DB_NAME = os.getenv("DB_NAME")


class TestLoginStatus(unittest.TestCase):
    def setUp(self):
        self.url = "/api/user"
        app.testing = True
        self.app = app.test_client()
        self.email = "chi@chi.com"
        self.pwd = "123"
        self.data = {"email":self.email, "password":self.pwd}

    def login(self):
        headers = {"Content-Type":"application/json;charset=UTF-8"}
        return self.app.patch(self.url, data=json.dumps(self.data), headers=headers)

    def get_login(self):
        return self.app.get(self.url)

    def logout(self):
        return self.app.delete(self.url)

    def test_login(self):
        login = self.login()
        self.assertEqual(login.status_code, 200)

    def test_login_400(self):
        self.pwd = "111"
        self.data = {"email":self.email, "password":self.pwd}
        login = self.login()
        self.assertEqual(login.status_code, 400) 

    def test_login_info(self):
        self.login()
        get_info = self.get_login()
        self.assertEqual(get_info.json, {'data': {'email': 'chi@chi.com', 'id': 35, 'name': 'chichi'}})

    def test_logout(self):
        self.login()
        get_info = self.get_login()
        self.assertEqual(get_info.json, {'data': {'email': 'chi@chi.com', 'id': 35, 'name': 'chichi'}})
        logout = self.logout()
        self.assertEqual(logout.json, {'ok': True})
        get_info = self.get_login()
        self.assertEqual(get_info.json, {'data': None})



class TestRegister(unittest.TestCase):
    def setUp(self):
        self.url = "/api/user"
        app.testing = True
        self.app = app.test_client()
        self.name = "imi"
        self.email = "imi@mi.com"
        self.pwd = "123"
        self.data = {"name":self.name, "email":self.email, "password":self.pwd}
    
    def tearDown(self): #失敗 無法刪除db裡的資料
        db = DB_controller(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PWD,
            db=DB_NAME
        )
        db.delete(table_name="user", column_name="name", value=self.name)
        db.close()

    def register(self):
        headers = {"Content-Type":"application/json;charset=UTF-8"}
        return self.app.post(self.url, data=json.dumps(self.data),headers=headers)

    def test_register_400(self): #註冊過了
        self.name = "chichi"
        self.email = "chi@chi.com"
        self.pwd = "123"
        self.data = {"name":self.name, "email":self.email, "password":self.pwd}
        register = self.register()
        self.assertEqual(register.status_code, 400)

    def test_register_200(self):
        register = self.register()
        self.assertEqual(register.status_code, 200)





if __name__ == "__main__":
    unittest.main()