from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

def print_list():
    titles = browser.find_elements_by_css_selector('td.list_td1')

    for title in titles:
        try:
            a = title.find_element_by_css_selector("a")
            href = a.get_attribute("href")
            print("-", href)
            print("-",title.text)
            # a.click()
        except NoSuchElementException:
            print("-",title.text)

    return;

url = 'http://english.sookmyung.ac.kr/wiz/contents/board/board.php?home_id=english&handle=3'
browser = webdriver.PhantomJS()
browser.implicitly_wait(3)
browser.get(url)
time.sleep(5)
#print(browser.find_element_by_css_selector('html').text)
print_list()

browser.quit()

