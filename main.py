from MainNotice import MainNotice
from Wiz5Departments import Wiz5Departments
from DBManager import DBManager


class Main:
    def __init__(self):
        DBManager()
        return


start = Main()

main_notice = MainNotice()
main_notice.start()
main_notice.quit()

wiz5_department = Wiz5Departments()
wiz5_department.start()
wiz5_department.quit()
