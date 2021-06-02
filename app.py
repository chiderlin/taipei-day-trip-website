from flask import Flask, render_template
from apis.attractions import attr
from apis.user import user
from apis.booking import booking
from apis.orders import order


app = Flask(__name__, static_url_path="/", static_folder="static")
app.register_blueprint(attr, url_prefix="/api")
app.register_blueprint(user, url_prefix="/api")
app.register_blueprint(booking, url_prefix="/api")
app.register_blueprint(order, url_prefix="/api")

app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = "test@test.com"

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

@app.route("/historyorder")
def historyorder():
    return render_template("historyorder.html")


if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0", debug=True)
