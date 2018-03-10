#-*-coding:utf-8-*-
import pymysql.cursors

class DBManager:
    USER = "root"
    PW = ""

    @staticmethod
    def isDepartment(category):
        return category != "공통" and category != "취업" and category != "국제"

    @staticmethod
    def isDepartmentAlreadyDivided(category):
        return category != "중어중문학부" and category != "일본학과" and category != "프랑스언어문화학과" \
               and category != "한국어문학부" and category != "문화관광학전공" and category != "수학과" \
               and category != "아동복지학부" and category != "법학부" and category != "경영학부" and category != "영어영문학부" \
               and category != "교육학부" and category != "화학과" and category != "생명시스템학부" and category != "무용과" \
               and category != "IT공학전공" and category != "의류학과" and category != "회화과"

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
                if DBManager.isDepartment(category[0]):
                    sql = sql + "category='" + category[0] + "' or "
            sql = sql[:len(sql) - 4]
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
            if len(categoryList) > 0:
                sql = "select title, division, category from univ where "
                for category in categoryList:
                    if DBManager.isDepartment(category):
                        sql = sql + "category='" +  category + "' or "

                sql = sql[:len(sql) - 4]
                print("sql_test:", sql)
                cursor.execute(sql)
                conn.commit()
                result = cursor.fetchall()
                for row in result:
                    rows.append(row)
            else:
                print("sql_test:", "already classified data")
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
