import json
from pprint import pprint

data = json.load(open('wiz_departments.json'))

pprint(data)

print('url개수 : ',len(data))
#print(data[0]['college'])
exit()