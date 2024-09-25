import sqlite3
import random
con = sqlite3.connect("fishdb.db")

cur = con.cursor()
i = 6
j = 11
cur.execute("CREATE TABLE fish_marking(number, amount)")

def insert_in_db(number:int, amount:int):
    con = sqlite3.connect("fishdb.db")
    cur = con.cursor()
    if len(cur.execute(f"SELECT number, amount FROM fish_marking WHERE number = {number} AND amount = {-1}").fetchall()) == 1:
        cur.execute("UPDATE fish_marking SET amount = ? WHERE number = ?", (amount, number))
        con.commit()
    con.close()

def create_template_db(amount: int):
    con = sqlite3.connect("fishdb.db")
    cur = con.cursor()
    length_db = len(cur.execute("SELECT * from fish_marking").fetchall())
    if length_db >= amount:
        return
    for i in range(length_db, amount):
        cur.execute(f"INSERT INTO fish_marking (number, amount) VALUES (?,?)", (i, -1))
        # cursor.execute('INSERT INTO users (name, surname, age, faculty) VALUES (?, ?, ?, ?)', (name, surname, age, faculty))

        con.commit()
    con.close()

def get_avalible_entries():
    con = sqlite3.connect("fishdb.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT number FROM fish_marking WHERE amount = {-1}").fetchall()
    con.commit()
    con.close()
    return res
def get_not_avalible_entries():
    con = sqlite3.connect("fishdb.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT number,amount FROM fish_marking WHERE amount != {-1}").fetchall()
    con.commit()
    con.close()
    return res
con.commit()
con.close()

create_template_db(150)
