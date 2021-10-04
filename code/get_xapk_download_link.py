import re
import time
from queue import Queue

from sqlite3 import IntegrityError
import sqlite3
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
prefs = {
    'download.default_directory': "E:\\temp",
    'safebrowsing.enabled': 'false'
}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=options)

# 用于记录已经访问过的app
requested_app_id = set()
# 用于记录需要下载的任务
download_task = Queue()

con = sqlite3.connect("../../apk_pure.db")


def get_download_link(app_id):
    if app_id in requested_app_id:
        print("{+} %s has request before" % app_id)
        return
    else:
        requested_app_id.add(app_id)

    driver.get("https://apkpure.com/search?q=%s" % app_id)
    download_link = ""
    success = False

    try:
        apk_detail_url = driver.find_element_by_tag_name("p>a").get_attribute('href')
        # 将similar apk加入任务队列中
        add_similar_app_id_to_mission(apk_detail_url)
        driver.get(apk_detail_url + "/versions")
    except NoSuchElementException:
        print("{+} no result find in apk pure ")
        return ""
    if "Page Deleted or Gone" in driver.title:
        print("{+} fail to get download link, page maybe deleted or gone")
        return ""

    for apk_details in driver.find_elements_by_class_name("ver-item"):
        if 'XAPK' in apk_details.text and 'OBB' not in apk_details.text:
            try:
                variants = apk_details.find_element_by_class_name("ver-item-v")
                if 'Variants' in variants.text:
                    driver.get(apk_detail_url + "/variant/" +
                               apk_details.find_element_by_class_name("ver-item-n").text[1:] + "-XAPK")
            except NoSuchElementException:
                download_link = driver.find_element_by_css_selector(".ver-wrap>li>a").get_attribute("href")
                success = True
                break
            try:
                download_link = driver.find_element_by_css_selector(".table-cell>a").get_attribute("href")
                success = True
                break
            except NoSuchElementException:
                download_link = ""
                success = False

    if success:
        print("{+} find download link %s" % download_link)
        add_app_info_to_db(app_id, download_link)
    else:
        print("{+} no apks find, fail to find download link")

    return download_link


def add_similar_app_id_to_mission(apk_detail_url):
    driver.get(apk_detail_url)
    top_list = driver.find_element_by_css_selector(".top-list")
    for _ in top_list.find_elements_by_css_selector("a[target=\"_blank\"]"):
        similar_app_id = _.get_attribute('href')
        if re.match(r"https://apkpure.com/[\s\S]*/[\s\S]*", similar_app_id):
            similar_app_id = similar_app_id.split('/')[-1]
            if similar_app_id not in requested_app_id:
                download_task.put(similar_app_id)


def add_app_info_to_db(app_id, download_link):
    cur = con.cursor()
    sql = '''INSERT INTO apk_info(app_id, download_link) VALUES (?, ?)'''
    data = (app_id, download_link)

    try:
        cur.execute(sql, data)
    except IntegrityError:
        print("{+} app_id duplicate")
    con.commit()


def get_init_task_from_predefined():
    with open("../base-app.txt", "r") as f:
        for line in f.readlines():
            if line == "\n" or line == "":
                continue
            app_id = line.replace("\n", "")
            download_task.put(app_id)


def get_init_task_from_backup():
    with open("../backup.txt", "r") as f:
        for line in f.readlines():
            if line == "\n" or line == "":
                continue
            app_id = line.replace("\n", "")
            download_task.put(app_id)


if __name__ == "__main__":
    get_init_task_from_backup()
    count = 0
    while download_task.qsize() != 0:
        time.sleep(1)
        app_id = download_task.get()
        print("{+} start find download link %s" % app_id)
        get_download_link(app_id)
        print(str(download_task.qsize()) + " tasks remaining")
        count = count + 1
        if count == 10:
            print("{+} back up download task")
            with open("../backup.txt", "w") as f:
                temp = ""
                task_size = download_task.qsize()
                print(task_size)
                while task_size != 0:
                    temp = download_task.get()
                    f.write(temp + "\n")
                    download_task.put(temp)
                    task_size = task_size - 1
            count = 0
        print("--------------------------")
