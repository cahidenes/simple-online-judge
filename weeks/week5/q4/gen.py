import random
print('4 4')
mat = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
for i in range(4):
    for j in range(4):
        if random.randint(0, 1) == 1:
            mat[i][j] ^= 1
            if i > 0:
                mat[i - 1][j] ^= 1
            if i < 3:
                mat[i + 1][j] ^= 1
            if j > 0:
                mat[i][j - 1] ^= 1
            if j < 3:
                mat[i][j + 1] ^= 1
for i in range(4):
    for j in range(4):
        print(mat[i][j], end=' ')
    print()


