from flask import Blueprint
from flask import request, jsonify, make_response, session
import json
import hashlib
import sys
# sys.path.append("C:\\Users\\user\\Desktop\\GitHub\\taipei-day-trip-website")
sys.path.append("/home/ubuntu/root/taipei-day-trip-website")
from model.db import DB_controller


with open("./data/config.json", mode="r", encoding="utf-8") as f: # 依照app.py的位置來寫路徑
    conf = json.load(f)

user = Blueprint("user", __name__)
# user.secret_key = "test@test.com" //要在app設secret_key才對


@user.route("/user", methods=["GET"])
def get_logined_user():
    if request.method == "GET":
        # 判斷有sessionId  => 取得db裡的資料 => 回傳使用者資料
        if session.get("email") is None:
            return jsonify({"data": None})
        else:
            try:
                db = DB_controller(
                    host=conf["HOST"],
                    user=conf["USER"],
                    password=conf["PWD"],
                    db=conf["DB"]
                )
                data = db.show_data("user", "email", session.get("email"))
                db.close()
                res = make_response(jsonify({"data": {
                    "id": data[0],
                    "name": data[1],
                    "email": data[2]
                }}))

                # res.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3000'
                return res
            except Exception as e:
                return jsonify({"error": True, "message": str(e)}), 500


@user.route("/user", methods=["POST"])
def user_register():
    if request.method == "POST":
        post_data = request.get_json()
        # 登入才要給一個sessionId
        name = post_data["name"]
        email = post_data["email"]
        pwd = post_data["password"]
        try:
            db = DB_controller(
                host=conf["HOST"],
                user=conf["USER"],
                password=conf["PWD"],
                db=conf["DB"]
            )
            email_check = db.show_data("user", "email", email)
            name_check = db.show_data("user", "name", name)
            if not email_check:
                if not name_check:
                    hash_ = conf["HASH"]
                    hash_pwd = pwd + hash_
                    hash_pwd = hashlib.sha256(
                        hash_pwd.encode("utf-8")).hexdigest()
                    db.insert_data("user", "name, email, password",
                                   f'"{name}","{email}","{hash_pwd}"')
                    db.close()
                    res = make_response(jsonify({"ok": True}))
                    # res.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3000'
                    return res
                else:
                    return jsonify({"error": True, "message": "此暱稱已被使用"}), 400
            else:
                return jsonify({"error": True, "message": "此email已註冊過"}), 400
        except Exception as e:
            return jsonify({"error": True, "message": str(e)}), 500


@user.route("/user", methods=["PATCH"])
def user_login():
    if request.method == "PATCH":
        login_data = request.get_json()
        # 這樣應該就會回傳sessionId到使用者Response Headers
        email = login_data["email"]
        pwd = login_data["password"]
        try:
            db = DB_controller(
                host=conf["HOST"],
                user=conf["USER"],
                password=conf["PWD"],
                db=conf["DB"]
            )
            data = db.show_data("user", "email", email)
            db.close()
            if data:
                if data[2] == email: # 帳號大小寫比對
                    hash_ = conf["HASH"]
                    hash_pwd = pwd + hash_
                    hash_pwd = hashlib.sha256(hash_pwd.encode("utf-8")).hexdigest()
                    if hash_pwd == data[3]:
                        session["email"] = email # 確認email&密碼輸入正確才會存session
                        res = make_response(jsonify({"ok": True}))
                        # res.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3000'
                        # res.headers['Access-Control-Allow-Methods'] = 'PATCH'
                        # res.headers['Access-Control-Allow-Credentials'] = True
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
    if request.method == "DELETE":
        res = make_response(jsonify({"ok": True}))
        # res.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3000'
        # res.headers['Access-Control-Allow-Methods'] = 'DELETE'
        # res.headers['Access-Control-Allow-Credentials'] = True
        session.pop("email", None)
        return res