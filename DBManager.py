from pymysql.err import InternalError
import pymysql.cursors

class DBManager:
    USER = YOUR_USER
    PW = YOUR_PW

    @staticmethod
    def insert(record):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'INSERT INTO univ (id, category, division, title, content,view,date) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql, (record.id, record.category, record.division, record.title, record.content,record.view,record.date))
        conn.commit()
        return

    @staticmethod
    def selectEach20():
        rows = []
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            divisions = ["공지","학사","장학","행사","모집","학생"]
            sql=""
            for division in divisions:
                sql = sql + "(select title, division from univ where division = '"+division+"' order by view limit 20) union all"
            sql = sql + "(select title, division from univ where division ='시스템' order by view limit 20)"
            cursor.execute(sql)
            conn.commit()
            result = cursor.fetchall()
            for row in result:
                rows.append(row)
        return rows

    @staticmethod
    def selectALL():
        rows = []
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'SELECT title, division FROM univ'
            cursor.execute(sql)
            conn.commit()
            result = cursor.fetchall()
            for row in result:
                rows.append(row)
        return rows

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