import json
from pprint import pprint

data = json.load(open('wiz_departments.json'))

# pprint(data)

print('url개수 : ',len(data))
for count in range(0,len(data)):
    print(str(count))
    print('college:',data[count]['college'])
    print('department:', data[count]['department'])
    print('domain_name:', data[count]['domain_name'])
    print('home_id:', data[count]['home_id'])
    print('handle:', data[count]['handle'])
#"college":"문과대학","department":"한국어문학부","domain_name":"korean","home_id":"korean","handle":1
exit()