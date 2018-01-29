from selenium import webdriver
import time

url = 'https://snowe.sookmyung.ac.kr/bbs5/boards/jobcareer'

browser = webdriver.Chrome()
browser.implicitly_wait(3)
browser.get(url)
time.sleep(5)

browser.find_element_by_id('userId').send_keys('')
browser.find_element_by_id('userPassword').send_keys('')
browser.find_element_by_id('loginButton').click()
browser.get(url)

browser.find_element_by_id('fnshVDT').click()
page_end = browser.find_element_by_css_selector('a.next_end').click()
url = browser.current_url

notice_list = browser.find_elements_by_class_name('notice')
