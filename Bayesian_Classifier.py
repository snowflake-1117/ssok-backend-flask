from BayesianDBManager import DBManager
from BayesianFilter import BayesianFilter

bf = BayesianFilter()

DBManager()
classified_set = DBManager.selectClassifiedData()
for row in classified_set:
    bf.fit(row[0], row[1])

unclassified_set = DBManager.selectUnclassifiedData()

for row in unclassified_set:
    pre, scorelist = bf.predict(row[0])
    DBManager.updateAt(row[0], pre)