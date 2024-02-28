# from tmpcode import topla
import random
import os
os.system('rm yapistir.txt')

mat = [[str(random.randint(10, 99)) for _ in range(random.rantint(8, 12))] for _ in range(5, 20)]

with open('kopyala.txt', 'w') as f:
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            f.write(mat[i][j] + '\t')
        f.write('\n')

with open('kopyala.txt') as f:
    soru = f.read()

import tmpcode

try:
    with open('yapistir.txt') as f:
        file = f.read().strip()
except:
    print('yapistir.txt diye bir dosya açmamışsın')
    exit(1)

ans = ''
for i in range(len(mat)-1, -1, -1):
    for j in range(len(mat[j]-1, -1, -1)):
        ans += mat[i][j] + '\t'
    ans += '\n'
ans.strip()
if ans == file:
    exit(0)
else:
    print('Soru:')
    print(soru)
    print('Beklenen Cevap:')
    print(ans)
    print('Senin Cevap:')
    print(file)
    exit(1)
