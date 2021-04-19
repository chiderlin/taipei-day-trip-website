import json
from db import DB_controller

with open("config.json", mode="r", encoding="utf-8") as config:
    conf = json.load(config)

db = DB_controller(
    host=conf["HOST"],
    user=conf["USER"],
    password=conf["PWD"],
    db=conf["DB"])

with open("taipei-attractions.json", mode="r", encoding="utf-8") as f:
    data = json.load(f)

data = data["result"]["results"]


for j in range(len(data)):
    data[j]["file"] = data[j]["file"].replace("http", " http")
    data[j]["file"] = data[j]["file"].split(" ")
    data[j]["file"].pop(0)
    clean_img = []
    for i in range(len(data[j]["file"])):
        image_web = data[j]["file"][i] # 在每個網址
        image_web = image_web.lower()
        if ".jpg" in image_web or ".png" in image_web:
            clean_img.append(image_web)
        
    name = data[j]["stitle"]
    category = data[j]["CAT2"]
    description = data[j]["xbody"]
    address = data[j]["address"]
    transport = data[j]["info"]
    mrt = data[j]["MRT"]
    latitude = data[j]["latitude"]
    longitude = data[j]["longitude"]    
    test = db.insert_data(name, category, description, address, transport, mrt, latitude, longitude, clean_img)
    print(test)



# TODO:
# API => JSON
# name=> stitle
# category => CAT2
# description => xbody
# address => address
# transport => info
# mrt => MRT
# latitude => latitude
# longitude => longitude
# image => file  