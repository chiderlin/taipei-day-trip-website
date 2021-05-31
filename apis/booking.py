from flask import Blueprint
from flask import request, jsonify, make_response, session
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


booking = Blueprint("booking", __name__)


def selectOneImage(images):
    '''etl images data, pick first picture'''
    images = images.replace("[","").replace("]","").replace("\'","")
    images = images.split(", ")
    return images[0]



@booking.route("/booking", methods=["GET"])
def uncheck_booking():
    '''user scheduled trip record'''

    # 搜尋userId，如果該id存在，表示按過開始預定行程
    if request.method == "GET":
        user_email = session.get("email")
        if not user_email:
            return jsonify({"error": True, "message": "請先登入會員"}), 403
        else:
            try:
                db = DB_controller(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PWD,
                    db=DB_NAME
                )
                user_data = db.show_data("user", "email", user_email)
                booking_data = db.show_data("booking", "userId", user_data[0]) #此使用人的booking資料
                if booking_data is None:
                    return jsonify({"data": None})
                else:
                    attraction_data = db.show_data("attractions", "id", booking_data[1])
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
                    db.close()
                    return res
            except Exception as e:
                return jsonify({"error":True, "message":str(e)}), 500


@booking.route("/booking", methods=["POST"])
def build_booking():
    '''build a trip if interested'''

    if request.method == "POST":
        post_data = request.get_json()
        attractionId = post_data["attractionId"]
        date = post_data["date"]
        time = post_data["time"]
        price = post_data["price"]
        user_email = session.get("email")
        rex_date = r"(^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$)" #yyyy-mm-dd
        match_date = re.match(rex_date, date)

        if date == "":
            return jsonify({"error":True, "message":"請選擇日期"}), 400

        if not match_date:
            return jsonify({"error":True, "message":"日期格式不正確"}), 400

        if time == "":
            return jsonify({"error":True, "message":"請選擇時間"}), 400
        elif time != "afternoon" or time != "morning":
            return jsonify({"error":True, "message":"時間格式不正確"}), 400
        
        if price == "":
            return jsonify({"error":True, "message":"請填入費用"}), 400
        
        if not user_email:
            return jsonify({"error":True, "message":"請先登入會員"}), 403
        else:
            try:
                db = DB_controller(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PWD,
                    db=DB_NAME
                )
                user_data = db.show_data("user", "email", user_email)
                userId = user_data[0]
                
                booking_data = db.show_data("booking", "userId", userId)
                # 先判斷booking table裡面是否已經有資料了，
                if booking_data: # 如果有 => 刪除原本的 insert此筆
                    delete = db.delete("booking", "userId", userId)
                    insert = db.insert_data(table_name="booking", settingrow='attractionId, userId, date, time, price', settingvalue=f'"{attractionId}","{userId}","{date}", "{time}", "{price}"')
                    db.close()
                    res = make_response(jsonify({"ok":True}))
                    return res
                else: 
                    # 沒找到的話直接insert
                    insert = db.insert_data(table_name="booking", settingrow='attractionId, userId, date, time, price', settingvalue=f'"{attractionId}","{userId}","{date}", "{time}", "{price}"')
                    db.close()
                    res = make_response(jsonify({"ok":True}))
                    return res
            except Exception as e:
                return jsonify({"error":True, "message": str(e)}), 500



@booking.route("/booking", methods=["DELETE"])
def delete_booking():
    '''want to delete a scheduled'''

    if request.method == "DELETE":
        user_email = session.get("email")
        if not user_email:
            return jsonify({"error":True, "message": "請先登入會員"}), 403
        
        try:
            db = DB_controller(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PWD,
                db=DB_NAME
            )
            user_data = db.show_data("user", "email", user_email) # 查詢使用者
            booking_data = db.show_data("booking", "userId", user_data[0]) #此使用人的booking資料
            db.delete("booking", "bookingId", booking_data[0]) #刪除該資料
            res = make_response(jsonify({"ok":True}))
            return res
        except Exception as e:
            return jsonify({"error":True, "message":str(e)}), 500
        