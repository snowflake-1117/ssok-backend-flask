# -*-coding:utf-8-*-
from app import app
import json
from app.crawlers.DBManager import DBManager


@app.route('/')
def index():
    return 'Sookpam main page'


@app.route('/<category_name>/<division_name>')
def get_major_category(category_name, division_name):
    record_list = DBManager.select_category_and_division_of('%s' % category_name, '%s' % division_name)
    json_dictionary = []
    for record in record_list:
        json_dictionary.append(
            {"category": record.category, "division": record.division, 'id': record.id, 'title': record.title,
             'content': record.content, 'view': record.view,
             'date': record.date,
             'url': record.url})
    json_data = json.dumps(json_dictionary, ensure_ascii=False)
    return ''.join(json_data)
