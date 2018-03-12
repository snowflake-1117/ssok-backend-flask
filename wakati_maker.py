import codecs
import pymysql
from konlpy.tag import Twitter
from app.crawlers.DBManager import DBManager

class WakatiMaker:

    def make_file(self, category, division, file_name):
        conn = pymysql.connect(host='localhost',
                               user=DBManager.USER,
                               password=DBManager.PW,
                               db='sookmyung',
                               charset='utf8mb4')
        with conn.cursor() as cursor:
            sql = 'select title from univ where category=\''+category+'\' AND division=\''+division+'\' into outfile \''+file_name+'\';'
            cursor.execute(sql)
        conn.commit()
        print(cursor.rowcount)
        return

    def read_file(self, file_name):
        text = ""
        fp = codecs.open(file_name, "r", encoding="utf-8")
        while True:
            line = fp.readline()
            text = text + line
            if not line: break
        fp.close()
        return text

    def parse(self, text):
        results = []
        twitter = Twitter()
        lines = text.split("\n")
        for line in lines:
            malist = twitter.pos(line, norm=True, stem=True)
            r = []
            for word in malist:
                if not word[1] in ["Josa", "Eomi", "Punctuation"]:
                    r.append(word[0])
            rl = (" ".join(r).strip())
            results.append(rl)
        return results

    def make_wakati(self, results, wakati_name):
        with open(wakati_name, 'w', encoding="utf-8") as fp:
            fp.write("\n".join(results))
        return wakati_name

    def do_snowe2vec(self, category, division, file_name, wakati_name):
        self.make_file(category, division, file_name)
        text = self.read_file(file_name)
        results = self.parse(text)
        wakati_name = self.make_wakati(results, wakati_name)
        return wakati_name

