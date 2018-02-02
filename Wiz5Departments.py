import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
import re
from DepartmentUrlData import DepartmentUrlData
from NoticeData import NoticeData
from DBManager import DBManager


class Wiz5Departments:
    def __init__(self):
        self.base_url = ".sookmyung.ac.kr/wiz5/wizard/frames/server_sub.html?"
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

        self.department_url_data_list = []
        self.department_large_category_list = []
        self.notice_data_list = []
        self.notice_numbers = []
        self.notice_list = []

    def start(self):
        data = json.load(open('wiz5_departments.json'))
        for i in data:
            department_url_data = self.save_department_url_data(i)
            self.department_url_data_list.append(department_url_data)
            self.department_large_category_list.append(i["type"])

        for department_url_data, department_large_category in zip(self.department_url_data_list,
                                                                  self.department_large_category_list):
            total_url = self.get_total_url(department_url_data)
            self.browser.get(total_url)

            start_notice_page = department_url_data.page
            numbers = self.browser.find_elements_by_xpath(
                "//*[@id=\"board-container\"]/div[2]/form/table/tbody/tr/td[2]")
            last_notice_number = self.get_last_notice_number(numbers)
            last_notice_page = self.get_last_page(last_notice_number, 15)

            self.scrap_current_to_max_page(department_url_data, start_notice_page, last_notice_page,
                                           department_large_category)
            self.save_notices_to_db()

    def quit(self):
        self.browser.quit()

    def save_department_url_data(self, item):
        url_data = DepartmentUrlData()
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
        url_data.type = item["type"]
        return url_data

    def get_total_url(self, url_data, page=1):
        url = "https://" + url_data.domain_name + self.base_url
        url += "home_id=" + url_data.home_id
        url += "&menu_seq=" + str(url_data.menu_seq)
        url += "&handle=" + str(url_data.handle)
        url += "&board_id=" + str(url_data.board_id)
        url += "&categoryId=" + str(url_data.category_id)
        url += "&page=" + str(page)
        url += "&siteId=" + url_data.site_id
        return url

    def get_last_notice_number(self, number_data):
        for number in number_data:
            last_number = number.text
            if last_number.isdigit():
                return int(last_number)

    def get_last_page(self, last_number, page_notices_count):
        if last_number % page_notices_count != 0:
            return last_number // page_notices_count + 1
        else:
            return last_number // page_notices_count

    def scrap_current_to_max_page(self, url_data, start_page, last_page, large_category):
        current_page = start_page
        while current_page <= last_page:
            print("page: " + str(current_page))
            notice_href_list = self.browser.find_elements_by_css_selector("td.title > a")
            notice_number_list = self.browser.find_elements_by_css_selector(
                "#board-container > div.list > form > table > tbody > tr > td:nth-child(2)")
            self.save_notices_data(notice_href_list, notice_number_list, large_category)
            current_page += 1
            self.browser.get(self.get_total_url(url_data, current_page))

    def save_notices_data(self, notice_href_list, notice_number_list, large_category):
        for notice, number in zip(notice_href_list, notice_number_list):
            if number.text.isdigit():
                notice_item_url = notice.get_attribute("href")
                notice_item_response = urllib.request.urlopen(notice_item_url)
                soup_notice = BeautifulSoup(notice_item_response, "html.parser")

                notice_data = NoticeData()
                notice_title = soup_notice.select_one("head > title")
                notice_data.title = self.get_content_output(notice_title)
                notice_content = soup_notice.select("td > div")
                notice_data.content = self.get_content_output(notice_content)
                notice_data.large_category = large_category
                self.notice_data_list.append(notice_data)

                time.sleep(1)

    def get_content_output(self, content):
        if content is None:
            return ""
        stripped = str(content).strip()
        stripped = re.sub(r'<[^>]*?>', '', stripped)
        pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
        return pattern.sub(u'\uFFFD', stripped)

    def save_notices_to_db(self):
        for i in self.notice_data_list:
            DBManager.insert(1, i.large_category, i.large_category, i.title, i.content)
            # To-do: change number
