import sqlite3

con = sqlite3.connect("apk_pure.db")
cur = con.cursor()
res = cur.execute("SELECT * FROM apk_info WHERE app_id=2")
print(len(res.fetchall()))
