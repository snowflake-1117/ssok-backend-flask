# -*-coding:utf-8-*-
from app import app
import json
from app.crawlers.DBManager import DBManager
from RecommendCondition import RecommendCondition


@app.route('/')
def index():
    return 'Sookpam main page'


@app.route('/<category_name>/<division_name>')
def get_major_category(category_name, division_name):
    record_list = DBManager.select_category_and_division_of(category_name, division_name)
    json_dictionary = []
    for record in record_list:
        json_dictionary.append(
            {"category": record.category, "division": record.division, 'id': record.id, 'title': record.title,
             'content': record.content, 'view': record.view,
             'date': record.date,
             'url': record.url})
    json_data = json.dumps(json_dictionary, ensure_ascii=False)
    return ''.join(json_data)


@app.route('/recommend/student_grade=<student_grade>&'
           'student_year=<student_year>&'
           'major1=<major1>&major2=<major2>&'
           'school_scholar=<school_scholar>&'
           'government_scholar=<government_scholar>&'
           'external_scholar=<external_scholar>&'
           'student_status=<student_status>&'
           'interest_scholarship=<interest_scholarship>&'
           'interest_academic=<interest_academic>&'
           'interest_entrance=<interest_entrance>&'
           'interest_recruit=<interest_recruit>&'
           'interest_system=<interest_system>&'
           'interest_global=<interest_global>&'
           'interest_career=<interest_career>&'
           'interest_student=<interest_student>')
def get_10_recommend_contents(student_grade, student_year,
                              major1, major2, school_scholar,
                              government_scholar, external_scholar, student_status,
                              interest_scholarship, interest_academic, interest_entrance, interest_recruit,
                              interest_system, interest_global, interest_career, interest_student):
    recommend_condition = RecommendCondition(student_grade, student_year,
                                             major1, major2, school_scholar,
                                             government_scholar, external_scholar, student_status,
                                             interest_scholarship, interest_academic, interest_entrance,
                                             interest_recruit,
                                             interest_system, interest_global, interest_career, interest_student)
    record_list = DBManager.select_recommend_list_by(recommend_condition)
    json_dictionary = []
    for record in record_list:
        json_dictionary.append(
            {"category": record.category, "division": record.division, 'id': record.id, 'title': record.title,
             'content': record.content, 'view': record.view,
             'date': record.date,
             'url': record.url})
    json_data = json.dumps(json_dictionary, ensure_ascii=False)
    return ''.join(json_data)
