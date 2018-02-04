import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime
from Record import Record
from DBManager import DBManager


class MainNotice:
    def __init__(self):
        self.url = "http://www.sookmyung.ac.kr"
        self.sub_url = "/bbs/sookmyungkr/66/artclList.do"
        self.notice_bbs_url = self.url + self.sub_url

        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.browser.get(self.notice_bbs_url)
        self.record_list = []

    def start(self):
        start_notice_page = 1
        last_notice_number = int(self.browser.find_element_by_class_name("num").text)
        last_notice_page = self.get_last_page(last_notice_number, 10)
        self.scrape_current_to_max_page(start_notice_page, last_notice_page)
        self.save_record_list_to_db()

    def quit(self):
        self.browser.quit()

    def get_last_page(self, last_number, page_notices_count):
        if last_number % page_notices_count != 0:
            return last_number // page_notices_count + 1
        else:
            return last_number // page_notices_count

    def scrape_current_to_max_page(self, start_page, last_page):
        current_page = start_page
        while current_page <= last_page:
            notice_list = self.browser.find_elements_by_css_selector("a.artclLinkView")
            notice_id_list = self.browser.find_elements_by_css_selector("td.num")
            self.record_notices_data_to_list(notice_list, notice_id_list)
            self.browser.find_element_by_xpath(self.get_page_link(current_page)).click()
            current_page += 1

    def record_notices_data_to_list(self, notice_list, notice_id_list):
        for notice, notice_id in zip(notice_list, notice_id_list):
            soup_notice = self.get_soup(notice)
            record = self.get_record_data(notice_id, soup_notice)
            self.record_list.append(record)
            time.sleep(1)

    def get_soup(self, notice):
        notice_item_url = notice.get_attribute("href")
        notice_item_response = urllib.request.urlopen(notice_item_url)
        return BeautifulSoup(notice_item_response, "html.parser")

    def get_record_data(self, notice_id, soup):
        record = Record()
        record.id = int(notice_id.text)
        record.category = soup.select("div.view_top > dl > dd")[0].text
        record.division = soup.select("div.view_top > dl > dd")[0].text
        record.title = self.get_content_output(soup.select_one("div.view_top > dl > dt").text)
        record.content = self.get_content_output(soup.select_one(".view_contents").text)
        record.view = int(soup.select("div.view_top > dl > dd")[1].text)
        record.date = datetime.strptime(soup.select("div.view_top > dl > dd")[2].text, "%Y.%m.%d").date()
        return record

    def get_content_output(self, content):
        if content is None:
            return ""
        stripped = str(content).strip()
        stripped = re.sub(r'<[^>]*?>', '', stripped)
        pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
        return pattern.sub(u'\uFFFD', stripped)

    def get_page_link(self, current_page):
        return "//a[@href=\"javascript:page_link('" + str(current_page) + "')\"]"

    def save_record_list_to_db(self):
        for i in self.record_list:
            DBManager.insert(i)
