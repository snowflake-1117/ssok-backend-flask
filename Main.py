from UnivDBManager import UnivDBManager
from DepartmentDBManager import DepartmentDBManager
from json_reader import read_wiz

class Main:
    def __init__(self):
        manager = UnivDBManager()
        manager = DepartmentDBManager()
        return

start = Main()
read_wiz()