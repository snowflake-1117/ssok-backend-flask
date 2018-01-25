from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time



def print_list():
    titles = browser.find_elements_by_css_selector('td.list_td1')
    list_len = len(titles)//5
    print('count list: '+str(list_len))
    START_OF_LIST_TD = 5
    current_url = browser.current_url
    for count in range(0, 2):
        try:
            a = browser.find_element_by_xpath('/html/body/form[2]/table/tbody/tr['+str(count+START_OF_LIST_TD)+']/td[3]/a')
            href = a.get_attribute("href")
            #print("href: ", href)
            print(str(count+1)+"."+"제목: ",a.text)
            print_link(a,current_url)
        except NoSuchElementException:
            print("-",a.text)

    move_to_next_page()
    return

def move_to_next_page():
    tr_list = browser.find_elements_by_xpath('/html/body/form[2]/table/tbody/tr[*]')
    table_len = str(len(tr_list)-2)
    page_list = browser.find_elements_by_xpath('/html/body/form[2]/table/tbody/tr['+table_len+']/td/table/tbody/tr/td[2]/*')
    current_page = browser.find_element_by_xpath('/html/body/form[2]/table/tbody/tr['+table_len+']/td/table/tbody/tr/td[2]/b')
    current_page_number = int(current_page.text[1:len(current_page.text)-1])
    print('page:',current_page_number)
    if(current_page_number==28):
        print("END OF PAGE")
    else:
        current_item_count = page_list.index(current_page)
        a = page_list.__getitem__(current_item_count+1)
        a.click()
        time.sleep(5)
    return

def print_link(a,start_url):
    # a.click()
    # time.sleep(5)
    # content_div =browser.find_element_by_xpath('//*[@id="contentsDiv"]')
    # print('<content>\n',content_div.text)
    # span_list = browser.find_elements_by_css_selector('span')
    # content = ""
    # for span in span_list:
    #     if span.text:
    #         content = content + span.text + '\n'
    # print('<content>\n',content)
    print('>')
    browser.get(start_url)
    time.sleep(5)
    return

browser = webdriver.PhantomJS()
browser.implicitly_wait(3)
browser.get('http://english.sookmyung.ac.kr/wiz/contents/board/board.php?home_id=english&handle=3')
time.sleep(5)

print_list()

browser.quit()

