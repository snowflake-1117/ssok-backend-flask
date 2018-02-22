from app.crawlers.DBManager import *
import re
from bs4 import BeautifulSoup
import urllib.request


class CrawlerHelper:
    @staticmethod
    def get_soup(notice):
        notice_item_url = notice.get_attribute("href")
        notice_item_response = urllib.request.urlopen(notice_item_url)
        return BeautifulSoup(notice_item_response, "html.parser")

    @staticmethod
    def get_last_notice_number(number_list):
        for number in number_list:
            last_number = number.text
            if last_number.isdigit():
                return int(last_number)

    @staticmethod
    def get_last_page(last_number, page_notices_count):
        if last_number % page_notices_count != 0:
            return last_number // page_notices_count + 1
        else:
            return last_number // page_notices_count

    @staticmethod
    def get_content_output(content):
        if content is None:
            return ""
        stripped = str(content).strip()
        stripped = re.sub(r'<[^>]*?>', '', stripped)
        pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
        return pattern.sub(u'\uFFFD', stripped)

    @staticmethod
    def save_record_list_to_db(record_list):
        for i in record_list:
            DBManager.insert(i)
