from BayesianDBManager import DBManager
from BayesianFilter import BayesianFilter
from sklearn.model_selection import train_test_split
import numpy

bf = BayesianFilter()

DBManager()
DBManager.reset_test_data_division()
original_set = numpy.array(DBManager.selectClassifiedData())

train_set, test_set = train_test_split(original_set, test_size=0.2)

print("size of (train, test) :", len(train_set), len(test_set))
# train
for row in train_set:
    bf.fit(row[0], row[1])

# test
accuracy = 0
for row in test_set:
    pre, scorelist = bf.predict(row[0])
    DBManager.updateAt(row[0], pre)
    if row[1] == pre:
        accuracy += 1
    else:
        print(row[0], pre, row[1])
print("정확도:", str(accuracy / len(test_set)))
