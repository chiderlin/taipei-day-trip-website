from flask import Flask, jsonify, request, render_template
from flask_restful import Resource
import json
from data.db import DB_controller
with open ("./data/config.json", mode="r", encoding="utf-8") as f:
	conf = json.load(f)


db = DB_controller(
	host=conf["HOST"],
	user=conf["USER"],
	password=conf["PWD"],
	db=conf["DB"]
	)

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

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


# Api 
@app.route("/api/attractions")
def attractions():
	'''
	Parameter:page (int)
	each page have 12 data,
	input the page you wanna search, and get the data.
	'''

	if request.method == "GET":
		page = request.args.get("page")
		if not page:
			return jsonify({"error":True, "message":"請輸入參數page"}), 500
		
		try:
			page = int(page)
		except ValueError: 
			try: # 如果是小數點，轉成整數部分來顯示
				page = float(page)
				page = int(page)
			except ValueError: # 不是的話直接顯示error
				return jsonify({"error":True, "message":"請輸入數字"}), 500

		count_data = db.count_data("attractions")
		count_data = int(count_data)
		data = []
		if count_data % 12 != 0:
			last_page = count_data // 12 + 1 # 有餘數就表示有下頁
			last_page_data = count_data % 12 # 最後一頁剩七筆
		else:
			last_page = count_data / 12

		end = 12 * page
		start = end - 11
		if page < 1: # page填負數的話
			return jsonify({"error": True, "message": "page number must >1"}), 500
		
		
		if page < last_page:
			for i in range(start, end+1): # 塞入12筆資料
				result = db.show_data("attractions", "id", i)
				data_dict = {
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
				data.append(data_dict)
				
			one_page = {
				"nextPage": page+1,
				"data": data,
			}
			return jsonify(one_page)

		elif page == last_page: # 最後一頁
			for i in range(start, start+last_page_data):
				result = db.show_data("attractions", "id", i)
				data_dict = {
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
				data.append(data_dict)
				
			one_page = {
				"nextPage": page+1,
				"data": data,
			}
			return jsonify(one_page)

		elif page > last_page: #大於現有頁數
			return jsonify({
				"error":True,
				"message":f"Total Page only up to {last_page}",
				}), 500
		else:
			return jsonify({"error":True, "message":"Something wrong"}), 500


@app.route("/api/attraction/<int:atrractionId>")
def view(atrractionId):
	if request.method == "GET":
		count_data = db.count_data("attractions")
		result = db.show_data("attractions","id", atrractionId)
		if not result:
			return jsonify({"error":True, "message": f"Data only up to {count_data}"}), 400
		
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



if __name__ == "__main__":
	app.run(port=3000, host="localhost", debug=True)