#!/usr/bin/python3
#-*-coding:utf-8-*-
from pymysql import InternalError
from selenium import webdriver
from app.crawlers.DBManager import DBManager
from app.crawlers.Record import Record
from selenium.common.exceptions import NoSuchElementException
import time
import json


class WizCrawler:
    record_list = []
    browser = None
    department = None
    type = None
    page_count = 0
    site_default_url = None

    def __init__(self):
        WizCrawler.browser = webdriver.PhantomJS()
        WizCrawler.browser.implicitly_wait(3)
        return

    @classmethod
    def setFields(cls, department, type):
        WizCrawler.department = department
        WizCrawler.type = type
        return

    @classmethod
    def print_list(cls):
        row_col = WizCrawler.browser.find_elements_by_css_selector('td.list_td1')
        NUMBER_COLUMN = len(WizCrawler.browser.find_elements_by_css_selector('td.title_bg1'))
        if NUMBER_COLUMN!=0:
            list_len = len(row_col) // NUMBER_COLUMN
        else: list_len = len(row_col)
        for count in range(0, list_len):
            record = Record()
            try:
                row_col = WizCrawler.browser.find_elements_by_css_selector('td.list_td1')
                number = row_col.__getitem__(count * NUMBER_COLUMN)
                if number.text != '공지':
                    title_tr = row_col.__getitem__(count * NUMBER_COLUMN + 2)
                    title_a = title_tr.find_element_by_css_selector('a')
                    if DBManager.is_notice_already_saved(title_a.text, WizCrawler.department):
                        return True
                    else:
                        record.title = title_a.text
                        record.id = number.text
                        record.view = row_col.__getitem__(NUMBER_COLUMN * (count + 1) - 1).text
                        WizCrawler.print_link_content(title_a, record)
            except IndexError:
                print(str(count) + " " + record.title)
        return False

    @classmethod
    def move_to_next_page(cls):
        WizCrawler.page_count += 1
        if WizCrawler.page_count > 8:
            return
        if WizCrawler.print_list():
            return
        else:
            try:
                bott_line0 = WizCrawler.browser.find_element_by_css_selector('td.bott_line0')
                next_page = bott_line0.find_element_by_xpath('//b//following-sibling::a')
                next_page.click()
                WizCrawler.browser.implicitly_wait(3)
                time.sleep(2)
                WizCrawler.move_to_next_page()
            except NoSuchElementException:
                print("END OF PAGE")

        return

    @classmethod
    def print_link_content(cls, a, record):
        try:
            a.click()
            WizCrawler.browser.implicitly_wait(3)
            time.sleep(2)
            content = WizCrawler.browser.find_element_by_id('contentsDiv').text
            record.category = WizCrawler.department
            record.division = WizCrawler.type
            record.content = content
            record.date = WizCrawler.browser.find_element_by_css_selector(
                'body > table:nth-child(1) > tbody > tr > td > table > tbody > tr > td:nth-child(2) > font').text.split(
                ' ')[0]
            record.url = WizCrawler.site_default_url
            WizCrawler.record_list.append(record)
            WizCrawler.browser.execute_script("javascript:jf_list()")
            WizCrawler.browser.implicitly_wait(3)
            time.sleep(2)
        except NoSuchElementException:
            print(a.text, " can not find")
        return

    @staticmethod
    def crawl_site(url):
        WizCrawler.site_default_url = url
        WizCrawler.page_count = 0
        WizCrawler.browser.set_window_size(1000, 500)
        WizCrawler.browser.get(url)
        WizCrawler.browser.implicitly_wait(3)
        time.sleep(2)
        WizCrawler.move_to_next_page()
        if WizCrawler.record_list.__len__() > 0:
            WizCrawler.store_to_db()
            WizCrawler.record_list.clear()
        return

    @staticmethod
    def store_to_db():
        for record in WizCrawler.record_list:
            try:
                DBManager.insert(record)
            except InternalError:
                record.content = "InternalError"
                DBManager.insert(record)
                print(record.category + " " + record.division + " " + record.title)
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        WizCrawler.browser.quit()
        return


def read_wiz():
    data = json.load(open('wiz_departments.json', "r", encoding="utf8"))

    crawler = WizCrawler()
    for count in range(0, len(data)):
        department = data[count]['department']
        domain_name = data[count]['domain_name']
        home_id = data[count]['home_id']
        handle = str(data[count]['handle'])
        type = data[count]['type']
        crawler.setFields(department, type)
        wiz = '.sookmyung.ac.kr/wiz/contents/board/board.php?home_id='
        url = 'http://' + domain_name + wiz + home_id + '&handle=' + handle
        crawler.crawl_site(url)
    exit()
    return


DBManager()
read_wiz()
