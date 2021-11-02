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


class XAPK:
    def __init__(self, version, is_variants, download_link="", variants_link=""):
        self.version = version
        self.download_link = download_link
        self.is_variants = is_variants
        self.variants_link = variants_link


class APK:
    def __init__(self, version, is_variants, download_link="", variants_link=""):
        self.version = version
        self.download_link = download_link
        self.is_variants = is_variants
        self.variants_link = variants_link


def write_log(data):
    with open("apk_log.txt", 'a', encoding='utf8') as f:
        f.write(data + '\n')


def get_version(text):
    find_result = re.search(r"V\d+(.\d+)+", text)
    if find_result:
        apk_version = text[find_result.span()[0]: find_result.span()[1]]
        return apk_version
    return ""


def get_download_match_link(apks, xapks):
    apks.sort(key=lambda a: a.version, reverse=True)
    xapks.sort(key=lambda xa: xa.version, reverse=True)
    for apk in apks:
        for xapk in xapks:
            if apk.version == xapk.version:
                if xapk.is_variants:
                    driver.get(xapk.variants_link)
                    xapk.download_link = driver.find_element_by_css_selector(".table-cell>a").get_attribute('href')
                elif apk.is_variants:
                    driver.get(apk.variants_link)
                    apk.download_link = driver.find_element_by_css_selector(".table-cell>a").get_attribute('href')
                return [apk.download_link, xapk.download_link]
    return []


def get_download_link(app_id):
    driver.get("https://apkpure.com/search?q=%s" % app_id)

    print("{+} start find download link %s" % app_id)
    try:
        apk_detail_url = driver.find_element_by_tag_name("p>a").get_attribute('href')
        apk_detail_url = apk_detail_url + "/versions"
        driver.get(apk_detail_url)
    except NoSuchElementException:
        print("{+} no result find in apk pure ")
        return []

    if "Page Deleted or Gone" in driver.title or "404" in driver.title:
        print("{+} fail to get download link, page maybe deleted or gone")
        return []

    warp_element = driver.find_element_by_css_selector(".ver-wrap")
    apks = []
    xapks = []

    for li_element in warp_element.find_elements_by_tag_name("li"):
        if "APK" in li_element.text and "XAPK" not in li_element.text:
            apk_version = get_version(li_element.text)
            try:
                if "Variants" in li_element.text:
                    variants_link = driver.find_element_by_css_selector(".table-cell>a").get_attribute('href')
                    apks.append(APK(apk_version, True, variants_link))
                else:
                    download_link = li_element.find_element_by_tag_name("a").get_attribute("href")
                    apks.append(APK(apk_version, False, download_link))
            except NoSuchElementException:
                print("{+}no link find")

        elif "XAPK" in li_element.text:
            xapk_version = get_version(li_element.text)
            try:
                if "Variants" in li_element.text:
                    variants_link = li_element.find_element_by_tag_name("a").get_attribute("href")
                    xapks.append(XAPK(xapk_version, True, variants_link=variants_link))
                else:
                    download_link = li_element.find_element_by_tag_name("a").get_attribute("href")
                    xapks.append(XAPK(xapk_version, False, download_link=download_link))
            except NoSuchElementException:
                print("{+}no link find")

    return get_download_match_link(apks, xapks)


def update_apk_download_info(apk_download_link, apk_id):
    cur = conn.cursor()
    cur.execute("UPDATE apk_info SET apk_download_link=? WHERE app_id=?", (apk_download_link, apk_id,))
    conn.commit()


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


def get_stored_dir():
    return "D:\\apk_pure\\matched_download"


def get_download_dir():
    return "D:\\apk_pure\\temp"


if __name__ == "__main__":
    current_task = "com.cabify.driver"
    cur = conn.cursor()
    cur.execute("SELECT app_id FROM apk_info WHERE apk_download_link IS NOT NULL order by ID")
    res = cur.fetchall()
    flag = False

    for app_id in res:
        if current_task in app_id:
            flag = True

        if flag:
            try:
                download_links = get_download_link(app_id[0])
                if len(download_links) == 2:
                    download_apk(download_links[0])
                    download_apk(download_links[1])
                    update_apk_download_info(download_links[0], apk_id=app_id[0])
                else:
                    print("no matched apk find")
            except TimeoutException:
                write_log(app_id[0] + "time out")
                time.sleep(10)
