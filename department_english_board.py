from selenium import webdriver

def submit(href):
    #browser.execute_script("return "+href)
    #browser.find_element_by_xpath("//a[@href=\"javascript:page_link('" + str(count) + "')\"]").click()
    browser.find_element_by_xpath("//a[@href=\""+href+"\"]").click()
    return;
#urllib.error.URLError: <urlopen error [Errno 111] Connection

url = 'http://english.sookmyung.ac.kr/wiz/contents/board/board.php?home_id=english&handle=3'
browser = webdriver.PhantomJS()
browser.implicitly_wait(3)
browser.get(url)
