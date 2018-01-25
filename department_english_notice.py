from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

def print_list():
    a_list = browser.find_elements_by_xpath('/html/body/form[2]/table/tbody/tr[*]/td[3]/a')
    for a in a_list:
        try:
            href = a.get_attribute("href")
            print("-", href)
            print("-",a.text)
            # print_link(a)
        except NoSuchElementException:
            print("-",a.text)

    return

def print_link(a):
    a.click()
    time.sleep(5)
    span_list = browser.find_elements_by_css_selector('span')
    content = ""
    for span in span_list:
        if span.text:
            content = content + span.text + '\n'
    print('<content>\n',content)
    browser.get(board_url)
    time.sleep(5)
    return

global board_url
board_url = 'http://english.sookmyung.ac.kr/wiz/contents/board/board.php?home_id=english&handle=3'
browser = webdriver.PhantomJS()
browser.implicitly_wait(3)
browser.get(board_url)
time.sleep(5)
print_list()
browser.quit()

