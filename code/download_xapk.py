from selenium import webdriver
import os
import shutil
import re
import time
import sqlite3

options = webdriver.ChromeOptions()
prefs = {
    'download.default_directory': "F:\\temp",
    'safebrowsing.enabled': 'false',
}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=options)


def get_download_dir():
    return "F:\\temp"


def get_stored_dir():
    return "F:\\download"


def download_apk(url):
    if url != "":
        driver.get(url)
        file_name = re.sub(r" \(\d+\.?\d* MB\)", "", driver.find_element_by_class_name("file").text)

        while not check_finished(file_name):
            print("downloading %s" % file_name)
            time.sleep(3)
        print("{+} download %s success" % file_name)
        move_apk(file_name)
    else:
        print("{+} no valid url provided")


def check_finished(apk_name):
    download_dir = get_download_dir()
    apk_file_path = os.path.join(download_dir, apk_name)
    if os.path.isfile(apk_file_path):
        return True
    return False


def move_apk(apk_name):
    download_dir = get_download_dir()
    download_path = os.path.join(download_dir, apk_name)
    stored_dir = get_stored_dir()

    if os.path.isdir(stored_dir) and os.path.isfile(download_path):
        if os.path.exists(os.path.join(stored_dir, apk_name)):
            os.remove(os.path.join(stored_dir, apk_name))
        shutil.move(download_path, stored_dir)


if __name__ == "__main__":
    start_index = 431
    con = sqlite3.connect("../../apk_pure.db")
    cur = con.cursor()
    task_count_res = cur.execute("select count(*) from apk_info")
    task_count = task_count_res.fetchone()
    while start_index < 431 + task_count[0]:
        sql = '''SELECT * FROM apk_info WHERE id = ?'''
        cur.execute(sql, (start_index,))
        download_link_res = cur.fetchall()
        if len(download_link_res) == 0:
            print("{+} no download link find")
        else:
            download_apk(download_link_res[0][2])
            time.sleep(2)

        # 更新表长度
        task_count_res = cur.execute("select count(*) from apk_info")
        task_count = task_count_res.fetchone()
        print(task_count[0])
        start_index = start_index + 1
        print("----------------------------")
