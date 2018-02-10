from DBManager import DBManager
from bayes import BayesianFilter
import csv
bf = BayesianFilter()

DBManager()
rows = DBManager.selectEach20()
for row in rows:
    bf.fit(row[0], row[1])

rows = DBManager.selectALL()
equals = 0
with open('NaivesBayes.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Title', 'Expected', 'Actual'])
    for row in rows:
            pre, scorelist = bf.predict(row[0])
            filewriter.writerow([row[0], row[1], pre])
            if row[1] == pre :
                print(pre, row[1])
                equals += 1

print("정확도:",str(100*equals/len(rows))+"%")