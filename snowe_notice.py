from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from snowe_notice_board import *
import time

def set_page_crawling():
    global page_max
    page_end = browser.find_element_by_css_selector('a.next_end')
    page_max = page_end.get_attribute('href')[len(url) + 1:]
    print(page_max)
    page_max = int(page_max)
    return;

def crawl_pages():
    global count
    count = 1
    while count <= page_max:
        print('page: ',str(count))
        browser.get(url+'#'+str(count))
        time.sleep(5)
        call_list()
        count+=1
    return;

def call_list():
    board = browser.find_element_by_xpath('//*[@id="messageListBody"]')
    td_list = board.find_elements_by_css_selector('td.title')
    for td in td_list:
        try:
            a = td.find_element_by_css_selector('a')
            href = a.get_attribute('href')
            print("-", href)
            span = a.find_element_by_css_selector('span')
            print("-", span.text)
            print_page(href)
        except NoSuchElementException:
            print("-", td.text)
    return;

global url
url = 'https://snowe.sookmyung.ac.kr/bbs5/boards/notice'
browser = webdriver.PhantomJS()
browser.implicitly_wait(3)
browser.get(url)
time.sleep(5)
set_page_crawling()
crawl_pages()
call_list()
browser.quit()

