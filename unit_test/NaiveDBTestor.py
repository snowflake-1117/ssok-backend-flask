import unittest

import pymysql

from NaiveDBManager_department import DBManager


class DBTestor(unittest.TestCase):
    def setUp(self):
        string = "hello it's a great day at 'sookmyung'"
        string.replace("\'","\'\'")
        string.replace("\"","\"\"")
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            categoryList = DBManager.getTrainCategoryList()
            sql = "insert into univ (id,category,division,title) values (10000,'테스트','테스트',"+str+")"
            cursor.execute(sql)
            conn.commit()

    def checkDoubledQuotes(self):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = " select title from univ where id=10000"
            cursor.execute(sql)
            conn.commit()
            result = cursor.fetchone()
        self.assertEqual(result[0],str)

    def tearDown(self):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = " delete from univ where id=10000;"
            cursor.execute(sql)
            conn.commit()
            result = cursor.fetchone()
        return result
        pass