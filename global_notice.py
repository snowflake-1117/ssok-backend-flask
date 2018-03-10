#!/usr/bin/python3
#-*-coding:utf-8-*-
from selenium import webdriver
from app.crawlers.DBManager import DBManager
from app.crawlers.Record import Record
import time


def set_record_list(length, url_list):
    global num
    for url in url_list:
        if length > 0:
            length -= 1
        else:
            browser.set_window_size(1024, 768)
            browser.get(url)
            time.sleep(3)
            title = browser.find_element_by_class_name('tit').text
            content = browser.find_element_by_id('contentsDiv').get_attribute('innerHTML')
            num = num + 1
            date = browser.find_element_by_css_selector(
                '#board-container > div.view > table > tbody > tr:nth-child(1) > td.date').text
            view = browser.find_element_by_css_selector('td.no').text
            view = int(view)

            if DBManager.is_notice_url_already_saved(url):
                return True
            else:
                record = Record()
                record.title = title
                record.content = content
                record.id = num
                record.date = date
                record.view = view
                record.category = '공통'
                record.division = '국제'
                record.url = url
                record_list.append(record)
    return False


def move_page():
    for i in range(1, last_page_num + 1):
        current_list_page = global_url + "&page=" + str(i)
        browser.get(current_list_page)
        element_list = browser.find_elements_by_css_selector(
            '#board-container > div.list > form > table > tbody > tr > td.title > a')
        url_list = []
        for element in element_list:
            url_list.append(element.get_attribute('href'))

        if set_record_list(notice_len, url_list):
            return


DBManager()

global_url = 'http://cms.sookmyung.ac.kr/wiz5/contents/board/board_action.php?home_id=exchange&handle=7&scale=15&categoryId=1&categoryDepth=&parent='
browser = webdriver.PhantomJS()
browser.get(global_url)

last_page_num = len(browser.find_elements_by_tag_name('li'))

notice_list = browser.find_elements_by_css_selector(
    '#board-container > div.list > form > table > tbody > tr > td > img')
notice_len = len(notice_list)

record_list = []

num = 0
move_page()

if record_list.__len__() > 0:
    for record_data in record_list:
        DBManager.insert(record_data)

browser.quit()
