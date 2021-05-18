from flask import Blueprint
from flask import request, jsonify, make_response
import json
import sys
sys.path.append("C:\\Users\\user\\Desktop\\GitHub\\taipei-day-trip-website")
# sys.path.append("/home/ubuntu/root/taipei-day-trip-website")
from model.db import DB_controller

with open("./data/config.json", mode="r", encoding="utf-8") as f:
    conf = json.load(f)

attr = Blueprint("attr", __name__,
                       static_folder="static", template_folder="templates")


# db = DB_controller(
#     host=conf["HOST"],
#     user=conf["USER"],
#     password=conf["PWD"],
#     db=conf["DB"]
# )

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


# APIs
@attr.route("/attractions")
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
                        "latitude": str(ans[7]), #小數點 jsonify會有問題(Decimal error)，所以轉成str
                        "longitude": str(ans[8]),
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
                        res = make_response(jsonify(one_page))
                        res.headers['Access-Control-Allow-Origin'] = '*'
                        return res
                    else:
                        one_page = {
                            "nextPage": None,
                            "data": None,
                        }
                        res = make_response(jsonify(one_page))
                        res.headers['Access-Control-Allow-Origin'] = '*'
                        return res

                else: # 大於12筆資料
                    last_page, last_page_data = count_pages(count_data)
                    if page < last_page: # 但不是最後一頁
                        for i in range(start, end):
                            data.append(tmp_db[i])

                        one_page = {
                            "nextPage": page+1,
                            "data": data,
                        }
                        res = make_response(jsonify(one_page))
                        res.headers['Access-Control-Allow-Origin'] = '*'
                        return res

                    elif page == last_page: # 最後一頁
                        for i in range(start, start+last_page_data):
                            data.append(tmp_db[i])

                        one_page = {
                            "nextPage": None,
                            "data": data,
                        }
                        res = make_response(jsonify(one_page))
                        res.headers['Access-Control-Allow-Origin'] = '*'
                        return res
                    else:  # page > last_page
                        one_page = {
                            "nextPage": None,
                            "data": None,
                        }
                        res = make_response(jsonify(one_page))
                        res.headers['Access-Control-Allow-Origin'] = '*'
                        return res

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
                    "latitude": str(res[7]),
                    "longitude": str(res[8]),
                    "images": res[9],
                }
                data.append(data_dict)

            if page < last_page:
                one_page = {
                    "nextPage": page+1,
                    "data": data,
                }
                res = make_response(jsonify(one_page))
                res.headers['Access-Control-Allow-Origin'] = '*'
                return res

            elif page == last_page:  # 最後一頁
                one_page = {
                    "nextPage": None,
                    "data": data,
                }
                res = make_response(jsonify(one_page))
                res.headers['Access-Control-Allow-Origin'] = '*'
                return res

            elif page > last_page:  # 大於現有頁數
                one_page = {
                    "nextPage": None,
                    "data": None,
                }
                res = make_response(jsonify(one_page))
                res.headers['Access-Control-Allow-Origin'] = '*'
                return res

            else:
                return jsonify({"error": True, "message": "Something wrong"}), 500

@attr.route("/attraction/<int:attractionId>")
def view(attractionId):
    '''restful-api, select single data using id.'''
    
    if request.method == "GET":
        try:
            db = DB_controller(
                host=conf["HOST"],
                user=conf["USER"],
                password=conf["PWD"],
                db=conf["DB"]
            )
            result = db.show_data("attractions", "id", attractionId)
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
                    "latitude": str(result[7]),
                    "longitude": str(result[8]),
                    "images": result[9],
                }
            }
            res = make_response(jsonify(data))
            res.headers['Access-Control-Allow-Origin'] = '*'
            
            return res
        except Exception as e:
            return jsonify({"error": True, "message": str(e)}), 500


