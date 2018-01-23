import urllib.request
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

url = 'http://english.sookmyung.ac.kr/wiz/contents/board/board.php?home_id=english&handle=3'
browser = webdriver.PhantomJS()
browser.implicitly_wait(3)
browser.get(url)

titles = browser.find_elements_by_xpath('/html/body/form[2]/table/tbody/tr[*]/td[3]')

# get the lists
#for title in titles:
#        print ("-",title.text)

for title in titles:
    try:
        a = title.find_element_by_css_selector("a")
        print ("-",a.get_attribute("href"))
        print(title.text)
    except NoSuchElementException:
        print(title.text)

browser.quit()

