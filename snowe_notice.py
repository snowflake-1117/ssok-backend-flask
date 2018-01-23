import urllib.request
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

url = 'https://snowe.sookmyung.ac.kr/bbs5/boards/notice'
browser = webdriver.PhantomJS()
browser.implicitly_wait(3)
browser.get(url)

#print(browser.find_element_by_tag_name('html').text)
board = browser.find_element_by_xpath('//*[@id="messageListBody"]')
noticeTds = board.find_elements_by_css_selector('td.title')
for td in noticeTds:
    a = td.find_element_by_css_selector('a')
    href = a.get_attribute('href')
    try:
        print("-",href)
        span = a.find_element_by_css_selector('span')
        print(span.text)
    except NoSuchElementException:
        print("-", href)


browser.quit()

