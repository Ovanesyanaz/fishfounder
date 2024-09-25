from flask import request
from flask import Flask
from PIL import Image
from io import BytesIO
import base64
import sqlite3
import random

def insert_in_db(number:int, amount:int):
    con = sqlite3.connect("fishdb.db")
    cur = con.cursor()
    if len(cur.execute(f"SELECT number, amount FROM fish_marking WHERE number = {number} AND amount = {-1}").fetchall()) == 1:
        cur.execute("UPDATE fish_marking SET amount = ? WHERE number = ?", (amount, number))
        con.commit()
    con.close()

def get_avalible_entries():
    con = sqlite3.connect("fishdb.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT number FROM fish_marking WHERE amount = {-1}").fetchall()
    con.commit()
    con.close()
    return res


def get_byte(number):
    with Image.open(f'photo/{number}.png') as img:
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("ascii")
        return img_str

app = Flask(__name__, static_folder='../server/build', static_url_path='/')
@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/server/get_first_img",methods=["POST"])
def get_first_img():
    res = random.choice(get_avalible_entries())[0]
    return {"img" : str(get_byte(res)), "amount" : str(res)}

@app.route("/server/get_img",methods=["POST"])
def sayHello():
    data = request.get_json()
    insert_in_db(int(data["amount"]), int(data["value"]))
    res = random.choice(get_avalible_entries())[0]
    return {"img" : str(get_byte(res)), "amount" : str(res)}

if __name__ == "__main__":
    app.run(debug=True)