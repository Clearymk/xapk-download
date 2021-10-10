import re
from queue import Queue
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException

driver = webdriver.Chrome()
temp = set()
# 用于记录需要下载的任务
download_task = Queue()
base_url = "https://apkpure.com/"
categorys = []

def add_base_mission(category):
    target_url = base_url + category
    driver.get(target_url)
    for item in driver.find_elements_by_css_selector("a[target=\"_blank\"]"):
        if re.match(r"https://apkpure.com/[\s\S]*/[\s\S]*", item.get_attribute("href")):
            temp.add(item.get_attribute("href"))


def get_category_info():
    target_url = base_url + "app"
    driver.get(target_url)
    for item in driver.find_elements_by_css_selector("ul[class=\"index-category cicon\"]>li>a"):
        categorys.append(item.get_attribute("href").split("/")[-1])


if __name__ == "__main__":
    # add_base_mission("art_and_design")
    # for item in temp:
    #     print(item)
    get_category_info()
    for category in categorys:
        add_base_mission(category)
    with open("../mission.txt", "a+") as f:
        for item in temp:
            print(item.split("/")[-1])
            f.write(item.split("/")[-1])
    driver.quit()
