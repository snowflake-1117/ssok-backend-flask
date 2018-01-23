import bs4 as bs
import urllib.request

sauce = urllib.request.urlopen('https://snowe.sookmyung.ac.kr/bbs5/boards/notice/1105825?boardKey=1&sort=sequence&order=desc&rows=20&messageCategoryKey=1&pageNumber=1&viewType=noticeGeneric&targetType=12&targetKey=1&status=&period=&startdt=&enddt=&queryField=&query=&validDateType=&processStatusType=&boardDiv=').read()
soup = bs.BeautifulSoup(sauce,'lxml')

#print(soup.find_all('tr'))
spans = soup.find_all('span')

for item in spans:
    print(item.text)