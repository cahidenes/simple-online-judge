import random
print('10 10')
mat = [[0 for i in range(10)] for j in range(10)]
for i in range(10):
    for j in range(10):
        if random.randint(0, 1) == 1:
            mat[i][j] ^= 1
            if i > 0:
                mat[i - 1][j] ^= 1
            if i < 9:
                mat[i + 1][j] ^= 1
            if j > 0:
                mat[i][j - 1] ^= 1
            if j < 9:
                mat[i][j + 1] ^= 1
for i in range(10):
    for j in range(10):
        print(mat[i][j], end=' ')
    print()


