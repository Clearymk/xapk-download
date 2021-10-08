import sqlite3

con = sqlite3.connect("../../apk_pure.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS apk_info ("
            "ID INTEGER PRIMARY KEY AUTOINCREMENT"
            ", app_id TEXT UNIQUE"
            ", download_link TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS visit_app_info ("
            "ID INTEGER PRIMARY KEY AUTOINCREMENT"
            ", app_id TEXT UNIQUE)")