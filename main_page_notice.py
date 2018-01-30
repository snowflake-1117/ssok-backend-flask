import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
from NoticeData import NoticeData


def get_last_page(last_number):
    if last_number % 10 != 0:
        return last_number // 10 + 1
    else:
        return last_number // 10


def scrape_current_to_max_page(start_page, last_page):
    current_page = start_page
    while current_page <= last_page:
        print("page: " + str(current_page))
        page_notices = browser.find_elements_by_css_selector("a.artclLinkView")
        save_notices_data(page_notices)
        current_page += 1
        browser.find_element_by_xpath(get_page_link(current_page)).click()


def save_notices_data(selected_page):
    for notice in selected_page:
        main_page_notice = NoticeData()
        save_title(notice, main_page_notice)
        save_content_and_category(notice, main_page_notice)
        main_page_notice_list.append(main_page_notice)
        time.sleep(1)


def save_title(notice, main_page_notice):
    main_page_notice.title = notice.text


def save_content_and_category(notice, main_page_notice):
    notice_item_url = notice.get_attribute("href")
    notice_item_response = urllib.request.urlopen(notice_item_url)
    soup_notice = BeautifulSoup(notice_item_response, "html.parser")
    notice_content = soup_notice.select_one(".view_contents")
    main_page_notice.content = get_content_output(notice_content)
    notice_large_category = soup_notice.select_one("div.view_top > dl > dd")
    main_page_notice.large_category = notice_large_category.text


def get_content_output(content_sentences):
    output = ""
    for content_sentence in content_sentences.contents:
        stripped = str(content_sentence).strip()
        if stripped == "":
            continue
        output += re.sub(r'<[^>]*?>', '', stripped)
    return output


def get_page_link(current_page):
    return "//a[@href=\"javascript:page_link('" + str(current_page) + "')\"]"


url = "http://www.sookmyung.ac.kr"
sub_url = "/bbs/sookmyungkr/66/artclList.do"
notice_bbs_url = url + sub_url

browser = webdriver.PhantomJS()
browser.implicitly_wait(3)
browser.get(notice_bbs_url)

start_notice_page = 1
last_notice_number = int(browser.find_element_by_class_name("num").text)
last_notice_page = get_last_page(last_notice_number)

main_page_notice_list = []
scrape_current_to_max_page(start_notice_page, last_notice_page)

browser.quit()
