from pymysql.err import InternalError
import pymysql.cursors

class DBManager:
    YOUR_USER = 'admin'
    YOUR_PW = '2846'
    USER = YOUR_USER
    PW = YOUR_PW

    @staticmethod
    def isDepartment(category):
        return category != "공통" and category != "취업" and category!="국제"

    @staticmethod
    def selectClassifiedData():
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
                if DBManager.isDepartment(category[0]):
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
    def reset_test_data_division():
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            categoryList = DBManager.getTestCategoryList()
            sql = "update univ set division='취업' where "
            for category in categoryList:
                sql = sql + "category='" + category + "' or "

            sql = sql[:len(sql) - 4]
            print("sql_test:", sql)
            cursor.execute(sql)
            conn.commit()


    @staticmethod
    def selectUnclassifiedData():
        rows = []
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            categoryList = DBManager.getTestCategoryList()
            if len(categoryList) > 0 :
                sql = "select title, division, category from univ where "
                for category in categoryList:
                    if DBManager.isDepartment(category):
                        sql = sql + "category='" +  category + "' or "

                sql = sql[:len(sql) - 4]
                print("sql_test:",sql)
                cursor.execute(sql)
                conn.commit()
                result = cursor.fetchall()
                for row in result:
                    rows.append(row)
            else :
                print("sql_test:","already classified data")
        return rows

    @staticmethod
    def getTestCategoryList():
        rows = ["역사문화학과", "독일언어문화학과", "프랑스언어문화학과", "문헌정보학과", "체육교육과", "응용물리전공", "소프트웨어학부",
                "식품영양학과", "정치외교학과", "행정학과", "환경디자인학과", "글로벌서비스학부", "테슬", "화학과", "생명시스템학부", "회화과"
                , "무용과", "화공생명학부", "전자공학전공", "기계시스템학부", "가족자원경영학과", "소비자경제학과", "미디어학부", "약햑대학"]
        return rows


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