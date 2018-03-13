from pymysql.err import InternalError
import pymysql.cursors

class DBManager:
    USER = YOUR_USER
    PW = YOUR_PW

    @staticmethod
    def updateAt(title, division):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = "update univ set division=%s where title=%s;"
            cursor.execute(sql, (division, title))
            conn.commit()
        return