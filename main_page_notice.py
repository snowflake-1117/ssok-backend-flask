import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re


def get_last_page(last_number):
    if last_number % 10 != 0:
        return last_number // 10 + 1
    else:
        return last_number // 10


def scrape_current_to_max_page(start_page, last_page):
    while start_page <= last_page:
        # print page
        current_page = start_page
        print("page: " + str(current_page))

        selected_notice = browser.find_elements_by_css_selector("a.artclLinkView")
        print_titles_and_contents_of(selected_notice)

        # click next page
        current_page += 1
        browser.find_element_by_xpath("//a[@href=\"javascript:page_link('" + str(current_page) + "')\"]").click()


def print_titles_and_contents_of(selected_page):
    # print result: title, and content
    for notice in selected_page:
        print("제목: ", notice.text)
        notice_item_url = notice.get_attribute("href")
        notice_item_response = urllib.request.urlopen(notice_item_url)
        soup_notice = BeautifulSoup(notice_item_response, "html.parser")
        notice_content = soup_notice.select_one(".view_contents")
        notice_content_output = get_content_output(notice_content)

        print(notice_content_output)
        print("")

        # sleep
        time.sleep(1)


def get_content_output(content_sentences):
    output = ""
    for content_sentence in content_sentences.contents:
        stripped = str(content_sentence).strip()
        if stripped == "":
            continue
        output += re.sub(r'<[^>]*?>', '', stripped)
    return output


# request main notice url
url = "http://www.sookmyung.ac.kr"
sub_url = "/bbs/sookmyungkr/66/artclList.do"
notice_bbs_url = url + sub_url
response = urllib.request.urlopen(notice_bbs_url)

# start PhantomJS
browser = webdriver.PhantomJS()
browser.implicitly_wait(3)
browser.get(notice_bbs_url)

# get last page number
soup = BeautifulSoup(response, "html.parser")
last_notice_number = int(soup.select(".num")[0].text)
last_notice_page = get_last_page(last_notice_number)

# initialize start page number
start_notice_page = 1
scrape_current_to_max_page(start_notice_page, last_notice_page)

# close PhantomJS
browser.quit()
