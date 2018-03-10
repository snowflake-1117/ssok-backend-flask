import time

from selenium import webdriver

from app.crawlers.DBManager import *
from CrawlerHelper import CrawlerHelper


class SnowCrawler:
    def __init__(self):
        self.record_list = []
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(3)
        time.sleep(5)
        return

    def set_info(self, user_id, password):
        self.browser.set_window_size(1000, 500)
        self.browser.get('https://snowe.sookmyung.ac.kr/bbs5/users/login')
        time.sleep(3)
        self.browser.find_element_by_id('userId').send_keys(user_id)
        self.browser.find_element_by_id('userPassword').send_keys(password)
        time.sleep(5)
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
        last_page = str(self.browser.find_element_by_css_selector("#pagingBar > a.next_end").get_attribute('href'))
        last_page_num_str = last_page.replace(selected_url, "").replace("#", "")
        if last_page_num_str != "":
            last_page_num_int = int(last_page_num_str)
        else:
            last_page_num_int = 1

        for i in range(1, last_page_num_int+1):
            self.browser.implicitly_wait(3)
            time.sleep(3)
            notice_list = self.browser.find_elements_by_css_selector('#messageListBody > tr.notice')
            notice_len = len(notice_list)
            url_list = self.browser.find_elements_by_css_selector('#messageListBody > tr > td.title > a')
            url_href_list = []
            for url in url_list:
                if notice_len > 0:
                    notice_len -= 1
                else:
                    url_href_list.append(url.get_attribute("href"))
            num_list = self.browser.find_elements_by_css_selector('#messageListBody > tr > td.num')
            num_string_list = []
            for num in num_list:
                num_string_list.append(num.text)
            if self.extract_data(selected_url, num_string_list, url_href_list):
                return
            else:
                self.browser.get(selected_url + "#" + str(i))
        return

    def extract_data(self, select_url, num_list, url_list):
        for (num, url) in zip(num_list, url_list):
            self.browser.implicitly_wait(3)
            self.browser.get(url)
            time.sleep(3)
            current_url = self.browser.find_element_by_css_selector(
                '#content > div.boardWrap.noticeGeneric > div.board_detail > div:nth-child(2) > em').text
            if DBManager.is_notice_url_already_saved(current_url):
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
            title = self.browser.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[1]/strong/span[1]').text
            content = self.browser.find_element_by_css_selector('#_ckeditorContents').get_attribute('innerHTML')
            article_num = int(num)
            record = Record()
            record.content = content
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
crawler.set_info('', '')
crawler.start()
crawler.quit()
DBManager.delete_duplicated_rows()