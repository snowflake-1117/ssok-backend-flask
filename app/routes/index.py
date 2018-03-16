# -*-coding:utf-8-*-
from app import app
import json
from app.crawlers.DBManager import DBManager
from RecommendCondition import RecommendCondition
from RecommendHelper import RecommendHelper
import RelevantContentCommender

@app.route('/')
def index():
    return 'Ssok main page'


@app.route('/공통/취업')
def get_career_list():
    record_list = DBManager.select_category_of("취업")
    json_dictionary = []
    for record in record_list:
        json_dictionary.append(
            {"category": record.category, "division": record.division, 'id': record.id, 'title': record.title,
             'content': record.content, 'view': record.view,
             'date': record.date, 'url': record.url, 'attach': record.attach})
    json_data = json.dumps(json_dictionary, ensure_ascii=False)
    return ''.join(json_data)


@app.route('/<category_name>/<division_name>')
def get_major_category_list(category_name, division_name):
    record_list = DBManager.select_category_and_division_of(category_name, division_name)
    json_dictionary = []
    for record in record_list:
        json_dictionary.append(
            {"category": record.category, "division": record.division, 'id': record.id, 'title': record.title,
             'content': record.content, 'view': record.view,
             'date': record.date, 'url': record.url, 'attach': record.attach})
    json_data = json.dumps(json_dictionary, ensure_ascii=False)
    return ''.join(json_data)


@app.route('/search/<words>')
def get_search_list_by_words(words):
    search_list = DBManager.select_search_by(words)
    json_dictionary = []
    if search_list is None:
        return ''
    for record in search_list:
        json_dictionary.append(
            {"category": record.category, "division": record.division, 'id': record.id, 'title': record.title,
             'content': record.content, 'view': record.view, 'date': record.date, 'url': record.url,
             'attach': record.attach})
    json_data = json.dumps(json_dictionary, ensure_ascii=False)
    return ''.join(json_data)


@app.route('/recommend/student_grade=<student_grade>&'
           'student_year=<student_year>&'
           'majors=<majors>&'
           'school_scholar=<school_scholar>&'
           'government_scholar=<government_scholar>&'
           'external_scholar=<external_scholar>&'
           'student_status=<student_status>&'
           'interest_scholarship=<interest_scholarship>&'
           'interest_academic=<interest_academic>&'
           'interest_event=<interest_event>&'
           'interest_recruit=<interest_recruit>&'
           'interest_system=<interest_system>&'
           'interest_global=<interest_global>&'
           'interest_career=<interest_career>&'
           'interest_student=<interest_student>')
def get_10_recommend_list(student_grade, student_year,
                          majors, school_scholar,
                          government_scholar, external_scholar, student_status,
                          interest_scholarship, interest_academic, interest_event, interest_recruit,
                          interest_system, interest_global, interest_career, interest_student):
    recommend_condition = RecommendCondition(student_grade, student_year,
                                             majors, school_scholar,
                                             government_scholar, external_scholar, student_status,
                                             interest_scholarship, interest_academic, interest_event,
                                             interest_recruit,
                                             interest_system, interest_global, interest_career, interest_student)
    print("interest_scholarship: ", interest_scholarship)
    db_manager = DBManager()
    recommend_helper = RecommendHelper()
    filtered_record_list = db_manager.select_recommend_list_by(recommend_condition)
    selected_record_list = recommend_helper.select_recommend_list_from(filtered_record_list, recommend_condition)
    json_dictionary = []
    for selected_item in selected_record_list:
        json_dictionary.append(
            {"category": selected_item.record.category, "division": selected_item.record.division,
             'id': selected_item.record.id, 'title': selected_item.record.title,
             'content': selected_item.record.content, 'view': selected_item.record.view,
             'date': selected_item.record.date, 'url': selected_item.record.url, 'attach': selected_item.record.attach})
    json_data = json.dumps(json_dictionary, ensure_ascii=False)
    return ''.join(json_data)


@app.route('/ngram/<title>')
def get_ngram_results(title):
    ngram_result_list = RelevantContentCommender.compare_with(title.replace('-', ' ').replace('__', '/'), DBManager.select_all_titles(title))
    json_dictionary = []
    if ngram_result_list is None:
        return ''
    for record in ngram_result_list:
        json_dictionary.append(
            {"category": record.category, "division": record.division, 'id': record.id, 'title': record.title,
             'content': record.content, 'view': record.view, 'date': record.date, 'url': record.url,
             'attach': record.attach})
    json_data = json.dumps(json_dictionary, ensure_ascii=False)
    return ''.join(json_data)
