from app import app
from app.crawlers import *


@app.route('/')
def index():
    DBManager()
    wiz5_department = Wiz5DepartmentsCrawler()
    wiz5_department.start()
    wiz5_department.quit()
    return 'Hello world'
