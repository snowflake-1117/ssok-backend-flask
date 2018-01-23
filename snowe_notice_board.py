from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

def printPage(url):
    browser = webdriver.PhantomJS()
    browser.implicitly_wait(3)
    browser.get(url)

    article = browser.find_element_by_css_selector('div.article')
    pList = article.find_elements_by_tag_name('p')

    content = ""
    for p in pList:
        if p.text:
            content = content + p.text + '\n'
    print(content)
    return;
