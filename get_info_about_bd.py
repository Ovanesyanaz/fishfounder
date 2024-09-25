import sqlite3
def get_avalible_entries():
    con = sqlite3.connect("fishdb.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT number,amount FROM fish_marking WHERE amount != {-1}").fetchall()
    con.commit()
    con.close()
    return res
print(get_avalible_entries())