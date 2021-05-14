from flask import Blueprint
from flask import request, jsonify, make_response, session
import json
import sys
import datetime
sys.path.append("C:\\Users\\user\\Desktop\\GitHub\\taipei-day-trip-website")
from model.db import DB_controller

with open("./data/config.json", mode="r", encoding="utf-8") as f:
    conf = json.load(f)


booking = Blueprint("booking", __name__)


def selectOneImage(images):
    images = images.replace("[","").replace("]","").replace("\'","")
    images = images.split(", ")
    return images[0]


@booking.route("/booking", methods=["GET"])
def uncheck_booking_list():
    pass
    # 搜尋attractionId，如果該id存在，表示按過開始預定行程
    if request.method == "GET":
        user_email = session.get("email")
        if not user_email:
            return jsonify({"error": True, "message": "請先登入會員"}), 403
        else:
            try:
                db = DB_controller(
                    host=conf["HOST"],
                    user=conf["USER"],
                    password=conf["PWD"],
                    db=conf["DB"]
                )
                user_data = db.show_data("user", "email", user_email)
                booking_data = db.show_data("booking", "userId", user_data[0]) #此使用人的booking資料
                if booking_data is None:
                    return jsonify({"data": None})
                else:
                    attraction_data = db.show_data("attractions", "id", booking_data[1])
                    db.close()

                    images = attraction_data[9]
                    image = selectOneImage(images)
                    date = booking_data[3]
                    date_format = date.strftime("%Y-%m-%d")
                    data = {
                        "data": {
                            "attraction": {
                                "id": attraction_data[0],
                                "name":attraction_data[1],
                                "address": attraction_data[4],
                                "image": image
                            },
                            "date": date_format,
                            "time": booking_data[4],
                            "price": booking_data[5]
                        }
                    }
                    res = make_response(jsonify(data))
                    return res
            except Exception as e:
                return jsonify({"error":True, "message":str(e)}), 500


@booking.route("/booking", methods=["POST"])
def build_booking():
    if request.method == "POST":
        post_data = request.get_json()
        print(post_data)
        attractionId = post_data["attractionId"]
        date = post_data["date"]
        time = post_data["time"]
        price = post_data["price"]
        user_email = session.get("email")
        if date == "":
            return jsonify({"error":True, "message":"請選擇日期"}), 400
        if time == "":
            return jsonify({"error":True, "message":"請選擇時間"}), 400
        if price == "":
            return jsonify({"error":True, "message":"請填入費用"}), 400
        
        if user_email is None:
            return jsonify({"error":True, "message":"請先登入會員"}), 403
        else:
            try:
                db = DB_controller(
                    host=conf["HOST"],
                    user=conf["USER"],
                    password=conf["PWD"],
                    db=conf["DB"]
                )
                user_data = db.show_data("user", "email", user_email)
                userId = user_data[0]
                db.insert_data(table_name="booking", settingrow='attractionId, userId, date, time, price', settingvalue=f'"{attractionId}","{userId}","{date}", "{time}", "{price}"')
                db.close()
                res = make_response(jsonify({"ok":True}))
                return res
            except Exception as e:
                return jsonify({"error":True, "message": str(e)}), 500



@booking.route("/booking", methods=["DELETE"])
def delete_booking():
    if request.method == "DELETE":
        user_email = session.get("email")
        if not user_email:
            return jsonify({"error":True, "message": "請先登入會員"}), 403
        
        try:
            db = DB_controller(
                host=conf["HOST"],
                user=conf["USER"],
                password=conf["PWD"],
                db=conf["DB"]
            )
            user_data = db.show_data("user", "email", user_email) # 查詢使用者
            booking_data = db.show_data("booking", "userId", user_data[0]) #此使用人的booking資料
            db.delete("booking", "bookingId", booking_data[0]) #刪除該資料
            res = make_response(jsonify({"ok":True}))
            return res
        except Exception as e:
            return jsonify({"error":True, "message":str(e)})
        