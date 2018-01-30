from DBManager import DBManager
from SnoweCrawler import SnoweCrawler

class Main:
    def __init__(self):
        manager = DBManager()
        return

    def crawl_snowe_notice(self):
        crawler = SnoweCrawler()
        crawler.crawl_pages()
        return

start = Main()
start.crawl_snowe_notice()