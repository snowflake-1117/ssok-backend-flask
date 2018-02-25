from NaiveDBManager_department import DBManager
from bayes import BayesianFilter
import csv
bf = BayesianFilter()

DBManager()
rows = DBManager.selectTrainData()
for row in rows:
    bf.fit(row[0], row[1])

rows = DBManager.selectTestData()
equals = 0
with open('NaivesBayes_departments.csv', mode='w', encoding='utf8') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['Title',  'Division', 'category'])
    for row in rows:
            pre, scorelist = bf.predict(row[0])
            filewriter.writerow([row[0], pre, row[2]])

