from DBManager import DBManager
from bayes import BayesianFilter
import csv
bf = BayesianFilter()

DBManager()
rows = DBManager.selectExceptNotice()
for row in rows:
    bf.fit(row[0], row[1])

rows = DBManager.selectNotice()
equals = 0
with open('NaivesBayes.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
                           # quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Title',  'Division'])
    for row in rows:
            pre, scorelist = bf.predict(row[0])
            filewriter.writerow([row[0], pre])

