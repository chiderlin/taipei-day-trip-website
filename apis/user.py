from flask import Blueprint
from flask import request, jsonify, make_response, session
import hashlib
import re
import os
from dotenv import load_dotenv
import sys
sys.path.append("C:\\Users\\user\\Desktop\\GitHub\\taipei-day-trip-website")
# sys.path.append("/home/ubuntu/root/taipei-day-trip-website")
from model.db import DB_controller


load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PWD")
DB_NAME = os.getenv("DB_NAME")
HASH = os.getenv("HASH")
# with open("./data/config.json", mode="r", encoding="utf-8") as f: # 在app執行程式，所以依照app.py的位置來寫路徑
#     conf = json.load(f)

user = Blueprint("user", __name__)
# user.secret_key = "test@test.com" //要在app設secret_key才對


@user.route("/user", methods=["GET"])
def get_logined_user():
    '''logined user infomation'''
    if request.method == "GET":
        # 判斷有sessionId  => 取得db裡的資料 => 回傳使用者資料
        if session.get("email") is None:
            return jsonify({"data": None})
        else:
            try:
                db = DB_controller(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PWD,
                    db=DB_NAME
                )
                data = db.show_data("user", "email", session.get("email"))
                db.close()
                res = make_response(jsonify({"data": {
                    "id": data[0],
                    "name": data[1],
                    "email": data[2]
                }}))
                return res
            except Exception as e:
                return jsonify({"error": True, "message": str(e)}), 500


@user.route("/user", methods=["POST"])
def user_register():
    '''new user register process'''
    if request.method == "POST":
        post_data = request.get_json()
        # 登入才要給一個sessionId
        name = post_data["name"]
        email = post_data["email"]
        pwd = post_data["password"]
        rex_email = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" # email格式
        match = re.match(rex_email, email)
        if name == "":
            return jsonify({"error": True, "message": "不可為空值"}), 400 
        
        if email == "":
            return jsonify({"error": True, "message": "不可為空值"}), 400

        if not match:
            return jsonify({"error": True, "message": "請輸入正確email"}), 400 

        if pwd == "":
            return jsonify({"error": True, "message": "不可為空值"}), 400 
        try:
            db = DB_controller(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PWD,
                db=DB_NAME
            )
            email_check = db.show_data("user", "email", email)
            name_check = db.show_data("user", "name", name)
            if not email_check:
                if not name_check:
                    hash_ = HASH
                    hash_pwd = pwd + hash_
                    hash_pwd = hashlib.sha256(
                        hash_pwd.encode("utf-8")).hexdigest()
                    db.insert_data("user", "name, email, password",
                                   f'"{name}","{email}","{hash_pwd}"')
                    db.close()
                    res = make_response(jsonify({"ok": True}))
                    return res
                else:
                    return jsonify({"error": True, "message": "此暱稱已被使用"}), 400
            else:
                return jsonify({"error": True, "message": "此email已註冊過"}), 400
        except Exception as e:
            return jsonify({"error": True, "message": str(e)}), 500


@user.route("/user", methods=["PATCH"])
def user_login():
    '''user login process'''
    if request.method == "PATCH":
        login_data = request.get_json()
        # 這樣應該就會回傳sessionId到使用者Response Headers
        email = login_data["email"]
        pwd = login_data["password"]
        rex_email = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" # email格式
        match = re.match(rex_email, email)
        if email == "":
            return jsonify({"error": True, "message": "不可為空值"}), 400
            
        if not match:
            return jsonify({"error": True, "message": "請輸入正確email"}), 400 

        if pwd == "":
            return jsonify({"error": True, "message": "不可為空值"}), 400 
        
        try:
            db = DB_controller(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PWD,
                db=DB_NAME
            )
            data = db.show_data("user", "email", email)
            db.close()
            if data:
                if data[2] == email: # 帳號大小寫比對
                    hash_ = HASH
                    hash_pwd = pwd + hash_
                    hash_pwd = hashlib.sha256(hash_pwd.encode("utf-8")).hexdigest()
                    if hash_pwd == data[3]:
                        session["email"] = email # 確認email&密碼輸入正確才會存session
                        res = make_response(jsonify({"ok": True}))
                        return res
                    else:
                        return jsonify({"error": True, "message": "帳號或密碼錯誤"}), 400
                else: 
                    return jsonify({"error": True, "message": "帳號或密碼錯誤"}), 400
            else:
                return jsonify({"error": True, "message": "此email尚未被註冊"}), 400
        except Exception as e:
            return jsonify({"error": True, "message": str(e)}), 500


@user.route("/user", methods=["DELETE"])
def user_logout():
    '''user logout process'''
    if request.method == "DELETE":
        res = make_response(jsonify({"ok": True}))
        session.pop("email", None)
        return res