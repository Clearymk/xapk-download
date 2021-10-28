import sqlite3
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
import shutil
import re
import time

options = webdriver.ChromeOptions()
prefs = {
    'download.default_directory': "D:\\apk_pure\\temp",
    'safebrowsing.enabled': 'false',
}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=options)
conn = sqlite3.connect("../../apk_pure.db")


# driver = 1


def get_stored_dir():
    return "D:\\apk_pure\\download"


def get_download_dir():
    return "D:\\apk_pure\\temp"


def get_download_link(app_id):
    driver.get("https://apkpure.com/search?q=%s" % app_id)
    download_link = ""
    success = False
    print("{+} start find download link %s" % app_id)
    try:
        apk_detail_url = driver.find_element_by_tag_name("p>a").get_attribute('href')
        apk_name = str(apk_detail_url).replace('https://apkpure.com/', '').split("/")[0]
        dir_path = find_dir(apk_name.replace('-', ' '))
        if dir_path != "":
            download_vision = check_vision(dir_path)
            if len(download_vision) == 2:
                driver.get(apk_detail_url + "/versions")
            else:
                print("{+} do not need re-download")
                return ""
        else:
            print("{+} no apk dir find")
            return ""
    except NoSuchElementException:
        print("{+} no result find in apk pure ")
        return ""
    print("{+} target download apk vision %s" % download_vision[1])
    print("{+} target download xapk vision %s" % download_vision[0])

    if "Page Deleted or Gone" in driver.title or "404" in driver.title:
        print("{+} fail to get download link, page maybe deleted or gone")
        return ""

    warp_element = driver.find_element_by_css_selector(".ver-wrap")
    for li_element in warp_element.find_elements_by_tag_name("li"):
        if "APK" in li_element.text and "XAPK" not in li_element.text and download_vision[1].upper() in li_element.text:
            try:
                if "Variants" in li_element.text:
                    driver.get(li_element.find_element_by_tag_name("a").get_attribute("href"))
                    download_link = driver.find_element_by_css_selector(".table-cell>a").get_attribute('href')
                    success = True
                    break
                else:
                    download_link = li_element.find_element_by_tag_name("a").get_attribute("href")
                    success = True
                    break
            except NoSuchElementException:
                download_link = ""
                success = False
        elif "XAPK" in li_element.text and download_vision[0].upper() in li_element.text:
            try:
                if "Variants" in li_element.text:
                    driver.get(li_element.find_element_by_tag_name("a").get_attribute("href"))
                    download_link = driver.find_element_by_css_selector(".table-cell>a").get_attribute('href')
                    success = True
                    break
                else:
                    download_link = li_element.find_element_by_tag_name("a").get_attribute("href")
                    success = True
                    break
            except NoSuchElementException:
                download_link = ""
                success = False

    if success:
        print("{+} find download link %s" % download_link)
        update_apk_download_info(download_link, app_id)
        download_apk(download_link)
    else:
        write_log(app_id + " no apk find")
        print("{+} no apk find, fail to find download link")

    return download_link


def find_dir(name):
    file_path = os.path.join(get_stored_dir(), name)
    if os.path.exists(file_path):
        return file_path
    return ""


def check_vision(path):
    apk_vision = ""
    xapk_vision = ""
    for file in os.listdir(path):
        if file.endswith(".apk"):
            apk_vision = file.split("_")[1]
        elif file.endswith(".xapk"):
            xapk_vision = file.split("_")[1]
    if apk_vision != xapk_vision:
        return apk_vision, xapk_vision
    return ""


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


def download_apk(url):
    if url != "":
        driver.get(url)

        file_name = re.sub(r" \(\d+\.?\d* MB\)", "", driver.find_element_by_class_name("file").text)
        print("{+} start downloading %s" % file_name)
        count = 0
        success = False
        while not check_finished(file_name):
            print("downloading %s" % file_name)
            time.sleep(3)
            count = count + 1

            if count == 30:
                print("{+} download time out")
                write_log(file_name + "download time out")
                success = False
                break
            success = True

        if success:
            print("{+} download %s success" % file_name)
            move_apk(file_name)
        else:
            print("{+} download %s fail" % file_name)
    else:
        print("{+} no valid url provided")


def update_apk_download_info(apk_download_link, apk_id):
    cur = conn.cursor()
    cur.execute("UPDATE apk_info SET apk_download_link=? WHERE app_id=?", (apk_download_link, apk_id,))
    conn.commit()


def write_log(data):
    with open("apk_log.txt", 'a', encoding='utf8') as f:
        f.write(data + '\n')


if __name__ == "__main__":
    current_task = "com.cephalon.navis"
    cur = conn.cursor()
    cur.execute("SELECT app_id, apk_download_link FROM apk_info WHERE apk_download_link IS NOT NULL order by ID")
    res = cur.fetchall()
    flag = False

    for app_id in res:
        if current_task in app_id:
            flag = True

        if flag:
            try:
                get_download_link(app_id[0])
            except TimeoutException:
                write_log(app_id[0] + "time out")
                time.sleep(10)
