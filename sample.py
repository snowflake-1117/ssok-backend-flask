from gensim.models import word2vec
model = word2vec.Word2Vec.load("whole.model")
results = model.most_similar(positive=["수강"])[0:4]
