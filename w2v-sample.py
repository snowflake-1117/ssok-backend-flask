import Word2Vec

w2v = Word2Vec.W2V()
results = w2v.get_similar_words("수강", 4)

print(results[1])

results2 = w2v.get_similar_words("조회", 4)

print(results2[2])