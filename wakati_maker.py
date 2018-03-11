import codecs
from konlpy.tag import Twitter

class WakatiMaker:

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

    def do_snowe2vec(self, file_name, wakati_name):
        text = self.read_file(file_name)
        results = self.parse(text)
        wakati_name = self.make_wakati(results, wakati_name)
        return wakati_name

