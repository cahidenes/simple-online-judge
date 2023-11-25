p = input().split()
f = {}
for kelime in p:
    if kelime in f:
        f[kelime] += 1
    else:
        f[kelime] = 1

kelimeler = []
for kelime in f:
    kelimeler.append((f[kelime], kelime))
kelimeler.sort(reverse=True)
print(kelimeler[0][1], kelimeler[0][0])
