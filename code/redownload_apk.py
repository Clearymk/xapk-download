from selenium import webdriver
import os
import shutil
import re
import time
import sqlite3

options = webdriver.ChromeOptions()
prefs = {
    'download.default_directory': "E:\\temp",
    'safebrowsing.enabled': 'false',
}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=options)


def get_stored_dir():
    return "E:\\download"


if __name__ == "__main__":
    for file in os.listdir(get_stored_dir()):
        if file.endswith(".apk"):
            app_name = file.split('.apk')[0].split("_")[0]
            driver.get("https://apkpure.com/search?q=%s" % app_name)
            apk_detail_url = driver.find_element_by_tag_name("p>a").get_attribute('href')
            driver.get(apk_detail_url + "/versions")