import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
from DepartmentUrlData import DepartmentUrlData


def save_department_url_data(item, url_data):
    url_data.college = item["college"]
    url_data.department = item["department"]
    url_data.domain_name = item["domain_name"]
    url_data.home_id = item["home_id"]
    url_data.menu_seq = item["menu_seq"]
    url_data.handle = item["handle"]
    url_data.board_id = item["board_id"]
    url_data.category_id = item["categoryId"]
    url_data.page = item["page"]
    url_data.site_id = item["siteId"]


def get_total_url(url_data, page):
    url = "https://" + url_data.domain_name + base_url
    url += "home_id=" + url_data.home_id
    url += "&menu_seq=" + str(url_data.menu_seq)
    url += "&handle=" + str(url_data.handle)
    url += "&board_id=" + str(url_data.board_id)
    url += "&categoryId=" + str(url_data.category_id)
    url += "&page=" + str(page)
    url += "&siteId=" + url_data.site_id
    return url


def get_last_page(last_number, page_notices_count):
    if last_number % page_notices_count != 0:
        return last_number // page_notices_count + 1
    else:
        return last_number // page_notices_count


def save_titles_and_contents_of(selected_page):
    for notice in selected_page:
        print("title: ", notice.text)
        #time.sleep(1)
        # print("content: ", )


def scrap_current_to_max_page(url_data, start_page, last_page):
    current_page = start_page
    while current_page <= last_page:
        print("page: " + str(current_page))
        page_notices = browser.find_elements_by_css_selector("tbody > tr > td.title")
        save_titles_and_contents_of(page_notices)
        current_page += 1
        browser.get(get_total_url(url_data, current_page))


def get_last_notice_number(number_data):
    for number in number_data:
        last_number = number.text
        if last_number.isdigit():
            return int(last_number)


department_url_data_list = []
data = json.load(open('wiz5_departments.json'))
base_url = ".sookmyung.ac.kr/wiz5/wizard/frames/server_sub.html?"

browser = webdriver.PhantomJS()
browser.implicitly_wait(3)

for i in data:
    department_url_data = DepartmentUrlData()
    save_department_url_data(i, department_url_data)
    department_url_data_list.append(department_url_data)

departments_notice_list = []

count = 0

for department_url_data in department_url_data_list:
    total_url = get_total_url(department_url_data, department_url_data.page)
    browser.get(total_url)
    browser.save_screenshot("department" + str(count) + ".png")

    start_notice_page = department_url_data.page
    numbers = browser.find_elements_by_xpath("//*[@id=\"board-container\"]/div[2]/form/table/tbody/tr/td[2]")
    last_notice_number = get_last_notice_number(numbers)
    last_notice_page = get_last_page(last_notice_number, len(browser.find_elements_by_css_selector("tbody > tr > td.title")))

    notice_list = []
    scrap_current_to_max_page(department_url_data, start_notice_page, last_notice_page)
    count += 1

browser.quit()
