# -*-coding:utf-8-*-
from app import app
import json
from app.crawlers.DBManager import DBManager
from app.crawlers.Wiz5DepartmentsCrawler import Wiz5DepartmentsCrawler


@app.route('/')
def index():
    db_manager = DBManager()
    wiz5_department = Wiz5DepartmentsCrawler()
    wiz5_department.start()
    wiz5_department.quit()
    record_list = db_manager.select_all()
    json_dictionary = []
    for record in record_list:
        json_dictionary.append({record.category: {record.division: {'id': record.id, 'title': record.title,
                                                                    'content': record.content, 'view': record.view,
                                                                    'date': record.date,
                                                                    'url': record.url}}})
    json_data = json.dumps(json_dictionary, ensure_ascii=False)
    return ''.join(json_data)
