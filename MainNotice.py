import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
from NoticeData import NoticeData
from UnivDBManager import UnivDBManager
from pymysql import InternalError


class MainNotice:
    def __init__(self):
        self.url = "http://www.sookmyung.ac.kr"
        self.sub_url = "/bbs/sookmyungkr/66/artclList.do"
        self.notice_bbs_url = self.url + self.sub_url

        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.browser.get(self.notice_bbs_url)
        self.main_page_notice_list = []

    def start(self):
        start_notice_page = 1
        last_notice_number = int(self.browser.find_element_by_class_name("num").text)
        last_notice_page = self.get_last_page(last_notice_number, 10)
        self.scrape_current_to_max_page(start_notice_page, last_notice_page)
        self.save_notices_to_db()

    def quit(self):
        self.browser.quit()

    def get_last_page(self, last_number, page_notices_count=10):
        if last_number % page_notices_count != 0:
            return last_number // page_notices_count + 1
        else:
            return last_number // page_notices_count

    def scrape_current_to_max_page(self, start_page, last_page):
        current_page = start_page
        while current_page <= last_page:
            print("page: " + str(current_page))
            page_notices = self.browser.find_elements_by_css_selector("a.artclLinkView")
            self.save_notices_data(page_notices)
            self.browser.find_element_by_xpath(self.get_page_link(current_page)).click()
            current_page += 1

    def save_notices_data(self, selected_page):
        for notice in selected_page:
            main_page_notice = NoticeData()
            self.save_title(notice, main_page_notice)
            self.save_content_and_category(notice, main_page_notice)
            self.main_page_notice_list.append(main_page_notice)
            time.sleep(1)

    def save_title(self, notice, main_page_notice):
        main_page_notice.title = notice.text

    def save_content_and_category(self, notice, main_page_notice):
        notice_item_url = notice.get_attribute("href")
        notice_item_response = urllib.request.urlopen(notice_item_url)
        soup_notice = BeautifulSoup(notice_item_response, "html.parser")
        notice_content = soup_notice.select_one(".view_contents")
        main_page_notice.content = self.get_content_output(notice_content)
        notice_large_category = soup_notice.select_one("div.view_top > dl > dd")
        main_page_notice.large_category = notice_large_category.text

    def get_content_output(self, content_sentences):
        if content_sentences is None:
            return ""
        output = ""
        for content_sentence in content_sentences.contents:
            stripped = str(content_sentence).strip()
            if stripped == "":
                continue
            output += re.sub(r'<[^>]*?>', '', stripped)
        return output

    def get_page_link(self, current_page):
        return "//a[@href=\"javascript:page_link('" + str(current_page) + "')\"]"

    def save_notices_to_db(self):
        for i in self.main_page_notice_list:
            try:
                UnivDBManager.insert(1, i.large_category, i.large_category, i.title, i.content)
                # To-do: change number
            except InternalError:
                continue
