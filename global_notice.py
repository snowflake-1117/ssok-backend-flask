from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://cms.sookmyung.ac.kr/wiz5/contents/board/board_action.php?home_id=exchange&handle=7&page=4&scale=15&categoryId=1&categoryDepth=&parent=')


element_list = browser.find_elements_by_css_selector('#board-container > div.list > form > table > tbody > tr > td.title > a')
url_list = [element_list[i].get_attribute("href") for i in range(3, len(element_list))]

for url in url_list:
    browser.implicitly_wait(3)
    browser.get(url)
    title = browser.find_element_by_class_name('tit').text
    content = browser.find_element_by_id('contentsDiv').text
    print(title)
    print(content)


""""
current_list_page = browser.current_url

next_page = browser.find_element_by_css_selector('#board-container > div.list > div.leftBtn > div > a').get_attribute('href')


for title in listbody:
    title = title.text
    print(title)


browser.find_element_by_name('id').send_keys('solitarius')
browser.find_element_by_name('pw').send_keys('@navEl01')
browser.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

url = "http://cms.sookmyung.ac.kr/wiz5/contents/board/board_action.php?home_id=exchange&command=list&listhome_id=exchange&listhandle=7&handle=7&board_id=7"
res = urlopen(url)
soup = BeautifulSoup(res, "html.parser")

titleList = soup.findAll('a')

for title in titleList:
    title = title.getText()
    print(title)
"""""