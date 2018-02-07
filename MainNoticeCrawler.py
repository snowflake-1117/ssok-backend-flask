from selenium import webdriver
import time
from datetime import datetime
from Record import Record
from CrawlerHelper import CrawlerHelper


class MainNoticeCrawler:
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
        number_list = self.browser.find_elements_by_class_name("num")
        last_notice_number = CrawlerHelper.get_last_notice_number(number_list)
        last_notice_page = CrawlerHelper.get_last_page(last_notice_number, 10)
        self.scrape_current_to_max_page(start_notice_page, last_notice_page)
        CrawlerHelper.save_record_list_to_db(self.record_list)

    def quit(self):
        self.browser.quit()

    def scrape_current_to_max_page(self, start_page, last_page):
        current_page = start_page
        while current_page <= last_page:
            current_page += 1
            self.set_notices_data()
            self.browser.find_element_by_xpath(self.get_page_link(current_page)).click()

    def set_notices_data(self):
        notice_list = self.browser.find_elements_by_css_selector("a.artclLinkView")
        notice_notice_id_list = self.browser.find_elements_by_css_selector("td.notice")
        notice_num_id_list = self.browser.find_elements_by_css_selector("td.num")
        notice_id_list = notice_notice_id_list + notice_num_id_list
        for notice, notice_id in zip(notice_list, notice_id_list):
            if notice_id.text.isdigit():
                soup_notice = CrawlerHelper.get_soup(notice)
                record = self.get_record_data(notice_id, soup_notice)
                self.record_list.append(record)
                time.sleep(1)

    def get_record_data(self, notice_id, soup):
        record = Record()
        record.id = int(notice_id.text)
        record.category = soup.select("div.view_top > dl > dd")[0].text
        record.division = soup.select("div.view_top > dl > dd")[0].text
        record.title = CrawlerHelper.get_content_output(soup.select_one("div.view_top > dl > dt").text)
        record.content = CrawlerHelper.get_content_output(soup.select_one(".view_contents").text)
        record.view = int(soup.select("div.view_top > dl > dd")[1].text)
        record.date = datetime.strptime(soup.select("div.view_top > dl > dd")[2].text, "%Y.%m.%d").date()
        return record

    def get_page_link(self, current_page):
        return "//a[@href=\"javascript:page_link('" + str(current_page) + "')\"]"
