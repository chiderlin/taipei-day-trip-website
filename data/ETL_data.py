import json
import sys
# sys.path.append("C:\\Users\\user\\Desktop\\GitHub\\taipei-day-trip-website")
sys.path.append("/home/ubuntu/root/taipei-day-trip-website")
# sys.path.append("/app") # 容器裡面
from model.db import DB_controller  # 原本會有紅紅的底線，但在該檔案中加上__init__.py 錯誤就消失了
import os
from dotenv import load_dotenv

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PWD =  os.getenv("DB_PWD")
DB_NAME = os.getenv("DB_NAME")

db = DB_controller(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PWD,
    db=DB_NAME)

with open("taipei-attractions.json", mode="r", encoding="utf-8") as f:
    data = json.load(f)

data = data["result"]["results"]


for j in range(len(data)):
    data[j]["file"] = data[j]["file"].replace("http", " http")
    data[j]["file"] = data[j]["file"].split(" ")
    data[j]["file"].pop(0)
    clean_img = []
    for i in range(len(data[j]["file"])):
        image_web = data[j]["file"][i]  # 在每個網址
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
    test = db.insert_data(table_name="attractions", settingrow='name, category, description, address, transport, mrt, latitude, longitude, images', settingvalue=f'"{name}","{category}","{description}","{address}","{transport}","{mrt}","{latitude}","{longitude},"{clean_img}"')
    # name, category, description, address, transport, mrt, latitude, longitude, clean_img
    print(test)


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
