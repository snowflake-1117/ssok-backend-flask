from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def printList():
    titles = browser.find_elements_by_xpath('/html/body/form[2]/table/tbody/tr[*]/td[3]')

    for title in titles:
        try:
            a = title.find_element_by_css_selector("a")
            href = a.get_attribute("href")
            print("-", href)
            print(title.text)
        except NoSuchElementException:
            print(title.text)
    return;

url = 'http://english.sookmyung.ac.kr/wiz/contents/board/board.php?home_id=english&handle=3'
browser = webdriver.PhantomJS()
browser.implicitly_wait(3)
browser.get(url)

browser.quit()

