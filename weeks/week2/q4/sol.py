n, m = input().split()
n = int(n)
m = int(m)
mat = []
for i in range(n):
    mat.append(input().split())

k = int(input())
kelimeler = []
for i in range(k):
    kelimeler.append(input())

for kelime in kelimeler:
    for i in range(n):
        for j in range(m):
            soldansaga = True
            sagdansola = True
            yukaridan = True
            asagidan = True
            for k in range(len(kelime)):
                if j + k >= m or mat[i][j + k] != kelime[k]:
                    soldansaga = False
                if j - k < 0 or mat[i][j - k] != kelime[k]:
                    sagdansola = False
                if i + k >= n or mat[i + k][j] != kelime[k]:
                    yukaridan = False
                if i - k < 0 or mat[i - k][j] != kelime[k]:
                    asagidan = False
            for k in range(len(kelime)):
                if soldansaga:
                    mat[i][j + k] = ''
                if sagdansola:
                    mat[i][j - k] = ''
                if yukaridan:
                    mat[i + k][j] = ''
                if asagidan:
                    mat[i - k][j] = ''

sonuc = ''
for i in range(n):
    for j in range(m):
        sonuc += mat[i][j]

print(sonuc)



