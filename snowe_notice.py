from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

def printPage(contentUrl):
    browser.get(contentUrl)
    article = browser.find_element_by_css_selector('div.article')
    pList = article.find_elements_by_tag_name('p')
    content = ""
    for p in pList:
        if p.text:
            content = content + p.text + '\n'
    print(content)
    return;

def setPageCrawling():
    global page_max
    page_end = browser.find_element_by_css_selector('a.next_end')
    page_max = page_end.get_attribute('href')[len(url) + 1:]
    print(page_max)
    page_max = int(page_max)
    return;

def crawlPages():
    global count
    count = 1
    while count <= page_max:
        print('page: '+str(count))
        callBoardList()
        time.sleep(1)
        count+=1
        browser.get(url+count)
    return;

def callBoardList():
    board = browser.find_element_by_xpath('//*[@id="messageListBody"]')
    noticeTds = board.find_elements_by_css_selector('td.title')
    for td in noticeTds:
        try:
            a = td.find_element_by_css_selector('a')
            href = a.get_attribute('href')
            print("-", href)
            span = a.find_element_by_css_selector('span')
            print("-", span.text)
            printPage(href)
        except NoSuchElementException:
            print("-", td.text)
    return;

global url
url = 'https://snowe.sookmyung.ac.kr/bbs5/boards/notice'
browser = webdriver.PhantomJS()
global browser
browser.implicitly_wait(3)
browser.get(url)
time.sleep(5)
setPageCrawling()
crawlPages()
browser.quit()

