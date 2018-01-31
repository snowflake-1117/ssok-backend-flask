from MainNotice import MainNotice
from Wiz5Departments import Wiz5Departments
from UnivDBManager import UnivDBManager
from DBManager import DBManager
from DepartmentDBManager import DepartmentDBManager


class Main:
    def __init__(self):
        UnivDBManager()
        DepartmentDBManager()
        return


start = Main()

main_notice = MainNotice()
main_notice.start()
main_notice.quit()

wiz5_department = Wiz5Departments()
wiz5_department.start()
wiz5_department.quit()
