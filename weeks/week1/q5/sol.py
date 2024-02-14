asallar = [2, 3, 5, 7, 11, 13, 17, 19]
listem = []
for p in asallar:
    for q in asallar:
        for r in asallar:
            listem.append(p**2 + q**3 + r**4)

listem.sort()
print(listem[int(input())-1])

