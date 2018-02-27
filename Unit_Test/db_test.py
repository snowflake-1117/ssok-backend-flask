from db_manager import DBManager
import unittest
import pymysql.cursors


class DB_Testor(unittest.TestCase):
    def setUp(self):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = " Insert into univ (id, category,division,title) values (10000,'공통','공지','테스트 라인 입니다.');"
            cursor.execute(sql)
            conn.commit()
        return

    def selectDivisionByTitle(self):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = " SELECT division from univ where title='테스트 라인 입니다.';"
            cursor.execute(sql)
            conn.commit()
            result = cursor.fetchone()
        return result

    def tearDown(self):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = " delete from univ where title='테스트 라인 입니다.';"
            cursor.execute(sql)
            conn.commit()
            result = cursor.fetchone()
        return result
        pass

    def test_db_update(self):
        DBManager.updateAt("테스트 라인 입니다.", "장학")
        result = DB_Testor.selectDivisionByTitle(self)
        self.assertEqual("장학",result[0])
