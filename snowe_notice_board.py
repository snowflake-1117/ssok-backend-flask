from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

def printPage(url):
    browser = webdriver.PhantomJS()
    browser.implicitly_wait(3)
    browser.get(url)

    article = browser.find_element_by_css_selector('div.article')
    try:
        img = article.find_element_by_tag_name("img")
        print(img.get_attribute(img))
    except WebDriverException:
        print(article.text)
    except NoSuchElementException:
        print(article.text)
    return;
