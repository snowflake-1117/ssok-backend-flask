from bs4 import BeautifulSoup
import urllib.request as request


def print_page(url):
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html,'lxml')
    article = soup.select_one('div.article')
    p_list = article.find_all('p')
    imgs = article.findAll('img')
    content = ""
    if imgs:
        print('img:\n', "\n".join(set(tag['src'] for tag in imgs)))
    elif p_list:
        for p in p_list:
            if p.text:
                content = content + p.text + '\n'
        print('content:\n',content+'\n')
    else:
        board = article.select_one('div#_ckeditorContents')
        content = board.text
        print('content:\n',content+'\n')

    return content

