import sqlite3
import zipfile
import os

conn = sqlite3.connect("../../apk_pure.db")


def get_stored_path():
    return "D:\\apk_pure\\result"


def get_result_dir():
    return "D:\\apk_pure\\t"


def query_app_id(app_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM apk_info WHERE app_id=?", (app_id,))
    res = cur.fetchall()
    if len(res) > 0:
        return True
    return False


def extract_base_apk(xapk_path, dest_path):
    if not zipfile.is_zipfile(xapk_path):
        return
    with zipfile.ZipFile(xapk_path, 'r') as xapk_file:
        for file in xapk_file.namelist():
            if file.endswith(".apk"):
                apk_name = file.replace(".apk", "")
                if query_app_id(apk_name):
                    if not os.path.exists(os.path.join(dest_path, file)):
                        print(file)
                        xapk_file.extract(file, path=dest_path)
                        print("---------------------")


def recheck_result_file():
    for file in os.listdir(get_result_dir()):
        file = os.path.join(get_result_dir(), file)
        if os.path.isdir(file):
            count = 0
            for _ in os.listdir(file):
                if _.endswith(".apk") or _.endswith(".xapk"):
                    count = count + 1
            if count != 3:
                print(os.path.join(file))


if __name__ == "__main__":
    for file in os.listdir(get_stored_path()):
        file = os.path.join(get_stored_path(), file)
        if os.path.isdir(file):
            for _ in os.listdir(file):
                _ = os.path.join(file, _)
                if _.endswith(".xapk"):
                    extract_base_apk(_, file)
