from flask import Blueprint
from flask import request, jsonify, session
import tappay
import requests
from datetime import datetime as dt
import re
import os
from dotenv import load_dotenv
import sys
sys.path.append("C:\\Users\\user\\Desktop\\GitHub\\taipei-day-trip-website")
from model.db import DB_controller
from apis.booking import selectOneImage

order = Blueprint("order", __name__)

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PWD")
DB_NAME = os.getenv("DB_NAME")
PARTNER_KEY =  os.getenv("PARTNER_KEY")
MERCHANT_ID = os.getenv("MERCHANT_ID")

@order.route("/orders", methods=["POST"])
def build_order():
    if request.method == "POST":
        post_data = request.get_json()
        if not session.get("email"):
            return jsonify({"error":True, "message": "未登入會員系統"}), 403
        user_name = post_data["contact"]["name"]
        email = post_data["contact"]["email"]
        phone = post_data["contact"]["phone"]
        attractionId = post_data["order"]["trip"]["attraction"]["id"]
        date = post_data["order"]["date"]
        time = post_data["order"]["time"]
        price = post_data["order"]["price"]
        rex_email = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" # email格式
        rex_phone = r"\d\d\d\d\d\d\d\d\d\d"
        match_email = re.match(rex_email, email)
        match_phone = re.match(rex_phone, phone)
        if user_name == "":
            return jsonify({"error": True, "message": "不可為空值"}), 400

        if email == "":
            return jsonify({"error": True, "message": "不可為空值"}), 400
        
        if not match_email:
            return jsonify({"error": True, "message": "email格式錯誤"}), 400

        if phone == "":
            return jsonify({"error": True, "message": "不可為空值"}), 400

        if not match_phone:
            return jsonify({"error": True, "message": "手機號碼格式錯誤"}), 400

        try:
            # 創建訂單編號
            now = dt.today()
            order_number = now.strftime("%Y%m%d%H%M%S")
            order_status = -1 # 記錄訂單付款狀態 初始值設-1 0付款成功, 1付款失敗
            try: 
                #訂單資訊存到db
                db = DB_controller(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PWD,
                    db=DB_NAME
                )

                
                user_data = db.show_data("user", "email", post_data["contact"]["email"])
                userId = user_data[0]
                prev_order_data = db.show_data("orders", "userId", userId)
                

                #還沒有付款成功 => 不用存bank_transaction
                if not prev_order_data: # 沒有過訂單
                    db.insert_data(table_name='orders', settingrow='order_number, attractionId, userId, phone, date, time, price, status', settingvalue=f'"{order_number}","{attractionId}", "{userId}", "{phone}","{date}", "{time}", "{price}", "{order_status}"')
                
                elif prev_order_data[9] == 0: #成功付款過，直接新增新的資料
                    db.insert_data(table_name='orders', settingrow='order_number, attractionId, userId, phone, date, time, price, status', settingvalue=f'"{order_number}","{attractionId}", "{userId}", "{phone}","{date}", "{time}", "{price}", "{order_status}"')
                
                elif prev_order_data[9] == 1: #付款失敗過(紀錄留存)，可直接新增資料
                    db.insert_data(table_name='orders', settingrow='order_number, attractionId, userId, phone, date, time, price, status', settingvalue=f'"{order_number}","{attractionId}", "{userId}", "{phone}","{date}", "{time}", "{price}", "{order_status}"')
                
            except Exception as e:
                return jsonify({"error": True, "message": str(e)}), 500

            # 進行付款動作
            # tayppay.Client(is_sanbox, partner_key, merchant_id) 這裡都用官方提供測試用 => 沙盒 (要使用自己的key,id需要真的創建公司並且通過審核)
            client = tappay.Client(True, PARTNER_KEY, MERCHANT_ID)
            card_holder_data = tappay.Models.CardHolderData(post_data["contact"]["phone"], post_data["contact"]["name"], post_data["contact"]["email"])
            
            # client.pay_by_prime(prime, amount, details, card_holder_data)
            response_data_dict = client.pay_by_prime("test_3a2fb2b7e892b914a03c95dd4dd5dc7970c908df67a49527c0a648b2bc9", post_data["order"]["price"], post_data["order"]["trip"]["attraction"]["name"], card_holder_data)
            
            if response_data_dict["status"] == 0:
                order_status = 0
                try: 
                    #update bank_transaction & status
                    db.update(table_name='orders', set=f'bank_transaction="{response_data_dict["bank_transaction_id"]}", status={order_status}', search=f'order_number="{order_number}"')
                    order_data = db.show_data("orders", "order_number", order_number)
                    db.delete("booking", "userId", userId) # 付款成功 把booking的待預訂刪除
                    db.close()
                    data = {
                        "data": {
                            "number": order_data[1],
                            "payment": {
                                "status": order_data[9],
                                "message": "付款成功"
                            }
                        }
                    }
                    return jsonify(data)

                except Exception as e: #資料庫錯誤
                    return jsonify({"error": True, "message": str(e)}), 500

            else: # response_data_dict不是0，付款失敗
                order_status = 1
                db.update(table_name='orders', set=f'status={order_status}', search=f'order_number="{order_number}"')
                order_data = db.show_data("orders", "order_number", order_number)
                data = {
                    "error":True,
                    "number": order_number,
                    "payment": {
                        "status": order_data[9],
                        "message": "付款失敗"
                    }
                }
                return jsonify(data), 400

        except Exception as e:
            return jsonify({"error": True, "message": str(e)}), 400

        # 想用requests試試看抓資料 但一直JSON FORMAT錯誤??
        #     name = post_data["contact"]["name"]
        #     email = post_data["contact"]["email"]
        #     phone = post_data["contact"]["phone"]
        #     data = {
        #         "prime": "test_3a2fb2b7e892b914a03c95dd4dd5dc7970c908df67a49527c0a648b2bc9",
        #         "partner_key": "partner_6ID1DoDlaPrfHw6HBZsULfTYtDmWs0q0ZZGKMBpp4YICWBxgK97eK3RM",
        #         "merchant_id": "GlobalTesting_CTBC",
        #         "details": "新北投溫泉區",
        #         "amount": 2000,
        #         "cardholder": {
        #             "name": name,
        #             "email": email,
        #             "phone_number": phone
        #         },
        #         "remember": True
        #     }
        #     print(data)
        #     header = {"user-agent": "Mozilla/5.0", "Content-Type": "application/json", "x-api-key": "partner_6ID1DoDlaPrfHw6HBZsULfTYtDmWs0q0ZZGKMBpp4YICWBxgK97eK3RM"}
        #     req = requests.post("https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime", data=data, headers=header)
        #     req_dict = req.json()
        #     if req_dict["status"] != 0:
        #         return jsonify({"error":True, "message":req.json()}),400
        #     else:
        #         return jsonify(req.json())
        # except Exception as e:
        #     return jsonify({"error":True, "message": str(e)}),400


