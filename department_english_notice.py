from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

def print_list():
    titles = browser.find_elements_by_css_selector('td.list_td1')
    list_len = len(titles)//5
    print('count list: '+str(list_len))
    START_OF_LIST_TD = 5
    count =0
    while count < list_len:
        list = browser.find_elements_by_xpath('/html/body/form[2]/table/tbody/tr[*]/td[3]/a')
        a = list.__getitem__(count)
        print(str(count+1)+"."+"제목: ",a.text)
        print_link(a)
        count+=1
        #print("-",'NoSuchElementException')
    return

def move_to_next_page():
    print_list()
    total_tr = browser.find_elements_by_xpath('/html/body/form[2]/table/tbody/tr[*]')
    page_location = str(len(total_tr) - 2)
    page_list = browser.find_elements_by_xpath(
        '/html/body/form[2]/table/tbody/tr[' + page_location + ']/td/table/tbody/tr/td[2]/*')
    current_page = browser.find_element_by_xpath(
        '/html/body/form[2]/table/tbody/tr[' + page_location + ']/td/table/tbody/tr/td[2]/b')
    CURRENT_NUMBER = current_page.text
    page_last = page_list.__getitem__(len(page_list) - 1)
    LAST_NUMBER = page_last.text
    print('page:', CURRENT_NUMBER + '/' + LAST_NUMBER)
    if(LAST_NUMBER !='[다음]' and CURRENT_NUMBER==LAST_NUMBER):
        print("END OF PAGE")
    else:
        current_item_count = page_list.index(current_page)
        next_page = page_list.__getitem__(current_item_count+1)
        next_page.click()
        time.sleep(5)
        move_to_next_page()
    return


def print_link(a):
    a.click()
    time.sleep(5)
    content_div =browser.find_element_by_xpath('//*[@id="contentsDiv"]')
    print('<content>\n',content_div.text)
    browser.execute_script("window.history.go(-1)")
    time.sleep(5)
    return

url = 'http://english.sookmyung.ac.kr/wiz/contents/board/board.php?home_id=english&handle=3'
browser = webdriver.PhantomJS()
browser.implicitly_wait(3)
browser.get(url)
time.sleep(5)
move_to_next_page()
browser.quit()

