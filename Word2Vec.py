from gensim.models import word2vec

class W2V:
    model = word2vec.Word2Vec.load("whole.model")

    def get_similar_words(cls, target_word, number):
        results = cls.model.most_similar(positive=[target_word])[0:number]
        return results