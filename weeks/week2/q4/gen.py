import random
alf = 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ'

while True:
    try:
        n = random.randint(3, 6)
        m = random.randint(3, 6)
        mat = []
        for i in range(n):
            mat.append([])
            for j in range(m):
                mat[-1].append(random.choice(alf))
        birlesik = ''
        for i in range(n):
            for j in range(m):
                birlesik += mat[i][j]
        for j in range(m):
            for i in range(n):
                birlesik += mat[i][j]
        birlesik += birlesik[::-1]
        k = random.randint(4, 9)
        kelimeler = []
        sil = [x.copy() for x in mat]
        for _ in range(k):
            leng = random.randint(3, 7)
            kelime = ''
            yon = random.randint(0, 3)
            if yon == 1:
                kelimebasi = random.randint(0, n-leng-1)
                kelimebasj = random.randint(0, m-1)
            elif yon == 2:
                kelimebasi = random.randint(leng, n-1)
                kelimebasj = random.randint(0, m-1)
            elif yon == 3:
                kelimebasi = random.randint(0, n-1)
                kelimebasj = random.randint(0, m-1-leng)
            elif yon == 4:
                kelimebasi = random.randint(0, n-1)
                kelimebasj = random.randint(leng, m-1)
            for s in range(leng):
                if yon == 1:
                    kelime += sil[kelimebasi+s][kelimebasj]
                    sil[kelimebasi+s][kelimebasj] = ' '
                elif yon == 2:
                    kelime += sil[kelimebasi-s][kelimebasj]
                    sil[kelimebasi-s][kelimebasj] = ' '
                elif yon == 3:
                    kelime += sil[kelimebasi][kelimebasj+s]
                    sil[kelimebasi][kelimebasj+s] = ' '
                elif yon == 4:
                    kelime += sil[kelimebasi][kelimebasj-s]
                    sil[kelimebasi][kelimebasj-s] = ' '
            if ' ' in kelime:
                break
            if birlesik.count(kelime) != 1:
                break
            kelimeler.append(kelime)
        else:
            break
    except:
        pass

print(n, m)
for i in range(n):
    for j in range(m):
        print(mat[i][j], end=' ')
    print()
print(k)
for i in range(k):
    print(kelimeler[i])






