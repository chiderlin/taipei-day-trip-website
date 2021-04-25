from flask import Flask, jsonify, request, render_template
from flask_restful import Resource
import json
from data.db import DB_controller
with open("./data/config.json", mode="r", encoding="utf-8") as f:
    conf = json.load(f)

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True


# db = DB_controller(
#     host=conf["HOST"],
#     user=conf["USER"],
#     password=conf["PWD"],
#     db=conf["DB"]
# )


# Pages
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


# function
def count_pages(count_data):
    ''' count pages '''
    count_data = int(count_data)
    if count_data % 12 != 0:  # 12筆一頁
        last_page = count_data // 12 + 1-1  # 餘數+1 page從0開始-1 # 有餘數就表示有下頁
        last_page_data = count_data % 12  # 最後一頁剩七筆
    else:
        last_page = count_data / 12 - 1  # page從0開始-1

    return last_page, last_page_data


# Api
@app.route("/api/attractions")
def attractions():
    '''
    Parameter:page (int), keyword(string)
    each page have 12 data,
    input the page and keyword you wanna search, and get the data.
    '''

    if request.method == "GET":
        page = request.args.get("page")
        keyword = request.args.get("keyword")
        if not page:
            return jsonify({"error": True, "message": "請輸入參數page"}), 500

        # 有 page ， page輸入判斷
        try:
            page = int(page)
        except ValueError:
            try:  # 如果是小數點，轉成整數部分來顯示
                page = float(page)
                page = int(page)
            except ValueError:  # 不是的話直接顯示error
                return jsonify({"error": True, "message": "請輸入數字"}), 500

        if page < 0:  # page填負數的話
            return jsonify({"error": True, "message": "page number must >0"}), 500

        data = []
        tmp_db = []

        # page 規律
        start = 12 * page
        end = start + 12
        if keyword:
            try:
                db = DB_controller(
                    host=conf["HOST"],
                    user=conf["USER"],
                    password=conf["PWD"],
                    db=conf["DB"]
                    )

                result = db.relative_data("attractions", "name", keyword)
                db.close()
                for ans in result:
                    data_dict = {
                        "id": ans[0],
                        "name": ans[1],
                        "category": ans[2],
                        "description": ans[3],
                        "address": ans[4],
                        "transport": ans[5],
                        "mrt": ans[6],
                        "latitude": ans[7],
                        "longitude": ans[8],
                        "images": ans[9],
                    }
                    tmp_db.append(data_dict)
                count_data = len(tmp_db)
                if count_data <= 12: 
                    if page == 0: # 必須在第0頁顯示
                        one_page = {
                            "nextPage": None,
                            "data": tmp_db,
                        }
                        return jsonify(one_page)
                    else:
                        one_page = {
                            "nextPage": None,
                            "data": None,
                        }
                        return jsonify(one_page)

                else: # 大於12筆資料
                    last_page, last_page_data = count_pages(count_data)
                    if page < last_page: # 但不是最後一頁
                        for i in range(start, end):
                            data.append(tmp_db[i])

                        one_page = {
                            "nextPage": page+1,
                            "data": data,
                        }
                        return jsonify(one_page)

                    elif page == last_page: # 最後一頁
                        for i in range(start, start+last_page_data):
                            data.append(tmp_db[i])

                        one_page = {
                            "nextPage": None,
                            "data": data,
                        }
                        return jsonify(one_page)

                    else:  # page > last_page
                        one_page = {
                            "nextPage": None,
                            "data": None,
                        }
                        return jsonify(one_page)

            except Exception as e:
                return jsonify({"error": True, "message": str(e)}), 500

        else:  # 沒有keyword
            # 查詢資料庫目前有幾筆資料
            try:
                db = DB_controller(
                    host=conf["HOST"],
                    user=conf["USER"],
                    password=conf["PWD"],
                    db=conf["DB"]
                )
            except Exception as e:
                return jsonify({"error": True, "message": str(e)}), 500

            count_data = db.count_data("attractions")
            last_page, last_page_data = count_pages(count_data)
            result = db.limit_data("attractions", start, 12)  # 改limit分頁 LIMITE優點是假如最後一頁不足12筆資料也不會報錯，就顯示剩下的全部
            db.close() 
            for res in result:  # 塞入12筆資料
                data_dict = {
                    "id": res[0],
                    "name": res[1],
                    "category": res[2],
                    "description": res[3],
                    "address": res[4],
                    "transport": res[5],
                    "mrt": res[6],
                    "latitude": res[7],
                    "longitude": res[8],
                    "images": res[9],
                }
                data.append(data_dict)

            if page < last_page:
                one_page = {
                    "nextPage": page+1,
                    "data": data,
                }
                return jsonify(one_page)

            elif page == last_page:  # 最後一頁
                one_page = {
                    "nextPage": None,
                    "data": data,
                }
                return jsonify(one_page)

            elif page > last_page:  # 大於現有頁數
                one_page = {
                    "nextPage": None,
                    "data": None,
                }
                return jsonify(one_page)

            else:
                return jsonify({"error": True, "message": "Something wrong"}), 500


@app.route("/api/attraction/<int:atrractionId>")
def view(atrractionId):
    '''restful-api, select single data using id.'''
    
    if request.method == "GET":
        try:
            db = DB_controller(
                host=conf["HOST"],
                user=conf["USER"],
                password=conf["PWD"],
                db=conf["DB"]
            )
            result = db.show_data("attractions", "id", atrractionId)
            db.close()
            if not result:
                return jsonify({"data": None})

            data = {
                "data": {
                    "id": result[0],
                    "name": result[1],
                    "category": result[2],
                    "description": result[3],
                    "address": result[4],
                    "transport": result[5],
                    "mrt": result[6],
                    "latitude": result[7],
                    "longitude": result[8],
                    "images": result[9],
                }
            }
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": True, "message": str(e)}), 500




if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0", debug=True)
