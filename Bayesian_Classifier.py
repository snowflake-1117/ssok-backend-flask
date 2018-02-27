from NaiveDBManager_department import DBManager
from BayesianFilter import BayesianFilter
import csv

bf = BayesianFilter()

DBManager()
train_set = DBManager.selectTrainData()
for row in train_set:
    bf.fit(row[0], row[1])

test_set = DBManager.selectTestData()
equals = 0

def conTainsQuotes(title):
    return "\'" in title or "\"" in title

for row in test_set:
    pre, scorelist = bf.predict(row[0])
    row[0].replace("\'", "\'\'")
    row[0].replace("\"", "\"\"")
    DBManager.updateAt(row[0], pre)
