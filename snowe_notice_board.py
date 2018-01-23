import bs4 as bs
import urllib.request

def printPage(url):
    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce,'lxml')
    spans = soup.find_all('span')

    for item in spans:
        print(item.text)
    return;
