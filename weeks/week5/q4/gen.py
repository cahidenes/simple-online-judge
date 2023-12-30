import random
print('3 3')
mat = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
for i in range(3):
    for j in range(3):
        if random.randint(0, 1) == 1:
            mat[i][j] ^= 1
            if i > 0:
                mat[i - 1][j] ^= 1
            if i < 2:
                mat[i + 1][j] ^= 1
            if j > 0:
                mat[i][j - 1] ^= 1
            if j < 2:
                mat[i][j + 1] ^= 1
for i in range(3):
    for j in range(3):
        print(mat[i][j], end=' ')
    print()


