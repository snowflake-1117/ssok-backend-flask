# -*-coding:utf-8-*-
from app import app
import json
from app.crawlers.DBManager import DBManager


@app.route('/')
def index():
    record_list = DBManager.select_all()
    json_dictionary = []
    for record in record_list:
        json_dictionary.append({record.category: {record.division: {'id': record.id, 'title': record.title,
                                                                    'content': record.content, 'view': record.view,
                                                                    'date': record.date,
                                                                    'url': record.url}}})
    json_data = json.dumps(json_dictionary, ensure_ascii=False)
    return ''.join(json_data)
