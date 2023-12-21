dic = {}
for c in input():
    if c not in dic:
        dic[c] = 0
    dic[c] += 1

for k, v in dic.items():
    print(k, v)
