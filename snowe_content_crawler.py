from bs4 import BeautifulSoup
import urllib.request as request


def print_page(url):
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html,'lxml')
    article = soup.select_one('div.article')
    p_list = article.find_all('p')
    content = ""
    if p_list:
        for p in p_list:
            if p.text:
                content = content + p.text + '\n'
    else:
        board = article.select_one('div#_ckeditorContents')
        content = board.text
    content = ' '.join(content.split())
    return content

