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
        self.main_page_notice_list = []

    def start(self):
        start_notice_page = 1
        last_notice_number = int(self.browser.find_element_by_class_name("num").text)
        last_notice_page = self.get_last_page(last_notice_number, 10)
        self.scrape_current_to_max_page(start_notice_page, last_notice_page)
        # self.save_notices_to_db()

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
            notice_list = self.browser.find_elements_by_css_selector("a.artclLinkView")
            notice_id_list = self.browser.find_elements_by_css_selector("td.num")
            self.record_notices_data_to_list(notice_list,notice_id_list)
            self.browser.find_element_by_xpath(self.get_page_link(current_page)).click()
            current_page += 1

    def record_notices_data_to_list(self, notice_list, notice_id_list):
        for notice, notice_id in zip(notice_list, notice_id_list):
            main_page_notice = Record()
            notice_item_url = notice.get_attribute("href")
            notice_item_response = urllib.request.urlopen(notice_item_url)
            soup_notice = BeautifulSoup(notice_item_response, "html.parser")

            self.record_id(notice_id, main_page_notice)
            self.record_category_and_division(soup_notice, main_page_notice)
            self.record_title(soup_notice, main_page_notice)
            self.record_content(soup_notice, main_page_notice)
            self.record_view(soup_notice, main_page_notice)
            self.record_date(soup_notice, main_page_notice)
            DBManager.insert(main_page_notice)
            self.main_page_notice_list.append(main_page_notice)
            time.sleep(1)

    def record_id(self, notice_id, main_page_notice):
        main_page_notice.id = int(notice_id.text)

    def record_title(self, soup_notice, main_page_notice):
        main_page_notice.title = soup_notice.select_one("div.view_top > dl > dt")

    def record_content(self, soup_notice, main_page_notice):
        notice_content = soup_notice.select_one(".view_contents")
        main_page_notice.content = self.get_content_output(notice_content)

    def record_category_and_division(self, soup_notice, main_page_notice):
        notice_category = soup_notice.select("div.view_top > dl > dd")[0]
        main_page_notice.category = notice_category.text
        main_page_notice.division = notice_category.text

    def record_view(self, soup_notice, main_page_notice):
        notice_view = soup_notice.select("div.view_top > dl > dd")[1]
        main_page_notice.view = int(notice_view.text)

    def record_date(self, soup_notice, main_page_notice):
        notice_date = soup_notice.select("div.view_top > dl > dd")[2]
        main_page_notice.date = datetime.strptime(notice_date.text, "%Y.%m.%d").date()

    def get_content_output(self, content_sentences):
        if content_sentences is None:
            return ""
        output = ""
        for content_sentence in content_sentences.contents:
            stripped = str(content_sentence).strip()
            if stripped == "":
                continue
            output += re.sub(r'<[^>]*?>', '', stripped)
        pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
        return pattern.sub(u'\uFFFD', output)

    def get_page_link(self, current_page):
        return "//a[@href=\"javascript:page_link('" + str(current_page) + "')\"]"

    # def save_notices_to_db(self):
    #     for i in self.main_page_notice_list:
    #         DBManager.insert(i)
            # To-do: change number
