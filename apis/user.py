from flask import Blueprint
from flask import Flask, request, jsonify
import json
import sys
sys.path.append("C:\\Users\\user\\Desktop\\GitHub\\taipei-day-trip-website")
from model.db import DB_controller


with open("./data/config.json", mode="r", encoding="utf-8") as f:
    conf = json.load(f)

user = Blueprint("user", __name__)

@user.route("/user", methods=["GET"])
def get_logined_user():
    if request.method == "GET":
        pass


@user.route("/user", methods=["POST"])
def user_register():
    if request.method == "POST":
        pass


@user.route("/user", methods=["PATCH"])
def user_login():
    pass


@user.route("/user", methods=["DELETE"])
def user_logout():
    pass

