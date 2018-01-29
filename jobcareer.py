from selenium import webdriver
import time

url = 'https://snowe.sookmyung.ac.kr/bbs5/boards/jobcareer'

browser = webdriver.Chrome()
browser.implicitly_wait(3)
browser.get(url)
time.sleep(3)

browser.find_element_by_id('userId').send_keys('')
browser.find_element_by_id('userPassword').send_keys('')
browser.find_element_by_id('loginButton').click()
browser.implicitly_wait(3)
browser.get(url)

browser.implicitly_wait(3)
browser.find_element_by_id('fnshVDT').click()
browser.implicitly_wait(3)
time.sleep(2)
browser.find_element_by_css_selector('#pagingBar > a.next_end').click()
#url = browser.current_url

time.sleep(2)
element_list = browser.find_elements_by_css_selector('#messageListBody > tr')
total_len = len(element_list)
time.sleep(2)
notice_list = browser.find_elements_by_css_selector('#messageListBody > tr.notice')
notice_len = len(notice_list)
real_len = total_len - notice_len

url_list = [element_list[i].find_element_by_css_selector('td.title.unread > a').get_attribute("href") for i in range(notice_len, len(element_list))]

print(url_list)