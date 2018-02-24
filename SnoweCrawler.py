import time

from selenium import webdriver

from app.crawlers.DBManager import *
from CrawlerHelper import CrawlerHelper


class SnowCrawler:
    def __init__(self):
        self.browser = None
        self.url_list = None
        self.titles = None
        self.nums = None
        self.record_list = []
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(3)
        time.sleep(5)
        return

    def set_info(self, user_id, password):
        self.browser.set_window_size(1124, 850)
        self.browser.get('https://snowe.sookmyung.ac.kr/bbs5/users/login')
        time.sleep(3)
        self.browser.find_element_by_id('userId').send_keys(user_id)
        self.browser.find_element_by_id('userPassword').send_keys(password)
        self.browser.find_element_by_id('loginButton').click()
        self.browser.implicitly_wait(3)
        return

    def crawl_at(self, selected_url):
        self.browser.get(selected_url)
        self.crawl_pages(selected_url)
        self.browser.implicitly_wait(3)
        return

    def crawl_pages(self, selected_url):
        self.browser.implicitly_wait(3)
        time.sleep(2)
        last_page = str(self.browser.find_element_by_css_selector("#pagingBar > a.next_end").get_attribute('href'))
        last_page_num = int(last_page.replace(selected_url, "").replace("#", ""))

        notice_list = self.browser.find_elements_by_css_selector('#messageListBody > tr.notice')
        notice_len = len(notice_list)

        for i in range(2, last_page_num + 1):
            time.sleep(5)
            element_list = self.browser.find_elements_by_css_selector('#messageListBody > tr')
            self.browser.implicitly_wait(3)
            time.sleep(2)
            self.url_list = [element_list[j].find_element_by_css_selector('td.title > a').get_attribute("href")
                             for j in
                             range(len(element_list) - 1, notice_len - 1, -1)]
            num_list = self.browser.find_elements_by_css_selector('#messageListBody > tr > td.num')
            self.nums = [num_list[j].text for j in range(len(num_list) - 1, -1, -1)]
            self.titles = [element_list[j].find_element_by_css_selector('td.title').text for j in
                           range(len(element_list) - 1, notice_len - 1, -1)]

            if self.extract_data(selected_url):
                return
            else:
                self.browser.get(selected_url + "#" + str(i))
        return

    def extract_data(self, select_url):
        k = 0  # index of article numbers and titles
        for url in self.url_list:
            self.browser.implicitly_wait(3)
            self.browser.get(url)
            current_url = self.browser.find_element_by_css_selector(
                '#content > div.boardWrap.noticeGeneric > div.board_detail > div:nth-child(2) > em').text
            if DBManager.does_notice_already_saved(current_url):
                return True
            page_view = self.browser.find_element_by_css_selector(
                '#content > div.boardWrap.noticeGeneric > div.board_detail > div.titleWrap > ul > li.pageview').text
            page_view = page_view.replace('조회수 ', '')
            page_view = int(page_view)
            division = self.browser.find_element_by_css_selector(
                '#content > div.boardWrap.noticeGeneric > div.board_detail > div.titleWrap > strong > span.title_head > span').text
            division = division.replace('[', '')
            division = division.replace(']', '')
            date = self.browser.find_element_by_css_selector(
                '#content > div.boardWrap.noticeGeneric > div.board_detail > div.titleWrap > ul > li:nth-child(4)').text
            date = date[0:10]
            title = self.titles[k]
            content = self.browser.find_element_by_css_selector('#_ckeditorContents').text
            article_num = int(self.nums[k])
            k = k + 1
            record = Record()
            record.content = ' '.join(content.split())
            record.title = title
            record.id = article_num
            if select_url == 'https://snowe.sookmyung.ac.kr/bbs5/boards/notice':
                record.category = '공통'
            else:
                record.category = '취업'
            record.division = division
            record.view = page_view
            record.date = date
            record.url = current_url
            self.record_list.append(record)
            return False
        return

    def start(self):
        urls = ['https://snowe.sookmyung.ac.kr/bbs5/boards/jobcareer',
                'https://snowe.sookmyung.ac.kr/bbs5/boards/notice']
        for url in urls:
            crawler.crawl_at(url)
            if self.record_list.__len__() > 0:
                CrawlerHelper.save_record_list_to_db(self.record_list)
                self.record_list.clear()

    def quit(self):
        self.browser.quit()


DBManager()
crawler = SnowCrawler()
crawler.start()
crawler.quit()
