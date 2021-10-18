from selenium import webdriver
import os
import shutil
import re
import time
import sqlite3
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
prefs = {
    'download.default_directory': "D:\\apk_pure\\temp",
    'safebrowsing.enabled': 'false',
}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=options)


def get_download_dir():
    return "D:\\apk_pure\\temp"


def get_stored_dir():
    return "D:\\apk_pure\\download"


def download_apk(url):
    if url != "":
        driver.get(url)

        file_name = re.sub(r" \(\d+\.?\d* MB\)", "", driver.find_element_by_class_name("file").text)
        count = 0
        success = False
        while not check_finished(file_name):
            print("downloading %s" % file_name)
            time.sleep(3)
            count = count + 1

            if count == 30:
                print("{+} download time out")
                with open("log.txt", 'a') as f:
                    f.write(file_name + "\n")
                break
            success = True

        if success:
            print("{+} download %s success" % file_name)
            move_apk(file_name)
        else:
            print("{+} download %s fail" % file_name)
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
    # driver.get("https://apkpure.com")
    start_index = 1
    con = sqlite3.connect("../../apk_pure.db")
    cur = con.cursor()
    task_count_res = cur.execute("select count(*) from apk_info")
    task_count = task_count_res.fetchone()
    while start_index < task_count[0]:
        print("{+} download id = %s" % start_index)
        sql = '''SELECT * FROM apk_info WHERE id = ?'''
        cur.execute(sql, (start_index,))
        download_link_res = cur.fetchall()
        if len(download_link_res) == 0:
            print("{+} no download link find")
        else:
            try:
                download_apk(download_link_res[0][2])
            except NoSuchElementException:
                print("fail to download")
                with open("log.txt", "a") as f:
                    f.write(str(download_link_res[0]) + "\n")
            time.sleep(2)

        # 更新表长度
        task_count_res = cur.execute("select count(*) from apk_info")
        task_count = task_count_res.fetchone()
        start_index = start_index + 1
        print("----------------------------")
    driver.quit()
