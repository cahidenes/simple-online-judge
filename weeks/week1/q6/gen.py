import random
print('9 9')
mat = [[0 for i in range(9)] for j in range(9)]
for i in range(9):
    for j in range(9):
        if random.randint(0, 1) == 1:
            mat[i][j] ^= 1
            if i > 0:
                mat[i - 1][j] ^= 1
            if i < 8:
                mat[i + 1][j] ^= 1
            if j > 0:
                mat[i][j - 1] ^= 1
            if j < 8:
                mat[i][j + 1] ^= 1
for i in range(9):
    for j in range(9):
        print(mat[i][j], end=' ')
    print()


