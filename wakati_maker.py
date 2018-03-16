#!/usr/bin/python3
# -*-coding:utf-8-*-
import codecs
from konlpy.tag import Twitter
from app.crawlers.DBManager import DBManager


class WakatiMaker:
    previous_file_result = []

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
        if wakati_name != 'data/job/job_gongji.wakati' and wakati_name != 'data/snowe/snowe_gongji.wakati':
            with open("/home/ubuntu/sookpam-backend-flask/" + wakati_name, 'r', encoding="utf-8") as fp:
                self.previous_file_result = fp.read().split('\n')
            all_results = results + self.previous_file_result
        else:
            all_results = results
        with open("/var/lib/mysql/"+wakati_name, 'w', encoding="utf-8") as fp:
            fp.write("\n".join(all_results))

    def do_snowe2vec(self, category, division, file_name, wakati_name):
        DBManager.make_file(category, division, file_name)
        text = self.read_file(file_name)
        results = self.parse(text)
        self.make_wakati(results, wakati_name)
