import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re

# request main notice url
url = "http://www.sookmyung.ac.kr"
sub_url = "/bbs/sookmyungkr/66/artclList.do"
notice_bbs_url = url + sub_url
response = urllib.request.urlopen(notice_bbs_url)

# start PhantomJS
browser = webdriver.PhantomJS()
browser.implicitly_wait(3)
browser.get(notice_bbs_url)

# browser.save_screenshot("notice_main.png")

# get max page number
soup = BeautifulSoup(response, "html.parser")
max_count = int(soup.select(".num")[0].text) // 10
max_count = max_count + 1

# initialize start page number
count = 1

while count <= max_count:
    # print page
    print("page: " + str(count))

    # get notice items
    results = browser.find_elements_by_css_selector("a.artclLinkView")

    # print result: title, and content
    for result in results:
        print("제목: ", result.text)
        notice_item_url = result.get_attribute("href")
        response = urllib.request.urlopen(notice_item_url)
        soup_notice = BeautifulSoup(response, "html.parser")
        content = soup_notice.select_one(".view_contents")
        output = ""
        for item in content.contents:
            stripped = str(item).strip()
            if stripped == "":
                continue
            output += re.sub(r'<[^>]*?>', '', stripped)
        print(output)
        print("")

        # sleep
        time.sleep(1)

    # click next page
    count += 1
    browser.find_element_by_xpath("//a[@href=\"javascript:page_link('" + str(count) + "')\"]").click()

# close PhantomJS
browser.quit()
