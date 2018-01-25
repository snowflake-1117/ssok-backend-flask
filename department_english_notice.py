from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


def print_list():
    titles = browser.find_elements_by_css_selector('td.list_td1')
    list_len = len(titles)//5
    print('count list: '+str(list_len))
    START_OF_LIST_TD = 5

    for count in range(0, list_len):
        try:
            a = browser.find_element_by_xpath('/html/body/form[2]/table/tbody/tr['+str(count+START_OF_LIST_TD)+']/td[3]/a')
            href = a.get_attribute("href")
            print("href: ", href)
            print(str(count)+"."+"제목: ",a.text)
            print_link(a)
        except NoSuchElementException:
            print("-",a.text)

    return

def print_link(a):
    a.click()
    time.sleep(5)
    content_div =browser.find_element_by_xpath('//*[@id="contentsDiv"]')
    print('<content>\n',content_div.text)
    # span_list = browser.find_elements_by_css_selector('span')
    # content = ""
    # for span in span_list:
    #     if span.text:
    #         content = content + span.text + '\n'
    # print('<content>\n',content)
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

