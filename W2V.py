from gensim.models import word2vec

global model
class W2V:
    def __init__(self):
        model = word2vec.Word2Vec.load("whole.model")

    @classmethod
    def get_similar_words(target, number):
        results = model.most_similar(positive=[target])[0:number]
        return results


