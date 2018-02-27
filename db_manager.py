from pymysql.err import InternalError
import pymysql.cursors

class DBManager:
    USER = YOUR_USER
    PW = YOUR_PW

    @staticmethod
    def updateAt(title, division):
        title.replace("\'","\'\'")
        title.replace("\"", "\"\"")
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = " update univ "
            sql = sql + "set division='"+division+"' "
            sql = sql + "where title='"+title+"';"
            cursor.execute(sql)
            conn.commit()
        return