@order.route("/order/<ordernumber>", methods=["GET"])
def order_info(ordernumber):
    # 訂單資訊
    if request.method == "GET":
        if not session.get("email"):
            return jsonify({"error": True, "message": "尚未登入系統"}), 403
        try:
            db = DB_controller(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PWD,
                db=DB_NAME
            )
            order_data = db.show_data("orders", "order_number", ordernumber)
            if not order_data:
                return jsonify({"data": None})

            user_data = db.show_data("user", "email", session.get("email"))
            attraction_data = db.show_data("attractions", "id", order_data[3])
            db.close()
            images = attraction_data[9]
            image = selectOneImage(images)
            date_format = order_data[6].strftime("%Y-%m-%d")
            return_data = {
                "data": {
                    "number": ordernumber,
                    "bank_transaction": order_data[2],
                    "price": order_data[8],
                    "date": date_format,
                    "time": order_data[7],
                    "status": order_data[9],
                    "trip": {
                        "attraction": {
                            "id": attraction_data[0],
                            "name": attraction_data[1],
                            "address": attraction_data[4],
                            "image": image
                        }
                    },
                    "contact": {
                        "name": user_data[1],
                        "email": user_data[2],
                        "phone": order_data[4]
                    }
                }
            }
            return jsonify(return_data)
        except Exception as e:
            return jsonify({"error":True, "message": str(e)}), 500


# 自己新增 for historyorder page
@order.route("/orders/history", methods=["GET"])
def order_list():
    if request.method == "GET":
        if not session.get("email"):
            return jsonify({"error":True, "message":"尚未登入會員"}), 403
        
        clean_order_list = []
        try:
            db = DB_controller(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PWD,
                db=DB_NAME
            )
            user_data = db.show_data("user", "email", session.get("email"))
            order_list = db.fetch_all_data("orders", "userId", user_data[0])
            if not order_list:
                return jsonify({"data": None})
            
            
            for one in order_list:
                time_format = one[10]
                time_format = time_format.strftime("%Y-%m-%d %H:%M:%S")
                one_data = {
                    "number": one[1],
                    "create_time": time_format,
                    "order_price": one[8],
                    "status": one[9]
                }
                clean_order_list.append(one_data)
            return jsonify({"data": clean_order_list})

        except Exception as e:
            return jsonify({"error":True, "message": str(e)}), 500