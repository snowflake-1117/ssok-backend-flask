import pymysql.cursors
from pymysql.err import InternalError
from .Record import Record
from RecommendCondition import RecommendCondition


class DBManager:
    USER = "root"
    PW = ""

    def __init__(self):
        DBManager.createDB()
        DBManager.createUniv()
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
    def createUniv():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = '''
                       CREATE TABLE IF NOT EXISTS univ( 
                        id int(11) NOT NULL,
                        category varchar(50) NOT NULL,
                        division varchar(50) NOT NULL, 
                        title varchar(200) NOT NULL,
                        content varchar(20000),
                        view int(10),
                        date Date,
                        url varchar(500)
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
            sql = 'INSERT INTO univ (id, category, division, title, content,view, date, url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql, (
                record.id, record.category, record.division, record.title, record.content, record.view, record.date,
                record.url))
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
            sql = 'SELECT * FROM univ'
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
            sql = 'SELECT DISTINCT * FROM univ WHERE category=%s AND division=%s'
            cursor.execute(sql, (category, division))
            conn.commit()
            results = cursor.fetchall()
            record_list = []
            for result in results:
                record = Record()
                record.id = str(result[0])
                record.category = str(result[1])
                record.division = str(result[2])
                record.title = str(result[3])
                record.content = str(result[4])
                record.view = str(result[5])
                record.date = str(result[6])
                record.url = str(result[7])
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
            sql = 'SELECT DISTINCT * FROM univ ' \
                  'WHERE DATE(date) >= DATE(subdate(now(), INTERVAL 7 DAY)) AND DATE (date) <= DATE(now())' \
                  'ORDER BY date DESC'
            cursor.execute(sql)
            conn.commit()
            results = cursor.fetchall()
            record_list = []
            for result in results:
                record = Record()
                record.id = str(result[0])
                record.category = str(result[1])
                record.division = str(result[2])
                record.title = str(result[3])
                record.content = str(result[4])
                record.view = str(result[5])
                record.date = str(result[6])
                record.url = str(result[7])
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
            sql = 'SELECT url FROM univ WHERE url=%s'
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
            sql = 'SELECT title FROM univ WHERE title=%s AND category=%s'
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
            sql = 'DELETE FROM univ'
            cursor.execute(sql)
            conn.commit()
        return
