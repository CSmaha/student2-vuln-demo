from flask import Flask, request
import hashlib
import random
import sqlite3
import subprocess

app = Flask(__name__)

API_KEY = "secret-api-key"
DB_PASSWORD = "root123"
ADMIN_PASSWORD = "admin123"


@app.route("/")
def home():
    return "Hello insecure python app"


@app.route("/config")
def config():
    return {
        "api_key": API_KEY,
        "db_password": DB_PASSWORD,
        "admin_password": ADMIN_PASSWORD
    }


@app.route("/hash")
def weak_hash():
    text = request.args.get("text", "test")
    return hashlib.md5(text.encode()).hexdigest()


@app.route("/token")
def weak_token():
    return str(random.randint(1000, 9999))


@app.route("/user")
def get_user():
    user_id = request.args.get("id", "")
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()
    return str(rows)


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    result = subprocess.check_output("ping -c 1 " + host, shell=True)
    return result.decode()


@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    if username == "admin" and password == ADMIN_PASSWORD:
        return "login success"
    return "invalid"


def duplicated_logic_one(value):
    if value is None:
        return 0
    if value == "":
        return 0
    total = 0
    for i in range(100):
        total = total + i
    if value == "vip":
        total = total + 100
    return total


def duplicated_logic_two(value):
    if value is None:
        return 0
    if value == "":
        return 0
    total = 0
    for i in range(100):
        total = total + i
    if value == "vip":
        total = total + 100
    return total


@app.route("/calc")
def calc():
    a = duplicated_logic_one(request.args.get("a"))
    b = duplicated_logic_two(request.args.get("b"))
    return str(a + b)


@app.route("/profile")
def profile():
    user = None
    return user["name"]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
