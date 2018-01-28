from selenium import webdriver
import time

class WizCrawler:
    browser = None

    def __init__(self):
        WizCrawler.browser = webdriver.PhantomJS()
        WizCrawler.browser.implicitly_wait(3)
        return

    @classmethod
    def print_list(cls):
        titles = WizCrawler.browser.find_elements_by_css_selector('td.list_td1')
        NUMBER_COLUMN = 5
        list_len = len(titles)//NUMBER_COLUMN
        print('count list: '+str(list_len))
        count =0
        while count < list_len:
            titles = WizCrawler.browser.find_elements_by_css_selector('td.list_td1')
            number = titles.__getitem__(count*NUMBER_COLUMN)
            print('number:',number.text)
            if(number.text!='공지'):
                title = titles.__getitem__(count*NUMBER_COLUMN+2)
                link = title.find_element_by_css_selector('a')
                print(str(count + 1) + "." + "제목: ", link.text)
                WizCrawler.print_link_content(link)
            count+=1
        return

    @classmethod
    def move_to_next_page(cls):
        WizCrawler.print_list()
        total_tr = WizCrawler.browser.find_elements_by_xpath('/html/body/form[2]/table/tbody/tr[*]')
        page_location = str(len(total_tr) - 2)
        page_table = WizCrawler.browser.find_element_by_xpath('/html/body/form[2]/table/tbody/tr[' + page_location + ']/td/table/tbody/tr/td[2]')
        page_list = page_table.find_elements_by_css_selector('*')
        current_page = page_table.find_element_by_css_selector('b')
        CURRENT_NUMBER = current_page.text
        last_page = page_list.__getitem__(len(page_list) - 1)
        LAST_NUMBER = last_page.text
        print('page:', CURRENT_NUMBER + '/' + LAST_NUMBER)
        if(LAST_NUMBER !='[다음]' and CURRENT_NUMBER==LAST_NUMBER):
            print("END OF PAGE")
        else:
            current_item_count = page_list.index(current_page)
            next_page = page_list.__getitem__(current_item_count+1)
            next_page.click()
            time.sleep(5)
            WizCrawler.move_to_next_page()
        return

    @classmethod
    def print_link_content(cls,a):
        a.click()
        time.sleep(5)
        content_div =WizCrawler.browser.find_element_by_xpath('//*[@id="contentsDiv"]')
        print('<content>\n',content_div.text)
        WizCrawler.browser.execute_script("window.history.go(-1)")
        time.sleep(5)
        return

    @staticmethod
    def crawl_site(url):
        WizCrawler.browser.get(url)
        time.sleep(5)
        WizCrawler.move_to_next_page()

        return

    @staticmethod
    def quit():
        WizCrawler.browser.quit()
        return


crawler = WizCrawler()
domain_name='csweb'
home_id='cs'
handle=str(1)
url='http://'+domain_name+'.sookmyung.ac.kr/wiz/contents/board/board.php?home_id='+home_id+'&handle='+handle
crawler.crawl_site(url)