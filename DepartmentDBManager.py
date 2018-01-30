import pymysql.cursors


class DepartmentDBManager:
    USER = YOUR_USER
    PW = YOUR_PW

    def __init__(self):
        DepartmentDBManager.create_department()
        return

    @staticmethod
    def create_department():
        conn = pymysql.connect(host='localhost',
                               user=DepartmentDBManager.USER,
                               password=DepartmentDBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = '''
                    CREATE TABLE IF NOT EXISTS department( 
                    id int(11) NOT NULL,
                    large_category varchar(50) NOT NULL,
                    small_category varchar(50) NOT NULL, 
                    title varchar(200) NOT NULL,
                    content varchar(13000) 
                   ) ENGINE=InnoDB DEFAULT CHARSET=utf8
            '''
            cursor.execute(sql)
            conn.commit()
        return

    @staticmethod
    def insert(id, large_category, small_category, title, content):
        conn = pymysql.connect(host='localhost',
                               user=DepartmentDBManager.USER,
                               password=DepartmentDBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'INSERT INTO department (id, large_category, small_category, title, content) VALUES (%s,%s,%s,%s,%s)'
            cursor.execute(sql, (str(id), large_category, small_category, title, content))
        conn.commit()
        # 1 (last insert id)
        return

    @staticmethod
    def select():
        conn = pymysql.connect(host='localhost',
                               user=DepartmentDBManager.USER,
                               password=DepartmentDBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'SELECT * FROM department'
            cursor.execute(sql)
            conn.commit()
            result = cursor.fetchall()
            for row in result:
                print(row)
            # (1, 'test@test.com', 'my-passwd')
        return

    @staticmethod
    def delete_all():
        conn = pymysql.connect(host='localhost',
                               user=DepartmentDBManager.USER,
                               password=DepartmentDBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')

        with conn.cursor() as cursor:
            sql = 'DELETE FROM department'
            cursor.execute(sql)
            conn.commit()
        return