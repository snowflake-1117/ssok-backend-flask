from DBManager import DBManager
from SnoweCrawler import SnoweCrawler
from json_reader import read_wiz

class Main:
    def __init__(self):
        DBManager()
        return

Main()
crawler = SnoweCrawler()
crawler.check_out_process()
crawler.check_out_finished()