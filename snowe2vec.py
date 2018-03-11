from gensim.models import word2vec
import codecs
from konlpy.tag import Twitter

class Snowe2Vec:

    def get_text(self, file_name):
        fp = codecs.open(file_name, "r", encoding="utf-8")
        while True:
            line = fp.readline()
            text = text + line
            if not line: break
        fp.close()
        return text

    def do_parse(self, text):
        results = ""
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

    def make_model(self, wakati_file, model_name):
        data = word2vec.LineSentence(wakati_file)
        model = word2vec.Word2Vec(data, size=200, window=10, hs=1, min_count=2, sg=1)
        model.save_word2vec_format()
        model.save(model_name)

    def do_snowe2vec(self, file_name, wakati_name, model_name):
        text = self.get_text(file_name)
        results = self.do_parse(text)
        wakati_name = self.make_wakati(results, wakati_name)
        model_name = self.make_model(wakati_name, model_name)
        return wakati_name, model_name