from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    return render_template("home.html")


@app.route("/expense")
def addexpense():
    return render_template("addexpense.html")


@app.route("/manageexpense")
def manageexpense():
    return render_template("manageexpense.html")
