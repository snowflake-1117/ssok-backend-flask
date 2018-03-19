from gensim.models import word2vec

class W2V:
    model = word2vec.Word2Vec.load("whole.model")

    @classmethod
    def get_similar_words(cls, target_word):
        try:
            results = cls.model.most_similar(positive=[target_word])[0:4]
            return results
        except Exception as e:
            return None
