import requests
import json
import pyperclip

session = requests.Session()
session.get('http://134.122.124.224/loginn?username=cahid&password=cenescenes')
data = session.get('http://134.122.124.224/veriler').json()
data = json.loads(data)
cp = ''
for username, user in data.items():
    if user['show'] == False or username == 'ahmettarik' or username == 'yusufefe' or username == 'muhammedakif':
        continue
    print(user['fullname'],end='\t')
    cp += user['fullname']+'\t'
    l = []
    for week in range(5):
        for q in range(10):
            p = 0
            p += 1 if q in user['solved'][week] else 0
            p += 1 if (q in user['intime'][week] or (p and week in [0, 4] and q < 5)) else 0
            if p and week == 3 and q == 4:
                p += 3
            l.append(p)
    for q in range(10):
        p = 3 if  q in user['solved'][5] else 0
        l.append(p)
    l.append(user['golf'])
    l = [str(x) for x in l]

    print(*l, sep='\t')
    cp += '\t'.join(l) + '\n'

pyperclip.copy(cp)
