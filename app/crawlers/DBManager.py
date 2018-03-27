import pymysql.cursors
from pymysql.err import InternalError
from .Record import Record
from RecommendHelper import RecommendHelper
import os


class DBManager:
    USER = "root"

    def __init__(self):
        DBManager.createDB()
        DBManager.createWeb()
        return

    @staticmethod
    def createDB():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               charset='utf8mb4')
        try:
            with conn.cursor() as cursor:
                sql = 'USE sookmyung'
                cursor.execute(sql)
        except InternalError:
            with conn.cursor() as cursor:
                sql = 'CREATE DATABASE IF NOT EXISTS sookmyung'
                cursor.execute(sql)
        finally:
            conn.commit()
        return

    @staticmethod
    def createWeb():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = '''
                       CREATE TABLE IF NOT EXISTS web( 
                        id int(11) NOT NULL,
                        category varchar(50) NOT NULL,
                        division varchar(50) NOT NULL, 
                        title varchar(200) NOT NULL,
                        content MEDIUMTEXT ,
                        view int(10),
                        date Date,
                        url varchar(500),
                        attach varchar(10000),
                        db_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
                '''
            cursor.execute(sql)
        return

    @staticmethod
    def insert(record):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'INSERT INTO web (id, category, division, title, content, view, date, url, attach) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);'
            cursor.execute(sql, (
                record.id, record.category, record.division, record.title, record.content, record.view, record.date,
                record.url, record.attach))
        conn.commit()
        return

    @staticmethod
    def select():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'SELECT * FROM web'
            cursor.execute(sql)
            conn.commit()
            result = cursor.fetchall()
            for row in result:
                print(row)
        return

    @staticmethod
    def select_category_and_division_of(category, division):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'SELECT * FROM web WHERE category=%s AND division=%s ORDER BY date DESC'
            cursor.execute(sql, (category, division))
            conn.commit()
            results = cursor.fetchall()
            record_list = []
            for result in results:
                record = Record()
                record.db_id = str(result[0])
                record.id = str(result[1])
                record.category = str(result[2])
                record.division = str(result[3])
                record.title = str(result[4])
                record.content = str(result[5])
                record.view = str(result[6])
                record.date = str(result[7])
                record.url = str(result[8])
                record.attach = str(result[9])
                record_list.append(record)
        return record_list

    @staticmethod
    def select_category_of(category):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'SELECT * FROM web WHERE category=%s ORDER BY date DESC'
            cursor.execute(sql, category)
            conn.commit()
            results = cursor.fetchall()
            record_list = []
            for result in results:
                record = Record()
                record.db_id = str(result[0])
                record.id = str(result[1])
                record.category = str(result[2])
                record.division = str(result[3])
                record.title = str(result[4])
                record.content = str(result[5])
                record.view = str(result[6])
                record.date = str(result[7])
                record.url = str(result[8])
                record.attach = str(result[9])
                record_list.append(record)
        return record_list

    @staticmethod
    def select_recommend_list_by(recommend_condition):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'SELECT * FROM web WHERE '
            recommend_helper = RecommendHelper()
            sql = recommend_helper.add_date_condition_within_7days(sql)
            sql = recommend_helper.add_category_and_division_condition(recommend_condition, sql)
            sql += ' ORDER BY date DESC;'
            cursor.execute(sql)
            conn.commit()
            results = cursor.fetchall()
            record_list = []
            for result in results:
                record = Record()
                record.db_id = str(result[0])
                record.id = str(result[1])
                record.category = str(result[2])
                record.division = str(result[3])
                record.title = str(result[4])
                record.content = str(result[5])
                record.view = str(result[6])
                record.date = str(result[7])
                record.url = str(result[8])
                record.attach = str(result[9])
                record_list.append(record)
        return record_list

    @staticmethod
    def is_notice_url_already_saved(url):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')
        with conn.cursor() as cursor:
            sql = 'SELECT url FROM web WHERE url=%s'
            cursor.execute(sql, url)
            conn.commit()
            result = cursor.fetchall()
            if result.__len__() > 0:
                return True
            else:
                return False

    @staticmethod
    def is_notice_already_saved(title, category):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')
        with conn.cursor() as cursor:
            sql = 'SELECT title FROM web WHERE title=%s AND category=%s'
            cursor.execute(sql, (title, category))
            conn.commit()
            result = cursor.fetchall()
            if result.__len__() > 0:
                return True
            else:
                return False

    @staticmethod
    def delete_all():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'DELETE FROM web'
            cursor.execute(sql)
            conn.commit()
        return

    @staticmethod
    def delete_duplicated_rows():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')
        with conn.cursor() as cursor:
            sql = 'delete u1 from web u1, web u2 where u1.db_id < u2.db_id ' \
                  'and u1.title=u2.title and u1.content=u2.content ' \
                  'and u1.category=u2.category and u1.division=u2.division and u1.date=u2.date;'
            cursor.execute(sql)
        conn.commit()
        return

    @classmethod
    def select_search_by(cls, words):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'SELECT * FROM web WHERE '
            for index, word in enumerate(words):
                if index < len(words) - 1:
                    sql += '(title LIKE ' + '\"%' + word + '%\") AND '
                else:
                    sql += '(title LIKE ' + '\"%' + word + '%\") ORDER BY date DESC;'
            cursor.execute(sql)
            conn.commit()
            results = cursor.fetchall()
            record_list = []
            for result in results:
                record = Record()
                record.db_id = str(result[0])
                record.id = str(result[1])
                record.category = str(result[2])
                record.division = str(result[3])
                record.title = str(result[4])
                record.content = str(result[5])
                record.view = str(result[6])
                record.date = str(result[7])
                record.url = str(result[8])
                record.attach = str(result[9])
                record_list.append(record)
        return record_list

    @staticmethod
    def select_all_titles(title):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'SELECT DISTINCT title FROM web WHERE title!=%s;'
            cursor.execute(sql, title)
            conn.commit()
            results = cursor.fetchall()
            title_list = []
            for result in results:
                if result[0] != title:
                    title_list.append(str(result[0]))
        return title_list

    @staticmethod
    def select_max_list(title_list):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'SELECT * FROM web WHERE title=%s or title=%s;'
            cursor.execute(sql, (title_list[0].subject_line, title_list[1].subject_line))
            conn.commit()
            results = cursor.fetchall()
            record_list = []
            for result in results:
                record = Record()
                record.db_id = str(result[0])
                record.id = str(result[1])
                record.category = str(result[2])
                record.division = str(result[3])
                record.title = str(result[4])
                record.content = str(result[5])
                record.view = str(result[6])
                record.date = str(result[7])
                record.url = str(result[8])
                record.attach = str(result[9])
                record_list.append(record)
        return record_list[0:2]

    @staticmethod
    def update_at(title, division):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = "update web set division=%s where title=%s;"
            cursor.execute(sql, (division, title.replace("\n", "")))
            conn.commit()
        return

    @staticmethod
    def make_file(category, division, file_name):
        os.chdir("/var/lib/mysql")
        if os.path.isfile(file_name):
            os.remove(file_name)
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')
        with conn.cursor() as cursor:
            sql = 'select title from web where category=%s AND division=%s into outfile %s;'
            cursor.execute(sql, (category, division, file_name))
        conn.commit()
        print(cursor.rowcount)
        return

    @classmethod
    def get_clipped_records(cls, id_list):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'SELECT * FROM web WHERE '
            for index, db_id in enumerate(id_list):
                if index < id_list.__len__() - 1:
                    sql += "db_id=" + db_id + " or "
                else:
                    sql += "db_id=" + db_id + ";"
            cursor.execute(sql)
            conn.commit()
            results = cursor.fetchall()
            record_list = []
            for result in results:
                record = Record()
                record.db_id = str(result[0])
                record.id = str(result[1])
                record.category = str(result[2])
                record.division = str(result[3])
                record.title = str(result[4])
                record.content = str(result[5])
                record.view = str(result[6])
                record.date = str(result[7])
                record.url = str(result[8])
                record.attach = str(result[9])
                record_list.append(record)
        return record_list
