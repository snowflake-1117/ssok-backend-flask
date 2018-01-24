from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def submit(href):
    #browser.execute_script("return "+href)
    #browser.find_element_by_xpath("//a[@href=\"javascript:page_link('" + str(count) + "')\"]").click()
    browser.find_element_by_xpath("//a[@href=\""+href+"\"]").click()
    return;

def printList():
    titles = browser.find_elements_by_xpath('/html/body/form[2]/table/tbody/tr[*]/td[3]')

    for title in titles:
        try:
            a = title.find_element_by_css_selector("a")
            global href
            href = a.get_attribute("href")
            href = href[:len(href)-1]
            print("-", href)
            print(title.text)
            submit(href)
        except NoSuchElementException:
            print(title.text)
    return;

url = 'http://english.sookmyung.ac.kr/wiz/contents/board/board.php?home_id=english&handle=3'
browser = webdriver.PhantomJS()
browser.implicitly_wait(3)
browser.get(url)

printList()

browser.quit()

