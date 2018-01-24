from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def jf_view(href):
    browser.execute_script("return "+href)
    return;


url = 'http://english.sookmyung.ac.kr/wiz/contents/board/board.php?home_id=english&handle=3'
browser = webdriver.PhantomJS()
browser.implicitly_wait(3)
browser.get(url)
browser.quit()