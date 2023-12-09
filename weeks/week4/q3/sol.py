l = input().split()

for i in range(len(l)):
    l[i] = int(l[i])

hedef = int(input())

from itertools import combinations

buldum = False
for a, b, c in combinations(l, 3):
    if a+b+c == hedef:
        print(a, b, c, sep='+')
        buldum = True

if not buldum:
    print("YOK")

