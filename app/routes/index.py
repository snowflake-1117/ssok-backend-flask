from app import app
from app.crawlers.DBManager import DBManager
from app.crawlers.Wiz5DepartmentsCrawler import Wiz5DepartmentsCrawler


@app.route('/')
def index():
    db_manager = DBManager()
    wiz5_department = Wiz5DepartmentsCrawler()
    wiz5_department.start()
    wiz5_department.quit()
    title_list = db_manager.select_all_titles()
    return ''.join(title_list)
