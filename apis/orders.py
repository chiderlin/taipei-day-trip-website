from flask import Blueprint
from flask import request, jsonify, session
import tappay
import json
import sys
sys.path.append("C:\\Users\\user\\Desktop\\GitHub\\taipei-day-trip-website")
from model.db import DB_controller
from apis.booking import selectOneImage

order = Blueprint("order", __name__)

with open("./data/config.json", mode="r", encoding="utf-8") as f:
    conf = json.load(f)


@order.route("/orders", methods=["POST"])
def build_order():
    if request.method == "POST":
        post_data = request.get_json()
        if not session.get("email"):
            return jsonify({"error":True, "message": "未登入會員系統"}), 403
        # 進行付款動作
        try:
            # tayppay.Client(is_sanbox, partner_key, merchant_id) 這裡都用官方提供測試用
            client = tappay.Client(True, "partner_6ID1DoDlaPrfHw6HBZsULfTYtDmWs0q0ZZGKMBpp4YICWBxgK97eK3RM", "GlobalTesting_CTBC")
            card_holder_data = tappay.Models.CardHolderData(post_data["contact"]["phone"], post_data["contact"]["name"], post_data["contact"]["email"])
            # response_data_dict = client.pay_by_prime(post_data["prime"], post_data["order"]["price"], post_data["order"]["trip"]["attraction"]["name"], card_holder_data)
            # client.pay_by_prime(prime, amount, details, card_holder_data)
            response_data_dict = client.pay_by_prime("test_3a2fb2b7e892b914a03c95dd4dd5dc7970c908df67a49527c0a648b2bc9", post_data["order"]["price"], post_data["order"]["trip"]["attraction"]["name"], card_holder_data)
            print("response_data_dict", response_data_dict)
            if response_data_dict["status"] == 0:
                data = {
                    "data": {
                        "number": response_data_dict["bank_transaction_id"],
                        "payment": {
                            "status": response_data_dict["status"],
                            "message": "付款成功"
                        }
                    }
                }
                try: #付款成功把訂單資訊存到db
                    db = DB_controller(
                        host=conf["HOST"],
                        user=conf["USER"],
                        password=conf["PWD"],
                        db=conf["DB"]
                    )
                    attractionId = post_data["order"]["trip"]["attraction"]["id"]
                    user_data = db.show_data("user", "email", post_data["contact"]["email"])
                    userId = user_data[0]
                    phone = post_data["contact"]["phone"]
                    date = post_data["order"]["date"]
                    time = post_data["order"]["time"]
                    price = post_data["order"]["price"] 
                    status = response_data_dict["status"]
                    db.insert_data(table_name='orders', settingrow='order_number, attractionId, userId, phone, date, time, price, status', settingvalue=f'"{data["data"]["number"]}", "{attractionId}", "{userId}", "{phone}","{date}", "{time}", "{price}", "{status}"')
                    db.close()
                except Exception as e:
                    return jsonify({"error": True, "message": str(e)}), 500
                # 回傳成功資訊到前端
                return jsonify(data)
        except Exception as e:
            # 付款失敗
            return jsonify({"error": True, "message": str(e)}), 400



        #     data = {
        #         "prime": "test_3a2fb2b7e892b914a03c95dd4dd5dc7970c908df67a49527c0a648b2bc9",
        #         "partner_key": "partner_6ID1DoDlaPrfHw6HBZsULfTYtDmWs0q0ZZGKMBpp4YICWBxgK97eK3RM",
        #         "merchant_id": "GlobalTesting_CTBC",
        #         "datails": post_data["order"]["trip"]["attraction"]["name"],
        #         "amount": post_data["order"]["price"],
        #         "cardholder": post_data["contact"],
        #         "remember": False
        #     }
        #     print(data)
        #     header = {"user-agent": "Mozilla/5.0", "Content-Type": "application/json", "x-api-key": "partner_6ID1DoDlaPrfHw6HBZsULfTYtDmWs0q0ZZGKMBpp4YICWBxgK97eK3RM"}
        #     req = requests.post("https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime", data=data, headers=header)

        #     print(req.json())
        #     return req.json()
        # except Exception as e:
        #     return jsonify({"error":True, "message": str(e)}),400


@order.route("/order/<ordernumber>", methods=["GET"]) #現在用bank_transaction_id當number =>用str
def order_info(ordernumber):
    # 訂單資訊
    if request.method == "GET":
        if not session.get("email"):
            return jsonify({"error": True, "message": "尚未登入系統"}), 403
        try:
            db = DB_controller(
                host=conf["HOST"],
                user=conf["USER"],
                password=conf["PWD"],
                db=conf["DB"]
            )
            order_data = db.show_data("orders", "order_number", ordernumber)
            user_data = db.show_data("user", "email", session["email"])
            attraction_data = db.show_data("attractions", "id", order_data[2])
            db.close()
            images = attraction_data[9]
            image = selectOneImage(images)
            date_format = order_data[5].strftime("%Y-%m-%d")
            return_data = {
                "data": {
                    "number": ordernumber,
                    "price": order_data[7],
                    "date": date_format,
                    "time": order_data[6],
                    "status": order_data[8],
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