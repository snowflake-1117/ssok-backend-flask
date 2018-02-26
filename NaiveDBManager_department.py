from pymysql.err import InternalError
import pymysql.cursors

class DBManager:
    USER = YOUR_USER
    PW = YOUR_PW

    @staticmethod
    def selectTrainData():
        rows = []
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            categoryList = DBManager.getTrainCategoryList()
            sql = "select title, division, category from univ where "
            for category in categoryList:
                sql = sql +  "category='"+ category[0] +"' or "
            sql = sql[:len(sql)-4]
            print("sql_train:", sql)
            cursor.execute(sql)
            conn.commit()
            result = cursor.fetchall()
            for row in result:
                rows.append(row)
        return rows

    @staticmethod
    def getTrainCategoryList():
        rows = []
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = " select distinct(category) from univ "
            sql = sql + "group by category "
            sql = sql + "having count(distinct(division))>1;"
            cursor.execute(sql)
            conn.commit()
            result = cursor.fetchall()
            for row in result:
                rows.append(row)
        return rows

    @staticmethod
    def selectTestData():
        rows = []
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            categoryList = DBManager.getTestCategoryList()
            sql = "select title, division, category from univ where "
            for category in categoryList:
                sql = sql + "category='" +  category[0] + "' or "

            sql = sql[:len(sql) - 4]
            print("sql_train:",sql)
            cursor.execute(sql)
            conn.commit()
            result = cursor.fetchall()
            for row in result:
                rows.append(row)
        return rows

    @staticmethod
    def getTestCategoryList():
        rows = []
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = " select distinct(category) from univ "
            sql = sql + "group by category "
            sql = sql + "having count(distinct(division))=1;"
            cursor.execute(sql)
            conn.commit()
            result = cursor.fetchall()
            for row in result:
                rows.append(row)
        return rows


    @staticmethod
    def updateAt(title, division):
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